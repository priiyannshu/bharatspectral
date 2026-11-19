/**
 * TelemetryHUD.tsx - Numerical Physical Spectroscopy Telemetry Display
 */

import React from "react";
import { Sparkles, Target } from "lucide-react";
import { DiagnosticPayload } from "../types/spectroscopy";

interface TelemetryHUDProps {
  payload: DiagnosticPayload | null;
  onOpenCopilot: () => void;
}

export const TelemetryHUD: React.FC<TelemetryHUDProps> = ({ payload, onOpenCopilot }) => {
  if (!payload) return null;

  const idx = payload.narrowband_indices;
  const cont = payload.continuum_diagnostics;
  const sub = payload.subpixel_abundances;
  const sam = payload.sam_classification;

  // Percentage calculations
  const pGreen = Math.round(sub.healthy_crop_fraction * 100);
  const pStressed = Math.round(sub.stressed_crop_fraction * 100);
  const pSoil = Math.round(sub.exposed_soil_fraction * 100);
  const pResidue = Math.round(sub.dry_residue_fraction * 100);
  const pWater = Math.round(sub.standing_water_fraction * 100);

  return (
    <div className="w-full glass-panel rounded-xl p-4 space-y-4 text-xs">
      {/* Header & Copilot Trigger */}
      <div className="flex items-center justify-between border-b border-[#253041] pb-2.5">
        <div className="flex items-center space-x-2">
          <Target className="w-4 h-4 text-[#00d2ff]" />
          <div>
            <h3 className="font-bold text-white tracking-wide">PHYSICAL SPECTROSCOPIC TELEMETRY</h3>
            <p className="text-[10px] text-slate-400 font-mono">
              Lat {payload.coordinates.latitude.toFixed(4)}°N • Lon {payload.coordinates.longitude.toFixed(4)}°E
            </p>
          </div>
        </div>

        <button
          onClick={onOpenCopilot}
          className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-medium shadow-lg shadow-cyan-900/30 transition-all cursor-pointer"
        >
          <Sparkles className="w-3.5 h-3.5 text-yellow-300" />
          <span>Run Specialist Diagnostic</span>
        </button>
      </div>

      {/* Row 1: Narrowband Indices Grid */}
      <div>
        <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-2 font-mono">
          Narrowband Hyperspectral Indices
        </div>
        <div className="grid grid-cols-5 gap-2">
          <div className="bg-[#0f141d] rounded-lg p-2.5 border border-[#1f2937] text-center">
            <div className="text-[10px] text-slate-400 font-mono">NDRE</div>
            <div className={`font-mono text-base font-bold ${idx.ndre >= 0.28 ? "text-emerald-400" : "text-amber-400"}`}>
              {idx.ndre.toFixed(3)}
            </div>
            <div className="text-[9px] text-slate-500">Nitrogen</div>
          </div>

          <div className="bg-[#0f141d] rounded-lg p-2.5 border border-[#1f2937] text-center">
            <div className="text-[10px] text-slate-400 font-mono">PRI</div>
            <div className={`font-mono text-base font-bold ${idx.pri >= -0.05 ? "text-emerald-400" : "text-rose-400"}`}>
              {idx.pri.toFixed(3)}
            </div>
            <div className="text-[9px] text-slate-500">Light Stress</div>
          </div>

          <div className="bg-[#0f141d] rounded-lg p-2.5 border border-[#1f2937] text-center">
            <div className="text-[10px] text-slate-400 font-mono">WBI</div>
            <div className="font-mono text-base font-bold text-cyan-400">{idx.wbi.toFixed(3)}</div>
            <div className="text-[9px] text-slate-500">Water Band</div>
          </div>

          <div className="bg-[#0f141d] rounded-lg p-2.5 border border-[#1f2937] text-center">
            <div className="text-[10px] text-slate-400 font-mono">NDTI</div>
            <div className={`font-mono text-base font-bold ${idx.ndti >= 0.15 ? "text-yellow-400" : "text-slate-300"}`}>
              {idx.ndti.toFixed(3)}
            </div>
            <div className="text-[9px] text-slate-500">Residue/Straw</div>
          </div>

          <div className="bg-[#0f141d] rounded-lg p-2.5 border border-[#1f2937] text-center">
            <div className="text-[10px] text-slate-400 font-mono">MTCI</div>
            <div className="font-mono text-base font-bold text-slate-200">{idx.mtci.toFixed(2)}</div>
            <div className="text-[9px] text-slate-500">Red-Edge Chl</div>
          </div>
        </div>
      </div>

      {/* Row 2: Continuum Diagnostics & FCLS Subpixel Distribution */}
      <div className="grid grid-cols-2 gap-4">
        {/* Continuum Depths */}
        <div className="bg-[#0f141d] rounded-lg p-3 border border-[#1f2937] space-y-2">
          <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider font-mono">
            Continuum Absorption Depths
          </div>
          <div className="space-y-1.5 font-mono text-[11px]">
            <div className="flex justify-between">
              <span className="text-slate-400">Chlorophyll Well (680nm):</span>
              <span className="text-rose-400 font-bold">{cont.chlorophyll_depth_680nm.toFixed(3)} (AUC: {cont.chlorophyll_auc})</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Red-Edge Inflection:</span>
              <span className="text-emerald-400 font-bold">
                {cont.red_edge_inflection_nm} nm ({cont.red_edge_shift_nm > 0 ? "+" : ""}{cont.red_edge_shift_nm} nm)
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Plant Water Depth (970nm):</span>
              <span className="text-cyan-400 font-bold">{cont.water_depth_970nm.toFixed(3)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Cellulose / Lignin (2100nm):</span>
              <span className="text-yellow-400 font-bold">{cont.cellulose_depth_2100nm.toFixed(3)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Clay Hydroxyl (2200nm):</span>
              <span className="text-purple-400 font-bold">{cont.clay_hydroxyl_depth_2200nm.toFixed(3)}</span>
            </div>
          </div>
        </div>

        {/* FCLS Subpixel Unmixing & SAM */}
        <div className="bg-[#0f141d] rounded-lg p-3 border border-[#1f2937] space-y-2.5">
          <div className="flex justify-between items-center text-[10px] font-semibold text-slate-400 uppercase tracking-wider font-mono">
            <span>FCLS Subpixel Fractions (Sum = 100%)</span>
            <span className="text-slate-500 font-normal">RMSE: {sub.reconstruction_rmse.toFixed(4)}</span>
          </div>

          {/* Stacked Fraction Bar */}
          <div className="w-full h-3.5 bg-[#18202c] rounded overflow-hidden flex shadow-inner">
            {pGreen > 0 && <div style={{ width: `${pGreen}%` }} className="bg-emerald-500" title={`Green: ${pGreen}%`} />}
            {pStressed > 0 && <div style={{ width: `${pStressed}%` }} className="bg-amber-500" title={`Stressed: ${pStressed}%`} />}
            {pSoil > 0 && <div style={{ width: `${pSoil}%` }} className="bg-[#b45309]" title={`Soil: ${pSoil}%`} />}
            {pResidue > 0 && <div style={{ width: `${pResidue}%` }} className="bg-yellow-400" title={`Residue: ${pResidue}%`} />}
            {pWater > 0 && <div style={{ width: `${pWater}%` }} className="bg-cyan-500" title={`Water: ${pWater}%`} />}
          </div>

          {/* Legend chips */}
          <div className="flex flex-wrap gap-2 text-[10px] font-mono">
            <span className="flex items-center space-x-1 text-emerald-400">
              <span className="w-2 h-2 rounded bg-emerald-500 inline-block" />
              <span>Green: {pGreen}%</span>
            </span>
            <span className="flex items-center space-x-1 text-amber-400">
              <span className="w-2 h-2 rounded bg-amber-500 inline-block" />
              <span>Stressed: {pStressed}%</span>
            </span>
            <span className="flex items-center space-x-1 text-orange-400">
              <span className="w-2 h-2 rounded bg-[#b45309] inline-block" />
              <span>Soil: {pSoil}%</span>
            </span>
            {pResidue > 0 && (
              <span className="flex items-center space-x-1 text-yellow-300">
                <span className="w-2 h-2 rounded bg-yellow-400 inline-block" />
                <span>Residue: {pResidue}%</span>
              </span>
            )}
            {pWater > 0 && (
              <span className="flex items-center space-x-1 text-cyan-400">
                <span className="w-2 h-2 rounded bg-cyan-500 inline-block" />
                <span>Water: {pWater}%</span>
              </span>
            )}
          </div>

          {/* SAM Classification Match */}
          <div className="pt-2 border-t border-[#1f2937] flex justify-between items-center text-[11px]">
            <span className="text-slate-400">Spectral Angle Match:</span>
            <span className="font-mono text-[#00d2ff] font-medium">
              {sam.top_match} ({sam.confidence_pct}% • {sam.spectral_angle_rad} rad)
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
