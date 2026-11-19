"""
pipeline.py - Unified BharatSpectral Deterministic Hyperspectral Diagnostic Engine

Executes end-to-end physical spectroscopy pipeline on 1D spectral vectors
and 3D spatial-spectral cubes:
1. Atmospheric Absorption Masking (AAM) & radiometric clamping
2. Narrowband hyperspectral indices (NDRE, PRI, WBI, NDTI, MTCI, NDVI, CAI)
3. Convex hull continuum removal & targeted absorption diagnostics
4. Fully Constrained Linear Spectral Unmixing (FCLS / LSU)
5. Spectral Angle Mapper (SAM) classification & material matching

Maintains strict schema parity with the Cloudflare Worker engine JSON contract
(Section 3 of plans/deterministic_hyperspectral_engine_plan.md).
"""

from dataclasses import dataclass, asdict, field
from typing import Dict, List, Tuple, Sequence, Optional, Union, Any
import json
import os
import sys
import time
import argparse
import logging
import numpy as np

from src.gis_spectroscopy.wavelength_utils import (
    DEFAULT_AAM_WINDOWS,
    SENSOR_METADATA,
    is_band_masked,
    get_valid_band_indices,
    clamp_reflectance,
    resample_spectrum,
)
from src.gis_spectroscopy.indices import (
    NarrowbandIndices,
    compute_narrowband_indices,
    compute_cube_indices,
)
from src.gis_spectroscopy.continuum_removal import (
    ContinuumDiagnostics,
    ContinuumRemovalResult,
    compute_continuum_diagnostics,
    compute_cube_continuum_diagnostics,
)
from src.gis_spectroscopy.linear_unmixing import (
    SubpixelAbundances,
    compute_standard_subpixel_abundances,
    compute_cube_unmixing,
    solve_fcls_pgd,
)
from src.gis_spectroscopy.sam_classifier import (
    SamCandidate,
    SamClassification,
    compute_sam_classification,
    compute_cube_sam,
)
from src.gis_spectroscopy.endmember_vca import load_reference_library

logger = logging.getLogger("BharatSpectral.Engine")


@dataclass
class SensorMetadataPayload:
    name: str
    platform: str
    total_bands: int
    valid_bands_used: int
    wavelength_range_nm: List[float]
    ground_sampling_distance_m: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "platform": self.platform,
            "total_bands": int(self.total_bands),
            "valid_bands_used": int(self.valid_bands_used),
            "wavelength_range_nm": [float(self.wavelength_range_nm[0]), float(self.wavelength_range_nm[1])],
            "ground_sampling_distance_m": float(self.ground_sampling_distance_m),
        }


@dataclass
class CoordinateMetadataPayload:
    latitude: float
    longitude: float
    agro_ecological_zone: str
    flightline_id: str = ""
    flightline_name: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "agro_ecological_zone": self.agro_ecological_zone,
        }
        if self.flightline_id:
            d["flightline_id"] = self.flightline_id
        if self.flightline_name:
            d["flightline_name"] = self.flightline_name
        return d


@dataclass
class SpectralCurvePayload:
    wavelengths: List[float]
    reflectance: List[float]
    hull_reflectance: List[float]
    continuum_removed: List[float]
    masked_windows: List[List[float]]
    reference_curves: Optional[Dict[str, List[float]]] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "wavelengths": [float(w) for w in self.wavelengths],
            "reflectance": [float(r) for r in self.reflectance],
            "hull_reflectance": [float(h) for h in self.hull_reflectance],
            "continuum_removed": [float(cr) for cr in self.continuum_removed],
            "masked_windows": [[float(w[0]), float(w[1])] for w in self.masked_windows],
        }
        if self.reference_curves is not None:
            d["reference_curves"] = {
                k: [float(v) for v in vals] for k, vals in self.reference_curves.items()
            }
        return d


@dataclass
class DiagnosticPayload:
    """
    Unified JSON Output Schema conforming strictly to Section 3 of
    plans/deterministic_hyperspectral_engine_plan.md
    """
    sensor: SensorMetadataPayload
    coordinates: CoordinateMetadataPayload
    spectral_curve: SpectralCurvePayload
    narrowband_indices: NarrowbandIndices
    continuum_diagnostics: ContinuumDiagnostics
    subpixel_abundances: SubpixelAbundances
    sam_classification: SamClassification

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sensor": self.sensor.to_dict(),
            "coordinates": self.coordinates.to_dict(),
            "spectral_curve": self.spectral_curve.to_dict(),
            "narrowband_indices": self.narrowband_indices.to_dict(),
            "continuum_diagnostics": self.continuum_diagnostics.to_dict(),
            "subpixel_abundances": self.subpixel_abundances.to_dict(),
            "sam_classification": self.sam_classification.to_dict(),
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


