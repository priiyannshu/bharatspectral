# Benchmark Metrics & Evaluation Tables (`outputs/tables/`)

This directory contains quantitative benchmark evaluation logs, comparison tables, and cross-scene validation results.

---

## 📋 Evaluation Tables

### 1. [`benchmark_results.csv`](benchmark_results.csv)
Comprehensive accuracy, Kappa coefficient, parameter count, and inference latency across baseline models:
* Classical Machine Learning: SVM (RBF), Random Forest
* Deep Learning: 3D-CNN (Hamida et al.), HybridSN (Roy et al.), Spectral Transformer
* Classical GIS Baselines: Spectral Angle Mapper (SAM), Linear Spectral Unmixing (LSU)

### 2. [`cross_scene_evaluation.json`](cross_scene_evaluation.json)
Cross-domain generalization scores evaluating zero-shot transfer across distinct sensor flight lines (AVIRIS-NG India vs. Indian Pines / Salinas transfer).

### 3. [`gis_spectroscopy_metrics.json`](gis_spectroscopy_metrics.json)
Deterministic physical spectroscopy performance metrics (SAM angular error, LSU root-mean-square abundance residuals).

### 4. [`gis_vs_ai_summary.json`](gis_vs_ai_summary.json)
Comprehensive multi-criteria comparison matrix between traditional GIS remote sensing software (ENVI / QGIS) and Deep Learning / BharatSpectral Foundation Model.
