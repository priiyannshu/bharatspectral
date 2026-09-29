/**
 * deck.js
 * Interactive Presentation Engine for BharatSpectral Academic Pinboard Deck
 * 16-Slide Active Sequence across 4 Speakers:
 * - Speaker 1 (Slides 1-5): Foundation, Objectives, Web of Fields, Spectroscopy, 3D Data Cube
 * - Speaker 2 (Slides 6-9): India Coverage, Preprocessing, Benchmarks, Need for BharatSpectral
 * - Speaker 3 (Slide 10): Execution Progression & Roadmap (Phases 1 to 5)
 * - Speaker 4 (Slides 11-16): 4 Operational Comics, Literature References, Team & Supervisor Thank You
 */

document.addEventListener("DOMContentLoaded", () => {
  const slides = Array.from(document.querySelectorAll(".slide"));
  const totalSlides = slides.length;
  let currentSlide = 0;

  const slideCounterEl = document.getElementById("slideCounter");
  const slideTitleEl = document.getElementById("slideTitleIndicator");
  const progressBarEl = document.getElementById("progressBar");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const fullscreenBtn = document.getElementById("fullscreenBtn");
  const dialogueBtn = document.getElementById("dialogueBtn");
  const dialogueDrawer = document.getElementById("dialogueDrawer");
  const closeDialogueBtn = document.getElementById("closeDialogueBtn");
  const copyDialogueBtn = document.getElementById("copyDialogueBtn");
  const dialogueSlideNumEl = document.getElementById("dialogueSlideNum");
  const dialogueTitleEl = document.getElementById("dialogueTitle");
  const dialogueContentEl = document.getElementById("dialogueContent");

  const slideTitles = [
    "Slide 1: Beyond Human Sight — Democratized Spectral-Semantic Intelligence",
    "Slide 2: Project Objectives — Capstone Scope & Synergistic Goals",
    "Slide 3: The Web of Fields — Interdisciplinary Multi-Field Convergence",
    "Slide 4: Continuous Spectroscopy — The Chemical Barcode of Earth",
    "Slide 5: Hyperspectral Data Cube & Canopy Radiative Transfer",
    "Slide 6: Indian Landmass Hyperspectral Coverage & Sensor Heterogeneity",
    "Slide 7: Automated Preprocessing & Physical Normalization Pipeline",
    "Slide 8: Empirical Baseline Benchmarking & Failure Modes",
    "Slide 9: The Need for BharatSpectral — Smallholder Imperatives",
    "Slide 10: Project Progression: Phases 1 to 5 Roadmap",
    "Slide 11: Operational Scenario 1: The Invisible Hunger (Crop Nitrogen Deficit)",
    "Slide 12: Operational Scenario 2: The Canal Lifeline (Inland Water Quality)",
    "Slide 13: Operational Scenario 3: 14-Day Drought Warning (Cellular Water Stress)",
    "Slide 14: Operational Scenario 4: Salinity Encroachment (Soil Sodicity & Gypsum)",
    "Slide 15: Key Literature References — Foundational Academic Bibliography",
    "Slide 16: BharatSpectral: Team, Supervision & Concluding Discussion"
  ];

  const slideDialogues = [
    // Slide 1 - Speaker 1
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 1 (Slide 1 Opening)</span></p>
    <p>Good morning, respected committee members and faculty.</p>
    <p>We are creating a system that understands the language of <strong>radiative transfer and optical physics</strong> beyond human visual capabilities. As human beings, our vision is confined to a razor-thin 300-nanometer slice of visible light: Red, Green, and Blue. What we cannot see, we cannot diagnose.</p>
    <p>Every day, 140 million Indian smallholders look at their crops through these limited RGB eyes. But nature does not speak in RGB. The true biochemical language of Earth — cellular water stress, nitrogen deficiency, leaf carotenoids, and soil sodicity — is written across <strong>400 to 2,500 nanometers</strong> of continuous reflected solar radiation.</p>
    <p>This project bridges that perceptual chasm. This is <strong>BharatSpectral: Democratized Spectral-Semantic Intelligence (DSSI)</strong>.</p>`,

    // Slide 2 - Speaker 1
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 1 (Slide 2 Objectives)</span></p>
    <p>To systematically address this grand challenge, our capstone is structured around five concrete, testable objectives:</p>
    <p><strong>1. Data Acquisition & Benchmark Creation:</strong> Ingest heterogeneous hyperspectral cubes across AVIRIS-NG India (425 bands), ISRO HysIS (220 bands), and NASA EMIT (285 bands) to construct <strong>BharatHSI-Bench</strong> — India's first open, labeled smallholder agricultural benchmark.</p>
    <p><strong>2. Empirical Failure Proof:</strong> Rigorously evaluate global Foundation Models and classical baselines directly on BharatHSI-Bench, quantifying severe domain-shift degradation (22%–37% Overall Accuracy drop) over fragmented Indian plots.</p>
    <p><strong>3. Physics-Informed Foundation Model:</strong> Design <strong>BharatSpectral-MAE</strong>, introducing seven named architectural innovations to achieve state-of-the-art representations under Indian agricultural conditions.</p>
    <p><strong>4. Multi-Domain Biochemical Adaptation:</strong> Fine-tune foundation representations for downstream diagnostic tasks including nitrogen deficit mapping, soil organic carbon estimation, inland water quality, and soil salinity defense.</p>
    <p><strong>5. Democratized Public Delivery:</strong> Deploy an open, zero-cost WebGIS platform with sub-second Serverless Spectral Inference (SSI) via Cloudflare Workers and ONNX edge runtime, translating complex spectral tensors into direct vernacular farmer advisories.</p>`,

    // Slide 3 - Speaker 1
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 1 (Slide 3 Web of Fields)</span></p>
    <p>Respected committee members, true scientific breakthroughs cannot occur within the isolated silos of a single academic department.</p>
    <p>BharatSpectral sits at the confluence of seven distinct fields: <strong>Atmospheric Physics, Plant Physiology, Optical Spectroscopy, Self-Supervised Transformers, Cloudflare Edge Infrastructure, Smallholder Agronomy, and Public Policy</strong>.</p>
    <p>By synthesizing these seven domains into a unified framework, we ensure that every algorithm we design is physically grounded in spectroscopic reality and practically deployable as digital public infrastructure.</p>`,

    // Slide 4 - Speaker 1
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 1 (Slide 4 Continuous Spectroscopy)</span></p>
    <p>Slide 4 demonstrates the physical difference between standard multispectral imaging and continuous hyperspectral spectroscopy.</p>
    <p>Multispectral sensors like Sentinel-2 capture only 10 broad spectral bands. They can register that a crop is stressed, but cannot diagnose why. It is an alarm bell, but physically colorblind to chemistry.</p>
    <p>Hyperspectral sensors record 425 continuous 5-nanometer channels. This allows us to detect subtle biochemical signatures like the Chlorophyll Red-Edge slope inflection (680–740nm), cellular moisture absorption at 970nm and 1200nm, and leaf protein/nitrogen doublets at 2100–2300nm.</p>`,

    // Slide 5 - Speaker 1
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 1 (Slide 5 3D Data Cube)</span></p>
    <p>When solar photons enter a crop canopy, they undergo complex multi-bounce volumetric scattering between leaves, soil, and moisture droplets.</p>
    <p>The resulting 3D Hyperspectral Data Cube captures two spatial dimensions and one dense spectral dimension. Every pixel represents a continuous physical spectrum governed by radiative transfer, establishing the foundation for our deep learning pipeline.</p>
    <p>I now hand over to <strong>Speaker 2</strong> to discuss our real Indian Earth observation data sources and empirical benchmarks.</p>`,

    // Slide 6 - Speaker 2
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 2 (Slide 6 India Coverage)</span></p>
    <p>Thank you. Respected committee members, our research is anchored directly on real hyperspectral missions covering India.</p>
    <p>We leverage <strong>AVIRIS-NG India</strong>, flown collaboratively by ISRO and NASA with 425 spectral bands at high spatial resolution (4–8m GSD) over key agricultural corridors; <strong>NASA EMIT</strong> aboard the International Space Station with 285 channels at 60m GSD; and <strong>ISRO's HysIS</strong> satellite with 220 bands.</p>
    <p>Harmonizing these disparate datasets requires robust preprocessing, as shown in our next slide.</p>`,

    // Slide 7 - Speaker 2
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 2 (Slide 7 Preprocessing)</span></p>
    <p>Raw hyperspectral data straight from orbit contains atmospheric distortions, solar glare, water vapor absorption gaps, and detector noise.</p>
    <p>Our automated preprocessing assembly line processes raw flight lines through five standardized stages: radiometric calibration, atmospheric correction, bad-band removal around moisture absorption windows, spatial tiling tailored to smallholder plot scales, and tensor packing.</p>
    <p>This clean, standardized data forms the foundation of our benchmark evaluation.</p>`,

    // Slide 8 - Speaker 2
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 2 (Slide 8 Benchmarks)</span></p>
    <p>Can existing AI models be applied directly to Indian agricultural remote sensing? Our empirical evaluation proves they cannot.</p>
    <p>When evaluated on our testbed, leading architectures — from Random Forests and 3D-CNNs to modern Vision Transformers like SpectralGPT — suffer a severe collapse of <strong>22% to 37% in Overall Accuracy</strong>.</p>
    <p>These models were benchmarked on homogeneous Western monoculture fields (e.g. 40-hectare Indiana corn farms). On fragmented Indian smallholder farms with multi-crop intercropping, they fail.</p>`,

    // Slide 9 - Speaker 2
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 2 (Slide 9 Need for BharatSpectral)</span></p>
    <p>Why do we specifically need BharatSpectral? These four pinned requirements capture the core justification:</p>
    <p><strong>1. Sub-Pixel Spatial Fragmentation:</strong> Addressing smallholder plot mixing that breaks Western monoculture assumptions.</p>
    <p><strong>2. Multi-Sensor Heterogeneity:</strong> Unifying AVIRIS-NG, EMIT, and HysIS into a shared physical embedding space across varying GSDs.</p>
    <p><strong>3. Subtle Biochemical Absorption:</strong> Preserving faint chemical signals in the shortwave infrared (<5% reflectance) that standard MSE losses discard.</p>
    <p><strong>4. Democratized Accessibility:</strong> Replacing $10,000/seat proprietary desktop software with zero-cost edge browser inference for smallholders.</p>
    <p>To outline our technical roadmap across all project phases, I hand over to <strong>Speaker 3</strong>.</p>`,

    // Slide 10 - Speaker 3
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 3 (Slide 10 Project Progression)</span></p>
    <p>Respected committee members, our project execution spans five progressive phases.</p>
    <p>For our mid-term milestone, we have completed <strong>Phase 1: Data Acquisition & Preprocessing</strong>, assembling clean standardized datasets; and <strong>Phase 2: Baseline Benchmarking</strong>, demonstrating the 22% to 37% accuracy collapse across classical and deep learning models.</p>
    <p>Looking forward, <strong>Phase 3</strong> will engineer BharatSpectral-MAE, incorporating our physics-informed tokenization and loss formulations; <strong>Phase 4</strong> adapts representations across biochemical and stress downstream tasks; and <strong>Phase 5</strong> deploys our zero-cost edge WebGIS infrastructure.</p>
    <p>I will now pass to <strong>Speaker 4</strong> to demonstrate our operational use cases and conclude the presentation.</p>`,

    // Slide 11 - Speaker 4
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 4 (Slide 11 Use Case 1)</span></p>
    <p>Thank you. To illustrate the tangible real-world impact of BharatSpectral, we present four operational field scenarios.</p>
    <p>Scenario 1 addresses <strong>'The Invisible Hunger'</strong> — sub-visual crop nitrogen deficiency. Under standard RGB or multispectral satellite imaging, crops appear healthy green until cellular damage has already occurred.</p>
    <p>BharatSpectral analyzes diagnostic absorption dips at 2.1 to 2.3 microns, detecting nitrogen deficits two weeks earlier and generating precise micro-dosing advisories that save fertilizer costs and preserve yields.</p>`,

    // Slide 12 - Speaker 4
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 4 (Slide 12 Use Case 2)</span></p>
    <p>Scenario 2 addresses agricultural canal contamination and toxic algal blooms.</p>
    <p>Agricultural canals are vital lifelines across rural India, but run-off from chemical fertilizers triggers dangerous cyanobacteria blooms.</p>
    <p>By tracking phycocyanin absorption features at 620nm and unmixing industrial effluents from suspended sediments, BharatSpectral detects water toxicity before irrigation water reaches sensitive crop fields.</p>`,

    // Slide 13 - Speaker 4
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 4 (Slide 13 Use Case 3)</span></p>
    <p>Scenario 3 showcases pre-symptomatic moisture stress detection.</p>
    <p>When drought strikes, plant cell walls dehydrate long before leaves turn yellow or curl. Conventional satellites provide warnings only after visual wilting sets in.</p>
    <p>BharatSpectral tracks Equivalent Water Thickness across the 970nm and 1200nm water absorption windows, delivering <strong>14-day advance warnings</strong> that allow farmers to schedule protective irrigation before yield loss becomes irreversible.</p>`,

    // Slide 14 - Speaker 4
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 4 (Slide 14 Use Case 4)</span></p>
    <p>Scenario 4 focuses on soil salinity and sodicity reclamation.</p>
    <p>In irrigated canal tracts across northern and western India, secondary salinization silently degrades soil fertility. Surface visual checks cannot distinguish harmless white crusting from destructive soil sodicity.</p>
    <p>Using diagnostic shortwave infrared hydroxyl and carbonate absorption signatures, BharatSpectral maps subsurface soil health, directing targeted gypsum soil remediation before land degradation becomes permanent.</p>`,

    // Slide 15 - Speaker 4
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 4 (Slide 15 References)</span></p>
    <p>Our research builds upon foundational literature across hyperspectral Vision Transformers and spectroscopic unmixing.</p>
    <p>We ground our self-supervised learning on <strong>SpectralGPT, SS-MAE, and HyperSIGMA</strong>, while adapting scale-aware principles from <strong>Scale-MAE</strong> and physical unmixing constraints from <strong>Keshava & Mustard</strong>.</p>
    <p>These peer-reviewed foundations provide the theoretical rigor underlying our architecture.</p>`,

    // Slide 16 - Speaker 4
    `<p><span class="speaker-cue">🎙️ Presenter Script • Speaker 4 (Slide 16 Conclusion & Q&A)</span></p>
    <p>On behalf of our entire capstone team — Priyanshu and our fellow researchers — and with sincere gratitude to our project supervisor, we thank the respected evaluation committee and faculty members for your time and guidance.</p>
    <p>BharatSpectral represents our commitment to democratizing advanced spectral intelligence for Indian agriculture, ecology, and public science.</p>
    <p>We now welcome your questions, feedback, and discussion.</p>`
  ];

  function updateSlide(index) {
    if (index < 0 || index >= totalSlides) return;
    slides[currentSlide].classList.remove("active");
    slides[index].classList.add("active");
    currentSlide = index;

    if (slideCounterEl) {
      slideCounterEl.textContent = `${String(currentSlide + 1).padStart(2, "0")} / ${String(totalSlides).padStart(2, "0")}`;
    }

    if (slideTitleEl) {
      slideTitleEl.textContent = slideTitles[currentSlide] || `Slide ${currentSlide + 1}`;
    }

    if (progressBarEl) {
      const pct = ((currentSlide + 1) / totalSlides) * 100;
      progressBarEl.style.width = `${pct}%`;
    }

    if (prevBtn) prevBtn.disabled = currentSlide === 0;
    if (nextBtn) nextBtn.disabled = currentSlide === totalSlides - 1;

    updateDialogueContent();
  }

  function updateDialogueContent() {
    if (!dialogueDrawer) return;
    if (dialogueSlideNumEl) dialogueSlideNumEl.textContent = String(currentSlide + 1).padStart(2, "0");
    if (dialogueTitleEl) dialogueTitleEl.textContent = slideTitles[currentSlide] || `Slide ${currentSlide + 1}`;
    if (dialogueContentEl) {
      dialogueContentEl.innerHTML = slideDialogues[currentSlide] || "<p><em>No dialogue notes available for this slide.</em></p>";
    }
  }

  function toggleDialogueDrawer() {
    if (!dialogueDrawer) return;
    const isOpen = dialogueDrawer.classList.toggle("open");
    if (dialogueBtn) {
      dialogueBtn.classList.toggle("active", isOpen);
      dialogueBtn.setAttribute("aria-expanded", isOpen ? "true" : "false");
    }
    if (isOpen) updateDialogueContent();
  }

  function closeDialogue() {
    if (dialogueDrawer && dialogueDrawer.classList.contains("open")) {
      dialogueDrawer.classList.remove("open");
      if (dialogueBtn) dialogueBtn.classList.remove("active");
    }
  }

  function copyDialogueToClipboard() {
    if (!dialogueContentEl || !copyDialogueBtn) return;
    const textToCopy = dialogueContentEl.innerText;
    navigator.clipboard.writeText(textToCopy).then(() => {
      const origText = copyDialogueBtn.innerHTML;
      copyDialogueBtn.innerHTML = "✅ Copied!";
      setTimeout(() => { copyDialogueBtn.innerHTML = origText; }, 2000);
    }).catch(err => {
      console.error("Clipboard copy failed: ", err);
    });
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        console.warn("Fullscreen request error:", err);
      });
    } else {
      if (document.exitFullscreen) document.exitFullscreen();
    }
  }

  if (prevBtn) prevBtn.addEventListener("click", () => updateSlide(currentSlide - 1));
  if (nextBtn) nextBtn.addEventListener("click", () => updateSlide(currentSlide + 1));
  if (fullscreenBtn) fullscreenBtn.addEventListener("click", toggleFullscreen);
  if (dialogueBtn) dialogueBtn.addEventListener("click", toggleDialogueDrawer);
  if (closeDialogueBtn) closeDialogueBtn.addEventListener("click", closeDialogue);
  if (copyDialogueBtn) copyDialogueBtn.addEventListener("click", copyDialogueToClipboard);

  document.addEventListener("keydown", (e) => {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
    if (e.key === "ArrowRight" || e.key === " " || e.key === "PageDown" || e.key === "n" || e.key === "N") {
      e.preventDefault();
      updateSlide(currentSlide + 1);
    } else if (e.key === "ArrowLeft" || e.key === "PageUp" || e.key === "p" || e.key === "P") {
      e.preventDefault();
      updateSlide(currentSlide - 1);
    } else if (e.key === "Home") {
      e.preventDefault();
      updateSlide(0);
    } else if (e.key === "End") {
      e.preventDefault();
      updateSlide(totalSlides - 1);
    } else if (e.key === "f" || e.key === "F") {
      e.preventDefault();
      toggleFullscreen();
    } else if (e.key === "d" || e.key === "D" || e.key === "s" || e.key === "S") {
      e.preventDefault();
      toggleDialogueDrawer();
    } else if (e.key === "Escape") {
      closeDialogue();
    } else if (!isNaN(e.key) && parseInt(e.key) >= 1 && parseInt(e.key) <= 9) {
      const slideIndex = parseInt(e.key) - 1;
      if (slideIndex < totalSlides) updateSlide(slideIndex);
    }
  });

  // Touch Swipe gestures
  let touchStartX = 0;
  let touchStartY = 0;
  document.addEventListener("touchstart", (e) => {
    touchStartX = e.changedTouches[0].screenX;
    touchStartY = e.changedTouches[0].screenY;
  }, { passive: true });

  document.addEventListener("touchend", (e) => {
    const diffX = e.changedTouches[0].screenX - touchStartX;
    const diffY = e.changedTouches[0].screenY - touchStartY;
    if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 40) {
      if (diffX < 0) updateSlide(currentSlide + 1);
      else updateSlide(currentSlide - 1);
    }
  }, { passive: true });

  updateSlide(0);
  console.log("✓ BharatSpectral 16-Slide Presentation initialized successfully.");
});