class HyperspectralDiagnosticEngine:
    """
    BharatSpectral Deterministic Physical Spectroscopy Engine.
    Executes physical algorithms over 1D spectral vectors and 3D data cubes.
    """

    def __init__(
        self,
        endmembers_library_path: Optional[str] = None,
        masked_windows: Sequence[Tuple[float, float]] = DEFAULT_AAM_WINDOWS
    ):
        self.masked_windows = list(masked_windows)
        self.reference_library = load_reference_library(endmembers_library_path)
        self._build_endmember_cache()

    def _build_endmember_cache(self):
        """
        Extracts endmember arrays for fast FCLS unmixing and reference curves.
        """
        self.raw_endmembers_dict: Dict[str, List[float]] = {}
        for ref in self.reference_library:
            self.raw_endmembers_dict[ref["id"]] = ref["reflectance"]

        # Default endmember wavelengths (425 bands)
        self.library_wavelengths = np.linspace(380.0, 2510.0, 425)
        self._resampled_cache: Dict[Tuple[int, float, float], Dict[str, np.ndarray]] = {}

    def _get_resampled_endmembers(self, target_wavelengths: Sequence[float]) -> Dict[str, np.ndarray]:
        """
        Resamples endmembers library to match sensor wavelengths, caching by wavelength signature.
        """
        tgt_w = np.asarray(target_wavelengths, dtype=np.float64)
        cache_key = (len(tgt_w), float(tgt_w[0]), float(tgt_w[-1]))
        if cache_key in self._resampled_cache:
            return self._resampled_cache[cache_key]

        resampled = {}
        for k, v in self.raw_endmembers_dict.items():
            if len(v) == len(tgt_w) and np.allclose(self.library_wavelengths[:len(tgt_w)], tgt_w, atol=0.1):
                resampled[k] = np.asarray(v, dtype=np.float64)
            else:
                resampled[k] = resample_spectrum(self.library_wavelengths, np.asarray(v, dtype=np.float64), tgt_w)

        self._resampled_cache[cache_key] = resampled
        return resampled

    def analyze_pixel(
        self,
        wavelengths: Sequence[float],
        reflectance: Sequence[float],
        sensor_name: str = "AVIRIS-NG India",
        latitude: float = 21.1458,
        longitude: float = 79.0882,
        agro_ecological_zone: str = "Deccan Plateau (Rainfed Cotton-Soybean)",
        flightline_id: str = "",
        flightline_name: str = "",
        ground_sampling_distance_m: Optional[float] = None,
        continuum_mode: str = "hull"
    ) -> DiagnosticPayload:
        """
        Executes end-to-end deterministic spectroscopy analysis on a single pixel.
        Returns a typed DiagnosticPayload conforming to Section 3.
        """
        wls = np.asarray(wavelengths, dtype=np.float64)
        raw_r = np.asarray(reflectance, dtype=np.float64)

        if len(wls) != len(raw_r):
            raise ValueError(f"Wavelengths length ({len(wls)}) does not match reflectance length ({len(raw_r)}).")

        # 1. Radiometric Clamping & Atmospheric Masking
        r_clamped = clamp_reflectance(raw_r, 0.0, 1.0)
        valid_indices = get_valid_band_indices(wls, self.masked_windows)
        total_bands = len(wls)
        valid_bands_count = len(valid_indices)

        # 2. Narrowband Hyperspectral Indices
        indices = compute_narrowband_indices(wls, r_clamped, masked_windows=self.masked_windows)

        # 3. Continuum Removal Diagnostics (hull or local shoulder baseline)
        cr_result = compute_continuum_diagnostics(wls, r_clamped, mode=continuum_mode)

        # 4. Endmember Resampling & FCLS Unmixing
        resampled_em = self._get_resampled_endmembers(wls)
        subpixel = compute_standard_subpixel_abundances(
            r_clamped,
            resampled_em,
            valid_band_indices=valid_indices,
            solver="pgd"
        )

        # 5. SAM Material Classification
        sam_references = []
        for ref in self.reference_library:
            r_em = resampled_em.get(ref["id"])
            sam_references.append({
                "id": ref["id"],
                "label": ref.get("label", ref["id"]),
                "reflectance": r_em if r_em is not None else ref["reflectance"]
            })

        sam_result = compute_sam_classification(
            r_clamped,
            sam_references,
            valid_band_indices=valid_indices
        )

        # 6. Build Overlaid Reference Curves (Healthy, Soil, Residue)
        ref_curves = {}
        if "green_healthy_canopy" in resampled_em:
            ref_curves["healthy"] = np.round(resampled_em["green_healthy_canopy"], 4).tolist()
        if "black_cotton_soil" in resampled_em:
            ref_curves["soil"] = np.round(resampled_em["black_cotton_soil"], 4).tolist()
        if "dry_crop_residue" in resampled_em:
            ref_curves["residue"] = np.round(resampled_em["dry_crop_residue"], 4).tolist()

        # Sensor metadata
        sensor_info = SENSOR_METADATA.get(sensor_name, {
            "name": sensor_name,
            "platform": "Airborne" if "AVIRIS" in sensor_name else "Spaceborne",
            "total_bands": total_bands,
            "wavelength_range_nm": [float(wls[0]), float(wls[-1])],
            "ground_sampling_distance_m": ground_sampling_distance_m or 4.8,
        })
        gsd = ground_sampling_distance_m or sensor_info.get("ground_sampling_distance_m", 4.8)

        sensor_meta = SensorMetadataPayload(
            name=sensor_info.get("name", sensor_name),
            platform=sensor_info.get("platform", "Airborne"),
            total_bands=total_bands,
            valid_bands_used=valid_bands_count,
            wavelength_range_nm=[float(wls[0]), float(wls[-1])],
            ground_sampling_distance_m=float(gsd),
        )

        coord_meta = CoordinateMetadataPayload(
            latitude=float(latitude),
            longitude=float(longitude),
            agro_ecological_zone=agro_ecological_zone,
            flightline_id=flightline_id,
            flightline_name=flightline_name,
        )

        curve_payload = SpectralCurvePayload(
            wavelengths=np.round(wls, 2).tolist(),
            reflectance=np.round(r_clamped, 4).tolist(),
            hull_reflectance=cr_result.hull_reflectance.tolist(),
            continuum_removed=cr_result.continuum_removed.tolist(),
            masked_windows=[list(w) for w in self.masked_windows],
            reference_curves=ref_curves if ref_curves else None,
        )

        return DiagnosticPayload(
            sensor=sensor_meta,
            coordinates=coord_meta,
            spectral_curve=curve_payload,
            narrowband_indices=indices,
            continuum_diagnostics=cr_result.diagnostics,
            subpixel_abundances=subpixel,
            sam_classification=sam_result,
        )

    def analyze_cube(
        self,
        wavelengths: Sequence[float],
        cube: np.ndarray,
        sensor_name: str = "AVIRIS-NG India",
        output_file: Optional[str] = None,
        continuum_mode: str = "hull"
    ) -> Dict[str, Any]:
        """
        Executes high-throughput spatial analysis over a 3D hyperspectral cube (H, W, B).
        Returns spatial diagnostic rasters and optionally writes to .npz or GeoTIFF (.tif).
        """
        cube_arr = clamp_reflectance(cube, 0.0, 1.0)
        H, W, B = cube_arr.shape
        wls = np.asarray(wavelengths, dtype=np.float64)

        valid_indices = get_valid_band_indices(wls, self.masked_windows)
        resampled_em = self._get_resampled_endmembers(wls)

        logger.info("Computing cube narrowband indices for shape (%d, %d, %d)...", H, W, B)
        index_maps = compute_cube_indices(wls, cube_arr, masked_windows=self.masked_windows)

        logger.info("Computing cube continuum diagnostics (mode=%s)...", continuum_mode)
        continuum_maps = compute_cube_continuum_diagnostics(wls, cube_arr, mode=continuum_mode)

        logger.info("Computing cube FCLS unmixing...")
        abundance_cube, rmse_map, em_keys = compute_cube_unmixing(
            cube_arr,
            resampled_em,
            valid_band_indices=valid_indices
        )

        logger.info("Computing cube SAM classification...")
        sam_refs = [{"id": k, "label": k, "reflectance": v} for k, v in resampled_em.items()]
        sam_cube_results = compute_cube_sam(cube_arr, sam_refs, valid_band_indices=valid_indices)

        result_bundle = {
            "dimensions": {"rows": H, "cols": W, "bands": B},
            "indices": index_maps,
            "continuum": continuum_maps,
            "abundances": {
                "cube": abundance_cube,
                "endmembers": em_keys,
                "rmse": rmse_map,
            },
            "sam": sam_cube_results,
        }

        if output_file:
            if output_file.endswith(".npz"):
                np.savez_compressed(
                    output_file,
                    abundance_cube=abundance_cube,
                    rmse_map=rmse_map,
                    **index_maps,
                    **continuum_maps
                )
                logger.info("Saved cube analysis rasters to %s", output_file)
            elif output_file.endswith(".tif") or output_file.endswith(".tiff"):
                try:
                    import tifffile
                    # Stack abundance channels and index maps into multi-band TIFF
                    layers = [abundance_cube, rmse_map[..., None]]
                    for k in sorted(index_maps.keys()):
                        layers.append(index_maps[k][..., None])
                    stacked = np.concatenate(layers, axis=-1).astype(np.float32)
                    tifffile.imwrite(output_file, stacked, photometric='minisblack')
                    logger.info("Saved multi-band GeoTIFF (%d channels) to %s", stacked.shape[-1], output_file)
                except Exception as e:
                    logger.warning("Failed to save GeoTIFF raster: %s", e)

        return result_bundle


