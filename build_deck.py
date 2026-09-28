import sys, os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    # Color Palette - Modern High-Tech Executive
    C_BG_DARK    = RGBColor(11, 15, 25)      # #0B0F19 Dark Canvas
    C_CARD_DARK  = RGBColor(21, 29, 46)      # #151D2E Dark Card
    C_CARD_HOVER = RGBColor(30, 41, 59)      # #1E293B Secondary Dark
    C_BORDER     = RGBColor(45, 60, 85)      # #2D3C55 Border
    C_WHITE      = RGBColor(255, 255, 255)  # Pure White
    C_GRAY_LIGHT = RGBColor(226, 232, 240)  # #E2E8F0 Body Text
    C_GRAY_MUTED = RGBColor(148, 163, 184)  # #94A3B8 Secondary Text
    C_CYAN       = RGBColor(56, 189, 248)   # #38BDF8 Vibrant Cyan
    C_CYAN_BG    = RGBColor(12, 45, 72)     # #0C2D48 Cyan Tint
    C_TEAL       = RGBColor(20, 184, 166)   # #14B8A6 Emerald / Teal
    C_AMBER      = RGBColor(245, 158, 11)   # #F59E0B Amber / Warning
    C_PURPLE     = RGBColor(168, 85, 247)   # #A855F7 Purple Accent
    C_RED        = RGBColor(239, 68, 68)    # #EF4444 Alert Red
    C_NAVY_ACC   = RGBColor(2, 132, 199)    # #0284C7 Blue Accent

    def set_slide_bg(slide, color=C_BG_DARK):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, tag_text, title_text, subtitle_text=""):
        # Category Tag Badge
        tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.45), Inches(2.8), Inches(0.32))
        tag_box.fill.solid()
        tag_box.fill.fore_color.rgb = C_CYAN_BG
        tag_box.line.color.rgb = C_CYAN
        tag_box.line.width = Pt(1)
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_CYAN
        p_tag.alignment = PP_ALIGN.CENTER

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.82), Inches(11.7), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE

        # Subtitle (if present)
        if subtitle_text:
            p_sub = tf_title.add_paragraph()
            p_sub.text = subtitle_text
            p_sub.font.name = "Arial"
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = C_GRAY_MUTED
            p_sub.space_before = Pt(3)

    def add_card(slide, left, top, width, height, bg_color=C_CARD_DARK, border_color=C_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Cover)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, C_BG_DARK)

    # Decorative top bar
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_CYAN
    top_bar.line.fill.background()

    # Tag Badge
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.1), Inches(3.6), Inches(0.38))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_CYAN_BG
    badge.line.color.rgb = C_CYAN
    badge.line.width = Pt(1.2)
    b_tf = badge.text_frame
    b_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    bp = b_tf.paragraphs[0]
    bp.text = "B.TECH CAPSTONE PROJECT REVIEW"
    bp.font.name = "Arial"
    bp.font.size = Pt(11)
    bp.font.bold = True
    bp.font.color.rgb = C_CYAN
    bp.alignment = PP_ALIGN.CENTER

    # Main Project Title
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(11.3), Inches(2.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "BharatSpectral"
    p1.font.name = "Arial"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    p2 = tf1.add_paragraph()
    p2.text = "Democratized Spectral Intelligence for Indian Earth Observation Through Physics-Informed Foundation Modeling & Public Geospatial Infrastructure"
    p2.font.name = "Arial"
    p2.font.size = Pt(20)
    p2.font.bold = False
    p2.font.color.rgb = C_CYAN
    p2.space_before = Pt(8)

    # 3 Summary Pillar Cards at bottom
    c1 = add_card(s1, 1.0, 4.2, 3.5, 2.3, C_CARD_DARK, C_CYAN)
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    p_c1_h = tf_c1.paragraphs[0]
    p_c1_h.text = "🔬 RESEARCH PILLAR"
    p_c1_h.font.bold = True
    p_c1_h.font.size = Pt(14)
    p_c1_h.font.color.rgb = C_CYAN
    p_c1_b = tf_c1.add_paragraph()
    p_c1_b.text = "BharatSpectral-MAE: 1st hyperspectral Foundation Model custom-engineered for Indian smallholder fragmentation, intercropping, and multi-season phenology via 7 novel architectural mechanisms."
    p_c1_b.font.size = Pt(11)
    p_c1_b.font.color.rgb = C_GRAY_LIGHT
    p_c1_b.space_before = Pt(6)

    c2 = add_card(s1, 4.9, 4.2, 3.5, 2.3, C_CARD_DARK, C_TEAL)
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    p_c2_h = tf_c2.paragraphs[0]
    p_c2_h.text = "🌐 PRODUCT PILLAR"
    p_c2_h.font.bold = True
    p_c2_h.font.size = Pt(14)
    p_c2_h.font.color.rgb = C_TEAL
    p_c2_b = tf_c2.add_paragraph()
    p_c2_b.text = "BharatSpectral Platform: Zero-cost, public WebGIS platform delivering biochemical analytics (Nitrogen, Soil Organic Carbon, Water Quality) using serverless edge inference and zero-egress tile streaming."
    p_c2_b.font.size = Pt(11)
    p_c2_b.font.color.rgb = C_GRAY_LIGHT
    p_c2_b.space_before = Pt(6)

    c3 = add_card(s1, 8.8, 4.2, 3.5, 2.3, C_CARD_DARK, C_PURPLE)
    tf_c3 = c3.text_frame
    tf_c3.word_wrap = True
    p_c3_h = tf_c3.paragraphs[0]
    p_c3_h.text = "🇮🇳 NATIONAL ALIGNMENT"
    p_c3_h.font.bold = True
    p_c3_h.font.size = Pt(14)
    p_c3_h.font.color.rgb = C_PURPLE
    p_c3_b = tf_c3.add_paragraph()
    p_c3_b.text = "Harnessing IndiaAI AIRAWAT DGX A100 HPC, ISRO AVIRIS-NG & HysIS missions, and open Digital Public Infrastructure (DPI) to empower farmers, KVKs, and state water collectors without paywalls."
    p_c3_b.font.size = Pt(11)
    p_c3_b.font.color.rgb = C_GRAY_LIGHT
    p_c3_b.space_before = Pt(6)

    print("Created Slide 1")

    # =========================================================================
    # SLIDE 2: THE REAL-WORLD PROBLEM & PARADOX
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, C_BG_DARK)
    add_header(s2, "Context & Motivation", "The Indian Geospatial Paradox: Data Abundance vs. Field Paralysis", "Why 140 million smallholder farmers remain locked in guesswork despite India's top-5 space program")

    # Left Card: The Data Availability Paradox
    card_l2 = add_card(s2, 0.8, 1.8, 5.6, 5.0)
    tf_l2 = card_l2.text_frame
    tf_l2.word_wrap = True
    p = tf_l2.paragraphs[0]
    p.text = "🛰️ THE OBSERVATIONAL ABUNDANCE"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = C_CYAN

    bullets_l2 = [
        ("Top-5 Global Space Power: ", "ISRO launches advanced hyperspectral sensors (HysIS, AVIRIS-NG airborne campaigns) capturing petabytes of spectral data across the subcontinent."),
        ("Massive Public Investment: ", "Billions invested in satellites, yet operational usage is restricted to academic research papers and institutional labs."),
        ("The 'Data Graveyard' Syndrome: ", "Airborne AVIRIS-NG data sits in raw ENVI / HDF binary files (5–10 GB per scene) on Bhoonidhi. Unusable by agronomists or non-technical district officers.")
    ]
    for b_title, b_desc in bullets_l2:
        p_b = tf_l2.add_paragraph()
        p_b.space_before = Pt(12)
        run1 = p_b.add_run()
        run1.text = "• " + b_title
        run1.font.bold = True
        run1.font.size = Pt(12)
        run1.font.color.rgb = C_WHITE
        run2 = p_b.add_run()
        run2.text = b_desc
        run2.font.size = Pt(11)
        run2.font.color.rgb = C_GRAY_LIGHT

    # Right Card: The Field-Level Ground Reality
    card_r2 = add_card(s2, 6.8, 1.8, 5.7, 5.0)
    tf_r2 = card_r2.text_frame
    tf_r2.word_wrap = True
    p = tf_r2.paragraphs[0]
    p.text = "🌾 THE SMALLHOLDER REALITY"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = C_AMBER

    bullets_r2 = [
        ("1.08 Hectare Average Landholding: ", "86% of Indian farmers are smallholders. They operate on tight margins where a single crop failure or delayed rust diagnosis triggers devastating debt cycles."),
        ("The Cost Barrier: ", "Commercial hyperspectral analytics (e.g. Pixxel Aurora, SatSure) target enterprise agribusinesses at thousands of dollars per month — completely inaccessible to rural Panchayats."),
        ("The Compute & Software Barrier: ", "Hyperspectral analysis currently requires high-end workstations, proprietary desktop GIS (ENVI, ERDAS), or specialized Python programming in Google Earth Engine."),
        ("The Core Mission: ", "BharatSpectral bridges this chasm by delivering laboratory-grade biochemical intelligence directly to any mobile browser as free Digital Public Infrastructure.")
    ]
    for b_title, b_desc in bullets_r2:
        p_b = tf_r2.add_paragraph()
        p_b.space_before = Pt(10)
        run1 = p_b.add_run()
        run1.text = "• " + b_title
        run1.font.bold = True
        run1.font.size = Pt(12)
        run1.font.color.rgb = C_WHITE
        run2 = p_b.add_run()
        run2.text = b_desc
        run2.font.size = Pt(11)
        run2.font.color.rgb = C_GRAY_LIGHT

    print("Created Slide 2")

    # =========================================================================
    # SLIDE 3: BIOPHYSICAL VS BIOCHEMICAL INTELLIGENCE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, C_BG_DARK)
    add_header(s3, "Spectroscopy Principles", "The Fundamental Distinction: Biophysical vs. Biochemical Intelligence", "Why current satellite platforms fail to provide actionable root-cause diagnosis")

    # Comparison Grid - 2 Big Columns
    # Left: Multispectral
    c_multi = add_card(s3, 0.8, 1.8, 5.6, 5.0, C_CARD_DARK, C_BORDER)
    tf_m = c_multi.text_frame
    tf_m.word_wrap = True
    p = tf_m.paragraphs[0]
    p.text = "MULTISPECTRAL SENSING (Current Status Quo)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_GRAY_MUTED
    p_sub = tf_m.add_paragraph()
    p_sub.text = "Sentinel-2, Landsat-8/9, ISRO LISS-IV (10–12 Broad Spectral Bands)"
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = C_CYAN

    multi_points = [
        ("Intelligence Type: ", "Biophysical only. Calculates broad aggregate indices like NDVI, NDRE, EVI."),
        ("What it Detects: ", "Detects THAT a plant is losing greenness or experiencing vigor reduction."),
        ("The Critical Limitation: ", "Cannot determine WHY the crop is failing. Nitrogen starvation, fungal leaf rust, soil salinity, and moisture stress look spectrally IDENTICAL across broad 100 nm bands."),
        ("Diagnostic Timing: ", "Late detection. By the time broad-band NDVI drops, chlorophyll breakdown is extensive and irreversible yield loss (15–30%) has already occurred.")
    ]
    for m_t, m_d in multi_points:
        p_pt = tf_m.add_paragraph()
        p_pt.space_before = Pt(8)
        r1 = p_pt.add_run()
        r1.text = "• " + m_t
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_WHITE
        r2 = p_pt.add_run()
        r2.text = m_d
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_GRAY_LIGHT

    # Right: Hyperspectral
    c_hyper = add_card(s3, 6.8, 1.8, 5.7, 5.0, C_CARD_DARK, C_CYAN)
    tf_h = c_hyper.text_frame
    tf_h.word_wrap = True
    p = tf_h.paragraphs[0]
    p.text = "HYPERSPECTRAL INTELLIGENCE (BharatSpectral)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_CYAN
    p_sub = tf_h.add_paragraph()
    p_sub.text = "AVIRIS-NG, NASA EMIT, ISRO HysIS (200–425 Continuous Narrow Bands, 5nm)"
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = C_TEAL

    hyper_points = [
        ("Intelligence Type: ", "Biochemical & Molecular. Operates as continuous spectroscopy across 380–2500 nm."),
        ("Pre-Symptomatic Nitrogen (720 nm): ", "Isolates the specific Red-Edge inflection point shift driven by cellular nitrogen binding 7–14 days before visible leaf yellowing."),
        ("Fungal Leaf Rust (680 nm vs 710 nm): ", "Differentiates fungal spore penetration from water stress via precise cell structure backscatter inflection, preventing unnecessary pesticide spraying."),
        ("Soil Organic Carbon (2200 nm): ", "Directly measures the SWIR Al-OH and clay-organic absorption doublet, generating lab-grade soil health maps from orbit without manual core sampling.")
    ]
    for h_t, h_d in hyper_points:
        p_pt = tf_h.add_paragraph()
        p_pt.space_before = Pt(8)
        r1 = p_pt.add_run()
        r1.text = "✓ " + h_t
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_CYAN
        r2 = p_pt.add_run()
        r2.text = h_d
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_GRAY_LIGHT

    print("Created Slide 3")

    # =========================================================================
    # SLIDE 4: LITERATURE GAP & VERIFICATION (GLOBAL AI FOUNDATION MODELS)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, C_BG_DARK)
    add_header(s4, "Literature Gap & Verification", "Why Western Foundation Models Fail on Indian Landscapes", "Empirical analysis of why SOTA hyperspectral Foundation Models suffer catastrophic domain transfer")

    # Top summary banner
    banner = add_card(s4, 0.8, 1.8, 11.7, 0.9, C_CARD_HOVER, C_AMBER)
    tf_ban = banner.text_frame
    tf_ban.word_wrap = True
    p_b = tf_ban.paragraphs[0]
    p_b.text = "⚠️ THE 'INDIAN PINES' BENCHMARK FALLACY"
    p_b.font.bold = True
    p_b.font.size = Pt(12)
    p_b.font.color.rgb = C_AMBER
    p_b_sub = tf_ban.add_paragraph()
    p_b_sub.text = "SOTA models (SpectralGPT, HyperSIGMA, SS-MAE) are evaluated on the canonical 'Indian Pines' benchmark. Despite its name, this dataset was captured in Indiana, USA (1992) over giant rectilinear corn/soybean monocultures, sharing ZERO agronomic, ecological, or spatial characteristics with Indian agriculture!"
    p_b_sub.font.size = Pt(10.5)
    p_b_sub.font.color.rgb = C_GRAY_LIGHT

    # 4 Detailed Grid Cards on Why They Fail
    reasons = [
        ("1. Extreme Spatial Fragmentation",
         "Indian average plot size is 1.08 ha (millions <0.5 ha). At 30–60m spaceborne pixel resolution (EMIT/HysIS), every pixel contains multiple crops, field bunds, and irrigation channels. Western models assume pure pixels; Indian data requires sub-pixel spectral unmixing at every point.",
         C_CYAN),
        ("2. Severe Intercropping Mixing",
         "Traditional Indian agronomy co-plants 2–3 species simultaneously (e.g. Sorghum + Pigeon Pea, Maize + Groundnut). The resulting canopy spectra are non-linear mixtures completely absent from Western industrial monoculture datasets.",
         C_TEAL),
        ("3. Multi-Season Phenological Drift",
         "India experiences three distinct agricultural seasons: Kharif (monsoon), Rabi (winter), and Zaid (summer). The same GPS coordinate shows completely divergent phenology. Single-season Foundation Models suffer catastrophic accuracy drops across seasonal transitions.",
         C_PURPLE),
        ("4. Multi-Sensor Cross-Scale Gap",
         "No existing model harmonizes airborne AVIRIS-NG (4–8m GSD, 425 bands) with spaceborne NASA EMIT (60m GSD, 285 bands) and ISRO HysIS (30m GSD, 220 bands). Existing scale-aware models (Scale-MAE) encode spatial scale only, completely ignoring spectral bandwidth variation.",
         C_RED)
    ]

    col_w = 5.7
    col_h = 2.0
    for idx, (r_title, r_desc, r_col) in enumerate(reasons):
        c_left = 0.8 if idx % 2 == 0 else 6.8
        c_top = 2.9 if idx < 2 else 5.1
        c_card = add_card(s4, c_left, c_top, col_w, col_h, C_CARD_DARK, r_col)
        tf_c = c_card.text_frame
        tf_c.word_wrap = True
        p_h = tf_c.paragraphs[0]
        p_h.text = r_title
        p_h.font.bold = True
        p_h.font.size = Pt(12)
        p_h.font.color.rgb = r_col
        p_d = tf_c.add_paragraph()
        p_d.text = r_desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_GRAY_LIGHT
        p_d.space_before = Pt(4)

    print("Created Slide 4")

    # =========================================================================
    # SLIDE 5: ECOSYSTEM AUDIT & VERIFICATION (INDIAN PLATFORMS)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, C_BG_DARK)
    add_header(s5, "Ecosystem Audit & Verification", "National Remote Sensing Landscape: The Public Infrastructure Gap", "Exhaustive 2026 audit of Indian geospatial platforms verifying that no citizen hyperspectral engine exists")

    # Table of Platforms
    table_shape = s5.shapes.add_table(7, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.5)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(2.4)
    table.columns[4].width = Inches(2.4)

    headers = ["Platform / Entity", "Data Modality", "Access Model", "Web HSI Inference?", "The Translational Gap"]
    for i, h_text in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_CARD_HOVER
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = h_text
        p.font.name = "Arial"
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_CYAN
        p.alignment = PP_ALIGN.CENTER

    rows_data = [
        ("ISRO Bhuvan / Krishi-DSS", "Multispectral (LISS, Sentinel-2)", "Public Web Portal", "None (No HSI)", "Biophysical stress only; cannot diagnose biochemical root cause."),
        ("ISRO VEDAS (AVHYAS)", "Hyperspectral (AVIRIS-NG)", "Desktop QGIS Plugin", "Offline Only", "Requires heavy local workstation install; zero browser/citizen access."),
        ("ISRO Bhoonidhi", "Raw HSI Data Catalog", "Public (Registration)", "None (Raw ENVI)", "Distributes raw 5–10 GB binary cubes; no automated analytics engine."),
        ("Pixxel Aurora", "Hyperspectral (Constellation)", "Commercial B2B SaaS", "Yes (Proprietary)", "Enterprise paywall; inaccessible to smallholders and public research."),
        ("Google Earth Engine (GEE)", "PaaS (Hosts NASA EMIT)", "Freemium PaaS", "User Must Code", "Requires Python/JS GIS scripting; no pre-trained smallholder AI models."),
        ("BharatSpectral (Ours)", "Multi-Sensor HSI (200–425 b)", "100% Free Public Infra", "Yes (Real-Time Edge)", "The ONLY open Foundation Model + zero-cost WebGIS platform in India.")
    ]

    for row_idx, rdata in enumerate(rows_data, start=1):
        for col_idx, text_val in enumerate(rdata):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            # Highlight our row
            if row_idx == 6:
                cell.fill.fore_color.rgb = C_CYAN_BG
            else:
                cell.fill.fore_color.rgb = C_CARD_DARK if row_idx % 2 == 1 else RGBColor(16, 22, 36)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = text_val
            p.font.name = "Arial"
            p.font.size = Pt(10)
            if row_idx == 6:
                p.font.bold = (col_idx == 0 or col_idx == 3)
                p.font.color.rgb = C_CYAN if col_idx < 4 else C_WHITE
            else:
                p.font.color.rgb = C_WHITE if col_idx == 0 else C_GRAY_LIGHT

    # Bottom takeaway
    bot_card = add_card(s5, 0.8, 6.2, 11.7, 0.7, C_CARD_HOVER, C_TEAL)
    tf_bot = bot_card.text_frame
    tf_bot.word_wrap = True
    p_bot = tf_bot.paragraphs[0]
    p_bot.text = "🎯 VERIFIED FINDING: No system exists globally or nationally combining physics-informed self-supervised foundation modeling for Indian smallholders with zero-egress, citizen-accessible public WebGIS deployment."
    p_bot.font.bold = True
    p_bot.font.size = Pt(10.5)
    p_bot.font.color.rgb = C_TEAL

    print("Created Slide 5")

    # =========================================================================
    # SLIDE 6: DUAL-PILLAR ARCHITECTURE OVERVIEW
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, C_BG_DARK)
    add_header(s6, "System Overview", "The Dual-Pillar Framework: Synergizing AI Research & Public Infrastructure", "Engineering Democratized Spectral-Semantic Intelligence (DSSI) from lab to field")

    # Left Big Box: Research Pillar
    p1_card = add_card(s6, 0.8, 1.8, 5.6, 5.1, C_CARD_DARK, C_CYAN)
    tf_p1 = p1_card.text_frame
    tf_p1.word_wrap = True
    p = tf_p1.paragraphs[0]
    p.text = "PILLAR 1: AI FOUNDATION RESEARCH"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = C_CYAN

    p_sub = tf_p1.add_paragraph()
    p_sub.text = "BharatSpectral-MAE Engine (AIRAWAT HPC DGX A100)"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = C_WHITE
    p_sub.space_before = Pt(2)

    p1_bullets = [
        ("Multi-Sensor Training: ", "Harmonizes airborne ISRO AVIRIS-NG (4–8m, 425b), NASA EMIT (60m, 285b), and ISRO HysIS (30m, 220b)."),
        ("7 Named Architectural Innovations: ", "SSPE, RNRL, SHT, AAM, ECSA, Ph-LoRA, and FASU designed explicitly for Indian agro-ecological realities."),
        ("BharatHSI-Bench: ", "Creating India's first standardized, open, labeled hyperspectral benchmark with ground truth crop and soil labels."),
        ("Model Distillation: ", "Distills heavy Vision Transformer representations into a lightweight mobile student for sub-second edge execution.")
    ]
    for b_title, b_desc in p1_bullets:
        p_b = tf_p1.add_paragraph()
        p_b.space_before = Pt(8)
        r1 = p_b.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_CYAN
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_GRAY_LIGHT

    # Right Big Box: Product Pillar
    p2_card = add_card(s6, 6.8, 1.8, 5.7, 5.1, C_CARD_DARK, C_TEAL)
    tf_p2 = p2_card.text_frame
    tf_p2.word_wrap = True
    p = tf_p2.paragraphs[0]
    p.text = "PILLAR 2: PUBLIC GEOSPATIAL INFRASTRUCTURE"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = C_TEAL

    p_sub = tf_p2.add_paragraph()
    p_sub.text = "BharatSpectral WebGIS Platform (Cloudflare Serverless)"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = C_WHITE
    p_sub.space_before = Pt(2)

    p2_bullets = [
        ("Zero-Egress Streaming: ", "Multi-terabyte Zarr datacubes and Cloud-Optimized GeoTIFFs (COG) hosted on Cloudflare R2 with $0 egress fees."),
        ("Serverless Spectral Inference (SSI): ", "Quantized ONNX student model executes inside Cloudflare Workers V8 isolates within strict 128 MB RAM constraints."),
        ("Citizen MapLibre WebGIS: ", "Intuitive, high-performance web frontend allowing farmers, officers, and researchers to query any GPS coordinate with zero installation."),
        ("Actionable Translation: ", "Converts complex 200-band spectral tensors into single-click diagnostic maps: Nitrogen (kg/ha), Soil Carbon (%), Water Bloom Toxicity.")
    ]
    for b_title, b_desc in p2_bullets:
        p_b = tf_p2.add_paragraph()
        p_b.space_before = Pt(8)
        r1 = p_b.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_TEAL
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_GRAY_LIGHT

    print("Created Slide 6")

    # =========================================================================
    # SLIDE 7: THE 7 NAMED ARCHITECTURAL INNOVATIONS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, C_BG_DARK)
    add_header(s7, "Research Core", "BharatSpectral-MAE: The 7 Named Architectural Innovations", "Engineered to overcome the physical and ecological constraints of Indian smallholder Earth Observation")

    # 7 Cards in a 2-column or 3-column arrangement
    # We will do 4 on left, 3 on right + a synthesis box
    innovations = [
        ("SSPE", "Scale-Spectral Positional Encoding", "Extends Scale-MAE into hyperspectral: jointly encodes GSD (4m–60m), spectral bandwidth, and mixture entropy across 3 sensors.", C_CYAN),
        ("RNRL", "Reflectance-Normalized Reconstruction Loss", "Normalizes reconstruction loss by target magnitude, preventing water/wetland signatures (<5% SWIR) from being ignored as noise.", C_TEAL),
        ("SHT", "Spectral Harmonic Tokenizer", "Dynamically allocates fine 3D tokens (4×4×4) in high-density Red-Edge absorption zones (700–750 nm) and coarse tokens in continuum.", C_PURPLE),
        ("AAM", "Atmospheric Absorption Masking", "Simulates atmospheric water vapor (1350–1420 nm, 1800–1950 nm) & CO2 gaps, forcing the model to learn radiative transfer physics.", C_AMBER),
        ("ECSA", "Endmember-Constrained Attention", "Regularizes self-attention via spectral unmixing similarity, attending to matching crop signatures across plot boundaries.", C_CYAN),
        ("Ph-LoRA", "Phenology-Conditioned LoRA", "Modulates PEFT adapter weights with crop growth stage embeddings across Kharif, Rabi, and Zaid seasons, stopping temporal drift.", C_TEAL),
        ("FASU", "Foundation-Augmented Unmixing", "Direct sub-pixel abundance unmixing head operating on pre-trained representations, unmixing mixed pixels without retraining.", C_PURPLE)
    ]

    for idx, (code, full_name, desc, color) in enumerate(innovations):
        # 4 on left (0..3), 3 on right (4..6)
        if idx < 4:
            left_pos = 0.8
            top_pos = 1.8 + idx * 1.25
            width_pos = 5.6
        else:
            left_pos = 6.8
            top_pos = 1.8 + (idx - 4) * 1.25
            width_pos = 5.7

        inv_card = add_card(s7, left_pos, top_pos, width_pos, 1.15, C_CARD_DARK, color)
        tf_inv = inv_card.text_frame
        tf_inv.word_wrap = True
        p_h = tf_inv.paragraphs[0]
        r_code = p_h.add_run()
        r_code.text = f"[{code}] "
        r_code.font.bold = True
        r_code.font.size = Pt(11.5)
        r_code.font.color.rgb = color
        r_name = p_h.add_run()
        r_name.text = full_name
        r_name.font.bold = True
        r_name.font.size = Pt(11)
        r_name.font.color.rgb = C_WHITE

        p_d = tf_inv.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = C_GRAY_LIGHT
        p_d.space_before = Pt(2)

    # 4th box on right side: Synthesis Summary
    syn_card = add_card(s7, 6.8, 1.8 + 3 * 1.25, 5.7, 1.15, C_CARD_HOVER, C_CYAN)
    tf_syn = syn_card.text_frame
    tf_syn.word_wrap = True
    p_syn = tf_syn.paragraphs[0]
    p_syn.text = "💡 SCIENTIFIC SIGNIFICANCE"
    p_syn.font.bold = True
    p_syn.font.size = Pt(11)
    p_syn.font.color.rgb = C_CYAN
    p_syn_d = tf_syn.add_paragraph()
    p_syn_d.text = "These 7 mechanisms replace arbitrary computer vision heuristics with domain-informed radiative transfer physics, creating the first model natively resilient to Indian agricultural topography."
    p_syn_d.font.size = Pt(9.5)
    p_syn_d.font.color.rgb = C_GRAY_LIGHT
    p_syn_d.space_before = Pt(2)

    print("Created Slide 7")

    # =========================================================================
    # SLIDE 8: SOLVING THE 3 STRUCTURAL CLOUD BOTTLENECKS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, C_BG_DARK)
    add_header(s8, "Software Architecture", "Product Pillar: Breaking the 3 Structural Bottlenecks of Hyperspectral WebGIS", "How our serverless architecture reduces marginal operating costs to near-zero for sustained public access")

    bottlenecks = [
        ("BOTTLENECK 1: DATA VOLUME",
         "The Problem:",
         "A single hyperspectral scene ranges from 2 GB to 10 GB. Serving 200+ raw bands to thousands of concurrent citizen users crashes standard WebGIS tile servers (GeoServer/MapServer) and saturates network bandwidth.",
         "Our Solution: Zero-Egress Spectral Tile Streaming",
         "Convert raw ENVI cubes into Cloud-Optimized GeoTIFFs (COG) and chunked Zarr datacubes. The browser requests ONLY the exact bounding box and 3–5 diagnostic wavelengths via HTTP Range GET requests, slashing payload sizes by 98%.",
         C_CYAN),

        ("BOTTLENECK 2: EGRESS COSTS",
         "The Problem:",
         "Traditional cloud providers (AWS S3, Google Cloud Storage) charge exorbitant outbound data transfer fees ($0.08–$0.12/GB). Streaming gigabyte-scale spectral cubes to the public would result in thousands of dollars in monthly cloud debt.",
         "Our Solution: Cloudflare R2 Object Storage",
         "Leverage Cloudflare R2's revolutionary S3-compatible architecture with guaranteed $0 DATA EGRESS FEES. Public users can query, pan, and stream spectral cubes infinitely without incurring incremental bandwidth costs.",
         C_TEAL),

        ("BOTTLENECK 3: INFERENCE COMPUTE",
         "The Problem:",
         "Evaluating a 200-band Transformer foundation model requires dedicated GPU clusters (e.g. A100/V100 instances costing $1,500+/month), making continuous public deployment economically unsustainable.",
         "Our Solution: Serverless Spectral Inference (SSI)",
         "Through Knowledge Distillation and INT8 quantization, BharatSpectral-MAE is compressed into a compact mobile student running directly on Cloudflare Workers V8 isolates within strict 128 MB RAM limits, providing sub-second inference at the edge.",
         C_PURPLE)
    ]

    card_w = 3.65
    card_h = 5.0
    for idx, (b_name, p_lbl, p_txt, s_lbl, s_txt, b_col) in enumerate(bottlenecks):
        b_left = 0.8 + idx * 4.02
        b_card = add_card(s8, b_left, 1.8, card_w, card_h, C_CARD_DARK, b_col)
        tf_b = b_card.text_frame
        tf_b.word_wrap = True

        p_h = tf_b.paragraphs[0]
        p_h.text = b_name
        p_h.font.bold = True
        p_h.font.size = Pt(12)
        p_h.font.color.rgb = b_col

        p1_l = tf_b.add_paragraph()
        p1_l.text = p_lbl
        p1_l.font.bold = True
        p1_l.font.size = Pt(10.5)
        p1_l.font.color.rgb = C_RED
        p1_l.space_before = Pt(8)

        p1_t = tf_b.add_paragraph()
        p1_t.text = p_txt
        p1_t.font.size = Pt(9.5)
        p1_t.font.color.rgb = C_GRAY_LIGHT
        p1_t.space_before = Pt(2)

        p2_l = tf_b.add_paragraph()
        p2_l.text = s_lbl
        p2_l.font.bold = True
        p2_l.font.size = Pt(10.5)
        p2_l.font.color.rgb = C_TEAL
        p2_l.space_before = Pt(12)

        p2_t = tf_b.add_paragraph()
        p2_t.text = s_txt
        p2_t.font.size = Pt(9.5)
        p2_t.font.color.rgb = C_GRAY_LIGHT
        p2_t.space_before = Pt(2)

    print("Created Slide 8")

    # =========================================================================
    # SLIDE 9: END-TO-END PIPELINE & DATA JOURNEY
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9, C_BG_DARK)
    add_header(s9, "Engineering Pipeline", "The End-to-End Data Journey: From Raw Photons to Citizen Action", "Detailed architectural workflow connecting ISRO/NASA satellites to browser-based edge inference")

    # 4 Flow Steps horizontally
    flow_steps = [
        ("STAGE 1: ACQUISITION & PREPROCESSING",
         "• ISRO AVIRIS-NG (Airborne Bhoonidhi)\n• NASA EMIT & ISRO HysIS passes\n• Bad Band Removal (BBR: 1350–1420 & 1800–1950 nm dropped)\n• Radiative transfer surface reflectance conversion\n• Export to Analysis-Ready Zarr & Cloud-Optimized GeoTIFFs (COG)",
         C_CYAN),

        ("STAGE 2: AIRAWAT HPC FOUNDATION MODEL",
         "• IndiaAI AIRAWAT DGX A100 nodes\n• PyTorch DDP distributed scaling\n• Self-supervised pre-training with 7 innovations (SSPE, RNRL, SHT, AAM, ECSA)\n• bfloat16 mixed precision & gradient checkpointing for 200+ band cubes\n• Ph-LoRA fine-tuning for Kharif/Rabi phenology",
         C_PURPLE),

        ("STAGE 3: KNOWLEDGE DISTILLATION",
         "• Heavy Spectral-MAE Transformer acting as Teacher\n• Compact Mobile 3D-2D CNN acting as Student\n• Transfers 'dark knowledge' & absorption inflection sensitivities\n• INT8 post-training quantization\n• ONNX runtime compilation optimized for 128 MB V8 isolates",
         C_AMBER),

        ("STAGE 4: SERVERLESS WEBGIS DELIVERY",
         "• Cloudflare R2 zero-egress tile hosting\n• Cloudflare Workers running Serverless Spectral Inference (SSI)\n• Next.js + MapLibre GL JS client portal\n• Instant sub-pixel maps: Nitrogen deficiency, Soil Organic Carbon, and Algal Bloom alerts\n• Sub-second response on standard mobile 4G/5G",
         C_TEAL)
    ]

    step_w = 2.75
    step_h = 5.0
    for idx, (s_title, s_bullets, s_col) in enumerate(flow_steps):
        s_left = 0.8 + idx * 3.0
        s_card = add_card(s9, s_left, 1.8, step_w, step_h, C_CARD_DARK, s_col)
        tf_s = s_card.text_frame
        tf_s.word_wrap = True

        p_h = tf_s.paragraphs[0]
        p_h.text = f"STEP {idx+1}"
        p_h.font.bold = True
        p_h.font.size = Pt(11)
        p_h.font.color.rgb = s_col

        p_t = tf_s.add_paragraph()
        p_t.text = s_title
        p_t.font.bold = True
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = C_WHITE
        p_t.space_before = Pt(4)

        p_b = tf_s.add_paragraph()
        p_b.text = s_bullets
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = C_GRAY_LIGHT
        p_b.space_before = Pt(8)

    print("Created Slide 9")

    # =========================================================================
    # SLIDE 10: REAL-WORLD USE CASE 1 - PRECISION AGRICULTURE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10, C_BG_DARK)
    add_header(s10, "Real-World Impact: Use Case 1", "Precision Agriculture: The Smallholder Farmer in Ludhiana", "Pre-symptomatic nitrogen deficiency and yellow rust diagnosis 7 to 14 days before visible damage")

    # Left Card: The Story & Scenario
    card_l10 = add_card(s10, 0.8, 1.8, 5.6, 5.0, C_CARD_DARK, C_CYAN)
    tf_l10 = card_l10.text_frame
    tf_l10.word_wrap = True
    p = tf_l10.paragraphs[0]
    p.text = "🌾 PERSONA: GURPREET SINGH (Ludhiana, Punjab)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_CYAN

    story_bullets = [
        ("The Smallholder Challenge: ", "Gurpreet cultivates 2.4 acres of wheat during Rabi. Over-application of urea has degraded his soil and spiked input expenses, while recurring stripe rust (yellow rust) threatens his entire harvest every February."),
        ("The Status Quo Dilemma: ", "Current multispectral satellite apps (NDVI) only show distress once his wheat leaves turn yellow. By then, the fungal mycelium has penetrated the mesophyll tissue, and 20% yield destruction is already locked in."),
        ("BharatSpectral Intervention: ", "Gurpreet opens BharatSpectral on his smartphone. The platform queries recent NASA EMIT / AVIRIS-NG passes and performs sub-pixel unmixing over his exact coordinates."),
        ("Pre-Symptomatic Diagnosis: ", "Identifies a distinct Red-Edge inflection shift at 720 nm (nitrogen deficit) and distinguishes it from fungal rust spore activity (680 nm absorption drop) 10 days before visual signs appear.")
    ]
    for b_title, b_desc in story_bullets:
        p_b = tf_l10.add_paragraph()
        p_b.space_before = Pt(8)
        r1 = p_b.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_WHITE
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_GRAY_LIGHT

    # Right Card: Tangible Economic & Agronomic Outcomes
    card_r10 = add_card(s10, 6.8, 1.8, 5.7, 5.0, C_CARD_DARK, C_TEAL)
    tf_r10 = card_r10.text_frame
    tf_r10.word_wrap = True
    p = tf_r10.paragraphs[0]
    p.text = "📈 QUANTIFIABLE IMPACT & OUTCOMES"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_TEAL

    outcomes = [
        ("₹3,500 / Acre Fertilizer Savings: ", "Variable-rate nitrogen application maps pinpoint exact sub-field deficiency zones, reducing blanket urea over-application by 30%."),
        ("Yield Protection (15–22% Preserved): ", "Early targeted fungicide spraying in infected micro-clusters halts yellow rust epidemics before whole-field infestation occurs."),
        ("Groundwater Protection: ", "Mitigates toxic nitrate runoff into Punjab's over-exploited Malwa aquifer by preventing unnecessary fertilizer broadcast."),
        ("Zero Technical Overhead: ", "Outputs a simple color-coded prescription map on mobile WhatsApp/PWA with zero spectroscopy jargon ('Zone A: Apply 8kg Urea; Zone B: Healthy').")
    ]
    for o_title, o_desc in outcomes:
        p_o = tf_r10.add_paragraph()
        p_o.space_before = Pt(10)
        r1 = p_o.add_run()
        r1.text = "✓ " + o_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_TEAL
        r2 = p_o.add_run()
        r2.text = o_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_GRAY_LIGHT

    print("Created Slide 10")

    # =========================================================================
    # SLIDE 11: REAL-WORLD USE CASE 2 - SOIL HEALTH & GOVERNANCE
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11, C_BG_DARK)
    add_header(s11, "Real-World Impact: Use Case 2", "Soil Health & Governance: District Collector & KVK in Karnal", "Automating Soil Organic Carbon (SOC) and Soil Health Card verification across entire districts")

    card_l11 = add_card(s11, 0.8, 1.8, 5.6, 5.0, C_CARD_DARK, C_AMBER)
    tf_l11 = card_l11.text_frame
    tf_l11.word_wrap = True
    p = tf_l11.paragraphs[0]
    p.text = "🏛️ PERSONA: DR. ANITA VERMA (KVK Officer, Karnal)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_AMBER

    sh_bullets = [
        ("The Administrative Bottleneck: ", "Dr. Verma is mandated to issue 25,000 Soil Health Cards annually. Physical soil sampling requires laboratory wet-chemistry (Walkley-Black titration) taking 4–6 weeks per sample, leaving 80% of plots unverified."),
        ("Post-Harvest Residue Crisis: ", "Stubble burning in October degrades topsoil organic matter while blanket fertilizer subsidies mask progressive soil biological dead zones."),
        ("The BharatSpectral Solution: ", "Leverages Ph-LoRA pre-sowing bare soil attention to map Soil Organic Carbon (SOC) and clay mineralogy directly from 2200 nm SWIR absorption doublets across the entire district at 10m resolution."),
        ("Automated Digital Soil Cards: ", "Pairs hyperspectral reflectance directly with National Soil Health Card laboratory databases, generating continuous spatial soil health layers without physical soil transport delays.")
    ]
    for b_title, b_desc in sh_bullets:
        p_b = tf_l11.add_paragraph()
        p_b.space_before = Pt(8)
        r1 = p_b.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_WHITE
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_GRAY_LIGHT

    card_r11 = add_card(s11, 6.8, 1.8, 5.7, 5.0, C_CARD_DARK, C_PURPLE)
    tf_r11 = card_r11.text_frame
    tf_r11.word_wrap = True
    p = tf_r11.paragraphs[0]
    p.text = "📊 POLICY & AGRICULTURAL IMPACT"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_PURPLE

    sh_outcomes = [
        ("100% District Coverage vs 5% Manual: ", "Replaces sparse point-sample interpolations with exhaustive, continuous wall-to-wall soil carbon mapping."),
        ("Stubble Burning Impact Tracking: ", "Quantifies immediate post-fire topsoil carbon volatilization, providing district magistrates with empirical evidence to reward regenerative farming practices."),
        ("Rationalized Fertilizer Subsidies: ", "Enables state agriculture departments to redirect subsidized NPK fertilizer based on true biochemical soil deficiencies rather than political quotas."),
        ("Climate Carbon Credit Verification: ", "Provides the spatial baseline required for Indian farmers to participate in international voluntary carbon markets for soil carbon sequestration.")
    ]
    for o_title, o_desc in sh_outcomes:
        p_o = tf_r11.add_paragraph()
        p_o.space_before = Pt(10)
        r1 = p_o.add_run()
        r1.text = "✓ " + o_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_PURPLE
        r2 = p_o.add_run()
        r2.text = o_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_GRAY_LIGHT

    print("Created Slide 11")

    # =========================================================================
    # SLIDE 12: REAL-WORLD USE CASE 3 - WATER QUALITY & ENVIRONMENTAL
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12, C_BG_DARK)
    add_header(s12, "Real-World Impact: Use Case 3", "Environmental Protection: Water Quality Inspector in Varanasi", "Detecting toxic cyanobacterial blooms and industrial effluent plumes in low-reflectance inland waters")

    card_l12 = add_card(s12, 0.8, 1.8, 5.6, 5.0, C_CARD_DARK, C_TEAL)
    tf_l12 = card_l12.text_frame
    tf_l12.word_wrap = True
    p = tf_l12.paragraphs[0]
    p.text = "🌊 PERSONA: RAJESH TRIPATHI (Pollution Control, Varanasi)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_TEAL

    water_bullets = [
        ("The Ganga Basin Challenge: ", "Inland water bodies and river corridors absorb >95% of incoming solar radiation in the SWIR spectrum (reflectance <5%). Standard AI models and multispectral satellites treat inland water as pure dark noise."),
        ("Toxic Cyanobacteria vs. Algae: ", "Multispectral sensors (Sentinel-2) measure broad chlorophyll-a (665 nm), mistaking harmless green algae for life-threatening cyanobacterial (blue-green) blooms releasing microcystin liver toxins."),
        ("BharatSpectral Breakthrough: ", "Our Reflectance-Normalized Reconstruction Loss (RNRL) forces the foundation model to learn subtle spectral variations in low-reflectance water bodies."),
        ("Diagnostic Phycocyanin Detection: ", "Isolates the specific 620 nm phycocyanin absorption feature, uniquely detecting toxic cyanobacteria 5 days before massive fish kills and water treatment shutdowns occur.")
    ]
    for b_title, b_desc in water_bullets:
        p_b = tf_l12.add_paragraph()
        p_b.space_before = Pt(8)
        r1 = p_b.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_WHITE
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_GRAY_LIGHT

    card_r12 = add_card(s12, 6.8, 1.8, 5.7, 5.0, C_CARD_DARK, C_CYAN)
    tf_r12 = card_r12.text_frame
    tf_r12.word_wrap = True
    p = tf_r12.paragraphs[0]
    p.text = "🛡️ ENVIRONMENTAL & PUBLIC HEALTH OUTCOMES"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_CYAN

    water_outcomes = [
        ("Drinking Water Intake Protection: ", "Early warning alerts dispatch automatically to Varanasi municipal water treatment plants to switch coagulants and activate carbon filters before toxin ingestion."),
        ("Tannery & Industrial Effluent Tracing: ", "Narrow-band spectral unmixing traces chromium and chemical dye plume dispersion from Kanpur/Unnao industrial drains along the riverbank."),
        ("Namami Gange Mission Support: ", "Provides the National Mission for Clean Ganga with verifiable, transparent, satellite-derived water quality indices (Turbidity, CDOM, Chl-a) without manual boat sampling."),
        ("Zero Laboratory Lag: ", "Reduces environmental compliance reporting from 14 days of wet-lab incubation to instant sub-minute web map inspection.")
    ]
    for o_title, o_desc in water_outcomes:
        p_o = tf_r12.add_paragraph()
        p_o.space_before = Pt(10)
        r1 = p_o.add_run()
        r1.text = "✓ " + o_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_CYAN
        r2 = p_o.add_run()
        r2.text = o_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_GRAY_LIGHT

    print("Created Slide 12")

    # =========================================================================
    # SLIDE 13: REAL-WORLD USE CASE 4 - CROP INSURANCE & DISASTER
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13, C_BG_DARK)
    add_header(s13, "Real-World Impact: Use Case 4", "Disaster Resilience & Crop Insurance: PMFBY Claim Verification", "Objective sub-pixel quantification of crop lodging, drought desiccation, and flood inundation")

    card_l13 = add_card(s13, 0.8, 1.8, 5.6, 5.0, C_CARD_DARK, C_PURPLE)
    tf_l13 = card_l13.text_frame
    tf_l13.word_wrap = True
    p = tf_l13.paragraphs[0]
    p.text = "⚖️ THE INSURANCE BOTTLENECK (PMFBY)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_PURPLE

    ins_bullets = [
        ("Crop Cutting Experiment (CCE) Delays: ", "Pradhan Mantri Fasal Bima Yojana relies on manual CCEs. Conducting millions of physical field cuts takes 3–6 months, leading to prolonged claim settlement delays and farmer distress."),
        ("Subjective Dispute Litigation: ", "Disagreements between insurance companies and state governments over drought or unseasonal hailstorm damage frequently freeze compensation funds."),
        ("Flash Drought Canopy Water Loss: ", "Multispectral sensors detect drought only after plant canopies brown. Hyperspectral 970 nm and 1200 nm liquid water absorption bands measure cell turgor pressure drop in real time."),
        ("Sub-Pixel Crop Lodging Detection: ", "Severe cyclonic winds flatten crops. BharatSpectral unmixes the soil-canopy structural geometry shift at sub-pixel levels, distinguishing flattened crops from healthy standing fields.")
    ]
    for b_title, b_desc in ins_bullets:
        p_b = tf_l13.add_paragraph()
        p_b.space_before = Pt(8)
        r1 = p_b.add_run()
        r1.text = "• " + b_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_WHITE
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_GRAY_LIGHT

    card_r13 = add_card(s13, 6.8, 1.8, 5.7, 5.0, C_CARD_DARK, C_AMBER)
    tf_r13 = card_r13.text_frame
    tf_r13.word_wrap = True
    p = tf_r13.paragraphs[0]
    p.text = "⚡ AUTOMATED CLAIM SETTLEMENT IMPACT"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = C_AMBER

    ins_outcomes = [
        ("Claim Payouts in Days, Not Months: ", "Instant satellite-derived loss assessment enables direct benefit transfers (DBT) to farmers' bank accounts within 72 hours of catastrophic weather."),
        ("Sub-Hectare Plot Granularity: ", "FASU sub-pixel unmixing accurately resolves damage on plots as small as 0.2 hectares, ensuring smallholders are not excluded by coarse pixel averaging."),
        ("100% Tamper-Proof Audit Trail: ", "Publicly verifiable, open-access hyperspectral records eliminate fraudulent claims and political tampering."),
        ("Disaster Relief Coordination: ", "State disaster management authorities can immediately prioritize relief supplies to the exact tehsils with critical crop biomass destruction.")
    ]
    for o_title, o_desc in ins_outcomes:
        p_o = tf_r13.add_paragraph()
        p_o.space_before = Pt(10)
        r1 = p_o.add_run()
        r1.text = "✓ " + o_title
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_AMBER
        r2 = p_o.add_run()
        r2.text = o_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_GRAY_LIGHT

    print("Created Slide 13")

    # =========================================================================
    # SLIDE 14: MASTER TIMELINE & ROADMAP (PHASE 1 TO 5)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14, C_BG_DARK)
    add_header(s14, "Master Execution Roadmap", "End-to-End Project Timeline: Engineering Phases 1 Through 5", "Systematic progression from raw data ingestion to national-scale public infrastructure deployment")

    # 5 Horizontal Phase Cards / Timeline Nodes
    phases = [
        ("PHASE 1", "DATA CURATION & INGESTION",
         "• ISRO AVIRIS-NG, NASA EMIT, ISRO HysIS ingestion\n• Bad Band Removal (BBR) & Radiative Transfer\n• Chunked Zarr & COG creation on Cloudflare R2\n• BharatHSI-Bench ground truth curation\n• SOTA failure documentation on Indian benchmarks",
         C_CYAN),

        ("PHASE 2", "BASELINE MODELING & HPC",
         "• 1D-CNN, 3D-CNN & HybridSN baselines\n• Classical unmixing (VCA & FCLSU endmembers)\n• AIRAWAT HPC Slurm orchestration scripts\n• Establishing quantitative evaluation baselines\n• Strict GPU memory & DDP communication setup",
         C_TEAL),

        ("PHASE 3", "FOUNDATION AI & DISTILLATION",
         "• BharatSpectral-MAE implementation (7 innovations)\n• Self-supervised pre-training on multi-sensor cubes\n• Ph-LoRA fine-tuning for Kharif/Rabi phenology\n• Teacher-Student Knowledge Distillation\n• Model compression & INT8 quantization",
         C_PURPLE),

        ("PHASE 4", "WEBGIS PLATFORM DEV",
         "• Next.js + MapLibre GL JS frontend on Cloudflare Pages\n• Cloudflare R2 zero-egress tile streaming API\n• Serverless Spectral Inference (SSI) on Workers\n• Interactive sub-pixel agricultural map overlays\n• Latency & memory optimization (<128MB)",
         C_AMBER),

        ("PHASE 5", "VALIDATION & OPEN RELEASE",
         "• End-to-end latency & accuracy benchmarking\n• Cloud cost validation ($0 egress vs AWS EC2)\n• Open-source release on GitHub & AIKosh\n• Comprehensive capstone thesis & documentation\n• Final viva & public platform demonstration",
         C_CYAN)
    ]

    phase_w = 2.22
    phase_h = 5.0
    for idx, (p_num, p_title, p_desc, p_col) in enumerate(phases):
        p_left = 0.8 + idx * 2.38
        p_card = add_card(s14, p_left, 1.8, phase_w, phase_h, C_CARD_DARK, p_col)
        tf_p = p_card.text_frame
        tf_p.word_wrap = True

        p_h = tf_p.paragraphs[0]
        p_h.text = p_num
        p_h.font.bold = True
        p_h.font.size = Pt(12)
        p_h.font.color.rgb = p_col

        p_t = tf_p.add_paragraph()
        p_t.text = p_title
        p_t.font.bold = True
        p_t.font.size = Pt(10.5)
        p_t.font.color.rgb = C_WHITE
        p_t.space_before = Pt(4)

        p_d = tf_p.add_paragraph()
        p_d.text = p_desc
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = C_GRAY_LIGHT
        p_d.space_before = Pt(8)

    print("Created Slide 14")

    # =========================================================================
    # SLIDE 15: QUANTITATIVE EVALUATION & SUCCESS METRICS
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s15, C_BG_DARK)
    add_header(s15, "Evaluation Framework", "Quantitative Benchmarking & Success Metrics", "Rigorous empirical standards across AI accuracy, sub-pixel unmixing, and platform performance")

    # 4 Metric Cards
    metric_cards = [
        ("🎯 CLASSIFICATION ACCURACY",
         "Target Benchmark: BharatHSI-Bench",
         "• Overall Accuracy (OA): Target > 92.5%\n• Average Accuracy (AA): Target > 89.0%\n• Kappa Coefficient (κ): Target > 0.90\n• Baseline Comparison: Must demonstrate +15% to +25% OA gain over Western-pretrained SpectralGPT and HyperSIGMA.",
         C_CYAN),

        ("🔬 SUB-PIXEL UNMIXING FIDELITY",
         "Target: Fractional Abundance Maps",
         "• Abundance RMSE: < 0.08 across mixed pixels\n• Spectral Angle Distance (SAD): < 0.05 rad\n• Endmember Recovery: Faithful extraction of co-planted crops in smallholder plots (<0.5 ha)\n• FASU Validation: Tested against ground truth laboratory spectroscopy.",
         C_TEAL),

        ("⚡ SYSTEM LATENCY TARGETS",
         "Deployment: Cloudflare Serverless",
         "• Tile Streaming Latency: < 200 ms per 256×256 tile\n• Serverless Inference: < 5 seconds per km² on Cloudflare Workers V8 isolates\n• Edge Memory Footprint: Strictly under 128 MB RAM\n• Mobile Responsiveness: Smooth 60 FPS map panning on mobile 4G/5G.",
         C_PURPLE),

        ("💰 ECONOMIC SUSTAINABILITY",
         "Target: Long-Term Public Operation",
         "• Marginal Egress Cost: Exactly $0.00 / month on Cloudflare R2\n• Total Infrastructure Cost: < $50 / month vs $1,200+ / month for equivalent AWS EC2 + GeoServer cluster\n• 100% Free Public Access: No subscriber fees for farmers, KVKs, or researchers.",
         C_AMBER)
    ]

    m_w = 5.7
    m_h = 2.35
    for idx, (m_title, m_sub, m_bullets, m_col) in enumerate(metric_cards):
        m_left = 0.8 if idx % 2 == 0 else 6.8
        m_top = 1.8 if idx < 2 else 4.45
        m_card = add_card(s15, m_left, m_top, m_w, m_h, C_CARD_DARK, m_col)
        tf_m = m_card.text_frame
        tf_m.word_wrap = True

        p_h = tf_m.paragraphs[0]
        p_h.text = m_title
        p_h.font.bold = True
        p_h.font.size = Pt(12)
        p_h.font.color.rgb = m_col

        p_s = tf_m.add_paragraph()
        p_s.text = m_sub
        p_s.font.bold = True
        p_s.font.size = Pt(10)
        p_s.font.color.rgb = C_WHITE
        p_s.space_before = Pt(2)

        p_b = tf_m.add_paragraph()
        p_b.text = m_bullets
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = C_GRAY_LIGHT
        p_b.space_before = Pt(4)

    print("Created Slide 15")

    # =========================================================================
    # SLIDE 16: CONCLUSION & NATIONAL IMPACT
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s16, C_BG_DARK)
    add_header(s16, "Conclusion & Vision", "BharatSpectral: Democratizing Spectral Intelligence as Digital Public Infrastructure", "From closed scientific repositories to nationwide citizen empowerment")

    # 3 Summary Cards
    c16_1 = add_card(s16, 0.8, 1.8, 3.65, 4.0, C_CARD_DARK, C_CYAN)
    tf_c16_1 = c16_1.text_frame
    tf_c16_1.word_wrap = True
    p1 = tf_c16_1.paragraphs[0]
    p1.text = "7 ARCHITECTURAL NOVELTIES"
    p1.font.bold = True
    p1.font.size = Pt(12)
    p1.font.color.rgb = C_CYAN
    p1_d = tf_c16_1.add_paragraph()
    p1_d.text = "Engineered the first foundation model built specifically for Indian smallholders. SSPE, RNRL, SHT, AAM, ECSA, Ph-LoRA, and FASU close the empirical gap that causes Western models to fail."
    p1_d.font.size = Pt(10)
    p1_d.font.color.rgb = C_GRAY_LIGHT
    p1_d.space_before = Pt(8)

    c16_2 = add_card(s16, 4.82, 1.8, 3.65, 4.0, C_CARD_DARK, C_TEAL)
    tf_c16_2 = c16_2.text_frame
    tf_c16_2.word_wrap = True
    p2 = tf_c16_2.paragraphs[0]
    p2.text = "3 NATIONAL BENCHMARKS"
    p2.font.bold = True
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEAL
    p2_d = tf_c16_2.add_paragraph()
    p2_d.text = "Establishes BharatHSI-Bench, Multi-Sensor Indian Datacubes, and Paired Spectral-SoilHealth records on AIKosh, freeing Indian academia from its 30-year reliance on outdated foreign datasets."
    p2_d.font.size = Pt(10)
    p2_d.font.color.rgb = C_GRAY_LIGHT
    p2_d.space_before = Pt(8)

    c16_3 = add_card(s16, 8.85, 1.8, 3.65, 4.0, C_CARD_DARK, C_PURPLE)
    tf_c16_3 = c16_3.text_frame
    tf_c16_3.word_wrap = True
    p3 = tf_c16_3.paragraphs[0]
    p3.text = "PUBLIC DIGITAL GOOD"
    p3.font.bold = True
    p3.font.size = Pt(12)
    p3.font.color.rgb = C_PURPLE
    p3_d = tf_c16_3.add_paragraph()
    p3_d.text = "Translates complex aerospace spectroscopy into a zero-cost, high-speed WebGIS tool accessible to any farmer, extension worker, or policymaker on any device without paywalls."
    p3_d.font.size = Pt(10)
    p3_d.font.color.rgb = C_GRAY_LIGHT
    p3_d.space_before = Pt(8)

    # Bottom closing banner
    close_bar = add_card(s16, 0.8, 6.0, 11.7, 0.9, C_CARD_HOVER, C_CYAN)
    tf_cb = close_bar.text_frame
    tf_cb.word_wrap = True
    p_cb = tf_cb.paragraphs[0]
    p_cb.text = "🇮🇳 ALIGNMENT WITH NATIONAL MISSIONS"
    p_cb.font.bold = True
    p_cb.font.size = Pt(11)
    p_cb.font.color.rgb = C_CYAN
    p_cb_d = tf_cb.add_paragraph()
    p_cb_d.text = "Directly advancing the IndiaAI Mission, Digital Public Infrastructure (DPI), and National Mission on Sustainable Agriculture — proving that world-class AI research can deliver direct social utility to the common citizen."
    p_cb_d.font.size = Pt(10)
    p_cb_d.font.color.rgb = C_WHITE
    p_cb_d.space_before = Pt(2)

    print("Created Slide 16")

    output_path = "/data/data/com.termux/files/home/btp/BharatSpectral_MidTerm_Presentation.pptx"
    prs.save(output_path)
    print(f"Successfully generated PowerPoint presentation at: {output_path}")

if __name__ == "__main__":
    create_presentation()
