"""
wavelength_utils.py - Wavelength Alignment & Atmospheric Absorption Masking (AAM)

Provides physical atmospheric masking, radiometric calibration clamping,
and high-precision band interpolation across sensor bandsets:
- AVIRIS-NG India (425 bands, 380–2510 nm, Airborne)
- NASA EMIT (285 bands, 381–2493 nm, Spaceborne ISS)
- ISRO HysIS (64 VNIR + 256 SWIR = 320 bands, Spaceborne)
- Sentinel-2 MSI (12/13 bands, Spaceborne)
"""

from typing import List, Tuple, Sequence, Optional, Union, Dict, Any
import numpy as np

# Standard Atmospheric Absorption Masking (AAM) windows (water vapor & CO2)
# Window 1: 1350 - 1440 nm (can extend to 1450 nm)
# Window 2: 1800 - 1950 nm
DEFAULT_AAM_WINDOWS: List[Tuple[float, float]] = [
    (1350.0, 1440.0),
    (1800.0, 1950.0),
]

# Standard Sensor Reference Grids
AVIRIS_NG_WAVELENGTHS = np.round(np.linspace(380.0, 2510.0, 425), 2)
EMIT_WAVELENGTHS = np.round(np.linspace(381.0, 2493.0, 285), 2)
HYSIS_VNIR_WAVELENGTHS = np.round(np.linspace(400.0, 950.0, 64), 2)
HYSIS_SWIR_WAVELENGTHS = np.round(np.linspace(900.0, 2500.0, 256), 2)
HYSIS_WAVELENGTHS = np.unique(np.concatenate([HYSIS_VNIR_WAVELENGTHS, HYSIS_SWIR_WAVELENGTHS]))
SENTINEL2_WAVELENGTHS = np.array([
    443.0, 490.0, 560.0, 665.0, 705.0, 740.0, 783.0, 842.0, 865.0, 945.0, 1610.0, 2190.0
], dtype=np.float64)

SENSOR_METADATA: Dict[str, Dict[str, Any]] = {
    "AVIRIS-NG India": {
        "name": "AVIRIS-NG India",
        "platform": "Airborne",
        "total_bands": 425,
        "wavelength_range_nm": [380.0, 2510.0],
        "ground_sampling_distance_m": 4.8,
        "nominal_fwhm_nm": 5.0,
    },
    "NASA EMIT": {
        "name": "NASA EMIT",
        "platform": "Spaceborne (ISS)",
        "total_bands": 285,
        "wavelength_range_nm": [381.0, 2493.0],
        "ground_sampling_distance_m": 60.0,
        "nominal_fwhm_nm": 7.4,
    },
    "ISRO HysIS": {
        "name": "ISRO HysIS",
        "platform": "Spaceborne",
        "total_bands": 320,
        "wavelength_range_nm": [400.0, 2500.0],
        "ground_sampling_distance_m": 30.0,
        "nominal_fwhm_nm": 10.0,
    },
    "Sentinel-2 MSI": {
        "name": "Sentinel-2 MSI",
        "platform": "Spaceborne",
        "total_bands": 12,
        "wavelength_range_nm": [443.0, 2190.0],
        "ground_sampling_distance_m": 10.0,
        "nominal_fwhm_nm": 20.0,
    },
}


def is_band_masked(wavelength: float, windows: Sequence[Tuple[float, float]] = DEFAULT_AAM_WINDOWS) -> bool:
    """
    Returns True if the given wavelength falls inside any atmospheric absorption window.
    """
    for start, end in windows:
        if start <= wavelength <= end:
            return True
    return False


def get_valid_band_indices(
    wavelengths: Sequence[float],
    windows: Sequence[Tuple[float, float]] = DEFAULT_AAM_WINDOWS
) -> np.ndarray:
    """
    Returns array of 0-based indices corresponding to clean (unmasked) spectral bands.
    """
    valid = [i for i, wl in enumerate(wavelengths) if not is_band_masked(wl, windows)]
    return np.array(valid, dtype=int)


def clamp_reflectance(
    reflectance: np.ndarray,
    min_val: float = 0.0,
    max_val: float = 1.0
) -> np.ndarray:
    """
    Clamps radiometric reflectance values to physically meaningful bounds [min_val, max_val].
    Negative values arise from dark current subtraction or calibration artifacts.
    Values > 1.0 represent specular reflectance or edge anomalies.
    NaN and infinite values from corrupted sensor pixels are safely neutralized.
    """
    arr = np.asarray(reflectance, dtype=np.float64)
    clean = np.nan_to_num(arr, nan=min_val, posinf=max_val, neginf=min_val)
    return np.clip(clean, min_val, max_val)


