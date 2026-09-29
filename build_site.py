#!/usr/bin/env python3
"""
build_site.py - Unified Static Site Generator & Deployment Assembler for BharatSpectral
Assembles the complete DSSI ecosystem for Cloudflare Pages deployment:
- Master Ecosystem Portal Landing Page (index.html)
- Interactive Presentation Deck (presentation.html)
- PowerPoint Mid-Term Defense Deck (BharatSpectral_MidTerm_Presentation.pptx)
- Empirical Benchmark Suite & Evidence Gallery (benchmarks.html)
- Grand Narrative 7-Chapter Curriculum & Publication PDFs (narratives.html & narratives/pdfs/)
- Technical Phase Reports (phase1.html, phase2.html, phase3.html, phase4&5.html)
- Operational Guides (workflow-handbook.html, references_pinboard.html)
- Research Documentation Readers (docs/project_synopsis.html, docs/midterm_defense.html, etc.)
- Model Checkpoints, Tables, and High-Res Figures
"""

import os
import sys
import shutil
import json
import subprocess
import markdown

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(REPO_ROOT, "dist")

NAVBAR_HTML = """
<header id="bharat-portal-bar">
  <div class="portal-inner">
    <a href="/index.html" class="portal-brand">
      <span class="portal-badge-logo">🛰️</span>
      <div class="portal-brand-text">
        <span class="portal-name">BharatSpectral</span>
        <span class="portal-tag">DSSI Ecosystem</span>
      </div>
    </a>
    <nav class="portal-links">
      <a href="/index.html" class="p-link" id="nav-home">🏠 Home Portal</a>
      <a href="/presentation.html" class="p-link" id="nav-slides">📽️ Slide Deck</a>
      <a href="/benchmarks.html" class="p-link" id="nav-benchmarks">📊 Benchmarks</a>
      <a href="/phase1.html" class="p-link" id="nav-phase1">Phase 1</a>
      <a href="/phase2.html" class="p-link" id="nav-phase2">Phase 2</a>
      <a href="/phase3.html" class="p-link" id="nav-phase3">Phase 3</a>
      <a href="/phase4&5.html" class="p-link" id="nav-phase45">Phase 4&amp;5</a>
      <a href="/narratives.html" class="p-link" id="nav-narratives">📚 Grand Narrative</a>
      <a href="/references_pinboard.html" class="p-link" id="nav-pinboard">📌 Pinboard</a>
      <a href="/workflow-handbook.html" class="p-link" id="nav-handbook">🛠️ Handbook</a>
      <a href="/BharatSpectral_MidTerm_Presentation.pptx" download class="p-link p-btn">📥 PPTX Deck</a>
    </nav>
  </div>
</header>
<style>
  #bharat-portal-bar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 52px;
    background: rgba(11, 15, 25, 0.95);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-bottom: 1px solid #1e293b;
    z-index: 99999;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }
  .portal-inner {
    max-width: 1600px;
    margin: 0 auto;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    gap: 12px;
  }
  .portal-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    flex-shrink: 0;
  }
  .portal-badge-logo {
    font-size: 1.35rem;
    filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.4));
  }
  .portal-brand-text {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .portal-name {
    font-weight: 800;
    font-size: 1.05rem;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .portal-tag {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 2px 7px;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.3);
    color: #38bdf8;
    border-radius: 9999px;
  }
  .portal-links {
    display: flex;
    align-items: center;
    gap: 4px;
    overflow-x: auto;
    white-space: nowrap;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  .portal-links::-webkit-scrollbar {
    display: none;
  }
  .p-link {
    color: #94a3b8;
    text-decoration: none;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 6px 10px;
    border-radius: 6px;
    transition: all 0.15s ease;
  }
  .p-link:hover {
    color: #f8fafc;
    background: rgba(255, 255, 255, 0.08);
  }
  .p-link.active {
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.15);
    border: 1px solid rgba(56, 189, 248, 0.35);
  }
  .p-btn {
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
    color: #ffffff !important;
    border: 1px solid #38bdf8;
    padding: 6px 12px;
    margin-left: 6px;
    box-shadow: 0 2px 8px rgba(2, 132, 199, 0.3);
  }
  .p-btn:hover {
    background: #0284c7 !important;
    box-shadow: 0 0 14px rgba(56, 189, 248, 0.5);
  }
  @media (max-width: 900px) {
    .portal-tag { display: none; }
    .p-link { font-size: 0.75rem; padding: 5px 8px; }
  }
</style>
"""

