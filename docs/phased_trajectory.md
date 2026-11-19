# BharatSpectral: Research Thread Phased Trajectory

This document defines the comprehensive, end-to-end research trajectory for the **BharatSpectral** foundation modeling and spectral intelligence framework.

---

## Phase 1: Data Infrastructure & Corpus Curation

### 1.1 Corpus Curation Strategy
**Objective:** Construct a high-entropy, physics-rich pre-training corpus representing the full complexity of Indian landscapes, avoiding the redundancy of "downloading the whole internet." The corpus acts as a foundational dataset to teach the model intrinsic material chemistry (reflectance physics) rather than sensor-specific or atmospheric artifacts.

#### A. Geographic & Agro-Ecological Scoping (The 5 Archetypes)
To ensure generalization across India's highly fragmented and diverse terrain, data is strictly curated across five landscape archetypes (target: 3–5 flightlines/scenes per archetype):
1. **Intensive Agriculture & Residue:** Indo-Gangetic Plains (Wheat-Paddy rotation, high N-fertilizer, stubble burning). Locations: Kurukshetra, Ludhiana.
2. **Rainfed Polyculture & Bare Soils:** Deccan Plateau & Central India (Cotton/Soybean, fragmented <0.5 ha plots, red/black soils). Locations: Vidarbha, Rayalaseema.
3. **Inland Water & Coastal Wetlands:** Lakes & Deltas (Chlorophyll-a, turbidity, salinity). Locations: Chilika Lake, Sundarbans.
4. **Forestry & Complex Canopy:** Forest Ecosystems (Multi-layer vegetation biochemicals). Locations: Western Ghats, Mudumalai.
5. **Mineralogy & Degraded Lands:** Mining belts (High-contrast geological endmembers). Locations: Jharia Coalfields.

#### B. Sensor & Product Level Strategy
*   **Product Standard:** Strictly Level-2A Bottom-of-Atmosphere (BOA) Surface Reflectance.
*   **Primary Pre-training Anchor (~80%): AVIRIS-NG India Campaign.** (4–8m GSD, 425 bands). Provides true sub-field fidelity, pure endmembers, and resolves sub-hectare plot fragmentation without spectral smearing.
*   **Spaceborne Transfer Set (~20%): NASA EMIT.** (~60m GSD, 285 bands). Spaceborne scenes overlapping AVIRIS-NG bounding boxes to enable zero-shot multi-sensor generalization.
*   **No Lossy Resampling:** Sensors are kept in their native spatial and spectral formats. The model handles multi-scale ingestion dynamically via the Scale-Spectral Positional Encoding (SSPE) architecture.

#### C. Volume Limits & Distillation Targets
*   **Target Volume:** ~120–150 GB raw data, compressing to ~80-100 GB ML-ready Zarr/HDF5 format.
*   **Data Yield:** ~100,000+ high-variance spatial-spectral patches.
*   **Model Sizing Pipeline:** The corpus is sized to optimally train a heavyweight Masked Autoencoder **Teacher (ViT-Base/Large: ~86M–300M parameters)** on AIRAWAT HPC. This teacher acts as a "neural surrogate physics engine," which will later be distilled down into a lightweight **Student (~1–5M parameters, <15 MB ONNX)** for execution on the Cloudflare WebGIS edge.
