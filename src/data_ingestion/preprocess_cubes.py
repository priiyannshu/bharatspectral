"""
preprocess_cubes.py - Hyperspectral Cube Preprocessing Pipeline
Applies atmospheric water absorption masking (1350-1450 nm, 1800-1950 nm)
and radiometric reflectance normalization.
"""

import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BharatSpectral.Preprocess")

ATMOSPHERIC_ABSORPTION_WINDOWS = [
    (1350, 1450),  # Strong atmospheric water vapor absorption
    (1800, 1950),  # Major water vapor / CO2 absorption gap
]

def mask_atmospheric_bands(wavelengths, cube_data=None):
    """
    Identifies clean spectral bands outside atmospheric absorption windows.
    Returns valid band indices.
    """
    valid_indices = []
    for idx, wl in enumerate(wavelengths):
        is_bad = any(start <= wl <= end for start, end in ATMOSPHERIC_ABSORPTION_WINDOWS)
        if not is_bad:
            valid_indices.append(idx)
    logger.info("Atmospheric masking: %d / %d clean bands retained.", len(valid_indices), len(wavelengths))
    return valid_indices

def normalize_reflectance(cube, scale_factor=10000.0):
    """
    Scales integer reflectance values [0, 10000] to float [0.0, 1.0].
    """
    return cube / scale_factor

if __name__ == "__main__":
    sample_wls = list(range(400, 2500, 10))
    clean = mask_atmospheric_bands(sample_wls)
    print(f"Masked sample: {len(clean)} valid bands from {len(sample_wls)} total bands.")
