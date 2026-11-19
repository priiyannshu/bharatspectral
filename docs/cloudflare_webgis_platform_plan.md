# BharatSpectral — Cloudflare WebGIS Platform Plan

## Executive Summary
This document specifies the architecture, UI/UX specification, data ingestion pipeline, and implementation roadmap for the **BharatSpectral WebGIS Platform**, engineered as a decoupled, zero-barrier Digital Public Infrastructure (DPI) on the **Cloudflare Ecosystem**.

The platform is engineered as a clean, hyper-functional remote sensing workstation void of marketing filler or promotional AI text. Users explore high-resolution hyperspectral flightlines across India, click any parcel to inspect real continuous 425-band reflectance curves (380–2510 nm), examine physical spectroscopy metrics (continuum removal, FCLS unmixing, narrowband indices), and optionally consult an on-demand, data-grounded Remote Sensing Specialist drawer.

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          CLOUDFLARE PLATFORM ARCHITECTURE                              │
│                                                                                        │
│   [ Cloudflare Pages: platform/frontend ]         [ Cloudflare Worker: platform/worker ]│
│   • Full-Screen MapLibre GL (100% Viewport)       • Edge Routing & Range-Request Slicing│
│   • Dual Basemap (Tactical Dark + High-Res Sat)  • Deterministic Spectroscopy Engine   │
│   • Floating Glassmorphism Tool Docks            • Native Workers AI (Llama 3.1 8B SSE)│
│   • 425-Band Interactive Curve + Convex Hull     • CORS & Cache-Control Headers        │
│   • On-Demand Specialist Drawer (No Chat Clutter)│                                     │
│                         │                                        │                     │
│                         └───────────────────┬────────────────────┘                     │
│                                             │ HTTP Range / Fetch                       │
│                                             ▼                                          │
│                                 [ Cloudflare R2 Storage ]                              │
│                                 • Bucket: bharatspectral-cubes                         │
│                                 • Curated 4-Zone Seed Flightline Cubes                 │
│                                 • Indian Reference Endmember Spectral Library          │
│                                 • Flightlines Vector GeoJSON Manifest                  │
│                                 • Zero Egress Bandwidth Fees                           │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Cloudflare Storage & Compute Architecture

### 1.1 Decoupled Monorepo Structure
The platform is organized with clean boundaries between serverless edge compute and client delivery:

```text
platform/
├── worker/                                # Standalone Cloudflare Worker
│   ├── wrangler.jsonc                     # Worker config (R2, Workers AI bindings)
│   ├── package.json
│   ├── tsconfig.json
│   └── src/
│       ├── index.ts                       # Edge API router & CORS handler
│       ├── spectroscopy/                  # In-isolate deterministic spectroscopy math
│       │   ├── indices.ts                 # NDRE, PRI, WBI, NDTI, MTCI
│       │   ├── continuum.ts               # Convex hull absorption depth calculator
│       │   └── unmixing.ts                # Non-negative linear unmixing (FCLS)
│       ├── storage/                       # R2 byte-slicing and cube loaders
│       │   └── r2_cube_reader.ts
│       └── ai/                            # Cloudflare Workers AI streaming integration
│           └── copilot.ts                 # SSE streaming remote sensing specialist
│
├── frontend/                              # Cloudflare Pages SPA
│   ├── wrangler.jsonc                     # Pages deployment configuration
│   ├── package.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       ├── App.tsx                        # Master layout (full-screen map + floating docks)
│       ├── components/
│       │   ├── MapCanvas.tsx              # MapLibre GL JS engine (100% viewport)
│       │   ├── BasemapToggle.tsx          # 1-click Dark Matter <-> ESRI Satellite switch
│       │   ├── FlightlineDock.tsx         # Floating left panel: corridor selector & band modes
│       │   ├── SpectralCurveDock.tsx      # Floating bottom-right dock: 425-band curve & hull
│       │   ├── TelemetryHUD.tsx           # Numerical metrics display (no fluff, raw data)
│       │   └── CopilotDrawer.tsx          # On-demand slide-over diagnostic drawer
│       ├── lib/
│       │   ├── api.ts                     # Worker API client
│       │   └── chart_utils.ts             # High-performance canvas/uPlot curve renderer
│       └── types/
│           └── spectroscopy.ts
│
└── data_seed/                             # R2 Seeding & Calibrated Reference Generators
    ├── generate_seed_granules.py          # Builds calibrated 4-zone cubes & endmembers
    ├── flightlines_manifest.geojson       # Spatial footprints & sensor metadata
    └── endmembers_india.json              # Pure reference signatures (green, soil, stubble, water)
```

