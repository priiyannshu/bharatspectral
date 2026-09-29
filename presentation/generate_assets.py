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
C_ORANGE = (217, 72, 15, 255)
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

def make_venn_diagram():
    w, h = 1280, 720
    im = Image.new("RGBA", (w, h), (255, 253, 245, 255))
    d = ImageDraw.Draw(im)
    
    font_title = get_font(36, bold=True)
    title = "The Web of Fields: 7-Disciplinary Convergence"
    tw = d.textlength(title, font=font_title)
    d.text((w//2 - tw//2, 40), title, fill=C_DARK, font=font_title)
    
    cx, cy = 640, 400
    R = 170
    r_circ = 200
    
    fields = [
        {"name": "Deep Learning", "angle": -90, "color": (217, 72, 15), "asset": "seven_innovations_flowchart.png"},
        {"name": "Computer Vision", "angle": -38.57, "color": (43, 138, 62), "asset": "photon_pinball_cube.png"},
        {"name": "Software\nEngineering", "angle": 12.86, "color": (11, 114, 133), "asset": "preprocessing_pipeline.png"},
        {"name": "Digital Public\nInfrastructure", "angle": 64.29, "color": (103, 65, 217), "asset": "farmer_mobile_app.png"},
        {"name": "Geoinformatics", "angle": 115.71, "color": (59, 130, 246), "asset": "india_hsi_coverage.png"},
        {"name": "Optical Physics", "angle": 167.14, "color": (217, 155, 0), "asset": "continuous_spectroscopy.png"},
        {"name": "Radiative Transfer\nPhysics", "angle": 218.57, "color": (201, 42, 42), "asset": "photon_pinball_cube.png"}
    ]
    
    circ_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    
    for f in fields:
        ang_rad = math.radians(f["angle"])
        fx = int(cx + R * math.cos(ang_rad))
        fy = int(cy + R * math.sin(ang_rad))
        
        col = f["color"]
        
        asset_p = os.path.join(ASSETS_DIR, f["asset"])
        bg_img = Image.new("RGBA", (r_circ*2, r_circ*2), (col[0], col[1], col[2], 90))
        
        has_img = False
        if os.path.exists(asset_p):
            try:
                with Image.open(asset_p) as src:
                    src = src.convert("RGBA")
                    src_w, src_h = src.size
                    scale = max(r_circ*2 / src_w, r_circ*2 / src_h)
                    new_w, new_h = int(src_w * scale), int(src_h * scale)
                    resized = src.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    left = (new_w - r_circ*2)//2
                    top = (new_h - r_circ*2)//2
                    cropped = resized.crop((left, top, left + r_circ*2, top + r_circ*2))
                    
                    tint = Image.new("RGBA", (r_circ*2, r_circ*2), (col[0], col[1], col[2], 160))
                    blended = Image.alpha_composite(cropped, tint)
                    
                    mask = Image.new("L", (r_circ*2, r_circ*2), 0)
                    ImageDraw.Draw(mask).ellipse([0, 0, r_circ*2, r_circ*2], fill=140)
                    blended.putalpha(mask)
                    bg_img = blended
                    has_img = True
            except Exception:
                pass
        
        if not has_img:
            mask = Image.new("L", (r_circ*2, r_circ*2), 0)
            ImageDraw.Draw(mask).ellipse([0, 0, r_circ*2, r_circ*2], fill=90)
            bg_img.putalpha(mask)
            
        circ_layer.alpha_composite(bg_img, (fx - r_circ, fy - r_circ))

    im = Image.alpha_composite(im, circ_layer)
    d = ImageDraw.Draw(im)
    
    font_field = get_font(18, bold=True)
    for f in fields:
        ang_rad = math.radians(f["angle"])
        fx = int(cx + R * math.cos(ang_rad))
        fy = int(cy + R * math.sin(ang_rad))
        col = f["color"]
        
        d.ellipse([fx - r_circ, fy - r_circ, fx + r_circ, fy + r_circ], outline=(col[0], col[1], col[2], 200), width=3)
        
        # text position
        dist = R + r_circ - 30
        if f["angle"] in [-90]:
            dist = R + r_circ - 50
        tx = cx + dist * math.cos(ang_rad)
        ty = cy + dist * math.sin(ang_rad)
        
        lines = f["name"].split("\n")
        total_h = len(lines) * 22
        start_y = ty - total_h/2
        
        max_lw = max([d.textlength(line, font=font_field) for line in lines])
        
        bx0 = tx - max_lw/2 - 16
        bx1 = tx + max_lw/2 + 16
        by0 = start_y - 8
        by1 = start_y + total_h + 8
        
        d.rounded_rectangle([bx0, by0, bx1, by1], radius=12, fill=(255, 255, 255, 230), outline=col, width=2)
        
        for i, line in enumerate(lines):
            lw = d.textlength(line, font=font_field)
            d.text((tx - lw/2, start_y + i*22 + 2), line, fill=col, font=font_field)
            
    # Center text
    font_center_main = get_font(26, bold=True)
    font_center_sub = get_font(16, bold=True)
    d.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], fill=(255, 255, 255, 255), outline=(42, 35, 27), width=4)
    
    c_tw1 = d.textlength("BHARAT", font=font_center_main)
    c_tw2 = d.textlength("SPECTRAL", font=font_center_main)
    d.text((cx - c_tw1/2, cy - 45), "BHARAT", fill=(217, 155, 0), font=font_center_main)
    d.text((cx - c_tw2/2, cy - 15), "SPECTRAL", fill=(217, 155, 0), font=font_center_main)
    
    d.line([(cx - 60, cy + 20), (cx + 60, cy + 20)], fill=(200, 200, 200), width=2)
    
    c_tw3 = d.textlength("DSSI", font=font_center_sub)
    d.text((cx - c_tw3/2, cy + 30), "DSSI", fill=C_DARK, font=font_center_sub)
    c_tw4 = d.textlength("Intersection", font=get_font(12))
    d.text((cx - c_tw4/2, cy + 50), "Intersection", fill=(100,100,100), font=get_font(12))

    im.save(os.path.join(ASSETS_DIR, "venn_diagram.png"))
    im.convert("RGB").save(os.path.join(ASSETS_DIR, "venn_diagram.jpg"), quality=95)
    print("✓ Generated aesthetic 7-Field venn_diagram.png & venn_diagram.jpg")

