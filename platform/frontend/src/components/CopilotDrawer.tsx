/**
 * CopilotDrawer.tsx - On-Demand Remote Sensing Specialist Drawer
 * Streams authoritative physical diagnostics via Cloudflare Workers AI SSE.
 */

import React, { useState, useEffect, useRef } from "react";
import { X, Sparkles, User, Microscope, Landmark, RefreshCw, Send } from "lucide-react";
import { DiagnosticPayload, SpecialistRole } from "../types/spectroscopy";
import { streamCopilotAdvisory } from "../lib/api";

interface CopilotDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  telemetry: DiagnosticPayload | null;
}

export const CopilotDrawer: React.FC<CopilotDrawerProps> = ({ isOpen, onClose, telemetry }) => {
  const [role, setRole] = useState<SpecialistRole>("farmer");
  const [customQuery, setCustomQuery] = useState("");
  const [streamedText, setStreamedText] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const streamCancelRef = useRef<(() => void) | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  const startStream = (targetRole: SpecialistRole, query?: string) => {
    if (!telemetry) return;
    if (streamCancelRef.current) {
      streamCancelRef.current();
    }

    setStreamedText("");
    setIsStreaming(true);
    setErrorMsg(null);

    streamCopilotAdvisory(
      targetRole,
      telemetry,
      query || undefined,
      (chunk) => {
        setStreamedText((prev) => prev + chunk);
        if (scrollRef.current) {
          scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
      },
      () => {
        setIsStreaming(false);
      },
      (err) => {
        console.error("Copilot stream error:", err);
        setErrorMsg("Failed to stream advisory from edge isolate. Using deterministic physical telemetry.");
        setIsStreaming(false);
      }
    ).then((cancelFn) => {
      streamCancelRef.current = cancelFn;
    });
  };

  useEffect(() => {
    if (isOpen && telemetry) {
      setCustomQuery("");
      startStream(role);
    }
    return () => {
      if (streamCancelRef.current) {
        streamCancelRef.current();
      }
    };
  }, [isOpen, role, telemetry]);

  const handleSendQuery = (e?: React.FormEvent) => {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    const q = customQuery.trim();
    if (q) {
      startStream(role, q);
    }
  };

  if (!isOpen || !telemetry) return null;

  const idx = telemetry.narrowband_indices;
  const cont = telemetry.continuum_diagnostics;
  const sub = telemetry.subpixel_abundances;

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full max-w-xl glass-panel border-l border-[#253041] shadow-2xl flex flex-col text-slate-200 animate-in slide-in-from-right duration-200">
      {/* Header */}
      <div className="bg-[#121822] px-5 py-4 border-b border-[#253041] flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          <Sparkles className="w-5 h-5 text-[#00d2ff]" />
          <div>
            <h2 className="font-bold text-sm text-white tracking-wide">REMOTE SENSING SPECIALIST DRAWER</h2>
            <p className="text-[10px] text-slate-400 font-mono">
              Cloudflare Workers AI • Llama 3.1 8B • Physically Grounded
            </p>
          </div>
        </div>

        <button
          onClick={onClose}
          className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#1f2937] transition-all cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Role Selection Tabs */}
      <div className="px-5 pt-4 pb-2 border-b border-[#1f2937] bg-[#0c1017]">
        <label className="block text-[10px] font-semibold text-slate-400 uppercase tracking-wider mb-2 font-mono">
          Specialist Perspective
        </label>
        <div className="grid grid-cols-3 gap-2">
          <button
            onClick={() => setRole("farmer")}
            className={`flex items-center justify-center space-x-1.5 py-2 px-3 rounded-lg border text-xs font-medium transition-all ${
              role === "farmer"
                ? "bg-[#18202c] text-emerald-400 border-emerald-500 shadow-sm"
                : "bg-[#0f141d] text-slate-400 border-[#253041] hover:text-slate-200"
            }`}
          >
            <User className="w-3.5 h-3.5" />
            <span>Farmer Advisory</span>
          </button>

          <button
            onClick={() => setRole("agronomist")}
            className={`flex items-center justify-center space-x-1.5 py-2 px-3 rounded-lg border text-xs font-medium transition-all ${
              role === "agronomist"
                ? "bg-[#18202c] text-[#00d2ff] border-[#00d2ff] shadow-sm"
                : "bg-[#0f141d] text-slate-400 border-[#253041] hover:text-slate-200"
            }`}
          >
            <Microscope className="w-3.5 h-3.5" />
            <span>Agronomist</span>
          </button>

          <button
            onClick={() => setRole("admin")}
            className={`flex items-center justify-center space-x-1.5 py-2 px-3 rounded-lg border text-xs font-medium transition-all ${
              role === "admin"
                ? "bg-[#18202c] text-amber-400 border-amber-500 shadow-sm"
                : "bg-[#0f141d] text-slate-400 border-[#253041] hover:text-slate-200"
            }`}
          >
            <Landmark className="w-3.5 h-3.5" />
            <span>District Admin</span>
          </button>
        </div>
      </div>

      {/* Telemetry Grounding HUD Preview */}
      <div className="px-5 py-3 bg-[#0a0d13] border-b border-[#1f2937] text-[10px] font-mono text-slate-400 flex flex-wrap gap-x-4 gap-y-1">
        <span className="text-slate-500 uppercase font-semibold">Active Parcel Grounding:</span>
        <span>NDRE: <b className="text-slate-200">{idx.ndre}</b></span>
        <span>PRI: <b className="text-slate-200">{idx.pri}</b></span>
        <span>WBI: <b className="text-slate-200">{idx.wbi}</b></span>
        <span>Chl Well: <b className="text-slate-200">{cont.chlorophyll_depth_680nm}</b></span>
        <span>Green%: <b className="text-slate-200">{(sub.healthy_crop_fraction * 100).toFixed(0)}%</b></span>
        <span>Residue%: <b className="text-slate-200">{(sub.dry_residue_fraction * 100).toFixed(0)}%</b></span>
      </div>

      {/* Streamed Output Body */}
      <div ref={scrollRef} className="flex-1 p-5 overflow-y-auto space-y-4 font-sans text-xs leading-relaxed">
        {errorMsg && (
          <div className="p-3 rounded-lg bg-rose-950/40 border border-rose-800 text-rose-300 text-xs">
            {errorMsg}
          </div>
        )}

        <div className="bg-[#0f141d] border border-[#1f2937] rounded-xl p-4 text-slate-200 font-sans text-xs leading-6 shadow-inner space-y-1">
          {streamedText ? (
            formatAdvisoryContent(streamedText)
          ) : (
            <div className="text-slate-500 italic flex items-center space-x-2 font-mono text-[11px]">
              <RefreshCw className="w-3.5 h-3.5 animate-spin text-[#00d2ff]" />
              <span>Synthesizing zero-hallucination physical diagnosis from 425 spectral bands...</span>
            </div>
          )}
          {isStreaming && (
            <span className="inline-block w-2 h-3.5 bg-[#00d2ff] ml-1 animate-pulse" />
          )}
        </div>
      </div>

      {/* Custom Query Input & Regenerate Action */}
      <div className="p-4 bg-[#121822] border-t border-[#253041] space-y-2">
        <form onSubmit={handleSendQuery} className="flex items-center space-x-2">
          <input
            type="text"
            value={customQuery}
            onChange={(e) => setCustomQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSendQuery();
              }
            }}
            placeholder="Ask specific spectroscopic question (e.g. nitrogen dose, stubble risk)..."
            className="flex-1 bg-[#18202c] border border-[#253041] rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-[#00d2ff]"
          />
          <button
            type="button"
            onClick={() => handleSendQuery()}
            disabled={isStreaming || !customQuery.trim()}
            className="px-3 py-2 bg-[#00d2ff] hover:bg-[#38bdf8] text-slate-950 rounded-lg font-medium text-xs flex items-center space-x-1 disabled:opacity-50 cursor-pointer"
          >
            <Send className="w-3.5 h-3.5" />
            <span>Send</span>
          </button>
          <button
            type="button"
            onClick={() => startStream(role, customQuery.trim() || undefined)}
            disabled={isStreaming}
            className="p-2 bg-[#18202c] hover:bg-[#253041] text-slate-300 rounded-lg border border-[#253041] disabled:opacity-50 cursor-pointer"
            title="Re-run diagnostic"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isStreaming ? "animate-spin" : ""}`} />
          </button>
        </form>
      </div>
    </div>
  );
};

function formatAdvisoryContent(text: string) {
  const lines = text.split("\n");
  return lines.map((line, idx) => {
    const trimmed = line.trim();
    if (trimmed.startsWith("### ")) {
      return (
        <h4
          key={idx}
          className="text-[#00d2ff] font-bold text-xs uppercase tracking-wider mt-3 mb-1.5 border-b border-[#253041] pb-1 font-mono"
        >
          {trimmed.replace("### ", "")}
        </h4>
      );
    }
    if (trimmed.startsWith("- **")) {
      const parts = trimmed.slice(2).split("**");
      if (parts.length >= 3) {
        return (
          <div key={idx} className="flex items-start space-x-1.5 py-0.5 text-slate-300">
            <span className="text-[#00d2ff] font-bold mt-0.5">•</span>
            <div>
              <strong className="text-white font-semibold">{parts[1]}:</strong>
              <span>{renderBoldSegments(parts.slice(2).join("**"))}</span>
            </div>
          </div>
        );
      }
    }
    if (trimmed.startsWith("- ")) {
      return (
        <div key={idx} className="flex items-start space-x-1.5 py-0.5 text-slate-300">
          <span className="text-[#00d2ff] font-bold mt-0.5">•</span>
          <div>{renderBoldSegments(trimmed.slice(2))}</div>
        </div>
      );
    }
    if (!trimmed) {
      return <div key={idx} className="h-1.5" />;
    }
    return (
      <p key={idx} className="text-slate-300">
        {renderBoldSegments(line)}
      </p>
    );
  });
}

function renderBoldSegments(text: string) {
  const parts = text.split("**");
  return parts.map((part, i) =>
    i % 2 === 1 ? (
      <strong key={i} className="text-[#38bdf8] font-bold font-mono">
        {part}
      </strong>
    ) : (
      part
    )
  );
}
