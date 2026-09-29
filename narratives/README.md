# The Grand Narrative Primer (`narratives/`)

The **Grand Narrative** is a structured, 7-chapter foundational curriculum written to bridge hyperspectral spectroscopy physics, deep learning architecture, and Indian agricultural domain challenges.

---

## 📚 Chapter Index & Overview

| Chapter | Markdown Source | Topic & Scope |
|---|---|---|
| **00** | [`00_master_narrative_overview.md`](00_master_narrative_overview.md) | **Master Overview:** The philosophical vision, dual-pillar concept, and why BharatSpectral matters. |
| **01** | [`01_the_invisible_rainbow.md`](01_the_invisible_rainbow.md) | **Hyperspectral Physics:** Photon interactions, molecular bond vibrations ($C\text{--}H, O\text{--}H, N\text{--}H$), and atmospheric absorption windows. |
| **02** | [`02_how_ai_perceives_light.md`](02_how_ai_perceives_light.md) | **AI & Spectral Representation:** Progression from 1D/2D/3D CNNs to Transformers, Masked Autoencoding, and foundation paradigms. |
| **03** | [`03_the_seven_breakthroughs.md`](03_the_seven_breakthroughs.md) | **The 7 Breakthroughs:** Detailed mathematical and architectural mechanics of SSPE, RNRL, SHT, AAM, ECSA, Ph-LoRA, and FASU. |
| **04** | [`04_the_web_of_disciplines.md`](04_the_web_of_disciplines.md) | **Interdisciplinary Synthesis:** Unifying Agronomy, Radiometry, Machine Learning, and Public Policy into a coherent platform. |
| **05** | [`05_gis_baseline_vs_ai_brain.md`](05_gis_baseline_vs_ai_brain.md) | **GIS Baselines vs. AI:** Spectral Angle Mapper (SAM) & LSU vs. Non-linear Foundation Embeddings. |
| **06** | [`06_literature_references_and_reading_guide.md`](06_literature_references_and_reading_guide.md) | **Literature & Reading Guide:** Exhaustive citations, foundational papers, and annotated research guide. |

---

## 📄 Formatted PDFs (`pdfs/`)
Compiled publication-quality PDFs for all chapters are available in the [`pdfs/`](pdfs/) directory.

### Recompiling PDFs:
To rebuild PDFs after updating any Markdown chapter:
```bash
python3 narratives/convert_md_to_pdf.py
```
*Prerequisite:* `pip install reportlab`
