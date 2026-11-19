/**
 * api.ts - Worker API Client for BharatSpectral
 */

import { DiagnosticPayload, FlightlinesManifest, SpecialistRole } from "../types/spectroscopy";

const API_BASE = "https://bharatspectral-worker.priyanshukh1201.workers.dev";

export async function fetchFlightlines(): Promise<FlightlinesManifest> {
  const res = await fetch(`${API_BASE}/api/flightlines`);
  if (!res.ok) {
    throw new Error(`Failed to fetch flightlines manifest: ${res.statusText}`);
  }
  return await res.json();
}

export async function fetchSpectrum(
  flightlineId: string,
  lat?: number,
  lon?: number
): Promise<DiagnosticPayload> {
  let url = `${API_BASE}/api/spectrum?flightline_id=${encodeURIComponent(flightlineId)}`;
  if (lat !== undefined && lon !== undefined) {
    url += `&lat=${lat}&lon=${lon}`;
  }
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch spectrum telemetry: ${res.statusText}`);
  }
  return await res.json();
}

export async function streamCopilotAdvisory(
  role: SpecialistRole,
  telemetry: DiagnosticPayload,
  query: string | undefined,
  onChunk: (text: string) => void,
  onDone: () => void,
  onError: (err: any) => void
): Promise<() => void> {
  const controller = new AbortController();

  (async () => {
    try {
      const res = await fetch(`${API_BASE}/api/copilot/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ role, telemetry, query }),
        signal: controller.signal,
      });

      if (!res.ok || !res.body) {
        throw new Error(`Copilot streaming error: ${res.statusText}`);
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed.startsWith("data:")) continue;

          const dataStr = trimmed.slice(5).trim();
          if (dataStr === "[DONE]") {
            onDone();
            return;
          }

          try {
            const parsed = JSON.parse(dataStr);
            // Handle both Cloudflare OpenAI-compatible chunks and custom response formats
            const textChunk =
              parsed.response !== undefined
                ? parsed.response
                : parsed.choices?.[0]?.delta?.content !== undefined
                ? parsed.choices[0].delta.content
                : parsed.choices?.[0]?.text !== undefined
                ? parsed.choices[0].text
                : "";

            if (textChunk) {
              onChunk(textChunk);
            }
          } catch {
            // Raw text fallback
            onChunk(dataStr);
          }
        }
      }
      onDone();
    } catch (err: any) {
      if (err.name !== "AbortError") {
        onError(err);
      }
    }
  })();

  // Return cancel function
  return () => controller.abort();
}
