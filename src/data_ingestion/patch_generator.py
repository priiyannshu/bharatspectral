"""
patch_generator.py - Indian Smallholder Spatial-Spectral Patch Sampler
Generates 9x9xB and 15x15xB patches reflecting typical parcel fragmentation.
"""

import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BharatSpectral.PatchGenerator")

def sample_patches(cube_shape, patch_size=9, stride=4):
    """
    Computes valid patch coordinates for spatial-spectral sampling.
    """
    h, w, b = cube_shape
    patches = []
    half = patch_size // 2
    for r in range(half, h - half, stride):
        for c in range(half, w - half, stride):
            patches.append((r - half, r + half + 1, c - half, c + half + 1))
    logger.info("Sampled %d spatial patches of size %dx%d from cube shape %s", len(patches), patch_size, patch_size, cube_shape)
    return patches

if __name__ == "__main__":
    p = sample_patches((145, 145, 200), patch_size=9, stride=8)
    print(f"Generated {len(p)} patch boundaries.")
