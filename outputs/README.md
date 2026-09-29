# Experimental Outputs & Baseline Benchmarks (`outputs/`)

This directory houses experimental benchmarks, baseline model checkpoints, high-resolution figures, and statistical evaluations comparing classical GIS spectroscopic methods against deep learning and foundation model architectures.

---

## 📂 Subdirectories

| Directory | Content Description | Link |
|---|---|---|
| [`checkpoints/`](checkpoints/) | Trained weights for classical baselines (SVM, RF) and deep learning architectures (3D-CNN, HybridSN, Spectral Transformer). | [`checkpoints/README.md`](checkpoints/README.md) |
| [`figures/`](figures/) | High-resolution publication plots demonstrating domain shift collapse, fragmentation, and GIS residual failures. | [`figures/README.md`](figures/README.md) |
| [`tables/`](tables/) | Structured benchmark evaluations (`benchmark_results.csv`), cross-scene transfer metrics, and GIS comparison JSONs. | [`tables/README.md`](tables/README.md) |

---

## 📊 Summary of Baseline Findings
* Classical GIS methods (**SAM**, **Linear Spectral Unmixing**) achieve fast deterministic outputs but suffer high error rates under intra-class illumination variations and complex canopy mixing.
* Deep learning baselines trained on single scenes (e.g. Indian Pines) experience severe performance drop (**> 35% accuracy collapse**) when transferred to Indian agricultural scenes without Scale-Spectral Positional Encoding (SSPE) and reflectance normalization (RNRL).