# 5. Slide 6: India HSI Coverage

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

# 6. Slide 7: Preprocessing Pipeline (Lightweight Factory Line Visual)
def make_preprocessing_pipeline():
    w, h = 1080, 380
    im = Image.new("RGBA", (w, h), (253, 250, 242, 255))
    d = ImageDraw.Draw(im)
    
    # Factory Conveyor Track Background
    track_y = 212
    track_h = 30
    for leg_x in [100, 315, 530, 745, 960]:
        d.rectangle([leg_x, track_y + track_h - 2, leg_x + 10, track_y + track_h + 20], fill=(90, 56, 24))
    
    d.rounded_rectangle([15, track_y, 1065, track_y + track_h], radius=5, fill=(66, 40, 19), outline=(115, 74, 38), width=2)
    d.rounded_rectangle([20, track_y + 4, 1060, track_y + track_h - 4], radius=3, fill=(42, 31, 24))
    
    for rx in [45, 260, 475, 690, 905, 1035]:
        d.ellipse([rx - 8, track_y + 7, rx + 8, track_y + 23], fill=(168, 130, 87), outline=(61, 35, 13), width=2)
        d.ellipse([rx - 2, track_y + 13, rx + 2, track_y + 17], fill=(61, 35, 13))

    for ax in [160, 375, 590, 805]:
        d.polygon([(ax, track_y + 12), (ax + 10, track_y + 15), (ax, track_y + 18)], fill=(255, 209, 128))
        d.polygon([(ax + 14, track_y + 12), (ax + 24, track_y + 15), (ax + 14, track_y + 18)], fill=(255, 209, 128))

    stations = [
        {
            "num": "01", "name": "RAW CAPTURE", "col": (108, 117, 125), "head_bg": (241, 243, 245),
            "main": "Raw Earth Feeds", "sub1": "Captured scans from", "sub2": "satellites & aircraft",
            "pill": "Noisy & Distorted Feeds", "pill_bg": (233, 236, 239), "payload": "RAW DN"
        },
        {
            "num": "02", "name": "HAZE REMOVAL", "col": C_CYAN, "head_bg": (227, 250, 252),
            "main": "Strip Atmosphere", "sub1": "Removes air haze, dust", "sub2": "& solar glare distortion",
            "pill": "True Surface Reflections", "pill_bg": (197, 246, 250), "payload": "TOC ρ"
        },
        {
            "num": "03", "name": "NOISE FILTER", "col": C_ORANGE, "head_bg": (255, 244, 230),
            "main": "Cut Dead Bands", "sub1": "Prunes water vapor gaps;", "sub2": "keeps 200 purest channels",
            "pill": "200 Diagnostic Bands", "pill_bg": (255, 232, 204), "payload": "200 BANDS"
        },
        {
            "num": "04", "name": "FIELD CROPPING", "col": C_PURPLE, "head_bg": (243, 240, 255),
            "main": "Smallholder Tiles", "sub1": "Screens clouds & slices", "sub2": "into Indian farm patches",
            "pill": "Uniform Farm Patches", "pill_bg": (229, 219, 255), "payload": "PATCHES"
        },
        {
            "num": "05", "name": "AI-READY TENSORS", "col": C_GREEN, "head_bg": (235, 251, 238),
            "main": "Clean Benchmark", "sub1": "Standardized & indexed", "sub2": "for instant neural training",
            "pill": "⚡ Ready for Phase 3", "pill_bg": (211, 249, 216), "payload": "AI TENSOR"
        }
    ]

    sx = 15
    sw = 195
    gap = 20
    for idx, st in enumerate(stations):
        x = sx + idx * (sw + gap)
        d.rounded_rectangle([x, 15, x + sw, 165], radius=6, fill=(255, 255, 255), outline=st["col"], width=2)
        d.rounded_rectangle([x, 15, x + sw, 45], radius=6, fill=st["head_bg"])
        d.line([(x, 45), (x + sw, 45)], fill=st["col"], width=1)
        
        d.text((x + 10, 24), f"{st['num']} • {st['name']}", fill=st["col"], font=get_font(11, bold=True))
        d.text((x + 10, 58), st["main"], fill=C_DARK, font=get_font(12, bold=True))
        d.text((x + 10, 78), st["sub1"], fill=C_MUTED, font=get_font(10))
        d.text((x + 10, 94), st["sub2"], fill=C_MUTED, font=get_font(10))
        
        d.rounded_rectangle([x + 8, 125, x + sw - 8, 150], radius=4, fill=st["pill_bg"])
        d.text((x + 14, 131), st["pill"], fill=st["col"], font=get_font(9, bold=True))
        
        cx = x + sw // 2
        d.line([(cx, 165), (cx, 192)], fill=st["col"], width=2)
        d.ellipse([cx - 3, 190, cx + 3, 196], fill=st["col"])
        
        px = cx - 20
        d.rounded_rectangle([px, 200, px + 40, 222], radius=3, fill=st["head_bg"], outline=st["col"], width=2)
        d.text((px + 4, 204), st["payload"], fill=st["col"], font=get_font(8, bold=True))

    # Bottom Linear Flow Summary
    d.rounded_rectangle([15, 290, 1065, 360], radius=6, fill=(252, 250, 246), outline=C_BORDER, width=1)
    
    flow_items = [
        ("1. Raw Scans", "Spaceborne capture", (108, 117, 125)),
        ("2. Atmosphere Cleared", "Sun glare & haze removed", C_CYAN),
        ("3. 200 Pure Channels", "Dead noise bands pruned", C_ORANGE),
        ("4. Farm-Scale Patches", "Sliced to Indian plot sizes", C_PURPLE),
        ("5. Phase 3 AI-Ready", "Clean input for Model", C_GREEN)
    ]
    
    for idx, (title, desc, col) in enumerate(flow_items):
        fx = 30 + idx * 210
        d.text((fx, 305), title, fill=col, font=get_font(10, bold=True))
        d.text((fx, 323), desc, fill=C_MUTED, font=get_font(9))
        if idx < 4:
            d.text((fx + 165, 310), "→", fill=(140, 123, 107), font=get_font(14, bold=True))

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

def preserve_or_generate(func, filename):
    target = os.path.join(ASSETS_DIR, filename)
    jpg_target = os.path.join(ASSETS_DIR, os.path.splitext(filename)[0] + ".jpg")
    if os.path.exists(jpg_target) or (os.path.exists(target) and os.path.getsize(target) > 100000):
        print(f"✓ Preserving high-resolution AI generated asset: {filename}")
        return
    func()

def main():
    print("Verifying presentation visual assets for BharatSpectral...")
    preserve_or_generate(make_spectrum_contrast, "spectrum_contrast.png")
    preserve_or_generate(make_continuous_spectroscopy, "continuous_spectroscopy.png")
    preserve_or_generate(make_photon_pinball_cube, "photon_pinball_cube.png")
    make_venn_diagram()  # Always re-generate updated Venn diagram
    preserve_or_generate(make_india_coverage, "india_hsi_coverage.png")
    make_preprocessing_pipeline()  # Always re-generate updated factory line asset
    preserve_or_generate(make_project_timeline, "project_timeline.png")
    preserve_or_generate(generate_comics, "comic1_invisible_hunger.png")
    print("All presentation visual assets verified and ready in presentation/assets/!")

if __name__ == "__main__":
    main()
