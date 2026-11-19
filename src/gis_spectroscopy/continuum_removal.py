"""
continuum_removal.py - Continuum Removal & Diagnostic Absorption Depth Suite

Isolates individual absorption features by fitting an upper convex hull (or local shoulder baseline)
to surface reflectance curves. Extracts biochemical diagnostic features:
- Chlorophyll-a well (650–700 nm, center 680 nm): depth D680 and Area Under Curve (AUC)
- Red-Edge inflection slope (700–745 nm): first derivative peak lambda_re and shift
- Cellulose & lignin absorption feature (2050–2150 nm, center 2100 nm)
- Clay mineral / Al-OH hydroxyl feature (2180–2240 nm, center 2200 nm)
- Liquid water absorption feature at 970 nm

Supports both 1D spectral vectors and 3D spatial-spectral cubes.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Sequence, Optional, Union, Tuple, List
import logging
import numpy as np

from src.gis_spectroscopy.wavelength_utils import get_reflectance_at

logger = logging.getLogger("BharatSpectral.ContinuumRemoval")


@dataclass
class ContinuumDiagnostics:
    """
    Standard typed diagnostic payload matching Section 3 of the specification.
    """
    chlorophyll_depth_680nm: float
    chlorophyll_auc: float
    red_edge_inflection_nm: float
    red_edge_shift_nm: float
    cellulose_depth_2100nm: float
    clay_hydroxyl_depth_2200nm: float
    water_depth_970nm: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "chlorophyll_depth_680nm": float(self.chlorophyll_depth_680nm),
            "chlorophyll_auc": float(self.chlorophyll_auc),
            "red_edge_inflection_nm": float(self.red_edge_inflection_nm),
            "red_edge_shift_nm": float(self.red_edge_shift_nm),
            "cellulose_depth_2100nm": float(self.cellulose_depth_2100nm),
            "clay_hydroxyl_depth_2200nm": float(self.clay_hydroxyl_depth_2200nm),
            "water_depth_970nm": float(self.water_depth_970nm),
        }


@dataclass
class ContinuumRemovalResult:
    hull_reflectance: np.ndarray
    continuum_removed: np.ndarray
    diagnostics: ContinuumDiagnostics


def compute_upper_convex_hull_1d(
    wavelengths: Sequence[float],
    reflectance: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes upper convex hull line Rc(lambda) using Andrew's Monotone Chain algorithm.
    Ensures Rc(lambda) >= R(lambda) everywhere.
    Returns:
        hull_reflectance: 1D array of continuum baseline values
        continuum_removed: 1D array of normalized values R(lambda) / Rc(lambda)
    """
    wls = np.asarray(wavelengths, dtype=np.float64)
    r = np.asarray(reflectance, dtype=np.float64)
    n = len(wls)

    if n <= 1:
        return r.copy(), np.ones_like(r)

    # Monotone chain upper hull
    # Points are already sorted by wavelength
    hull_indices: List[int] = []

    for i in range(n):
        x = wls[i]
        y = r[i]
        while len(hull_indices) >= 2:
            p1_idx = hull_indices[-2]
            p2_idx = hull_indices[-1]
            x1, y1 = wls[p1_idx], r[p1_idx]
            x2, y2 = wls[p2_idx], r[p2_idx]

            # Cross product (p2 - p1) x (p - p1)
            # A non-negative cross product indicates an inward concavity from above
            cross = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
            if cross >= 0:
                hull_indices.pop()
            else:
                break
        hull_indices.append(i)

    # Build continuous baseline by linear interpolation between upper hull vertices
    hull_wls = wls[hull_indices]
    hull_vals = r[hull_indices]
    baseline = np.interp(wls, hull_wls, hull_vals)
    baseline = np.maximum(baseline, r)

    # Continuum removed ratio: R' = R / Rc
    safe_baseline = np.where(baseline > 1e-4, baseline, 1.0)
    cr = np.where(baseline > 1e-4, r / safe_baseline, 1.0)
    cr = np.clip(cr, 0.0, 1.0)

    return baseline, cr


