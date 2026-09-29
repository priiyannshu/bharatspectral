#!/usr/bin/env python3
"""
build_deck.py
Constructs the complete 16-Slide Academic Pinboard Presentation in PowerPoint (.pptx)
for BharatSpectral in the exact corkboard pinboard theme:
- Clean slide title in every header note (no secondary text or clutter)
- 4-Speaker Defense Sequence:
    * Speaker 1 (Slides 1-5): Intro, Objectives, Web of Fields, Continuous Spectroscopy, 3D Data Cube
    * Speaker 2 (Slides 6-9): India Coverage, Preprocessing Pipeline, Benchmarking, Need for BharatSpectral
    * Speaker 3 (Slide 10): Project Progression (Phases 1-5 Roadmap)
    * Speaker 4 (Slides 11-16): 4 Operational Scenario Comics, Minimal References, Final Team & Supervisor Thank You
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

SLIDE_WIDTH_IN = 13.333
SLIDE_HEIGHT_IN = 7.5

COLOR_TEXT = RGBColor(42, 35, 27)         # #2A231B Primary dark ink
COLOR_TEXT_DIM = RGBColor(109, 95, 82)    # #6D5F52 Secondary ink
COLOR_CYAN = RGBColor(11, 114, 133)       # #0B7285 Primary accent
COLOR_PURPLE = RGBColor(103, 65, 217)     # #6741D9 Scientific accent
COLOR_ORANGE = RGBColor(217, 72, 15)      # #D9480F Warning / key parameter
COLOR_GREEN = RGBColor(43, 138, 62)       # #2B8A3E Suitable / success
COLOR_RED = RGBColor(201, 42, 42)         # #C92A2A Hazard / drop
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

def add_header_note(slide, title_text, tape=True, pin_color="cyan"):
    """
    Renders a clean pinned header note containing ONLY the clean slide title.
    No secondary subtext or clutter per user requirements.
    """
    header_w = Inches(11.2)
    header_h = Inches(0.68)
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
    tf.margin_top = Inches(0.12)
    tf.margin_bottom = Inches(0.08)

    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Trebuchet MS"
    p.font.size = Pt(16.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    if tape and os.path.exists(TAPE_STRIP):
        slide.shapes.add_picture(TAPE_STRIP, Inches((SLIDE_WIDTH_IN - 1.8) / 2), Inches(0.18), Inches(1.8), Inches(0.36))

    pin_path = {"cyan": PIN_CYAN, "yellow": PIN_YELLOW, "red": PIN_RED, "green": PIN_GREEN, "purple": PIN_PURPLE}.get(pin_color, PIN_CYAN)
    if os.path.exists(pin_path):
        slide.shapes.add_picture(pin_path, header_x + Inches(0.25), header_y - Inches(0.14), Inches(0.38), Inches(0.38))
        slide.shapes.add_picture(pin_path, header_x + header_w - Inches(0.63), header_y - Inches(0.14), Inches(0.38), Inches(0.38))

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

def add_picture_safely(slide, img_path, x_in, y_in, w_in, h_in, keep_aspect=True):
    if not os.path.exists(img_path):
        return None
    if not keep_aspect:
        return slide.shapes.add_picture(img_path, Inches(x_in), Inches(y_in), Inches(w_in), Inches(h_in))
    try:
        with Image.open(img_path) as im:
            img_w, img_h = im.size
        ar = img_w / img_h
        box_ar = w_in / h_in
        if box_ar > ar:
            actual_h = h_in
            actual_w = h_in * ar
            actual_x = x_in + (w_in - actual_w) / 2
            actual_y = y_in
        else:
            actual_w = w_in
            actual_h = w_in / ar
            actual_x = x_in
            actual_y = y_in + (h_in - actual_h) / 2
        return slide.shapes.add_picture(img_path, Inches(actual_x), Inches(actual_y), Inches(actual_w), Inches(actual_h))
    except Exception:
        return slide.shapes.add_picture(img_path, Inches(x_in), Inches(y_in), Inches(w_in), Inches(h_in))

def build_presentation():
    prs, blank = create_deck()
    print("Building clean 16-Slide Academic Pinboard Presentation...")

    # =========================================================================
    # SPEAKER 1: SLIDES 1 to 5
    # =========================================================================

    # SLIDE 1: Beyond Human Sight (Intro)
    s1 = prs.slides.add_slide(blank)
    apply_cork_background(s1)
    
    title_card = add_paper_card(s1, 2.2, 0.28, 8.93, 0.65, bg_color=BG_PARCHMENT, pin_color="cyan", tape=True)
    tf1 = title_card.text_frame
    tf1.word_wrap = False
    tf1.margin_left = Inches(0.1)
    tf1.margin_right = Inches(0.1)
    tf1.margin_top = Inches(0.08)
    tf1.margin_bottom = Inches(0.08)
    p = tf1.paragraphs[0]
    p.text = "BharatSpectral: Democratized Spectral-Semantic Intelligence"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Trebuchet MS"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN

    polaroids_data = [
        ("hero_satellite_earth.png", 0.6, 1.25, 2.85, 2.55),
        ("photon_pinball_cube.png", 2.95, 3.85, 3.0, 2.7),
        ("continuous_spectroscopy.png", 5.25, 1.15, 3.0, 2.65),
        ("india_hsi_coverage.png", 7.5, 3.9, 3.0, 2.7),
        ("spectrum_contrast.png", 9.8, 1.3, 2.85, 2.55),
    ]
    
    for img_name, px, py, pw, ph in polaroids_data:
        add_paper_card(s1, px, py, pw, ph, bg_color=RGBColor(255, 255, 255), pin_color="red")
        img_p = os.path.join(ASSETS_DIR, img_name)
        if os.path.exists(img_p):
            add_picture_safely(s1, img_p, px + 0.12, py + 0.14, pw - 0.24, ph - 0.32, keep_aspect=False)

    s1.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 1 - SPEAKER 1):\n"
        "Good morning, respected committee members and faculty.\n\n"
        "We are creating a system that understands the physical language of radiative transfer and optical physics "
        "beyond human visual capabilities. As human beings, our vision is confined to a razor-thin 300-nanometer slice "
        "of visible light: Red, Green, and Blue. What we cannot see, we cannot diagnose.\n\n"
        "Every day, 140 million Indian smallholders look at their crops through these limited RGB eyes. But nature does not speak in RGB. "
        "The true biochemical language of Earth — cellular water stress, nitrogen deficiency, leaf carotenoids, and soil sodicity — "
        "is written across 400 to 2,500 nanometers of continuous reflected solar radiation.\n\n"
        "This project bridges that perceptual chasm. This is BharatSpectral: Democratized Spectral-Semantic Intelligence (DSSI)."
    )
    print("Created Slide 1 (Beyond Human Sight)")

    # SLIDE 2: Project Objectives
    s2 = prs.slides.add_slide(blank)
    apply_cork_background(s2)
    add_header_note(s2, "Project Objectives", pin_color="cyan")

    card_x, card_y, card_w, card_h = 1.0, 1.15, 11.33, 5.85
    c_main = add_paper_card(s2, card_x, card_y, card_w, card_h, bg_color=BG_PARCHMENT, border_color=BORDER_CARD)

    for pin_img, px, py in [
        (PIN_CYAN, card_x + 0.15, card_y + 0.15),
        (PIN_YELLOW, card_x + card_w - 0.53, card_y + 0.15),
        (PIN_GREEN, card_x + 0.15, card_y + card_h - 0.53),
        (PIN_PURPLE, card_x + card_w - 0.53, card_y + card_h - 0.53),
    ]:
        if os.path.exists(pin_img):
            s2.shapes.add_picture(pin_img, Inches(px), Inches(py), Inches(0.38), Inches(0.38))

    tf = c_main.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.45)
    tf.margin_right = Inches(0.45)
    tf.margin_top = Inches(0.35)
    tf.margin_bottom = Inches(0.35)

    bullets = [
        ("Data Acquisition & Benchmark Creation: ", "Ingest heterogeneous hyperspectral cubes across AVIRIS-NG India (425 bands), ISRO HysIS (220 bands), and NASA EMIT (285 bands) to construct BharatHSI-Bench — India's first open, labeled smallholder agricultural benchmark dataset with standardized evaluation protocols.", COLOR_CYAN),
        ("Empirical Failure Proof: ", "Rigorously evaluate global Foundation Models (SpectralGPT, HyperSIGMA) and baseline architectures directly on BharatHSI-Bench, quantifying severe domain-shift degradation (15%–30% Overall Accuracy drop) over fragmented Indian plots.", COLOR_ORANGE),
        ("Physics-Informed Foundation Model: ", "Design BharatSpectral-MAE, introducing seven named architectural innovations (Scale-Spectral Positional Encoding, Atmospheric Absorption Masking, Reflectance-Normalized Loss) to achieve state-of-the-art representations under Indian agricultural conditions.", COLOR_PURPLE),
        ("Multi-Domain Biochemical Adaptation: ", "Fine-tune foundation representations for downstream diagnostic tasks including nitrogen deficit mapping, soil organic carbon estimation, inland water chlorophyll-a monitoring, and soil salinity/sodicity defense.", COLOR_GREEN),
        ("Democratized Public Delivery: ", "Deploy an open, zero-cost WebGIS platform with sub-second Serverless Spectral Inference (SSI) via Cloudflare Workers and ONNX edge runtime, translating complex spectral tensors into direct vernacular farmer advisories.", COLOR_RED),
    ]

    p_first = tf.paragraphs[0]
    p_first.text = "1. " + bullets[0][0]
    p_first.font.bold = True
    p_first.font.size = Pt(11)
    p_first.font.color.rgb = bullets[0][2]
    r1 = p_first.add_run()
    r1.text = bullets[0][1]
    r1.font.bold = False
    r1.font.color.rgb = COLOR_TEXT

    for idx, (head, body, col) in enumerate(bullets[1:], start=2):
        p = tf.add_paragraph()
        p.space_before = Pt(10)
        p.text = f"{idx}. " + head
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = col
        r = p.add_run()
        r.text = body
        r.font.bold = False
        r.font.color.rgb = COLOR_TEXT

    s2.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 2 - SPEAKER 1):\n"
        "To systematically address this grand challenge, our capstone is structured around five concrete, testable objectives.\n\n"
        "First, Data Acquisition & Benchmark Creation: We curate BharatHSI-Bench across AVIRIS-NG India, ISRO HysIS, and NASA EMIT.\n"
        "Second, Empirical Failure Proof: We demonstrate why existing models fail when transferred to Indian landscapes.\n"
        "Third, Physics-Informed Foundation Model: We build BharatSpectral-MAE, incorporating optical physics into self-supervised learning.\n"
        "Fourth, Multi-Domain Biochemical Adaptation: We fine-tune representations for agricultural, water, and soil diagnostics.\n"
        "Fifth, Democratized Public Delivery: We engineer a zero-cost edge WebGIS providing actionable vernacular advisories."
    )
    print("Created Slide 2 (Project Objectives)")

    # SLIDE 3: The Web of Fields
    s3 = prs.slides.add_slide(blank)
    apply_cork_background(s3)
    add_header_note(s3, "The Web of Fields: Multi-Disciplinary Convergence", pin_color="cyan")

    card_x, card_y, card_w, card_h = 1.0, 1.15, 11.33, 5.85
    c_venn = add_paper_card(s3, card_x, card_y, card_w, card_h, bg_color=BG_PARCHMENT, border_color=BORDER_CARD)

    for pin_img, px, py in [
        (PIN_CYAN, card_x + 0.15, card_y + 0.15),
        (PIN_YELLOW, card_x + card_w - 0.53, card_y + 0.15),
        (PIN_GREEN, card_x + 0.15, card_y + card_h - 0.53),
        (PIN_PURPLE, card_x + card_w - 0.53, card_y + card_h - 0.53),
    ]:
        if os.path.exists(pin_img):
            s3.shapes.add_picture(pin_img, Inches(px), Inches(py), Inches(0.38), Inches(0.38))

    venn_img = os.path.join(ASSETS_DIR, "venn_diagram.png")
    if not os.path.exists(venn_img):
        venn_img = os.path.join(ASSETS_DIR, "venn_diagram.jpg")
    add_picture_safely(s3, venn_img, card_x + 0.35, card_y + 0.35, card_w - 0.70, card_h - 0.70)

    s3.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 3 - SPEAKER 1):\n"
        "Respected committee members, true scientific breakthroughs cannot occur within the isolated silos of a single academic department.\n\n"
        "BharatSpectral sits at the confluence of seven distinct fields: Atmospheric Physics, Plant Physiology, Optical Spectroscopy, "
        "Self-Supervised Transformers, Cloudflare Edge Infrastructure, Smallholder Agronomy, and Public Policy.\n\n"
        "By merging these fields, we create a system that is physically grounded and practically deployable."
    )
    print("Created Slide 3 (The Web of Fields)")

    # SLIDE 4: Continuous Spectroscopy
    s4 = prs.slides.add_slide(blank)
    apply_cork_background(s4)
    add_header_note(s4, "Continuous Spectroscopy: The Chemical Barcode", pin_color="green")

    add_paper_card(s4, 1.0, 1.15, 6.2, 5.85, pin_color="green")
    add_picture_safely(s4, os.path.join(ASSETS_DIR, "continuous_spectroscopy.png"), 1.2, 1.45, 5.8, 5.25)

    c4_r = add_paper_card(s4, 7.5, 1.15, 4.8, 5.85, bg_color=BG_KRAFT, pin_color="yellow")
    tf = c4_r.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Diagnostic Absorption Physics"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.color.rgb = COLOR_CYAN
    for item in [
        "Narrow-Band Continuity: 425 contiguous 5nm bands capture narrow chemical absorption doublets invisible to 10-band multispectral sensors.",
        "Chlorophyll Red-Edge (680–740nm): Slope inflection accurately isolates plant vigor from background soil reflectance.",
        "Cellular Water Absorption (970nm & 1200nm): Quantifies canopy equivalent water thickness before visual wilting occurs.",
        "Protein & Nitrogen (2100–2300nm): Direct molecular absorption bonds (C-H, N-H) enable precise leaf nitrogen profiling."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10)
        p.space_before = Pt(6)

    s4.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 4 - SPEAKER 1):\n"
        "Slide 4 demonstrates the physical difference between standard multispectral imaging and continuous hyperspectral spectroscopy.\n\n"
        "Multispectral sensors like Sentinel-2 capture only 10 broad spectral bands. They can register that a crop is stressed, but cannot diagnose why.\n\n"
        "Hyperspectral sensors record 425 continuous 5-nanometer channels. This allows us to detect subtle biochemical signatures like the Chlorophyll "
        "Red-Edge, cellular moisture absorption at 970nm, and leaf nitrogen at 2200nm."
    )
    print("Created Slide 4 (Continuous Spectroscopy)")

    # SLIDE 5: Hyperspectral Data Cube & Radiative Transfer
    s5 = prs.slides.add_slide(blank)
    apply_cork_background(s5)
    add_header_note(s5, "Hyperspectral Data Cube & Canopy Radiative Transfer", pin_color="purple")

    add_paper_card(s5, 1.0, 1.15, 6.2, 5.85, pin_color="purple")
    add_picture_safely(s5, os.path.join(ASSETS_DIR, "photon_pinball_cube.png"), 1.2, 1.45, 5.8, 5.25)

    c5_r = add_paper_card(s5, 7.5, 1.15, 4.8, 5.85, bg_color=BG_KRAFT, pin_color="yellow")
    tf = c5_r.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Canopy Radiative Transfer Breakdown"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.color.rgb = COLOR_ORANGE
    for item in [
        "Multi-Bounce Scattering: Sunlight enters intercropped canopies and ricochets between leaves and soil before sensor reception.",
        "Failure of Linear Unmixing: Classical GIS tools (LSU/FCLS) assume linear mixing, leading to severe error (RMSE > 0.15) in multi-tier crops.",
        "3D Data Cube Structure: Two spatial dimensions (X, Y) and one dense spectral dimension (lambda) capture continuous physical interactions.",
        "Physics-Informed Modeling: Incorporating radiative transfer physics ensures our model decodes non-linear mixture dynamics."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10)
        p.space_before = Pt(6)

    s5.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 5 - SPEAKER 1):\n"
        "When solar photons enter a crop canopy, they undergo complex multi-bounce volumetric scattering between leaves, soil, and moisture droplets.\n\n"
        "The resulting 3D Hyperspectral Data Cube captures two spatial dimensions and one dense spectral dimension. Every pixel represents a continuous "
        "physical spectrum governed by radiative transfer, establishing the foundation for our deep learning pipeline.\n\n"
        "I now hand over to Speaker 2 to discuss our data sources and empirical benchmarks."
    )
    print("Created Slide 5 (Hyperspectral Data Cube & Radiative Transfer)")

    # =========================================================================
    # SPEAKER 2: SLIDES 6 to 9
    # =========================================================================

    # SLIDE 6: Indian Landmass Hyperspectral Coverage
    s6 = prs.slides.add_slide(blank)
    apply_cork_background(s6)
    add_header_note(s6, "Indian Landmass Hyperspectral Coverage", pin_color="green")

    add_paper_card(s6, 1.0, 1.15, 6.2, 5.85, pin_color="green")
    add_picture_safely(s6, os.path.join(ASSETS_DIR, "india_hsi_coverage.png"), 1.2, 1.45, 5.8, 5.25)

    c6_r = add_paper_card(s6, 7.5, 1.15, 4.8, 5.85, bg_color=BG_KRAFT, pin_color="cyan")
    tf = c6_r.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Sensor Heterogeneity & Coverage"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(13)
    tf.paragraphs[0].font.color.rgb = COLOR_CYAN
    for item in [
        "AVIRIS-NG India (Airborne): 425 spectral channels (380–2510nm) at 4–8m GSD across key agro-ecological zones (Punjab, Gujarat, Andhra Pradesh).",
        "NASA EMIT (ISS Spaceborne): 285 spectral channels (381–2493nm) at 60m GSD providing regional mineral and canopy observations.",
        "ISRO HysIS (Orbital Satellite): 220 spectral channels across VNIR/SWIR providing national continuous monitoring.",
        "Resolution Harmonization: Requires specialized handling to bridge Ground Sample Distances from 4m airborne to 60m orbital scales."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(10)
        p.space_before = Pt(6)

    s6.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 6 - SPEAKER 2):\n"
        "Thank you. Respected committee members, our research is anchored directly on real hyperspectral missions covering India.\n\n"
        "We leverage AVIRIS-NG India, flown collaboratively by ISRO and NASA with 425 spectral bands at high spatial resolution; "
        "NASA EMIT aboard the International Space Station with 285 channels; and ISRO's HysIS satellite with 220 bands.\n\n"
        "Harmonizing these disparate datasets requires robust preprocessing, as shown in our next slide."
    )
    print("Created Slide 6 (Indian Landmass Coverage)")

    # SLIDE 7: Automated Preprocessing Pipeline
    s7 = prs.slides.add_slide(blank)
    apply_cork_background(s7)
    add_header_note(s7, "Automated Preprocessing Pipeline", pin_color="cyan")

    add_paper_card(s7, 1.0, 1.15, 11.33, 5.85, pin_color="cyan")
    add_picture_safely(s7, os.path.join(ASSETS_DIR, "preprocessing_pipeline.png"), 1.2, 1.35, 10.9, 5.45)

    s7.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 7 - SPEAKER 2):\n"
        "Raw hyperspectral data straight from orbit contains atmospheric distortions, water vapor gaps, and noise.\n\n"
        "Our automated preprocessing assembly line processes raw flight lines through five standardized stages: "
        "radiometric calibration, atmospheric correction, bad-band removal around moisture absorption windows, "
        "spatial tiling tailored to smallholder plot scales, and tensor packing.\n\n"
        "This clean, standardized data forms the foundation of our benchmark evaluation."
    )
    print("Created Slide 7 (Automated Preprocessing Pipeline)")

    # SLIDE 8: Empirical Baseline Benchmarking & Failure Modes
    s8 = prs.slides.add_slide(blank)
    apply_cork_background(s8)
    add_header_note(s8, "Empirical Baseline Benchmarking & Failure Modes", pin_color="red")

    add_paper_card(s8, 1.0, 1.15, 5.8, 5.85, pin_color="red")
    add_picture_safely(s8, os.path.join(REPO_ROOT, "outputs/figures/domain_shift_collapse.png"), 1.2, 1.45, 5.4, 5.25)

    c8_r = add_paper_card(s8, 7.1, 1.15, 5.23, 5.85, bg_color=BG_KRAFT, pin_color="yellow")
    tf = c8_r.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Empirical Benchmark Results (Testbed Evaluation)"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(12.5)
    tf.paragraphs[0].font.color.rgb = COLOR_RED

    bench_data = [
        ("Random Forest (100 Trees)", "85.4%", "57.8%", "-27.6%"),
        ("SVM (RBF Kernel)", "84.6%", "62.2%", "-22.4%"),
        ("3D-CNN (Hamida et al.)", "90.8%", "56.4%", "-34.4%"),
        ("HybridSN (3D-2D CNN)", "92.4%", "55.1%", "-37.3%"),
        ("Spectral Transformer", "93.5%", "60.8%", "-32.7%"),
        ("SpectralGPT (Hong et al.)", "93.5%", "61.5%", "-32.0%"),
        ("HyperSIGMA (Wang et al.)", "93.8%", "64.2%", "-29.6%"),
    ]

    for model, base_oa, shift_oa, drop in bench_data:
        p = tf.add_paragraph()
        p.text = f"• {model}: {base_oa} → {shift_oa} (Drop: {drop})"
        p.font.size = Pt(10)
        p.space_before = Pt(4)

    p_sum = tf.add_paragraph()
    p_sum.space_before = Pt(12)
    p_sum.text = "Key Finding: Standard AI models suffer a 22%–37% accuracy collapse when transferred to fragmented Indian smallholder plots."
    p_sum.font.bold = True
    p_sum.font.size = Pt(10.5)
    p_sum.font.color.rgb = COLOR_ORANGE

    s8.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 8 - SPEAKER 2):\n"
        "Can existing AI models be applied directly to Indian agricultural remote sensing? Our empirical evaluation proves they cannot.\n\n"
        "When evaluated on our testbed, leading architectures — from Random Forests and 3D-CNNs to modern Vision Transformers like SpectralGPT — "
        "suffer a severe collapse of 22% to 37% in Overall Accuracy.\n\n"
        "These models were benchmarked on homogeneous Western monoculture fields. On fragmented Indian smallholder farms, they fail."
    )
    print("Created Slide 8 (Empirical Baseline Benchmarking)")

    # SLIDE 9: The Need for BharatSpectral (Loosely Pinned Notes)
    s9 = prs.slides.add_slide(blank)
    apply_cork_background(s9)
    add_header_note(s9, "The Need for BharatSpectral", pin_color="yellow")

    notes_spec = [
        (1.0, 1.15, 5.4, 2.75, BG_PARCHMENT, "cyan", "🌾 Sub-Pixel Spatial Fragmentation", [
            "Indian smallholdings average 0.5 to 2.0 hectares with multi-crop intercropping.",
            "Western models trained on 40-hectare monocultures blur plot boundaries and collapse on mixed pixels.",
            "Requires foundation representations explicitly conditioned on mixture entropy."
        ]),
        (6.9, 1.15, 5.4, 2.75, BG_KRAFT, "green", "🛰️ Multi-Sensor Heterogeneity", [
            "Indian EO relies on 425-band AVIRIS-NG, 285-band EMIT, and 220-band HysIS.",
            "Ground Sample Distances vary widely from 4m airborne to 60m satellite imagery.",
            "Demands a sensor-agnostic tokenizer rather than fixed single-sensor architectures."
        ]),
        (1.0, 4.25, 5.4, 2.75, BG_KRAFT, "purple", "🔬 Subtle Biochemical Absorption", [
            "Critical features (nitrogen at 2.2μm, soil carbon, moisture) exhibit < 5% reflectance.",
            "Standard MSE loss functions overlook subtle diagnostic dips in favor of bright soil.",
            "Requires reflectance-normalized loss formulations to preserve diagnostic depth."
        ]),
        (6.9, 4.25, 5.4, 2.75, BG_PARCHMENT, "yellow", "🌐 Democratized Edge Accessibility", [
            "Hyperspectral analytics are currently locked behind $10,000/seat desktop GIS licenses.",
            "Smallholder farmers require zero-cost, sub-second browser inference (SSI).",
            "Bridges the gap between research models and direct vernacular advisories."
        ]),
    ]

    for nx, ny, nw, nh, bg, pin_col, n_title, n_bullets in notes_spec:
        nc = add_paper_card(s9, nx, ny, nw, nh, bg_color=bg, pin_color=pin_col)
        ntf = nc.text_frame
        ntf.word_wrap = True
        ntf.margin_left = Inches(0.2)
        ntf.margin_right = Inches(0.2)
        ntf.margin_top = Inches(0.18)
        
        p0 = ntf.paragraphs[0]
        p0.text = n_title
        p0.font.bold = True
        p0.font.size = Pt(12)
        p0.font.color.rgb = COLOR_CYAN if pin_col in ["cyan", "green"] else COLOR_PURPLE

        for b in n_bullets:
            pb = ntf.add_paragraph()
            pb.text = "• " + b
            pb.font.size = Pt(9.5)
            pb.space_before = Pt(3)

    s9.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 9 - SPEAKER 2):\n"
        "Why do we specifically need BharatSpectral? These four pinned requirements capture the core justification:\n\n"
        "1. Sub-Pixel Fragmentation: Addressing smallholder plot mixing that breaks Western monoculture assumptions.\n"
        "2. Multi-Sensor Heterogeneity: Unifying AVIRIS-NG, EMIT, and HysIS into a shared physical embedding space.\n"
        "3. Subtle Biochemical Absorption: Preserving faint chemical signals in the shortwave infrared.\n"
        "4. Democratized Accessibility: Replacing prohibitive desktop software with zero-cost edge inference for farmers.\n\n"
        "To outline our technical roadmap across all project phases, I hand over to Speaker 3."
    )
    print("Created Slide 9 (The Need for BharatSpectral)")

    # =========================================================================
    # SPEAKER 3: SLIDE 10
    # =========================================================================

    # SLIDE 10: Project Progression: Phases 1 to 5
    s10 = prs.slides.add_slide(blank)
    apply_cork_background(s10)
    add_header_note(s10, "Project Progression: Phases 1 to 5", pin_color="cyan")

    add_paper_card(s10, 1.0, 1.15, 11.33, 5.85, pin_color="cyan")
    add_picture_safely(s10, os.path.join(ASSETS_DIR, "project_timeline.png"), 1.2, 1.35, 10.9, 5.45)

    s10.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 10 - SPEAKER 3):\n"
        "Respected committee members, our project execution spans five progressive phases.\n\n"
        "For our mid-term milestone, we have completed Phase 1: Data Acquisition & Preprocessing, assembling clean standardized datasets; "
        "and Phase 2: Baseline Benchmarking, demonstrating the 22% to 37% accuracy collapse across classical and deep learning models.\n\n"
        "Looking forward, Phase 3 will engineer BharatSpectral-MAE, incorporating our physics-informed tokenization and loss formulations; "
        "Phase 4 adapts representations across biochemical and stress downstream tasks; and Phase 5 deploys our zero-cost edge WebGIS infrastructure.\n\n"
        "I will now pass to Speaker 4 to demonstrate our operational use cases and conclude the presentation."
    )
    print("Created Slide 10 (Project Progression)")

    # =========================================================================
    # SPEAKER 4: SLIDES 11 to 16
    # =========================================================================

    # SLIDE 11: Comic 1 - The Invisible Hunger
    s11 = prs.slides.add_slide(blank)
    apply_cork_background(s11)
    add_header_note(s11, "Operational Scenario 1: The Invisible Hunger", pin_color="green")
    add_paper_card(s11, 1.0, 1.15, 11.33, 5.85, pin_color="green")
    add_picture_safely(s11, os.path.join(ASSETS_DIR, "comic1_invisible_hunger.png"), 1.2, 1.35, 10.9, 5.45)

    s11.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 11 - SPEAKER 4):\n"
        "Thank you. To illustrate the tangible real-world impact of BharatSpectral, we present four operational field scenarios.\n\n"
        "Scenario 1 addresses 'The Invisible Hunger' — sub-visual crop nitrogen deficiency. Under standard RGB or multispectral satellite imaging, "
        "crops appear healthy green until cellular damage has already occurred.\n\n"
        "BharatSpectral analyzes diagnostic absorption dips at 2.1 to 2.3 microns, detecting nitrogen deficits two weeks earlier and generating "
        "precise micro-dosing advisories that save fertilizer costs and preserve yields."
    )
    print("Created Slide 11 (Comic 1 - The Invisible Hunger)")

    # SLIDE 12: Comic 2 - The Canal Lifeline
    s12 = prs.slides.add_slide(blank)
    apply_cork_background(s12)
    add_header_note(s12, "Operational Scenario 2: The Canal Lifeline", pin_color="cyan")
    add_paper_card(s12, 1.0, 1.15, 11.33, 5.85, pin_color="cyan")
    add_picture_safely(s12, os.path.join(ASSETS_DIR, "comic2_canal_lifeline.png"), 1.2, 1.35, 10.9, 5.45)

    s12.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 12 - SPEAKER 4):\n"
        "Scenario 2 addresses agricultural canal contamination and toxic algal blooms.\n\n"
        "Agricultural canals are vital lifelines across rural India, but run-off from chemical fertilizers triggers dangerous cyanobacteria blooms.\n\n"
        "By tracking phycocyanin absorption features at 620nm and unmixing industrial effluents from suspended sediments, BharatSpectral detects "
        "water toxicity before irrigation water reaches sensitive crop fields."
    )
    print("Created Slide 12 (Comic 2 - The Canal Lifeline)")

    # SLIDE 13: Comic 3 - 14-Day Drought Warning
    s13 = prs.slides.add_slide(blank)
    apply_cork_background(s13)
    add_header_note(s13, "Operational Scenario 3: 14-Day Drought Warning", pin_color="yellow")
    add_paper_card(s13, 1.0, 1.15, 11.33, 5.85, pin_color="yellow")
    add_picture_safely(s13, os.path.join(ASSETS_DIR, "comic3_drought_warning.png"), 1.2, 1.35, 10.9, 5.45)

    s13.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 13 - SPEAKER 4):\n"
        "Scenario 3 showcases pre-symptomatic moisture stress detection.\n\n"
        "When drought strikes, plant cell walls dehydrate long before leaves turn yellow or curl. Conventional satellites provide warnings only "
        "after visual wilting sets in.\n\n"
        "BharatSpectral tracks Equivalent Water Thickness across the 970nm and 1200nm water absorption windows, delivering 14-day advance warnings "
        "that allow farmers to schedule protective irrigation before yield loss becomes irreversible."
    )
    print("Created Slide 13 (Comic 3 - 14-Day Drought Warning)")

    # SLIDE 14: Comic 4 - Salinity Encroachment
    s14 = prs.slides.add_slide(blank)
    apply_cork_background(s14)
    add_header_note(s14, "Operational Scenario 4: Salinity Encroachment", pin_color="purple")
    add_paper_card(s14, 1.0, 1.15, 11.33, 5.85, pin_color="purple")
    add_picture_safely(s14, os.path.join(ASSETS_DIR, "comic4_salinity_defense.png"), 1.2, 1.35, 10.9, 5.45)

    s14.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 14 - SPEAKER 4):\n"
        "Scenario 4 focuses on soil salinity and sodicity reclamation.\n\n"
        "In irrigated canal tracts across northern and western India, secondary salinization silently degrades soil fertility. Surface visual checks "
        "cannot distinguish harmless white crusting from destructive soil sodicity.\n\n"
        "Using diagnostic shortwave infrared hydroxyl and carbonate absorption signatures, BharatSpectral maps subsurface soil health, directing "
        "targeted gypsum soil remediation before land degradation becomes permanent."
    )
    print("Created Slide 14 (Comic 4 - Salinity Encroachment)")

    # SLIDE 15: Key Literature References (Minimal Clean Slide)
    s15 = prs.slides.add_slide(blank)
    apply_cork_background(s15)
    add_header_note(s15, "Key Literature References", pin_color="cyan")

    # Two Clean Parchment Cards for Literature
    c15_l = add_paper_card(s15, 1.0, 1.15, 5.45, 5.85, bg_color=BG_PARCHMENT, pin_color="cyan")
    tf_l = c15_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.3)
    tf_l.margin_right = Inches(0.3)
    tf_l.margin_top = Inches(0.25)
    
    p = tf_l.paragraphs[0]
    p.text = "Foundational Hyperspectral Transformers"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_CYAN

    refs_left = [
        ("SpectralGPT: Spectral Foundation Model", "Hong, D., Zhang, B., Li, X., Chanussot, J., & Zhu, X. X. (2024).", "IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), 46(8), 5412–5427."),
        ("SS-MAE: Spectral-Spatial Masked Autoencoder", "Lin, Y., Gao, L., Zheng, X., & Zhang, B. (2024).", "IEEE Transactions on Geoscience and Remote Sensing (TGRS), 62, 1–14."),
        ("HyperSIGMA: Scalable Foundation Model for Remote Sensing", "Wang, X., Zhang, L., & Chanussot, J. (2024).", "IEEE Transactions on Geoscience and Remote Sensing (TGRS), 62, 1–16.")
    ]

    for title, authors, venue in refs_left:
        p1 = tf_l.add_paragraph()
        p1.space_before = Pt(12)
        p1.text = "• " + title
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = COLOR_PURPLE

        p2 = tf_l.add_paragraph()
        p2.text = "   " + authors
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_TEXT

        p3 = tf_l.add_paragraph()
        p3.text = "   " + venue
        p3.font.italic = True
        p3.font.size = Pt(9)
        p3.font.color.rgb = COLOR_TEXT_DIM

    c15_r = add_paper_card(s15, 6.85, 1.15, 5.48, 5.85, bg_color=BG_KRAFT, pin_color="yellow")
    tf_r = c15_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = Inches(0.3)
    tf_r.margin_right = Inches(0.3)
    tf_r.margin_top = Inches(0.25)

    p_r = tf_r.paragraphs[0]
    p_r.text = "Scale Invariance & Spectroscopic Unmixing"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = COLOR_ORANGE

    refs_right = [
        ("Scale-MAE: High-Resolution Masked Autoencoders", "Reed, C. J., Metzger, R., Srinivas, A., Darrell, T., & Keutzer, K. (2023).", "IEEE/CVF Conference on Computer Vision and Pattern Recognition (ICCV), 14288–14299."),
        ("HybridSN: 3D-2D CNN Feature Hierarchy for HSI", "Roy, S. K., Krishna, G., Dubey, S. R., & Chaudhuri, B. B. (2020).", "IEEE Geoscience and Remote Sensing Letters (GRSL), 17(8), 1352–1356."),
        ("Spectral Unmixing: Algorithms & Physical Principles", "Keshava, N., & Mustard, J. F. (2002).", "IEEE Signal Processing Magazine, 19(1), 44–57.")
    ]

    for title, authors, venue in refs_right:
        p1 = tf_r.add_paragraph()
        p1.space_before = Pt(12)
        p1.text = "• " + title
        p1.font.bold = True
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = COLOR_GREEN

        p2 = tf_r.add_paragraph()
        p2.text = "   " + authors
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_TEXT

        p3 = tf_r.add_paragraph()
        p3.text = "   " + venue
        p3.font.italic = True
        p3.font.size = Pt(9)
        p3.font.color.rgb = COLOR_TEXT_DIM

    s15.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 15 - SPEAKER 4):\n"
        "Our research builds upon foundational literature across hyperspectral Vision Transformers and spectroscopic unmixing.\n\n"
        "We ground our self-supervised learning on SpectralGPT, SS-MAE, and HyperSIGMA, while adapting scale-aware principles from Scale-MAE "
        "and physical unmixing constraints from Keshava & Mustard.\n\n"
        "These peer-reviewed foundations provide the theoretical rigor underlying our architecture."
    )
    print("Created Slide 15 (Key Literature References)")

    # SLIDE 16: Project Team, Supervision & Thank You (Final Slide)
    s16 = prs.slides.add_slide(blank)
    apply_cork_background(s16)
    add_header_note(s16, "BharatSpectral: Democratized Spectral Intelligence", pin_color="cyan")

    # Center Top Thank You Art Image
    thank_you_img = os.path.join(ASSETS_DIR, "thank_you_art.png")
    add_picture_safely(s16, thank_you_img, 2.0, 1.15, 9.33, 2.3)

    # Left Pinned Card: Team Members
    c16_l = add_paper_card(s16, 1.0, 3.65, 5.45, 3.35, bg_color=BG_PARCHMENT, pin_color="cyan")
    tf_l = c16_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.3)
    tf_l.margin_right = Inches(0.3)
    tf_l.margin_top = Inches(0.2)
    
    p = tf_l.paragraphs[0]
    p.text = "Project Research Team"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_CYAN

    team_members = [
        ("Priyanshu", "Lead Researcher & System Architect"),
        ("Team Member 2", "Machine Learning & Preprocessing Pipeline"),
        ("Team Member 3", "Radiative Physics & Empirical Benchmarking"),
        ("Team Member 4", "Geospatial Edge WebGIS & Evaluation")
    ]

    for name, role in team_members:
        p_name = tf_l.add_paragraph()
        p_name.space_before = Pt(4)
        p_name.text = f"• {name}"
        p_name.font.bold = True
        p_name.font.size = Pt(10)
        p_name.font.color.rgb = COLOR_TEXT
        
        p_role = tf_l.add_paragraph()
        p_role.text = f"   {role}"
        p_role.font.size = Pt(8.5)
        p_role.font.color.rgb = COLOR_TEXT_DIM

    # Right Pinned Card: Supervision & Institution
    c16_r = add_paper_card(s16, 6.85, 3.65, 5.48, 3.35, bg_color=BG_KRAFT, pin_color="purple")
    tf_r = c16_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = Inches(0.3)
    tf_r.margin_right = Inches(0.3)
    tf_r.margin_top = Inches(0.2)

    p_r = tf_r.paragraphs[0]
    p_r.text = "Project Guidance & Supervision"
    p_r.font.bold = True
    p_r.font.size = Pt(13)
    p_r.font.color.rgb = COLOR_PURPLE

    p_g1 = tf_r.add_paragraph()
    p_g1.space_before = Pt(8)
    p_g1.text = "Under the Esteemed Guidance of:"
    p_g1.font.size = Pt(9.5)
    p_g1.font.color.rgb = COLOR_TEXT_DIM

    p_g2 = tf_r.add_paragraph()
    p_g2.text = "Dr. / Prof. [Project Supervisor Name]"
    p_g2.font.bold = True
    p_g2.font.size = Pt(12)
    p_g2.font.color.rgb = COLOR_CYAN

    p_g3 = tf_r.add_paragraph()
    p_g3.text = "Department of Computer Science & Engineering"
    p_g3.font.size = Pt(9.5)
    p_g3.font.color.rgb = COLOR_TEXT

    p_g4 = tf_r.add_paragraph()
    p_g4.space_before = Pt(10)
    p_g4.text = "Open-Source DSSI Initiative • Built for Indian Earth Observation"
    p_g4.font.bold = True
    p_g4.font.size = Pt(9.5)
    p_g4.font.color.rgb = COLOR_GREEN

    p_g5 = tf_r.add_paragraph()
    p_g5.text = "Open for Committee Review & Defense Discussion"
    p_g5.font.italic = True
    p_g5.font.size = Pt(9)
    p_g5.font.color.rgb = COLOR_TEXT_DIM

    s16.notes_slide.notes_text_frame.text = (
        "PRESENTER SCRIPT (SLIDE 16 - SPEAKER 4):\n"
        "On behalf of our entire capstone team — Priyanshu and our fellow researchers — and with sincere gratitude to our project supervisor, "
        "we thank the respected evaluation committee and faculty members for your time and guidance.\n\n"
        "BharatSpectral represents our commitment to democratizing advanced spectral intelligence for Indian agriculture, ecology, and public science.\n\n"
        "We now welcome your questions, feedback, and discussion."
    )
    print("Created Slide 16 (Project Team, Supervision & Thank You)")

    # Save PPTX
    prs.save(OUTPUT_PPTX)
    print(f"✓ PowerPoint presentation successfully saved to: {OUTPUT_PPTX}")
    print(f"Total slides generated: {len(prs.slides)}")

if __name__ == "__main__":
    build_presentation()
