# BharatSpectral — Cloudflare WebGIS Platform & Edge Spectroscopy Engine

This directory contains the production-grade, serverless **BharatSpectral WebGIS Platform**, engineered as a zero-barrier Digital Public Infrastructure (DPI) on the Cloudflare Ecosystem (Cloudflare Pages, Cloudflare Workers, R2 Storage, and Workers AI).

---

## Architecture Overview

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

## Directory Layout

```text
platform/
├── worker/                                # Standalone Cloudflare Worker API
│   ├── wrangler.jsonc                     # Worker config (R2, Workers AI bindings)
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── index.ts                       # Edge API router & CORS handler
│   │   ├── types.ts                       # TypeScript engine contracts
│   │   ├── spectroscopy/                  # In-isolate deterministic spectroscopy math
│   │   │   ├── indices.ts                 # NDRE, PRI, WBI, NDTI, MTCI
│   │   │   ├── continuum.ts               # Convex hull & absorption depth calculator
│   │   │   ├── unmixing.ts                # Simplex projected gradient descent (FCLS)
│   │   │   ├── sam.ts                     # Spectral Angle Mapper similarity classifier
│   │   │   └── masking.ts                 # Atmospheric water vapor absorption masking
│   │   ├── storage/                       # R2 byte-slicing and cube loaders
│   │   │   └── r2_cube_reader.ts
│   │   └── ai/                            # Cloudflare Workers AI streaming integration
│   │       └── copilot.ts                 # SSE streaming remote sensing specialist
│   └── test/
│       └── spectroscopy.test.ts           # Vitest unit and integration suite (14 tests)
│
├── frontend/                              # Cloudflare Pages SPA
│   ├── wrangler.jsonc                     # Pages deployment configuration
│   ├── package.json
│   ├── vite.config.ts                     # Vite + React config with Worker proxy
│   ├── index.html                         # Full-screen viewport container
│   ├── src/
│   │   ├── main.tsx                       # React DOM root mount
│   │   ├── App.tsx                        # Master layout (full-screen map + docks)
│   │   ├── index.css                      # Tailwind & glassmorphism theme
│   │   ├── components/
│   │   │   ├── MapCanvas.tsx              # MapLibre GL JS engine (100% viewport)
│   │   │   ├── BasemapToggle.tsx          # 1-click Dark Matter <-> ESRI Satellite switch
│   │   │   ├── FlightlineDock.tsx         # Floating left panel: corridor selector & band modes
│   │   │   ├── SpectralCurveDock.tsx      # Floating bottom-right dock: 425-band curve & hull
│   │   │   ├── TelemetryHUD.tsx           # Numerical metrics display (no fluff, raw data)
│   │   │   └── CopilotDrawer.tsx          # On-demand slide-over diagnostic drawer
│   │   ├── lib/
│   │   │   ├── api.ts                     # Worker API client & SSE streaming reader
│   │   │   └── chart_utils.ts             # Ultra-smooth canvas 425-band curve renderer
│   │   └── types/
│   │       └── spectroscopy.ts
│   └── dist/                              # Production build output
│
└── data_seed/                             # R2 Seeding & Calibrated Reference Datasets
    ├── generate_seed_granules.py          # Python granule & endmember generator
    ├── flightlines_manifest.geojson       # Multi-corridor GeoJSON polygons
    ├── endmembers_india.json              # 425-band Indian reference endmembers
    └── flightlines/                       # 4 calibrated agro-ecological cubes
        ├── vidarbha_wardha_cotton.json    # AVIRIS-NG 425 bands, 4.8m GSD
        ├── punjab_ludhiana_residue.json   # NASA EMIT 285 bands, 60m GSD
        ├── gujarat_anand_canopy.json      # AVIRIS-NG 425 bands, 5.0m GSD
        └── godavari_delta_wetland.json    # NASA EMIT 285 bands, 60m GSD
```

---

## Local Development Quickstart

### 1. Test the Spectroscopy Math & Worker API
```bash
cd platform/worker
npm install
npm test
```

### 2. Run the Worker Locally
```bash
cd platform/worker
npm run dev
# Starts worker at http://localhost:8787
```

### 3. Run the Frontend Workstation Locally
```bash
cd platform/frontend
npm install
npm run dev
# Starts Vite at http://localhost:3000 with automatic /api proxy to localhost:8787
```

---

## Cloudflare Deployment

### 1. Deploy Cloudflare Worker (`platform/worker`)
```bash
cd platform/worker
npx wrangler deploy
```

### 2. Deploy Cloudflare Pages Frontend (`platform/frontend`)
```bash
cd platform/frontend
npm run build
npx wrangler pages deploy dist --project-name bharatspectral
```

### 3. Upload Granules to Cloudflare R2
```bash
npx wrangler r2 object put bharatspectral-cubes/metadata/flightlines_manifest.geojson --file platform/data_seed/flightlines_manifest.geojson
npx wrangler r2 object put bharatspectral-cubes/metadata/endmembers_india.json --file platform/data_seed/endmembers_india.json
npx wrangler r2 object put bharatspectral-cubes/flightlines/vidarbha_wardha_cotton.json --file platform/data_seed/flightlines/vidarbha_wardha_cotton.json
npx wrangler r2 object put bharatspectral-cubes/flightlines/punjab_ludhiana_residue.json --file platform/data_seed/flightlines/punjab_ludhiana_residue.json
npx wrangler r2 object put bharatspectral-cubes/flightlines/gujarat_anand_canopy.json --file platform/data_seed/flightlines/gujarat_anand_canopy.json
npx wrangler r2 object put bharatspectral-cubes/flightlines/godavari_delta_wetland.json --file platform/data_seed/flightlines/godavari_delta_wetland.json
```