READER_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} • BharatSpectral DSSI</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #0b0f19;
      --bg-card: #151d2e;
      --border: #1e293b;
      --cyan: #38bdf8;
      --teal: #14b8a6;
      --text: #e2e8f0;
      --text-muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg-dark);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      line-height: 1.7;
      padding-top: 72px;
      padding-bottom: 60px;
    }}
    .reader-container {{
      max-width: 960px;
      margin: 0 auto;
      padding: 0 24px;
    }}
    .back-nav {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--cyan);
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 24px;
    }}
    .back-nav:hover {{ text-decoration: underline; }}
    .content-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 44px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }}
    h1, h2, h3, h4 {{
      color: #ffffff;
      margin-top: 1.8em;
      margin-bottom: 0.6em;
      letter-spacing: -0.02em;
    }}
    h1 {{ font-size: 2.2rem; margin-top: 0; border-bottom: 1px solid var(--border); padding-bottom: 16px; }}
    h2 {{ font-size: 1.5rem; color: var(--cyan); }}
    h3 {{ font-size: 1.2rem; }}
    p {{ margin-bottom: 1.2em; }}
    ul, ol {{ margin-left: 24px; margin-bottom: 1.4em; }}
    li {{ margin-bottom: 6px; }}
    pre {{
      background: #090d16;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      overflow-x: auto;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.88rem;
      margin-bottom: 1.4em;
    }}
    code {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.88rem;
      background: rgba(56, 189, 248, 0.1);
      color: var(--cyan);
      padding: 2px 6px;
      border-radius: 4px;
    }}
    pre code {{
      background: transparent;
      padding: 0;
      color: #e2e8f0;
    }}
    blockquote {{
      border-left: 4px solid var(--cyan);
      padding-left: 18px;
      color: var(--text-muted);
      margin: 1.4em 0;
      font-style: italic;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.4em 0;
      font-size: 0.9rem;
    }}
    th, td {{
      padding: 10px 14px;
      border: 1px solid var(--border);
      text-align: left;
    }}
    th {{
      background: #0f172a;
      color: var(--cyan);
      font-weight: 700;
    }}
    tr:nth-child(even) {{ background: rgba(255, 255, 255, 0.02); }}
    hr {{
      border: none;
      border-top: 1px solid var(--border);
      margin: 2em 0;
    }}
    .pdf-download-bar {{
      margin-bottom: 24px;
      background: rgba(56, 189, 248, 0.08);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 10px;
      padding: 14px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
  </style>
</head>
<body>
{navbar}
<div class="reader-container">
  <a href="{back_url}" class="back-nav">← Back to {back_label}</a>
  {download_bar}
  <div class="content-card">
    {content}
  </div>
</div>
</body>
</html>
"""

def generate_index_portal_html():
    """Generates the Master Public Portal Landing Page for index.html."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BharatSpectral • Master Public Research & Infrastructure Portal</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #0b0f19;
      --bg-card: #151d2e;
      --bg-card-hover: #1e293b;
      --border: #233148;
      --cyan: #38bdf8;
      --teal: #14b8a6;
      --amber: #f59e0b;
      --purple: #a855f7;
      --red: #ef4444;
      --text: #e2e8f0;
      --text-muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg-dark);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      padding-top: 72px;
      padding-bottom: 80px;
    }}
    .container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 0 24px;
    }}
    .hero {{
      text-align: center;
      margin-bottom: 44px;
    }}
    .hero-badge {{
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 4px 14px;
      border-radius: 9999px;
      background: rgba(56, 189, 248, 0.12);
      color: var(--cyan);
      border: 1px solid var(--cyan);
      margin-bottom: 14px;
    }}
    h1 {{
      font-size: 2.8rem;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.03em;
      margin-bottom: 14px;
      line-height: 1.2;
    }}
    .hero-subtitle {{
      color: var(--text-muted);
      font-size: 1.15rem;
      max-width: 960px;
      margin: 0 auto 32px;
      line-height: 1.6;
    }}
    .main-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
      margin-bottom: 48px;
    }}
    .action-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
    }}
    .action-card:hover {{
      transform: translateY(-4px);
      border-color: var(--cyan);
      box-shadow: 0 16px 36px rgba(56, 189, 248, 0.12);
    }}
    .action-icon {{
      font-size: 2.2rem;
      margin-bottom: 14px;
    }}
    .action-title {{
      font-size: 1.3rem;
      font-weight: 800;
      color: #fff;
      margin-bottom: 8px;
    }}
    .action-desc {{
      font-size: 0.88rem;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 24px;
      flex: 1;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 10px 18px;
      border-radius: 8px;
      font-size: 0.88rem;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s;
    }}
    .btn-cyan {{
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      color: #ffffff;
      border: 1px solid #38bdf8;
    }}
    .btn-cyan:hover {{
      background: #0284c7;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.4);
    }}
    .btn-outline {{
      border: 1px solid var(--border);
      color: var(--text);
      background: rgba(255, 255, 255, 0.04);
    }}
    .btn-outline:hover {{
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
      border-color: var(--cyan);
    }}
    .section-head {{
      font-size: 1.6rem;
      font-weight: 800;
      color: #fff;
      margin: 40px 0 16px;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .card-box {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 24px;
    }}
    .fig-row {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      margin-top: 16px;
    }}
    .fig-item {{
      background: #090d16;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }}
    .fig-item img {{
      width: 100%;
      height: 140px;
      object-fit: cover;
      border-radius: 6px;
      margin-bottom: 8px;
    }}
    .fig-item-title {{
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--cyan);
      margin-bottom: 4px;
    }}
    .fig-item-desc {{
      font-size: 0.75rem;
      color: var(--text-muted);
    }}
    .dl-row {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 14px;
    }}
  </style>
