# BharatSpectral Presentation Decks (`presentation/`)

This directory houses the presentation artifacts and automated deck generation scripts for midterm reviews, committee defenses, and public demonstrations.

---

## 📽️ Files & Deliverables

| File | Type | Description |
|---|---|---|
| [`BharatSpectral_MidTerm_Presentation.pptx`](BharatSpectral_MidTerm_Presentation.pptx) | PPTX | 16-Slide executive 16:9 widescreen presentation deck styled with high-tech custom dark cards and infographics. |
| [`presentation.html`](presentation.html) | HTML | Interactive, keyboard-navigable slide deck with speaker notes, live diagram renders, and progress tracker. |
| [`build_deck.py`](build_deck.py) | Python | Programmatic compiler for `BharatSpectral_MidTerm_Presentation.pptx` using `python-pptx`. |
| [`build_html_deck.py`](build_html_deck.py) | Python | Generator for the standalone interactive `presentation.html` web presentation. |

---

## 🛠️ How to Regenerate Slide Decks

### 1. Rebuild PowerPoint (`.pptx`)
```bash
python3 presentation/build_deck.py
```
*Prerequisite:* `pip install python-pptx`

### 2. Rebuild Web Slide Deck (`.html`)
```bash
python3 presentation/build_html_deck.py
```
*Output:* Opens directly in any web browser (`presentation/presentation.html`).

---

## ⌨️ Interactive Web Deck Controls (`presentation.html`)
* `→` / `Space` / `Page Down` : Next slide
* `←` / `Page Up` : Previous slide
* `Home` / `End` : Jump to first / last slide
* `N` : Toggle speaker notes drawer
* `F` : Toggle fullscreen

---

## 🌐 Cloudflare Pages Deployment

* **Live URL:** [https://bharatspectral.pages.dev/](https://bharatspectral.pages.dev/)
* **Direct PPTX Download:** [https://bharatspectral.pages.dev/BharatSpectral_MidTerm_Presentation.pptx](https://bharatspectral.pages.dev/BharatSpectral_MidTerm_Presentation.pptx)

To rebuild and deploy latest changes:
```bash
./deploy.sh
```
*(Can be executed from repository root `~/btp` or `presentation/`)*
