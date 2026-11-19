/**
 * FlightlineDock.tsx - Floating Left Panel: Corridor Selector & Band Modes
 */

import React from "react";
import { MapPin, Satellite, Sliders, ChevronDown } from "lucide-react";
import { BandRenderingMode, FlightlineFeature } from "../types/spectroscopy";

interface FlightlineDockProps {
  flightlines: FlightlineFeature[];
  selectedId: string;
  onSelectFlightline: (id: string) => void;
  bandMode: BandRenderingMode;
  onChangeBandMode: (mode: BandRenderingMode) => void;
  opacity: number;
  onChangeOpacity: (opacity: number) => void;
  onFlyToCorridor: () => void;
  currentCoord: { lat: number; lon: number } | null;
}

export const FlightlineDock: React.FC<FlightlineDockProps> = ({
  flightlines,
  selectedId,
  onSelectFlightline,
  bandMode,
  onChangeBandMode,
  opacity,
  onChangeOpacity,
  onFlyToCorridor,
  currentCoord,
}) => {
  const currentFl = flightlines.find((f) => f.id === selectedId) || flightlines[0];
  const p = currentFl?.properties;

  return (
    <div className="absolute top-4 left-4 z-20 w-80 glass-panel rounded-xl text-slate-200 overflow-hidden text-xs">
      {/* Platform Header */}
      <div className="bg-[#121822] px-4 py-3 border-b border-[#253041] flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Satellite className="w-4 h-4 text-[#00d2ff]" />
          <div>
            <h1 className="font-bold text-sm tracking-wide text-white">BHARATSPECTRAL</h1>
            <p className="text-[10px] text-slate-400 font-mono">DSSI WebGIS • Cloudflare Edge</p>
          </div>
        </div>
        <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-mono bg-emerald-950 text-emerald-400 border border-emerald-800">
          LIVE
        </span>
      </div>

      <div className="p-4 space-y-4">
        {/* Corridor Selector */}
        <div>
          <label className="block text-[11px] font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Flightline Corridor
          </label>
          <div className="relative">
            <select
              value={selectedId}
              onChange={(e) => onSelectFlightline(e.target.value)}
              className="w-full bg-[#18202c] border border-[#253041] rounded-lg px-3 py-2 pr-8 text-xs text-white appearance-none cursor-pointer focus:outline-none focus:border-[#00d2ff]"
            >
              {flightlines.map((fl) => (
                <option key={fl.id} value={fl.id}>
                  {fl.properties.name}
                </option>
              ))}
            </select>
            <ChevronDown className="w-4 h-4 text-slate-400 absolute right-2.5 top-2.5 pointer-events-none" />
          </div>
        </div>

        {/* Corridor Metadata Chips */}
        {p && (
          <div className="bg-[#0f141d] rounded-lg p-3 border border-[#1f2937] space-y-2">
            <div className="flex justify-between items-center text-[11px]">
              <span className="text-slate-400">Sensor Platform:</span>
              <span className="font-mono text-[#00d2ff] font-medium">{p.sensor}</span>
            </div>
            <div className="flex justify-between items-center text-[11px]">
              <span className="text-slate-400">Resolution / Bands:</span>
              <span className="font-mono text-slate-200">
                {p.gsd_m}m GSD • {p.total_bands} Bands
              </span>
            </div>
            <div className="text-[10px] text-slate-400 border-t border-[#1f2937] pt-2 italic leading-relaxed">
              {p.agro_zone}
            </div>
          </div>
        )}

        {/* Band Rendering Mode */}
        <div>
          <label className="block text-[11px] font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Band Rendering Mode
          </label>
          <div className="grid grid-cols-2 gap-1.5">
            <button
              onClick={() => onChangeBandMode("rgb")}
              className={`px-2.5 py-1.5 rounded text-left border transition-all ${
                bandMode === "rgb"
                  ? "bg-[#18202c] text-[#00d2ff] border-[#00d2ff]"
                  : "bg-[#0f141d] text-slate-400 border-[#253041] hover:text-slate-200"
              }`}
            >
              <div className="font-medium">True Color</div>
              <div className="text-[9px] text-slate-500 font-mono">RGB (640/550/460)</div>
            </button>

            <button
              onClick={() => onChangeBandMode("cir")}
              className={`px-2.5 py-1.5 rounded text-left border transition-all ${
                bandMode === "cir"
                  ? "bg-[#18202c] text-[#00d2ff] border-[#00d2ff]"
                  : "bg-[#0f141d] text-slate-400 border-[#253041] hover:text-slate-200"
              }`}
            >
              <div className="font-medium">False Color (CIR)</div>
              <div className="text-[9px] text-slate-500 font-mono">NIR/Red/Green</div>
            </button>

            <button
              onClick={() => onChangeBandMode("ndre")}
              className={`px-2.5 py-1.5 rounded text-left border transition-all ${
                bandMode === "ndre"
                  ? "bg-[#18202c] text-[#00d2ff] border-[#00d2ff]"
                  : "bg-[#0f141d] text-slate-400 border-[#253041] hover:text-slate-200"
              }`}
            >
              <div className="font-medium">NDRE Nitrogen</div>
              <div className="text-[9px] text-slate-500 font-mono">Red-Edge Canopy</div>
            </button>

            <button
              onClick={() => onChangeBandMode("ndti")}
              className={`px-2.5 py-1.5 rounded text-left border transition-all ${
                bandMode === "ndti"
                  ? "bg-[#18202c] text-[#00d2ff] border-[#00d2ff]"
                  : "bg-[#0f141d] text-slate-400 border-[#253041] hover:text-slate-200"
              }`}
            >
              <div className="font-medium">Residue / NDTI</div>
              <div className="text-[9px] text-slate-500 font-mono">Lignin/Cellulose</div>
            </button>
          </div>
        </div>

        {/* Opacity Slider */}
        <div>
          <div className="flex justify-between text-[11px] text-slate-400 mb-1">
            <span className="flex items-center space-x-1">
              <Sliders className="w-3 h-3" />
              <span>Layer Opacity</span>
            </span>
            <span className="font-mono text-slate-200">{Math.round(opacity * 100)}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={opacity}
            onChange={(e) => onChangeOpacity(parseFloat(e.target.value))}
            className="w-full h-1.5 bg-[#1f2937] rounded-lg appearance-none cursor-pointer accent-[#00d2ff]"
          />
        </div>

        {/* Actions & Coordinates HUD */}
        <div className="pt-2 border-t border-[#253041] flex items-center justify-between">
          <button
            onClick={onFlyToCorridor}
            className="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-[#18202c] hover:bg-[#222d3d] text-slate-300 hover:text-white border border-[#253041] transition-all"
          >
            <MapPin className="w-3.5 h-3.5 text-[#00d2ff]" />
            <span>Center Corridor</span>
          </button>

          {currentCoord && (
            <div className="text-right font-mono text-[10px] text-slate-400">
              <div>{currentCoord.lat.toFixed(4)}°N</div>
              <div>{currentCoord.lon.toFixed(4)}°E</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
