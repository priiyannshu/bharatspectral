# Benchmark Figures & Visual Proofs (`outputs/figures/`)

This directory contains publication-ready figures visualizing baseline failures, domain shifts, and the physical motivation for BharatSpectral-MAE's 7 architectural innovations.

---

## 🖼️ Figures Index

| Figure | Description | Key Insight |
|---|---|---|
| [`domain_shift_collapse.png`](domain_shift_collapse.png) | **Cross-Scene Generalization Collapse:** Degradation of standard DL models when tested across different sensor geometries and flight lines. | Proves that standard CNNs/Transformers fail when GSD and sensor wavelength calibration change across Indian scenes. |
| [`spatial_patch_fragmentation.png`](spatial_patch_fragmentation.png) | **Indian Smallholder Patch Fragmentation:** Sub-pixel boundary mixing across small agricultural holdings (< 0.5 ha). | Demonstrates why naive large spatial patches ($16 \times 16$) fail on fragmented Indian fields. |
| [`sam_magnitude_confusion.png`](sam_magnitude_confusion.png) | **Spectral Angle Mapper (SAM) Magnitude Insensitivity:** Failure to distinguish vegetation stress levels. | Shows that SAM only measures angle, losing absolute reflectance and nutrient absorption depth. |
| [`gis_linear_unmixing_residuals.png`](gis_linear_unmixing_residuals.png) | **Linear Spectral Unmixing (LSU) Error Residuals:** Sub-pixel non-linear canopy scattering residuals. | Shows significant unmodeled residuals in classical LSU caused by multi-layer crop canopies. |
