# AGENTS.md — Developer & AI Agent Context for BharatSpectral

Welcome to the **BharatSpectral** codebase. This document serves as the authoritative operational manual for AI agents and human developers collaborating on this project.

---

## 1. Project Philosophy: The Platform-First Paradigm

**BharatSpectral** democratizes hyperspectral Earth Observation for Indian smallholders and public agencies through **Democratized Spectral-Semantic Intelligence (DSSI)**.

### The "Reverse Engineering" Paradigm
Historically, remote sensing research builds heavyweight neural networks in isolation and treats user delivery as an afterthought. **BharatSpectral works backwards:**

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   STEP 1: THE WEBGIS PLATFORM (DPI)                    │
│  • Public, zero-cost, browser-native WebGIS interface (MapLibre/Deck)   │
│  • Serverless Spectral Inference (SSI) via Cloudflare Workers + R2     │
│  • Pixel-level interactive spectral curve inspection & GeoJSON layers  │
│  • Deterministic Physical GIS Spectroscopy Baseline (VCA, SAM, LSU)    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Identifies real bottlenecks
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   STEP 2: THE NEURAL SURROGATE ENGINE                  │
│  • BharatSpectral-MAE Foundation Model (trained on AIRAWAT DGX A100)   │
│  • Physics-informed self-supervised learning on Indian agroecosystems  │
│  • Distilled lightweight ONNX models (<15 MB) injected into WebGIS    │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Build the Platform First:** Create a fully functional, zero-barrier WebGIS application delivering continuous hyperspectral inspection and physical spectroscopic analytics (continuum removal, spectral angle mapping, linear unmixing) directly in the browser.
2. **Build the Model Second:** Once the platform, ingestion pipelines, tile serving, and physical baselines are operational, train and distill **BharatSpectral-MAE** to replace traditional linear GIS tools with non-linear biochemical intelligence.

---

## 2. Platform Architecture & Technology Stack

The platform is engineered as open **Digital Public Infrastructure (DPI)**:

