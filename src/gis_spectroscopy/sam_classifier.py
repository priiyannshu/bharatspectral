"""
sam_classifier.py - Spectral Angle Mapper (SAM) Classification Baseline

Implements classical GIS spectroscopic angle mapping:
theta = arccos( (s1 . s2) / (||s1|| * ||s2||) )
confidence = max(0, min(100, (1 - theta / (pi / 2)) * 100))

Demonstrates magnitude invariance failure (brightness insensitivity)
for academic comparison against non-linear foundation representations.
Supports 1D spectral vectors and 3D spatial cubes.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Sequence, Optional, Union, Any
import math
import logging
import numpy as np

logger = logging.getLogger("BharatSpectral.SAM")


@dataclass
class SamCandidate:
    id: str
    label: str
    spectral_angle_rad: float
    confidence_pct: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "spectral_angle_rad": float(self.spectral_angle_rad),
            "confidence_pct": float(self.confidence_pct),
        }


@dataclass
class SamClassification:
    top_match: str
    spectral_angle_rad: float
    confidence_pct: float
    candidates: List[SamCandidate]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "top_match": self.top_match,
            "spectral_angle_rad": float(self.spectral_angle_rad),
            "confidence_pct": float(self.confidence_pct),
            "candidates": [c.to_dict() for c in self.candidates],
        }


def compute_spectral_angle(s1: Sequence[float], s2: Sequence[float]) -> float:
    """
    Computes spectral angle in radians between two vectors:
    theta = arccos( (s1 . s2) / (||s1|| * ||s2||) )
    Returns pi/2 (orthogonal) if either vector has near-zero magnitude.
    """
    v1 = np.asarray(s1, dtype=np.float64)
    v2 = np.asarray(s2, dtype=np.float64)

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if np.isnan(norm1) or np.isnan(norm2) or norm1 < 1e-7 or norm2 < 1e-7:
        return float(np.pi / 2)

    cosine = float(np.dot(v1, v2) / (norm1 * norm2))
    cosine = max(-1.0, min(1.0, cosine))
    return float(np.arccos(cosine))


def compute_sam_classification(
    pixel_reflectance: Sequence[float],
    reference_signatures: Sequence[Dict[str, Any]],
    valid_band_indices: Optional[Sequence[int]] = None
) -> SamClassification:
    """
    Evaluates spectral angle between an observed pixel vector and a library of reference signatures.
    Args:
        pixel_reflectance: (B,) observed surface reflectance
        reference_signatures: list of dicts with {"id": str, "label": str, "reflectance": Sequence[float]}
        valid_band_indices: optional indices of unmasked bands
    Returns:
        SamClassification object containing top match, angle, confidence, and ranked candidates.
    """
    raw_y = np.asarray(pixel_reflectance, dtype=np.float64)
    if valid_band_indices is not None:
        bands = np.asarray(valid_band_indices, dtype=int)
        y = raw_y[bands]
    else:
        y = raw_y

    norm_y = np.linalg.norm(y)
    candidates: List[SamCandidate] = []

    for ref in reference_signatures:
        ref_id = ref.get("id", "unknown")
        ref_label = ref.get("label", ref_id)
        raw_r = np.asarray(ref["reflectance"], dtype=np.float64)

        if valid_band_indices is not None:
            r = raw_r[bands]
        else:
            r = raw_r

        norm_r = np.linalg.norm(r)
        if np.isnan(norm_y) or np.isnan(norm_r) or norm_y < 1e-7 or norm_r < 1e-7:
            angle_rad = float(np.pi / 2)
            confidence = 0.0
        else:
            dot = np.dot(y, r)
            cosine = np.clip(dot / (norm_y * norm_r), -1.0, 1.0)
            angle_rad = float(np.arccos(cosine))
            confidence = max(0.0, min(100.0, (1.0 - angle_rad / (np.pi / 2)) * 100.0))

        candidates.append(SamCandidate(
            id=ref_id,
            label=ref_label,
            spectral_angle_rad=round(angle_rad, 4),
            confidence_pct=round(confidence, 1)
        ))

    candidates.sort(key=lambda c: c.spectral_angle_rad)

    top = candidates[0] if candidates else None
    return SamClassification(
        top_match=top.label if top else "Unknown Material",
        spectral_angle_rad=top.spectral_angle_rad if top else 0.0,
        confidence_pct=top.confidence_pct if top else 0.0,
        candidates=candidates
    )


def compute_cube_sam(
    cube: np.ndarray,
    reference_signatures: Sequence[Dict[str, Any]],
    valid_band_indices: Optional[Sequence[int]] = None
) -> Dict[str, Any]:
    """
    Vectorized SAM classification across a 3D spatial-spectral cube (H, W, B).
    Returns:
        - 'top_class_index': (H, W) array of class index
        - 'min_angle_rad': (H, W) array of lowest spectral angle
        - 'confidence_pct': (H, W) array of classification confidence
        - 'class_labels': list of string class labels
    """
    cube_arr = np.asarray(cube, dtype=np.float64)
    if cube_arr.ndim != 3:
        raise ValueError("compute_cube_sam expects a 3D array (H, W, B).")

    H, W, B = cube_arr.shape
    p = len(reference_signatures)
    class_labels = [ref.get("label", ref.get("id", f"Class_{i}")) for i, ref in enumerate(reference_signatures)]

    if valid_band_indices is not None:
        idx = np.asarray(valid_band_indices, dtype=int)
        flat_pixels = cube_arr[:, :, idx].reshape(H * W, len(idx))  # (N, B_valid)
        ref_matrix = np.column_stack([np.asarray(ref["reflectance"], dtype=np.float64)[idx] for ref in reference_signatures])  # (B_valid, p)
    else:
        flat_pixels = cube_arr.reshape(H * W, B)
        ref_matrix = np.column_stack([np.asarray(ref["reflectance"], dtype=np.float64) for ref in reference_signatures])

    N = H * W
    pixel_norms = np.linalg.norm(flat_pixels, axis=1, keepdims=True)  # (N, 1)
    ref_norms = np.linalg.norm(ref_matrix, axis=0, keepdims=True)    # (1, p)

    # Dot products: (N, p)
    dots = flat_pixels @ ref_matrix
    denoms = pixel_norms @ ref_norms
    safe_denoms = np.where(denoms > 1e-6, denoms, 1.0)
    cosines = np.clip(dots / safe_denoms, -1.0, 1.0)
    angles = np.arccos(cosines)  # (N, p)

    # Top match per pixel
    top_indices = np.argmin(angles, axis=1)  # (N,)
    min_angles = angles[np.arange(N), top_indices]  # (N,)
    confidences = np.clip((1.0 - min_angles / (np.pi / 2)) * 100.0, 0.0, 100.0)

    return {
        "top_class_index": top_indices.reshape(H, W),
        "min_angle_rad": min_angles.reshape(H, W).astype(np.float32),
        "confidence_pct": confidences.reshape(H, W).astype(np.float32),
        "class_labels": class_labels,
    }


def evaluate_sam_magnitude_blindness() -> float:
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