---

### 1.2 Cloudflare R2 Storage Configuration (`bharatspectral-cubes`)

To support instant interactivity without multi-gigabyte client downloads, R2 hosts calibrated granules and manifests:

```text
r2://bharatspectral-cubes/
├── metadata/
│   ├── flightlines_manifest.geojson       # Multi-zone footprints & metadata
│   └── endmembers_india.json              # 425-band reference endmember signatures
└── flightlines/
    ├── vidarbha_wardha_cotton.json        # 425-band calibrated grid (AVIRIS-NG, 4.8m GSD)
    ├── punjab_ludhiana_residue.json       # 285-band calibrated grid (EMIT, 60m GSD)
    ├── gujarat_anand_canopy.json          # 425-band calibrated grid (AVIRIS-NG, 5.0m GSD)
    └── godavari_delta_wetland.json        # 285-band calibrated grid (EMIT, 60m GSD)
```

#### Agro-Ecological Seed Profiles:
1. **Vidarbha, Wardha (Maharashtra):** Rainfed cotton & soybean agroecosystem. Deep black cotton soil (Regur), clay hydroxyl ($2200\,\text{nm}$) absorption, moisture variation.
2. **Ludhiana, Punjab:** Post-monsoon Kharif/Rabi transition. Post-harvest wheat/rice parcels with combustible straw residue, diagnostic cellulose/lignin ($2100\,\text{nm}$) feature, stubble burn risk.
3. **Anand, Gujarat:** Intensive mixed canopy, high chlorophyll density, deep $680\,\text{nm}$ well, sharp red-edge inflection point ($705\text{--}725\,\text{nm}$).
4. **Godavari Delta (Andhra Pradesh):** Coastal wetland paddy rice, high liquid water band absorption ($970\,\text{nm}$ and $1200\,\text{nm}$), saturated soil endmember.

---

### 1.3 Cloudflare Worker API Specification

The worker (`platform/worker`) provides low-latency serverless routes:

1. **`GET /api/flightlines`**:
   * Reads and caches `metadata/flightlines_manifest.geojson` from R2.
   * Returns available flightlines with bounding coordinates, GSD, sensor type, and band count.
2. **`GET /api/spectrum?flightline_id=...&lat=...&lon=...`**:
   * Extracts the continuous reflectance vector for the requested coordinate from R2 storage.
   * Runs the in-isolate spectroscopy engine:
     - Atmospheric water absorption masking ($1350\text{--}1450\,\text{nm}$, $1800\text{--}1950\,\text{nm}$).
     - Narrowband indices (NDRE, PRI, WBI, NDTI, MTCI).
     - Diagnostic continuum removal (absorption depths at $680\,\text{nm}$, $705\,\text{nm}$, $970\,\text{nm}$, $2100\,\text{nm}$, $2200\,\text{nm}$, red-edge inflection $\lambda_{re}$, and convex hull baseline).
     - Fully Constrained Linear Spectral Unmixing (fractional abundances summing to $1.0$).
     - Spectral Angle Mapper (SAM) match against reference endmembers.
   * Returns a complete typed JSON payload in $<15\,\text{ms}$.