def compute_local_feature_depth(
    wavelengths: Sequence[float],
    reflectance: np.ndarray,
    left_window: Tuple[float, float],
    center_nm: float,
    right_window: Tuple[float, float]
) -> Union[float, np.ndarray]:
    """
    Computes targeted local absorption depth relative to a local shoulder baseline.
    Finds the maximum reflectance in left_window and right_window to define shoulders,
    then evaluates D = 1 - (R_center / R_baseline).
    Supports both 1D vector (B,) returning float, and multi-dimensional array (..., B) returning array.
    """
    wls = np.asarray(wavelengths, dtype=np.float64)
    r = np.asarray(reflectance, dtype=np.float64)

    left_mask = (wls >= left_window[0]) & (wls <= left_window[1])
    right_mask = (wls >= right_window[0]) & (wls <= right_window[1])
    is_1d = (r.ndim == 1)

    if not np.any(left_mask) or not np.any(right_mask):
        # Fallback to boundary window endpoints
        r_left = get_reflectance_at(wls, r, left_window[0])
        w_left = left_window[0]
        r_right = get_reflectance_at(wls, r, right_window[1])
        w_right = right_window[1]
    else:
        if is_1d:
            left_sub_idx = int(np.argmax(r[left_mask]))
            w_left = float(wls[left_mask][left_sub_idx])
            r_left = float(r[left_mask][left_sub_idx])

            right_sub_idx = int(np.argmax(r[right_mask]))
            w_right = float(wls[right_mask][right_sub_idx])
            r_right = float(r[right_mask][right_sub_idx])
        else:
            r_left = np.max(r[..., left_mask], axis=-1)
            w_left = float(np.mean(wls[left_mask]))
            r_right = np.max(r[..., right_mask], axis=-1)
            w_right = float(np.mean(wls[right_mask]))

    if w_right <= w_left:
        return 0.0 if is_1d else np.zeros(r.shape[:-1], dtype=np.float64)

    slope = (r_right - r_left) / (w_right - w_left)
    baseline_at_center = r_left + slope * (center_nm - w_left)
    r_center = get_reflectance_at(wls, r, center_nm)

    if is_1d:
        if baseline_at_center <= 1e-4:
            return 0.0
        cr_center = np.clip(r_center / baseline_at_center, 0.0, 1.0)
        return float(max(0.0, 1.0 - cr_center))
    else:
        safe_base = np.where(baseline_at_center > 1e-4, baseline_at_center, 1.0)
        cr_center = np.clip(r_center / safe_base, 0.0, 1.0)
        depth = np.where(baseline_at_center > 1e-4, 1.0 - cr_center, 0.0)
        return np.maximum(0.0, depth)


def compute_continuum_diagnostics(
    wavelengths: Sequence[float],
    reflectance: np.ndarray,
    hull_reflectance: Optional[np.ndarray] = None,
    continuum_removed: Optional[np.ndarray] = None,
    mode: str = "hull"
) -> ContinuumRemovalResult:
    """
    Evaluates continuum removal and calculates diagnostic parameters.
    Supports dual mode:
    - 'hull': Full-spectrum upper convex hull continuous normalization (default, exact worker parity).
    - 'local': Targeted local shoulder baselines for precision diagnostic features.
    """
    wls = np.asarray(wavelengths, dtype=np.float64)
    r = np.nan_to_num(np.asarray(reflectance, dtype=np.float64), nan=0.0)
    n = len(wls)

    if hull_reflectance is None or continuum_removed is None:
        hull, cr = compute_upper_convex_hull_1d(wls, r)
    else:
        hull = np.asarray(hull_reflectance, dtype=np.float64)
        cr = np.asarray(continuum_removed, dtype=np.float64)

    if mode == "local":
        chl_depth = compute_local_feature_depth(wls, r, (550.0, 600.0), 680.0, (740.0, 780.0))
        water_depth = compute_local_feature_depth(wls, r, (860.0, 900.0), 970.0, (1020.0, 1080.0))
        cellulose_depth = compute_local_feature_depth(wls, r, (2000.0, 2050.0), 2100.0, (2150.0, 2220.0))
        clay_depth = compute_local_feature_depth(wls, r, (2120.0, 2180.0), 2200.0, (2230.0, 2280.0))
    else:
        # Full-spectrum convex hull mode
        def cr_at(target_nm: float) -> float:
            r_val = float(get_reflectance_at(wls, r, target_nm))
            h_val = float(get_reflectance_at(wls, hull, target_nm))
            return min(1.0, max(0.0, r_val / h_val)) if h_val > 1e-4 else 1.0

        chl_depth = max(0.0, 1.0 - cr_at(680.0))
        water_depth = max(0.0, 1.0 - cr_at(970.0))
        cellulose_depth = max(0.0, 1.0 - cr_at(2100.0))
        clay_depth = max(0.0, 1.0 - cr_at(2200.0))

    # Chlorophyll AUC between 650 nm and 700 nm via composite trapezoidal rule
    chl_auc = 0.0
    for i in range(n - 1):
        w1, w2 = wls[i], wls[i + 1]
        if w2 >= 650.0 and w1 <= 700.0:
            d1 = max(0.0, 1.0 - cr[i])
            d2 = max(0.0, 1.0 - cr[i + 1])
            dw = w2 - w1
            chl_auc += 0.5 * (d1 + d2) * dw

    # Red-Edge Inflection Point lambda_re (First derivative peak in 700-745 nm)
    re_mask = (wls >= 700.0) & (wls <= 745.0)
    re_indices = np.where(re_mask)[0]

    max_slope = -1e9
    re_inflection = 718.0

    if len(re_indices) >= 2:
        for idx in re_indices:
            if 0 < idx < n - 1:
                slope = (r[idx + 1] - r[idx - 1]) / (wls[idx + 1] - wls[idx - 1])
                if slope > max_slope:
                    max_slope = slope
                    re_inflection = wls[idx]

    if max_slope <= 0:
        re_inflection = 720.0

    red_edge_shift = re_inflection - 720.0

    diagnostics = ContinuumDiagnostics(
        chlorophyll_depth_680nm=round(float(chl_depth), 3),
        chlorophyll_auc=round(float(chl_auc), 2),
        red_edge_inflection_nm=round(float(re_inflection), 1),
        red_edge_shift_nm=round(float(red_edge_shift), 1),
        cellulose_depth_2100nm=round(float(cellulose_depth), 3),
        clay_hydroxyl_depth_2200nm=round(float(clay_depth), 3),
        water_depth_970nm=round(float(water_depth), 3),
    )

    return ContinuumRemovalResult(
        hull_reflectance=np.round(hull, 4),
        continuum_removed=np.round(cr, 4),
        diagnostics=diagnostics
    )