def find_closest_band_index(wavelengths: Sequence[float], target_nm: float) -> int:
    """
    Returns the index of the band with wavelength closest to target_nm.
    """
    wls = np.asarray(wavelengths, dtype=np.float64)
    if wls.size == 0:
        raise ValueError("Wavelength array is empty.")
    return int(np.argmin(np.abs(wls - target_nm)))


def get_reflectance_at(
    wavelengths: Sequence[float],
    reflectance: np.ndarray,
    target_nm: float
) -> Union[float, np.ndarray]:
    """
    Linearly interpolates reflectance at target_nm.
    Supports 1D vector (B,) returning float,
    or multi-dimensional array (..., B) returning array with shape (...).
    """
    wls = np.asarray(wavelengths, dtype=np.float64)
    r = np.asarray(reflectance, dtype=np.float64)

    if wls.ndim != 1 or wls.size == 0:
        raise ValueError("Wavelengths must be a non-empty 1D array.")

    # Boundary cases
    if target_nm <= wls[0]:
        return float(r[..., 0]) if r.ndim == 1 else r[..., 0]
    if target_nm >= wls[-1]:
        return float(r[..., -1]) if r.ndim == 1 else r[..., -1]

    idx = find_closest_band_index(wls, target_nm)
    if np.isclose(wls[idx], target_nm, atol=1e-3):
        return float(r[..., idx]) if r.ndim == 1 else r[..., idx]

    if wls[idx] < target_nm:
        lower_idx = idx
        upper_idx = min(idx + 1, len(wls) - 1)
    else:
        lower_idx = max(0, idx - 1)
        upper_idx = idx

    if lower_idx == upper_idx:
        return float(r[..., lower_idx]) if r.ndim == 1 else r[..., lower_idx]

    x0 = wls[lower_idx]
    x1 = wls[upper_idx]
    dx = x1 - x0
    if abs(dx) < 1e-7:
        return float(r[..., lower_idx]) if r.ndim == 1 else r[..., lower_idx]

    t = (target_nm - x0) / dx
    y0 = r[..., lower_idx]
    y1 = r[..., upper_idx]
    res = y0 + t * (y1 - y0)
    return float(res) if r.ndim == 1 else res


def resample_spectrum(
    src_wls: Sequence[float],
    src_reflectance: np.ndarray,
    target_wls: Sequence[float]
) -> np.ndarray:
    """
    Resamples a 1D or multi-dimensional spectral array along the last axis
    from src_wls to target_wls using linear interpolation.
    """
    src_w = np.asarray(src_wls, dtype=np.float64)
    tgt_w = np.asarray(target_wls, dtype=np.float64)
    src_r = np.asarray(src_reflectance, dtype=np.float64)

    if src_r.ndim == 1:
        return np.interp(tgt_w, src_w, src_r)

    # Multi-dimensional: reshape to (N, B_src), interpolate, reshape back
    orig_shape = src_r.shape
    B_src = orig_shape[-1]
    flat_r = src_r.reshape(-1, B_src)
    N = flat_r.shape[0]
    B_tgt = len(tgt_w)

    resampled = np.empty((N, B_tgt), dtype=np.float64)
    for i in range(N):
        resampled[i] = np.interp(tgt_w, src_w, flat_r[i])

    new_shape = list(orig_shape[:-1]) + [B_tgt]
    return resampled.reshape(new_shape)


def resample_cube(
    src_wls: Sequence[float],
    cube: np.ndarray,
    target_wls: Sequence[float]
) -> np.ndarray:
    """
    Resamples a 3D hyperspectral cube (H, W, B_src) to target_wls (H, W, B_dst).
    """
    return resample_spectrum(src_wls, cube, target_wls)


if __name__ == "__main__":
    valid_emit = get_valid_band_indices(EMIT_WAVELENGTHS)
    valid_aviris = get_valid_band_indices(AVIRIS_NG_WAVELENGTHS)
    print(f"Wavelength Utils module verified: AVIRIS {len(valid_aviris)}/425 clean bands, EMIT {len(valid_emit)}/285 clean bands.")

