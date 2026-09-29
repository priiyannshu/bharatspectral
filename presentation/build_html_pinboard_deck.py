#!/usr/bin/env python3
"""
build_html_pinboard_deck.py
Builds the 19-Slide Academic Pinboard Presentation Deck for BharatSpectral
in the exact ~/ppt/vs theme (references_pinboard.html corkboard & pushpins):
- Pure corkboard surface with beveled wooden frame
- Parchment & Kraft paper cards with realistic drop shadows
- Washi tape strips and 3D pushpins
- High-resolution scientific diagrams and comic strip assets
- Single clean PPTX download button
- Full keyboard and click navigation via deck.js
"""

import os

OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>BharatSpectral — Democratized Spectral-Semantic Intelligence (DSSI)</title>

  <!-- Google Fonts: Inter, Kalam, JetBrains Mono, Caveat -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&family=Kalam:wght@400;700&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="style.css">
  <style>
    /* Pinboard slide card layout enhancements */
    .slide {
      display: none;
      width: 100%;
      height: 100%;
      padding: 24px 32px;
      overflow-y: auto;
      box-sizing: border-box;
      position: absolute;
      top: 0;
      left: 0;
    }
    .slide.active {
      display: flex;
      flex-direction: column;
      animation: fadeInCard 0.25s ease-out;
    }
    @keyframes fadeInCard {
      from { opacity: 0; transform: scale(0.99); }
      to { opacity: 1; transform: scale(1); }
    }
    .board-header-note {
      position: relative;
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px 22px;
      margin-bottom: 18px;
      box-shadow: var(--shadow-paper);
    }
    .board-header-note h2 {
      font-family: 'Kalam', cursive;
      font-size: 1.55rem;
      font-weight: 700;
      color: var(--text);
      line-height: 1.25;
    }
    .board-header-note p {
      font-size: 0.85rem;
      color: var(--text-dim);
      margin-top: 2px;
    }
    .grid-2col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      flex: 1;
    }
    .grid-3col {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      flex: 1;
    }
    .paper-card {
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px 24px;
      position: relative;
      box-shadow: var(--shadow-paper);
    }
    .paper-card.style-kraft {
      background: var(--surface2);
      border-color: var(--border-dark);
    }
    .paper-card.style-parchment {
      background: #fffdf5;
    }
    .paper-card.style-lined {
      background-image: repeating-linear-gradient(transparent, transparent 27px, #e8ddcf 28px);
    }
    .card-title {
      font-size: 1.05rem;
      font-weight: 800;
      color: var(--text);
      margin-bottom: 8px;
      font-family: 'Inter', sans-serif;
    }
    .card-img-box {
      background: #090d16;
      border-radius: 8px;
      padding: 8px;
      text-align: center;
      margin: 10px 0;
      border: 1px solid var(--border);
    }
    .card-img-box img {
      max-width: 100%;
      max-height: 250px;
      object-fit: contain;
      border-radius: 4px;
    }
    .badge {
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      padding: 3px 10px;
      border-radius: 6px;
      margin-bottom: 8px;
    }
    .badge-cyan { background: rgba(11, 114, 133, 0.15); color: var(--accent-cyan); border: 1px solid var(--accent-cyan); }
    .badge-green { background: rgba(43, 138, 62, 0.15); color: var(--accent-green); border: 1px solid var(--accent-green); }
    .badge-purple { background: rgba(103, 65, 217, 0.15); color: var(--accent-purple); border: 1px solid var(--accent-purple); }
    .badge-amber { background: rgba(217, 155, 0, 0.15); color: var(--accent-yellow); border: 1px solid var(--accent-yellow); }
    .badge-red { background: rgba(201, 42, 42, 0.15); color: var(--accent-red); border: 1px solid var(--accent-red); }
    
    .status-widget {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.76rem;
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 9999px;
      background: #e6f4ea;
      color: #137333;
      border: 1px solid #ceead6;
      margin-left: 10px;
    }
    .note-badge {
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 2px 7px;
      background: rgba(103, 65, 217, 0.12);
      border: 1px solid var(--accent-purple);
      color: var(--accent-purple);
      border-radius: 4px;
      margin-top: 6px;
    }
    .bullet-list {
      margin-left: 18px;
      font-size: 0.85rem;
      color: var(--text-dim);
      line-height: 1.55;
    }
    .bullet-list li { margin-bottom: 6px; }
    table.pin-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.82rem;
      margin-top: 8px;
    }
    table.pin-table th {
      background: #eae0ce;
      color: var(--text);
      font-weight: 700;
      padding: 6px 10px;
      text-align: left;
      border: 1px solid #d8c8af;
    }
    table.pin-table td {
      padding: 6px 10px;
      border: 1px solid #d8c8af;
      color: var(--text);
    }
    table.pin-table tr:nth-child(even) {
      background: #fbf7ee;
    }
  </style>
