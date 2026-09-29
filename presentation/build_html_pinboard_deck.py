#!/usr/bin/env python3
"""
build_html_pinboard_deck.py
Builds the clean 16-Slide Academic Pinboard Presentation Deck for BharatSpectral
in the exact corkboard pinboard theme:
- Clean slide title in every header note (no secondary text or clutter)
- 4-Speaker Defense Sequence:
    * Speaker 1 (Slides 1-5): Intro, Objectives, Web of Fields, Continuous Spectroscopy, 3D Data Cube & 2D Curve
    * Speaker 2 (Slides 6-9): India Coverage, Preprocessing Pipeline, Benchmarking, Need for BharatSpectral
    * Speaker 3 (Slide 10): Project Progression (Phases 1-5 Roadmap)
    * Speaker 4 (Slides 11-16): 4 Operational Comics, Minimal References, Final Team & Supervisor Thank You
- Single clean PPTX download button
- Full keyboard, touch, and click navigation via deck.js
"""

import os
import shutil

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
    .corkboard-surface {
      position: relative;
      width: 100%;
      height: calc(100vh - 64px);
      overflow: hidden;
      background-image: url('assets/cork_bg.png');
      background-size: cover;
      background-position: center;
    }
    .slides-wrapper {
      position: relative;
      width: 100%;
      height: 100%;
    }
    .card-img-box {
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: 6px;
      overflow: hidden;
      background: rgba(0,0,0,0.02);
    }
    .card-img-box img {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      border-radius: 4px;
    }
    .grid-2col {
      display: grid;
      grid-template-columns: 1.15fr 1fr;
      gap: 16px;
      flex: 1;
      min-height: 0;
    }
    .grid-2col-equal {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      flex: 1;
      min-height: 0;
    }
    .grid-4col-pinned {
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      gap: 16px;
      flex: 1;
      min-height: 0;
    }
    .card-title {
      font-family: 'Inter', system-ui, sans-serif;
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--accent-cyan);
      margin-bottom: 8px;
    }
    .clean-header-title {
      margin: 0;
      font-size: 1.45rem;
      color: var(--accent-cyan);
      font-family: 'Trebuchet MS', system-ui, sans-serif;
      font-weight: 700;
      letter-spacing: 0.2px;
    }
    .ref-title {
      font-family: 'Inter', system-ui, sans-serif;
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--accent-purple);
      margin-bottom: 2px;
    }
    .ref-authors {
      font-size: 0.82rem;
      color: var(--text);
      line-height: 1.35;
    }
    .ref-venue {
      font-size: 0.78rem;
      color: var(--text-dim);
      font-style: italic;
      margin-bottom: 10px;
    }
    .thank-you-svg-box {
      width: 100%;
      padding: 10px;
      display: flex;
      justify-content: center;
      align-items: center;
    }
  </style>
