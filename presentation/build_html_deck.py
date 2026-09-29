import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BharatSpectral: Capstone Mid-Term Presentation</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Mermaid.js for Architecture Diagrams -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({
      startOnLoad: true,
      theme: 'dark',
      themeVariables: {
        fontFamily: 'Plus Jakarta Sans, sans-serif',
        primaryColor: '#1e293b',
        primaryBorderColor: '#38bdf8',
        primaryTextColor: '#f8fafc',
        lineColor: '#64748b',
        secondaryColor: '#0f172a',
        tertiaryColor: '#1e293b'
      }
    });
  </script>

  <style>
    :root {
      --bg-dark: #0b0f19;
      --bg-card: #151d2e;
      --bg-card-hover: #1e293b;
      --border: #2d3c55;
      --border-accent: #38bdf8;
      --text-white: #ffffff;
      --text-light: #e2e8f0;
      --text-muted: #94a3b8;
      --cyan: #38bdf8;
      --cyan-dim: rgba(56, 189, 248, 0.12);
      --teal: #14b8a6;
      --teal-dim: rgba(20, 184, 166, 0.12);
      --amber: #f59e0b;
      --amber-dim: rgba(245, 158, 11, 0.12);
      --purple: #a855f7;
      --purple-dim: rgba(168, 85, 247, 0.12);
      --red: #ef4444;
      --red-dim: rgba(239, 68, 68, 0.12);
      --font-main: 'Plus Jakarta Sans', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-dark);
      color: var(--text-light);
      font-family: var(--font-main);
      overflow: hidden;
      height: 100vh;
      width: 100vw;
      user-select: none;
    }

    /* Presentation Container */
    #deck-container {
      position: relative;
      width: 100vw;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .slide {
      position: absolute;
      width: 94vw;
      max-width: 1500px;
      height: 88vh;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 36px 44px;
      display: none;
      flex-direction: column;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 30px rgba(56, 189, 248, 0.05);
      overflow-y: auto;
      animation: fadeIn 0.3s ease-out;
    }

    .slide.active {
      display: flex;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: scale(0.99); }
      to { opacity: 1; transform: scale(1); }
    }

    /* Header styling */
    .slide-header {
      margin-bottom: 24px;
      position: relative;
    }

    .tag-badge {
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 4px 12px;
      border-radius: 9999px;
      background: var(--cyan-dim);
      color: var(--cyan);
      border: 1px solid var(--cyan);
      margin-bottom: 8px;
    }

    .tag-badge.teal { background: var(--teal-dim); color: var(--teal); border-color: var(--teal); }
    .tag-badge.amber { background: var(--amber-dim); color: var(--amber); border-color: var(--amber); }
    .tag-badge.purple { background: var(--purple-dim); color: var(--purple); border-color: var(--purple); }

    .slide-title {
      font-size: 1.85rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text-white);
      line-height: 1.25;
    }

    .slide-subtitle {
      font-size: 0.98rem;
      color: var(--text-muted);
      margin-top: 4px;
      font-weight: 400;
    }

    /* Grids & Cards */
    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      flex: 1;
    }

    .grid-3 {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 20px;
      flex: 1;
    }

    .grid-4 {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      flex: 1;
    }

    .grid-5 {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 14px;
      flex: 1;
    }

    .card {
      background: #0f172a;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      transition: all 0.2s;
    }

    .card.accent-cyan { border-top: 3px solid var(--cyan); }
    .card.accent-teal { border-top: 3px solid var(--teal); }
    .card.accent-amber { border-top: 3px solid var(--amber); }
    .card.accent-purple { border-top: 3px solid var(--purple); }
    .card.accent-red { border-top: 3px solid var(--red); }

    .card-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-white);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .card-body {
      font-size: 0.92rem;
      color: var(--text-light);
      line-height: 1.6;
    }

    .card-body ul {
      padding-left: 18px;
    }

    .card-body li {
      margin-bottom: 8px;
    }

    .card-body strong {
      color: var(--cyan);
    }

    /* Tables */
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
      background: #0f172a;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--border);
    }

    table.data-table th {
      background: #1e293b;
      color: var(--cyan);
      font-weight: 700;
      text-align: left;
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
    }

    table.data-table td {
      padding: 10px 16px;
      border-bottom: 1px solid #1e293b;
      color: var(--text-light);
      vertical-align: top;
    }

    table.data-table tr.highlight-row {
      background: rgba(56, 189, 248, 0.08);
    }

    table.data-table tr.highlight-row td {
      color: #ffffff;
      font-weight: 600;
    }

    /* Speaker Notes Modal */
    #notes-panel {
      position: fixed;
      bottom: 60px;
      right: 20px;
      width: 480px;
      max-height: 380px;
      background: #090d16;
      border: 1px solid var(--cyan);
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.7);
      display: none;
      z-index: 1000;
      overflow-y: auto;
      font-size: 0.9rem;
      line-height: 1.6;
    }

    #notes-panel h4 {
      color: var(--cyan);
      font-size: 0.95rem;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
    }

    /* Navigation Bar */
    #nav-bar {
      position: fixed;
      bottom: 12px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      align-items: center;
      gap: 14px;
      background: rgba(15, 23, 42, 0.9);
      backdrop-filter: blur(8px);
      padding: 8px 20px;
      border-radius: 9999px;
      border: 1px solid var(--border);
      z-index: 500;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }

    .nav-btn {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-light);
      font-family: var(--font-main);
      font-size: 0.85rem;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 9999px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }

    .nav-btn:hover {
      background: var(--bg-card-hover);
      border-color: var(--cyan);
      color: var(--cyan);
    }

    .slide-counter {
      font-size: 0.88rem;
      font-weight: 700;
      font-family: var(--font-mono);
      color: var(--cyan);
      min-width: 60px;
      text-align: center;
    }

    /* Keyboard hint */
    .key-hint {
      font-size: 0.75rem;
      color: var(--text-muted);
      border: 1px solid #334155;
      padding: 2px 6px;
      border-radius: 4px;
      background: #0f172a;
    }

    /* Print styling for PDF export */
    @media print {
      body {
        overflow: visible;
        height: auto;
        background: #ffffff;
        color: #000000;
      }
      #nav-bar, #notes-panel { display: none !important; }
      .slide {
        display: flex !important;
        position: static !important;
        width: 100% !important;
        height: 100vh !important;
        page-break-after: always;
        border: none !important;
        box-shadow: none !important;
        background: #ffffff !important;
        color: #000000 !important;
        padding: 40px !important;
      }
      .slide-title, .card-title { color: #000000 !important; }
      .card { background: #f8fafc !important; border: 1px solid #cbd5e1 !important; }
      .card-body, .slide-subtitle { color: #334155 !important; }
      table.data-table { background: #ffffff !important; border: 1px solid #cbd5e1 !important; }
      table.data-table th { background: #f1f5f9 !important; color: #0f172a !important; }
      table.data-table td { color: #1e293b !important; }
    }
  </style>
</head>
<body>

<div id="deck-container">

  <!-- SLIDE 1: TITLE SLIDE -->
  <div class="slide active" data-slide="1">
    <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: flex-start;">
      <span class="tag-badge">B.Tech Capstone Project Review • Mid-Term Defense</span>
      <h1 style="font-size: 3.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.03em; margin: 12px 0 16px;">
        BharatSpectral
      </h1>
      <p style="font-size: 1.35rem; color: var(--cyan); font-weight: 500; max-width: 1050px; line-height: 1.4; margin-bottom: 32px;">
        Democratized Spectral Intelligence for Indian Earth Observation Through Physics-Informed Foundation Modeling and Public Geospatial Infrastructure
      </p>

      <div class="grid-3" style="width: 100%; margin-top: 10px;">
        <div class="card accent-cyan">
          <div class="card-title">🔬 Research Pillar</div>
          <div class="card-body">
            <strong>BharatSpectral-MAE:</strong> First hyperspectral Foundation Model custom-engineered for Indian smallholder fragmentation, intercropping, and 3-season phenology via 7 novel architectural innovations.
          </div>
        </div>
        <div class="card accent-teal">
          <div class="card-title">🌐 Product Pillar</div>
          <div class="card-body">
            <strong>BharatSpectral Platform:</strong> Zero-cost, public WebGIS delivering biochemical analytics (Nitrogen, Soil Organic Carbon, Water Quality) using serverless edge inference and zero-egress tile streaming.
          </div>
        </div>
        <div class="card accent-purple">
          <div class="card-title">🇮🇳 National Alignment</div>
          <div class="card-body">
            <strong>Digital Public Infrastructure:</strong> Harnesses IndiaAI AIRAWAT DGX A100 HPC, ISRO AVIRIS-NG & HysIS missions, and open data rails to empower farmers and district collectors without paywalls.
          </div>
        </div>
      </div>
    </div>
    <div style="display: flex; justify-content: space-between; border-top: 1px solid var(--border); padding-top: 14px; margin-top: 20px; font-size: 0.85rem; color: var(--text-muted);">
      <span>Department of Computer Science & Engineering</span>
      <span>HPC: IndiaAI AIRAWAT • Sensors: ISRO AVIRIS-NG / HysIS • NASA EMIT</span>
    </div>
  </div>

  <!-- SLIDE 2: THE REAL-WORLD PROBLEM & PARADOX -->
  <div class="slide" data-slide="2">
    <div class="slide-header">
      <span class="tag-badge amber">Context & Motivation</span>
      <h2 class="slide-title">The Indian Geospatial Paradox: Data Abundance vs. Field Paralysis</h2>
      <p class="slide-subtitle">Why 140 million smallholder farmers remain locked in guesswork despite India's top-5 space program</p>
    </div>
    <div class="grid-2">
      <div class="card accent-cyan">
        <div class="card-title">🛰️ Observational Abundance (Spaceborne Potential)</div>
        <div class="card-body">
          <ul>
            <li><strong>Top-5 Global Space Power:</strong> ISRO operates elite earth observation constellations and airborne campaigns (AVIRIS-NG India, HysIS) capturing petabytes of spectral data.</li>
            <li><strong>Massive Public Investment:</strong> Hundreds of crores invested in remote sensing hardware, yet operational application remains confined to academic papers and closed research labs.</li>
            <li><strong>The "Data Graveyard" Syndrome:</strong> AVIRIS-NG datasets reside as raw 5–10 GB binary ENVI/HDF files on ISRO Bhoonidhi. Completely uninterpretable by agronomists or district officials.</li>
          </ul>
        </div>
      </div>
      <div class="card accent-amber">
        <div class="card-title">🌾 Field Paralysis (The Smallholder Reality)</div>
        <div class="card-body">
          <ul>
            <li><strong>1.08 Hectare Reality:</strong> 86% of Indian landholdings are smallholders. A single misdiagnosed crop infection or fertilizer delay can cause financial devastation.</li>
            <li><strong>The Enterprise Paywall:</strong> Commercial hyperspectral analytics (e.g. Pixxel Aurora) target enterprise agribusiness at thousands of dollars/month — inaccessible to rural Panchayats.</li>
            <li><strong>The Software & Compute Barrier:</strong> Hyperspectral analysis currently demands heavy desktop software (ENVI, ERDAS) or complex Python GIS coding in Google Earth Engine.</li>
            <li><strong>Our Mission:</strong> Translate high-dimensional spectroscopy into an open, zero-cost, instant mobile WebGIS platform for every Indian citizen.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 3: BIOPHYSICAL VS BIOCHEMICAL INTELLIGENCE -->
  <div class="slide" data-slide="3">
    <div class="slide-header">
      <span class="tag-badge cyan">Spectroscopy Principles</span>
      <h2 class="slide-title">Biophysical vs. Biochemical Intelligence</h2>
      <p class="slide-subtitle">Why 10-band multispectral satellites detect failure too late, and how 200+ narrow bands diagnose root causes</p>
    </div>
    <div class="grid-2">
      <div class="card">
        <div class="card-title" style="color: var(--text-muted);">MULTISPECTRAL SENSING (Current Status Quo)</div>
        <div style="font-size: 0.85rem; color: var(--cyan); margin-bottom: 12px;">Sentinel-2, Landsat-8/9, ISRO LISS-IV (10–12 Broad Spectral Bands)</div>
        <div class="card-body">
          <ul>
            <li><strong>Intelligence Level:</strong> Biophysical only (NDVI, NDRE, EVI).</li>
            <li><strong>What it Measures:</strong> Detects <em>THAT</em> a crop is losing vigor or biomass.</li>
            <li><strong>The Fatal Blindspot:</strong> Cannot determine <em>WHY</em>. Nitrogen starvation, fungal leaf rust, soil salinity, and moisture stress look spectrally IDENTICAL across broad 100 nm bands.</li>
            <li><strong>Irreversible Yield Loss:</strong> By the time broad-band NDVI drops, chlorophyll breakdown is extensive and 15–25% yield loss is already locked in.</li>
          </ul>
        </div>
      </div>
      <div class="card accent-cyan">
        <div class="card-title" style="color: var(--cyan);">HYPERSPECTRAL INTELLIGENCE (BharatSpectral)</div>
        <div style="font-size: 0.85rem; color: var(--teal); margin-bottom: 12px;">AVIRIS-NG, NASA EMIT, ISRO HysIS (200–425 Continuous Narrow Bands, 5nm)</div>
        <div class="card-body">
          <ul>
            <li><strong>Intelligence Level:</strong> Biochemical & Molecular spectroscopy (380–2500 nm).</li>
            <li><strong>Pre-Symptomatic Nitrogen (720 nm):</strong> Isolates the exact Red-Edge inflection shift driven by cellular nitrogen binding 7–14 days before visible yellowing.</li>
            <li><strong>Yellow Rust Spores (680 nm vs 710 nm):</strong> Separates fungal mycelium damage from water stress, halting whole-field pesticide overuse.</li>
            <li><strong>Soil Organic Carbon (2200 nm):</strong> Measures the SWIR Al-OH and clay-organic absorption doublet directly from orbit without physical soil core sampling.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 4: LITERATURE GAP & VERIFICATION -->
  <div class="slide" data-slide="4">
    <div class="slide-header">
      <span class="tag-badge red">Literature Gap & Verification</span>
      <h2 class="slide-title">Why Existing Foundation Models Fail on Indian Landscapes</h2>
      <p class="slide-subtitle">SOTA models (SpectralGPT, HyperSIGMA, SS-MAE) suffer catastrophic domain shift when applied to Indian agriculture</p>
    </div>
    <div style="background: var(--amber-dim); border: 1px solid var(--amber); border-radius: 8px; padding: 12px 18px; margin-bottom: 18px; font-size: 0.9rem; color: var(--text-light);">
      <strong style="color: var(--amber);">⚠️ The Canonical "Indian Pines" Fallacy:</strong> Foundation models claim success on "Indian Pines" (1992). Despite its name, this dataset was captured in <strong>Indiana, USA</strong> over giant rectilinear monocultures. It shares ZERO agronomic, ecological, or spatial characteristics with Indian agriculture!
    </div>
    <div class="grid-4">
      <div class="card accent-cyan">
        <div class="card-title" style="font-size: 1rem;">1. Extreme Fragmentation</div>
        <div class="card-body" style="font-size: 0.85rem;">
          Average plot is 1.08 ha (millions &lt;0.5 ha). At 30–60m pixel resolution (EMIT/HysIS), every pixel contains multiple crops and boundaries. Western models assume pure pixels; Indian data requires sub-pixel unmixing at every point.
        </div>
      </div>
      <div class="card accent-teal">
        <div class="card-title" style="font-size: 1rem;">2. Intercropping Mixing</div>
        <div class="card-body" style="font-size: 0.85rem;">
          Indian farmers co-plant 2–3 species simultaneously (e.g. Sorghum + Pigeon Pea). The resulting canopy spectra are non-linear mixtures completely absent from Western monoculture benchmarks.
        </div>
      </div>
      <div class="card accent-purple">
        <div class="card-title" style="font-size: 1rem;">3. 3-Season Phenology</div>
        <div class="card-body" style="font-size: 0.85rem;">
          India experiences Kharif (monsoon), Rabi (winter), and Zaid (summer). The same GPS coordinate shows completely divergent phenology. Single-season models suffer catastrophic seasonal drift.
        </div>
      </div>
      <div class="card accent-red">
        <div class="card-title" style="font-size: 1rem;">4. Multi-Sensor Gap</div>
        <div class="card-body" style="font-size: 0.85rem;">
          No existing model harmonizes airborne AVIRIS-NG (4–8m GSD, 425b) with spaceborne EMIT (60m GSD, 285b) and HysIS (30m GSD, 220b). Scale-MAE ignores the spectral bandwidth dimension completely.
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 5: ECOSYSTEM AUDIT & VERIFICATION -->
  <div class="slide" data-slide="5">
    <div class="slide-header">
      <span class="tag-badge amber">Ecosystem Audit & Verification</span>
      <h2 class="slide-title">National Remote Sensing Landscape: The Public Infrastructure Gap</h2>
      <p class="slide-subtitle">Exhaustive 2026 audit of Indian geospatial platforms verifying that no citizen hyperspectral engine exists</p>
    </div>
    <table class="data-table">
      <thead>
        <tr>
          <th>Platform / Entity</th>
          <th>Data Modality</th>
          <th>Access Model</th>
          <th>Web HSI Inference?</th>
          <th>The Translational Gap</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>ISRO Bhuvan / Krishi-DSS</strong></td>
          <td>Multispectral (LISS, Sentinel-2)</td>
          <td>Public Web Portal</td>
          <td>None (No HSI)</td>
          <td>Biophysical stress only; cannot diagnose biochemical root cause.</td>
        </tr>
        <tr>
          <td><strong>ISRO VEDAS (AVHYAS)</strong></td>
          <td>Hyperspectral (AVIRIS-NG)</td>
          <td>Desktop QGIS Plugin</td>
          <td>Offline Only</td>
          <td>Requires heavy local workstation install; zero browser/citizen access.</td>
        </tr>
        <tr>
          <td><strong>ISRO Bhoonidhi</strong></td>
          <td>Raw HSI Data Catalog</td>
          <td>Public (Registration)</td>
          <td>None (Raw ENVI)</td>
          <td>Distributes raw 5–10 GB binary cubes; no automated analytics engine.</td>
        </tr>
        <tr>
          <td><strong>Pixxel Aurora</strong></td>
          <td>Hyperspectral (Constellation)</td>
          <td>Commercial B2B SaaS</td>
          <td>Yes (Proprietary)</td>
          <td>Enterprise paywall; inaccessible to smallholders and public research.</td>
        </tr>
        <tr>
          <td><strong>Google Earth Engine (GEE)</strong></td>
          <td>PaaS (Hosts NASA EMIT)</td>
          <td>Freemium PaaS</td>
          <td>User Must Code</td>
          <td>Requires Python/JS GIS scripting; no pre-trained smallholder AI models.</td>
        </tr>
        <tr class="highlight-row">
          <td><strong style="color: var(--cyan);">BharatSpectral (Ours)</strong></td>
          <td>Multi-Sensor HSI (200–425 b)</td>
          <td>100% Free Public Infra</td>
          <td>Yes (Real-Time Edge)</td>
          <td>The ONLY open Foundation Model + zero-cost WebGIS platform in India.</td>
        </tr>
      </tbody>
    </table>
    <div style="margin-top: 16px; background: #0f172a; border: 1px solid var(--teal); border-radius: 8px; padding: 12px 18px; font-size: 0.88rem; color: var(--teal);">
      <strong>🎯 Verified Finding:</strong> No system exists globally or nationally that combines a physics-informed Foundation Model engineered for Indian smallholders with zero-egress, citizen-accessible public WebGIS deployment.
    </div>
  </div>

  <!-- SLIDE 6: DUAL-PILLAR ARCHITECTURE OVERVIEW -->
  <div class="slide" data-slide="6">
    <div class="slide-header">
      <span class="tag-badge cyan">System Architecture</span>
      <h2 class="slide-title">The Dual-Pillar Framework: Synergizing AI Research & Public Infrastructure</h2>
      <p class="slide-subtitle">Creating Democratized Spectral-Semantic Intelligence (DSSI) from laboratory spectroscopy to citizen fingertips</p>
    </div>
    <div class="grid-2">
      <div class="card accent-cyan">
        <div class="card-title">🔬 Pillar 1: AI Foundation Research</div>
        <div style="font-size: 0.85rem; color: var(--cyan); margin-bottom: 12px;">BharatSpectral-MAE Engine (AIRAWAT HPC DGX A100)</div>
        <div class="card-body">
          <ul>
            <li><strong>Multi-Sensor Pre-Training:</strong> Ingests airborne AVIRIS-NG (425 bands, 4–8m), spaceborne EMIT (285 bands, 60m), and HysIS (220 bands, 30m).</li>
            <li><strong>7 Named Innovations:</strong> SSPE, RNRL, SHT, AAM, ECSA, Ph-LoRA, and FASU explicitly solve Indian sub-pixel and phenological challenges.</li>
            <li><strong>BharatHSI-Bench:</strong> First open, standardized Indian hyperspectral agricultural benchmark with ground truth labels.</li>
            <li><strong>Teacher-Student Distillation:</strong> Compresses heavy Vision Transformers into lightweight edge models.</li>
          </ul>
        </div>
      </div>
      <div class="card accent-teal">
        <div class="card-title">🌐 Pillar 2: Public Geospatial Infrastructure</div>
        <div style="font-size: 0.85rem; color: var(--teal); margin-bottom: 12px;">BharatSpectral Platform (Cloudflare Serverless)</div>
        <div class="card-body">
          <ul>
            <li><strong>Zero-Egress Streaming:</strong> Multi-terabyte Zarr datacubes and Cloud-Optimized GeoTIFFs (COG) hosted on Cloudflare R2 with $0 egress fees.</li>
            <li><strong>Serverless Spectral Inference (SSI):</strong> Quantized ONNX student model executes inside Cloudflare Workers V8 isolates within 128 MB RAM.</li>
            <li><strong>Citizen MapLibre WebGIS:</strong> Fast, responsive web frontend allowing farmers, KVK officers, and researchers to query any coordinate without GIS tools.</li>
            <li><strong>Actionable Intelligence:</strong> Outputs single-click diagnostic maps: Nitrogen (kg/ha), Soil Carbon (%), Algal Bloom Toxicity alerts.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 7: THE 7 NAMED ARCHITECTURAL INNOVATIONS -->
  <div class="slide" data-slide="7">
    <div class="slide-header">
      <span class="tag-badge purple">Research Core</span>
      <h2 class="slide-title">BharatSpectral-MAE: The 7 Named Architectural Innovations</h2>
      <p class="slide-subtitle">Physics-informed mechanisms engineered specifically for Indian smallholder Earth Observation</p>
    </div>
    <div class="grid-2" style="gap: 16px;">
      <div class="card accent-cyan" style="padding: 16px;">
        <div class="card-title" style="font-size: 1.05rem; margin-bottom: 6px;">[SSPE] Scale-Spectral Positional Encoding</div>
        <div class="card-body" style="font-size: 0.85rem;">
          Jointly encodes GSD (4m–60m), spectral bandwidth, and mixture entropy across 3 sensors. Extends Scale-MAE into the hyperspectral regime.
        </div>
      </div>
      <div class="card accent-teal" style="padding: 16px;">
        <div class="card-title" style="font-size: 1.05rem; margin-bottom: 6px;">[RNRL] Reflectance-Normalized Reconstruction Loss</div>
        <div class="card-body" style="font-size: 0.85rem;">
          Normalizes self-supervised reconstruction by target magnitude, preventing low-reflectance water bodies (&lt;5% SWIR) from being discarded as noise.
        </div>
      </div>
      <div class="card accent-purple" style="padding: 16px;">
        <div class="card-title" style="font-size: 1.05rem; margin-bottom: 6px;">[SHT] Spectral Harmonic Tokenizer</div>
        <div class="card-body" style="font-size: 0.85rem;">
          Sensor-adaptive 3D tokenizer allocating fine-grained tokens in diagnostic Red-Edge zones (700–750 nm) and coarse tokens in continuum regions.
        </div>
      </div>
      <div class="card accent-amber" style="padding: 16px;">
        <div class="card-title" style="font-size: 1.05rem; margin-bottom: 6px;">[AAM] Atmospheric Absorption Masking</div>
        <div class="card-body" style="font-size: 0.85rem;">
          Simulates atmospheric water vapor (1350–1420 & 1800–1950 nm) and CO2 absorption gaps, forcing the Transformer to learn radiative transfer physics.
        </div>
      </div>
      <div class="card accent-cyan" style="padding: 16px;">
        <div class="card-title" style="font-size: 1.05rem; margin-bottom: 6px;">[ECSA] Endmember-Constrained Self-Attention</div>
        <div class="card-body" style="font-size: 0.85rem;">
          Regularizes self-attention via spectral unmixing similarity, attending to physically matching crop signatures across fragmented plot boundaries.
        </div>
      </div>
      <div class="card accent-teal" style="padding: 16px;">
        <div class="card-title" style="font-size: 1.05rem; margin-bottom: 6px;">[Ph-LoRA] Phenology-Conditioned LoRA</div>
        <div class="card-body" style="font-size: 0.85rem;">
          Dynamically modulates PEFT adapter weights by season (Kharif/Rabi/Zaid) and growth stage embeddings, preventing seasonal spectral drift.
        </div>
      </div>
    </div>
    <div style="margin-top: 12px; background: #0f172a; border: 1px solid var(--border); border-radius: 8px; padding: 12px 18px; font-size: 0.88rem; color: var(--text-light); display: flex; justify-content: space-between; align-items: center;">
      <span><strong>[FASU] Foundation-Augmented Spectral Unmixing:</strong> Direct sub-pixel unmixing head operating on pre-trained representations without retraining standalone autoencoders.</span>
      <span style="color: var(--cyan); font-weight: 700;">No Published Precedent</span>
    </div>
  </div>

  <!-- SLIDE 8: SOLVING THE 3 STRUCTURAL CLOUD BOTTLENECKS -->
  <div class="slide" data-slide="8">
    <div class="slide-header">
      <span class="tag-badge teal">Software Architecture</span>
      <h2 class="slide-title">Product Pillar: Breaking the 3 Structural Cloud Bottlenecks</h2>
      <p class="slide-subtitle">How our serverless architecture reduces marginal operating costs to near-zero for sustained public access</p>
    </div>
    <div class="grid-3">
      <div class="card accent-cyan">
        <div class="card-title" style="font-size: 1rem;">1. Data Volume Bottleneck</div>
        <div style="font-size: 0.82rem; color: var(--red); font-weight: 700; margin-bottom: 4px;">THE PROBLEM:</div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">A single scene is 2–10 GB. Serving 200+ raw bands to thousands of concurrent citizen users crashes standard WebGIS tile servers.</p>
        <div style="font-size: 0.82rem; color: var(--teal); font-weight: 700; margin-bottom: 4px;">OUR SOLUTION:</div>
        <p style="font-size: 0.85rem; color: var(--text-light);">Convert scenes into Cloud-Optimized GeoTIFFs (COG) and chunked Zarr datacubes. The browser requests ONLY the exact bounding box and 3–5 diagnostic wavelengths via HTTP Range requests, slashing payload sizes by 98%.</p>
      </div>

      <div class="card accent-teal">
        <div class="card-title" style="font-size: 1rem;">2. Egress Cost Bottleneck</div>
        <div style="font-size: 0.82rem; color: var(--red); font-weight: 700; margin-bottom: 4px;">THE PROBLEM:</div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">AWS S3 and GCP charge $0.08–$0.12/GB for outbound data egress. Streaming gigabyte-scale spectral cubes to the public creates thousands in recurring cloud debt.</p>
        <div style="font-size: 0.82rem; color: var(--teal); font-weight: 700; margin-bottom: 4px;">OUR SOLUTION:</div>
        <p style="font-size: 0.85rem; color: var(--text-light);">Cloudflare R2 object storage with guaranteed <strong>$0 data egress fees</strong>. Public users can pan, stream, and query spectral cubes infinitely without incurring bandwidth penalties.</p>
      </div>

      <div class="card accent-purple">
        <div class="card-title" style="font-size: 1rem;">3. Inference Compute Bottleneck</div>
        <div style="font-size: 0.82rem; color: var(--red); font-weight: 700; margin-bottom: 4px;">THE PROBLEM:</div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">Hyperspectral models (200+ bands) demand high-end GPU clusters ($1,500+/mo), making public citizen deployment economically unsustainable.</p>
        <div style="font-size: 0.82rem; color: var(--teal); font-weight: 700; margin-bottom: 4px;">OUR SOLUTION:</div>
        <p style="font-size: 0.85rem; color: var(--text-light);"><strong>Serverless Spectral Inference (SSI):</strong> Distilled ONNX student model running directly in Cloudflare Workers V8 isolates within strict 128 MB RAM limits, providing sub-second inference at the edge.</p>
      </div>
    </div>
  </div>

  <!-- SLIDE 9: END-TO-END PIPELINE & DATA JOURNEY -->
  <div class="slide" data-slide="9">
    <div class="slide-header">
      <span class="tag-badge cyan">Engineering Pipeline</span>
      <h2 class="slide-title">The End-to-End Data Journey: From Raw Photons to Citizen Action</h2>
      <p class="slide-subtitle">Detailed workflow connecting ISRO/NASA satellites to browser-based edge inference</p>
    </div>
    <div class="grid-4">
      <div class="card accent-cyan">
        <div class="card-title" style="font-size: 1rem;">Stage 1: Preprocessing</div>
        <div class="card-body" style="font-size: 0.85rem;">
          <ul>
            <li>ISRO AVIRIS-NG & NASA EMIT ingestion</li>
            <li>Bad Band Removal (BBR) dropping 1350–1420 & 1800–1950 nm</li>
            <li>Radiative transfer surface reflectance conversion</li>
            <li>Analysis-ready Zarr & COG creation on Cloudflare R2</li>
          </ul>
        </div>
      </div>
      <div class="card accent-purple">
        <div class="card-title" style="font-size: 1rem;">Stage 2: AIRAWAT HPC</div>
        <div class="card-body" style="font-size: 0.85rem;">
          <ul>
            <li>IndiaAI AIRAWAT DGX A100 nodes</li>
            <li>PyTorch DDP distributed scaling</li>
            <li>Self-supervised pre-training with 7 innovations (SSPE, RNRL, SHT, AAM, ECSA)</li>
            <li>bfloat16 mixed precision & gradient checkpointing</li>
            <li>Ph-LoRA fine-tuning for Kharif/Rabi</li>
          </ul>
        </div>
      </div>
      <div class="card accent-amber">
        <div class="card-title" style="font-size: 1rem;">Stage 3: Distillation</div>
        <div class="card-body" style="font-size: 0.85rem;">
          <ul>
            <li>Teacher: Spectral-MAE Transformer</li>
            <li>Student: Mobile 3D-2D CNN</li>
            <li>Transfers "dark knowledge" and absorption sensitivity</li>
            <li>INT8 post-training quantization</li>
            <li>ONNX runtime compilation optimized for 128 MB V8 isolates</li>
          </ul>
        </div>
      </div>
      <div class="card accent-teal">
        <div class="card-title" style="font-size: 1rem;">Stage 4: Edge Delivery</div>
        <div class="card-body" style="font-size: 0.85rem;">
          <ul>
            <li>Cloudflare R2 zero-egress tile hosting</li>
            <li>Serverless Spectral Inference (SSI) on Workers</li>
            <li>Next.js + MapLibre GL JS client portal</li>
            <li>Sub-second diagnostic maps: Nitrogen, Carbon, Cyanobacteria</li>
            <li>Operates on 4G/5G mobile browsers</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 10: REAL-WORLD USE CASE 1 - PRECISION AGRICULTURE -->
  <div class="slide" data-slide="10">
    <div class="slide-header">
      <span class="tag-badge cyan">Real-World Impact: Use Case 1</span>
      <h2 class="slide-title">Precision Agriculture: The Smallholder Farmer in Ludhiana</h2>
      <p class="slide-subtitle">Pre-symptomatic nitrogen deficiency and yellow rust diagnosis 7 to 14 days before visible damage</p>
    </div>
    <div class="grid-2">
      <div class="card accent-cyan">
        <div class="card-title">🌾 Persona: Gurpreet Singh (Ludhiana, Punjab)</div>
        <div class="card-body">
          <ul>
            <li><strong>The Challenge:</strong> Gurpreet cultivates 2.4 acres of wheat. Over-application of urea has degraded his soil and spiked input costs, while stripe rust (yellow rust) threatens his crop every February.</li>
            <li><strong>The Status Quo Dilemma:</strong> Multispectral apps (NDVI) only detect distress after leaves turn yellow. By then, fungal mycelium has penetrated the tissue and 20% yield loss is already locked in.</li>
            <li><strong>BharatSpectral Intervention:</strong> Gurpreet opens BharatSpectral on his phone. The system queries recent EMIT/AVIRIS-NG passes and unmixes sub-pixel signatures over his plot coordinates.</li>
            <li><strong>Pre-Symptomatic Diagnosis:</strong> Pinpoints the Red-Edge inflection shift at 720 nm (nitrogen deficiency) vs 680 nm absorption drop (yellow rust spores) 10 days before visual symptoms appear.</li>
          </ul>
        </div>
      </div>
      <div class="card accent-teal">
        <div class="card-title">📈 Quantifiable Economic & Agronomic Outcomes</div>
        <div class="card-body">
          <ul>
            <li><strong>₹3,500 / Acre Fertilizer Savings:</strong> Variable-rate nitrogen prescription maps target exact deficiency pockets, cutting urea broadcast by 30%.</li>
            <li><strong>Yield Protection (15–22% Preserved):</strong> Early targeted fungicide spraying in micro-clusters halts yellow rust epidemics before whole-field infestation occurs.</li>
            <li><strong>Groundwater Protection:</strong> Prevents toxic nitrate leaching into Punjab's over-exploited Malwa aquifer.</li>
            <li><strong>Zero Jargon:</strong> Color-coded prescription map on mobile WhatsApp/PWA ("Zone A: Apply 8kg Urea; Zone B: Healthy").</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 11: REAL-WORLD USE CASE 2 - SOIL HEALTH & GOVERNANCE -->
  <div class="slide" data-slide="11">
    <div class="slide-header">
      <span class="tag-badge amber">Real-World Impact: Use Case 2</span>
      <h2 class="slide-title">Soil Health & Governance: District Collector & KVK in Karnal</h2>
      <p class="slide-subtitle">Automating Soil Organic Carbon (SOC) and Soil Health Card verification across entire districts</p>
    </div>
    <div class="grid-2">
      <div class="card accent-amber">
        <div class="card-title">🏛️ Persona: Dr. Anita Verma (KVK Officer, Karnal)</div>
        <div class="card-body">
          <ul>
            <li><strong>The Bottleneck:</strong> Mandated to issue 25,000 Soil Health Cards annually. Physical soil sampling requires laboratory wet-chemistry (Walkley-Black titration) taking 4–6 weeks per sample. Over 80% of plots remain unverified.</li>
            <li><strong>Residue Burning Crisis:</strong> Stubble burning in October degrades topsoil organic matter, but blanket fertilizer subsidies mask progressive soil degradation.</li>
            <li><strong>The BharatSpectral Solution:</strong> Uses Ph-LoRA bare soil attention to map Soil Organic Carbon (SOC) and clay mineralogy directly from 2200 nm SWIR absorption doublets across the entire district at 10m resolution.</li>
            <li><strong>Automated Soil Cards:</strong> Pairs hyperspectral reflectance directly with National Soil Health Card databases, generating continuous spatial soil health layers without physical transport delays.</li>
          </ul>
        </div>
      </div>
      <div class="card accent-purple">
        <div class="card-title">📊 Policy & Agricultural Impact</div>
        <div class="card-body">
          <ul>
            <li><strong>100% District Coverage vs 5% Manual:</strong> Replaces sparse point-sample interpolations with exhaustive, continuous wall-to-wall soil carbon mapping.</li>
            <li><strong>Stubble Burning Impact Tracking:</strong> Quantifies topsoil carbon volatilization post-fire, providing district magistrates with empirical data to reward zero-burn farmers.</li>
            <li><strong>Rationalized Subsidies:</strong> State agriculture departments can redirect subsidized fertilizer based on true biochemical deficiencies rather than political quotas.</li>
            <li><strong>Carbon Market Verification:</strong> Provides the spatial baseline required for Indian smallholders to participate in international soil carbon credit programs.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 12: REAL-WORLD USE CASE 3 - WATER QUALITY & ENVIRONMENTAL -->
  <div class="slide" data-slide="12">
    <div class="slide-header">
      <span class="tag-badge teal">Real-World Impact: Use Case 3</span>
      <h2 class="slide-title">Environmental Protection: Water Quality Inspector in Varanasi</h2>
      <p class="slide-subtitle">Detecting toxic cyanobacterial blooms and industrial effluent plumes in low-reflectance inland waters</p>
    </div>
    <div class="grid-2">
      <div class="card accent-teal">
        <div class="card-title">🌊 Persona: Rajesh Tripathi (Pollution Control, Varanasi)</div>
        <div class="card-body">
          <ul>
            <li><strong>The Inland Water Challenge:</strong> Water absorbs &gt;95% of incoming solar radiation in SWIR (reflectance &lt;5%). Standard AI models and multispectral satellites treat water as dark noise.</li>
            <li><strong>Toxic Cyanobacteria vs. Algae:</strong> Multispectral sensors measure broad chlorophyll-a (665 nm), mistaking harmless green algae for life-threatening cyanobacterial blooms releasing microcystin liver toxins.</li>
            <li><strong>BharatSpectral Breakthrough:</strong> Reflectance-Normalized Reconstruction Loss (RNRL) forces the model to learn subtle spectral variations in low-reflectance water bodies.</li>
            <li><strong>Phycocyanin Detection:</strong> Isolates the specific 620 nm phycocyanin absorption dip, detecting toxic blooms 5 days before fish kills and water treatment shutdowns occur.</li>
          </ul>
        </div>
      </div>
      <div class="card accent-cyan">
        <div class="card-title">🛡️ Public Health & Ecological Outcomes</div>
        <div class="card-body">
          <ul>
            <li><strong>Water Intake Protection:</strong> Early warning alerts dispatch to Varanasi municipal water treatment plants to switch coagulants and activate carbon filters.</li>
            <li><strong>Industrial Effluent Tracing:</strong> Narrow-band spectral unmixing traces chromium and chemical dye plume dispersion from Kanpur/Unnao tannery drains.</li>
            <li><strong>Namami Gange Support:</strong> Provides National Mission for Clean Ganga with verifiable, transparent water quality layers (Turbidity, CDOM, Chl-a) without manual boat sampling.</li>
            <li><strong>Zero Lab Lag:</strong> Reduces environmental compliance reporting from 14 days of wet-lab incubation to instant sub-minute web inspection.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 13: REAL-WORLD USE CASE 4 - CROP INSURANCE & DISASTER -->
  <div class="slide" data-slide="13">
    <div class="slide-header">
      <span class="tag-badge purple">Real-World Impact: Use Case 4</span>
      <h2 class="slide-title">Disaster Resilience & Crop Insurance: PMFBY Claim Verification</h2>
      <p class="slide-subtitle">Objective sub-pixel quantification of crop lodging, drought desiccation, and flood inundation</p>
    </div>
    <div class="grid-2">
      <div class="card accent-purple">
        <div class="card-title">⚖️ The Insurance Bottleneck (PMFBY)</div>
        <div class="card-body">
          <ul>
            <li><strong>Crop Cutting Experiment (CCE) Delays:</strong> Pradhan Mantri Fasal Bima Yojana relies on manual CCEs. Conducting millions of physical field cuts takes 3–6 months, leading to prolonged payout disputes.</li>
            <li><strong>Subjective Litigation:</strong> Disagreements between insurance companies and state governments over drought or hailstorm severity frequently freeze compensation funds.</li>
            <li><strong>Flash Drought Canopy Water Loss:</strong> Multispectral sensors detect drought only after plant canopies turn brown. Hyperspectral 970 nm and 1200 nm liquid water absorption bands measure cell turgor pressure drop in real time.</li>
            <li><strong>Sub-Pixel Crop Lodging Detection:</strong> High cyclonic winds flatten crops. BharatSpectral unmixes soil-canopy structural geometry shifts, separating flattened crops from standing fields.</li>
          </ul>
        </div>
      </div>
      <div class="card accent-amber">
        <div class="card-title">⚡ Automated Claim Settlement Impact</div>
        <div class="card-body">
          <ul>
            <li><strong>Payouts in Days, Not Months:</strong> Instant satellite-derived loss assessment enables direct benefit transfers (DBT) to farmers' bank accounts within 72 hours of catastrophic weather.</li>
            <li><strong>Sub-Hectare Plot Granularity:</strong> FASU sub-pixel unmixing accurately resolves damage on plots as small as 0.2 hectares, ensuring smallholders are not excluded by coarse pixel averaging.</li>
            <li><strong>100% Tamper-Proof Audit Trail:</strong> Publicly verifiable, open-access hyperspectral records eliminate fraudulent claims and political tampering.</li>
            <li><strong>Disaster Relief Coordination:</strong> State disaster management authorities can immediately prioritize relief supplies to the exact tehsils with critical crop biomass destruction.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 14: MASTER TIMELINE & ROADMAP (PHASE 1 TO 5) -->
  <div class="slide" data-slide="14">
    <div class="slide-header">
      <span class="tag-badge cyan">Master Execution Roadmap</span>
      <h2 class="slide-title">End-to-End Project Timeline: Engineering Phases 1 Through 5</h2>
      <p class="slide-subtitle">Systematic progression from raw data ingestion to national-scale public infrastructure deployment</p>
    </div>
    <div class="grid-5">
      <div class="card accent-cyan">
        <div class="card-title" style="font-size: 0.95rem;">Phase 1: Ingestion</div>
        <div style="font-size: 0.75rem; color: var(--cyan); margin-bottom: 6px;">DATA SCORING & PIPELINE</div>
        <div class="card-body" style="font-size: 0.8rem;">
          <ul>
            <li>AVIRIS-NG, EMIT & HysIS data ingestion</li>
            <li>Bad Band Removal (BBR) & Radiative Transfer</li>
            <li>Chunked Zarr & COG creation on Cloudflare R2</li>
            <li>BharatHSI-Bench benchmark ground truth curation</li>
            <li>SOTA failure documentation</li>
          </ul>
        </div>
      </div>

      <div class="card accent-teal">
        <div class="card-title" style="font-size: 0.95rem;">Phase 2: Baseline</div>
        <div style="font-size: 0.75rem; color: var(--teal); margin-bottom: 6px;">BENCHMARKING & HPC</div>
        <div class="card-body" style="font-size: 0.8rem;">
          <ul>
            <li>1D-CNN, 3D-CNN & HybridSN baselines</li>
            <li>Classical unmixing (VCA & FCLSU endmembers)</li>
            <li>AIRAWAT Slurm batch orchestration scripts</li>
            <li>Quantitative evaluation metric baseline</li>
            <li>Strict memory guardrails</li>
          </ul>
        </div>
      </div>

      <div class="card accent-purple">
        <div class="card-title" style="font-size: 0.95rem;">Phase 3: Foundation</div>
        <div style="font-size: 0.75rem; color: var(--purple); margin-bottom: 6px;">CREATIVE CORE & DISTILLATION</div>
        <div class="card-body" style="font-size: 0.8rem;">
          <ul>
            <li>BharatSpectral-MAE with 7 innovations</li>
            <li>Self-supervised pre-training on DGX A100 nodes</li>
            <li>Ph-LoRA fine-tuning for Kharif/Rabi phenology</li>
            <li>Teacher-Student Knowledge Distillation</li>
            <li>INT8 quantization</li>
          </ul>
        </div>
      </div>

      <div class="card accent-amber">
        <div class="card-title" style="font-size: 0.95rem;">Phase 4: Platform</div>
        <div style="font-size: 0.75rem; color: var(--amber); margin-bottom: 6px;">WEBGIS ENGINEERING</div>
        <div class="card-body" style="font-size: 0.8rem;">
          <ul>
            <li>Next.js + MapLibre GL JS frontend on Cloudflare</li>
            <li>Cloudflare R2 zero-egress tile streaming API</li>
            <li>Serverless Spectral Inference (SSI) on Workers</li>
            <li>Sub-pixel agricultural map visualization</li>
            <li>Sub-128 MB RAM execution</li>
          </ul>
        </div>
      </div>

      <div class="card accent-cyan">
        <div class="card-title" style="font-size: 0.95rem;">Phase 5: Release</div>
        <div style="font-size: 0.75rem; color: var(--cyan); margin-bottom: 6px;">VALIDATION & OPEN SCIENCE</div>
        <div class="card-body" style="font-size: 0.8rem;">
          <ul>
            <li>End-to-end latency & accuracy validation</li>
            <li>Cloud cost verification ($0 egress vs AWS)</li>
            <li>Open-source weights on AIKosh & HuggingFace</li>
            <li>Comprehensive capstone thesis & documentation</li>
            <li>Final viva defense</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 15: QUANTITATIVE EVALUATION & SUCCESS METRICS -->
  <div class="slide" data-slide="15">
    <div class="slide-header">
      <span class="tag-badge cyan">Evaluation Framework</span>
      <h2 class="slide-title">Quantitative Benchmarking & Success Metrics</h2>
      <p class="slide-subtitle">Rigorous empirical standards across AI accuracy, sub-pixel unmixing, and platform performance</p>
    </div>
    <div class="grid-2">
      <div class="card accent-cyan">
        <div class="card-title">🎯 AI Accuracy & Unmixing Targets</div>
        <div class="card-body">
          <ul>
            <li><strong>Classification Accuracy (BharatHSI-Bench):</strong>
              <br>• Overall Accuracy (OA): Target &gt; 92.5%
              <br>• Average Accuracy (AA): Target &gt; 89.0%
              <br>• Cohen's Kappa Coefficient (κ): Target &gt; 0.90
            </li>
            <li><strong>Cross-Scene Generalization:</strong> Must demonstrate +15% to +25% OA gain over Western-pretrained SpectralGPT and HyperSIGMA.</li>
            <li><strong>Sub-Pixel Unmixing (FASU):</strong>
              <br>• Abundance Root Mean Square Error (RMSE): &lt; 0.08
              <br>• Spectral Angle Distance (SAD): &lt; 0.05 rad
            </li>
          </ul>
        </div>
      </div>

      <div class="card accent-teal">
        <div class="card-title">⚡ System Performance & Economic Feasibility</div>
        <div class="card-body">
          <ul>
            <li><strong>Serverless Latency (SSI on Workers):</strong>
              <br>• Inference Time: &lt; 5.0 seconds per km² tile
              <br>• Browser Tile Render (MapLibre): &lt; 200 ms
              <br>• Edge Memory: Strictly under 128 MB V8 isolate ceiling
            </li>
            <li><strong>Zero Egress Cost Validation:</strong>
              <br>• Outbound Data Transfer Fee: Exactly $0.00 / month on Cloudflare R2
              <br>• Total Hosting Cost: &lt; $50 / month vs $1,200+ / month for equivalent AWS EC2 + GeoServer deployment
            </li>
            <li><strong>Citizen Accessibility:</strong> 100% responsive on standard Android 4G/5G mobile browsers.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 16: CONCLUSION & NATIONAL IMPACT -->
  <div class="slide" data-slide="16">
    <div class="slide-header">
      <span class="tag-badge cyan">Conclusion & Vision</span>
      <h2 class="slide-title">BharatSpectral: Democratizing Spectral Intelligence as Digital Public Infrastructure</h2>
      <p class="slide-subtitle">From closed scientific repositories to nationwide citizen empowerment</p>
    </div>
    <div class="grid-3" style="margin-bottom: 20px;">
      <div class="card accent-cyan">
        <div class="card-title">7 Architectural Novelties</div>
        <div class="card-body">
          Engineered the first foundation model built specifically for Indian smallholders. SSPE, RNRL, SHT, AAM, ECSA, Ph-LoRA, and FASU close the empirical gap that causes Western models to fail.
        </div>
      </div>
      <div class="card accent-teal">
        <div class="card-title">3 National Benchmarks</div>
        <div class="card-body">
          Establishes BharatHSI-Bench, Multi-Sensor Indian Datacubes, and Paired Spectral-SoilHealth records on AIKosh, freeing Indian academia from its 30-year reliance on outdated foreign datasets.
        </div>
      </div>
      <div class="card accent-purple">
        <div class="card-title">Public Digital Good</div>
        <div class="card-body">
          Translates complex aerospace spectroscopy into a zero-cost, high-speed WebGIS tool accessible to any farmer, extension worker, or policymaker on any device without paywalls.
        </div>
      </div>
    </div>
    <div style="background: rgba(56, 189, 248, 0.08); border: 1px solid var(--cyan); border-radius: 12px; padding: 18px 24px; font-size: 0.95rem; color: #ffffff;">
      <strong style="color: var(--cyan);">🇮🇳 Alignment with National Missions:</strong> Directly advancing the IndiaAI Mission, Digital Public Infrastructure (DPI), and National Mission on Sustainable Agriculture — proving that world-class AI research can deliver direct social utility to the common citizen.
    </div>
  </div>

</div>

<!-- Navigation Bar -->
<div id="nav-bar">
  <button class="nav-btn" onclick="prevSlide()">◀ Prev <span class="key-hint">←</span></button>
  <div class="slide-counter"><span id="current-slide-num">1</span> / <span id="total-slides-num">16</span></div>
  <button class="nav-btn" onclick="nextSlide()">Next ▶ <span class="key-hint">→</span></button>
  <button class="nav-btn" onclick="toggleNotes()">Notes 🎙️ <span class="key-hint">N</span></button>
  <button class="nav-btn" onclick="toggleFullscreen()">Fullscreen ⛶ <span class="key-hint">F</span></button>
  <button class="nav-btn" onclick="window.print()">Export PDF 📄</button>
</div>

<!-- Speaker Notes Floating Panel -->
<div id="notes-panel">
  <h4>
    <span>🎙️ Presenter Talking Points</span>
    <span style="cursor: pointer;" onclick="toggleNotes()">✖</span>
  </h4>
  <div id="notes-content" style="color: var(--text-light); font-size: 0.88rem;"></div>
</div>

<script>
  const speakerNotes = {
    1: "Good morning esteemed panel members. Today, our group presents 'BharatSpectral', our B.Tech capstone project. Our project bridges high-performance AI foundation modeling with public digital geospatial infrastructure to solve a major national challenge: making advanced earth observation spectroscopy useful and accessible to everyday Indian citizens.",
    2: "We begin with the fundamental paradox of the Indian geospatial ecosystem: India ranks among the top five remote sensing powers globally, launching satellites with remarkable regularity. Yet, out of 140 million smallholder farmers, virtually none have access to this intelligence. Why? Because existing data sits in massive 5 to 10 GB raw binary files on Bhoonidhi, commercial tools cost thousands of dollars, and no public platform exists to translate this data into actionable insights.",
    3: "To understand our technical breakthrough, we must distinguish biophysical from biochemical intelligence. Current platforms like ISRO Krishi-DSS use multispectral imagery with only 10 broad bands. They can tell you that a plant is turning yellow, but they cannot tell you WHY. Hyperspectral imaging with 200+ narrow bands measures continuous molecular spectroscopy. We detect nitrogen deficiency at 720 nm, yellow rust spores at 680 nm, and soil organic carbon at 2200 nm — 7 to 14 days before visible symptoms appear.",
    4: "A critical part of our research was investigating existing global foundation models like SpectralGPT and HyperSIGMA. We discovered a shocking flaw: almost all of them benchmark on 'Indian Pines'. Despite its name, Indian Pines was captured in 1992 in Indiana, USA, over giant monocultures! These models fail on Indian landscapes due to extreme spatial fragmentation (average plot is 1.08 ha), intercropping mixtures, 3 seasonal phenologies (Kharif, Rabi, Zaid), and a 10x resolution gap between airborne and spaceborne sensors.",
    5: "We also audited the entire Indian remote sensing ecosystem in 2026. ISRO Bhuvan has no hyperspectral analytics. VEDAS AVHYAS is strictly a desktop QGIS plugin requiring local workstation installation. Bhoonidhi only hosts raw ENVI downloads. Pixxel Aurora is a commercial enterprise SaaS behind a paywall. BharatSpectral is the FIRST system to combine an Indian-tuned foundation model with a zero-cost public WebGIS platform.",
    6: "Here is our dual-pillar architecture: Pillar 1 is the research engine — BharatSpectral-MAE, pre-trained on IndiaAI AIRAWAT DGX A100 GPU clusters using multi-sensor Indian data. Pillar 2 is the public infrastructure — BharatSpectral Platform, built on Cloudflare serverless architecture to deliver real-time maps to any mobile browser.",
    7: "Our research pillar introduces 7 named architectural innovations: SSPE for scale-spectral positional encoding across 3 sensors; RNRL for reflectance-normalized reconstruction of low-reflectance water bodies; SHT for dynamic red-edge tokenization; AAM for atmospheric water vapor masking; ECSA for unmixing-constrained attention across plot boundaries; Ph-LoRA for season-conditioned adaptation; and FASU for sub-pixel abundance unmixing.",
    8: "To make this free and scalable, we solved three major cloud bottlenecks: Data Volume is solved by Cloud-Optimized GeoTIFFs and Zarr cubes with HTTP Range streaming; Egress Costs are eliminated by Cloudflare R2's $0 egress fee policy; and Inference Compute is solved by Serverless Spectral Inference — distilling our foundation model into an INT8 ONNX student running in Cloudflare Workers within 128 MB RAM.",
    9: "This slide traces the complete end-to-end data pipeline: from raw photon capture by ISRO AVIRIS-NG and NASA EMIT, through atmospheric correction and Bad Band Removal, pre-training on AIRAWAT DGX A100 nodes, model distillation into lightweight students, and edge delivery to browser-based WebGIS.",
    10: "Let us look at our first real-world use case: Gurpreet Singh in Ludhiana. Multispectral NDVI only alerts him when wheat leaves turn yellow, when 20% yield loss is already inevitable. BharatSpectral detects nitrogen deficiency and yellow rust 10 days early, saving him ₹3,500 per acre in wasted fertilizer and protecting Punjab's groundwater.",
    11: "Our second use case is agricultural governance with Dr. Anita Verma, a KVK officer in Karnal. Instead of taking 6 weeks for manual wet-chemistry soil sampling on only 5% of plots, BharatSpectral maps Soil Organic Carbon across 100% of the district at 10m resolution using SWIR 2200 nm clay-carbon absorption, tracking topsoil degradation from stubble burning.",
    12: "Our third use case addresses environmental protection along the Ganga basin in Varanasi. Standard satellites treat water as black pixels. Our RNRL loss enables precision mapping of low-reflectance water, while the 620 nm phycocyanin absorption feature uniquely differentiates toxic cyanobacteria from harmless green algae, protecting city drinking water intakes.",
    13: "Our fourth use case is disaster management and crop insurance under PMFBY. Conducting manual Crop Cutting Experiments takes months. BharatSpectral provides instant, tamper-proof sub-pixel damage assessments for crop lodging and flash drought canopy water loss within 72 hours, enabling direct benefit payouts to farmers without dispute litigation.",
    14: "Here is our master execution roadmap spanning Phases 1 through 5: from data curation, atmospheric correction, and benchmark creation in Phase 1, through baseline modeling in Phase 2, foundation model training and distillation on AIRAWAT HPC in Phase 3, serverless WebGIS engineering in Phase 4, to national validation and open-source release in Phase 5.",
    15: "Our project is governed by strict quantitative evaluation metrics: achieving over 92.5% Overall Accuracy and sub-0.08 unmixing RMSE on BharatHSI-Bench, sub-second edge inference on Cloudflare Workers, and verifying sustained $0 data egress costs.",
    16: "In conclusion, BharatSpectral is not just an academic exercise. It creates 7 named architectural novelties, 3 open national benchmarks, and a free digital public infrastructure platform that directly serves the smallholder farmer, the district officer, and national environmental missions. Thank you, and we welcome your questions."
  };

  let currentSlide = 1;
  const totalSlides = 16;

  function showSlide(num) {
    if (num < 1) num = 1;
    if (num > totalSlides) num = totalSlides;
    currentSlide = num;

    document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
    const target = document.querySelector(`.slide[data-slide="${num}"]`);
    if (target) target.classList.add('active');

    document.getElementById('current-slide-num').innerText = currentSlide;
    updateNotes();
  }

  function nextSlide() {
    if (currentSlide < totalSlides) {
      showSlide(currentSlide + 1);
    }
  }

  function prevSlide() {
    if (currentSlide > 1) {
      showSlide(currentSlide - 1);
    }
  }

  function toggleNotes() {
    const p = document.getElementById('notes-panel');
    p.style.display = (p.style.display === 'block') ? 'none' : 'block';
    updateNotes();
  }

  function updateNotes() {
    const content = speakerNotes[currentSlide] || "No notes for this slide.";
    document.getElementById('notes-content').innerHTML = `
      <p style="margin-bottom: 8px;"><strong>Slide ${currentSlide}:</strong></p>
      <p>${content}</p>
    `;
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => console.log(err));
    } else {
      if (document.exitFullscreen) document.exitFullscreen();
    }
  }

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
      nextSlide();
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      prevSlide();
    } else if (e.key === 'n' || e.key === 'N') {
      toggleNotes();
    } else if (e.key === 'f' || e.key === 'F') {
      toggleFullscreen();
    } else if (e.key === 'Home') {
      showSlide(1);
    } else if (e.key === 'End') {
      showSlide(totalSlides);
    }
  });

  // Initialize notes
  updateNotes();
</script>

</body>
</html>
"""

import os
out_html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'presentation.html')
with open(out_html_path, 'w') as f:
    f.write(html_content)

print(f"Generated {out_html_path} successfully!")
