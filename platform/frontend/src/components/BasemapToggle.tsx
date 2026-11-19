/**
 * BasemapToggle.tsx - 1-Click Tactical Dark <-> High-Res Satellite Switch
 */

import React from "react";
import { Layers, Globe } from "lucide-react";
import { BasemapMode } from "../types/spectroscopy";

interface BasemapToggleProps {
  currentBasemap: BasemapMode;
  onChangeBasemap: (mode: BasemapMode) => void;
}

export const BasemapToggle: React.FC<BasemapToggleProps> = ({ currentBasemap, onChangeBasemap }) => {
  return (
    <div className="absolute top-4 right-4 z-20 flex items-center bg-[#0d1117]/90 backdrop-blur border border-[#253041] rounded-lg p-1 shadow-xl">
      <button
        onClick={() => onChangeBasemap("dark")}
        className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
          currentBasemap === "dark"
            ? "bg-[#18202c] text-[#00d2ff] border border-[#253041] shadow-inner"
            : "text-slate-400 hover:text-slate-200"
        }`}
        title="Tactical Dark Matter Basemap"
      >
        <Layers className="w-3.5 h-3.5" />
        <span>Tactical Dark</span>
      </button>

      <button
        onClick={() => onChangeBasemap("satellite")}
        className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
          currentBasemap === "satellite"
            ? "bg-[#18202c] text-[#00d2ff] border border-[#253041] shadow-inner"
            : "text-slate-400 hover:text-slate-200"
        }`}
        title="High-Resolution ESRI World Imagery"
      >
        <Globe className="w-3.5 h-3.5" />
        <span>ESRI Satellite</span>
      </button>
    </div>
  );
};