* **Frontend / GIS Layer:**
  * **Map Engine:** MapLibre GL JS / Deck.gl for 2.5D/3D geospatial visualization.
  * **Layer Support:** Cloud-Optimized GeoTIFF (COG), Zarr/HDF5 tiles, and administrative GeoJSON boundaries ([`data/geo/india.geojson`](file:///home/deadpool/omniverse/btp/data/geo/india.geojson), [`data/geo/states.geojson`](file:///home/deadpool/omniverse/btp/data/geo/states.geojson)).
  * **Spectral Visualizer:** Interactive 425-band spectral curve plotting tool for clicked pixels or drawn polygon parcels.
* **Edge & Delivery Layer (Cloudflare SSI):**
  * **Storage:** Cloudflare R2 zero-egress bucket storing calibrated HSI flightlines (AVIRIS-NG India, NASA EMIT, ISRO HysIS).
  * **Edge Compute:** Cloudflare Workers (V8 Isolates) routing range requests and serving tiles.
  * **In-Browser / Edge Inference:** ONNX Runtime Web with WebAssembly / WebGPU execution for sub-second client-side unmixing.
* **Deterministic GIS Analytics Engine (`src/gis_spectroscopy/`):**
  * Exposes classical spectroscopy tools directly inside the UI as baseline analytical modes before deep learning inference.

---

## 3. Directory Layout & Key Modules

```text
/home/deadpool/omniverse/btp/
├── README.md                                  # Repository overview & quickstart
├── AGENTS.md                                  # Developer & AI Agent context (this file)
├── .gitignore                                 # Git exclusion rules
│
├── data/                                      # Spatial & Spectral Datasets
│   ├── geo/                                   # Administrative vector boundaries
│   │   ├── india.geojson                      # National boundary polygon
│   │   └── states.geojson                     # State-level boundary polygons
│   ├── raw/                                   # Raw HSI data granules & flightlines
│   └── processed/                             # Processed patches & endmember spectral libraries
│
├── src/                                       # Core Implementation
│   ├── gis_spectroscopy/                      # Deterministic Physical Spectroscopy Suite
│   │   ├── continuum_removal.py               # Convex hull continuum removal for absorption depth
│   │   ├── endmember_vca.py                   # Vertex Component Analysis endmember extraction
│   │   ├── linear_unmixing.py                 # Fully Constrained Least Squares (FCLS) unmixing
│   │   └── sam_classifier.py                  # Spectral Angle Mapper similarity classifier
│   ├── data_ingestion/                        # Preprocessing & Tile Generation
│   │   ├── preprocess_cubes.py                # BOA reflectance calibration & band alignment
│   │   ├── patch_generator.py                 # Spatial-spectral patch extraction
│   │   └── download_datasets.py               # Automated acquisition (Bhoonidhi, NASA Earthdata)
│   ├── baselines/                             # Classical & Deep Learning Transfer Baselines
│   │   ├── classical_ml.py                    # SVM (RBF) & Random Forest classifiers
│   │   ├── cnn3d.py                           # 3D-CNN spectral-spatial architecture
│   │   ├── hybrid_sn.py                       # HybridSN (3D/2D CNN) baseline
│   │   ├── spectral_gpt.py                    # SpectralGPT transfer baseline
│   │   └── ss_mae.py                          # SS-MAE baseline
│   └── evaluation/                            # Validation & Cross-Scene Benchmarking
│       ├── metrics.py                         # Overall Accuracy, Kappa, RMSE_A unmixing error
│       ├── evaluate_cross_scene.py            # Indian Pines -> Indian smallholder transfer audit
│       └── generate_figures.py                # Comparative benchmark visualizations
│
├── notebooks/                                 # Research Notebooks
│   └── 03_hyperspectral_information.ipynb     # Spectral entropy & radiative transfer math
│
├── docs/                                      # Specifications & Research Grounding
│   ├── VISION.md                              # Master capstone vision & dual-pillar manifesto
│   ├── MASTER_PLAN.md                         # Detailed milestone roadmap
│   ├── project_synopsis.md                    # Formal project proposal & technical synopsis
│   ├── red_team_validation.md                 # 6-Agent adversarial audit & novelty proof
│   ├── phased_trajectory.md                   # 5 agro-ecological landscape archetypes
│   └── midterm_defense_grounding_and_gis_analysis.md # Physical proof of GIS limitations
│
├── narratives/                                # "Grand Narrative" 7-Chapter Theory Primer
│   ├── 00_master_narrative_overview.md ... 06_literature_references_and_reading_guide.md
│   └── convert_md_to_pdf.py                   # ReportLab PDF compiler
│
├── outputs/                                   # Experimental Metrics & Visualizations
│   ├── figures/                               # Cross-scene collapse & domain shift plots
│   ├── tables/                                # Evaluation JSONs and benchmark CSVs
│   └── checkpoints/                           # Model weights & exported ONNX models
│
├── scripts/                                   # Distributed Compute Scripts
│   └── airawat_slurm_spectral_mae.sh          # AIRAWAT DGX A100 Distributed Slurm Training
│
└── archive/                                   # Historical ideation & transcripts
    └── enlightenment/                         # Early brainstorming transcripts
```

---

## 4. The 7 Core Architectural Innovations (Neural Engine Roadmap)

When designing the foundation model layer to plug into the WebGIS platform, preserve these 7 named innovations:

| ID | Name | Role in Platform Inference |
|---|---|---|
| **SSPE** | **Scale-Spectral Positional Encoding** | Dynamically ingests multi-sensor data (AVIRIS-NG 4–8m, ISRO HysIS 30m, EMIT 60m) without spatial resampling. |
| **RNRL** | **Reflectance-Normalized Reconstruction Loss** | Resolves subtle diagnostic SWIR absorption features (< 5% reflectance) such as cellulose and soil minerals. |
| **SHT** | **Spectral Harmonic Tokenizer** | Chunks bands adaptively according to physical absorption density (fine tokens across the Red-Edge, coarse across NIR plateaus). |
| **AAM** | **Atmospheric Absorption Masking** | Masks opaque atmospheric water vapor / CO₂ bands ($1350\text{--}1420\,\text{nm}$, $1800\text{--}1950\,\text{nm}$) to focus on ground chemistry. |
| **ECSA** | **Endmember-Constrained Self-Attention** | Guides attention heads using physical convex geometry to maintain valid fractional abundance mixtures. |
| **Ph-LoRA** | **Phenology-Conditioned LoRA** | Compact low-rank adapters tailored to Indian crop seasons (Kharif, Rabi, Zaid) for lightweight edge switching. |
| **FASU** | **Foundation-Augmented Spectral Unmixing** | Sub-pixel unmixing head producing instant abundance maps (crop health, sodicity, water toxins) for display on WebGIS layers. |

---

## 5. Development Principles for AI Agents

1. **Platform First, Always:** When authoring new code or tools, ask: *How does this run or render inside the WebGIS?* If a proposed model or format cannot be served or inspected over the web, adapt it (e.g., export to ONNX, COG, or GeoJSON).
2. **Physical Spectroscopy as the Anchor:**
   - Always retain deterministic physical tools ([`src/gis_spectroscopy/`](file:///home/deadpool/omniverse/btp/src/gis_spectroscopy/)) as the ground-truth baseline.
   - Do not discard physical principles (radiative transfer, absorption band physics) in favor of opaque black-box heuristics.
3. **Sensor Correctness:**
   - Primary high-resolution dataset: **AVIRIS-NG India** (425 bands, 4–8m GSD, Bhoonidhi).
   - Spaceborne transfer datasets: **ISRO HysIS** (220 bands, 30m GSD) and **NASA EMIT** (285 bands, 60m GSD).
   - **Indian Pines** (1992, Indiana, USA) is strictly a baseline transfer audit dataset—never confuse it with real Indian landscapes.
4. **Lean & Modular Code:**
   - Avoid bloated monolithic frameworks. Prefer standard scientific Python (`numpy`, `scipy`, `rasterio`, `shapely`, `torch`) and modern web standards.
   - Verify all scripts and pipeline tools after modification to ensure zero broken dependencies.
