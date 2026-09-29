#!/usr/bin/env python3
"""
Convert gn/ markdown files to styled PDFs using ReportLab.
Handles: headings (H1-H4), paragraphs, bold, italic, inline code,
code blocks, bullet lists, numbered lists, horizontal rules.
"""

import re
import os
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Preformatted, ListFlowable, ListItem, KeepTogether
)

# ─── Colour palette ───────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#1a3a5c")
MID_BLUE    = colors.HexColor("#2d6a9f")
ACCENT      = colors.HexColor("#e67e22")
LIGHT_GRAY  = colors.HexColor("#f5f5f5")
DARK_GRAY   = colors.HexColor("#333333")
CODE_BG     = colors.HexColor("#f0f0f0")
HR_COLOR    = colors.HexColor("#cccccc")

PAGE_W, PAGE_H = A4
MARGIN = 1.1 * inch

# ─── Style sheet ──────────────────────────────────────────────────────────────

def make_styles():
    styles = {}

    styles["h1"] = ParagraphStyle(
        "H1",
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=DARK_BLUE,
        spaceAfter=14,
        spaceBefore=6,
        alignment=TA_LEFT,
    )
    styles["h2"] = ParagraphStyle(
        "H2",
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=22,
        textColor=MID_BLUE,
        spaceAfter=8,
        spaceBefore=16,
    )
    styles["h3"] = ParagraphStyle(
        "H3",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=18,
        textColor=DARK_BLUE,
        spaceAfter=6,
        spaceBefore=12,
    )
    styles["h4"] = ParagraphStyle(
        "H4",
        fontName="Helvetica-BoldOblique",
        fontSize=11,
        leading=15,
        textColor=MID_BLUE,
        spaceAfter=4,
        spaceBefore=8,
    )
    styles["body"] = ParagraphStyle(
        "Body",
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        textColor=DARK_GRAY,
        spaceAfter=7,
        alignment=TA_JUSTIFY,
    )
    styles["bullet"] = ParagraphStyle(
        "Bullet",
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        textColor=DARK_GRAY,
        leftIndent=18,
        spaceAfter=3,
        bulletIndent=6,
    )
    styles["code"] = ParagraphStyle(
        "Code",
        fontName="Courier",
        fontSize=8.5,
        leading=13,
        textColor=DARK_GRAY,
        backColor=CODE_BG,
        leftIndent=12,
        rightIndent=12,
        spaceAfter=8,
        spaceBefore=4,
    )
    return styles


# ─── Inline markdown → ReportLab XML ──────────────────────────────────────────

def escape_xml(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text

def inline_format(text):
    text = escape_xml(text)
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)
    text = re.sub(r'`([^`]+)`', r'<font name="Courier" size="9"><b>\1</b></font>', text)
    return text


# ─── Markdown line parser → flowables ─────────────────────────────────────────

