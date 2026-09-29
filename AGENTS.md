# AGENTS.md — Developer & AI Agent Context for BharatSpectral Repository

Welcome to the **BharatSpectral** capstone codebase. This repository houses the research code, presentation generators, documentation, and architectural artifacts for the **BharatSpectral Dual-Pillar Project**.

---

## 1. Project Overview & Dual-Pillar Framework

**BharatSpectral** establishes **Democratized Spectral-Semantic Intelligence (DSSI)** for Indian Earth Observation across two synergistic pillars:

1.  **The Research Pillar (Spectral Foundation Model):** **BharatSpectral-MAE**, a physics-informed hyperspectral Foundation Model engineered specifically for Indian smallholder spatial fragmentation, multi-crop intercropping, multi-season phenology, and multi-sensor heterogeneity (AVIRIS-NG India, ISRO HysIS, NASA EMIT).
2.  **The Product Pillar (Geospatial Digital Public Infrastructure):** **BharatSpectral Platform**, a free, citizen-facing WebGIS delivering sub-pixel biochemical analytics (crop nutrients, soil health, water quality) running edge inference on Cloudflare R2 + Workers via Serverless Spectral Inference (SSI).

```text
┌──────────────────────────────────────────────────────────────────┐
│                     RESEARCH PILLAR                              │
│   BharatSpectral-MAE: Physics-Informed Foundation Model          │
│   Innovations: SSPE · RNRL · SHT · AAM · ECSA · Ph-LoRA · FASU  │
│   Sensors: AVIRIS-NG India · NASA EMIT · ISRO HysIS              │
│   Benchmark: BharatHSI-Bench                                     │
└────────────────────────────┬─────────────────────────────────────┘
                             │ Inference Engine
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                     PRODUCT PILLAR                               │
│   BharatSpectral Platform: WebGIS Public Infrastructure          │
│   Stack: Cloudflare R2 (zero-egress) · Workers (ONNX) · MapLibre │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Architectural Innovations (The 7 Research Innovations)

When editing model code or describing the system, preserve these 7 named architectural innovations:

| ID | Innovation Name | Architectural Role |
|---|---|---|
| **SSPE** | **Scale-Spectral Positional Encoding** | Jointly encodes spatial Ground Sample Distance (GSD), spectral bandwidth, and mixture entropy across 3 sensors. |
| **RNRL** | **Reflectance-Normalized Reconstruction Loss** | Normalizes MAE reconstruction by reflectance magnitude to preserve low-reflectance features (< 5% SWIR). |
| **SHT** | **Spectral Harmonic Tokenizer** | Sensor-adaptive 3D tokenizer that dynamically Chunks bands by absorption feature density (fine tokens in Red-Edge). |
| **AAM** | **Atmospheric Absorption Masking** | Replaces random masking with structured spectral gap masking across atmospheric water vapor/CO₂ absorption bands. |
| **ECSA** | **Endmember-Constrained Self-Attention** | Regularizes Transformer attention using a spectral unmixing prior to attend to physically similar endmembers. |
| **Ph-LoRA** | **Phenology-Conditioned LoRA** | Modulates low-rank adapter weights based on growing season (Kharif/Rabi/Zaid) and growth stage embeddings. |
| **FASU** | **Foundation-Augmented Spectral Unmixing** | Sub-pixel unmixing head operating on pre-trained foundation representations for non-linear canopy decomposition. |

---

## 3. Directory Structure & Key Files

```text
/data/data/com.termux/files/home/btp/
├── README.md                                  # Top-Level Repository Overview & Directory Map
├── AGENTS.md                                  # Developer & AI Agent Context
├── .gitignore                                 # Git Ignore Rules
│
├── docs/                                      # Research Documentation, Proposals & Roadmaps
│   ├── README.md                              # Docs directory guide
│   ├── project_synopsis.md                    # Master Capstone Synopsis & Formal Proposal
│   ├── midterm_defense_grounding_and_gis_analysis.md # Defense grounding, GIS vs AI analysis & baseline proofs
│   ├── MASTER_PLAN.md                         # Master execution roadmap & milestones
│   ├── workflow-handbook.html                 # Interactive workflow handbook
│   ├── references_pinboard.html               # Interactive visual references pinboard
│   └── phase1.html ... phase4&5.html          # Interactive phase-specific deep dive reports
│
├── presentation/                              # Slide Decks & Generation Scripts
│   ├── README.md                              # Presentation guide & regeneration manual
│   ├── build_deck.py                          # Python script (python-pptx) to assemble 16:9 PPTX deck
│   ├── build_html_deck.py                     # Python script to compile interactive HTML web slide deck
│   ├── presentation.html                      # Compiled interactive HTML presentation
│   └── BharatSpectral_MidTerm_Presentation.pptx # Compiled PowerPoint slide deck
│
├── narratives/                                # "Grand Narrative" 7-Chapter Foundational Primer
│   ├── README.md                              # Chapter curriculum & reading guide
│   ├── 00_master_narrative_overview.md ... 06_literature_references_and_reading_guide.md
│   ├── convert_md_to_pdf.py                   # ReportLab Markdown-to-PDF generator
│   └── pdfs/                                  # Pre-rendered publication PDFs (00 through 06)
│
└── outputs/                                   # Experimental Artifacts, Baselines & Benchmarks
    ├── README.md                              # Experimental summary & benchmarks guide
    ├── checkpoints/                           # Model weights (SVM, RF, 3D-CNN, HybridSN, Transformer)
    ├── figures/                               # Benchmark comparison plots & domain shift diagrams
    └── tables/                                # Benchmark CSVs, cross-scene evaluation & GIS metrics JSONs
```

---

## 4. Workflows for AI Agents

### Regenerating Presentation Decks
If you modify slides, update python scripts, or add presentation content:
*   To regenerate PPTX slides:
    ```bash
    python3 presentation/build_deck.py
    ```
*   To regenerate interactive HTML presentation:
    ```bash
    python3 presentation/build_html_deck.py
    ```

### Regenerating Grand Narrative PDFs
*   To rebuild PDFs from markdown chapters:
    ```bash
    python3 narratives/convert_md_to_pdf.py
    ```

### Code & Documentation Standards
1.  **Do Not Swallow Physical Logic:** Never replace physics-informed losses (RNRL, ECSA) or unmixing constraints with generic MSE loss or random dropout.
2.  **Dataset References:** Always reference **AVIRIS-NG India** (425 bands, Bhoonidhi), **ISRO HysIS** (220 bands), and **NASA EMIT** (285 bands). Do not treat **Indian Pines** (1992 Indiana) as an Indian dataset—it is a baseline transfer source.
3.  **File Modification Rules:** Use `replace_file_content` for precise contiguous edits. Do not re-write giant python scripts from scratch when making minor updates.
4.  **Verification:** Always run python scripts after modification to verify compilation and non-zero exit codes.

---

## 5. Defense & Presentation Context Guidelines

When assisting the user with defense preparation, presentations, or thesis writing:
*   **Emphasize the Dual-Pillar Structure:** Always highlight both the AI research novelty (Pillar 1) and the WebGIS public infrastructure (Pillar 2).
*   **GIS Tool Baseline:** Remember that GIS spectroscopic tools (SAM, LSU in ENVI/QGIS) serve as a deterministic physical baseline, but fail under non-linear unmixing and magnitude variations. BharatSpectral-MAE bridges deep learning scale with spectroscopic physics to surpass GIS accuracy while running sub-second edge inference.