</head>
<body>
{NAVBAR_HTML}
<div class="container">
  <div class="hero">
    <span class="hero-badge">B.Tech Capstone Project • Phase 1 &amp; 2 Delivery</span>
    <h1>BharatSpectral Ecosystem Portal</h1>
    <p class="hero-subtitle">Democratized Spectral-Semantic Intelligence (DSSI) for Indian Earth Observation. Synthesizing physics-informed hyperspectral foundation modeling with serverless WebGIS public digital infrastructure.</p>
  </div>

  <!-- Main Portal Action Cards -->
  <div class="main-grid">
    <div class="action-card" style="border-top: 4px solid var(--cyan);">
      <div>
        <div class="action-icon">📽️</div>
        <div class="action-title">Mid-Term Slide Deck</div>
        <div class="action-desc">Interactive 16-slide presentation with live speaker talking points, presenter notes, keyboard navigation, and embedded empirical proof figures.</div>
      </div>
      <a href="/presentation.html" class="btn btn-cyan">Launch Presentation Deck →</a>
    </div>

    <div class="action-card" style="border-top: 4px solid var(--teal);">
      <div>
        <div class="action-icon">📊</div>
        <div class="action-title">Empirical Benchmarks</div>
        <div class="action-desc">Hard quantitative proof from Raspberry Pi 5 benchmark testbed: 5 AI architectures + 2 physical GIS baselines evaluated on Indian agricultural scenes.</div>
      </div>
      <a href="/benchmarks.html" class="btn btn-cyan">Explore Benchmark Dashboard →</a>
    </div>

    <div class="action-card" style="border-top: 4px solid var(--purple);">
      <div>
        <div class="action-icon">📚</div>
        <div class="action-title">Grand Narrative &amp; PDFs</div>
        <div class="action-desc">7-chapter publication-grade curriculum bridging quantum spectroscopy, foundation model architectures, and citizen WebGIS infrastructure.</div>
      </div>
      <a href="/narratives.html" class="btn btn-cyan">Read 7 Chapters &amp; PDFs →</a>
    </div>

    <div class="action-card" style="border-top: 4px solid var(--amber);">
      <div>
        <div class="action-icon">📥</div>
        <div class="action-title">PowerPoint File (.pptx)</div>
        <div class="action-desc">Downloadable widescreen PowerPoint presentation deck compiled via <code>python-pptx</code> ready for formal defense and academic review.</div>
      </div>
      <a href="/BharatSpectral_MidTerm_Presentation.pptx" download class="btn btn-outline">Download PPTX Deck 📥</a>
    </div>
  </div>

  <!-- Empirical Evidence Showcase -->
  <h2 class="section-head">🔬 Empirical Proofs &amp; Evidence Gallery</h2>
  <div class="card-box">
    <p style="color: var(--text-muted); margin-bottom: 12px; font-size: 0.95rem;">
      Quantitative validation confirming that Western-pretrained models drop 22%–37% in Overall Accuracy when transferred to fragmented Indian smallholder parcels, while traditional GIS spectroscopic tools (SAM, LSU) fail on non-linear canopy scattering.
    </p>
    <div class="fig-row">
      <div class="fig-item">
        <a href="/outputs/figures/domain_shift_collapse.png" target="_blank">
          <img src="/outputs/figures/domain_shift_collapse.png" alt="Domain Shift Collapse">
        </a>
        <div class="fig-item-title">Domain Shift Collapse</div>
        <div class="fig-item-desc">22%–37% OA performance drop on Indian scenes.</div>
      </div>

      <div class="fig-item">
        <a href="/outputs/figures/spatial_patch_fragmentation.png" target="_blank">
          <img src="/outputs/figures/spatial_patch_fragmentation.png" alt="Spatial Patch Fragmentation">
        </a>
        <div class="fig-item-title">Spatial Fragmentation</div>
        <div class="fig-item-desc">Sub-pixel parcel boundary mixing at 30-60m GSD.</div>
      </div>

      <div class="fig-item">
        <a href="/outputs/figures/gis_linear_unmixing_residuals.png" target="_blank">
          <img src="/outputs/figures/gis_linear_unmixing_residuals.png" alt="GIS LSU Residuals">
        </a>
        <div class="fig-item-title">GIS LSU Residual Error</div>
        <div class="fig-item-desc">54.2% pixels fail linear unmixing threshold.</div>
      </div>

      <div class="fig-item">
        <a href="/outputs/figures/sam_magnitude_confusion.png" target="_blank">
          <img src="/outputs/figures/sam_magnitude_confusion.png" alt="SAM Magnitude Confusion">
        </a>
        <div class="fig-item-title">SAM Magnitude Blindness</div>
        <div class="fig-item-desc">36.4% false matches due to angle scaling invariance.</div>
      </div>
    </div>
  </div>

  <!-- Technical Phase Reports Grid -->
  <h2 class="section-head">📑 Capstone Engineering Phase Reports</h2>
  <div class="main-grid">
    <div class="action-card">
      <div>
        <div class="action-title">Phase 1: Ingestion &amp; Preprocessing</div>
        <div class="action-desc">Ingesting AVIRIS-NG India (425b), NASA EMIT (285b), ISRO HysIS (220b), bad band removal, and smallholder patch sampling.</div>
      </div>
      <a href="/phase1.html" class="btn btn-outline">Read Phase 1 Report →</a>
    </div>

    <div class="action-card">
      <div>
        <div class="action-title">Phase 2: Baselines &amp; GIS Analysis</div>
        <div class="action-desc">Evaluating RF, SVM, HybridSN, 3D-CNN, Spectral Transformer, and physical spectroscopy (SAM, LSU/FCLS).</div>
      </div>
      <a href="/phase2.html" class="btn btn-outline">Read Phase 2 Report →</a>
    </div>

    <div class="action-card">
      <div>
        <div class="action-title">Phase 3: BharatSpectral-MAE</div>
        <div class="action-desc">Physics-informed Foundation Model architecture: SSPE, RNRL, SHT, AAM, ECSA, Ph-LoRA, and FASU unmixing head.</div>
      </div>
      <a href="/phase3.html" class="btn btn-outline">Read Phase 3 Report →</a>
    </div>

    <div class="action-card">
      <div>
        <div class="action-title">Phase 4 &amp; 5: WebGIS &amp; Benchmark</div>
        <div class="action-desc">Cloudflare R2 zero-egress storage, Workers SSI engine, MapLibre GL frontend, and BharatHSI-Bench national suite.</div>
      </div>
      <a href="/phase4&5.html" class="btn btn-outline">Read Phase 4 &amp; 5 Report →</a>
    </div>
  </div>

  <!-- Operational & Academic Guides -->
  <h2 class="section-head">📌 Operational Guides &amp; Master Docs</h2>
  <div class="dl-row">
    <a href="/references_pinboard.html" class="btn btn-outline">📌 Visual References Pinboard</a>
    <a href="/workflow-handbook.html" class="btn btn-outline">🛠️ Workflow Handbook</a>
    <a href="/docs/MASTER_PLAN.html" class="btn btn-outline">📜 Master Execution Plan</a>
    <a href="/docs/midterm_defense_grounding_and_gis_analysis.html" class="btn btn-outline">🔬 Mid-Term Defense Grounding</a>
    <a href="/docs/project_synopsis.html" class="btn btn-outline">📄 Capstone Synopsis</a>
  </div>
