/**
 * MapCanvas.tsx - 100% Viewport MapLibre GL Geospatial Engine
 * Displays national/state boundaries, calibrated flightlines corridors,
 * dynamic band rendering modes, and precision coordinate inspection.
 */

import React, { useEffect, useRef } from "react";
import maplibregl, { Map as MapLibreMap, Marker } from "maplibre-gl";
import { BandRenderingMode, BasemapMode, FlightlinesManifest } from "../types/spectroscopy";

interface MapCanvasProps {
  manifest: FlightlinesManifest | null;
  selectedFlightlineId: string;
  onSelectFlightline: (id: string) => void;
  selectedCoord: { lat: number; lon: number } | null;
  onSelectPixel: (lat: number, lon: number, flightlineId: string) => void;
  basemapMode: BasemapMode;
  bandMode: BandRenderingMode;
  opacity: number;
  centerTrigger?: number;
}

const CARTO_API_KEY = "cb1_4s1w_1_71402736b23141ec84d29e44";

const DARK_STYLE: any = {
  version: 8,
  sources: {
    "carto-dark": {
      type: "raster",
      tiles: [
        `https://a.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}@2x.png?key=${CARTO_API_KEY}`,
        `https://b.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}@2x.png?key=${CARTO_API_KEY}`,
        `https://c.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}@2x.png?key=${CARTO_API_KEY}`,
      ],
      tileSize: 256,
      attribution: "© CARTO, © OpenStreetMap",
    },
  },
  layers: [
    {
      id: "base-raster-layer",
      type: "raster",
      source: "carto-dark",
      minzoom: 0,
      maxzoom: 19,
    },
  ],
};

const SATELLITE_TILES = [
  "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
];

const CARTO_DARK_TILES = [
  `https://a.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}@2x.png?key=${CARTO_API_KEY}`,
  `https://b.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}@2x.png?key=${CARTO_API_KEY}`,
  `https://c.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}@2x.png?key=${CARTO_API_KEY}`,
];

