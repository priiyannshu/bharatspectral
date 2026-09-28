# CAPSTONE PROJECT SYNOPSIS

## Project Title
**BharatSpectral: Democratized Spectral Intelligence for Indian Earth Observation Through Physics-Informed Foundation Modeling and Public Geospatial Infrastructure**

---

## Executive Summary & Dual-Pillar Framework

This capstone engineers a new category of geospatial capability — **Democratized Spectral-Semantic Intelligence (DSSI)** — through a synergistic Dual-Pillar Framework:

1. **The Research Pillar (Spectral Foundation Modeling):** Designs **BharatSpectral-MAE**, the first hyperspectral Foundation Model engineered for the spatial fragmentation, sub-pixel spectral mixing, and multi-season phenological complexity unique to Indian landscapes. Existing Foundation Models (SpectralGPT, HyperSIGMA, SS-MAE) are pre-trained on homogeneous Western benchmarks and fail on Indian smallholder topography. BharatSpectral-MAE introduces seven named architectural innovations — physics-informed pre-training losses, sensor-adaptive tokenization, atmosphere-aware masking, and endmember-constrained attention — to close this gap.

2. **The Product Pillar (Spectral Public Infrastructure):** Builds **BharatSpectral Platform**, a free, publicly accessible, citizen-facing WebGIS that embeds BharatSpectral-MAE as its inference engine. It delivers biochemical-grade spectral analytics — crop nutrient mapping, soil health assessment, water quality monitoring — as open Digital Public Infrastructure, solving the structural cost and compute bottlenecks that have kept hyperspectral analysis locked inside desktop software and commercial SaaS platforms.

```text
┌──────────────────────────────────────────────────────────────────┐
│                     RESEARCH PILLAR                              │
│                                                                  │
│   BharatSpectral-MAE: Physics-Informed Spectral Foundation Model │
│   for Indian Multi-Sensor Hyperspectral Data                     │
│                                                                  │
│   Innovations: SSPE · RNRL · SHT · AAM · ECSA · Ph-LoRA · FASU  │
│   Sensors: AVIRIS-NG India · NASA EMIT · ISRO HysIS              │
│   Benchmark: BharatHSI-Bench                                     │
└────────────────────────────┬─────────────────────────────────────┘
                             │ Provides Inference Engine
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                     PRODUCT PILLAR                               │
│                                                                  │
│   BharatSpectral Platform: Spectral Digital Public               │
│   Infrastructure for Citizen-Facing Hyperspectral Analytics      │
│                                                                  │
│   Stack: Cloudflare R2 (zero-egress) · Workers (edge inference)  │
│   · Pages + MapLibre (citizen frontend)                          │
└──────────────────────────────────────────────────────────────────┘
```

---

## The Intelligence Being Created

Existing Indian agricultural platforms — ISRO Krishi-DSS, SatSure, Cropin — operate on multispectral imagery (10–12 broad spectral bands). They provide **biophysical** intelligence: they detect that a crop is stressed. They cannot determine *why*. The spectral resolution is too coarse to isolate specific biochemical signatures.

BharatSpectral operates on hyperspectral imagery (200–425 continuous narrow bands spanning 380–2500 nm). It provides **biochemical** intelligence: it identifies that a crop is nitrogen-deficient by detecting absorption at 720 nm, diagnoses early-stage leaf rust from the Red-Edge inflection at 680 nm, and maps Soil Organic Carbon from SWIR absorption at 2200 nm — all 7 to 14 days before visible symptoms appear, at sub-pixel resolution, through a publicly accessible interface that requires no spectroscopy expertise to operate.

The precise intelligence type this system creates is **Democratized Spectral-Semantic Intelligence (DSSI)**: the automated translation of high-dimensional spectral reflectance signatures into actionable, semantically-labeled geospatial insights — delivered at sub-pixel resolution through free public infrastructure to non-specialist users. DSSI bridges laboratory-grade spectroscopy and field-level decision-making by embedding a self-supervised Foundation Model's learned spectral physics into a zero-cost citizen platform.

---

## Pillar 1: The AI Research Component

### Problem Statement 1 (Domain: Deep Learning & Remote Sensing)

The current state-of-the-art in hyperspectral Foundation Models — SpectralGPT (Hong et al., IEEE TPAMI 2024), HyperSIGMA, SS-MAE (Lin et al., IEEE TGRS 2024) — represents significant progress in self-supervised spectral representation learning. However, these models are pre-trained on datasets structurally unrepresentative of Indian landscapes: Indian Pines (Indiana, USA, 1992 — large rectilinear monoculture), Pavia University (Italy — urban), WHU-Hi (China — semi-suburban), Houston (USA — urban). The canonical "Indian Pines" benchmark shares zero geographical, ecological, or agronomic characteristics with Indian agriculture.