</div>
</body>
</html>
"""
    return html

def generate_benchmarks_html():
    """Generates the interactive benchmarks.html page."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Empirical Benchmarks & GIS Baseline Suite • BharatSpectral</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #0b0f19;
      --bg-card: #151d2e;
      --bg-card-hover: #1e293b;
      --border: #233148;
      --cyan: #38bdf8;
      --teal: #14b8a6;
      --amber: #f59e0b;
      --purple: #a855f7;
      --red: #ef4444;
      --text: #e2e8f0;
      --text-muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg-dark);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      padding-top: 72px;
      padding-bottom: 80px;
    }}
    .container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 0 24px;
    }}
    .hero {{
      text-align: center;
      margin-bottom: 40px;
    }}
    .tag {{
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 4px 14px;
      border-radius: 9999px;
      background: rgba(56, 189, 248, 0.12);
      color: var(--cyan);
      border: 1px solid var(--cyan);
      margin-bottom: 12px;
    }}
    h1 {{
      font-size: 2.6rem;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.02em;
      margin-bottom: 10px;
    }}
    .subtitle {{
      color: var(--text-muted);
      font-size: 1.1rem;
      max-width: 900px;
      margin: 0 auto;
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-bottom: 36px;
    }}
    .kpi-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
    }}
    .kpi-val {{
      font-size: 2rem;
      font-weight: 800;
      letter-spacing: -0.03em;
    }}
    .kpi-title {{
      font-size: 0.82rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}
    .kpi-desc {{
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-top: 6px;
    }}
    .section-title {{
      font-size: 1.6rem;
      font-weight: 800;
      color: #fff;
      margin: 40px 0 16px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 24px;
    }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
    }}
    table.data-table th {{
      background: #0f172a;
      color: var(--cyan);
      font-weight: 700;
      padding: 12px 16px;
      text-align: left;
      border: 1px solid var(--border);
    }}
    table.data-table td {{
      padding: 12px 16px;
      border: 1px solid var(--border);
      color: #f1f5f9;
    }}
    table.data-table tr:hover {{
      background: rgba(56, 189, 248, 0.04);
    }}
    .figure-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
      gap: 24px;
    }}
    @media (max-width: 768px) {{
      .figure-grid {{ grid-template-columns: 1fr; }}
    }}
    .fig-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}
    .fig-img-box {{
      background: #060911;
      padding: 12px;
      text-align: center;
      border-bottom: 1px solid var(--border);
    }}
    .fig-img {{
      width: 100%;
      height: 380px;
      object-fit: contain;
      border-radius: 8px;
    }}
    .fig-body {{
      padding: 20px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }}
    .fig-title {{
      font-size: 1.15rem;
      font-weight: 800;
      color: #fff;
      margin-bottom: 8px;
    }}
    .fig-text {{
      font-size: 0.85rem;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 14px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 0.82rem;
      font-weight: 700;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-cyan {{
      background: var(--cyan);
      color: #0b0f19;
    }}
    .btn-cyan:hover {{
      background: #7dd3fc;
    }}
    .btn-outline {{
      border: 1px solid var(--border);
      color: var(--text);
      background: rgba(255, 255, 255, 0.04);
    }}
    .btn-outline:hover {{
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
    }}
    .dl-row {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 14px;
    }}
  </style>
</head>
<body>
{NAVBAR_HTML}
<div class="container">
  <div class="hero">
    <span class="tag">Phase 1 &amp; Phase 2 Milestone Delivery</span>
    <h1>BharatSpectral Empirical Benchmark &amp; GIS Baseline Suite</h1>
    <p class="subtitle">Quantitative validation of Western HSI model collapse on Indian smallholder landscapes and failure modes of traditional physical GIS spectroscopic tools.</p>
  </div>

  <!-- KPI Cards -->
  <div class="kpi-grid">
    <div class="kpi-card" style="border-top: 4px solid var(--red);">
      <div class="kpi-title">Average Domain Shift Drop</div>
      <div class="kpi-val" style="color: var(--red);">-31.3% OA</div>
      <div class="kpi-desc">Across all 5 architectures when evaluating Western source pretraining on real Indian parcels.</div>
    </div>
    <div class="kpi-card" style="border-top: 4px solid var(--amber);">
      <div class="kpi-title">HybridSN 3D-2D CNN Drop</div>
      <div class="kpi-val" style="color: var(--amber);">-37.3%</div>
      <div class="kpi-desc">92.4% Source OA collapses to 55.1% Target OA due to spatial fragmentation.</div>
    </div>
    <div class="kpi-card" style="border-top: 4px solid var(--purple);">
      <div class="kpi-title">Spectral Transformer Drop</div>
      <div class="kpi-val" style="color: var(--purple);">-32.7%</div>
      <div class="kpi-desc">93.5% Source OA drops to 60.8% Target OA without Indian phenological priors.</div>
    </div>
    <div class="kpi-card" style="border-top: 4px solid var(--cyan);">
      <div class="kpi-title">GIS SAM Magnitude Blindness</div>
      <div class="kpi-val" style="color: var(--cyan);">36.4% Error</div>
      <div class="kpi-desc">SAM vector angle invariance produces false matches across illumination &amp; shadows.</div>
    </div>
    <div class="kpi-card" style="border-top: 4px solid var(--teal);">
      <div class="kpi-title">GIS LSU High Residuals</div>
      <div class="kpi-val" style="color: var(--teal);">54.2% Pixels</div>
      <div class="kpi-desc">Boundary RMSE reaches 0.2775 due to multi-canopy non-linear scattering.</div>
    </div>
  </div>

  <!-- Benchmark Table -->
  <h2 class="section-title">📊 Cross-Domain Model Comparison Table</h2>
  <div class="card">
    <table class="data-table">
      <thead>
        <tr>
          <th>Model Architecture</th>
          <th>Domain Setup</th>
          <th>Overall Accuracy (OA)</th>
          <th>Average Accuracy (AA)</th>
          <th>Cohen's Kappa (κ)</th>
          <th>Abundance RMSE</th>
          <th>OA Degradation</th>
          <th>Edge Latency (Pi 5)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Random Forest (100 Trees)</strong></td>
          <td>Source (Indian Pines 1992)</td>
          <td>85.4%</td>
          <td>80.28%</td>
          <td>0.832</td>
          <td>N/A</td>
          <td>—</td>
          <td>0.23 ms</td>
        </tr>
        <tr style="background: rgba(239, 68, 68, 0.05);">
          <td>Random Forest (100 Trees)</td>
          <td>Target Indian Zero-Shot</td>
          <td>57.8%</td>
          <td>53.18%</td>
          <td>0.521</td>
          <td>N/A</td>
          <td style="color: var(--red); font-weight: 700;">-27.6% (-32.3% rel)</td>
          <td>0.07 ms</td>
        </tr>
        <tr>
          <td><strong>SVM (RBF Kernel)</strong></td>
          <td>Source (Indian Pines 1992)</td>
          <td>84.6%</td>
          <td>81.37%</td>
          <td>0.825</td>
          <td>N/A</td>
          <td>—</td>
          <td>0.45 ms</td>
        </tr>
        <tr style="background: rgba(239, 68, 68, 0.05);">
          <td>SVM (RBF Kernel)</td>
          <td>Target Indian Zero-Shot</td>
          <td>62.2%</td>
          <td>41.29%</td>
          <td>0.516</td>
          <td>N/A</td>
          <td style="color: var(--red); font-weight: 700;">-22.4% (-26.5% rel)</td>
          <td>0.42 ms</td>
        </tr>
        <tr>
          <td><strong>HybridSN (Roy et al. 2020)</strong></td>
          <td>Source (Indian Pines 1992)</td>
          <td>92.4%</td>
          <td>86.86%</td>
          <td>0.912</td>
          <td>N/A</td>
          <td>—</td>
          <td>4.98 ms</td>
        </tr>
        <tr style="background: rgba(239, 68, 68, 0.08);">
          <td>HybridSN (Roy et al. 2020)</td>
          <td>Target Indian Zero-Shot</td>
          <td>55.1%</td>
          <td>50.69%</td>
          <td>0.495</td>
          <td>N/A</td>
          <td style="color: var(--red); font-weight: 800;">-37.3% (-40.4% rel)</td>
          <td>4.95 ms</td>
        </tr>
        <tr>
          <td><strong>3D-CNN (Hamida et al.)</strong></td>
          <td>Source (Indian Pines 1992)</td>
          <td>90.8%</td>
          <td>85.35%</td>
          <td>0.895</td>
          <td>N/A</td>
          <td>—</td>
          <td>15.78 ms</td>
        </tr>
        <tr style="background: rgba(239, 68, 68, 0.08);">
          <td>3D-CNN (Hamida et al.)</td>
          <td>Target Indian Zero-Shot</td>
          <td>56.4%</td>
          <td>51.89%</td>
          <td>0.510</td>
          <td>N/A</td>
          <td style="color: var(--red); font-weight: 800;">-34.4% (-37.9% rel)</td>
          <td>15.77 ms</td>
        </tr>
        <tr>
          <td><strong>Spectral Transformer (Baseline)</strong></td>
          <td>Source (Indian Pines 1992)</td>
          <td>93.5%</td>
          <td>87.89%</td>
          <td>0.924</td>
          <td>N/A</td>
          <td>—</td>
          <td>1.06 ms</td>
        </tr>
        <tr style="background: rgba(239, 68, 68, 0.08);">
          <td>Spectral Transformer (Baseline)</td>
          <td>Target Indian Zero-Shot</td>
          <td>60.8%</td>
          <td>55.94%</td>
          <td>0.562</td>
          <td>N/A</td>
          <td style="color: var(--red); font-weight: 800;">-32.7% (-35.0% rel)</td>
          <td>1.10 ms</td>
        </tr>
        <tr style="background: rgba(103, 65, 217, 0.04);">
          <td><strong>SpectralGPT (Hong et al., TPAMI 2024)</strong></td>
          <td>Source (Indian Pines 1992)</td>
          <td>93.5%</td>
          <td>88.10%</td>
          <td>0.925</td>
          <td>N/A</td>
          <td>—</td>
          <td>1.45 ms</td>
        </tr>
        <tr style="background: rgba(239, 68, 68, 0.08);">
          <td>SpectralGPT (Hong et al., TPAMI 2024)</td>
          <td>Target Indian Zero-Shot</td>
          <td>61.5%</td>
          <td>56.20%</td>
          <td>0.550</td>
          <td>0.1500</td>
          <td style="color: var(--red); font-weight: 800;">-32.0% (-34.2% rel)</td>
          <td>1.48 ms</td>
        </tr>
        <tr style="background: rgba(103, 65, 217, 0.04);">
          <td><strong>SS-MAE (Lin et al., TGRS 2024)</strong></td>
          <td>Source (Indian Pines 1992)</td>
          <td>93.5%</td>
          <td>88.40%</td>
          <td>0.926</td>
          <td>N/A</td>
          <td>—</td>
          <td>1.32 ms</td>
        </tr>
        <tr style="background: rgba(239, 68, 68, 0.08);">
          <td>SS-MAE (Lin et al., TGRS 2024)</td>
          <td>Target Indian Zero-Shot</td>
          <td>63.8%</td>
          <td>58.10%</td>
          <td>0.570</td>
          <td>0.1400</td>
          <td style="color: var(--red); font-weight: 800;">-29.7% (-31.8% rel)</td>
          <td>1.35 ms</td>
        </tr>
        <tr style="background: rgba(103, 65, 217, 0.04);">
          <td><strong>HyperSIGMA (Wang et al., 2024)</strong></td>
          <td>Source (Indian Pines 1992)</td>
          <td>93.8%</td>
          <td>88.70%</td>
          <td>0.929</td>
          <td>N/A</td>
          <td>—</td>
          <td>1.78 ms</td>
        </tr>
        <tr style="background: rgba(239, 68, 68, 0.08);">
          <td>HyperSIGMA (Wang et al., 2024)</td>
          <td>Target Indian Zero-Shot</td>
          <td>64.2%</td>
          <td>58.90%</td>
          <td>0.580</td>
          <td>0.1300</td>
          <td style="color: var(--red); font-weight: 800;">-29.6% (-31.6% rel)</td>
          <td>1.82 ms</td>
        </tr>
        <tr style="background: rgba(56, 189, 248, 0.08);">
          <td><strong>GIS SAM Physical Baseline</strong></td>
          <td>Target Indian Physical</td>
          <td>68.5%</td>
          <td>61.20%</td>
          <td>0.634</td>
          <td>N/A</td>
          <td style="color: var(--amber);">36.4% Magnitude Invariance Error</td>
          <td>0.20 ms</td>
        </tr>
        <tr style="background: rgba(20, 184, 166, 0.08);">
          <td><strong>GIS LSU / FCLS Unmixing</strong></td>
          <td>Target Indian Physical</td>
          <td>N/A</td>
          <td>N/A</td>
          <td>N/A</td>
          <td style="color: var(--teal); font-weight: 700;">0.1441 (0.278 Bound.)</td>
          <td style="color: var(--amber);">54.2% Exceed Residual Ceiling</td>
          <td>1.10 ms</td>
        </tr>
      </tbody>
    </table>
    <div class="dl-row">
      <a href="/outputs/tables/benchmark_results.csv" download class="btn btn-cyan">📥 Download benchmark_results.csv</a>
      <a href="/outputs/tables/gis_vs_ai_summary.json" download class="btn btn-outline">📥 Download gis_vs_ai_summary.json</a>
      <a href="/outputs/tables/cross_scene_evaluation.json" download class="btn btn-outline">📥 Download cross_scene_evaluation.json</a>
      <a href="/outputs/tables/gis_spectroscopy_metrics.json" download class="btn btn-outline">📥 Download gis_spectroscopy_metrics.json</a>
    </div>
  </div>

  <!-- High-Res Figures Showcase -->
  <h2 class="section-title">🔬 High-Resolution Empirical Evidence Gallery</h2>
  <div class="figure-grid">
    <!-- Figure 1 -->
    <div class="fig-card">
      <div class="fig-img-box">
        <a href="/outputs/figures/domain_shift_collapse.png" target="_blank">
          <img src="/outputs/figures/domain_shift_collapse.png" class="fig-img" alt="Domain Shift Collapse">
        </a>
      </div>
      <div class="fig-body">
        <div class="fig-title">Figure 1: Domain Shift Performance Collapse</div>
        <div class="fig-text">
          Direct quantitative proof that Western-trained architectures (HybridSN, 3D-CNN, Spectral Transformer) experience catastrophic degradation (-22% to -37% OA) when applied to Indian agricultural scenes without domain-specific physical conditioning.
        </div>
        <a href="/outputs/figures/domain_shift_collapse.png" target="_blank" class="btn btn-outline">🔍 View High-Res PNG (300 DPI)</a>
      </div>
    </div>

    <!-- Figure 2 -->
    <div class="fig-card">
      <div class="fig-img-box">
        <a href="/outputs/figures/spatial_patch_fragmentation.png" target="_blank">
          <img src="/outputs/figures/spatial_patch_fragmentation.png" class="fig-img" alt="Spatial Patch Fragmentation">
        </a>
      </div>
      <div class="fig-body">
        <div class="fig-title">Figure 2: Smallholder Spatial Patch Fragmentation</div>
        <div class="fig-text">
          Indian agricultural plots average 1.08 ha with millions below 0.5 ha. At 30m–60m spaceborne pixel resolution (ISRO HysIS, NASA EMIT), virtually every pixel is a mixed parcel boundary, causing standard monoculture CNNs to fail.
        </div>
        <a href="/outputs/figures/spatial_patch_fragmentation.png" target="_blank" class="btn btn-outline">🔍 View High-Res PNG (300 DPI)</a>
      </div>
    </div>

    <!-- Figure 3 -->
    <div class="fig-card">
      <div class="fig-img-box">
        <a href="/outputs/figures/gis_linear_unmixing_residuals.png" target="_blank">
          <img src="/outputs/figures/gis_linear_unmixing_residuals.png" class="fig-img" alt="GIS Linear Unmixing Residuals">
        </a>
      </div>
      <div class="fig-body">
        <div class="fig-title">Figure 3: GIS Linear Spectral Unmixing (LSU) Residuals</div>
        <div class="fig-text">
          Traditional GIS spectroscopic tools like LSU/FCLS assume linear photon scattering. On multi-layer Indian intercropped canopies, 54.19% of pixels fail with severe unmixing residuals ($RMSE_A$ reaching 0.2775 on boundaries).
        </div>
        <a href="/outputs/figures/gis_linear_unmixing_residuals.png" target="_blank" class="btn btn-outline">🔍 View High-Res PNG (300 DPI)</a>
      </div>
    </div>

    <!-- Figure 4 -->
    <div class="fig-card">
      <div class="fig-img-box">
        <a href="/outputs/figures/sam_magnitude_confusion.png" target="_blank">
          <img src="/outputs/figures/sam_magnitude_confusion.png" class="fig-img" alt="SAM Magnitude Confusion">
        </a>
      </div>
      <div class="fig-body">
        <div class="fig-title">Figure 4: SAM Magnitude Invariance Blindness</div>
        <div class="fig-text">
          Spectral Angle Mapper (SAM) computes vector cosine angles, making it mathematically blind to absolute reflectance magnitude. It produces a 36.4% false match rate, misclassifying shadowed and water-stressed canopies as healthy crops.
        </div>
        <a href="/outputs/figures/sam_magnitude_confusion.png" target="_blank" class="btn btn-outline">🔍 View High-Res PNG (300 DPI)</a>
      </div>
    </div>
  </div>

  <!-- Checkpoint Weights Registry -->
  <h2 class="section-title">💾 Model Checkpoints &amp; Weights Registry</h2>
  <div class="card">
    <p style="color: var(--text-muted); margin-bottom: 16px;">Trained model checkpoints evaluated on the Raspberry Pi 5 benchmark testbed:</p>
    <div class="dl-row">
      <a href="/outputs/checkpoints/spectralgpt.pth" download class="btn btn-outline">📦 spectralgpt.pth (85.2 MB)</a>
      <a href="/outputs/checkpoints/ss_mae.pth" download class="btn btn-outline">📦 ss_mae.pth (83.8 MB)</a>
      <a href="/outputs/checkpoints/hypersigma.pth" download class="btn btn-outline">📦 hypersigma.pth (88.1 MB)</a>
      <a href="/outputs/checkpoints/hybridsn_3d_2d_cnn.pth" download class="btn btn-outline">📦 hybridsn_3d_2d_cnn.pth (4.8 MB)</a>
      <a href="/outputs/checkpoints/spectral_transformer.pth" download class="btn btn-outline">📦 spectral_transformer.pth (292 KB)</a>
      <a href="/outputs/checkpoints/3d_cnn_hamida_et_al..pth" download class="btn btn-outline">📦 3d_cnn_hamida_et_al..pth (119 KB)</a>
      <a href="/outputs/checkpoints/random_forest.joblib" download class="btn btn-outline">📦 random_forest.joblib (10.7 MB)</a>
      <a href="/outputs/checkpoints/svm_rbf.joblib" download class="btn btn-outline">📦 svm_rbf.joblib (2.4 MB)</a>
    </div>
  </div>
</div>
</body>
</html>
"""
    return html

def generate_narratives_html():
    """Generates the narratives.html Grand Narrative curriculum portal."""
    chapters = [
        ("00", "Master Narrative Overview", "Dual-Pillar Framework & National Remote Sensing Gap", "00_master_narrative_overview"),
        ("01", "The Invisible Rainbow", "Physics & Chemistry of Hyperspectral Imaging", "01_the_invisible_rainbow"),
        ("02", "How AI Perceives Light", "Deep Learning & Hyperspectral Foundation Models", "02_how_ai_perceives_light"),
        ("03", "The Seven Breakthroughs", "BharatSpectral-MAE Core Architectural Innovations", "03_the_seven_breakthroughs"),
        ("04", "The Web of Disciplines", "Bridging Spectroscopy, Remote Sensing, Agronomy & Computer Science", "04_the_web_of_disciplines"),
        ("05", "GIS Baseline vs. AI Brain", "Why Traditional Deterministic Spectroscopy Needs Deep Learning", "05_gis_baseline_vs_ai_brain"),
        ("06", "Literature References & Reading Guide", "Exhaustive Academic Bibliography & Learning Roadmap", "06_literature_references_and_reading_guide")
    ]
    
    cards_html = ""
    for num, title, subtitle, basename in chapters:
        pdf_name = f"{basename}.pdf"
        html_name = f"/narratives/{basename}.html"
        pdf_path = f"/narratives/pdfs/{pdf_name}"
        cards_html += f"""
        <div class="chap-card">
          <div class="chap-num">CHAPTER {num}</div>
          <div class="chap-title">{title}</div>
          <div class="chap-sub">{subtitle}</div>
          <div class="chap-actions">
            <a href="{html_name}" class="btn btn-cyan">📖 Read Online</a>
            <a href="{pdf_path}" download class="btn btn-outline">📥 Download PDF</a>
          </div>
        </div>
        """
        
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Grand Narrative: 7-Chapter Curriculum • BharatSpectral</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #0b0f19;
      --bg-card: #151d2e;
      --border: #233148;
      --cyan: #38bdf8;
      --teal: #14b8a6;
      --text: #e2e8f0;
      --text-muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg-dark);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      padding-top: 72px;
      padding-bottom: 80px;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 24px;
    }}
    .hero {{
      text-align: center;
      margin-bottom: 40px;
    }}
    .tag {{
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 4px 14px;
      border-radius: 9999px;
      background: rgba(56, 189, 248, 0.12);
      color: var(--cyan);
      border: 1px solid var(--cyan);
      margin-bottom: 12px;
    }}
    h1 {{
      font-size: 2.6rem;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.02em;
      margin-bottom: 10px;
    }}
    .subtitle {{
      color: var(--text-muted);
      font-size: 1.1rem;
      max-width: 800px;
      margin: 0 auto;
    }}
    .chap-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 20px;
      margin-top: 30px;
    }}
    .chap-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s, border-color 0.2s;
    }}
    .chap-card:hover {{
      transform: translateY(-2px);
      border-color: var(--cyan);
    }}
    .chap-num {{
      font-size: 0.75rem;
      font-weight: 800;
      color: var(--cyan);
      letter-spacing: 0.1em;
      margin-bottom: 8px;
    }}
    .chap-title {{
      font-size: 1.25rem;
      font-weight: 800;
      color: #fff;
      margin-bottom: 6px;
    }}
    .chap-sub {{
      font-size: 0.85rem;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 20px;
      flex: 1;
    }}
    .chap-actions {{
      display: flex;
      gap: 10px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 0.82rem;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s;
    }}
    .btn-cyan {{
      background: var(--cyan);
      color: #0b0f19;
    }}
    .btn-cyan:hover {{
      background: #7dd3fc;
    }}
    .btn-outline {{
      border: 1px solid var(--border);
      color: var(--text);
      background: rgba(255, 255, 255, 0.04);
    }}
    .btn-outline:hover {{
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
    }}
  </style>
</head>
<body>
{NAVBAR_HTML}
<div class="container">
  <div class="hero">
    <span class="tag">Comprehensive Foundational Primer</span>
    <h1>BharatSpectral Grand Narrative</h1>
    <p class="subtitle">A 7-chapter publication-grade curriculum connecting quantum spectroscopy, foundation model architectures, and digital public infrastructure.</p>
  </div>

  <div class="chap-grid">
    {cards_html}
  </div>
</div>
</body>
</html>
"""
    return html

def render_markdown_file(src_md_path, dest_html_path, title, back_url="/index.html", back_label="Home", pdf_link=None):
    with open(src_md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    html_body = markdown.markdown(md_text, extensions=['extra', 'tables', 'fenced_code'])
    
    download_bar = ""
    if pdf_link:
        download_bar = f"""
        <div class="pdf-download-bar">
          <div>
            <strong>📄 Publication PDF Edition:</strong> Formatted with publication typography and diagrams.
          </div>
          <a href="{pdf_link}" download class="btn btn-cyan" style="text-decoration:none; padding: 6px 14px; border-radius: 6px; font-weight:700; font-size:0.82rem; background:#38bdf8; color:#0b0f19;">Download PDF 📥</a>
        </div>
        """
        
    page_html = READER_PAGE_TEMPLATE.format(
        title=title,
        navbar=NAVBAR_HTML,
        back_url=back_url,
        back_label=back_label,
        download_bar=download_bar,
        content=html_body
    )
    os.makedirs(os.path.dirname(dest_html_path), exist_ok=True)
    with open(dest_html_path, 'w', encoding='utf-8') as f:
        f.write(page_html)

def inject_navbar_into_html(file_path, active_id=""):
    """Injects the top navbar into existing HTML pages if not present."""
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "id=\"bharat-portal-bar\"" in content:
        return  # already injected
        
    navbar_instance = NAVBAR_HTML
    if active_id:
        navbar_instance = navbar_instance.replace(f'id="{active_id}"', f'id="{active_id}" class="p-link active"')
        
    # Inject after <body> tag
    if "<body" in content:
        parts = content.split("<body", 1)
        body_tag_and_rest = parts[1].split(">", 1)
        new_content = parts[0] + "<body" + body_tag_and_rest[0] + ">\n" + navbar_instance + "\n" + body_tag_and_rest[1]
        
        # Add body padding-top: 52px so navbar doesn't obscure content
        style_override = "<style> body { padding-top: 52px !important; } </style>\n</head>"
        new_content = new_content.replace("</head>", style_override)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

def build_all():
    print("=================================================================")
    print("🚀  BharatSpectral Master Build & Deployment Assembler")
    print("=================================================================")

    # 1. Build PPTX Deck
    print("1. Compiling PowerPoint presentation (.pptx)...")
    subprocess.run([sys.executable, os.path.join(REPO_ROOT, "presentation", "build_deck.py")], check=True)

    # 2. Build HTML Presentation
    print("2. Compiling Interactive HTML Deck (.html)...")
    subprocess.run([sys.executable, os.path.join(REPO_ROOT, "presentation", "build_html_pinboard_deck.py")], check=True)

    # 3. Build Grand Narrative PDFs
    print("3. Compiling Grand Narrative PDFs (7 chapters)...")
    subprocess.run([sys.executable, os.path.join(REPO_ROOT, "narratives", "convert_md_to_pdf.py")], check=True)

    # 4. Prepare dist/ directory
    print("4. Initializing dist/ directory...")
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR, exist_ok=True)

    # Write index.html (Master Public Portal Landing Page)
    print("5. Generating index.html (Master Ecosystem Portal)...")
    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_index_portal_html())

    # Copy dedicated interactive presentation.html and PPTX
    shutil.copy(os.path.join(REPO_ROOT, "presentation", "presentation.html"), os.path.join(DIST_DIR, "presentation.html"))
    shutil.copy(os.path.join(REPO_ROOT, "presentation", "BharatSpectral_MidTerm_Presentation.pptx"), os.path.join(DIST_DIR, "BharatSpectral_MidTerm_Presentation.pptx"))

    # Copy interactive phase reports
    for doc_file in ["phase1.html", "phase2.html", "phase3.html", "phase4&5.html", "workflow-handbook.html", "references_pinboard.html"]:
        src = os.path.join(REPO_ROOT, "docs", doc_file)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(DIST_DIR, doc_file))

    # Generate benchmarks.html & narratives.html
    print("6. Generating benchmarks.html & narratives.html...")
    with open(os.path.join(DIST_DIR, "benchmarks.html"), "w", encoding="utf-8") as f:
        f.write(generate_benchmarks_html())

    with open(os.path.join(DIST_DIR, "narratives.html"), "w", encoding="utf-8") as f:
        f.write(generate_narratives_html())

    # Render markdown documents
    print("7. Rendering Markdown documents into styled HTML reader pages...")
    os.makedirs(os.path.join(DIST_DIR, "docs"), exist_ok=True)
    os.makedirs(os.path.join(DIST_DIR, "narratives", "pdfs"), exist_ok=True)

    render_markdown_file(
        os.path.join(REPO_ROOT, "docs", "project_synopsis.md"),
        os.path.join(DIST_DIR, "docs", "project_synopsis.html"),
        "BharatSpectral Project Synopsis",
        back_url="/index.html",
        back_label="Home"
    )
    render_markdown_file(
        os.path.join(REPO_ROOT, "docs", "midterm_defense_grounding_and_gis_analysis.md"),
        os.path.join(DIST_DIR, "docs", "midterm_defense_grounding_and_gis_analysis.html"),
        "Mid-Term Defense Grounding & GIS Spectroscopic Analysis",
        back_url="/benchmarks.html",
        back_label="Benchmarks"
    )
    render_markdown_file(
        os.path.join(REPO_ROOT, "docs", "MASTER_PLAN.md"),
        os.path.join(DIST_DIR, "docs", "MASTER_PLAN.html"),
        "BharatSpectral Master Execution Plan",
        back_url="/index.html",
        back_label="Home"
    )

    # Render Grand Narrative chapters
    for f in sorted(os.listdir(os.path.join(REPO_ROOT, "narratives"))):
        if f.endswith(".md") and f != "README.md":
            base = os.path.splitext(f)[0]
            pdf_link = f"/narratives/pdfs/{base}.pdf"
            render_markdown_file(
                os.path.join(REPO_ROOT, "narratives", f),
                os.path.join(DIST_DIR, "narratives", f"{base}.html"),
                f"Chapter: {base.replace('_', ' ').title()}",
                back_url="/narratives.html",
                back_label="Grand Narrative",
                pdf_link=pdf_link
            )

    # Copy PDFs
    for pdf in os.listdir(os.path.join(REPO_ROOT, "narratives", "pdfs")):
        if pdf.endswith(".pdf"):
            shutil.copy(
                os.path.join(REPO_ROOT, "narratives", "pdfs", pdf),
                os.path.join(DIST_DIR, "narratives", "pdfs", pdf)
            )

    # Copy outputs (figures, tables, checkpoints)
    print("8. Copying empirical figures, tables, and checkpoints...")
    shutil.copytree(os.path.join(REPO_ROOT, "outputs", "figures"), os.path.join(DIST_DIR, "outputs", "figures"))
    shutil.copytree(os.path.join(REPO_ROOT, "outputs", "tables"), os.path.join(DIST_DIR, "outputs", "tables"))
    shutil.copytree(os.path.join(REPO_ROOT, "outputs", "checkpoints"), os.path.join(DIST_DIR, "outputs", "checkpoints"))

    # Copy src/ and pipeline script
    if os.path.exists(os.path.join(REPO_ROOT, "src")):
        shutil.copytree(os.path.join(REPO_ROOT, "src"), os.path.join(DIST_DIR, "src"))
    if os.path.exists(os.path.join(REPO_ROOT, "run_pipeline.sh")):
        shutil.copy(os.path.join(REPO_ROOT, "run_pipeline.sh"), os.path.join(DIST_DIR, "run_pipeline.sh"))

    # Inject navbar into all standalone HTML pages in dist/
    print("9. Injecting unified ecosystem navigation into all pages...")
    nav_mapping = {
        "index.html": "nav-home",
        "presentation.html": "nav-slides",
        "benchmarks.html": "nav-benchmarks",
        "phase1.html": "nav-phase1",
        "phase2.html": "nav-phase2",
        "phase3.html": "nav-phase3",
        "phase4&5.html": "nav-phase45",
        "narratives.html": "nav-narratives",
        "references_pinboard.html": "nav-pinboard",
        "workflow-handbook.html": "nav-handbook"
    }
    for filename, nav_id in nav_mapping.items():
        p = os.path.join(DIST_DIR, filename)
        if os.path.exists(p):
            inject_navbar_into_html(p, nav_id)

    print("=================================================================")
    print(f"✅  dist/ assembled successfully! Total files: {len(os.listdir(DIST_DIR))}")
    print("=================================================================")

if __name__ == "__main__":
    build_all()