def main():
    parser = argparse.ArgumentParser(description="BharatSpectral Deterministic Hyperspectral Pipeline CLI")
    parser.add_argument("--flightline", type=str, help="Path to seed flightline JSON file")
    parser.add_argument("--row", type=int, default=0, help="Row index for single-pixel inspection")
    parser.add_argument("--col", type=int, default=0, help="Col index for single-pixel inspection")
    parser.add_argument("--output", type=str, help="Output JSON path")
    parser.add_argument("--benchmark", action="store_true", help="Run latency benchmark on flightline pixels")

    args = parser.parse_args()
    engine = HyperspectralDiagnosticEngine()

    if args.flightline:
        with open(args.flightline, "r", encoding="utf-8") as f:
            data = json.load(f)

        wavelengths = data["wavelengths"]
        pixels = data["pixels"]
        grid = data.get("grid", {"rows": 20, "cols": 20})

        target_pixel = None
        for p in pixels:
            if p["row"] == args.row and p["col"] == args.col:
                target_pixel = p
                break
        if not target_pixel:
            target_pixel = pixels[0]

        payload = engine.analyze_pixel(
            wavelengths=wavelengths,
            reflectance=target_pixel["reflectance"],
            sensor_name=data.get("sensor", "AVIRIS-NG India"),
            latitude=target_pixel.get("lat", 21.1458),
            longitude=target_pixel.get("lon", 79.0882),
            agro_ecological_zone=data.get("agro_zone", "Indian Agroecosystem"),
            flightline_id=data.get("id", ""),
            flightline_name=data.get("name", ""),
            ground_sampling_distance_m=data.get("gsd_m", 4.8),
        )

        out_json = payload.to_json(indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(out_json)
            print(f"Diagnostic payload saved to {args.output}")
        else:
            print(out_json[:500] + "\n... [truncated]")

        if args.benchmark:
            n_samples = min(100, len(pixels))
            start_t = time.perf_counter()
            for i in range(n_samples):
                p = pixels[i]
                _ = engine.analyze_pixel(
                    wavelengths=wavelengths,
                    reflectance=p["reflectance"],
                    sensor_name=data.get("sensor", "AVIRIS-NG India")
                )
            elapsed = (time.perf_counter() - start_t) * 1000.0 / n_samples
            print(f"Benchmark: {n_samples} pixels evaluated, avg latency: {elapsed:.2f} ms/pixel")
    else:
        # Default self-test with AVIRIS wavelengths
        wls = np.linspace(380.0, 2510.0, 425)
        spec = np.clip(0.05 + 0.35 / (1.0 + np.exp(-(wls - 720) / 15)), 0.0, 1.0)
        payload = engine.analyze_pixel(wls, spec)
        print("Hyperspectral Diagnostic Engine self-test successful:")
        print(payload.to_json()[:400] + "...")


if __name__ == "__main__":
    main()
