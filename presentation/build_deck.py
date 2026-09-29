#!/usr/bin/env python3
"""
build_deck.py
Constructs the complete 19-Slide Academic Pinboard Presentation in PowerPoint (.pptx)
for BharatSpectral in the exact ~/ppt/vs theme:
- Corkboard background (assets/cork_bg.png) with beveled wooden frame
- Textured parchment and kraft paper cards with pushpins and washi tape
- Scientific diagrams, benchmark comparison tables, and comic strips
- 1:1 deterministic alignment with presentation/index.html
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

SLIDE_WIDTH_IN = 13.333
SLIDE_HEIGHT_IN = 7.5

COLOR_TEXT = RGBColor(42, 35, 27)         # #2A231B Primary dark ink
COLOR_TEXT_DIM = RGBColor(109, 95, 82)    # #6D5F52 Secondary ink
COLOR_CYAN = RGBColor(11, 114, 133)       # #0B7285 Water / Primary accent
COLOR_PURPLE = RGBColor(103, 65, 217)     # #6741D9 Scientific / citations
COLOR_ORANGE = RGBColor(217, 72, 15)      # #D9480F Warnings / parameters
COLOR_GREEN = RGBColor(43, 138, 62)       # #2B8A3E Suitable / safe
COLOR_RED = RGBColor(201, 42, 42)         # #C92A2A Hazard / unfit
COLOR_YELLOW = RGBColor(217, 155, 0)      # #D99B00 Amber

BG_PARCHMENT = RGBColor(255, 253, 245)    # #FFFDF5 Ivory parchment
BG_KRAFT = RGBColor(244, 236, 220)        # #F4ECDC Warm kraft
BORDER_CARD = RGBColor(216, 200, 175)     # #D8C8AF Card border

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")

CORK_BG = os.path.join(ASSETS_DIR, "cork_bg.png")
PIN_CYAN = os.path.join(ASSETS_DIR, "pin_cyan.png")
PIN_YELLOW = os.path.join(ASSETS_DIR, "pin_yellow.png")
PIN_RED = os.path.join(ASSETS_DIR, "pin_red.png")
PIN_GREEN = os.path.join(ASSETS_DIR, "pin_green.png")
PIN_PURPLE = os.path.join(ASSETS_DIR, "pin_purple.png")
TAPE_STRIP = os.path.join(ASSETS_DIR, "tape_strip.png")

OUTPUT_PPTX = os.path.join(SCRIPT_DIR, "BharatSpectral_MidTerm_Presentation.pptx")

def create_deck():
    prs = pptx.Presentation()
    prs.slide_width = Inches(SLIDE_WIDTH_IN)
    prs.slide_height = Inches(SLIDE_HEIGHT_IN)
    blank_layout = prs.slide_layouts[6]
    return prs, blank_layout

def apply_cork_background(slide):
    if os.path.exists(CORK_BG):
        slide.shapes.add_picture(CORK_BG, Inches(0), Inches(0), Inches(SLIDE_WIDTH_IN), Inches(SLIDE_HEIGHT_IN))

def add_header_note(slide, title_text, sub_text=None, tape=True, pin_color="cyan"):
    header_w = Inches(11.2)
    header_h = Inches(0.92)
    header_x = Inches((SLIDE_WIDTH_IN - 11.2) / 2)
    header_y = Inches(0.32)

    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, header_x, header_y, header_w, header_h)
    card.fill.solid()
    card.fill.fore_color.rgb = BG_PARCHMENT
    card.line.color.rgb = BORDER_CARD
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.08)
    tf.margin_bottom = Inches(0.08)

    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Trebuchet MS"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    if sub_text:
        p2 = tf.add_paragraph()
        p2.text = sub_text
        p2.alignment = PP_ALIGN.CENTER
        p2.font.name = "Calibri"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_TEXT_DIM

    if tape and os.path.exists(TAPE_STRIP):
        slide.shapes.add_picture(TAPE_STRIP, Inches((SLIDE_WIDTH_IN - 1.8) / 2), Inches(0.18), Inches(1.8), Inches(0.38))

    pin_path = {"cyan": PIN_CYAN, "yellow": PIN_YELLOW, "red": PIN_RED, "green": PIN_GREEN, "purple": PIN_PURPLE}.get(pin_color, PIN_CYAN)
    if os.path.exists(pin_path):
        slide.shapes.add_picture(pin_path, header_x + Inches(0.2), header_y - Inches(0.14), Inches(0.38), Inches(0.38))

    return card

def add_paper_card(slide, x_in, y_in, w_in, h_in, bg_color=BG_PARCHMENT, border_color=BORDER_CARD, pin_color=None, tape=False):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x_in), Inches(y_in), Inches(w_in), Inches(h_in))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)

    if tape and os.path.exists(TAPE_STRIP):
        slide.shapes.add_picture(TAPE_STRIP, Inches(x_in + (w_in - 1.5) / 2), Inches(y_in - 0.16), Inches(1.5), Inches(0.36))

    if pin_color:
        pin_path = {"cyan": PIN_CYAN, "yellow": PIN_YELLOW, "red": PIN_RED, "green": PIN_GREEN, "purple": PIN_PURPLE}.get(pin_color, PIN_CYAN)
        if os.path.exists(pin_path):
            slide.shapes.add_picture(pin_path, Inches(x_in + (w_in - 0.38) / 2), Inches(y_in - 0.16), Inches(0.38), Inches(0.38))

    return card

def add_picture_safely(slide, img_path, x_in, y_in, w_in, h_in):
    if os.path.exists(img_path):
        return slide.shapes.add_picture(img_path, Inches(x_in), Inches(y_in), Inches(w_in), Inches(h_in))
    return None

def build_presentation():
    prs, blank = create_deck()

    # SLIDE 1: Title Slide
    s1 = prs.slides.add_slide(blank)
    apply_cork_background(s1)
    title_card = add_paper_card(s1, 1.2, 0.45, 10.9, 1.8, bg_color=BG_PARCHMENT, pin_color="cyan", tape=True)
    tf1 = title_card.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "BHARATSPECTRAL: DEMOCRATIZED SPECTRAL-SEMANTIC INTELLIGENCE"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Trebuchet MS"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p2 = tf1.add_paragraph()
    p2.text = "Physics-Informed Hyperspectral Foundation Model & Serverless WebGIS Public Infrastructure for Indian Earth Observation"
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Calibri"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT

    # Left card: Spectrum Contrast
    add_paper_card(s1, 1.2, 2.45, 5.3, 4.5, bg_color=BG_PARCHMENT, pin_color="yellow")
    add_picture_safely(s1, os.path.join(ASSETS_DIR, "spectrum_contrast.png"), 1.4, 2.65, 4.9, 3.8)

    # Right card: Overview
    c_right = add_paper_card(s1, 6.8, 2.45, 5.3, 4.5, bg_color=BG_KRAFT, pin_color="green")
    tf_r = c_right.text_frame
    tf_r.word_wrap = True
    pr1 = tf_r.paragraphs[0]
    pr1.text = "Dual-Pillar National Innovation Framework"
    pr1.font.name = "Trebuchet MS"
    pr1.font.size = Pt(14)
    pr1.font.bold = True
    pr1.font.color.rgb = COLOR_GREEN

    points = [
        "Research Pillar: BharatSpectral-MAE Foundation Model (SSPE, RNRL, SHT, AAM, ECSA, Ph-LoRA, FASU).",
        "Product Pillar: Serverless Edge WebGIS on Cloudflare R2 + Workers for 140 million smallholders.",
        "Datasets Grounded: AVIRIS-NG India (425b), ISRO HysIS (220b), NASA EMIT (285b).",
        "Empirical Grounding: 22%-37% domain shift drop quantified; traditional GIS tools audited.",
        "National Mission Alignment: IndiaAI Mission & Geospatial Digital Public Infrastructure (DPI)."
    ]
    for pt_text in points:
        pr = tf_r.add_paragraph()
        pr.text = "• " + pt_text
        pr.font.name = "Calibri"
        pr.font.size = Pt(11)
        pr.font.color.rgb = COLOR_TEXT
    print("Created Slide 1")

    # SLIDE 2: Objectives
    s2 = prs.slides.add_slide(blank)
    apply_cork_background(s2)
    add_header_note(s2, "Engineering Objectives: Capstone 7th Semester Scope", "Formal milestone delivery evaluated against real Indian agricultural flightlines", pin_color="cyan")
    col_w = 3.6
    # 3 Column Cards
    c1 = add_paper_card(s2, 1.0, 1.5, col_w, 5.4, pin_color="cyan")
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "PILLAR 1: CURATE & STANDARDIZE"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_CYAN
    for item in ["Harmonize AVIRIS-NG India (425b), ISRO HysIS (220b), and NASA EMIT (285b).", "Apply 6S radiative atmospheric water vapor correction (1.4μm & 1.9μm masking).", "Standardize smallholder spatial patch generator.", "[STATUS: PHASE 1 COMPLETE]"]:
        p = tf_c1.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10.5)

    c2 = add_paper_card(s2, 4.86, 1.5, col_w, 5.4, pin_color="yellow")
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "PILLAR 2: BENCHMARK & DIAGNOSE"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_ORANGE
    for item in ["Train RF, SVM-RBF, HybridSN (3D-2D), 3D-CNN, and Spectral Transformer.", "Quantify catastrophic 22%-37% OA drop under Indian domain shift.", "Audit physical GIS spectroscopic tools (SAM, LSU/FCLS) under non-linear canopy scattering.", "[STATUS: PHASE 2 COMPLETE]"]:
        p = tf_c2.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10.5)

    c3 = add_paper_card(s2, 8.73, 1.5, col_w, 5.4, pin_color="purple")
    tf_c3 = c3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    p.text = "PILLAR 3: ARCHITECT NOVELTY"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_PURPLE
    for item in ["Formalize BharatSpectral-MAE: SSPE, RNRL, SHT, AAM, ECSA, Ph-LoRA, FASU.", "Bridge optical quantum physics with Transformer attention heads.", "Prepare high-performance GPU pretraining pipeline for 8th semester scaling.", "[STATUS: PHASE 3 ACTIVE FRONTIER]"]:
        p = tf_c3.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10.5)
    print("Created Slide 2")

    # SLIDE 3: Continuous Spectroscopy
    s3 = prs.slides.add_slide(blank)
    apply_cork_background(s3)
    add_header_note(s3, "Continuous Spectroscopy: What Each Spectral Band Captures", "Narrow-band molecular absorption physics across VNIR, Red-Edge, NIR, and SWIR regimes", pin_color="green")
    add_paper_card(s3, 1.0, 1.5, 6.0, 5.4, pin_color="green")
    add_picture_safely(s3, os.path.join(ASSETS_DIR, "continuous_spectroscopy.png"), 1.2, 1.8, 5.6, 4.7)

    c3_r = add_paper_card(s3, 7.3, 1.5, 5.0, 5.4, bg_color=BG_KRAFT, pin_color="cyan")
    tf = c3_r.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Diagnostic Absorption Bands & Innovations"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.color.rgb = COLOR_CYAN
    for item in [
        "400–700 nm (VNIR): Plant pigment absorption (Chlorophyll a/b, Carotenoids).",
        "700–750 nm (Red-Edge): Steep cellular structure cliff. [NOTE: SHT] Spectral Harmonic Tokenizer allocates fine tokens here.",
        "970 & 1200 nm (NIR): Cellular liquid Equivalent Water Thickness (EWT).",
        "1.4 & 1.9 μm: Atmospheric water vapor zero-transmission gaps. [NOTE: AAM] Atmospheric Absorption Masking.",
        "2.1–2.3 μm (SWIR): Organic protein nitrogen, soil organic carbon (SOC), clay mineral lattices."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10)
    print("Created Slide 3")

    # SLIDE 4: Photon Pinball
    s4 = prs.slides.add_slide(blank)
    apply_cork_background(s4)
    add_header_note(s4, "The 'Pinball Machine' Physics: Non-Linear Scattering & 3D Pixels", "Why multi-tier Indian smallholder canopies require 3D tensor foundation representations", pin_color="purple")
    add_paper_card(s4, 1.0, 1.5, 6.2, 5.4, pin_color="purple")
    add_picture_safely(s4, os.path.join(ASSETS_DIR, "photon_pinball_cube.png"), 1.2, 1.8, 5.8, 4.7)

    c4_r = add_paper_card(s4, 7.5, 1.5, 4.8, 5.4, bg_color=BG_KRAFT, pin_color="yellow")
    tf = c4_r.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Canopy Radiative Transfer Breakdown"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.color.rgb = COLOR_ORANGE
    for item in [
        "Multi-Bounce Scattering: Sunlight enters intercropped sorghum + pigeon pea and ricochets between leaves and soil before sensor reception.",
        "Failure of Linear Unmixing: Classical GIS (LSU/FCLS) assumes linear superposition. Ricochets cause non-linear cross-talk (RMSE > 0.15).",
        "[NOTE: SSPE] Scale-Spectral Positional Encoding: Jointly encodes GSD (4–60m), bandwidth, and mixture entropy.",
        "[NOTE: FASU] Foundation-Augmented Spectral Unmixing: Decomposes complex non-linear canopy mixtures using pretrained foundation representations."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10)
    print("Created Slide 4")

    # SLIDE 5: Venn Diagram
    s5 = prs.slides.add_slide(blank)
    apply_cork_background(s5)
    add_header_note(s5, "The Intersection of Human Knowledge Systems", "Synthesizing optical spectroscopy physics, foundation AI architectures, and open WebGIS public infrastructure", pin_color="cyan")
    add_paper_card(s5, 1.0, 1.5, 6.0, 5.4, pin_color="cyan")
    add_picture_safely(s5, os.path.join(ASSETS_DIR, "venn_diagram.png"), 1.2, 1.8, 5.6, 4.7)

    c5_r = add_paper_card(s5, 7.3, 1.5, 5.0, 5.4, bg_color=BG_KRAFT, pin_color="green")
    tf = c5_r.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Disciplinary Convergence"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.color.rgb = COLOR_GREEN
    for item in [
        "Spectroscopy Physics: Provides ground truth absorption laws, radiative transfer equations, and atmospheric absorption gap constraints.",
        "Foundation Model AI: Provides self-attention capacity, masked autoencoding pretraining, and non-linear parameter-efficient adaptation (LoRA).",
        "WebGIS Public Infrastructure: Eliminates cloud costs through Cloudflare R2 zero-egress storage and browser-edge ONNX WASM inference.",
        "Core Convergence: BharatSpectral (DSSI) delivers democratized biochemical intelligence directly to citizen devices."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10)
    print("Created Slide 5")

    # SLIDE 6: India Coverage
    s6 = prs.slides.add_slide(blank)
    apply_cork_background(s6)
    add_header_note(s6, "Open Hyperspectral Corpus over the Indian Landmass", "Phase 1 Complete • Harmonizing airborne AVIRIS-NG India, spaceborne ISRO HysIS, and NASA EMIT", pin_color="green")
    add_paper_card(s6, 1.0, 1.5, 6.0, 5.4, pin_color="green")
    add_picture_safely(s6, os.path.join(ASSETS_DIR, "india_hsi_coverage.png"), 1.2, 1.8, 5.6, 4.7)

    c6_r = add_paper_card(s6, 7.3, 1.5, 5.0, 5.4, bg_color=BG_KRAFT, pin_color="purple")
    tf = c6_r.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Corpus Harmonization & Status"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.color.rgb = COLOR_PURPLE
    for item in [
        "AVIRIS-NG India: 425 continuous bands (380–2510 nm), 4–8m GSD flightlines over Anand (Gujarat), Godavari Basin (AP), and Punjab tracts.",
        "ISRO HysIS: 220 bands (VNIR/SWIR), 30m spaceborne GSD.",
        "NASA EMIT: 285 bands (381–2493 nm), 60m GSD on the International Space Station.",
        "[NOTE: RNRL] Reflectance-Normalized Reconstruction Loss: Prevents gradients from collapsing in low-reflectance SWIR bands (<5% reflectance).",
        "Deliverable Status: Phase 1 Fully Completed (1.2 TB curated corpus)."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10)
    print("Created Slide 6")

    # SLIDE 7: Preprocessing Pipeline
    s7 = prs.slides.add_slide(blank)
    apply_cork_background(s7)
    add_header_note(s7, "Preprocessing & Physical Normalization Pipeline", "Phase 1 Detail • Converting raw Bhoonidhi/STAC binary radiance files into standardized analysis tensors", pin_color="cyan")
    add_paper_card(s7, 1.0, 1.5, 11.3, 5.4, pin_color="cyan")
    add_picture_safely(s7, os.path.join(ASSETS_DIR, "preprocessing_pipeline.png"), 1.2, 1.7, 10.9, 4.8)
    print("Created Slide 7")

    # SLIDE 8: Benchmarking Arena
    s8 = prs.slides.add_slide(blank)
    apply_cork_background(s8)
    add_header_note(s8, "Benchmarking Previous Attempts: Empirical Proof of Need", "Phase 2 Evaluation • Grounded proof that Western HSI models suffer catastrophic collapse in India", pin_color="red")
    add_paper_card(s8, 1.0, 1.5, 5.8, 5.4, pin_color="red")
    add_picture_safely(s8, os.path.join(REPO_ROOT, "outputs/figures/domain_shift_collapse.png"), 1.2, 1.8, 5.4, 4.7)

    c8_r = add_paper_card(s8, 7.1, 1.5, 5.2, 5.4, bg_color=BG_KRAFT, pin_color="yellow")
    tf = c8_r.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Empirical Benchmark Results (Pi 5 Testbed)"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(12)
    tf.paragraphs[0].font.color.rgb = COLOR_RED
    for item in [
        "Random Forest: 85.4% -> 57.8% (Drop: 27.6%)",
        "SVM (RBF Kernel): 84.6% -> 62.2% (Drop: 22.4%)",
        "HybridSN (3D-2D CNN): 92.4% -> 55.1% (Drop: 37.3%)",
        "3D-CNN (Hamida et al.): 90.8% -> 56.4% (Drop: 34.4%)",
        "Spectral Transformer: 93.5% -> 60.8% (Drop: 32.7%)",
        "The Indian Pines Fallacy: Canonical 1992 Indiana monoculture models collapse under Indian smallholder fragmentation (1.08 ha) and intercropping.",
        "Status: Phase 2 Empirical Evaluation Completed."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(9.5)
    print("Created Slide 8")

    # SLIDE 9: Traditional GIS Critique
    s9 = prs.slides.add_slide(blank)
    apply_cork_background(s9)
    add_header_note(s9, "Why Existing Methods Fail in Indian Smallholder Ecosystems", "Phase 2 Complete • Physical GIS tools (SAM, LSU in ENVI/QGIS) vs unconstrained deep learning", pin_color="yellow")
    add_paper_card(s9, 1.0, 1.5, 5.8, 5.4, pin_color="yellow")
    add_picture_safely(s9, os.path.join(REPO_ROOT, "outputs/figures/gis_linear_unmixing_residuals.png"), 1.2, 1.7, 5.4, 2.5)
    add_picture_safely(s9, os.path.join(REPO_ROOT, "outputs/figures/sam_magnitude_confusion.png"), 1.2, 4.3, 5.4, 2.4)

    c9_r = add_paper_card(s9, 7.1, 1.5, 5.2, 5.4, bg_color=BG_KRAFT, pin_color="cyan")
    tf = c9_r.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "The Dual Physical & AI Breakdown"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(12)
    tf.paragraphs[0].font.color.rgb = COLOR_CYAN
    for item in [
        "GIS SAM Baseline: Cosine angle ignores absolute reflectance magnitude, causing a 36.4% false match rate (confuses shadow/moisture with crop stress).",
        "GIS Linear Spectral Unmixing (LSU): Produces high residual error (RMSE = 0.2775 on boundaries; 54.2% pixels fail threshold) due to non-linear canopy scattering.",
        "[NOTE: ECSA] Endmember-Constrained Self-Attention: Regularizes Transformer attention weights using spectroscopic unmixing priors.",
        "[NOTE: Ph-LoRA] Phenology-Conditioned LoRA: Modulates adapter weights by Kharif, Rabi, and Zaid phenological stage embeddings."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(9.5)
    print("Created Slide 9")

    # SLIDE 10: Timeline
    s10 = prs.slides.add_slide(blank)
    apply_cork_background(s10)
    add_header_note(s10, "Project Progression: What is Done and The Road Ahead", "Systematic milestone completion across 7th semester and active roadmap for 8th semester scaling", pin_color="cyan")
    add_paper_card(s10, 1.0, 1.5, 11.3, 5.4, pin_color="cyan")
    add_picture_safely(s10, os.path.join(ASSETS_DIR, "project_timeline.png"), 1.2, 1.7, 10.9, 4.8)
    print("Created Slide 10")

    # SLIDE 11: 7 Innovations
    s11 = prs.slides.add_slide(blank)
    apply_cork_background(s11)
    add_header_note(s11, "The 7 Architectural Innovations: Physics-Informed Foundation Model", "Formalizing BharatSpectral-MAE: Engineered specifically for Indian smallholder Earth Observation", pin_color="purple")
    add_paper_card(s11, 1.0, 1.5, 11.3, 5.4, pin_color="purple")
    add_picture_safely(s11, os.path.join(ASSETS_DIR, "seven_innovations_flowchart.png"), 1.2, 1.7, 10.9, 4.8)
    print("Created Slide 11")

    # SLIDE 12: Biochemical Taxonomy
    s12 = prs.slides.add_slide(blank)
    apply_cork_background(s12)
    add_header_note(s12, "Actionable Yield: Multi-Domain Biochemical Diagnostics", "Translating continuous 425-band narrow spectroscopic signatures into 6 national public sector applications", pin_color="green")
    add_paper_card(s12, 1.0, 1.5, 11.3, 5.4, pin_color="green")
    add_picture_safely(s12, os.path.join(ASSETS_DIR, "biochemical_taxonomy.png"), 1.2, 1.7, 10.9, 4.8)
    print("Created Slide 12")

    # SLIDE 13: Farmer Mobile Experience
    s13 = prs.slides.add_slide(blank)
    apply_cork_background(s13)
    add_header_note(s13, "From Orbit to Smallholder: Democratized Mobile Delivery", "Bridging satellite spectroscopy with citizen smartphones via serverless edge browser inference", pin_color="cyan")
    add_paper_card(s13, 1.0, 1.5, 6.0, 5.4, pin_color="cyan")
    add_picture_safely(s13, os.path.join(ASSETS_DIR, "farmer_mobile_app.png"), 1.2, 1.8, 5.6, 4.7)

    c13_r = add_paper_card(s13, 7.3, 1.5, 5.0, 5.4, bg_color=BG_KRAFT, pin_color="green")
    tf = c13_r.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Serverless Spectral Inference (SSI)"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.color.rgb = COLOR_GREEN
    for item in [
        "Zero App Install: 100% web browser execution in mobile Chrome/Safari.",
        "Zero Egress Cost: Cloudflare R2 stores COG tiles with $0 egress fees.",
        "Edge Inference: Quantized ONNX WASM model executes sub-pixel unmixing directly inside the farmer's browser in <15 milliseconds.",
        "Plain Language Advisories: Translates spectral nitrogen deficit into direct KVK advice: 'Apply 12 kg Urea in Northern plot; skip Southern plot'."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10)
    print("Created Slide 13")

    # SLIDE 14: Comic 1 - Invisible Hunger
    s14 = prs.slides.add_slide(blank)
    apply_cork_background(s14)
    add_header_note(s14, "Operational Scenario 1: 'The Invisible Hunger' (Agriculture)", "3-Panel Field Story: Pre-symptomatic nitrogen deficiency detection saving fertilizer costs", pin_color="green")
    add_paper_card(s14, 1.0, 1.5, 11.3, 5.4, pin_color="green")
    add_picture_safely(s14, os.path.join(ASSETS_DIR, "comic1_invisible_hunger.png"), 1.2, 1.7, 10.9, 4.8)
    print("Created Slide 14")

    # SLIDE 15: Comic 2 - Canal Lifeline
    s15 = prs.slides.add_slide(blank)
    apply_cork_background(s15)
    add_header_note(s15, "Operational Scenario 2: 'The Canal Lifeline' (Hydrology)", "3-Panel Field Story: Spaceborne effluent tracking and automated irrigation canal sluice gate diversion", pin_color="cyan")
    add_paper_card(s15, 1.0, 1.5, 11.3, 5.4, pin_color="cyan")
    add_picture_safely(s15, os.path.join(ASSETS_DIR, "comic2_canal_lifeline.png"), 1.2, 1.7, 10.9, 4.8)
    print("Created Slide 15")

    # SLIDE 16: Comic 3 - 14-Day Drought Warning
    s16 = prs.slides.add_slide(blank)
    apply_cork_background(s16)
    add_header_note(s16, "Operational Scenario 3: 'The 14-Day Moisture Warning' (Climate)", "3-Panel Field Story: Detecting 970nm & 1200nm cellular water thickness depletion 2 weeks before visual wilting", pin_color="yellow")
    add_paper_card(s16, 1.0, 1.5, 11.3, 5.4, pin_color="yellow")
    add_picture_safely(s16, os.path.join(ASSETS_DIR, "comic3_drought_warning.png"), 1.2, 1.7, 10.9, 4.8)
    print("Created Slide 16")

    # SLIDE 17: Comic 4 - Salinity Defense
    s17 = prs.slides.add_slide(blank)
    apply_cork_background(s17)
    add_header_note(s17, "Operational Scenario 4: 'The Salinity Encroachment' (Soil)", "3-Panel Field Story: Subsurface electrical conductivity and clay mineral lattice tracking before salt crusting", pin_color="purple")
    add_paper_card(s17, 1.0, 1.5, 11.3, 5.4, pin_color="purple")
    add_picture_safely(s17, os.path.join(ASSETS_DIR, "comic4_salinity_defense.png"), 1.2, 1.7, 10.9, 4.8)
    print("Created Slide 17")

    # SLIDE 18: Democratization Drop
    s18 = prs.slides.add_slide(blank)
    apply_cork_background(s18)
    add_header_note(s18, "Breaking the Barriers: Compute, Economics & Accessibility", "Democratizing advanced hyperspectral intelligence across computational, economic, and knowledge dimensions", pin_color="cyan")
    add_paper_card(s18, 1.0, 1.5, 11.3, 5.4, pin_color="cyan")
    add_picture_safely(s18, os.path.join(ASSETS_DIR, "democratization_slabs.png"), 1.2, 1.7, 10.9, 4.8)
    print("Created Slide 18")

    # SLIDE 19: Sovereign Vision
    s19 = prs.slides.add_slide(blank)
    apply_cork_background(s19)
    add_header_note(s19, "BharatSpectral: Sovereign Foundation for Indian Earth Observation", "A National Public Good Aligning Science, Artificial Intelligence, and Public Policy", pin_color="purple")
    add_paper_card(s19, 1.0, 1.5, 11.3, 5.4, pin_color="purple")
    add_picture_safely(s19, os.path.join(ASSETS_DIR, "sovereign_vision.png"), 1.2, 1.7, 10.9, 4.8)
    print("Created Slide 19")

    prs.save(OUTPUT_PPTX)
    print(f"Successfully generated 19-slide PPTX deck at: {OUTPUT_PPTX}")

if __name__ == "__main__":
    build_presentation()