3. **`POST /api/copilot/chat`**:
   * Streams authoritative remote sensing diagnostics via Server-Sent Events (SSE) using Cloudflare Workers AI (`@cf/meta/llama-3.1-8b-instruct`).
   * Takes the exact numerical telemetry output from `/api/spectrum`.
   * Enforces zero hallucination: responses must strictly cite the computed numerical values.

---

## 2. Frontend Workstation Specification (UI/UX)

### 2.1 Aesthetic Directive: Zero AI Marketing Fluff
* **No promotional copy:** No "Welcome to our AI platform" headers, marketing bullet lists, or generic cards explaining what hyperspectral imaging is.
* **Platform-grade density:** High information density inspired by scientific workstations (USGS EarthExplorer, Sentinel Hub EO Browser, QGIS).
* **High-contrast dark theme:** Neutral dark gray/black backgrounds (`#0d1117`, `#161b22`) allowing vibrant false-color maps and spectral curves to take center stage.

### 2.2 Viewport & Dock Panel Layout

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 🛰 BHARATSPECTRAL [AVIRIS-NG / EMIT]        [Lat: 21.1458, Lon: 79.0882]  [ESRI Sat 🔘]│
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [FLOATING DOCK: LEFT]                                                                  │
│ ┌──────────────────────────┐                                                           │
│ │ Flightline Corridor:     │                                                           │
│ │ [Vidarbha Cotton ▼]      │                                                           │
│ │                          │                                                           │
│ │ Band Rendering Mode:     │                      FULL-SCREEN MAP CANVAS               │
│ │ (•) True Color (RGB)     │                       (MapLibre GL 100%)                  │
│ │ ( ) False Color (NIR)    │                                                           │
│ │ ( ) NDRE Canopy Nitrogen │                  • National & State vector boundaries     │
│ │ ( ) Residue / NDTI       │                  • Curated flightline polygon corridor    │
│ │                          │                  • Selected pixel reticle pin             │
│ │ Opacity: [====|===] 80%  │                                                           │
│ └──────────────────────────┘                                                           │
│                                                                                        │
│                                                                                        │
│                                             [FLOATING DOCK: BOTTOM-RIGHT]              │
│                                             ┌────────────────────────────────────────┐ │
│                                             │ 425-BAND SPECTRAL CURVE (380-2510 nm)  │ │
│                                             │ 1.0┌──────────────/\─────────────┐     │ │
│                                             │    │             /  \   /\       │     │ │
│                                             │ 0.5│   /\       /    \_/  \__    │     │ │
│                                             │ 0.0└──┴──────┴──────┴──────┴─────┘     │ │
│                                             │      680    705   970   2100 nm        │ │
│                                             │ [x] Show Convex Hull Baseline          │ │
│                                             │ [x] Pin Reference Curve (Healthy Crop) │ │
│                                             │ ────────────────────────────────────── │ │
│                                             │ TELEMETRY HUD                          │ │
│                                             │ • NDRE: 0.284    • Chl Depth: 0.362    │ │
│                                             │ • PRI:  -0.042   • WBI: 0.885          │ │
│                                             │ • FCLS: 52% Green | 34% Soil | 14% Dry │ │
│                                             │ • SAM Match: Gossypium hirsutum (94%)  │ │
│                                             │ [ ⚡ Run Specialist Diagnostic ]       │ │
│                                             └────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Interactive 425-Band Spectral Curve Visualizer
* **Continuous curve rendering:** Renders up to 425 discrete points smoothly with zero lag using fast HTML5 canvas / SVG interpolation.
* **Convex Hull Baseline Toggle:** Renders the upper convex hull dashed line above the absorption wells to visually demonstrate how depth $D(\lambda) = 1 - \frac{R(\lambda)}{R_c(\lambda)}$ is derived.
* **Diagnostic Feature Pins:** Interactive markers for key absorption bands:
  * `680 nm`: Chlorophyll-$a$ absorption well.
  * `705 nm`: Red-Edge inflection point.
  * `970 nm`: Plant tissue liquid water absorption.
  * `2100 nm`: Lignin & cellulose dry residue absorption.
  * `2200 nm`: Clay hydroxyl ($\text{Al-OH}$) mineral absorption.