</head>
<body class="deck-body">

  <div class="deck-container">
    <!-- Top Deck Control Toolbar -->
    <header class="deck-topbar">
      <div class="topbar-left">
        <a href="../" class="btn-ctrl btn-back-hub" title="Return to DSSI Public Ecosystem Portal">
          <span class="icon">⬵</span>
          <span class="label">Main Ecosystem</span>
        </a>
        <div class="deck-brand">
          <span class="deck-badge">RESEARCH PILLAR 1</span>
          <span class="deck-title">BharatSpectral-MAE</span>
        </div>
      </div>

      <div class="topbar-center">
        <span class="slide-title-indicator" id="slideTitleIndicator">Slide 1: Beyond Human Sight</span>
      </div>

      <div class="topbar-right">
        <a href="BharatSpectral_MidTerm_Presentation.pptx" download class="btn-ctrl btn-download btn-animated" title="Download Official PowerPoint Presentation">
          <span class="icon">📥</span>
          <span class="label">Download PPTX</span>
        </a>

        <button class="btn-ctrl btn-dialogue" id="dialogueBtn" title="Toggle Presenter Dialogue & Speech Notes (Key: D or S)">
          <span class="icon">🎙️</span>
          <span class="label">Speech Notes</span>
        </button>
        <span class="slide-counter" id="slideCounter">01 / 16</span>
        <button class="btn-ctrl" id="prevBtn" title="Previous Slide (← / P)">◀ Prev</button>
        <button class="btn-ctrl" id="nextBtn" title="Next Slide (→ / Space / N)">Next ▶</button>
        <button class="btn-ctrl" id="fullscreenBtn" title="Toggle Fullscreen (F)">⛶ Fullscreen</button>
      </div>
      <div class="deck-progress" id="progressBar"></div>
    </header>

    <!-- Slide Dialogue / Presenter Speech Notes Drawer -->
    <aside class="dialogue-drawer" id="dialogueDrawer" aria-label="Presenter Dialogue Drawer">
      <div class="dialogue-header">
        <div class="dialogue-title-box">
          <span class="dialogue-badge">SLIDE <span id="dialogueSlideNum">01</span></span>
          <span class="dialogue-title" id="dialogueTitle">Slide Dialogue</span>
        </div>
        <div class="dialogue-actions">
          <button class="btn-dialogue-act" id="copyDialogueBtn" title="Copy Dialogue to Clipboard">📋 Copy</button>
          <button class="btn-dialogue-act" id="closeDialogueBtn" title="Close Drawer (D / Esc)">✕ Close</button>
        </div>
      </div>
      <div class="dialogue-body" id="dialogueContent">
        <!-- Injected via deck.js -->
      </div>
    </aside>

    <!-- Main Corkboard Stage -->
    <main class="deck-stage">
      <div class="corkboard-frame">
        <div class="corkboard-surface">
          <div class="slides-wrapper">

            <!-- ============================================================== -->
            <!-- SPEAKER 1: SLIDES 1 to 5                                      -->
            <!-- ============================================================== -->

            <!-- SLIDE 1: Beyond Human Sight (Intro) -->
            <section class="slide active" id="slide-1">
              <div class="paper-card style-parchment title-strip-clean">
                <div class="washi-tape tape-center"></div>
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-cyan pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h1 class="title-strip-text">
                  BharatSpectral: Democratized Spectral-Semantic Intelligence
                </h1>
              </div>

              <!-- Organic Corkboard Pinboard with Red Pushpins & Connecting Red Yarn -->
              <div class="pinboard-investigator-grid" style="flex: 1; position: relative;">
                <svg class="yarn-overlay" viewBox="0 0 1200 600">
                  <path d="M 160 25 C 200 120, 300 280, 480 320" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="8,4" opacity="0.75"/>
                  <path d="M 480 320 C 600 200, 750 140, 950 120" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="8,4" opacity="0.75"/>
                  <path d="M 155 25 C 400 320, 650 300, 850 235" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="8,4" opacity="0.75"/>
                  <path d="M 385 230 C 600 60, 850 60, 1060 28" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="8,4" opacity="0.75"/>
                </svg>

                <div class="pinned-polaroid polaroid-1" title="Orbital Hyperspectral Sensor">
                  <div class="pushpin pin-red pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <img src="assets/hero_satellite_earth.png" alt="Hyperspectral Earth Observation Satellite">
                </div>

                <div class="pinned-polaroid polaroid-2" title="Radiative Transfer & Optical Physics">
                  <div class="pushpin pin-red pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <img src="assets/photon_pinball_cube.png" alt="Canopy Optical Scattering & Physics">
                </div>

                <div class="pinned-polaroid polaroid-3" title="Continuous Spectroscopy">
                  <div class="pushpin pin-red pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <img src="assets/continuous_spectroscopy.png" alt="Continuous Hyperspectral Spectroscopy">
                </div>

                <div class="pinned-polaroid polaroid-4" title="Indian Agricultural Mosaic">
                  <div class="pushpin pin-red pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <img src="assets/india_hsi_coverage.png" alt="Indian Hyperspectral Coverage & Agricultural Mosaic">
                </div>

                <div class="pinned-polaroid polaroid-5" title="Spectral Contrast & Diagnostic Barcode">
                  <div class="pushpin pin-red pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <img src="assets/spectrum_contrast.png" alt="Multispectral vs Hyperspectral Contrast">
                </div>
              </div>
            </section>

            <!-- SLIDE 2: Project Objectives -->
            <section class="slide" id="slide-2">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-cyan pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">Project Objectives</h2>
              </div>
              <div class="paper-card style-parchment" style="flex: 1; padding: 24px 36px; display: flex; flex-direction: column; justify-content: space-around; position: relative;">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-yellow pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-green pin-bottom-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-purple pin-bottom-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <ol class="objectives-list" style="font-size: 0.88rem; line-height: 1.55; margin-left: 20px; margin-top: 0; margin-bottom: 0; color: var(--text); padding-left: 8px;">
                  <li style="margin-bottom: 12px;"><strong style="color: var(--accent-cyan);">Data Acquisition &amp; Benchmark Creation:</strong> Ingest heterogeneous hyperspectral cubes across AVIRIS-NG India (425 bands), ISRO HysIS (220 bands), and NASA EMIT (285 bands) to construct <strong>BharatHSI-Bench</strong> — India's first open, labeled smallholder agricultural benchmark with standardized evaluation protocols.</li>
                  <li style="margin-bottom: 12px;"><strong style="color: var(--accent-orange);">Empirical Failure Proof:</strong> Rigorously evaluate global Foundation Models (SpectralGPT, HyperSIGMA) and classical baselines directly on BharatHSI-Bench, quantifying severe domain-shift degradation (22%–37% Overall Accuracy drop) over fragmented Indian plots.</li>
                  <li style="margin-bottom: 12px;"><strong style="color: var(--accent-purple);">Physics-Informed Foundation Model:</strong> Design <strong>BharatSpectral-MAE</strong>, introducing seven named architectural innovations (Scale-Spectral Positional Encoding, Atmospheric Absorption Masking, Reflectance-Normalized Loss) to achieve state-of-the-art representations under Indian agricultural conditions.</li>
                  <li style="margin-bottom: 12px;"><strong style="color: var(--accent-green);">Multi-Domain Biochemical Adaptation:</strong> Fine-tune foundation representations for downstream diagnostic tasks including nitrogen deficit mapping, soil organic carbon estimation, inland water chlorophyll-a monitoring, and soil salinity/sodicity defense.</li>
                  <li style="margin-bottom: 0px;"><strong style="color: var(--accent-red);">Democratized Public Delivery:</strong> Deploy an open, zero-cost WebGIS platform with sub-second Serverless Spectral Inference (SSI) via Cloudflare Workers and ONNX edge runtime, translating complex spectral tensors into direct vernacular farmer advisories.</li>
                </ol>
              </div>
            </section>

            <!-- SLIDE 3: The Web of Fields -->
            <section class="slide" id="slide-3">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-cyan pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">The Web of Fields: Multi-Disciplinary Convergence</h2>
              </div>
              <div class="paper-card style-parchment" style="flex: 1; padding: 12px; display: flex; align-items: center; justify-content: center; position: relative;">
                <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box" style="background: transparent; border: none; padding: 0; margin: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                  <img src="assets/venn_diagram.png" alt="The Web of Fields: 7-Field Interdisciplinary Venn Diagram" style="max-width: 100%; max-height: 520px; object-fit: contain;">
                </div>
              </div>
            </section>

            <!-- SLIDE 4: Continuous Spectroscopy -->
            <section class="slide" id="slide-4">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-green pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-green pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">Continuous Spectroscopy: The Chemical Barcode</h2>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-green pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-img-box">
                    <img src="assets/continuous_spectroscopy.png" alt="Continuous Hyperspectral Spectroscopy">
                  </div>
                </div>
                <div class="paper-card style-kraft">
                  <div class="pushpin pin-yellow pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title">Diagnostic Absorption Physics</div>
                  <ul class="bullet-list">
                    <li><strong>Narrow-Band Continuity:</strong> 425 contiguous 5nm bands capture narrow chemical absorption doublets invisible to 10-band multispectral sensors.</li>
                    <li><strong>Chlorophyll Red-Edge (680–740nm):</strong> Slope inflection accurately isolates plant vigor from background soil reflectance.</li>
                    <li><strong>Cellular Water Absorption (970nm &amp; 1200nm):</strong> Quantifies canopy equivalent water thickness before visual wilting occurs.</li>
                    <li><strong>Protein &amp; Nitrogen (2100–2300nm):</strong> Direct molecular absorption bonds (C-H, N-H) enable precise leaf nitrogen profiling.</li>
                  </ul>
                </div>
              </div>
            </section>

            <!-- SLIDE 5: Hyperspectral Data Cube & 2D Spectral Signature Curve -->
            <section class="slide" id="slide-5">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-purple pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-purple pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">Hyperspectral Data Cube &amp; Canopy Radiative Transfer</h2>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-purple pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-img-box">
                    <img src="assets/photon_pinball_cube.png" alt="Hyperspectral Data Cube & Canopy Radiative Transfer">
                  </div>
                </div>
                <div class="paper-card style-kraft">
                  <div class="pushpin pin-yellow pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title">2D Continuous Spectral Signature Curve</div>
                  <div style="width: 100%; height: 260px; display: flex; align-items: center; justify-content: center; background: #fffdf5; border-radius: 6px; border: 1px solid var(--border); padding: 8px;">
                    <svg viewBox="0 0 460 220" width="100%" height="100%">
                      <defs>
                        <linearGradient id="sigGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                          <stop offset="0%" stop-color="#38bdf8" />
                          <stop offset="25%" stop-color="#34d399" />
                          <stop offset="50%" stop-color="#fbbf24" />
                          <stop offset="100%" stop-color="#f87171" />
                        </linearGradient>
                      </defs>
                      <!-- Axes -->
                      <line x1="40" y1="180" x2="440" y2="180" stroke="#8c7865" stroke-width="1.5" />
                      <line x1="40" y1="20" x2="40" y2="180" stroke="#8c7865" stroke-width="1.5" />
                      <text x="240" y="205" font-family="'JetBrains Mono', monospace" font-size="10" fill="#6d5f52" text-anchor="middle">Wavelength (nm) • 400 to 2500 nm</text>
                      <text x="12" y="105" font-family="'JetBrains Mono', monospace" font-size="10" fill="#6d5f52" text-anchor="middle" transform="rotate(-90 12,105)">Reflectance %</text>
                      
                      <!-- Spectral Signature Curve -->
                      <path d="M 40 160 Q 60 162 75 145 T 105 168 T 130 90 T 170 65 T 220 70 T 260 120 T 300 85 T 350 140 T 400 120 T 440 165" fill="none" stroke="url(#sigGrad)" stroke-width="2.5" />
                      
                      <!-- Annotations -->
                      <circle cx="105" cy="168" r="3.5" fill="#e03131" />
                      <text x="105" y="155" font-family="'Inter', sans-serif" font-size="8.5" font-weight="700" fill="#c92a2a" text-anchor="middle">Chlorophyll 680nm</text>
                      
                      <circle cx="130" cy="90" r="3.5" fill="#2b8a3e" />
                      <text x="145" y="80" font-family="'Inter', sans-serif" font-size="8.5" font-weight="700" fill="#2b8a3e">Red-Edge Rise</text>
                      
                      <circle cx="260" cy="120" r="3.5" fill="#0b7285" />
                      <text x="260" y="140" font-family="'Inter', sans-serif" font-size="8.5" font-weight="700" fill="#0b7285" text-anchor="middle">H₂O Dip 1400nm</text>

                      <circle cx="400" cy="120" r="3.5" fill="#6741d9" />
                      <text x="400" y="105" font-family="'Inter', sans-serif" font-size="8.5" font-weight="700" fill="#6741d9" text-anchor="middle">Nitrogen 2200nm</text>
                    </svg>
                  </div>
                  <ul class="bullet-list" style="margin-top: 10px;">
                    <li><strong>3D Cube Dimension:</strong> Two spatial axes $(X, Y)$ and one dense spectral axis $(\\lambda)$ capture complete radiative physical interactions.</li>
                    <li><strong>Non-Linear Canopy Ricochet:</strong> Sunlight bouncing between multiple crop tiers invalidates standard linear unmixing.</li>
                  </ul>
                </div>
              </div>
            </section>

            <!-- ============================================================== -->
            <!-- SPEAKER 2: SLIDES 6 to 9                                      -->
            <!-- ============================================================== -->

            <!-- SLIDE 6: Indian Landmass Hyperspectral Coverage -->
            <section class="slide" id="slide-6">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-green pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-green pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">Indian Landmass Hyperspectral Coverage</h2>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-green pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-img-box">
                    <img src="assets/india_hsi_coverage.png" alt="Indian Hyperspectral Coverage Map">
                  </div>
                </div>
                <div class="paper-card style-kraft">
                  <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title">Sensor Heterogeneity &amp; Coverage</div>
                  <ul class="bullet-list">
                    <li><strong>AVIRIS-NG India (Airborne):</strong> 425 spectral channels (380–2510nm) at 4–8m GSD across key agro-ecological zones (Punjab, Gujarat, Andhra Pradesh).</li>
                    <li><strong>NASA EMIT (ISS Spaceborne):</strong> 285 spectral channels (381–2493nm) at 60m GSD providing regional mineral and canopy observations.</li>
                    <li><strong>ISRO HysIS (Orbital Satellite):</strong> 220 spectral channels across VNIR/SWIR providing national continuous monitoring.</li>
                    <li><strong>Resolution Harmonization:</strong> Requires specialized handling to bridge Ground Sample Distances from 4m airborne to 60m orbital scales.</li>
                  </ul>
                </div>
              </div>
            </section>

            <!-- SLIDE 7: Automated Preprocessing Pipeline -->
            <section class="slide" id="slide-7">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-cyan pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">Automated Preprocessing Pipeline</h2>
              </div>
              <div class="paper-card style-parchment" style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 12px 16px; position: relative;">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-cyan pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box" style="width: 100%; height: 100%;">
                  <img src="assets/preprocessing_pipeline.png" alt="Preprocessing Pipeline Assembly Line" style="max-height: 520px; object-fit: contain;">
                </div>
              </div>
            </section>

            <!-- SLIDE 8: The Benchmarking Arena -->
            <section class="slide" id="slide-8">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-red pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-red pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">Empirical Baseline Benchmarking &amp; Failure Modes</h2>
              </div>
              <div class="grid-2col">
                <div class="paper-card style-parchment">
                  <div class="pushpin pin-red pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-img-box">
                    <img src="../outputs/figures/domain_shift_collapse.png" alt="Domain Shift Collapse Bar Chart" onerror="this.src='../outputs/figures/domain_shift_collapse.png'">
                  </div>
                </div>
                <div class="paper-card style-kraft">
                  <div class="pushpin pin-yellow pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title" style="color: var(--accent-red);">Empirical Benchmark Results (Testbed Evaluation)</div>
                  <div style="font-size: 0.84rem; line-height: 1.5; color: var(--text);">
                    <p style="margin-bottom: 8px;"><strong>The Indian Pines Fallacy:</strong> Models trained on 40-hectare US monocultures collapse when transferred to fragmented Indian smallholder farms.</p>
                    <ul class="bullet-list">
                      <li><strong>Random Forest (100 Trees):</strong> 85.4% → 57.8% <span style="color: var(--accent-red); font-weight:700;">(-27.6%)</span></li>
                      <li><strong>SVM (RBF Kernel):</strong> 84.6% → 62.2% <span style="color: var(--accent-red); font-weight:700;">(-22.4%)</span></li>
                      <li><strong>3D-CNN (Hamida et al.):</strong> 90.8% → 56.4% <span style="color: var(--accent-red); font-weight:700;">(-34.4%)</span></li>
                      <li><strong>HybridSN (3D-2D CNN):</strong> 92.4% → 55.1% <span style="color: var(--accent-red); font-weight:700;">(-37.3%)</span></li>
                      <li><strong>Spectral Transformer:</strong> 93.5% → 60.8% <span style="color: var(--accent-red); font-weight:700;">(-32.7%)</span></li>
                      <li><strong>SpectralGPT (Hong et al.):</strong> 93.5% → 61.5% <span style="color: var(--accent-red); font-weight:700;">(-32.0%)</span></li>
                      <li><strong>HyperSIGMA (Wang et al.):</strong> 93.8% → 64.2% <span style="color: var(--accent-red); font-weight:700;">(-29.6%)</span></li>
                    </ul>
                    <div style="margin-top: 10px; padding: 6px 12px; background: #fff5f5; border-left: 3px solid var(--accent-red); font-weight: 600; font-size: 0.82rem; color: var(--accent-red);">
                      Consistent 22%–37% Overall Accuracy drop across all Western architectures.
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- SLIDE 9: The Need for BharatSpectral (Loosely Pinned Notes) -->
            <section class="slide" id="slide-9">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-yellow pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-yellow pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">The Need for BharatSpectral</h2>
              </div>
              <div class="grid-4col-pinned">
                <!-- Pinned Note 1: Spatial Fragmentation -->
                <div class="paper-card style-parchment" style="transform: rotate(-0.7deg); position: relative; padding: 16px 20px;">
                  <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title" style="color: var(--accent-cyan); font-size: 1.0rem;">🌾 Sub-Pixel Spatial Fragmentation</div>
                  <ul class="bullet-list" style="font-size: 0.82rem;">
                    <li>Indian farm parcels average 0.5 to 2.0 hectares with multi-crop intercropping.</li>
                    <li>Western models trained on 40-hectare monocultures blur plot boundaries and collapse on mixed pixels.</li>
                    <li>Demands foundation representations explicitly conditioned on mixture entropy.</li>
                  </ul>
                </div>

                <!-- Pinned Note 2: Multi-Sensor Heterogeneity -->
                <div class="paper-card style-kraft" style="transform: rotate(0.8deg); position: relative; padding: 16px 20px;">
                  <div class="pushpin pin-green pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title" style="color: var(--accent-green); font-size: 1.0rem;">🛰️ Multi-Sensor Heterogeneity</div>
                  <ul class="bullet-list" style="font-size: 0.82rem;">
                    <li>Indian EO relies on 425-band AVIRIS-NG, 285-band EMIT, and 220-band HysIS.</li>
                    <li>Ground Sample Distances vary widely from 4m airborne to 60m satellite imagery.</li>
                    <li>Requires a sensor-agnostic physical tokenizer rather than rigid single-sensor networks.</li>
                  </ul>
                </div>

                <!-- Pinned Note 3: Subtle Biochemical Absorption -->
                <div class="paper-card style-kraft" style="transform: rotate(-0.6deg); position: relative; padding: 16px 20px;">
                  <div class="pushpin pin-purple pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title" style="color: var(--accent-purple); font-size: 1.0rem;">🔬 Subtle Biochemical Absorption</div>
                  <ul class="bullet-list" style="font-size: 0.82rem;">
                    <li>Critical diagnostic features (leaf nitrogen at 2.2μm, soil carbon, moisture) exhibit &lt; 5% reflectance.</li>
                    <li>Standard MSE loss functions overlook subtle diagnostic dips in favor of high-reflectance background soil.</li>
                    <li>Requires reflectance-normalized loss formulations to preserve biochemical depth.</li>
                  </ul>
                </div>

                <!-- Pinned Note 4: Democratized Public Accessibility -->
                <div class="paper-card style-parchment" style="transform: rotate(0.6deg); position: relative; padding: 16px 20px;">
                  <div class="pushpin pin-yellow pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title" style="color: var(--accent-orange); font-size: 1.0rem;">🌐 Democratized Edge Accessibility</div>
                  <ul class="bullet-list" style="font-size: 0.82rem;">
                    <li>Hyperspectral analytics are currently locked behind $10,000/seat desktop GIS licenses.</li>
                    <li>Smallholder farmers require zero-cost, sub-second browser inference (SSI).</li>
                    <li>Bridges the gap between research models and direct vernacular advisories.</li>
                  </ul>
                </div>
              </div>
            </section>

            <!-- ============================================================== -->
            <!-- SPEAKER 3: SLIDE 10                                           -->
            <!-- ============================================================== -->

            <!-- SLIDE 10: Master Project Timeline -->
            <section class="slide" id="slide-10">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-cyan pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">Project Progression: Phases 1 to 5</h2>
              </div>
              <div class="paper-card style-parchment" style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 12px 16px; position: relative;">
                <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box" style="width: 100%; height: 100%;">
                  <img src="assets/project_timeline.png" alt="Project Timeline Roadmap" style="max-height: 520px; object-fit: contain;">
                </div>
              </div>
            </section>

            <!-- ============================================================== -->
            <!-- SPEAKER 4: SLIDES 11 to 16                                    -->
            <!-- ============================================================== -->

            <!-- SLIDE 11: Comic 1 - The Invisible Hunger -->
            <section class="slide" id="slide-11">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-green pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-green pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">Operational Scenario 1: The Invisible Hunger</h2>
              </div>
              <div class="paper-card style-parchment" style="flex: 1; display: flex; justify-content: center; align-items: center; padding: 10px;">
                <div class="pushpin pin-green pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box" style="width: 100%; height: 100%;">
                  <img src="assets/comic1_invisible_hunger.png" alt="Comic 1: The Invisible Hunger" style="max-height: 520px; object-fit: contain;">
                </div>
              </div>
            </section>

            <!-- SLIDE 12: Comic 2 - The Canal Lifeline -->
            <section class="slide" id="slide-12">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-cyan pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">Operational Scenario 2: The Canal Lifeline</h2>
              </div>
              <div class="paper-card style-parchment" style="flex: 1; display: flex; justify-content: center; align-items: center; padding: 10px;">
                <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box" style="width: 100%; height: 100%;">
                  <img src="assets/comic2_canal_lifeline.png" alt="Comic 2: The Canal Lifeline" style="max-height: 520px; object-fit: contain;">
                </div>
              </div>
            </section>

            <!-- SLIDE 13: Comic 3 - 14-Day Drought Warning -->
            <section class="slide" id="slide-13">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-amber pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-amber pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">Operational Scenario 3: 14-Day Drought Warning</h2>
              </div>
              <div class="paper-card style-parchment" style="flex: 1; display: flex; justify-content: center; align-items: center; padding: 10px;">
                <div class="pushpin pin-amber pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box" style="width: 100%; height: 100%;">
                  <img src="assets/comic3_drought_warning.png" alt="Comic 3: 14-Day Drought Warning" style="max-height: 520px; object-fit: contain;">
                </div>
              </div>
            </section>

            <!-- SLIDE 14: Comic 4 - Salinity Encroachment -->
            <section class="slide" id="slide-14">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-purple pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-purple pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">Operational Scenario 4: Salinity Encroachment</h2>
              </div>
              <div class="paper-card style-parchment" style="flex: 1; display: flex; justify-content: center; align-items: center; padding: 10px;">
                <div class="pushpin pin-purple pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="card-img-box" style="width: 100%; height: 100%;">
                  <img src="assets/comic4_salinity_defense.png" alt="Comic 4: Salinity Encroachment" style="max-height: 520px; object-fit: contain;">
                </div>
              </div>
            </section>

            <!-- SLIDE 15: Key Literature References -->
            <section class="slide" id="slide-15">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-cyan pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">Key Literature References</h2>
              </div>
              <div class="grid-2col-equal">
                <!-- Reference Card 1 -->
                <div class="paper-card style-parchment" style="padding: 22px 26px;">
                  <div class="pushpin pin-cyan pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title" style="color: var(--accent-cyan); font-size: 1.05rem; margin-bottom: 14px;">
                    Foundational Hyperspectral Transformers
                  </div>

                  <div class="ref-item">
                    <div class="ref-title">• SpectralGPT: Spectral Foundation Model</div>
                    <div class="ref-authors">Hong, D., Zhang, B., Li, X., Chanussot, J., &amp; Zhu, X. X. (2024).</div>
                    <div class="ref-venue">IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), 46(8), 5412–5427.</div>
                  </div>

                  <div class="ref-item">
                    <div class="ref-title">• SS-MAE: Spectral-Spatial Masked Autoencoder</div>
                    <div class="ref-authors">Lin, Y., Gao, L., Zheng, X., &amp; Zhang, B. (2024).</div>
                    <div class="ref-venue">IEEE Transactions on Geoscience and Remote Sensing (TGRS), 62, 1–14.</div>
                  </div>

                  <div class="ref-item">
                    <div class="ref-title">• HyperSIGMA: Scalable Foundation Model for Remote Sensing</div>
                    <div class="ref-authors">Wang, X., Zhang, L., &amp; Chanussot, J. (2024).</div>
                    <div class="ref-venue">IEEE Transactions on Geoscience and Remote Sensing (TGRS), 62, 1–16.</div>
                  </div>
                </div>

                <!-- Reference Card 2 -->
                <div class="paper-card style-kraft" style="padding: 22px 26px;">
                  <div class="pushpin pin-yellow pin-top-center"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title" style="color: var(--accent-orange); font-size: 1.05rem; margin-bottom: 14px;">
                    Scale Invariance &amp; Spectroscopic Unmixing
                  </div>

                  <div class="ref-item">
                    <div class="ref-title">• Scale-MAE: High-Resolution Masked Autoencoders Always Assist</div>
                    <div class="ref-authors">Reed, C. J., Metzger, R., Srinivas, A., Darrell, T., &amp; Keutzer, K. (2023).</div>
                    <div class="ref-venue">IEEE/CVF Conference on Computer Vision and Pattern Recognition (ICCV), 14288–14299.</div>
                  </div>

                  <div class="ref-item">
                    <div class="ref-title">• HybridSN: 3D-2D CNN Feature Hierarchy for HSI</div>
                    <div class="ref-authors">Roy, S. K., Krishna, G., Dubey, S. R., &amp; Chaudhuri, B. B. (2020).</div>
                    <div class="ref-venue">IEEE Geoscience and Remote Sensing Letters (GRSL), 17(8), 1352–1356.</div>
                  </div>

                  <div class="ref-item">
                    <div class="ref-title">• Spectral Unmixing: Algorithms &amp; Physical Principles</div>
                    <div class="ref-authors">Keshava, N., &amp; Mustard, J. F. (2002).</div>
                    <div class="ref-venue">IEEE Signal Processing Magazine, 19(1), 44–57.</div>
                  </div>
                </div>
              </div>
            </section>

            <!-- SLIDE 16: Final Slide (Thank You SVG + Team Members + Supervisor) -->
            <section class="slide" id="slide-16">
              <div class="board-header-note" style="margin-bottom: 12px; padding: 10px 24px; text-align: center;">
                <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-cyan pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <h2 class="clean-header-title">BharatSpectral: Democratized Spectral Intelligence</h2>
              </div>

              <!-- Top Decorative SVG Thank You Banner -->
              <div class="paper-card style-parchment" style="padding: 10px 20px; margin-bottom: 14px; text-align: center; position: relative;">
                <div class="washi-tape tape-center"></div>
                <div class="pushpin pin-green pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                <div class="pushpin pin-purple pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                
                <div class="thank-you-svg-box">
                  <svg viewBox="0 0 860 140" width="100%" height="110" style="display:block; margin: 0 auto;">
                    <defs>
                      <linearGradient id="spectralGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#0b7285" />
                        <stop offset="35%" stop-color="#6741d9" />
                        <stop offset="70%" stop-color="#2b8a3e" />
                        <stop offset="100%" stop-color="#d9480f" />
                      </linearGradient>
                      <filter id="svgGlow" x="-10%" y="-10%" width="120%" height="120%">
                        <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0b7285" flood-opacity="0.25"/>
                      </filter>
                    </defs>
                    <text x="50%" y="68" text-anchor="middle" font-family="'Kalam', cursive, sans-serif" font-size="52" font-weight="700" fill="url(#spectralGrad)" filter="url(#svgGlow)">
                      Thank You!
                    </text>
                    <text x="50%" y="102" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="12.5" font-weight="700" fill="#6d5f52" letter-spacing="2.5">
                      DEMOCRATIZED SPECTRAL-SEMANTIC INTELLIGENCE (DSSI)
                    </text>
                    <path d="M 220,118 Q 430,132 640,118" stroke="url(#spectralGrad)" stroke-width="2.5" fill="none" stroke-linecap="round"/>
                  </svg>
                </div>
              </div>

              <!-- Bottom 2 Columns: Team Members & Supervision -->
              <div class="grid-2col-equal">
                <div class="paper-card style-parchment" style="padding: 18px 24px; position: relative;">
                  <div class="pushpin pin-cyan pin-top-left"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title" style="color: var(--accent-cyan); font-size: 1.05rem; margin-bottom: 8px;">
                    Project Research Team
                  </div>
                  <ul class="bullet-list" style="font-size: 0.86rem; line-height: 1.6;">
                    <li><strong>Priyanshu</strong> — Lead Researcher &amp; System Architect</li>
                    <li><strong>[Team Member 2]</strong> — Machine Learning &amp; Preprocessing Pipeline</li>
                    <li><strong>[Team Member 3]</strong> — Radiative Physics &amp; Empirical Benchmarking</li>
                    <li><strong>[Team Member 4]</strong> — Geospatial Edge WebGIS &amp; Evaluation</li>
                  </ul>
                </div>

                <div class="paper-card style-kraft" style="padding: 18px 24px; position: relative;">
                  <div class="pushpin pin-purple pin-top-right"><div class="pushpin-head"></div><div class="pushpin-shadow"></div></div>
                  <div class="card-title" style="color: var(--accent-purple); font-size: 1.05rem; margin-bottom: 8px;">
                    Project Guidance &amp; Supervision
                  </div>
                  <div style="font-size: 0.86rem; line-height: 1.5; color: var(--text);">
                    <div style="color: var(--text-dim); margin-bottom: 4px;">Under the Esteemed Guidance of:</div>
                    <div style="font-size: 1.12rem; font-weight: 700; color: var(--accent-cyan); margin-bottom: 4px;">
                      Dr. / Prof. [Project Supervisor Name]
                    </div>
                    <div style="color: var(--text); font-weight: 500;">
                      Department of Computer Science &amp; Engineering
                    </div>
                    <div style="margin-top: 10px; font-size: 0.80rem; font-weight: 700; color: var(--accent-green);">
                      Open-Source DSSI Initiative • Built for Indian Earth Observation
                    </div>
                  </div>
                </div>
              </div>
            </section>

          </div><!-- .slides-wrapper -->
        </div><!-- .corkboard-surface -->
      </div><!-- .corkboard-frame -->
    </main>

  </div><!-- .deck-container -->

  <script src="deck.js"></script>
</body>
</html>
"""

def main():
    print("Compiling interactive 16-Slide HTML presentation...")
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content.strip())
    print(f"✓ Saved presentation HTML to: {OUT_PATH}")

    # Mirror to presentation.html
    pres_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presentation.html")
    shutil.copy(OUT_PATH, pres_path)
    print(f"✓ Mirrored to: {pres_path}")

if __name__ == "__main__":
    main()