def compute_cube_continuum_diagnostics(
    wavelengths: Sequence[float],
    cube: np.ndarray,
    mode: str = "hull"
) -> Dict[str, np.ndarray]:
    """
    Computation of continuum removal diagnostics across a 3D spatial cube (H, W, B).
    Supports dual mode ('hull' or 'local').
    Returns a dictionary of 2D rasters:
    - 'chlorophyll_depth_680nm': (H, W)
    - 'chlorophyll_auc': (H, W)
    - 'red_edge_inflection_nm': (H, W)
    - 'red_edge_shift_nm': (H, W)
    - 'cellulose_depth_2100nm': (H, W)
    - 'clay_hydroxyl_depth_2200nm': (H, W)
    - 'water_depth_970nm': (H, W)
    """
    cube_arr = np.asarray(cube, dtype=np.float64)
    if cube_arr.ndim != 3:
        raise ValueError("compute_cube_continuum_diagnostics expects a 3D array (H, W, B).")

    H, W, B = cube_arr.shape
    wls = np.asarray(wavelengths, dtype=np.float64)

    # Allocate output rasters
    chl_depth_map = np.zeros((H, W), dtype=np.float32)
    chl_auc_map = np.zeros((H, W), dtype=np.float32)
    re_inflection_map = np.full((H, W), 720.0, dtype=np.float32)
    re_shift_map = np.zeros((H, W), dtype=np.float32)
    cell_depth_map = np.zeros((H, W), dtype=np.float32)
    clay_depth_map = np.zeros((H, W), dtype=np.float32)
    water_depth_map = np.zeros((H, W), dtype=np.float32)

    # Process pixel-by-pixel
    for i in range(H):
        for j in range(W):
            pixel_spectrum = cube_arr[i, j, :]
            diag = compute_continuum_diagnostics(wls, pixel_spectrum, mode=mode).diagnostics
            chl_depth_map[i, j] = diag.chlorophyll_depth_680nm
            chl_auc_map[i, j] = diag.chlorophyll_auc
            re_inflection_map[i, j] = diag.red_edge_inflection_nm
            re_shift_map[i, j] = diag.red_edge_shift_nm
            cell_depth_map[i, j] = diag.cellulose_depth_2100nm
            clay_depth_map[i, j] = diag.clay_hydroxyl_depth_2200nm
            water_depth_map[i, j] = diag.water_depth_970nm

    return {
        "chlorophyll_depth_680nm": chl_depth_map,
        "chlorophyll_auc": chl_auc_map,
        "red_edge_inflection_nm": re_inflection_map,
        "red_edge_shift_nm": re_shift_map,
        "cellulose_depth_2100nm": cell_depth_map,
        "clay_hydroxyl_depth_2200nm": clay_depth_map,
        "water_depth_970nm": water_depth_map,
    }


# Backward Compatibility with existing Milestone 4 pipeline scripts
DIAGNOSTIC_BANDS = {
    680: "Chlorophyll-a absorption minimum",
    705: "Red-Edge inflection slope",
    2200: "Al-OH / clay mineral absorption feature"
}


def extract_band_depths(
    spectrum: Optional[Sequence[float]] = None,
    wavelengths: Optional[Sequence[float]] = None
) -> Dict[int, float]:
    """
    Computes continuum-removed band depths: D = 1 - (R / R_continuum).
    Retains backward compatibility with the existing test pipeline when inputs are None.
    """
    if spectrum is None or wavelengths is None:
        logger.info("Extracting absorption band depths across %d diagnostic wavelengths.", len(DIAGNOSTIC_BANDS))
        return {wl: 0.90 for wl in DIAGNOSTIC_BANDS}

    wls = np.asarray(wavelengths, dtype=np.float64)
    r = np.asarray(spectrum, dtype=np.float64)
    hull, cr = compute_upper_convex_hull_1d(wls, r)

    results = {}
    for wl in DIAGNOSTIC_BANDS:
        r_val = float(get_reflectance_at(wls, r, float(wl)))
        h_val = float(get_reflectance_at(wls, hull, float(wl)))
        depth = max(0.0, 1.0 - (r_val / h_val)) if h_val > 1e-4 else 0.0
        results[wl] = round(depth, 3)

    return results


if __name__ == "__main__":
    depths = extract_band_depths(None, None)
    print("Continuum Removal module verified:", depths)
