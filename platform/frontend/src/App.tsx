/**
 * App.tsx - Master Remote Sensing Workstation Layout
 */

import React, { useState, useEffect } from "react";
import { ChevronDown, ChevronUp, Loader2 } from "lucide-react";
import {
  BandRenderingMode,
  BasemapMode,
  DiagnosticPayload,
  FlightlinesManifest,
} from "./types/spectroscopy";
import { fetchFlightlines, fetchSpectrum } from "./lib/api";
import { MapCanvas } from "./components/MapCanvas";
import { BasemapToggle } from "./components/BasemapToggle";
import { FlightlineDock } from "./components/FlightlineDock";
import { SpectralCurveDock } from "./components/SpectralCurveDock";
import { TelemetryHUD } from "./components/TelemetryHUD";
import { CopilotDrawer } from "./components/CopilotDrawer";

export const App: React.FC = () => {
  const [manifest, setManifest] = useState<FlightlinesManifest | null>(null);
  const [selectedFlightlineId, setSelectedFlightlineId] = useState<string>("vidarbha_wardha_cotton");
  const [selectedCoord, setSelectedCoord] = useState<{ lat: number; lon: number } | null>(null);
  const [payload, setPayload] = useState<DiagnosticPayload | null>(null);
  const [isLoadingSpectrum, setIsLoadingSpectrum] = useState(false);

  // Map display settings
  const [basemapMode, setBasemapMode] = useState<BasemapMode>("dark");
  const [bandMode, setBandMode] = useState<BandRenderingMode>("rgb");
  const [opacity, setOpacity] = useState<number>(0.85);

  // UI Docks & Drawer
  const [isCopilotOpen, setIsCopilotOpen] = useState(false);
  const [isBottomDockExpanded, setIsBottomDockExpanded] = useState(true);
  const [centerTrigger, setCenterTrigger] = useState(0);

  // Load Flightlines Manifest on Mount
  useEffect(() => {
    fetchFlightlines()
      .then((m) => {
        setManifest(m);
        if (m.features.length > 0) {
          const first = m.features[0];
          setSelectedFlightlineId(first.id);
          const center = first.properties.center;
          const initialCoord = { lat: center[1], lon: center[0] };
          setSelectedCoord(initialCoord);
          loadSpectrum(first.id, initialCoord.lat, initialCoord.lon);
        }
      })
      .catch((err) => console.error("Manifest load error:", err));
  }, []);

  const loadSpectrum = async (flId: string, lat?: number, lon?: number) => {
    setIsLoadingSpectrum(true);
    try {
      const data = await fetchSpectrum(flId, lat, lon);
      setPayload(data);
      setSelectedCoord({ lat: data.coordinates.latitude, lon: data.coordinates.longitude });
    } catch (err) {
      console.error("Spectrum fetch error:", err);
    } finally {
      setIsLoadingSpectrum(false);
    }
  };

  const handleSelectFlightline = (id: string) => {
    setSelectedFlightlineId(id);
    const fl = manifest?.features.find((f) => f.id === id);
    if (fl) {
      const center = fl.properties.center;
      const coord = { lat: center[1], lon: center[0] };
      setSelectedCoord(coord);
      loadSpectrum(id, coord.lat, coord.lon);
    }
  };

  const handleSelectPixel = (lat: number, lon: number, flightlineId: string) => {
    if (flightlineId !== selectedFlightlineId) {
      setSelectedFlightlineId(flightlineId);
    }
    loadSpectrum(flightlineId, lat, lon);
  };

  const handleFlyToCorridor = () => {
    setCenterTrigger((c) => c + 1);
    const fl = manifest?.features.find((f) => f.id === selectedFlightlineId);
    if (fl && fl.properties.center) {
      const center = fl.properties.center;
      loadSpectrum(selectedFlightlineId, center[1], center[0]);
    }
  };

  // Keyboard Shortcuts (1-4 for band modes, ESC for drawer)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setIsCopilotOpen(false);
      } else if (e.key === "1") {
        setBandMode("rgb");
      } else if (e.key === "2") {
        setBandMode("cir");
      } else if (e.key === "3") {
        setBandMode("ndre");
      } else if (e.key === "4") {
        setBandMode("ndti");
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-[#080b0f] font-sans">
      {/* 100% Viewport Map Canvas */}
      <MapCanvas
        manifest={manifest}
        selectedFlightlineId={selectedFlightlineId}
        onSelectFlightline={handleSelectFlightline}
        selectedCoord={selectedCoord}
        onSelectPixel={handleSelectPixel}
        basemapMode={basemapMode}
        bandMode={bandMode}
        opacity={opacity}
        centerTrigger={centerTrigger}
      />

      {/* Top Right Basemap Toggle */}
      <BasemapToggle currentBasemap={basemapMode} onChangeBasemap={setBasemapMode} />

      {/* Top Left Floating Flightline Dock */}
      <FlightlineDock
        flightlines={manifest?.features || []}
        selectedId={selectedFlightlineId}
        onSelectFlightline={handleSelectFlightline}
        bandMode={bandMode}
        onChangeBandMode={setBandMode}
        opacity={opacity}
        onChangeOpacity={setOpacity}
        onFlyToCorridor={handleFlyToCorridor}
        currentCoord={selectedCoord}
      />

      {/* Floating Bottom-Right Spectroscopy Dock */}
      <div className="absolute bottom-4 right-4 z-20 w-[640px] max-w-[calc(100vw-32px)] flex flex-col space-y-2 pointer-events-auto">
        {/* Toggle Collapse Bar */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            {isLoadingSpectrum && (
              <span className="flex items-center space-x-1.5 px-2.5 py-1 rounded bg-[#0d1117]/90 text-[#00d2ff] border border-[#253041] text-[10px] font-mono">
                <Loader2 className="w-3 h-3 animate-spin" />
                <span>Extracting Pixel Spectrum...</span>
              </span>
            )}
          </div>

          <button
            onClick={() => setIsBottomDockExpanded((prev) => !prev)}
            className="flex items-center space-x-1.5 px-3 py-1 rounded-md bg-[#0d1117]/90 text-slate-400 hover:text-white border border-[#253041] text-[11px] font-mono backdrop-blur transition-all"
          >
            {isBottomDockExpanded ? (
              <>
                <span>Collapse Spectroscopy HUD</span>
                <ChevronDown className="w-3.5 h-3.5" />
              </>
            ) : (
              <>
                <span>Expand Spectroscopy HUD</span>
                <ChevronUp className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </div>

        {isBottomDockExpanded && (
          <div className="space-y-3 animate-in fade-in duration-200">
            {/* 425-Band Spectral Curve Visualizer */}
            <SpectralCurveDock
              curveData={payload ? payload.spectral_curve : null}
              sensorName={payload?.sensor.name}
              totalBands={payload?.sensor.total_bands}
            />

            {/* Numerical Telemetry HUD */}
            <TelemetryHUD payload={payload} onOpenCopilot={() => setIsCopilotOpen(true)} />
          </div>
        )}
      </div>

      {/* On-Demand Remote Sensing Specialist Drawer */}
      <CopilotDrawer
        isOpen={isCopilotOpen}
        onClose={() => setIsCopilotOpen(false)}
        telemetry={payload}
      />
    </div>
  );
};
export default App;
