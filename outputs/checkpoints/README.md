# Model Checkpoints (`outputs/checkpoints/`)

This directory stores trained baseline model weights for spectral and spatial-spectral classification baselines on hyperspectral benchmarks.

---

## 💾 Saved Checkpoint Weights

| Checkpoint File | Architecture / Method | Format | Description |
|---|---|---|---|
| [`svm_rbf.joblib`](svm_rbf.joblib) | Support Vector Machine (RBF Kernel) | Scikit-learn Joblib | Classical machine learning baseline operating on 1D spectral signatures. |
| [`random_forest.joblib`](random_forest.joblib) | Random Forest (100 Trees) | Scikit-learn Joblib | Ensemble tree baseline for pixel-wise band importance and classification. |
| [`3d_cnn_hamida_et_al..pth`](3d_cnn_hamida_et_al..pth) | 3D-CNN (Hamida et al.) | PyTorch State Dict | Joint spatial-spectral 3D convolutional network. |
| [`hybridsn_3d_2d_cnn.pth`](hybridsn_3d_2d_cnn.pth) | HybridSN (Roy et al.) | PyTorch State Dict | Hybrid 3D-2D convolutional architecture for spectral feature extraction. |
| [`spectral_transformer.pth`](spectral_transformer.pth) | Spectral Transformer Baseline | PyTorch State Dict | Standard Vision Transformer encoder applied to spectral band tokens. |

---

## 🔬 Loading Checkpoints Example

```python
import torch, joblib

# Load PyTorch baseline (e.g. HybridSN or Spectral Transformer)
model_state = torch.load("outputs/checkpoints/hybridsn_3d_2d_cnn.pth", map_location="cpu")

# Load Classical Sklearn model (e.g. SVM or Random Forest)
rf_model = joblib.load("outputs/checkpoints/random_forest.joblib")
```
