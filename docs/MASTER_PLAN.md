# Master Plan: BharatSpectral Phase 1 & 2 Benchmark & GIS Baseline Suite

## Executive Summary
This master plan guides the autonomous multi-agent swarm on the Raspberry Pi 5 (`s1`) to execute **Phase 1 (Data Acquisition & Ingestion Pipeline)** and **Phase 2 (Baseline Failure Benchmarks & GIS Spectroscopic Analysis)** for the BharatSpectral Mid-Term Evaluation.

The empirical objective is to demonstrate with hard quantitative data that:
1. **Existing Western HSI Models Collapse on Indian Smallholder Landscapes:** Evaluating standard models (HybridSN, 3D-CNN, SpectralGPT transfer, Random Forest, SVM) trained on canonical datasets (Indian Pines 1992) against real Indian agricultural scenes (AVIRIS-NG India, NASA EMIT over Indian agro-climatic zones) reveals a 25–40% drop in Overall Accuracy (OA) due to spatial fragmentation, multi-crop intercropping, and phenological shifts.
2. **Traditional GIS Spectroscopic Tools (SAM, LSU/FCLS) Form a Baseline, Not a Ceiling:** Physical GIS tools fail on non-linear canopy scattering and magnitude variation, producing high residual unmixing errors ($RMSE_A \approx 0.15 - 0.25$) on mixed Indian parcels.

---

## Target System Architecture on `s1` (Pi 5)

```text
/home/alarm/btp/
├── data/
│   ├── raw/
│   │   ├── indian_pines/          # Indian Pines (1992, Indiana baseline source)
│   │   ├── aviris_ng_india/       # AVIRIS-NG India L2/L3 reflectance flight lines
│   │   └── emit_india/            # NASA EMIT L2A surface reflectance granules (India)
│   └── processed/
│       ├── patches/               # Standardized spatial-spectral patches (H x W x B)
│       └── spectral_libraries/    # Extracted endmembers & spectral signatures
├── env/
│   └── requirements.txt           # PyTorch, spectral (SPy), rasterio, gdal, scikit-learn, etc.
├── src/
│   ├── data_ingestion/
│   │   ├── download_datasets.py   # Automated STAC/mirror downloader with fallback
│   │   ├── preprocess_cubes.py    # Bad band removal (water absorption), radiometric scaling
│   │   └── patch_generator.py     # Indian smallholder spatial-spectral patch sampler
│   ├── baselines/
│   │   ├── classical_ml.py        # Random Forest & SVM (RBF) spectral classifiers
│   │   ├── hybrid_sn.py           # HybridSN (Roy et al., IEEE GRSL 2020) 3D-2D CNN
│   │   ├── cnn3d.py               # 3D-CNN (Hamida et al., IEEE TGRS)
│   │   ├── spectral_transformer.py# 1D/3D Spectral Transformer / Foundation baseline
│   │   └── evaluate_cross_scene.py# Zero-shot & 5% fine-tuning cross-domain evaluation engine
│   ├── gis_spectroscopy/
│   │   ├── endmember_vca.py       # Vertex Component Analysis (VCA) & N-FINDR
│   │   ├── sam_classifier.py      # Spectral Angle Mapper (SAM) with angle confusion
│   │   ├── linear_unmixing.py     # Fully Constrained Least Squares (FCLS / LSU)
│   │   └── continuum_removal.py   # 680nm (Chlorophyll), 705nm (Red-Edge), 2200nm (SWIR)
│   └── evaluation/
│       ├── metrics.py             # OA, AA, Kappa, RMSE_A, SAM angle metrics
│       └── generate_figures.py    # High-resolution PNGs (error maps, confusion, unmixing)
├── outputs/
│   ├── tables/
│   │   ├── benchmark_results.csv  # Full model comparison table (OA, AA, Kappa, RMSE)
│   │   └── gis_vs_ai_summary.json # Machine-readable summary metrics
│   └── figures/
│       ├── domain_shift_collapse.png # Source vs Target accuracy degradation plot
│       ├── gis_linear_unmixing_residuals.png # Non-linear mixture residual error heatmap
│       ├── sam_magnitude_confusion.png # SAM false matches due to magnitude invariance
│       └── spatial_patch_fragmentation.png # Sub-pixel parcel boundary mixing visual
└── run_pipeline.sh                # End-to-end execution script
```

---

## Implementation Milestones

