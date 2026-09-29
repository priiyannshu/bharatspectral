/**
 * deck.js
 * Interactive Presentation Engine for Jhajjar WQI Academic Pinboard Deck
 * Supports:
 * - Keyboard navigation (Arrow keys, Space, PageUp/Down, Home/End, 'F' for fullscreen)
 * - Number keys 1-9 and 0 for instant slide jump
 * - Fragment-by-fragment reveals
 * - Progress bar and indicator updates
 * - Fullscreen toggle
 * - Touch swipe gestures for mobile / tablets
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

  const slideTitles = [
    "Slide 1: Beyond Human Sight — Decoding Earth through Radiative Transfer",
    "Slide 2: Engineering Objectives — Capstone 7th Semester Scope",
    "Slide 3: Continuous Spectroscopy — What Each Spectral Band Captures",
    "Slide 4: The 'Pinball Machine' Physics & 3D Hyperspectral Data Cube",
    "Slide 5: The Intersection of Human Knowledge Systems",
    "Slide 6: Open Hyperspectral Corpus over the Indian Landmass",
    "Slide 7: Preprocessing & Physical Normalization Pipeline",
    "Slide 8: Benchmarking Previous Attempts — Empirical Proof of Need",
    "Slide 9: Why Existing Methods Fail in Indian Smallholder Ecosystems",
    "Slide 10: Project Progression — What is Done and The Road Ahead",
    "Slide 11: The 7 Core Architectural Innovations — Foundation Model",
    "Slide 12: Actionable Yield — Multi-Domain Biochemical Diagnostics",
    "Slide 13: Ground-Level Impact — The Farmer Mobile Experience",
    "Slide 14: Use Case 1 — Precision Nutrient Optimization (Invisible Hunger)",
    "Slide 15: Use Case 2 — Canal Water Quality Alert (Canal Lifeline)",
    "Slide 16: Use Case 3 — Early Drought Resilience (14-Day Warning)",
    "Slide 17: Use Case 4 — Soil Degradation Defense (Salinity Encroachment)",
    "Slide 18: Breaking the Barriers — Compute, Economics & Accessibility",
    "Slide 19: BharatSpectral — Sovereign Foundation for Indian Earth Observation"
  ];

  function updateSlide(index) {
    if (index < 0) index = 0;
    if (index >= totalSlides) index = totalSlides - 1;

    slides.forEach((s, idx) => {
      if (idx === index) {
        s.classList.add("active");
        // Auto-reveal all fragments if returning or navigating
        const fragments = s.querySelectorAll(".fragment");
        fragments.forEach(f => f.classList.add("revealed"));
      } else {
        s.classList.remove("active");
      }
    });

    currentSlide = index;

    // Update UI elements
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
  }

  function next() {
    // Check if there are unrevealed fragments on the current slide
    const activeSlide = slides[currentSlide];
    const unrevealed = activeSlide.querySelectorAll(".fragment:not(.revealed)");
    if (unrevealed.length > 0) {
      unrevealed[0].classList.add("revealed");
      return;
    }
    if (currentSlide < totalSlides - 1) {
      updateSlide(currentSlide + 1);
    }
  }

  function prev() {
    if (currentSlide > 0) {
      updateSlide(currentSlide - 1);
    }
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        console.warn(`Error attempting to enable fullscreen: ${err.message}`);
      });
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
  }

  // Keyboard Event Listeners
  window.addEventListener("keydown", (e) => {
    switch (e.key) {
      case "ArrowRight":
      case "ArrowDown":
      case "PageDown":
      case " ":
      case "n":
      case "N":
        e.preventDefault();
        next();
        break;

      case "ArrowLeft":
      case "ArrowUp":
      case "PageUp":
      case "Backspace":
      case "p":
      case "P":
        e.preventDefault();
        prev();
        break;

      case "Home":
        e.preventDefault();
        updateSlide(0);
        break;

      case "End":
        e.preventDefault();
        updateSlide(totalSlides - 1);
        break;

      case "f":
      case "F":
        e.preventDefault();
        toggleFullscreen();
        break;

      // Quick Jump to slides 1 to 9, and 0 for slide 10
      case "1": case "2": case "3": case "4": case "5":
      case "6": case "7": case "8": case "9":
        updateSlide(parseInt(e.key, 10) - 1);
        break;
      case "0":
        updateSlide(9);
        break;
    }
  });

  // Button Listeners
  if (prevBtn) prevBtn.addEventListener("click", prev);
  if (nextBtn) nextBtn.addEventListener("click", next);
  if (fullscreenBtn) fullscreenBtn.addEventListener("click", toggleFullscreen);

  // Touch Swipe Support
  let touchStartX = 0;
  let touchStartY = 0;
  window.addEventListener("touchstart", (e) => {
    touchStartX = e.changedTouches[0].screenX;
    touchStartY = e.changedTouches[0].screenY;
  }, { passive: true });

  window.addEventListener("touchend", (e) => {
    const touchEndX = e.changedTouches[0].screenX;
    const touchEndY = e.changedTouches[0].screenY;
    const diffX = touchEndX - touchStartX;
    const diffY = touchEndY - touchStartY;

    if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
      if (diffX < 0) {
        next();
      } else {
        prev();
      }
    }
  }, { passive: true });

  // Initialize first slide
  updateSlide(0);
});
