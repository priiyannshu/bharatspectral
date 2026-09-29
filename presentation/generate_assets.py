#!/usr/bin/env python3
"""
generate_assets.py
Generates high-resolution scientific diagrams, flowcharts, and comic strip assets
for the BharatSpectral 19-Slide Academic Pinboard Presentation using pure Pillow (PIL).
All assets are saved into presentation/assets/
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Common Palette
C_PARCHMENT = (255, 253, 245, 255)
C_KRAFT = (244, 236, 220, 255)
C_DARK = (42, 35, 27, 255)
C_MUTED = (109, 95, 82, 255)
C_CYAN = (11, 114, 133, 255)
C_GREEN = (43, 138, 62, 255)
C_PURPLE = (103, 65, 217, 255)
C_AMBER = (217, 155, 0, 255)
C_RED = (201, 42, 42, 255)
C_BORDER = (216, 200, 175, 255)

def get_font(size=16, bold=False):
    try:
        # Check standard linux font paths
        paths = [
            "/system/fonts/Roboto-Bold.ttf" if bold else "/system/fonts/Roboto-Regular.ttf",
            "/system/fonts/DroidSans.ttf",
            "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf" if bold else "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans.ttf"
        ]
        for p in paths:
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
        return ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()

def draw_polaroid_frame(img, title, subtitle="", badge=""):
    w, h = img.size
    pad = 16
    bottom_pad = 54
    out = Image.new("RGBA", (w + pad * 2, h + pad + bottom_pad), C_PARCHMENT)
    d = ImageDraw.Draw(out)
    d.rectangle([0, 0, out.width - 1, out.height - 1], outline=C_BORDER, width=2)
    out.paste(img, (pad, pad))
    
    font_title = get_font(18, bold=True)
    font_sub = get_font(13, bold=False)
    
    d.text((pad + 4, h + pad + 8), title, fill=C_DARK, font=font_title)
    if subtitle:
        d.text((pad + 4, h + pad + 30), subtitle, fill=C_MUTED, font=font_sub)
    if badge:
        bbox = d.textbbox((0, 0), badge, font=get_font(12, bold=True))
        bw = bbox[2] - bbox[0] + 16
        bx = out.width - pad - bw
        by = h + pad + 12
        d.rounded_rectangle([bx, by, bx + bw, by + 24], radius=6, fill=(11, 114, 133, 40), outline=C_CYAN, width=1)
        d.text((bx + 8, by + 4), badge, fill=C_CYAN, font=get_font(12, bold=True))
        
    return out

# 1. Slide 1: Spectrum Contrast
def make_spectrum_contrast():
    w, h = 800, 360
    im = Image.new("RGBA", (w, h), (248, 244, 235, 255))
    d = ImageDraw.Draw(im)
    
    # Header
    d.text((24, 20), "Electromagnetic Spectrum: Human Sight vs. Hyperspectral", fill=C_DARK, font=get_font(20, bold=True))
    d.text((24, 48), "380–700 nm Visible vs. 400–2500 nm Full Continuous Spectroscopy", fill=C_MUTED, font=get_font(14))
    
    # 1. Human vision sliver bar
    y1 = 90
    d.text((24, y1), "Human Eye (RGB Bands: 3 Bands Only • 1.4% of Solar Reflected Spectrum)", fill=C_RED, font=get_font(13, bold=True))
    # Rainbow sliver
    colors = [(120, 0, 180), (0, 0, 255), (0, 200, 0), (255, 255, 0), (255, 120, 0), (255, 0, 0)]
    bx, bw = 24, 200
    for i in range(bw):
        t = i / bw
        idx = int(t * (len(colors) - 1))
        c1, c2 = colors[idx], colors[min(idx + 1, len(colors) - 1)]
        fr = (t * (len(colors) - 1)) - idx
        r = int(c1[0] + (c2[0] - c1[0]) * fr)
        g = int(c1[1] + (c2[1] - c1[1]) * fr)
        b = int(c1[2] + (c2[2] - c1[2]) * fr)
        d.line([(bx + i, y1 + 24), (bx + i, y1 + 54)], fill=(r, g, b, 255), width=1)
    d.rectangle([bx, y1 + 24, bx + bw, y1 + 54], outline=C_DARK, width=2)
    d.text((bx + bw + 16, y1 + 30), "Blind to 98.6% of chemical & mineral energy", fill=C_MUTED, font=get_font(13, bold=True))
    
    # 2. Continuous Hyperspectral Bar
    y2 = 180
    d.text((24, y2), "BharatSpectral Imaging (425 Continuous Narrow Spectral Channels • 400–2500 nm)", fill=C_CYAN, font=get_font(13, bold=True))
    full_w = 750
    # Spectrum gradient: Visible -> NIR -> SWIR-1 -> SWIR-2
    for i in range(full_w):
        wl = 400 + (i / full_w) * 2100
        if wl < 700:
            c = (40, 140, 200) # VNIR
        elif wl < 1100:
            c = (43, 138, 62)  # NIR
        elif wl < 1800:
            c = (217, 155, 0)  # SWIR-1
        else:
            c = (140, 50, 180)  # SWIR-2
        d.line([(bx + i, y2 + 24), (bx + i, y2 + 64)], fill=(c[0], c[1], c[2], 255), width=1)
        
    # Water absorption gaps
    gap1_x = int(bx + ((1350 - 400) / 2100) * full_w)
    gap1_w = int((100 / 2100) * full_w)
    d.rectangle([gap1_x, y2 + 24, gap1_x + gap1_w, y2 + 64], fill=(50, 40, 30, 200))
    d.text((gap1_x + 4, y2 + 70), "1.4μm H2O", fill=C_RED, font=get_font(11, bold=True))
    
    gap2_x = int(bx + ((1800 - 400) / 2100) * full_w)
    gap2_w = int((150 / 2100) * full_w)
    d.rectangle([gap2_x, y2 + 24, gap2_x + gap2_w, y2 + 64], fill=(50, 40, 30, 200))
    d.text((gap2_x + 4, y2 + 70), "1.9μm H2O/CO2", fill=C_RED, font=get_font(11, bold=True))
    
    d.rectangle([bx, y2 + 24, bx + full_w, y2 + 64], outline=C_CYAN, width=2)
    
    # Physics formula note
    d.rectangle([24, 280, 774, 340], fill=(234, 224, 206, 180), outline=C_BORDER)
    d.text((36, 292), "Radiative Transfer Equation:  L(λ) = L_ground(λ) + L_path(λ)", fill=C_DARK, font=get_font(13, bold=True))
    d.text((36, 314), "Every chemical bond (C-H, N-H, O-H, Al-OH) exhibits diagnostic quantum vibrational absorption.", fill=C_MUTED, font=get_font(12))

    im.save(os.path.join(ASSETS_DIR, "spectrum_contrast.png"))
    print("✓ Generated spectrum_contrast.png")

# 2. Slide 3: Continuous Spectroscopy Absorption Bands
def make_continuous_spectroscopy():
    w, h = 840, 420
    im = Image.new("RGBA", (w, h), (255, 253, 245, 255))
    d = ImageDraw.Draw(im)
    
    d.text((24, 18), "Diagnostic Molecular Absorption Spectrum (400–2500 nm)", fill=C_DARK, font=get_font(20, bold=True))
    d.text((24, 46), "Continuous canopy reflectance curve revealing biochemical concentrations", fill=C_MUTED, font=get_font(13))
    
    # Draw graph axes
    ox, oy = 60, 340
    gw, gh = 740, 240
    d.line([(ox, oy), (ox + gw, oy)], fill=C_DARK, width=2)
    d.line([(ox, oy), (ox, oy - gh)], fill=C_DARK, width=2)
    
    # Generate realistic green leaf reflectance curve
    pts = []
    for x_i in range(gw):
        wl = 400 + (x_i / gw) * 2100
        # Typical vegetation reflectance
        if wl < 500:
            refl = 0.06 + math.sin(wl * 0.02) * 0.01
        elif wl < 680:
            refl = 0.14 - (wl - 550)**2 * 0.000003
        elif wl < 750: # Red-edge steep cliff
            refl = 0.10 + ((wl - 680) / 70.0) * 0.45
        elif wl < 1300: # NIR plateau
            refl = 0.55 - math.sin(wl * 0.01) * 0.04
        elif wl < 1450: # Water dip
            refl = 0.20 + (abs(wl - 1400)/50.0) * 0.20
        elif wl < 1850:
            refl = 0.38 - math.sin(wl * 0.008) * 0.03
        elif wl < 2000: # Second water dip
            refl = 0.12 + (abs(wl - 1920)/80.0) * 0.18
        else: # SWIR protein & clay
            refl = 0.26 - (abs(wl - 2200)/300.0) * 0.10
        y = oy - int(refl * (gh * 1.5))
        pts.append((ox + x_i, y))
        
    d.line(pts, fill=C_GREEN, width=3)
    
    # Annotate key features
    features = [
        (680, "Chlorophyll-a (680nm)", C_RED),
        (720, "Red-Edge Cliff [SHT]", C_CYAN),
        (970, "Cellular Water (970nm)", C_PURPLE),
        (1400, "Water Gap [AAM]", C_AMBER),
        (1900, "CO2/H2O Gap [AAM]", C_AMBER),
        (2200, "Protein & Nitrogen (2.2μm)", C_GREEN)
    ]
    for wl, label, col in features:
        fx = ox + int(((wl - 400) / 2100) * gw)
        d.line([(fx, oy), (fx, oy - gh)], fill=(col[0], col[1], col[2], 80), width=1)
        d.ellipse([fx - 4, oy - 140 - 4, fx + 4, oy - 140 + 4], fill=col)
        d.text((fx - 30, oy - 165), label, fill=col, font=get_font(11, bold=True))
        
    im.save(os.path.join(ASSETS_DIR, "continuous_spectroscopy.png"))
    print("✓ Generated continuous_spectroscopy.png")

# 3. Slide 4: Photon Pinball Scattering & 3D Cube
def make_photon_pinball_cube():
    w, h = 860, 420
    im = Image.new("RGBA", (w, h), (244, 236, 220, 255))
    d = ImageDraw.Draw(im)
    
    d.text((24, 18), "The 'Pinball Machine' Physics & 3D Hyperspectral Cube", fill=C_DARK, font=get_font(20, bold=True))
    d.text((24, 46), "Multiple non-linear canopy scattering requires 3D tensor representations", fill=C_MUTED, font=get_font(13))
    
    # Left: Canopy Pinball
    cx, cy = 200, 240
    d.rectangle([40, 80, 400, 380], fill=(255, 253, 245, 255), outline=C_BORDER, width=2)
    d.text((54, 94), "Canopy Radiative Scattering (Non-Linear)", fill=C_CYAN, font=get_font(14, bold=True))
    
    # Sun and incoming ray
    d.ellipse([70, 130, 110, 170], fill=(255, 200, 0, 255))
    d.line([(100, 160), (160, 220)], fill=(255, 160, 0), width=3)
    
    # Leaves as pinball bumpers
    leaves = [(160, 220), (220, 200), (190, 280), (260, 260), (220, 340)]
    for lx, ly in leaves:
        d.ellipse([lx - 22, ly - 10, lx + 22, ly + 10], fill=C_GREEN)
        
    # Photon scattering ricochets
    d.line([(160, 220), (220, 200)], fill=(255, 120, 0), width=2)
    d.line([(220, 200), (190, 280)], fill=(255, 120, 0), width=2)
    d.line([(190, 280), (260, 260)], fill=(255, 120, 0), width=2)
    d.line([(260, 260), (320, 140)], fill=(255, 80, 0), width=3) # Escaping ray to sensor
    
    d.text((260, 140), "Reflected to Sensor", fill=C_RED, font=get_font(12, bold=True))
    d.text((54, 350), "LSU fails on multi-leaf ricochets", fill=C_MUTED, font=get_font(11, bold=True))
    
    # Right: 3D Data Cube
    d.rectangle([430, 80, 820, 380], fill=(255, 253, 245, 255), outline=C_BORDER, width=2)
    d.text((444, 94), "Hyperspectral 3D Tensor [H x W x 425 Bands]", fill=C_PURPLE, font=get_font(14, bold=True))
    
    # Isometric cube projection
    ix, iy = 560, 240
    size = 110
    bands = 90
    
    # Front face (Spatial H x W)
    d.polygon([(ix, iy), (ix + size, iy), (ix + size, iy + size), (ix, iy + size)], fill=(40, 140, 200, 220), outline=C_DARK)
    # Top face (Spatial W x Bands)
    d.polygon([(ix, iy), (ix + bands, iy - bands // 2), (ix + size + bands, iy - bands // 2), (ix + size, iy)], fill=(50, 170, 220, 220), outline=C_DARK)
    # Right face (Spatial H x Bands)
    d.polygon([(ix + size, iy), (ix + size + bands, iy - bands // 2), (ix + size + bands, iy + size - bands // 2), (ix + size, iy + size)], fill=(30, 110, 180, 220), outline=C_DARK)
    
    # Single pixel spear
    px, py = ix + 45, iy + 45
    d.line([(px, py), (px + bands, py - bands // 2)], fill=C_RED, width=3)
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=C_RED)
    d.text((px + bands + 10, py - bands // 2 - 8), "Single Pixel: 425 Spectral Values", fill=C_RED, font=get_font(12, bold=True))
    
    d.text((444, 350), "SSPE preserves spatial GSD & spectral bandwidth", fill=C_MUTED, font=get_font(11, bold=True))
    
    im.save(os.path.join(ASSETS_DIR, "photon_pinball_cube.png"))
    print("✓ Generated photon_pinball_cube.png")

# 4. Slide 5: Venn Diagram
def make_venn_diagram():
    w, h = 820, 420
    im = Image.new("RGBA", (w, h), (255, 253, 245, 255))
    d = ImageDraw.Draw(im)
    
    d.text((24, 18), "The Triad of Human Knowledge Systems", fill=C_DARK, font=get_font(20, bold=True))
    d.text((24, 46), "BharatSpectral (DSSI) sits at the exact synthesis of 3 foundational disciplines", fill=C_MUTED, font=get_font(13))
    
    # 3 Circles
    r = 130
    c1 = (320, 200) # Spectroscopy (Cyan)
    c2 = (500, 200) # Foundation AI (Green)
    c3 = (410, 310) # WebGIS DPI (Purple)
    
    circ_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cd = ImageDraw.Draw(circ_layer)
    cd.ellipse([c1[0] - r, c1[1] - r, c1[0] + r, c1[1] + r], fill=(11, 114, 133, 100), outline=C_CYAN, width=3)
    cd.ellipse([c2[0] - r, c2[1] - r, c2[0] + r, c2[1] + r], fill=(43, 138, 62, 100), outline=C_GREEN, width=3)
    cd.ellipse([c3[0] - r, c3[1] - r, c3[0] + r, c3[1] + r], fill=(103, 65, 217, 100), outline=C_PURPLE, width=3)
    
    im = Image.alpha_composite(im, circ_layer)
    d = ImageDraw.Draw(im)
    
    # Circle Labels
    d.text((150, 130), "Radiative Transfer &\nOptical Spectroscopy", fill=C_CYAN, font=get_font(14, bold=True))
    d.text((540, 130), "Foundation AI &\nSelf-Attention Vision", fill=C_GREEN, font=get_font(14, bold=True))
    d.text((320, 380), "Open Geospatial Public Infrastructure (WebGIS DPI)", fill=C_PURPLE, font=get_font(14, bold=True))
    
    # Center Label
    d.text((362, 230), "BHARAT\nSPECTRAL", fill=(255, 255, 255, 255), font=get_font(15, bold=True))
    
    im.save(os.path.join(ASSETS_DIR, "venn_diagram.png"))
    print("✓ Generated venn_diagram.png")

# 5. Slide 6: India HSI Coverage
def make_india_coverage():
    w, h = 840, 420
    im = Image.new("RGBA", (w, h), (248, 244, 235, 255))
    d = ImageDraw.Draw(im)
    
    d.text((24, 18), "Open Hyperspectral Corpus over the Indian Landmass", fill=C_DARK, font=get_font(20, bold=True))
    d.text((24, 46), "Phase 1 Complete • Automated Bhoonidhi & NASA STAC Ingestion Pipeline", fill=C_MUTED, font=get_font(13))
    
    # Left: Sensor Table
    tx, ty = 24, 90
    d.rectangle([tx, ty, tx + 400, ty + 300], fill=C_PARCHMENT, outline=C_BORDER, width=2)
    d.text((tx + 16, ty + 16), "Sensor Heterogeneity Specifications", fill=C_CYAN, font=get_font(15, bold=True))
    
    specs = [
        ("AVIRIS-NG India", "425 Bands • 4–8m GSD • 380–2510 nm"),
        ("ISRO HysIS", "220 Bands • 30m GSD • 400–2400 nm"),
        ("NASA EMIT (India)", "285 Bands • 60m GSD • 381–2493 nm"),
        ("Total Flightlines", "18+ Major Agro-Climatic Tracts"),
        ("Corpus Volume", "1.2 TB Analysis-Ready Tensors")
    ]
    for idx, (label, val) in enumerate(specs):
        sy = ty + 56 + idx * 46
        d.text((tx + 16, sy), label, fill=C_DARK, font=get_font(13, bold=True))
        d.text((tx + 16, sy + 18), val, fill=C_MUTED, font=get_font(12))
        d.line([(tx + 16, sy + 40), (tx + 384, sy + 40)], fill=(220, 210, 195), width=1)
        
    # Right: India Outline map representation
    mx, my = 460, 90
    d.rectangle([mx, my, mx + 350, my + 300], fill=C_PARCHMENT, outline=C_BORDER, width=2)
    d.text((mx + 16, my + 16), "National Footprint Coverage", fill=C_PURPLE, font=get_font(15, bold=True))
    
    # Draw simple stylized India bounding polygons
    india_pts = [
        (mx + 175, my + 60), (mx + 210, my + 100), (mx + 260, my + 130),
        (mx + 280, my + 180), (mx + 240, my + 230), (mx + 180, my + 280),
        (mx + 160, my + 240), (mx + 120, my + 180), (mx + 110, my + 130),
        (mx + 150, my + 90)
    ]
    d.polygon(india_pts, fill=(234, 224, 206, 180), outline=C_DARK, width=2)
    
    # Flight strips & points
    d.line([(mx + 130, my + 150), (mx + 160, my + 170)], fill=C_CYAN, width=4) # Gujarat Anand
    d.text((mx + 70, my + 160), "AVIRIS Anand", fill=C_CYAN, font=get_font(11, bold=True))
    
    d.line([(mx + 200, my + 190), (mx + 240, my + 210)], fill=C_GREEN, width=4) # Godavari Basin
    d.text((mx + 245, my + 200), "EMIT Godavari", fill=C_GREEN, font=get_font(11, bold=True))
    
    d.line([(mx + 160, my + 110), (mx + 190, my + 120)], fill=C_PURPLE, width=4) # Punjab/Haryana
    d.text((mx + 195, my + 110), "HysIS Ludhiana", fill=C_PURPLE, font=get_font(11, bold=True))

    im.save(os.path.join(ASSETS_DIR, "india_hsi_coverage.png"))
    print("✓ Generated india_hsi_coverage.png")

# 6. Slide 7: Preprocessing Pipeline
def make_preprocessing_pipeline():
    w, h = 840, 360
    im = Image.new("RGBA", (w, h), (255, 253, 245, 255))
    d = ImageDraw.Draw(im)
    
    d.text((24, 18), "4-Stage Preprocessing & Normalization Pipeline", fill=C_DARK, font=get_font(20, bold=True))
    d.text((24, 46), "From raw Bhoonidhi L1/L2 binaries to standardized machine learning tensors", fill=C_MUTED, font=get_font(13))
    
    stages = [
        ("Stage 1: 6S Correction", "Atmospheric water\nvapor & aerosol removal\nvia radiative 6S code", C_CYAN),
        ("Stage 2: Radiometric", "Integer scaling\n[0, 10000] -> [0.0, 1.0]\nsurface reflectance", C_GREEN),
        ("Stage 3: Band Masking", "Pruning 1.4μm & 1.9μm\natmospheric absorption\nzero-transmission gaps", C_AMBER),
        ("Stage 4: Tiling", "Sampling 9x9xB and\n15x15xB smallholder\nspatial-spectral patches", C_PURPLE)
    ]
    
    sx, sy = 24, 100
    card_w, card_h = 180, 180
    gap = 20
    for idx, (title, desc, col) in enumerate(stages):
        x = sx + idx * (card_w + gap)
        d.rectangle([x, sy, x + card_w, sy + card_h], fill=C_KRAFT, outline=col, width=2)
        d.rectangle([x, sy, x + card_w, sy + 38], fill=(col[0], col[1], col[2], 40))
        d.text((x + 10, sy + 10), title, fill=col, font=get_font(12, bold=True))
        d.text((x + 10, sy + 50), desc, fill=C_DARK, font=get_font(12))
        
        # Arrow
        if idx < 3:
            ax = x + card_w + 4
            ay = sy + card_h // 2
            d.line([(ax, ay), (ax + 12, ay)], fill=C_DARK, width=3)
            d.polygon([(ax + 12, ay - 5), (ax + 18, ay), (ax + 12, ay + 5)], fill=C_DARK)
            
    # Bottom callout
    d.rectangle([24, 300, 816, 344], fill=(234, 224, 206, 200), outline=C_BORDER)
    d.text((36, 312), "Tensors standardized with 200 clean bands across AVIRIS-NG India, HysIS, and NASA EMIT.", fill=C_MUTED, font=get_font(12, bold=True))

    im.save(os.path.join(ASSETS_DIR, "preprocessing_pipeline.png"))
    print("✓ Generated preprocessing_pipeline.png")

# 7. Slide 10: Timeline
def make_project_timeline():
    w, h = 840, 360
    im = Image.new("RGBA", (w, h), (248, 244, 235, 255))
    d = ImageDraw.Draw(im)
    
    d.text((24, 18), "Capstone Engineering Progression: 5-Phase Master Plan", fill=C_DARK, font=get_font(20, bold=True))
    d.text((24, 46), "Current Status: Phase 1 & 2 Completed • Entering Phase 3 Heavyweight Frontier", fill=C_MUTED, font=get_font(13))
    
    phases = [
        ("Phase 1", "Data Ingestion & Corpus", "● COMPLETE", C_GREEN),
        ("Phase 2", "Baselines & GIS Failure", "● COMPLETE", C_GREEN),
        ("Phase 3", "BharatSpectral-MAE Pretraining", "⚡ ACTIVE FRONTIER", C_RED),
        ("Phase 4", "Serverless Edge Engine (SSI)", "○ NEXT", C_MUTED),
        ("Phase 5", "WebGIS Public Infrastructure", "○ NEXT", C_MUTED)
    ]
    
    y = 100
    for idx, (p_title, p_desc, p_status, col) in enumerate(phases):
        py = y + idx * 46
        d.rectangle([24, py, 816, py + 38], fill=C_PARCHMENT, outline=C_BORDER)
        d.text((36, py + 10), p_title, fill=C_DARK, font=get_font(14, bold=True))
        d.text((150, py + 10), p_desc, fill=C_DARK, font=get_font(13))
        d.text((640, py + 10), p_status, fill=col, font=get_font(12, bold=True))
        
    im.save(os.path.join(ASSETS_DIR, "project_timeline.png"))
    print("✓ Generated project_timeline.png")

# 8. Slide 11: 7 Innovations Architecture
def make_seven_innovations_flowchart():
    w, h = 860, 420
    im = Image.new("RGBA", (w, h), (255, 253, 245, 255))
    d = ImageDraw.Draw(im)
    
    d.text((24, 18), "BharatSpectral-MAE: The 7 Core Architectural Innovations", fill=C_DARK, font=get_font(20, bold=True))
    d.text((24, 46), "Physics-informed Transformer engineered for Indian smallholder Earth Observation", fill=C_MUTED, font=get_font(13))
    
    innovations = [
        ("SHT", "Spectral Harmonic Tokenizer", "Chunks bands by diagnostic absorption density"),
        ("SSPE", "Scale-Spectral Positional Encoding", "Encodes spatial GSD (4-60m) & bandwidth together"),
        ("AAM", "Atmospheric Absorption Masking", "Structured masking of 1.4μm & 1.9μm water vapor gaps"),
        ("ECSA", "Endmember-Constrained Attention", "Regularizes self-attention via physical unmixing priors"),
        ("Ph-LoRA", "Phenology-Conditioned LoRA", "Adapts weights to Kharif / Rabi / Zaid seasonal drift"),
        ("RNRL", "Reflectance-Normalized Loss", "Preserves low-reflectance features (<5% in SWIR)"),
        ("FASU", "Foundation-Augmented Unmixing", "Sub-pixel unmixing head for non-linear canopies")
    ]
    
    # 2-column card layout
    for idx, (abbr, name, desc) in enumerate(innovations):
        col_idx = idx % 2
        row_idx = idx // 2
        cx = 24 + col_idx * 410
        cy = 90 + row_idx * 76
        
        card_w = 390
        card_h = 66
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=C_KRAFT, outline=C_CYAN if idx==0 else C_BORDER, width=2 if idx==0 else 1)
        d.rectangle([cx, cy, cx + 70, cy + card_h], fill=(11, 114, 133, 40))
        d.text((cx + 10, cy + 22), abbr, fill=C_CYAN, font=get_font(16, bold=True))
        d.text((cx + 82, cy + 12), name, fill=C_DARK, font=get_font(13, bold=True))
        d.text((cx + 82, cy + 34), desc, fill=C_MUTED, font=get_font(11))
        
    im.save(os.path.join(ASSETS_DIR, "seven_innovations_flowchart.png"))
    print("✓ Generated seven_innovations_flowchart.png")

# 9. Slide 12: Biochemical Taxonomy
def make_biochemical_taxonomy():
    w, h = 840, 420
    im = Image.new("RGBA", (w, h), (248, 244, 235, 255))
    d = ImageDraw.Draw(im)
    
    d.text((24, 18), "Multi-Domain Biochemical Diagnostics Yield", fill=C_DARK, font=get_font(20, bold=True))
    d.text((24, 46), "Continuous spectroscopic information across 6 national sectors", fill=C_MUTED, font=get_font(13))
    
    domains = [
        ("Precision Agriculture", "Leaf Nitrogen (2.1-2.3μm), Chlorophyll-a/b, Moisture (EWT), Yellow Rust Spores", C_GREEN),
        ("Soil Geochemistry", "Soil Organic Carbon (SOC), Salinity/EC, Kaolinite Clay, Iron Oxides", C_AMBER),
        ("Canal & Inland Water", "Chlorophyll-a (Algal blooms), Turbidity/TSS, CDOM, Industrial Effluent Plumes", C_CYAN),
        ("Forestry & Biomass", "Canopy Height, Lignin/Cellulose Ratios, Forest Fuel Moisture Desiccation", C_PURPLE),
        ("Geology & Minerals", "Hydroxyl Minerals (Al-OH, Mg-OH), Carbonates, Silicates, Lithium Pegmatites", C_RED),
        ("Urban & Disaster", "Asphalt Aging, PMFBY Inundation, Microplastic Film Detection", C_DARK)
    ]
    
    for idx, (title, items, col) in enumerate(domains):
        col_idx = idx % 2
        row_idx = idx // 2
        cx = 24 + col_idx * 400
        cy = 90 + row_idx * 100
        
        d.rectangle([cx, cy, cx + 380, cy + 86], fill=C_PARCHMENT, outline=col, width=2)
        d.text((cx + 14, cy + 12), title, fill=col, font=get_font(14, bold=True))
        d.text((cx + 14, cy + 38), items, fill=C_MUTED, font=get_font(11))
        
    im.save(os.path.join(ASSETS_DIR, "biochemical_taxonomy.png"))
    print("✓ Generated biochemical_taxonomy.png")

# 10. Slide 13: Farmer Mobile App UI
def make_farmer_mobile_app():
    w, h = 840, 420
    im = Image.new("RGBA", (w, h), (244, 236, 220, 255))
    d = ImageDraw.Draw(im)
    
    d.text((24, 18), "Democratized Public Delivery: Smallholder Mobile WebGIS", fill=C_DARK, font=get_font(20, bold=True))
    d.text((24, 46), "Zero-installation edge browser inference delivering actionable vernacular advisories", fill=C_MUTED, font=get_font(13))
    
    # Phone frame
    px, py = 280, 80
    pw, ph = 280, 320
    d.rectangle([px, py, px + pw, py + ph], fill=(20, 25, 35, 255), outline=C_DARK, width=3)
    
    # Phone screen
    d.rectangle([px + 12, py + 12, px + pw - 12, py + ph - 12], fill=(11, 15, 25, 255))
    
    # App header
    d.rectangle([px + 12, py + 12, px + pw - 12, py + 48], fill=(15, 29, 46, 255))
    d.text((px + 24, py + 22), "🛰️ BharatSpectral WebGIS", fill=C_CYAN, font=get_font(12, bold=True))
    
    # Field parcel heatmap
    d.rectangle([px + 24, py + 60, px + pw - 24, py + 180], fill=(30, 80, 50, 255), outline=C_GREEN, width=2)
    d.rectangle([px + 24, py + 60, px + 120, py + 120], fill=(160, 50, 40, 200)) # Deficit patch
    d.text((px + 32, py + 70), "N-Deficit", fill=(255, 255, 255), font=get_font(10, bold=True))
    d.text((px + 140, py + 130), "Parcel #42-B (0.6 ha)", fill=(255, 255, 255), font=get_font(10))
    
    # Vernacular Advisory Card
    d.rectangle([px + 24, py + 195, px + pw - 24, py + 295], fill=(255, 253, 245, 255), outline=C_BORDER)
    d.text((px + 32, py + 205), "🌾 KVK Advisory (Ludhiana)", fill=C_DARK, font=get_font(11, bold=True))
    d.text((px + 32, py + 225), "• Nitrogen deficit detected at 2.2μm\n• Apply 12 kg Urea in North plot\n• Skip South plot (Saved ₹450)", fill=C_MUTED, font=get_font(10))
    
    im.save(os.path.join(ASSETS_DIR, "farmer_mobile_app.png"))
    print("✓ Generated farmer_mobile_app.png")

# 11-14: Comics 1 through 4 (3-Panel Comic Strips)
def make_comic_strip(filename, comic_num, title, panels):
    w, h = 860, 380
    im = Image.new("RGBA", (w, h), (255, 253, 245, 255))
    d = ImageDraw.Draw(im)
    
    # Comic Header
    d.text((24, 16), f"Operational Scenario {comic_num}: {title}", fill=C_DARK, font=get_font(18, bold=True))
    
    pw = 256
    ph = 280
    for idx, (p_head, p_desc, col) in enumerate(panels):
        x = 24 + idx * (pw + 16)
        y = 60
        # Comic Panel Frame
        d.rectangle([x, y, x + pw, y + ph], fill=C_KRAFT, outline=C_DARK, width=2)
        
        # Panel header banner
        d.rectangle([x, y, x + pw, y + 36], fill=(col[0], col[1], col[2], 60))
        d.text((x + 10, y + 10), f"Panel {idx+1}: {p_head}", fill=col, font=get_font(12, bold=True))
        
        # Illustration placeholder graphic
        d.rectangle([x + 12, y + 48, x + pw - 12, y + 180], fill=(255, 255, 255, 200), outline=C_BORDER)
        # Inner decorative glyph
        glyphs = ["👁️ Naked Eye", "🛰️ Spectrometer", "📱 Action Alert"]
        d.text((x + 60, y + 100), glyphs[idx], fill=C_MUTED, font=get_font(14, bold=True))
        
        # Description text
        d.text((x + 12, y + 195), p_desc, fill=C_DARK, font=get_font(11))
        
    im.save(os.path.join(ASSETS_DIR, filename))
    print(f"✓ Generated {filename}")

def generate_comics():
    make_comic_strip(
        "comic1_invisible_hunger.png", 1, "The Invisible Hunger (Agriculture)",
        [
            ("Normal Green Canopy", "Farmer inspects wheat plot.\nCrop looks completely healthy\nand green to human vision.", C_GREEN),
            ("2.2μm Nitrogen Deficit", "Spaceborne spectrometer\nunmixes 2.1-2.3μm SWIR protein\ndeficit 10 days before yellowing.", C_CYAN),
            ("Targeted Micro-Dosing", "Vernacular SMS advisory\narrives; farmer top-dresses\nonly deficient zone (Saved 35%).", C_PURPLE)
        ]
    )
    make_comic_strip(
        "comic2_canal_lifeline.png", 2, "The Canal Lifeline (Canal Hydrology)",
        [
            ("Upstream Discharge", "Industrial effluent dumped\nupstream into rural agricultural\ndistributary canal system.", C_RED),
            ("Spectral Anomaly Spike", "Continuous 400-1000nm tracking\ndetects sudden toxic plume\nturbidity & absorption surge.", C_CYAN),
            ("Automated Sluice Gate", "Irrigation gate controller diverted\nbefore toxic plume inundates\nsaline smallholder fields.", C_GREEN)
        ]
    )
    make_comic_strip(
        "comic3_drought_warning.png", 3, "The 14-Day Moisture Warning (Climate)",
        [
            ("Dry Heat Spell", "High heat in Punjab/Haryana.\nLeaves appear outwardly\nunwilted during early stress.", C_AMBER),
            ("EWT Water Dip (970nm)", "Spectrometer detects cellular\nEquivalent Water Thickness\ndepletion in NIR/SWIR.", C_CYAN),
            ("Timely Tube-Well Pumping", "Advisory triggers micro-irrigation\n2 full weeks before visual\nstunting, saving the yield.", C_GREEN)
        ]
    )
    make_comic_strip(
        "comic4_salinity_defense.png", 4, "Salinity Encroachment (Soil Geochemistry)",
        [
            ("Rising Water Table", "Saline water table creeps\nsubsurface under fertile wheat\nplot without visible signs.", C_AMBER),
            ("Clay Lattice Shift", "SWIR absorption spectra at\n2.2μm detects subtle mineral\nalteration & electrical EC rise.", C_PURPLE),
            ("Gypsum Treatment", "Farmer receives soil amendment\nadvisory before irreversible\nwhite salt crusting forms.", C_GREEN)
        ]
    )

# 15. Slide 18: Democratization Drop
def make_democratization_slabs():
    w, h = 840, 360
    im = Image.new("RGBA", (w, h), (248, 244, 235, 255))
    d = ImageDraw.Draw(im)
    
    d.text((24, 18), "The Three-Fold Democratization Drop", fill=C_DARK, font=get_font(20, bold=True))
    d.text((24, 46), "Breaking computational, economic, and epistemic barriers for 140 million farmers", fill=C_MUTED, font=get_font(13))
    
    slabs = [
        ("1. Compute Barrier Smashed", "Cloud Multi-GPU Server ($500+/mo)  -->  ONNX Quantized Edge Inference (< 15 ms)", C_CYAN),
        ("2. Economic Egress Smashed", "AWS S3 Bandwidth Fees ($0.09 / GB)  -->  Cloudflare R2 Public WebGIS ($0 / month)", C_GREEN),
        ("3. Knowledge Barrier Smashed", "Esoteric Radiative Transfer Math  -->  Vernacular Color-Coded Phone Action Cards", C_PURPLE)
    ]
    
    for idx, (title, desc, col) in enumerate(slabs):
        sy = 90 + idx * 76
        d.rectangle([24, sy, 816, sy + 62], fill=C_PARCHMENT, outline=col, width=2)
        d.text((38, sy + 10), title, fill=col, font=get_font(14, bold=True))
        d.text((38, sy + 34), desc, fill=C_DARK, font=get_font(12, bold=True))
        
    im.save(os.path.join(ASSETS_DIR, "democratization_slabs.png"))
    print("✓ Generated democratization_slabs.png")

# 16. Slide 19: Sovereign Vision
def make_sovereign_vision():
    w, h = 840, 340
    im = Image.new("RGBA", (w, h), (255, 253, 245, 255))
    d = ImageDraw.Draw(im)
    
    d.text((24, 18), "BharatSpectral: Sovereign Foundation for Indian Earth Observation", fill=C_DARK, font=get_font(20, bold=True))
    d.text((24, 46), "A National Public Good Aligning Science, Artificial Intelligence, and Public Policy", fill=C_MUTED, font=get_font(13))
    
    pillars = [
        ("🌾 National Food Security", "Pre-symptomatic nitrogen & yellow rust diagnostics across 140M smallholders"),
        ("💧 Water & Ecological Defense", "Continuous monitoring of agricultural canals, industrial plumes, and inland lakes"),
        ("🛡️ Climate Adaptation", "14-day drought advance warnings and subsurface soil salinity reclamation")
    ]
    
    for idx, (p_title, p_desc) in enumerate(pillars):
        sy = 90 + idx * 64
        d.rectangle([24, sy, 816, sy + 52], fill=C_KRAFT, outline=C_BORDER)
        d.text((38, sy + 8), p_title, fill=C_CYAN if idx==0 else (C_GREEN if idx==1 else C_PURPLE), font=get_font(13, bold=True))
        d.text((38, sy + 28), p_desc, fill=C_DARK, font=get_font(11))
        
    d.text((300, 300), "Open for Committee Review & Defense Discussion", fill=C_MUTED, font=get_font(13, bold=True))
    im.save(os.path.join(ASSETS_DIR, "sovereign_vision.png"))
    print("✓ Generated sovereign_vision.png")

def main():
    print("Generating all presentation visual assets for BharatSpectral...")
    make_spectrum_contrast()
    make_continuous_spectroscopy()
    make_photon_pinball_cube()
    make_venn_diagram()
    make_india_coverage()
    make_preprocessing_pipeline()
    make_project_timeline()
    make_seven_innovations_flowchart()
    make_biochemical_taxonomy()
    make_farmer_mobile_app()
    generate_comics()
    make_democratization_slabs()
    make_sovereign_vision()
    print("All 16 visual assets generated successfully into presentation/assets/!")

if __name__ == "__main__":
    main()