* **Reference Curve Overlay:** 1-click toggle to overlay pure endmembers (Healthy Crop vs. Stressed Crop vs. Soil) over the clicked pixel's spectrum.

### 2.4 On-Demand Specialist Copilot Drawer
* Hidden by default to keep the interface uncluttered.
* Triggered explicitly by clicking **"Run Specialist Diagnostic"** in the Telemetry HUD.
* Opens as a sleek right-side slide-over drawer:
  * Select role: *Farmer Advisory*, *Agronomist / Soil Scientist*, or *District Administration*.
  * Shows exact telemetry numbers supplied to the model.
  * Streams crisp, structured bullet points strictly grounded in the physical measurements.

---

## 3. Implementation Milestones

### Phase 1: Storage & Seed Ingestion (`platform/data_seed/`)
* [ ] Build `generate_seed_granules.py` to create calibrated 4-zone datasets and reference endmember libraries.
* [ ] Generate `flightlines_manifest.geojson` with accurate bounding boxes for Vidarbha, Ludhiana, Anand, and Godavari.
* [ ] Verify local JSON structures match the engine's typed contract.

### Phase 2: Serverless Cloudflare Worker API (`platform/worker/`)
* [ ] Initialize Cloudflare Worker project using `wrangler.jsonc` with R2 and Workers AI bindings.
* [ ] Implement in-isolate spectroscopy math (`indices.ts`, `continuum.ts`, `unmixing.ts`).
* [ ] Implement `GET /api/flightlines` with in-memory caching.
* [ ] Implement `GET /api/spectrum` with atmospheric masking and physical diagnostic evaluation.
* [ ] Implement `POST /api/copilot/chat` with Workers AI native streaming SSE (`@cf/meta/llama-3.1-8b-instruct`).
* [ ] Add automated test suite for the Worker routes.

### Phase 3: Cloudflare Pages Frontend Application (`platform/frontend/`)
* [ ] Initialize Vite + React + TypeScript + Tailwind CSS project with `wrangler.jsonc` for Pages.
* [ ] Implement MapLibre GL full-screen map with dual basemaps (Dark Matter + ESRI Satellite).
* [ ] Render national boundary vector layers (`india.geojson`, `states.geojson`) and flightline polygon corridors.
* [ ] Build floating Flightline & Band Mode dock (RGB, False Color, NDRE).
* [ ] Build 425-band interactive spectral curve canvas with draggable scrubber, convex hull toggle, and diagnostic pins.
* [ ] Build Telemetry HUD displaying instant physical spectroscopy results.
* [ ] Build on-demand slide-over Copilot diagnostic drawer with SSE streaming.

### Phase 4: Integration, Build Verification & Cloudflare Deployment Prep
* [ ] Verify end-to-end flow: parcel click $\to$ Worker API $\to$ spectrum plot $\to$ telemetry HUD $\to$ on-demand copilot.
* [ ] Verify local worker execution via `wrangler dev` and production build via `npm run build`.
* [ ] Document deployment commands for Cloudflare Workers (`wrangler deploy`) and Cloudflare Pages.

---

## 4. Acceptance Criteria
1. **Zero Fluff:** No promotional AI text or filler marketing components anywhere in the application.
2. **Deterministic Precision:** All numerical telemetry indices and absorption depths are mathematically calculated from the reflectance vectors and strictly reproducible.
3. **Responsive WebGIS Experience:** Single-pixel inspection responds in $< 50\,\text{ms}$; spectral curve visualizer renders 425 bands at 60 FPS.
4. **Cloudflare Native:** Worker executes within Cloudflare's resource limits (< 15 MB memory footprint, < 5 ms isolate CPU time).
5. **On-Demand Intelligence:** Copilot drawer only opens when requested and streams responses strictly referencing the active pixel's telemetry data.
