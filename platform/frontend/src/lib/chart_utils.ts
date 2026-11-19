/**
 * chart_utils.ts - Ultra-Smooth HTML5 Canvas 425-Band Spectral Curve Renderer
 */

export interface ChartRenderOptions {
  showConvexHull?: boolean;
  showContinuumRemoved?: boolean;
  showReferenceCurves?: boolean;
  hoverWavelength?: number | null;
  referenceCurves?: {
    healthy?: number[];
    soil?: number[];
    residue?: number[];
  };
}

export const DIAGNOSTIC_PINS = [
  { nm: 680, label: "Chl-a (680nm)", color: "#ef4444" },
  { nm: 705, label: "Red-Edge (705nm)", color: "#10b981" },
  { nm: 970, label: "H2O (970nm)", color: "#06b6d4" },
  { nm: 2100, label: "Cellulose (2100nm)", color: "#f59e0b" },
  { nm: 2200, label: "Clay Al-OH (2200nm)", color: "#a855f7" },
];

export function renderSpectralChart(
  ctx: CanvasRenderingContext2D,
  width: number,
  height: number,
  wavelengths: number[],
  reflectance: number[],
  hullReflectance: number[],
  continuumRemoved: number[],
  maskedWindows: Array<[number, number]>,
  options: ChartRenderOptions = {}
) {
  // Clear canvas
  ctx.clearRect(0, 0, width, height);

  const padding = { top: 24, right: 30, bottom: 42, left: 52 };
  const plotW = width - padding.left - padding.right;
  const plotH = height - padding.top - padding.bottom;

  if (wavelengths.length === 0 || plotW <= 0 || plotH <= 0) return;

  const minWl = wavelengths[0];
  const maxWl = wavelengths[wavelengths.length - 1];

  // Auto-scale max Y based on data
  let maxY = 0.6;
  for (let i = 0; i < reflectance.length; i++) {
    if (reflectance[i] > maxY) maxY = Math.ceil(reflectance[i] * 10) / 10;
  }
  if (options.showContinuumRemoved) {
    maxY = Math.max(maxY, 1.05);
  }

  const toX = (wl: number) => padding.left + ((wl - minWl) / (maxWl - minWl)) * plotW;
  const toY = (r: number) => padding.top + plotH - (r / maxY) * plotH;

  // 1. Grid Background & Axes
  ctx.fillStyle = "#0c1017";
  ctx.fillRect(padding.left, padding.top, plotW, plotH);

  // Horizontal Grid Lines & Y-ticks
  ctx.lineWidth = 1;
  ctx.strokeStyle = "#1b2432";
  ctx.fillStyle = "#64748b";
  ctx.font = "10px monospace";
  ctx.textAlign = "right";
  ctx.textBaseline = "middle";

  const yStep = maxY <= 0.6 ? 0.1 : 0.2;
  for (let yVal = 0; yVal <= maxY; yVal += yStep) {
    const yPx = toY(yVal);
    ctx.beginPath();
    ctx.moveTo(padding.left, yPx);
    ctx.lineTo(padding.left + plotW, yPx);
    ctx.stroke();
    ctx.fillText(yVal.toFixed(1), padding.left - 8, yPx);
  }

  // Vertical Grid Lines & X-ticks (Wavelengths)
  ctx.textAlign = "center";
  ctx.textBaseline = "top";
  for (let wl = 500; wl <= 2400; wl += 300) {
    if (wl >= minWl && wl <= maxWl) {
      const xPx = toX(wl);
      ctx.beginPath();
      ctx.moveTo(xPx, padding.top);
      ctx.lineTo(xPx, padding.top + plotH);
      ctx.stroke();
      ctx.fillText(`${wl} nm`, xPx, padding.top + plotH + 8);
    }
  }

  // 2. Atmospheric Absorption Mask Windows (Shaded Hatching)
  for (const [start, end] of maskedWindows) {
    if (end < minWl || start > maxWl) continue;
    const x1 = Math.max(padding.left, toX(start));
    const x2 = Math.min(padding.left + plotW, toX(end));
    const maskW = x2 - x1;

    ctx.fillStyle = "rgba(239, 68, 68, 0.08)";
    ctx.fillRect(x1, padding.top, maskW, plotH);

    ctx.strokeStyle = "rgba(239, 68, 68, 0.25)";
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);
    ctx.strokeRect(x1, padding.top, maskW, plotH);
    ctx.setLineDash([]);

    // Label
    ctx.fillStyle = "rgba(239, 68, 68, 0.65)";
    ctx.font = "9px monospace";
    ctx.textAlign = "center";
    ctx.fillText("H2O Mask", (x1 + x2) / 2, padding.top + 8);
  }

  // 3. Reference Overlay Curves
  if (options.showReferenceCurves && options.referenceCurves) {
    const refs = [
      { label: "Ref Crop", data: options.referenceCurves.healthy, color: "rgba(34, 197, 94, 0.45)" },
      { label: "Ref Soil", data: options.referenceCurves.soil, color: "rgba(217, 119, 6, 0.45)" },
      { label: "Ref Residue", data: options.referenceCurves.residue, color: "rgba(234, 179, 8, 0.45)" },
    ];

    for (const ref of refs) {
      if (!ref.data || ref.data.length === 0) continue;
      ctx.strokeStyle = ref.color;
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 2]);
      ctx.beginPath();
      for (let i = 0; i < Math.min(wavelengths.length, ref.data.length); i++) {
        const x = toX(wavelengths[i]);
        const y = toY(ref.data[i]);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
    ctx.setLineDash([]);
  }

  // 4. Convex Hull Upper Baseline
  if (options.showConvexHull && hullReflectance.length > 0) {
    ctx.strokeStyle = "#eab308"; // Golden yellow
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    for (let i = 0; i < wavelengths.length; i++) {
      const x = toX(wavelengths[i]);
      const y = toY(hullReflectance[i]);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.setLineDash([]);
  }

  // 5. Continuum Removed Curve (Optional)
  if (options.showContinuumRemoved && continuumRemoved.length > 0) {
    ctx.strokeStyle = "#10b981"; // Emerald
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (let i = 0; i < wavelengths.length; i++) {
      const x = toX(wavelengths[i]);
      const y = toY(continuumRemoved[i]);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }

  // 6. Main Surface Reflectance Curve (Continuous Cyan Glow)
  ctx.save();
  ctx.strokeStyle = "#00d2ff";
  ctx.lineWidth = 2.2;
  ctx.shadowColor = "rgba(0, 210, 255, 0.5)";
  ctx.shadowBlur = 8;

  ctx.beginPath();
  for (let i = 0; i < wavelengths.length; i++) {
    const x = toX(wavelengths[i]);
    const y = toY(reflectance[i]);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();
  ctx.restore();

  // Subtle gradient fill under main curve
  const grad = ctx.createLinearGradient(0, padding.top, 0, padding.top + plotH);
  grad.addColorStop(0, "rgba(0, 210, 255, 0.15)");
  grad.addColorStop(1, "rgba(0, 210, 255, 0.0)");
  ctx.fillStyle = grad;
  ctx.beginPath();
  ctx.moveTo(toX(wavelengths[0]), padding.top + plotH);
  for (let i = 0; i < wavelengths.length; i++) {
    ctx.lineTo(toX(wavelengths[i]), toY(reflectance[i]));
  }
  ctx.lineTo(toX(wavelengths[wavelengths.length - 1]), padding.top + plotH);
  ctx.closePath();
  ctx.fill();

  // 7. Diagnostic Feature Pins
  for (const pin of DIAGNOSTIC_PINS) {
    if (pin.nm < minWl || pin.nm > maxWl) continue;
    const x = toX(pin.nm);
    // Find closest reflectance
    let closestR = reflectance[0];
    let minD = Infinity;
    for (let i = 0; i < wavelengths.length; i++) {
      const d = Math.abs(wavelengths[i] - pin.nm);
      if (d < minD) {
        minD = d;
        closestR = reflectance[i];
      }
    }
    const y = toY(closestR);

    // Vertical dashed marker line
    ctx.strokeStyle = pin.color;
    ctx.lineWidth = 1;
    ctx.setLineDash([2, 3]);
    ctx.beginPath();
    ctx.moveTo(x, padding.top);
    ctx.lineTo(x, padding.top + plotH);
    ctx.stroke();
    ctx.setLineDash([]);

    // Circle point
    ctx.fillStyle = pin.color;
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, 2 * Math.PI);
    ctx.fill();

    // Text Badge
    ctx.font = "9px monospace";
    ctx.fillStyle = pin.color;
    ctx.textAlign = "center";
    ctx.fillText(`${pin.nm}`, x, padding.top - 12);
  }

  // 8. Interactive Hover Scrubber
  if (options.hoverWavelength !== undefined && options.hoverWavelength !== null) {
    const hWl = options.hoverWavelength;
    if (hWl >= minWl && hWl <= maxWl) {
      const hX = toX(hWl);

      // Find closest reflectance value
      let hR = reflectance[0];
      let minDiff = Infinity;
      for (let i = 0; i < wavelengths.length; i++) {
        const d = Math.abs(wavelengths[i] - hWl);
        if (d < minDiff) {
          minDiff = d;
          hR = reflectance[i];
        }
      }
      const hY = toY(hR);

      // Scrubber line
      ctx.strokeStyle = "#ffffff";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(hX, padding.top);
      ctx.lineTo(hX, padding.top + plotH);
      ctx.stroke();

      // Scrubber point
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(hX, hY, 5, 0, 2 * Math.PI);
      ctx.fill();

      // Tooltip box
      const text = `${hWl.toFixed(1)} nm : ${hR.toFixed(3)}`;
      ctx.font = "bold 11px monospace";
      const metrics = ctx.measureText(text);
      const boxW = metrics.width + 16;
      const boxH = 22;
      let boxX = hX + 10;
      if (boxX + boxW > width - padding.right) {
        boxX = hX - boxW - 10;
      }
      const boxY = Math.max(padding.top + 10, Math.min(padding.top + plotH - boxH - 10, hY - 10));

      ctx.fillStyle = "rgba(15, 23, 42, 0.95)";
      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 1;
      ctx.fillRect(boxX, boxY, boxW, boxH);
      ctx.strokeRect(boxX, boxY, boxW, boxH);

      ctx.fillStyle = "#38bdf8";
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      ctx.fillText(text, boxX + 8, boxY + boxH / 2);
    }
  }

  // Plot Border
  ctx.strokeStyle = "#253041";
  ctx.lineWidth = 1;
  ctx.strokeRect(padding.left, padding.top, plotW, plotH);
}