def parse_md(md_text, styles):
    lines = md_text.splitlines()
    flowables = []

    in_code_block = False
    code_lines = []
    list_items = []
    in_list = False

    def flush_list():
        nonlocal list_items, in_list
        if not list_items:
            return
        items = []
        for (ordered, indent, txt) in list_items:
            bullet = "•" if not ordered else None
            p = Paragraph(inline_format(txt), styles["bullet"])
            items.append(ListItem(p, leftIndent=indent * 12 + 18, value=bullet))
        flowables.append(ListFlowable(
            items,
            bulletType="bullet",
            leftIndent=6,
            spaceAfter=4,
        ))
        list_items.clear()
        in_list = False

    def flush_code():
        nonlocal code_lines, in_code_block
        if code_lines:
            code_text = "\n".join(code_lines)
            flowables.append(Preformatted(code_text, styles["code"]))
        code_lines.clear()
        in_code_block = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Code fence
        if line.strip().startswith("```"):
            if in_code_block:
                flush_code()
            else:
                flush_list()
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^[-*_]{3,}\s*$', line.strip()):
            flush_list()
            flowables.append(Spacer(1, 6))
            flowables.append(HRFlowable(width="100%", thickness=0.8, color=HR_COLOR))
            flowables.append(Spacer(1, 6))
            i += 1
            continue

        # Headings
        m = re.match(r'^(#{1,4})\s+(.*)', line)
        if m:
            flush_list()
            level = len(m.group(1))
            text = m.group(2).strip()
            sk = f"h{min(level, 4)}"
            flowables.append(Paragraph(inline_format(text), styles[sk]))
            i += 1
            continue

        # Bullet list
        bm = re.match(r'^(\s*)[-*+]\s+(.*)', line)
        if bm:
            indent_lvl = len(bm.group(1)) // 2
            list_items.append((False, indent_lvl, bm.group(2)))
            in_list = True
            i += 1
            continue

        # Numbered list
        nm = re.match(r'^(\s*)\d+[.)]\s+(.*)', line)
        if nm:
            indent_lvl = len(nm.group(1)) // 2
            list_items.append((True, indent_lvl, nm.group(2)))
            in_list = True
            i += 1
            continue

        # Blank line
        if not line.strip():
            flush_list()
            flowables.append(Spacer(1, 4))
            i += 1
            continue

        # Normal paragraph — collect continuation lines
        flush_list()
        para_lines = [line]
        while i + 1 < len(lines):
            nxt = lines[i + 1]
            if (not nxt.strip()
                    or nxt.strip().startswith("#")
                    or nxt.strip().startswith("```")
                    or re.match(r'^(\s*)[-*+]\s+', nxt)
                    or re.match(r'^(\s*)\d+[.)]\s+', nxt)
                    or re.match(r'^[-*_]{3,}\s*$', nxt.strip())):
                break
            para_lines.append(nxt)
            i += 1
        text = " ".join(para_lines)
        try:
            flowables.append(Paragraph(inline_format(text), styles["body"]))
        except Exception:
            flowables.append(Paragraph(escape_xml(text), styles["body"]))
        i += 1

    flush_list()
    if in_code_block:
        flush_code()

    return flowables


# ─── PDF builder ──────────────────────────────────────────────────────────────

def md_to_pdf(md_path: Path, out_path: Path):
    styles = make_styles()
    md_text = md_path.read_text(encoding="utf-8")

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN + 0.1 * inch,
        bottomMargin=MARGIN,
        title=md_path.stem.replace("_", " ").title(),
        author="BharatSpectral",
    )

    story = parse_md(md_text, styles)

    def header_footer(canvas, doc):
        canvas.saveState()
        w, h = A4
        # Header bar
        canvas.setFillColor(DARK_BLUE)
        canvas.rect(0, h - 0.42 * inch, w, 0.42 * inch, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(MARGIN, h - 0.27 * inch, "BharatSpectral")
        canvas.setFont("Helvetica", 8)
        title_txt = md_path.stem.replace("_", " ").replace("-", " ").title()
        canvas.drawRightString(w - MARGIN, h - 0.27 * inch, title_txt)
        # Footer
        canvas.setFillColor(HR_COLOR)
        canvas.rect(0, 0, w, 0.32 * inch, fill=1, stroke=0)
        canvas.setFillColor(DARK_GRAY)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(MARGIN, 0.11 * inch, "BharatSpectral — Dual-Pillar DSSI Framework")
        canvas.drawRightString(w - MARGIN, 0.11 * inch, f"Page {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"  ✓  {out_path.name}")


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    gn_dir = Path(__file__).parent

    md_files = sorted([p for p in gn_dir.glob("*.md") if not p.name.lower().startswith("readme")])
    if not md_files:
        print("No .md files found in gn/")
        sys.exit(1)

    pdf_dir = gn_dir / "pdfs"
    pdf_dir.mkdir(exist_ok=True)

    print(f"Converting {len(md_files)} markdown file(s) → PDF ...\n")
    errors = []
    for md in md_files:
        out = pdf_dir / (md.stem + ".pdf")
        try:
            md_to_pdf(md, out)
        except Exception as e:
            print(f"  ✗  {md.name}: {e}")
            import traceback; traceback.print_exc()
            errors.append(md.name)

    print(f"\nDone. PDFs saved to: {pdf_dir}")
    if errors:
        print(f"Errors: {errors}")
        sys.exit(1)