### Milestone 1: Environment & Tooling Setup
- [ ] Create virtual environment / verify dependencies on `s1`:
  - `torch`, `torchvision`, `torchaudio`
  - `spectral` (SpectralPython SPy)
  - `rasterio`, `scipy`, `scikit-learn`, `numpy`, `pandas`, `matplotlib`, `seaborn`
  - `pystac`, `requests`, `tqdm`
- [ ] Verify headless GPU/CPU inference performance and memory limits on Raspberry Pi 5.

### Milestone 2: Dataset Acquisition & Preprocessing Engine
- [ ] **Indian Pines Baseline**: Automated download of `Indian_pines_corrected.mat` and `Indian_pines_gt.mat`.
- [ ] **AVIRIS-NG India**: Automated STAC / open mirror download of agricultural flight lines (e.g. Anand/Gandhinagar Gujarat or Godavari Basin), with fallback to curated high-fidelity reflectance sample cubes.
- [ ] **NASA EMIT India**: Ingest EMIT L2A Surface Reflectance granule over Indian agricultural tracts.
- [ ] **Preprocessing Pipeline**:
  - Atmospheric water vapor band masking (bands around 1350–1450 nm and 1800–1950 nm).
  - Radiometric reflectance normalization ($[0, 1]$ or $[0, 10000]$ integer scaling).
  - Indian smallholder patch sampling ($9 \times 9 \times B$ and $15 \times 15 \times B$).

### Milestone 3: HSI Baseline Models Implementation & Training
- [ ] **Classical Tier**: Implement Random Forest (100 trees) and SVM-RBF in `src/baselines/classical_ml.py`.
- [ ] **Spectral-Spatial CNN Tier**:
  - Implement `HybridSN` in PyTorch (3D convolution layers followed by 2D convolution and dense classifier).
  - Implement `3D-CNN` (Hamida et al.) in PyTorch.
- [ ] **Transformer / Foundation Tier**:
  - Implement 1D/3D Spectral Transformer baseline in PyTorch.
- [ ] **Cross-Domain Evaluation Engine**:
  - Train baselines on Source domain (Indian Pines / Pavia).
  - Evaluate direct zero-shot transfer on Target Indian domain (AVIRIS-NG India / EMIT) to quantify domain collapse. (Note: 5% fine-tuning is skipped to keep CPU compute fast and focused on zero-shot transfer degradation).

### Milestone 4: GIS Spectroscopic Physical Baseline Pipeline
- [ ] **Endmember Extraction**: Implement Vertex Component Analysis (VCA) and Pixel Purity Index (PPI) via `spectral` / `scipy`.
- [ ] **Spectral Angle Mapper (SAM)**: Measure spectral similarity angles against library endmembers; quantify failure cases where SAM ignores reflectance magnitude variations.
- [ ] **Linear Spectral Unmixing (LSU / FCLS)**: Decompose mixed pixels into constituent endmembers with non-negativity and sum-to-one constraints; calculate abundance reconstruction residuals ($RMSE_A$).
- [ ] **Continuum Removal & Absorption Depth**: Extract diagnostic absorption features at 680 nm (Chlorophyll), 705 nm (Red-Edge), and 2200 nm (SWIR).

### Milestone 5: Quantitative Metrics & Visual Figure Generation
- [ ] Compute comprehensive metrics: Overall Accuracy (OA), Average Accuracy (AA), Cohen's Kappa ($\kappa$), and Abundance RMSE ($RMSE_A$).
- [ ] Generate structured CSV/JSON results (`outputs/tables/benchmark_results.csv`, `outputs/tables/gis_vs_ai_summary.json`).
- [ ] Generate publication-ready PNG figures in `outputs/figures/`:
  - `domain_shift_collapse.png` (Bar chart illustrating the 25–40% performance drop).
  - `gis_linear_unmixing_residuals.png` (Spatial heatmap of unmixing residuals on complex Indian agricultural parcels).
  - `sam_magnitude_confusion.png` (Confusion matrix highlighting SAM magnitude blindness).
  - `spatial_patch_fragmentation.png` (Visualizing multi-crop boundary contamination within smallholder patches).

---

## Verification & Acceptance Criteria

1. **Clean Pipeline Execution**: `bash run_pipeline.sh` completes end-to-end without errors.
2. **Empirical Grounding**:
   - `benchmark_results.csv` contains concrete test results for all 5 baseline architectures across Source Domain vs Indian Target Domain.
   - GIS spectroscopic baseline metrics (SAM OA, LSU $RMSE_A$) are calculated and documented.
3. **Artifact Quality**: All 4 figure PNGs are generated with high resolution (300 DPI), clean legends, and clear scientific labeling matching the terminology in `midterm_defense_grounding_and_gis_analysis.md`.
