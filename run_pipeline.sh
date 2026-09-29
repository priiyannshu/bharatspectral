#!/data/data/com.termux/files/usr/bin/bash
# run_pipeline.sh - BharatSpectral Phase 1 & 2 Benchmark & GIS Baseline Pipeline
# Executes end-to-end verification of datasets, baselines, GIS spectroscopy, metrics, and figures.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "================================================================="
echo "🛰️  BharatSpectral Phase 1 & 2 Benchmark & GIS Baseline Suite"
echo "================================================================="

echo "1. Milestone 1: Verifying Environment & Directories..."
python3 src/data_ingestion/download_datasets.py

echo "2. Milestone 2: Testing Hyperspectral Cube Preprocessing & Patch Sampling..."
python3 src/data_ingestion/preprocess_cubes.py
python3 src/data_ingestion/patch_generator.py

echo "3. Milestone 3: Verifying Baseline Architectures (RF, SVM, HybridSN, 3D-CNN, Spectral Transformer)..."
python3 src/baselines/classical_ml.py
python3 src/baselines/hybrid_sn.py
python3 src/baselines/cnn3d.py
python3 src/baselines/spectral_transformer.py

echo "4. Milestone 4: Verifying GIS Physical Spectroscopy (VCA, SAM, LSU/FCLS, Continuum Removal)..."
python3 src/gis_spectroscopy/endmember_vca.py
python3 src/gis_spectroscopy/sam_classifier.py
python3 src/gis_spectroscopy/linear_unmixing.py
python3 src/gis_spectroscopy/continuum_removal.py

echo "5. Milestone 5: Evaluating Cross-Domain Results & Verifying Figures..."
python3 src/evaluation/metrics.py
python3 src/baselines/evaluate_cross_scene.py
python3 src/evaluation/generate_figures.py

echo "================================================================="
echo "✅ BharatSpectral Phase 1 & 2 Pipeline Execution Complete!"
echo "All baseline checkpoints, benchmark tables, and figures verified."
echo "================================================================="
