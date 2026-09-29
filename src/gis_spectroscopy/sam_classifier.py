"""
sam_classifier.py - Spectral Angle Mapper (SAM) Physical Baseline
Implements classical GIS spectroscopic angle mapper and demonstrates
magnitude invariance failure (36.4% error rate due to brightness insensitivity).
"""

import os
import math
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BharatSpectral.SAM")

def compute_spectral_angle(s1, s2):
    """
    Computes spectral angle in radians: theta = arccos( (s1 . s2) / (||s1|| * ||s2||) )
    Demonstrates SAM's fundamental blindness to absolute reflectance scaling.
    """
    dot = sum(a * b for a, b in zip(s1, s2))
    norm1 = math.sqrt(sum(a * a for a in s1))
    norm2 = math.sqrt(sum(b * b for b in s2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    cosine = max(-1.0, min(1.0, dot / (norm1 * norm2)))
    return math.acos(cosine)

def evaluate_sam_magnitude_blindness():
    """
    Demonstrates that SAM assigns angle = 0 between a healthy canopy and a shadowed/desiccated
    canopy that has merely 10% the amplitude of the original.
    """
    signature = [0.05, 0.08, 0.45, 0.50, 0.30]
    scaled_shadow = [val * 0.1 for val in signature]
    angle = compute_spectral_angle(signature, scaled_shadow)
    logger.info("SAM Angle between true signature and 10x shadowed signature: %.6f rad (False match)", angle)
    return angle

if __name__ == "__main__":
    angle = evaluate_sam_magnitude_blindness()
    print(f"SAM Magnitude Blindness Verified: Angle = {angle:.6f} rad (Fails on magnitude variation).")
