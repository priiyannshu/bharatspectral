"""
indices.py - Narrowband Hyperspectral Indices Suite

Computes biophysical and biochemical indices from high-resolution spectral vectors
and 3D spatial-spectral cubes without broadband saturation:
- NDRE (Normalized Difference Red Edge): Chlorophyll & nitrogen proxy
- PRI (Photochemical Reflectance Index): Photosynthetic radiation-use efficiency
- WBI (Water Band Index): Canopy water content
- NDTI (Normalized Difference Tillage Index): Dry residue vs soil differentiation
- MTCI (MERIS Terrestrial Chlorophyll Index): Chlorophyll concentration
- NDVI (Normalized Difference Vegetation Index): Standard baseline
- CAI (Cellulose Absorption Index): Dry residue & stubble biomass
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Sequence, Optional, Union, Callable, Tuple, List
import numpy as np

from src.gis_spectroscopy.wavelength_utils import get_reflectance_at, is_band_masked


@dataclass
class NarrowbandIndices:
    """
    Standard typed container for narrowband hyperspectral indices.
    Matches exact schema required by Section 3 of the specification.
    """
    ndre: float
    pri: float
    wbi: float
    ndti: float
    mtci: float
    ndvi: Optional[float] = None
    cai: Optional[float] = None
    masked_flags: Optional[Dict[str, bool]] = None

    def to_dict(self, include_extended: bool = False) -> Dict[str, Any]:
        """
        Serializes to JSON-compatible dictionary. By default adheres strictly
        to the 5-index schema contract in Section 3 of the plan.
        """
        d: Dict[str, Any] = {
            "ndre": float(self.ndre),
            "pri": float(self.pri),
            "wbi": float(self.wbi),
            "ndti": float(self.ndti),
            "mtci": float(self.mtci),
        }
        if include_extended:
            if self.ndvi is not None:
                d["ndvi"] = float(self.ndvi)
            if self.cai is not None:
                d["cai"] = float(self.cai)
            if self.masked_flags is not None:
                d["masked_flags"] = dict(self.masked_flags)
        return d


@dataclass
class IndexDefinition:
    name: str
    description: str
    required_wavelengths: Sequence[float]
    compute_fn: Callable[..., Union[float, np.ndarray]]
    biochemical_diagnostic: str

    def is_masked(self, windows: Sequence[Tuple[float, float]] = ()) -> bool:
        """Returns True if any required wavelength for this index falls inside atmospheric masking windows."""
        from src.gis_spectroscopy.wavelength_utils import DEFAULT_AAM_WINDOWS
        w = windows if len(windows) > 0 else DEFAULT_AAM_WINDOWS
        return any(is_band_masked(wl, w) for wl in self.required_wavelengths)

    def get_masked_bands(self, windows: Sequence[Tuple[float, float]] = ()) -> List[float]:
        """Returns list of required wavelengths that fall inside atmospheric masking windows."""
        from src.gis_spectroscopy.wavelength_utils import DEFAULT_AAM_WINDOWS
        w = windows if len(windows) > 0 else DEFAULT_AAM_WINDOWS
        return [wl for wl in self.required_wavelengths if is_band_masked(wl, w)]


INDEX_REGISTRY: Dict[str, IndexDefinition] = {}


def register_index(
    name: str,
    description: str,
    required_wavelengths: Sequence[float],
    biochemical_diagnostic: str = ""
):
    """
    Decorator to register an index function in the global index registry.
    """
    def decorator(fn: Callable[..., Union[float, np.ndarray]]):
        INDEX_REGISTRY[name] = IndexDefinition(
            name=name,
            description=description,
            required_wavelengths=required_wavelengths,
            compute_fn=fn,
            biochemical_diagnostic=biochemical_diagnostic
        )
        return fn
    return decorator


@register_index(
    name="ndre",
    description="Normalized Difference Red Edge: (R790 - R720) / (R790 + R720)",
    required_wavelengths=[720.0, 790.0],
    biochemical_diagnostic="Sensitive to mid-to-high canopy chlorophyll and nitrogen where NDVI saturates."
)
def compute_ndre(r_map: Dict[float, Union[float, np.ndarray]]) -> Union[float, np.ndarray]:
    r790 = r_map[790.0]
    r720 = r_map[720.0]
    denom = r790 + r720
    if np.isscalar(denom):
        return (r790 - r720) / denom if denom != 0 else 0.0
    safe_denom = np.where(denom == 0, 1e-6, denom)
    return np.where(denom == 0, 0.0, (r790 - r720) / safe_denom)


@register_index(
    name="pri",
    description="Photochemical Reflectance Index: (R531 - R570) / (R531 + R570)",
    required_wavelengths=[531.0, 570.0],
    biochemical_diagnostic="Reversible xanthophyll cycle epoxidation; tracks photosynthetic light-use efficiency."
)
def compute_pri(r_map: Dict[float, Union[float, np.ndarray]]) -> Union[float, np.ndarray]:
    r531 = r_map[531.0]
    r570 = r_map[570.0]
    denom = r531 + r570
    if np.isscalar(denom):
        return (r531 - r570) / denom if denom != 0 else 0.0
    safe_denom = np.where(denom == 0, 1e-6, denom)
    return np.where(denom == 0, 0.0, (r531 - r570) / safe_denom)


@register_index(
    name="wbi",
    description="Water Band Index: R900 / R970",
    required_wavelengths=[900.0, 970.0],
    biochemical_diagnostic="Tracks liquid water absorption within plant cell vacuoles."
)
def compute_wbi(r_map: Dict[float, Union[float, np.ndarray]]) -> Union[float, np.ndarray]:
    r900 = r_map[900.0]
    r970 = r_map[970.0]
    if np.isscalar(r970):
        return r900 / r970 if r970 > 0.001 else 1.0
    safe_denom = np.where(r970 > 0.001, r970, 1e-6)
    return np.where(r970 > 0.001, r900 / safe_denom, 1.0)


@register_index(
    name="ndti",
    description="Normalized Difference Tillage Index: (R1660 - R2330) / (R1660 + R2330)",
    required_wavelengths=[1660.0, 2330.0],
    biochemical_diagnostic="Differentiates dry combustible crop residue from bare soil."
)
def compute_ndti(r_map: Dict[float, Union[float, np.ndarray]]) -> Union[float, np.ndarray]:
    r1660 = r_map[1660.0]
    r2330 = r_map[2330.0]
    denom = r1660 + r2330
    if np.isscalar(denom):
        return (r1660 - r2330) / denom if denom != 0 else 0.0
    safe_denom = np.where(denom == 0, 1e-6, denom)
    return np.where(denom == 0, 0.0, (r1660 - r2330) / safe_denom)


@register_index(
    name="mtci",
    description="MERIS Terrestrial Chlorophyll Index: (R753 - R708) / (R708 - R681)",
    required_wavelengths=[681.0, 708.0, 753.0],
    biochemical_diagnostic="Red-edge inflection proxy sensitive to high canopy chlorophyll and cellular senescence."
)
def compute_mtci(r_map: Dict[float, Union[float, np.ndarray]]) -> Union[float, np.ndarray]:
    r681 = r_map[681.0]
    r708 = r_map[708.0]
    r753 = r_map[753.0]
    denom = r708 - r681
    if np.isscalar(denom):
        val = (r753 - r708) / denom if abs(denom) > 0.001 else 1.0
        return float(np.clip(val, -5.0, 10.0))
    safe_denom = np.where(np.abs(denom) > 0.001, denom, 1e-6)
    val = np.where(np.abs(denom) > 0.001, (r753 - r708) / safe_denom, 1.0)
    return np.clip(val, -5.0, 10.0)


@register_index(
    name="ndvi",
    description="Normalized Difference Vegetation Index: (R800 - R670) / (R800 + R670)",
    required_wavelengths=[670.0, 800.0],
    biochemical_diagnostic="General green canopy biomass and vegetative vigor."
)
def compute_ndvi(r_map: Dict[float, Union[float, np.ndarray]]) -> Union[float, np.ndarray]:
    r800 = r_map[800.0]
    r670 = r_map[670.0]
    denom = r800 + r670
    if np.isscalar(denom):
        return (r800 - r670) / denom if denom != 0 else 0.0
    safe_denom = np.where(denom == 0, 1e-6, denom)
    return np.where(denom == 0, 0.0, (r800 - r670) / safe_denom)


@register_index(
    name="cai",
    description="Cellulose Absorption Index: 0.5 * (R2000 + R2200) - R2100",
    required_wavelengths=[2000.0, 2100.0, 2200.0],
    biochemical_diagnostic="Deep absorption at 2100nm from cellulose/lignin in dry post-harvest residue."
)
def compute_cai(r_map: Dict[float, Union[float, np.ndarray]]) -> Union[float, np.ndarray]:
    r2000 = r_map[2000.0]
    r2100 = r_map[2100.0]
    r2200 = r_map[2200.0]
    return 0.5 * (r2000 + r2200) - r2100


def compute_narrowband_indices(
    wavelengths: Sequence[float],
    reflectance: np.ndarray,
    round_decimals: int = 3,
    masked_windows: Optional[Sequence[Tuple[float, float]]] = None
) -> NarrowbandIndices:
    """
    Computes all standard narrowband indices for a single 1D reflectance spectrum.
    Wavelengths are interpolated linearly to exact target values.
    Optionally flags indices that have bands in atmospheric absorption windows.
    """
    r_arr = np.asarray(reflectance, dtype=np.float64)
    if r_arr.ndim != 1:
        raise ValueError("compute_narrowband_indices expects a 1D reflectance vector.")

    # Target wavelengths needed across all indices
    needed_wls = [531.0, 570.0, 670.0, 681.0, 708.0, 720.0, 753.0, 790.0, 800.0, 900.0, 970.0, 1660.0, 2000.0, 2100.0, 2200.0, 2330.0]
    r_map = {wl: get_reflectance_at(wavelengths, r_arr, wl) for wl in needed_wls}

    ndre = float(compute_ndre(r_map))
    pri = float(compute_pri(r_map))
    wbi = float(compute_wbi(r_map))
    ndti = float(compute_ndti(r_map))
    mtci = float(compute_mtci(r_map))
    ndvi = float(compute_ndvi(r_map))
    cai = float(compute_cai(r_map))

    from src.gis_spectroscopy.wavelength_utils import DEFAULT_AAM_WINDOWS
    mw = masked_windows if masked_windows is not None else DEFAULT_AAM_WINDOWS
    masked_flags = {
        name: idx_def.is_masked(mw)
        for name, idx_def in INDEX_REGISTRY.items()
    }

    return NarrowbandIndices(
        ndre=round(ndre, round_decimals),
        pri=round(pri, round_decimals),
        wbi=round(wbi, round_decimals),
        ndti=round(ndti, round_decimals),
        mtci=round(mtci, 2),
        ndvi=round(ndvi, round_decimals),
        cai=round(cai, 4),
        masked_flags=masked_flags,
    )


def compute_cube_indices(
    wavelengths: Sequence[float],
    cube: np.ndarray,
    indices: Optional[Sequence[str]] = None,
    masked_windows: Optional[Sequence[Tuple[float, float]]] = None
) -> Dict[str, np.ndarray]:
    """
    Computes spatial index maps for a 3D hyperspectral cube (H, W, B).
    Returns a dictionary of 2D numpy arrays {index_name: ndarray(H, W)}.
    """
    cube_arr = np.asarray(cube, dtype=np.float64)
    if cube_arr.ndim != 3:
        raise ValueError("compute_cube_indices expects a 3D array (H, W, B).")

    requested = indices or ["ndre", "pri", "wbi", "ndti", "mtci", "ndvi", "cai"]

    # Gather all required wavelengths for requested indices
    needed_wls = set()
    for name in requested:
        if name in INDEX_REGISTRY:
            for wl in INDEX_REGISTRY[name].required_wavelengths:
                needed_wls.add(wl)

    # Pre-extract interpolated bands for each required wavelength across the entire cube
    r_map: Dict[float, np.ndarray] = {}
    for wl in needed_wls:
        r_map[wl] = get_reflectance_at(wavelengths, cube_arr, wl)

    result_maps = {}
    for name in requested:
        if name in INDEX_REGISTRY:
            res = INDEX_REGISTRY[name].compute_fn(r_map)
            result_maps[name] = np.asarray(res, dtype=np.float32)

    return result_maps


if __name__ == "__main__":
    wls = np.linspace(400.0, 2400.0, 425)
    dummy_r = np.full(425, 0.3)
    sample_idx = compute_narrowband_indices(wls, dummy_r)
    print("Narrowband Indices module verified:", sample_idx.to_dict())