</head>
<body>
  <div class="app-container">
    
    <!-- Top Control Bar (Only One PPTX Download Option) -->
    <header class="deck-topbar">
      <div class="topbar-left">
        <span class="brand-badge">BHARATSPECTRAL DSSI</span>
        <span class="slide-title-indicator" id="slideTitleIndicator">Slide 1: Beyond Human Sight</span>
      </div>
      <div class="topbar-center">
        <a href="BharatSpectral_MidTerm_Presentation.pptx" download class="btn-ctrl btn-download btn-animated" title="Download Official PowerPoint Presentation">
          📥 <strong>Download PPTX Deck</strong> (16:9 Widescreen)
        </a>
      </div>
      <div class="topbar-right">
        <span class="slide-counter" id="slideCounter">01 / 19</span>
        <button class="btn-ctrl" id="prevBtn" title="Previous Slide (← / P)">◀ Prev</button>
        <button class="btn-ctrl" id="nextBtn" title="Next Slide (→ / Space / N)">Next ▶</button>
        <button class="btn-ctrl" id="fullscreenBtn" title="Toggle Fullscreen (F)">⛶ Fullscreen</button>
      </div>
    </header>

    <!-- Pinboard Presentation Stage -->
    <main class="stage-viewport">
      <div class="corkboard-frame">
        <div class="corkboard-surface">
          <div class="slides-wrapper">

            <!-- SLIDE 1: Title Pinboard -->
            <section class="slide active" id="slide-1">
              <div class="paper-card style-parchment" style="text-align: center; margin-bottom: 16px;">
                <div class="washi-tape tape-center"></div>
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-purple pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-cyan">B.TECH CAPSTONE PROJECT REVIEW • MID-TERM EVALUATION</span>
                <h1 style="font-family:'Kalam', cursive; font-size:2.2rem; font-weight:700; color:var(--text); margin:8px 0;">
                  BharatSpectral: Democratized Spectral-Semantic Intelligence (DSSI)
                </h1>
                <div style="font-size:0.95rem; font-weight:600; color:var(--accent-cyan);">
                  Physics-Informed Hyperspectral Foundation Model &amp; Serverless WebGIS Public Infrastructure for Indian Earth Observation
                </div>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-yellow pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <span class="badge badge-amber">ACT I • FOUNDATIONAL MOTIVATION</span>
                  <div class="card-title">Beyond Human Sight: Continuous Spectroscopy</div>
                  <div class="card-img-box">
                    <img src="assets/spectrum_contrast.png" alt="Spectrum Contrast">
                  </div>
                  <p style="font-size:0.82rem; color:var(--text-dim); margin-top:6px;">
                    Human vision is restricted to a 380–700 nm optical sliver (1.4% of solar reflected photons). BharatSpectral captures 400–2500 nm across 425 continuous narrow channels.
                  </p>
                </div>
                <div class="paper-card style-kraft">
                  <div class="pushpin pin-green pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <span class="badge badge-green">STUDENT INVESTIGATORS &amp; SUPERVISOR</span>
                  <div class="card-title">Dual-Pillar National Innovation</div>
                  <ul class="bullet-list" style="margin-top:10px;">
                    <li><strong>Research Pillar:</strong> BharatSpectral-MAE Foundation Model (SSPE, RNRL, SHT, AAM, ECSA, Ph-LoRA, FASU).</li>
                    <li><strong>Product Pillar:</strong> Serverless Edge WebGIS on Cloudflare R2 + Workers for 140 million smallholders.</li>
                    <li><strong>Grounding:</strong> Evaluated on AVIRIS-NG India, ISRO HysIS, and NASA EMIT.</li>
                  </ul>
                  <div style="margin-top:16px; padding:10px; background:rgba(11,114,133,0.08); border-radius:8px; border:1px solid var(--accent-cyan); font-size:0.8rem;">
                    <strong>National Alignment:</strong> IndiaAI Mission &amp; Geospatial Digital Public Infrastructure (DPI).
                  </div>
                </div>
              </div>
            </section>

            <!-- SLIDE 2: Engineering Objectives -->
            <section class="slide" id="slide-2">
              <div class="board-header-note">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-cyan">SCOPE &amp; MILESTONES</span>
                <h2>Engineering Objectives: Capstone 7th Semester Scope</h2>
                <p>Formal deliverable commitments for Phase 1 &amp; Phase 2 evaluated against real Indian agricultural data</p>
              </div>
              <div class="grid-3col">
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <span class="badge badge-cyan">PILLAR 1: CURATE &amp; STANDARDIZE</span>
                  <div class="card-title">Indian HSI Corpus Assembly</div>
                  <ul class="bullet-list">
                    <li>Ingest heterogeneous cubes: AVIRIS-NG India (425b), ISRO HysIS (220b), NASA EMIT (285b).</li>
                    <li>Apply 6S radiative atmospheric water vapor correction (1.4μm &amp; 1.9μm masking).</li>
                    <li>Standardize spatial-spectral patch generator for fragmented smallholders.</li>
                  </ul>
                  <div class="status-widget" style="margin-top:12px;">● PHASE 1 COMPLETE</div>
                </div>
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-amber pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <span class="badge badge-amber">PILLAR 2: BENCHMARK &amp; DIAGNOSE</span>
                  <div class="card-title">Empirical Failure Proof</div>
                  <ul class="bullet-list">
                    <li>Train baseline architectures: RF, SVM-RBF, HybridSN (3D-2D CNN), 3D-CNN, Spectral Transformer.</li>
                    <li>Quantify catastrophic 22%–37% OA drop under Indian agricultural domain shift.</li>
                    <li>Audit GIS physical spectroscopic tools (SAM, LSU/FCLS) under non-linear canopy scattering.</li>
                  </ul>
                  <div class="status-widget" style="margin-top:12px;">● PHASE 2 COMPLETE</div>
                </div>
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-purple pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <span class="badge badge-purple">PILLAR 3: ARCHITECT NOVELTY</span>
                  <div class="card-title">The 7 Named Innovations</div>
                  <ul class="bullet-list">
                    <li>Formalize BharatSpectral-MAE: SSPE, RNRL, SHT, AAM, ECSA, Ph-LoRA, and FASU.</li>
                    <li>Bridge optical quantum physics with self-attention Transformer heads.</li>
                    <li>Prepare high-performance GPU pretraining pipeline for 8th semester scaling.</li>
                  </ul>
                  <div class="note-badge" style="margin-top:12px;">PHASE 3 ACTIVE FRONTIER</div>
                </div>
              </div>
            </section>

            <!-- SLIDE 3: Continuous Spectroscopy -->
            <section class="slide" id="slide-3">
              <div class="board-header-note">
                <div class="pushpin pin-green pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-green">SPECTRAL PHYSICS</span>
                <h2>Continuous Spectroscopy: What Each Spectral Band Captures</h2>
                <p>Narrow-band molecular absorption physics across VNIR, Red-Edge, NIR, and SWIR regimes</p>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-green pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title">Continuous Reflectance Signature</div>
                  <div class="card-img-box">
                    <img src="assets/continuous_spectroscopy.png" alt="Continuous Spectroscopy Curve">
                  </div>
                </div>
                <div class="paper-card style-kraft">
                  <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <span class="badge badge-cyan">ARCHITECTURAL INNOVATIONS SEEDED</span>
                  <div class="card-title">Diagnostic Absorption Physics</div>
                  <ul class="bullet-list" style="margin-top:8px;">
                    <li><strong>400–700 nm (VNIR):</strong> Plant pigment absorption (Chlorophyll a/b, Carotenoids).</li>
                    <li><strong>700–750 nm (Red-Edge):</strong> Steep cellular structure cliff. <span class="note-badge">NOTE: SHT</span> (Spectral Harmonic Tokenizer allocates fine tokens here).</li>
                    <li><strong>970 &amp; 1200 nm (NIR):</strong> Cellular liquid Equivalent Water Thickness (EWT).</li>
                    <li><strong>1.4 &amp; 1.9 μm:</strong> Atmospheric water vapor zero-transmission gaps. <span class="note-badge">NOTE: AAM</span> (Atmospheric Absorption Masking).</li>
                    <li><strong>2.1–2.3 μm (SWIR):</strong> Organic protein nitrogen, soil organic carbon (SOC), clay mineral lattices.</li>
                  </ul>
                </div>
              </div>
            </section>

            <!-- SLIDE 4: Photon Pinball Scattering -->
            <section class="slide" id="slide-4">
              <div class="board-header-note">
                <div class="pushpin pin-purple pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-purple">CANOPY RADIATIVE TRANSFER</span>
                <h2>The 'Pinball Machine' Physics: Non-Linear Scattering &amp; 3D Pixels</h2>
                <p>Why multi-tier Indian smallholder canopies require 3D tensor foundation representations</p>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-purple pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title">Canopy Ricochet vs. 3D Data Cube</div>
                  <div class="card-img-box">
                    <img src="assets/photon_pinball_cube.png" alt="Photon Pinball & 3D Cube">
                  </div>
                </div>
                <div class="paper-card style-kraft">
                  <div class="pushpin pin-yellow pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <span class="badge badge-amber">PHYSICAL BREAKDOWN</span>
                  <div class="card-title">Why Monoculture Assumptions Collapse</div>
                  <ul class="bullet-list" style="margin-top:8px;">
                    <li><strong>Multi-Bounce Scattering:</strong> Sunlight enters intercropped sorghum + pigeon pea and ricochets between leaves and soil before sensor reception.</li>
                    <li><strong>Failure of Linear Unmixing:</strong> Classical GIS (LSU/FCLS) assumes linear superposition ($r = \sum a_i e_i$). Ricochets cause non-linear cross-talk ($RMSE_A > 0.15$).</li>
                    <li><span class="note-badge">NOTE: SSPE</span> <strong>Scale-Spectral Positional Encoding:</strong> Jointly encodes GSD ($4–60\,\text{m}$), bandwidth, and mixture entropy.</li>
                    <li><span class="note-badge">NOTE: FASU</span> <strong>Foundation-Augmented Spectral Unmixing:</strong> Decomposes complex non-linear canopy mixtures using pretrained foundation representations.</li>
                  </ul>
                </div>
              </div>
            </section>

            <!-- SLIDE 5: Interdisciplinary Venn Diagram -->
            <section class="slide" id="slide-5">
              <div class="board-header-note">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-cyan">RESEARCH FOUNDATIONS</span>
                <h2>The Intersection of Human Knowledge Systems</h2>
                <p>Synthesizing optical spectroscopy physics, foundation AI architectures, and open WebGIS public infrastructure</p>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-img-box">
                    <img src="assets/venn_diagram.png" alt="Interdisciplinary Venn Diagram">
                  </div>
                </div>
                <div class="paper-card style-kraft">
                  <div class="pushpin pin-green pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <span class="badge badge-green">DISCIPLINARY CONVERGENCE</span>
                  <div class="card-title">Why Pure Computer Science is Insufficient</div>
                  <ul class="bullet-list" style="margin-top:8px;">
                    <li><strong>Spectroscopy Physics:</strong> Provides ground truth absorption laws, radiative transfer equations, and atmospheric absorption gap constraints.</li>
                    <li><strong>Foundation Model AI:</strong> Provides self-attention capacity, masked autoencoding pretraining, and non-linear parameter-efficient adaptation (LoRA).</li>
                    <li><strong>WebGIS Public Infrastructure:</strong> Eliminates cloud costs through Cloudflare R2 zero-egress storage and browser-edge ONNX WASM inference.</li>
                    <li><strong>Core Convergence:</strong> <strong>BharatSpectral (DSSI)</strong> delivers democratized biochemical intelligence directly to citizen devices.</li>
                  </ul>
                </div>
              </div>
            </section>

            <!-- SLIDE 6: Indian Landmass Coverage -->
            <section class="slide" id="slide-6">
              <div class="board-header-note">
                <div class="pushpin pin-green pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-green">DATASET FOUNDATIONS</span>
                <span class="status-widget">● PHASE 1 COMPLETE</span>
                <h2>Open Hyperspectral Corpus over the Indian Landmass</h2>
                <p>Curated heterogeneous dataset harmonizing airborne AVIRIS-NG India, spaceborne ISRO HysIS, and NASA EMIT</p>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-green pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-img-box">
                    <img src="assets/india_hsi_coverage.png" alt="India Coverage Map">
                  </div>
                </div>
                <div class="paper-card style-kraft">
                  <div class="pushpin pin-purple pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <span class="badge badge-purple">CORPUS HARMONIZATION</span>
                  <div class="card-title">Sensor Heterogeneity &amp; Coverage</div>
                  <ul class="bullet-list" style="margin-top:8px;">
                    <li><strong>AVIRIS-NG India:</strong> 425 continuous bands (380–2510 nm), 4–8m GSD flightlines over Anand (Gujarat), Godavari Basin (AP), and Punjab tracts.</li>
                    <li><strong>ISRO HysIS:</strong> 220 bands (VNIR/SWIR), 30m spaceborne GSD.</li>
                    <li><strong>NASA EMIT:</strong> 285 bands (381–2493 nm), 60m GSD on the International Space Station.</li>
                    <li><span class="note-badge">NOTE: RNRL</span> <strong>Reflectance-Normalized Reconstruction Loss:</strong> Prevents gradients from collapsing in low-reflectance SWIR bands (&lt;5% reflectance).</li>
                  </ul>
                </div>
              </div>
            </section>

            <!-- SLIDE 7: Preprocessing Pipeline -->
            <section class="slide" id="slide-7">
              <div class="board-header-note">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-cyan">DATA PIPELINE</span>
                <span class="status-widget">● PHASE 1 DETAIL</span>
                <h2>Preprocessing &amp; Physical Normalization Pipeline</h2>
                <p>Converting raw Bhoonidhi/STAC binary radiance files into analysis-ready standardized spatial-spectral patches</p>
              </div>
              <div class="paper-card style-parchment" style="margin-bottom:12px;">
                <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box">
                  <img src="assets/preprocessing_pipeline.png" alt="4-Stage Preprocessing Pipeline">
                </div>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-kraft">
                  <span class="badge badge-green">STAGE 1 &amp; 2: RADIATIVE NORMALIZATION</span>
                  <p style="font-size:0.84rem; color:var(--text); line-height:1.5;">
                    Removes atmospheric path radiance ($L_{path}$) via 6S radiative transfer code, then converts raw 16-bit integer Digital Numbers into $[0.0, 1.0]$ Top-of-Canopy surface reflectance tensors.
                  </p>
                </div>
                <div class="paper-card style-kraft">
                  <span class="badge badge-purple">STAGE 3 &amp; 4: MASKING &amp; SAMPLING</span>
                  <p style="font-size:0.84rem; color:var(--text); line-height:1.5;">
                    Prunes zero-transmission water absorption windows (1350–1450 nm and 1800–1950 nm) retaining 200 standardized bands, then generates $9\times 9 \times B$ and $15\times 15 \times B$ smallholder patches.
                  </p>
                </div>
              </div>
            </section>

            <!-- SLIDE 8: The Benchmarking Arena -->
            <section class="slide" id="slide-8">
              <div class="board-header-note">
                <div class="pushpin pin-red pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-red">EMPIRICAL EVIDENCE</span>
                <span class="status-widget">● PHASE 2 EVALUATION</span>
                <h2>Benchmarking Previous Attempts: Empirical Proof of Need</h2>
                <p>Grounded benchmark proving that Western HSI models suffer catastrophic collapse on Indian smallholder agriculture</p>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-red pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title">Domain Shift Collapse (22%–37% OA Drop)</div>
                  <div class="card-img-box">
                    <img src="outputs/figures/domain_shift_collapse.png" alt="Domain Shift Collapse Bar Chart">
                  </div>
                </div>
                <div class="paper-card style-kraft">
                  <div class="pushpin pin-amber pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title">Empirical Benchmark Results Table (Pi 5 Testbed)</div>
                  <table class="pin-table">
                    <thead>
                      <tr>
                        <th>Architecture</th>
                        <th>Source OA</th>
                        <th>Indian Target OA</th>
                        <th>Collapse</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr><td>Random Forest</td><td>85.4%</td><td>57.8%</td><td style="color:var(--accent-red); font-weight:700;">-27.6%</td></tr>
                      <tr><td>SVM (RBF Kernel)</td><td>84.6%</td><td>62.2%</td><td style="color:var(--accent-red); font-weight:700;">-22.4%</td></tr>
                      <tr><td><strong>HybridSN (3D-2D CNN)</strong></td><td>92.4%</td><td>55.1%</td><td style="color:var(--accent-red); font-weight:800;">-37.3%</td></tr>
                      <tr><td><strong>3D-CNN (Hamida et al.)</strong></td><td>90.8%</td><td>56.4%</td><td style="color:var(--accent-red); font-weight:800;">-34.4%</td></tr>
                      <tr><td><strong>Spectral Transformer</strong></td><td>93.5%</td><td>60.8%</td><td style="color:var(--accent-red); font-weight:800;">-32.7%</td></tr>
                    </tbody>
                  </table>
                  <p style="font-size:0.78rem; color:var(--text-dim); margin-top:8px;">
                    <strong>The Indian Pines Fallacy:</strong> Models trained on 1992 Indiana monocultures fail in India due to 1.08 ha plot fragmentation, intercropping, and 3-season phenology drift.
                  </p>
                </div>
              </div>
            </section>

            <!-- SLIDE 9: Traditional GIS Critique -->
            <section class="slide" id="slide-9">
              <div class="board-header-note">
                <div class="pushpin pin-amber pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-amber">PHYSICAL CRITIQUE</span>
                <span class="status-widget">● PHASE 2 COMPLETE</span>
                <h2>Why Existing Methods Fail in Indian Smallholder Ecosystems</h2>
                <p>Quantitative audit of physical GIS spectroscopic tools (SAM, LSU in ENVI/QGIS) vs unconstrained deep learning</p>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-amber pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title">GIS LSU Residuals &amp; SAM Magnitude Blindness</div>
                  <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                    <div class="card-img-box"><img src="outputs/figures/gis_linear_unmixing_residuals.png" alt="LSU Residuals"></div>
                    <div class="card-img-box"><img src="outputs/figures/sam_magnitude_confusion.png" alt="SAM Magnitude Confusion"></div>
                  </div>
                </div>
                <div class="paper-card style-kraft">
                  <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <span class="badge badge-cyan">THE DUAL BREAKDOWN</span>
                  <div class="card-title">Physical Tool Limitations</div>
                  <ul class="bullet-list" style="margin-top:8px;">
                    <li><strong>GIS SAM Baseline:</strong> Cosine angle ignores absolute reflectance magnitude, causing a <strong>36.4% false match rate</strong> (confuses shadow/moisture with crop stress).</li>
                    <li><strong>GIS Linear Spectral Unmixing (LSU):</strong> Produces high residual error ($RMSE_A = 0.2775$ on boundaries; <strong>54.2% pixels fail threshold</strong>) due to non-linear canopy scattering.</li>
                    <li><span class="note-badge">NOTE: ECSA</span> <strong>Endmember-Constrained Self-Attention:</strong> Regularizes Transformer attention weights using spectroscopic unmixing priors.</li>
                    <li><span class="note-badge">NOTE: Ph-LoRA</span> <strong>Phenology-Conditioned LoRA:</strong> Modulates adapter weights by Kharif, Rabi, and Zaid phenological stage embeddings.</li>
                  </ul>
                </div>
              </div>
            </section>

            <!-- SLIDE 10: Master Project Timeline -->
            <section class="slide" id="slide-10">
              <div class="board-header-note">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-cyan">EXECUTION ROADMAP</span>
                <h2>Project Progression: What is Done and The Road Ahead</h2>
                <p>Systematic milestone completion across 7th semester and active roadmap for 8th semester scaling</p>
              </div>
              <div class="paper-card style-parchment" style="margin-bottom:12px;">
                <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box">
                  <img src="assets/project_timeline.png" alt="Project Timeline Roadmap">
                </div>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-kraft">
                  <span class="badge badge-green">COMPLETED: PHASE 1 &amp; PHASE 2</span>
                  <p style="font-size:0.82rem; color:var(--text); line-height:1.5;">
                    Data ingestion pipelines verified across 3 sensors; baseline architectures evaluated on Raspberry Pi 5; 22%–37% domain shift collapse empirically proven; GIS spectroscopic failure modes audited.
                  </p>
                </div>
                <div class="paper-card style-kraft">
                  <span class="badge badge-red">ACTIVE: PHASE 3 HEAVYWEIGHT FRONTIER</span>
                  <p style="font-size:0.82rem; color:var(--text); line-height:1.5;">
                    BharatSpectral-MAE pretraining; LoRA adapter tuning; multi-sensor harmonization; followed by Phase 4 &amp; 5 serverless edge deployment on Cloudflare R2 + Workers WebGIS.
                  </p>
                </div>
              </div>
            </section>

            <!-- SLIDE 11: The 7 Core Innovations -->
            <section class="slide" id="slide-11">
              <div class="board-header-note">
                <div class="pushpin pin-purple pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-purple">RESEARCH NOVELTY</span>
                <h2>The 7 Architectural Innovations: Physics-Informed Foundation Model</h2>
                <p>Formalizing BharatSpectral-MAE: Engineered specifically for Indian smallholder Earth Observation</p>
              </div>
              <div class="paper-card style-parchment">
                <div class="pushpin pin-purple pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box">
                  <img src="assets/seven_innovations_flowchart.png" alt="7 Innovations Master Matrix">
                </div>
              </div>
            </section>

            <!-- SLIDE 12: Actionable Yield -->
            <section class="slide" id="slide-12">
              <div class="board-header-note">
                <div class="pushpin pin-green pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-green">ANALYTIC TAXONOMY</span>
                <h2>Actionable Yield: Multi-Domain Biochemical Diagnostics</h2>
                <p>Translating continuous 425-band narrow spectroscopic signatures into 6 national public sector applications</p>
              </div>
              <div class="paper-card style-parchment">
                <div class="pushpin pin-green pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box">
                  <img src="assets/biochemical_taxonomy.png" alt="6-Domain Diagnostic Taxonomy">
                </div>
              </div>
            </section>

            <!-- SLIDE 13: Ground-Level Impact (Farmer Mobile) -->
            <section class="slide" id="slide-13">
              <div class="board-header-note">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-cyan">PRODUCT PILLAR • DIGITAL PUBLIC INFRASTRUCTURE</span>
                <h2>From Orbit to Smallholder: Democratized Mobile Delivery</h2>
                <p>Bridging satellite spectroscopy with citizen smartphones via serverless edge browser inference</p>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title">Mobile WebGIS Edge Experience</div>
                  <div class="card-img-box">
                    <img src="assets/farmer_mobile_app.png" alt="Farmer Mobile Interface">
                  </div>
                </div>
                <div class="paper-card style-kraft">
                  <div class="pushpin pin-green pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <span class="badge badge-green">PUBLIC CITIZEN ACCESS</span>
                  <div class="card-title">The Serverless Spectral Inference (SSI) Stack</div>
                  <ul class="bullet-list" style="margin-top:8px;">
                    <li><strong>Zero App Install:</strong> 100% web browser execution in mobile Chrome/Safari.</li>
                    <li><strong>Zero Egress Cost:</strong> Cloudflare R2 stores COG tiles with $0 egress fees.</li>
                    <li><strong>Edge Inference:</strong> Quantized ONNX WASM model executes sub-pixel unmixing directly inside the farmer's browser in &lt;15 milliseconds.</li>
                    <li><strong>Plain Language Advisories:</strong> Translates spectral nitrogen deficit into direct KVK advice: <em>"Apply 12 kg Urea in Northern plot; skip Southern plot"</em>.</li>
                  </ul>
                </div>
              </div>
            </section>

            <!-- SLIDE 14: Comic 1 - The Invisible Hunger -->
            <section class="slide" id="slide-14">
              <div class="board-header-note">
                <div class="pushpin pin-green pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-green">OPERATIONAL SCENARIO 1</span>
                <h2>Precision Nutrient Optimization: 'The Invisible Hunger'</h2>
                <p>3-Panel Field Story: Pre-symptomatic nitrogen deficiency detection saving fertilizer costs</p>
              </div>
              <div class="paper-card style-parchment">
                <div class="pushpin pin-green pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box">
                  <img src="assets/comic1_invisible_hunger.png" alt="Comic 1: The Invisible Hunger">
                </div>
              </div>
            </section>

            <!-- SLIDE 15: Comic 2 - The Canal Lifeline -->
            <section class="slide" id="slide-15">
              <div class="board-header-note">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-cyan">OPERATIONAL SCENARIO 2</span>
                <h2>Canal Water Quality Alert: 'The Canal Lifeline'</h2>
                <p>3-Panel Field Story: Spaceborne effluent tracking and automated irrigation canal sluice gate diversion</p>
              </div>
              <div class="paper-card style-parchment">
                <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box">
                  <img src="assets/comic2_canal_lifeline.png" alt="Comic 2: The Canal Lifeline">
                </div>
              </div>
            </section>

            <!-- SLIDE 16: Comic 3 - 14-Day Drought Warning -->
            <section class="slide" id="slide-16">
              <div class="board-header-note">
                <div class="pushpin pin-amber pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-amber">OPERATIONAL SCENARIO 3</span>
                <h2>Early Drought Resilience: 'The 14-Day Moisture Warning'</h2>
                <p>3-Panel Field Story: Detecting 970nm &amp; 1200nm cellular water thickness depletion 2 weeks before visual wilting</p>
              </div>
              <div class="paper-card style-parchment">
                <div class="pushpin pin-amber pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box">
                  <img src="assets/comic3_drought_warning.png" alt="Comic 3: 14-Day Drought Warning">
                </div>
              </div>
            </section>

            <!-- SLIDE 17: Comic 4 - Salinity Encroachment -->
            <section class="slide" id="slide-17">
              <div class="board-header-note">
                <div class="pushpin pin-purple pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-purple">OPERATIONAL SCENARIO 4</span>
                <h2>Soil Degradation Defense: 'The Salinity Encroachment'</h2>
                <p>3-Panel Field Story: Subsurface electrical conductivity and clay mineral lattice tracking before salt crusting</p>
              </div>
              <div class="paper-card style-parchment">
                <div class="pushpin pin-purple pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box">
                  <img src="assets/comic4_salinity_defense.png" alt="Comic 4: Salinity Encroachment">
                </div>
              </div>
            </section>

            <!-- SLIDE 18: Three-Fold Democratization Drop -->
            <section class="slide" id="slide-18">
              <div class="board-header-note">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-cyan">SYSTEMS &amp; ECONOMICS</span>
                <h2>Breaking the Barriers: Compute, Economics &amp; Accessibility</h2>
                <p>Democratizing advanced hyperspectral intelligence across computational, economic, and knowledge dimensions</p>
              </div>
              <div class="paper-card style-parchment">
                <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box">
                  <img src="assets/democratization_slabs.png" alt="Three-Fold Democratization Slabs">
                </div>
              </div>
            </section>

            <!-- SLIDE 19: Sovereign Vision & Defense Discussion -->
            <section class="slide" id="slide-19">
              <div class="paper-card style-parchment" style="text-align: center; margin-bottom: 16px;">
                <div class="washi-tape tape-center"></div>
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-purple pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <span class="badge badge-cyan">CAPSTONE VISION • DEFENSE DISCUSSION</span>
                <h1 style="font-family:'Kalam', cursive; font-size:2.2rem; font-weight:700; color:var(--text); margin:8px 0;">
                  BharatSpectral: Sovereign Foundation for Indian Earth Observation
                </h1>
                <div style="font-size:0.95rem; font-weight:600; color:var(--accent-purple);">
                  From Closed Scientific Repositories to National Citizen Empowerment
                </div>
              </div>
              <div class="paper-card style-kraft">
                <div class="pushpin pin-green pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box">
                  <img src="assets/sovereign_vision.png" alt="Sovereign Earth Observation Vision">
                </div>
                <div style="margin-top:14px; text-align:center;">
                  <span class="status-widget" style="font-size:0.85rem; padding:6px 16px;">🌾 Food Security</span>
                  <span class="status-widget" style="font-size:0.85rem; padding:6px 16px;">💧 Water Security</span>
                  <span class="status-widget" style="font-size:0.85rem; padding:6px 16px;">🛡️ Climate Adaptation</span>
                </div>
              </div>
            </section>

          </div><!-- .slides-wrapper -->
        </div><!-- .corkboard-surface -->
      </div><!-- .corkboard-frame -->
    </main>
  </div><!-- .app-container -->

  <script src="deck.js"></script>
</body>
</html>
"""

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated {OUT_PATH} successfully!")
