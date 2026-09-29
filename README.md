# BharatSpectral: Democratized Spectral-Semantic Intelligence (DSSI)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Mission](https://img.shields.io/badge/National%20Mission-IndiaAI%20%7C%20ISRO-orange)](https://indiaai.gov.in/)

BharatSpectral is a dual-pillar hyperspectral foundation model and geospatial public infrastructure initiative tailored for Indian Earth Observation (EO). It addresses smallholder agricultural fragmentation, multi-crop intercropping, multi-season phenology, and multi-sensor heterogeneity across **AVIRIS-NG India** (425 bands), **ISRO HysIS** (220 bands), and **NASA EMIT** (285 bands).

---

## 🏛️ Dual-Pillar Framework

```text
┌──────────────────────────────────────────────────────────────────┐
│                     RESEARCH PILLAR                              │
│   BharatSpectral-MAE: Physics-Informed Foundation Model          │
│   Innovations: SSPE · RNRL · SHT · AAM · ECSA · Ph-LoRA · FASU  │
│   Sensors: AVIRIS-NG India · NASA EMIT · ISRO HysIS              │
│   Benchmark: BharatHSI-Bench                                     │
└────────────────────────────┬─────────────────────────────────────┘
                             │ Inference Engine
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                     PRODUCT PILLAR                               │
│   BharatSpectral Platform: WebGIS Public Infrastructure          │
│   Stack: Cloudflare R2 (zero-egress) · Workers (ONNX) · MapLibre │
└──────────────────────────────────────────────────────────────────┘
```

1. **Research Pillar (BharatSpectral-MAE):** A 100M-parameter physics-informed hyperspectral Masked Autoencoder designed with 7 novel architectural mechanisms for complex tropical agroecosystems.
2. **Product Pillar (BharatSpectral WebGIS Platform):** A zero-cost, citizen-facing Digital Public Infrastructure (DPI) delivering sub-pixel biochemical analytics (crop nutrients, soil health, water quality) with sub-second serverless edge inference on Cloudflare Workers (ONNX Runtime Web).

---

## 📂 Repository Directory Structure

| Directory | Description | Readme Link |
|---|---|---|
| [`docs/`](docs/) | Master capstone synopsis, thesis defense grounding, execution plan, and interactive phase reports | [`docs/README.md`](docs/README.md) |
| [`presentation/`](presentation/) | 16:9 Widescreen slide deck (PPTX) and interactive Web presentation generators | [`presentation/README.md`](presentation/README.md) |
| [`narratives/`](narratives/) | "Grand Narrative" 7-chapter foundational primer, physics theory, and compiled PDFs | [`narratives/README.md`](narratives/README.md) |
| [`outputs/`](outputs/) | Baseline model checkpoints, benchmark tables, cross-scene evaluations, and figure artifacts | [`outputs/README.md`](outputs/README.md) |

---

## 🔬 The 7 Core Architectural Innovations

* **SSPE (Scale-Spectral Positional Encoding):** Jointly encodes Ground Sample Distance (GSD: 4m–60m), spectral resolution, and mixture entropy.
* **RNRL (Reflectance-Normalized Reconstruction Loss):** Dynamically scales reconstruction errors by spectral reflectance magnitude to resolve low-reflectance SWIR features (< 5%).
* **SHT (Spectral Harmonic Tokenizer):** Dynamically chunks spectral bands according to absorption density (finer tokens in Red-Edge).
* **AAM (Atmospheric Absorption Masking):** Structured masking across physical atmospheric water vapor / CO₂ bands ($1350\text{--}1420\,\text{nm}$, $1800\text{--}1950\,\text{nm}$).
* **ECSA (Endmember-Constrained Self-Attention):** Physical spectral unmixing regularizer guiding Transformer attention heads to physically valid spectral mixtures.
* **Ph-LoRA (Phenology-Conditioned LoRA):** Crop calendar and season-aware low-rank adapters (Kharif, Rabi, Zaid).
* **FASU (Foundation-Augmented Spectral Unmixing):** Sub-pixel canopy decomposition head operating directly on pre-trained foundation embeddings.

---

## 🚀 Quickstart & Workflows

### Generating Presentations
* **Generate PowerPoint (`.pptx`):**
  ```bash
  python3 presentation/build_deck.py
  ```
* **Generate Web Slides (`.html`):**
  ```bash
  python3 presentation/build_html_deck.py
  ```

### Rebuilding Grand Narrative PDFs
```bash
python3 narratives/convert_md_to_pdf.py
```

---

## 👥 Team Orientation & Reading Guide

If you are new to the codebase, follow this onboarding sequence:
1. Read the **Grand Narrative** in [`narratives/`](narratives/) for physics, AI principles, and problem intuition.
2. Review the **Master Plan & Synopsis** in [`docs/`](docs/) for research milestones and architectural proofs.
3. Inspect benchmark figures and metrics in [`outputs/`](outputs/).
4. Check [`AGENTS.md`](AGENTS.md) before writing or refactoring foundation model code.