Indian smallholder landscapes present four compounding challenges that these models were never designed to handle:

- **Extreme spatial fragmentation.** The average Indian farm is 1.08 hectares (Agricultural Census 2015-16). Millions of plots fall below 0.5 ha. At spaceborne resolution (30–60 m), individual pixels routinely contain multiple crop types, boundary vegetation, and irrigation infrastructure. Every classification is a sub-pixel unmixing problem.
- **Severe intercropping spectral mixing.** Standard Indian practice co-plants two to three crops simultaneously (sorghum with pigeon pea, maize with groundnut). The resulting spectral signatures are non-linear mixtures absent from Western benchmarks where monoculture is the norm.
- **Multi-season phenological complexity.** India's three growing seasons — Kharif (June–October), Rabi (October–March), Zaid (March–June) — produce dramatically different spectral phenologies across identical geographies. Models trained on single-season assumptions exhibit catastrophic temporal drift.
- **Multi-sensor spatial-spectral heterogeneity.** No published work harmonizes airborne AVIRIS-NG (4–8 m GSD, 425 bands), spaceborne NASA EMIT (60 m GSD, 285 bands), and ISRO HysIS (30 m GSD, 220 bands) — instruments with different spectral response functions, noise profiles, and atmospheric correction artifacts, separated by a 10× spatial resolution gap.

This research tackles these challenges by engineering **BharatSpectral-MAE** — a physics-informed spectral Foundation Model built on seven named architectural innovations, each addressing a specific failure mode of existing approaches:

| ID | Named Innovation | What It Solves |
|---|---|---|
| **SSPE** | **Scale-Spectral Positional Encoding** | Extends Scale-MAE (Reed et al., ICCV 2023) from spatial-only GSD conditioning into the hyperspectral regime: jointly encodes spatial ground sample distance, spectral bandwidth, and expected spectral mixture entropy across three sensors. Existing scale-aware encodings ignore the spectral dimension entirely. |
| **RNRL** | **Reflectance-Normalized Reconstruction Loss** | Physics-informed normalization of the self-supervised reconstruction objective by target reflectance magnitude, forcing the model to learn subtle spectral variations in low-reflectance domains (inland water bodies at < 5% SWIR reflectance, cyanobacterial blooms) rather than discarding them as noise. Standard MAE losses (MSE, MSE+SAD) are dominated by high-variance land features. No published precedent in self-supervised HSI pre-training. |
| **SHT** | **Spectral Harmonic Tokenizer** | Sensor-adaptive 3D tokenizer that dynamically adjusts spectral chunking by absorption-feature density — fine-grained tokens (4×4 spatial × 4 spectral) in diagnostic Red-Edge regions (700–750 nm), coarser tokens in smooth continuum regions — and ingests different band counts (425, 285, 220) from three sensors into a unified token space. Replaces the fixed patch dimensions (e.g., SpectralGPT's static 3D tokenization) that ignore spectral information density. |
| **AAM** | **Atmospheric Absorption Masking** | Replaces standard random masking (75% in MAE/SatMAE, 90% in SpectralGPT) with structured spectral-gap masking that simulates atmospheric water vapor absorption (1350–1420 nm, 1800–1950 nm) and CO₂ interference. Forces the model to learn radiative transfer physics by reconstructing spectrally absent bands from surrounding spectral context — a physics-informed pre-training paradigm rather than arbitrary stochastic dropout. |
| **ECSA** | **Endmember-Constrained Self-Attention** | Regularizes the Transformer's self-attention by a spectral unmixing prior, forcing the model to attend to pixels containing physically similar materials (based on spectral endmember similarity) rather than merely spatially adjacent textures. Addresses the Indian fragmentation problem directly: neighbouring pixels across a plot boundary belong to entirely different crops. No existing attention mechanism is conditioned on spectral unmixing physics. |
| **Ph-LoRA** | **Phenology-Conditioned Low-Rank Adaptation** | Parameter-Efficient Fine-Tuning where low-rank adapter weights are dynamically modulated by crop growth stage embeddings encoding season (Kharif/Rabi/Zaid) and phenological phase. A model predicting soil nitrogen in April (pre-sowing bare soil) requires fundamentally different spectral attention patterns than one mapping Kharif paddy canopy in September. No published season-conditioned PEFT mechanism exists. |
| **FASU** | **Foundation-Augmented Spectral Unmixing** | Sub-pixel unmixing head operating on the Foundation Model's pre-trained spectral representations rather than training a standalone autoencoder from scratch. Decomposes mixed pixels into constituent material abundances using learned features that already encode cross-domain spectral physics, enabling unmixing even with limited labeled endmember data. |

The Foundation Model is self-supervised on unlabelled multi-sensor Indian data, with its **first downstream application** explicitly fine-tuning through Ph-LoRA and FASU heads for Indian precision agriculture — mapping crop type, nutrient status, and soil composition at sub-pixel granularity across smallholder landscapes — establishing a validated pathway for future adaptation to water quality and pollution monitoring domains.

### Research Action Objectives

*   **RO1 (Data Acquisition & Benchmark Creation):** To acquire Indian hyperspectral datasets from ISRO AVIRIS-NG campaigns (via Bhoonidhi), NASA EMIT (via LP DAAC), and ISRO HysIS; to establish a standardized preprocessing pipeline with atmospheric correction, Bad Band Removal, and Zarr/COG export; and to produce **BharatHSI-Bench** — India's first open, labeled hyperspectral agricultural benchmark dataset with standardized train/test/validation splits, crop-type ground truth, and reproducible evaluation protocols. No such benchmark currently exists; the field's reliance on Indian Pines (a 1992 American dataset) as a proxy for Indian agriculture is a documented methodological deficiency.

*   **RO2 (SOTA Failure Documentation):** To rigorously evaluate existing Foundation Models (SpectralGPT, HyperSIGMA) and standard baselines (HybridSN, 3D-CNN) — trained on their original Western/Chinese datasets — directly on BharatHSI-Bench, quantifying the domain-shift degradation and establishing the empirical justification for BharatSpectral-MAE. The expected 15–30% Overall Accuracy drop under cross-scene transfer constitutes the scientific case for domain-specific foundation modeling.

*   **RO3 (Architectural Innovation & Pre-training):** To design, implement, and pre-train BharatSpectral-MAE with the seven named innovations (SSPE, RNRL, SHT, AAM, ECSA, Ph-LoRA, FASU) on multi-sensor Indian data using AIRAWAT DGX A100 distributed compute (PyTorch DDP, bfloat16 mixed precision, gradient checkpointing), followed by Ph-LoRA downstream fine-tuning for agriculture.

*   **RO4 (Evaluation & Ablation):** To benchmark BharatSpectral-MAE against SpectralGPT, HyperSIGMA, SS-MAE, and classical baselines on BharatHSI-Bench using Overall Accuracy, Average Accuracy, Kappa Coefficient ($\kappa$), and sub-pixel unmixing RMSE on abundance fractions. Systematic ablation studies will isolate the marginal contribution of each named component (SSPE, RNRL, AAM, ECSA, Ph-LoRA, FASU) to final performance.

---

## Pillar 2: The Software Engineering Component

### Problem Statement 2 (Domain: Software Architecture & Geospatial Public Infrastructure)

Despite India ranking among the top five remote sensing data-generating nations globally, a verified translational gap persists in the operationalization of hyperspectral data. An exhaustive audit of the Indian geospatial ecosystem in 2026 confirms:

| Platform | Modality | Access Model | Hyperspectral Inference | Gap |
|---|---|---|---|---|
| **ISRO Bhuvan / Krishi-DSS** | Multispectral (LISS, Sentinel-2, AWiFS) | Public (limited) | None | No HSI analytics |
| **ISRO VEDAS (AVHYAS)** | Hyperspectral | Desktop QGIS plugin (local install) | Offline only | Not web-accessible |
| **ISRO Bhoonidhi** | Raw data catalog | Public (registration) | None — raw ENVI download only | No analytics engine |
| **Pixxel Aurora** | Hyperspectral (proprietary) | Commercial B2B SaaS | Yes | Not public — enterprise pricing |
| **Google Earth Engine** | Hosts EMIT data | PaaS (requires coding) | No built-in HSI models — user must code | Requires developer expertise |
| **SatSure / Cropin** | Multispectral + SAR | Commercial B2B | None | No HSI capability |

Three structural bottlenecks explain why no public hyperspectral analytics tool has been built:

1. **Data volume.** A single hyperspectral scene (2–10 GB) overwhelms traditional WebGIS tile architectures. Serving multi-band cubes to thousands of concurrent users on conventional cloud infrastructure is economically prohibitive.
2. **Egress costs.** Streaming raw spectral data from AWS S3 or GCP Cloud Storage incurs escalating egress fees that make sustained public hosting financially unviable.
3. **Inference compute.** Hyperspectral model inference (200+ input bands, spatial-spectral feature extraction, unmixing) demands compute resources traditionally available only in desktop or HPC environments.

This project solves all three through **BharatSpectral Platform** — an open, citizen-facing Spectral Digital Public Infrastructure — built on a serverless architecture that eliminates each bottleneck:

| Bottleneck | Solution | Named Innovation |
|---|---|---|
| Data volume | Cloud-Optimized GeoTIFFs (COG) and Zarr datacubes with HTTP Range request streaming, eliminating full-scene transfer | **Zero-Egress Spectral Tile Streaming** |
| Egress costs | Cloudflare R2 object storage with zero data egress fees, reducing marginal serving cost to near-zero regardless of user volume | Architecture-level cost innovation |
| Inference compute | Distilled lightweight student model executing directly on Cloudflare Workers V8 isolates via ONNX, solving the 128 MB memory constraint through spectral-spatial tiling | **Serverless Spectral Inference (SSI)** |

The platform translates BharatSpectral-MAE's learned spectral physics into a visual interface that a Block Development Officer, agricultural extension worker, or farmer cooperative can operate without spectroscopy training — converting 200-band tensors into actionable map overlays showing crop stress, nutrient deficiency, and soil composition at every pixel.

### Software Engineering Action Objectives

*   **EO1 (Platform Architecture):** To design and develop BharatSpectral Platform as a web application using Next.js on Cloudflare Pages with MapLibre GL JS for geospatial rendering, Cloudflare R2 for zero-egress hyperspectral tile storage, and Cloudflare Workers for edge API routing and Serverless Spectral Inference.

*   **EO2 (Model Distillation for Web Deployment):** To architect a distillation pipeline compressing BharatSpectral-MAE into a lightweight student model deployable within Cloudflare Workers' memory and CPU constraints, optimizing for sub-second inference latency per tile without sacrificing spectral discrimination fidelity on critical absorption features.

*   **EO3 (Compute & Data Infrastructure):** To establish the development workflow on AIRAWAT HPC (DGX A100 clusters) for Foundation Model pre-training, leverage AIKosh as the model/dataset repository, and publish BharatHSI-Bench as an open community resource.

*   **EO4 (System Validation & Cost Benchmarking):** To validate end-to-end platform performance against quantified targets — inference latency under 5 seconds per km² on Workers, tile rendering under 200 ms on the client — and benchmark the total hosting cost of the Cloudflare R2 + Workers architecture against an equivalent AWS EC2 + GeoServer deployment to quantify the economic viability of sustained public operation.

---

## Competitive Positioning

```text
 EXISTING FOUNDATION MODELS              WHY THEY FAIL ON INDIAN DATA
 ─────────────────────────               ──────────────────────────────
 SpectralGPT (TPAMI 2024)         →  Trained on global benchmarks; no
 HyperSIGMA                            Indian smallholder data; assumes
 SS-MAE (TGRS 2024)                    large homogeneous plots; single-
                                        sensor; no physics-informed loss
                                        for low-reflectance domains.

 EXISTING INDIAN PLATFORMS               WHY THEY CAN'T DO THIS
 ─────────────────────────               ──────────────────────────────
 Krishi-DSS (ISRO)                →  Multispectral only — detects stress,
 SatSure / Cropin                       cannot identify biochemical cause.
 Pixxel Aurora                    →  Commercial B2B — not public infra.
 GEE                              →  PaaS — requires coding expertise;
                                        no embedded HSI inference models.
```

**BharatSpectral occupies the intersection that neither group covers:** a Foundation Model trained on Indian hyperspectral data, deployed as free public infrastructure with embedded inference.

---

## Summary of Named Novel Contributions

**Architecture (7):**
SSPE · RNRL · SHT · AAM · ECSA · Ph-LoRA · FASU

**Data (3):**
BharatHSI-Bench (India's first open HSI agricultural benchmark) · Multi-Sensor Indian Spectral Datacube · Spectral-SoilHealth Paired Dataset (HSI matched with Soil Health Card NPK/OC measurements)

**Platform (3):**
BharatSpectral Platform (first public-access WebGIS with embedded HSI Foundation Model inference) · Serverless Spectral Inference · Zero-Egress Spectral Tile Streaming
