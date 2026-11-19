# BharatSpectral: Data Aggregation & Curation Plan (10 GB R2 Strategy)

## 1. Executive Summary & Core Philosophy

Rather than attempting to download massive, uncurated swaths of the Indian subcontinent, **BharatSpectral** employs an **entropy-driven, targeted sampling paradigm**. In hyperspectral remote sensing and biochemical foundation modeling, spatial redundancy (e.g., thousands of square kilometers of identical bare soil or monoculture) bloats storage without imparting new physical knowledge.

This plan establishes a focused **10.0 GB data curation pipeline** calibrated specifically for **Cloudflare R2's free tier**:
* **Zero Storage Cost:** Exactly fits within the 10 GB standard storage monthly allowance.
* **Zero Egress Fees:** Cloudflare R2 imposes **$0.00 egress**, allowing high-frequency WebGIS tile streaming and interactive pixel-level spectral queries from client browsers worldwide without incurring bandwidth charges.
* **Maximum Radiative Information:** Concentrated on 3–4 high-entropy agro-ecological archetypes featuring distinct chemical and physical absorption regimes.

---

## 2. Sensor Selection: The Dual-Sensor Paradigm

The corpus pairs an ultra-high-resolution airborne anchor with spaceborne multi-scale validation:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   PRIMARY ANCHOR: AVIRIS-NG INDIA                      │
│  • Platform: Airborne (ISRO SAC / NASA JPL Flight Campaigns)           │
│  • Spectral: 380–2510 nm (425 contiguous bands @ 5.0 nm FWHM)          │
│  • Spatial: 4.0–8.0 m Ground Sampling Distance (GSD)                   │
│  • Purpose: Resolves sub-hectare (<0.5 ha) Indian plots, pure crop     │
│             endmembers, and sub-pixel parcel fragmentation             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Cross-scale validation & transfer
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   SPACEBORNE TRANSFER: NASA EMIT                       │
│  • Platform: International Space Station (ISS)                         │
│  • Spectral: 381–2493 nm (285 contiguous bands @ ~7.5 nm FWHM)         │
│  • Spatial: ~60.0 m Ground Sampling Distance (GSD)                     │
│  • Purpose: Validates regional spaceborne transfer, coarse unmixing,   │
│             and Scale-Spectral Positional Encoding (SSPE)              │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Cross-domain benchmark baseline
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             AUDIT BASELINE: INDIAN PINES (1992, PURDUE)                │
│  • Spatial: 20 m GSD | Spectral: 220 bands (200 calibrated)            │
│  • Purpose: Canonical baseline proving failure of Western models       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Curated Target Locations: 4 High-Entropy Archetypes

Four distinct geographic sites in India are selected to capture maximum physical diversity across agricultural, soil, aquatic, and geological regimes:

| Archetype | Target Geographic Area | Key Spectral Signatures & Physical Targets | Target Sensor Coverage |
|---|---|---|---|
| **1. Intensive Agriculture & Crop Residue** | **Anand / Gandhinagar (Gujarat)** or **Punjab / Haryana** | • Chlorophyll-a / Chlorophyll-b Red-Edge steepness (680–750 nm)<br>• Stubble/Residue Cellulose & Lignin SWIR peaks (2100–2300 nm)<br>• Nitrogen / Protein absorption features | AVIRIS-NG India flightlines + overlapping NASA EMIT |
| **2. Rainfed Polyculture & Semi-Arid Soil** | **Vidarbha (Maharashtra)** or **Rayalaseema (Andhra Pradesh)** | • High soil background reflectance<br>• Black cotton soils, Smectite/Montmorillonite clay (2200 nm)<br>• Iron oxides (Hematite/Goethite @ 450–900 nm)<br>• Severe moisture stress in cotton/pulses | AVIRIS-NG India flightlines + NASA EMIT |
| **3. Inland Wetland & Aquatic Interface** | **Chilika Lake (Odisha)** or **Gulf of Khambhat (Gujarat)** | • Rapid water absorption in NIR/SWIR ($R \to 0$)<br>• Suspended particulate matter & turbidity (550–650 nm)<br>• Algal blooms (cyanobacteria phycocyanin @ 620 nm)<br>• Salinity and coastal mudflat transitions | AVIRIS-NG India flightlines + NASA EMIT |
| **4. Mineralogy & Degraded Landscapes** | **Jharia Coal Belt (Jharkhand)** or **Western Rajasthan** | • Pure mineral endmembers: Kaolinite, Alunite, Calcite<br>• Carbonaceous coal dust absorption<br>• Pristine endmember library creation for VCA and LSU | AVIRIS-NG India flightlines |

---

## 4. 10.0 GB Cloudflare R2 Storage Budget Allocation

Hyperspectral cubes in 32-bit float format are unnecessarily heavy for distribution. By masking non-transmissive atmospheric bands and quantizing reflectance to scaled **uint16** ($[0, 10000]$ where $10000 = 100.0\%$ reflectance), volume is reduced by ~50% with zero loss of physical fidelity.

