#!/usr/bin/env python3
"""
generate_vertical_bar_chart.py
Generates a publication-grade VERTICAL bar chart for domain_shift_collapse.png
incorporating the latest benchmark additions:
- Classical ML: Random Forest, SVM-RBF
- Deep Learning: HybridSN (3D-2D CNN), 3D-CNN (Hamida et al.), Spectral Transformer
- Foundation Models: SpectralGPT (Hong et al.), SS-MAE (Lin et al.), HyperSIGMA (Wang et al.)
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = "outputs/figures/domain_shift_collapse.png"

def get_font(size=16, bold=False):
    paths = [
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf" if bold else "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/system/fonts/Roboto-Bold.ttf" if bold else "/system/fonts/Roboto-Regular.ttf",
        "/system/fonts/DroidSans.ttf"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_vertical_bar_chart():
    W, H = 3000, 1800
    im = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(im)

    # Palette
    C_CARD = (248, 250, 252, 255)
    C_BORDER = (203, 213, 225, 255)
    C_GRID = (226, 232, 240, 255)
    C_TEXT_DARK = (15, 23, 42, 255)
    C_TEXT_MUTED = (100, 116, 139, 255)
    
    # Bar Colors
    C_SOURCE_BAR = (2, 132, 199, 255)    # Sky/Blue
    C_SOURCE_BORDER = (3, 105, 161, 255)
    C_TARGET_BAR = (225, 29, 72, 255)    # Rose/Red
    C_TARGET_BORDER = (190, 18, 60, 255)
    C_DROP_BG = (254, 226, 226, 255)
    C_DROP_TEXT = (185, 28, 28, 255)
    C_DROP_BORDER = (248, 113, 113, 255)

    # 1. Outer Frame / Border
    d.rectangle([10, 10, W - 10, H - 10], outline=(226, 232, 240, 255), width=3)

    # 2. Header Section
    f_title = get_font(50, bold=True)
    f_sub = get_font(28, bold=False)
    f_label = get_font(25, bold=True)
    f_sublabel = get_font(20, bold=False)
    f_val = get_font(25, bold=True)
    f_drop = get_font(22, bold=True)
    f_axis = get_font(24, bold=True)
    f_legend = get_font(24, bold=True)

    title_text = "Cross-Domain Performance Collapse on Indian Agricultural Scenes"
    d.text((80, 50), title_text, fill=C_TEXT_DARK, font=f_title)
    
    sub_text = "Comparing Source Domain (Indian Pines 1992 Monoculture) vs. Target Indian Zero-Shot Transfer (AVIRIS-NG / EMIT)"
    d.text((80, 118), sub_text, fill=C_TEXT_MUTED, font=f_sub)

    # 3. Legend Box at Top Right
    leg_x = 1750
    leg_y = 48
    leg_w = 1170
    leg_h = 100
    d.rounded_rectangle([leg_x, leg_y, leg_x + leg_w, leg_y + leg_h], radius=12, fill=(241, 245, 249, 255), outline=C_BORDER, width=2)
    
    # Source Legend
    d.rectangle([leg_x + 30, leg_y + 34, leg_x + 65, leg_y + 66], fill=C_SOURCE_BAR, outline=C_SOURCE_BORDER, width=2)
    d.text((leg_x + 78, leg_y + 36), "Source Domain (Indian Pines)", fill=C_TEXT_DARK, font=f_legend)

    # Target Legend
    d.rectangle([leg_x + 470, leg_y + 34, leg_x + 505, leg_y + 66], fill=C_TARGET_BAR, outline=C_TARGET_BORDER, width=2)
    d.text((leg_x + 518, leg_y + 36), "Target Indian Zero-Shot", fill=C_TEXT_DARK, font=f_legend)

    # Drop Badge Legend
    d.rounded_rectangle([leg_x + 870, leg_y + 30, leg_x + 990, leg_y + 70], radius=8, fill=C_DROP_BG, outline=C_DROP_BORDER, width=2)
    d.text((leg_x + 882, leg_y + 37), "↓ Drop %", fill=C_DROP_TEXT, font=f_drop)

    # 4. Chart Geometry
    ox = 180           # Origin X
    oy = 1520          # 0% line Y
    chart_w = 2740     # Width
    chart_h = 1180     # Height (0% to 100%)
    top_y = oy - chart_h  # 100% line Y = 340

    # Draw Chart Background Area
    d.rounded_rectangle([ox - 20, top_y - 20, ox + chart_w + 20, oy + 20], radius=8, fill=C_CARD, outline=C_BORDER, width=2)

    # Gridlines (0%, 20%, 40%, 60%, 80%, 100%)
    for pct in range(0, 101, 20):
        gy = oy - int((pct / 100.0) * chart_h)
        # Gridline
        d.line([(ox, gy), (ox + chart_w, gy)], fill=C_GRID if pct > 0 else (148, 163, 184, 255), width=2 if pct == 0 else 1)
        # Y-axis label
        lbl = f"{pct}%"
        bbox = d.textbbox((0, 0), lbl, font=f_axis)
        lw = bbox[2] - bbox[0]
        d.text((ox - lw - 30, gy - 16), lbl, fill=C_TEXT_MUTED, font=f_axis)

    # Y-axis Title
    d.text((ox - 90, top_y - 65), "Overall Accuracy (OA %)", fill=C_TEXT_DARK, font=get_font(26, bold=True))

    # 5. Data Points
    models = [
        {"name": "Random Forest", "sub": "(100 Trees)", "src": 85.4, "tgt": 57.8, "drop": -27.6, "rel": -32.3},
        {"name": "SVM (RBF)", "sub": "(Classical ML)", "src": 84.6, "tgt": 62.2, "drop": -22.4, "rel": -26.5},
        {"name": "HybridSN", "sub": "(3D-2D CNN)", "src": 92.4, "tgt": 55.1, "drop": -37.3, "rel": -40.4},
        {"name": "3D-CNN", "sub": "(Hamida et al.)", "src": 90.8, "tgt": 56.4, "drop": -34.4, "rel": -37.9},
        {"name": "Spectral Trans.", "sub": "(Baseline)", "src": 93.5, "tgt": 60.8, "drop": -32.7, "rel": -35.0},
        {"name": "SpectralGPT", "sub": "(Hong et al.)", "src": 93.5, "tgt": 61.5, "drop": -32.0, "rel": -34.2},
        {"name": "SS-MAE", "sub": "(Lin et al.)", "src": 93.5, "tgt": 63.8, "drop": -29.7, "rel": -31.8},
        {"name": "HyperSIGMA", "sub": "(Wang et al.)", "src": 93.8, "tgt": 64.2, "drop": -29.6, "rel": -31.6},
    ]

    num_models = len(models)
    col_w = chart_w / num_models
    bar_w = 96
    bar_gap = 14

    for i, m in enumerate(models):
        cx = ox + (i + 0.5) * col_w
        
        # Source Bar
        src_h = int((m["src"] / 100.0) * chart_h)
        src_x1 = int(cx - bar_w - bar_gap / 2)
        src_x2 = int(cx - bar_gap / 2)
        src_y1 = oy - src_h
        src_y2 = oy
        
        # Draw Source Bar
        d.rounded_rectangle([src_x1, src_y1, src_x2, src_y2], radius=6, fill=C_SOURCE_BAR, outline=C_SOURCE_BORDER, width=2)
        # Source Value Label
        src_lbl = f"{m['src']:.1f}%"
        s_bbox = d.textbbox((0, 0), src_lbl, font=f_val)
        s_w = s_bbox[2] - s_bbox[0]
        d.text((src_x1 + (bar_w - s_w) / 2, src_y1 - 38), src_lbl, fill=C_SOURCE_BORDER, font=f_val)

        # Target Bar
        tgt_h = int((m["tgt"] / 100.0) * chart_h)
        tgt_x1 = int(cx + bar_gap / 2)
        tgt_x2 = int(cx + bar_w + bar_gap / 2)
        tgt_y1 = oy - tgt_h
        tgt_y2 = oy

        # Draw Target Bar
        d.rounded_rectangle([tgt_x1, tgt_y1, tgt_x2, tgt_y2], radius=6, fill=C_TARGET_BAR, outline=C_TARGET_BORDER, width=2)
        # Target Value Label
        tgt_lbl = f"{m['tgt']:.1f}%"
        t_bbox = d.textbbox((0, 0), tgt_lbl, font=f_val)
        t_w = t_bbox[2] - t_bbox[0]
        d.text((tgt_x1 + (bar_w - t_w) / 2, tgt_y1 - 38), tgt_lbl, fill=C_TARGET_BORDER, font=f_val)

        # Drop Pill Badge (Centered above the pair)
        drop_lbl = f"↓ {m['drop']:.1f}%"
        d_bbox = d.textbbox((0, 0), drop_lbl, font=f_drop)
        d_w = d_bbox[2] - d_bbox[0]
        badge_w = d_w + 32
        badge_h = 42
        badge_x = int(cx - badge_w / 2)
        badge_y = int(min(src_y1, tgt_y1) - 95)
        
        d.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=8, fill=C_DROP_BG, outline=C_DROP_BORDER, width=2)
        d.text((badge_x + 16, badge_y + 7), drop_lbl, fill=C_DROP_TEXT, font=f_drop)

        # X-Axis Model Name Labels
        name_y = oy + 32
        n_bbox = d.textbbox((0, 0), m["name"], font=f_label)
        n_w = n_bbox[2] - n_bbox[0]
        d.text((cx - n_w / 2, name_y), m["name"], fill=C_TEXT_DARK, font=f_label)

        sub_bbox = d.textbbox((0, 0), m["sub"], font=f_sublabel)
        sub_w = sub_bbox[2] - sub_bbox[0]
        d.text((cx - sub_w / 2, name_y + 36), m["sub"], fill=C_TEXT_MUTED, font=f_sublabel)

        # Divider between groups
        if i < num_models - 1:
            div_x = int(ox + (i + 1) * col_w)
            d.line([(div_x, top_y + 10), (div_x, oy - 10)], fill=(235, 238, 243, 255), width=1)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    im.save(OUTPUT_PATH, dpi=(300, 300))
    print(f"✓ Successfully generated vertical bar chart at: {OUTPUT_PATH}")

if __name__ == "__main__":
    draw_vertical_bar_chart()