export const MapCanvas: React.FC<MapCanvasProps> = ({
  manifest,
  selectedFlightlineId,
  onSelectFlightline,
  selectedCoord,
  onSelectPixel,
  basemapMode,
  bandMode,
  opacity,
  centerTrigger = 0,
}) => {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<MapLibreMap | null>(null);
  const markerRef = useRef<Marker | null>(null);

  // Fresh refs to prevent stale closure bugs inside event listeners
  const manifestRef = useRef(manifest);
  manifestRef.current = manifest;

  const selectedFlightlineIdRef = useRef(selectedFlightlineId);
  selectedFlightlineIdRef.current = selectedFlightlineId;

  const onSelectPixelRef = useRef(onSelectPixel);
  onSelectPixelRef.current = onSelectPixel;

  const onSelectFlightlineRef = useRef(onSelectFlightline);
  onSelectFlightlineRef.current = onSelectFlightline;

  const bandModeRef = useRef(bandMode);
  bandModeRef.current = bandMode;

  const opacityRef = useRef(opacity);
  opacityRef.current = opacity;

  const ensureBoundaryLayers = (map: MapLibreMap) => {
    // 1. India National Boundary
    if (!map.getSource("india-boundary")) {
      map.addSource("india-boundary", {
        type: "geojson",
        data: "/geo/india.geojson",
      });
      map.addLayer({
        id: "india-boundary-line",
        type: "line",
        source: "india-boundary",
        paint: {
          "line-color": "#38bdf8",
          "line-width": 1.6,
          "line-opacity": 0.5,
        },
      });
    }

    // 2. State Administrative Boundaries
    if (!map.getSource("states-boundary")) {
      map.addSource("states-boundary", {
        type: "geojson",
        data: "/geo/states.geojson",
      });
      map.addLayer({
        id: "states-boundary-line",
        type: "line",
        source: "states-boundary",
        paint: {
          "line-color": "#64748b",
          "line-width": 0.8,
          "line-dasharray": [3, 2],
          "line-opacity": 0.35,
        },
      });
    }
  };

  const ensureCorridorLayers = (map: MapLibreMap, data: FlightlinesManifest) => {
    if (!map.getSource("flightlines-source")) {
      map.addSource("flightlines-source", {
        type: "geojson",
        data: data as any,
      });

      // Fill Layer
      map.addLayer({
        id: "flightlines-fill",
        type: "fill",
        source: "flightlines-source",
        paint: {
          "fill-color": getFillColor(bandModeRef.current),
          "fill-opacity": opacityRef.current * 0.45,
        },
      });

      // Outline Layer
      map.addLayer({
        id: "flightlines-line",
        type: "line",
        source: "flightlines-source",
        paint: {
          "line-color": "#00d2ff",
          "line-width": 2,
          "line-dasharray": [2, 1],
        },
      });

      // Labels
      map.addLayer({
        id: "flightlines-label",
        type: "symbol",
        source: "flightlines-source",
        layout: {
          "text-field": ["get", "name"],
          "text-size": 11,
          "text-font": ["Open Sans Regular", "Arial Unicode MS Regular"],
          "text-anchor": "top",
          "text-offset": [0, 0.6],
        },
        paint: {
          "text-color": "#ffffff",
          "text-halo-color": "#000000",
          "text-halo-width": 1.5,
        },
      });

      // Pointer cursor on hover over parcels
      map.on("mouseenter", "flightlines-fill", () => {
        map.getCanvas().style.cursor = "pointer";
      });
      map.on("mouseleave", "flightlines-fill", () => {
        map.getCanvas().style.cursor = "";
      });
    } else {
      const src = map.getSource("flightlines-source") as maplibregl.GeoJSONSource;
      src.setData(data as any);
    }
  };

  // Initialize MapLibre GL
  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const map = new maplibregl.Map({
      container: containerRef.current,
      style: DARK_STYLE,
      center: [78.60, 20.75], // Vidarbha default center
      zoom: 12.2,
      maxZoom: 18,
      minZoom: 4,
      attributionControl: false,
    });

    map.addControl(new maplibregl.NavigationControl({ showCompass: true }), "top-right");
    map.addControl(new maplibregl.ScaleControl({ unit: "metric" }), "bottom-left");

    map.on("load", () => {
      ensureBoundaryLayers(map);
      if (manifestRef.current) {
        ensureCorridorLayers(map, manifestRef.current);
      }
    });

    // Handle Clicks on Corridor or Map
    map.on("click", (e) => {
      const lat = e.lngLat.lat;
      const lon = e.lngLat.lng;
      const curManifest = manifestRef.current;

      // Check if user clicked inside a flightline polygon
      if (curManifest) {
        for (const fl of curManifest.features) {
          const [minLon, minLat, maxLon, maxLat] = fl.properties.bbox;
          if (lon >= minLon && lon <= maxLon && lat >= minLat && lat <= maxLat) {
            onSelectFlightlineRef.current(fl.id);
            onSelectPixelRef.current(lat, lon, fl.id);
            return;
          }
        }
      }

      // Default to clicking currently active corridor
      onSelectPixelRef.current(lat, lon, selectedFlightlineIdRef.current);
    });

    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  // Update corridor data whenever manifest arrives or updates
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !manifest) return;

    if (map.isStyleLoaded()) {
      ensureCorridorLayers(map, manifest);
    } else {
      map.once("load", () => ensureCorridorLayers(map, manifest));
    }
  }, [manifest]);

  // Smooth camera flyTo when selectedFlightlineId changes or Center Corridor clicked
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !manifest) return;

    const fl = manifest.features.find((f) => f.id === selectedFlightlineId);
    if (fl && fl.properties.center) {
      map.flyTo({
        center: [fl.properties.center[0], fl.properties.center[1]],
        zoom: 12.2,
        speed: 1.3,
        curve: 1.4,
        essential: true,
      });
    }
  }, [selectedFlightlineId, centerTrigger]);

  // Update Basemap Tiles (Carto Dark <-> ESRI Satellite)
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !map.isStyleLoaded()) return;

    const source = map.getSource("carto-dark") as maplibregl.RasterTileSource;
    if (source) {
      const newTiles = basemapMode === "satellite" ? SATELLITE_TILES : CARTO_DARK_TILES;
      if ((source as any).setTiles) {
        (source as any).setTiles(newTiles);
      }
    }
  }, [basemapMode]);

  // Update Fill Color & Opacity based on Band Mode
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !map.isStyleLoaded()) return;

    if (map.getLayer("flightlines-fill")) {
      map.setPaintProperty("flightlines-fill", "fill-color", getFillColor(bandMode));
      map.setPaintProperty("flightlines-fill", "fill-opacity", opacity * 0.45);
    }
  }, [bandMode, opacity]);

  // Update Reticle Marker for Selected Pixel
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    if (!selectedCoord) {
      if (markerRef.current) markerRef.current.remove();
      return;
    }

    if (!markerRef.current) {
      const el = document.createElement("div");
      el.className = "reticle-marker";
      el.innerHTML = `
        <div class="relative flex items-center justify-center w-7 h-7">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-60"></span>
          <span class="relative inline-flex rounded-full h-3.5 w-3.5 bg-[#00d2ff] border-2 border-white shadow-lg"></span>
          <div class="absolute w-6 h-0.5 bg-[#00d2ff] opacity-80 pointer-events-none"></div>
          <div class="absolute h-6 w-0.5 bg-[#00d2ff] opacity-80 pointer-events-none"></div>
        </div>
      `;
      markerRef.current = new maplibregl.Marker({ element: el })
        .setLngLat([selectedCoord.lon, selectedCoord.lat])
        .addTo(map);
    } else {
      markerRef.current.setLngLat([selectedCoord.lon, selectedCoord.lat]);
    }
  }, [selectedCoord]);

  return <div ref={containerRef} className="absolute inset-0 w-full h-full bg-[#080b0f]" />;
};

function getFillColor(mode: BandRenderingMode): string {
  switch (mode) {
    case "rgb":
      return "#38bdf8"; // Natural blue/cyan
    case "cir":
      return "#f43f5e"; // Infrared red/crimson
    case "ndre":
      return "#10b981"; // Emerald nitrogen
    case "ndti":
      return "#f59e0b"; // Residue amber
    default:
      return "#00d2ff";
  }
}