| Component | Raw Ingest Spec | Preprocessed / Quantized Format | Allocation |
|---|---|---|---|
| **AVIRIS-NG India Cubes** | 3–4 Level-2 Surface Reflectance flightlines across Archetypes 1, 2, and 4 | Cleaned uint16 NetCDF4/Zarr with atmospheric bands masked | **~5.0 GB** |
| **NASA EMIT India Granules** | 2–3 Level-2A Surface Reflectance granules (`EMIT_L2A_RFL`) | Cleaned uint16 NetCDF4/Zarr with ortho-rectified spatial grids | **~4.0 GB** |
| **Reference Baselines & Spectral Libraries** | Indian Pines (1992) baseline + USGS/ECOSTRESS pure mineral/vegetation libraries + India administrative GeoJSONs | MAT, CSV, GeoJSON | **~0.3 GB** |
| **WebGIS Layer Overviews & Buffer** | Multi-resolution visual COG pyramids (RGB, CIR, NDVI, NDRE) + Worker caches | Cloud-Optimized GeoTIFF (deflate) | **~0.7 GB** |
| **Total Corpus Size** | | | **~10.0 GB** |

---

## 5. Storage Architecture for Zero-Latency WebGIS Delivery

To serve continuous hyperspectral inspection over the web without downloading whole multi-gigabyte files to the browser:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                         CLOUDFLARE R2 STORAGE                          │
├───────────────────────────────────┬────────────────────────────────────┤
│   A. VISUAL STREAMING LAYERS      │   B. FULL-SPECTRUM CUBE STORAGE    │
│   • Format: Cloud-Optimized       │   • Format: Chunked Zarr v3 /      │
│     GeoTIFF (COG)                 │     Linear Binary with spatial idx │
│   • Compression: Deflate / LERC   │   • Bands: 425 / 285 clean bands   │
│   • Served: Directly to MapLibre  │   • Served: Via Cloudflare Worker  │
│     and Deck.gl tile workers      │     HTTP Range Requests            │
└─────────────────┬─────────────────┴──────────────────┬─────────────────┘
                  │                                    │
                  ▼                                    ▼
       Browser Map Viewport (60 FPS)      Pixel Click -> Sub-100ms
       Pan/Zoom False Color, NDVI,        425-band continuous curve
       Endmember Abundance Overlays       plot in client canvas
```

1. **Visual Display:** High-speed COG overviews serve RGB (Red-Green-Blue), CIR (Color Infrared: NIR-Red-Green), and spectral index layers (NDVI, NDRE, NDWI).
2. **Deep Spectral Inspection:** A Cloudflare Worker intercepts parcel clicks, issues an HTTP `Range: bytes=<start>-<end>` request into the Zarr/binary store on R2, extracts the single 425-band column (~850 bytes), and returns JSON to the browser within 50–100ms.

---

## 6. Acquisition Pipelines & Automation

### 6.1 NASA EMIT L2A Granule Ingestion
* **Product:** `EMIT_L2A_RFL` (Surface Reflectance).
* **Source:** NASA LP DAAC via CMR STAC API.
* **Credentials:** Free NASA Earthdata Login (`~/.netrc` or `EARTHDATA_USERNAME` / `EARTHDATA_PASSWORD`).
* **Tooling:** Python `earthaccess` library for programmatic search by bounding box over Gujarat, Maharashtra, and Andhra Pradesh, with automated multi-part download.

### 6.2 AVIRIS-NG India L2 Reflectance Flightlines
* **Product:** Level-2 Surface Reflectance (atmospherically corrected via ATREM/6S).
* **Source:** NASA JPL AVIRIS-NG Data Portal (`avirisng.jpl.nasa.gov`) and ISRO Bhoonidhi Portal (`bhoonidhi.nrsc.gov.in`).
* **Tooling:** Automated downloader querying the flightline index table, streaming tar.gz granules, and extracting `.hdr` and `.bil` files.

### 6.3 Baseline Dataset
* **Product:** Indian Pines (1992) corrected reflectance and ground truth matrices.
* **Source:** Purdue University / Remote Sensing Laboratory open mirrors.
* **Tooling:** Direct HTTPS acquisition in `src/data_ingestion/download_datasets.py`.

---

## 7. Execution Checklist & Milestones

- [ ] **Milestone 1: Ingestion Scripting (`src/data_ingestion/download_datasets.py`)**
  - Implement NASA Earthdata search & download handler (`earthaccess`).
  - Implement AVIRIS-NG India flightline retrieval and sample extraction.
  - Implement Indian Pines baseline verification and checksum test.
- [ ] **Milestone 2: Preprocessing & Atmospheric Band Masking (`src/data_ingestion/preprocess_cubes.py`)**
  - Mask non-transmissive water vapor absorption bands:
    - Band group 1: $1350\text{--}1420\,\text{nm}$
    - Band group 2: $1800\text{--}1950\,\text{nm}$
  - Quantize reflectance values to `uint16` with scale factor $10000$.
- [ ] **Milestone 3: Cloud-Native Packaging (`src/data_ingestion/prepare_r2_tiles.py`)**
  - Generate Cloud-Optimized GeoTIFFs (COGs) for false-color and NDVI/NDRE previews.
  - Package full spatial-spectral arrays into chunked Zarr v3 format.
- [ ] **Milestone 4: Cloudflare R2 Upload & Edge Range-Request Verification**
  - Configure `wrangler r2 object put` or S3-compatible SDK upload to the R2 bucket.
  - Verify HTTP `Range` query latency (<100ms) for arbitrary $(x, y)$ coordinate extraction.
