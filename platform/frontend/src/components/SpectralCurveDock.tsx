/**
 * SpectralCurveDock.tsx - Floating Spectral Visualizer & Hull Inspector
 */

import React, { useRef, useEffect, useState } from "react";
import { Activity } from "lucide-react";
import { SpectralCurvePayload } from "../types/spectroscopy";
import { renderSpectralChart, DIAGNOSTIC_PINS } from "../lib/chart_utils";

interface SpectralCurveDockProps {
  curveData: SpectralCurvePayload | null;
  sensorName?: string;
  totalBands?: number;
}

export const SpectralCurveDock: React.FC<SpectralCurveDockProps> = ({
  curveData,
  sensorName,
  totalBands,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [showConvexHull, setShowConvexHull] = useState(true);
  const [showContinuumRemoved, setShowContinuumRemoved] = useState(false);
  const [showReferenceCurves, setShowReferenceCurves] = useState(false);
  const [hoverWavelength, setHoverWavelength] = useState<number | null>(null);

  useEffect(() => {
    if (!canvasRef.current || !curveData) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Handle high DPI displays
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    renderSpectralChart(
      ctx,
      rect.width,
      rect.height,
      curveData.wavelengths,
      curveData.reflectance,
      curveData.hull_reflectance,
      curveData.continuum_removed,
      curveData.masked_windows || [],
      {
        showConvexHull,
        showContinuumRemoved,
        showReferenceCurves,
        hoverWavelength,
        referenceCurves: curveData.reference_curves,
      }
    );
  }, [curveData, showConvexHull, showContinuumRemoved, showReferenceCurves, hoverWavelength]);

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!canvasRef.current || !curveData) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const paddingLeft = 52;
    const paddingRight = 30;
    const plotW = rect.width - paddingLeft - paddingRight;

    if (x >= paddingLeft && x <= paddingLeft + plotW) {
      const minWl = curveData.wavelengths[0];
      const maxWl = curveData.wavelengths[curveData.wavelengths.length - 1];
      const wl = minWl + ((x - paddingLeft) / plotW) * (maxWl - minWl);
      setHoverWavelength(wl);
    } else {
      setHoverWavelength(null);
    }
  };

  const handleMouseLeave = () => {
    setHoverWavelength(null);
  };

  if (!curveData) {
    return (
      <div className="w-full glass-panel rounded-xl p-4 text-center text-slate-400 text-xs">
        <Activity className="w-5 h-5 mx-auto mb-2 text-[#00d2ff] animate-pulse" />
        Click any parcel in a flightline corridor to load continuous 425-band spectrum.
      </div>
    );
  }

  return (
    <div className="w-full glass-panel rounded-xl p-4 space-y-3">
      {/* Header & Controls */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#253041] pb-2 text-xs">
        <div className="flex items-center space-x-2">
          <Activity className="w-4 h-4 text-[#00d2ff]" />
          <div>
            <h2 className="font-bold text-white tracking-wide">
              CONTINUOUS REFLECTANCE SPECTRUM (380–2510 nm)
            </h2>
            <p className="text-[10px] text-slate-400 font-mono">
              {sensorName || "AVIRIS-NG India"} • {totalBands || curveData.wavelengths.length} Calibrated Bands
            </p>
          </div>
        </div>

        {/* Diagnostic Toggles */}
        <div className="flex items-center space-x-3 text-[11px] text-slate-300">
          <label className="flex items-center space-x-1 cursor-pointer hover:text-white">
            <input
              type="checkbox"
              checked={showConvexHull}
              onChange={(e) => setShowConvexHull(e.target.checked)}
              className="rounded bg-[#1f2937] border-[#374151] text-[#00d2ff] focus:ring-0 cursor-pointer"
            />
            <span className="text-[#eab308]">Convex Hull (Rc)</span>
          </label>

          <label className="flex items-center space-x-1 cursor-pointer hover:text-white">
            <input
              type="checkbox"
              checked={showContinuumRemoved}
              onChange={(e) => setShowContinuumRemoved(e.target.checked)}
              className="rounded bg-[#1f2937] border-[#374151] text-[#10b981] focus:ring-0 cursor-pointer"
            />
            <span className="text-[#10b981]">Continuum-Removed (R')</span>
          </label>

          <label className="flex items-center space-x-1 cursor-pointer hover:text-white">
            <input
              type="checkbox"
              checked={showReferenceCurves}
              onChange={(e) => setShowReferenceCurves(e.target.checked)}
              className="rounded bg-[#1f2937] border-[#374151] text-emerald-400 focus:ring-0 cursor-pointer"
            />
            <span>Ref Overlays</span>
          </label>
        </div>
      </div>

      {/* 425-Band Interactive Canvas */}
      <div className="relative w-full h-48 bg-[#0a0d13] rounded-lg border border-[#1b2432] overflow-hidden">
        <canvas
          ref={canvasRef}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
          className="w-full h-full cursor-crosshair block"
        />
      </div>

      {/* Diagnostic Feature Pins Legend */}
      <div className="flex flex-wrap items-center justify-between text-[10px] font-mono text-slate-400 pt-1">
        <div className="flex items-center space-x-3">
          {DIAGNOSTIC_PINS.map((pin) => (
            <span key={pin.nm} className="flex items-center space-x-1">
              <span className="w-2 h-2 rounded-full inline-block" style={{ backgroundColor: pin.color }} />
              <span>{pin.label}</span>
            </span>
          ))}
        </div>
        <div className="text-slate-500 italic">Hover crosshair over curve to inspect discrete band reflectance</div>
      </div>
    </div>
  );
};
