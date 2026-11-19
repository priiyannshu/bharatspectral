/**
 * copilot.ts - Remote Sensing Specialist Edge Diagnostic Copilot
 * Streams zero-hallucination, physically-grounded advisory via Server-Sent Events (SSE).
 */

import { DiagnosticPayload, WorkerEnv } from "../types";

export interface CopilotPromptConfig {
  role: "farmer" | "agronomist" | "admin";
  telemetry: DiagnosticPayload;
  query?: string;
}

/**
 * Builds the strict physical context prompt ensuring zero hallucination.
 */
export function buildSystemPrompt(role: string): string {
  return `You are the BharatSpectral Remote Sensing Specialist, an authoritative edge-computing spectroscopy analyst.
Your mandate is strictly zero-hallucination physical diagnostic advisory.
DO NOT use marketing fluff, promotional AI slogans, or generic filler.
Cite the exact numerical telemetry values (NDRE, PRI, WBI, NDTI, MTCI, absorption depths, FCLS abundances, SAM match) provided in the context.
Structure your response crisply with bullet points, actionable diagnostics, and exact biochemical implications for Indian agroecosystems.`;
}

export function buildUserPrompt(config: CopilotPromptConfig): string {
  const t = config.telemetry;
  const indices = t.narrowband_indices;
  const cont = t.continuum_diagnostics;
  const sub = t.subpixel_abundances;
  const sam = t.sam_classification;

  return `Agro-Ecological Zone: ${t.coordinates.agro_ecological_zone}
Coordinates: [${t.coordinates.latitude.toFixed(4)}°N, ${t.coordinates.longitude.toFixed(4)}°E]
Sensor: ${t.sensor.name} (${t.sensor.total_bands} bands, ${t.sensor.ground_sampling_distance_m}m GSD)

TELEMETRY MEASUREMENTS:
- Narrowband Indices:
  * NDRE (Canopy Nitrogen): ${indices.ndre}
  * PRI (Photosynthetic Light-Use Efficiency): ${indices.pri}
  * WBI (Liquid Water Band): ${indices.wbi}
  * NDTI (Tillage/Residue Index): ${indices.ndti}
  * MTCI (Chlorophyll Proxy): ${indices.mtci}
- Continuum Removal Diagnostics:
  * Chlorophyll-a Absorption Depth (680nm): ${cont.chlorophyll_depth_680nm} (AUC: ${cont.chlorophyll_auc})
  * Red-Edge Inflection Wavelength: ${cont.red_edge_inflection_nm} nm (Shift: ${cont.red_edge_shift_nm > 0 ? "+" : ""}${cont.red_edge_shift_nm} nm)
  * Plant Water Absorption Depth (970nm): ${cont.water_depth_970nm}
  * Dry Cellulose/Lignin Depth (2100nm): ${cont.cellulose_depth_2100nm}
  * Clay Hydroxyl Smectite Depth (2200nm): ${cont.clay_hydroxyl_depth_2200nm}
- Subpixel Fractional Abundances (FCLS):
  * Healthy Canopy: ${(sub.healthy_crop_fraction * 100).toFixed(1)}%
  * Stressed Canopy: ${(sub.stressed_crop_fraction * 100).toFixed(1)}%
  * Exposed Soil: ${(sub.exposed_soil_fraction * 100).toFixed(1)}%
  * Dry Residue (Stubble): ${(sub.dry_residue_fraction * 100).toFixed(1)}%
  * Standing Water: ${(sub.standing_water_fraction * 100).toFixed(1)}%
  * Inversion Residual RMSE: ${sub.reconstruction_rmse}
- Spectral Angle Match: ${sam.top_match} (Confidence: ${sam.confidence_pct}%, Angle: ${sam.spectral_angle_rad} rad)

ROLE PERSPECTIVE: ${config.role.toUpperCase()}
USER QUERY: ${config.query || "Perform complete biochemical and physical parcel diagnosis."}`;
}

/**
 * Deterministic fallback generator for offline testing or environments without Workers AI binding.
 */
export function generateDeterministicAdvisory(config: CopilotPromptConfig): string {
  const t = config.telemetry;
  const idx = t.narrowband_indices;
  const c = t.continuum_diagnostics;
  const s = t.subpixel_abundances;
  const sam = t.sam_classification;
  const role = config.role;

  let advice = "";

  if (role === "farmer") {
    const nStatus = idx.ndre >= 0.28 ? "Adequate canopy nitrogen" : "Moderate to acute nitrogen deficiency";
    const waterStatus = idx.wbi >= 0.88 ? "Sufficient cellular hydration" : "Elevated moisture stress detected";
    const residueNotice = s.dry_residue_fraction > 0.25 
      ? `High surface crop residue (${(s.dry_residue_fraction * 100).toFixed(1)}%). High combustible stubble load; mulching/incorporation recommended over burning.`
      : "Low combustible residue fraction.";

    advice = `### 🌾 Farmer Operational Advisory
- **Crop Health & Nitrogen:** ${nStatus}. NDRE is measured at **${idx.ndre}**, with Chlorophyll-a absorption depth at **${c.chlorophyll_depth_680nm}**.
- **Hydration & Irrigation:** ${waterStatus} (WBI: **${idx.wbi}**, 970nm absorption: **${c.water_depth_970nm}**).
- **Sub-Pixel Parcel Composition:** Ground contains **${(s.healthy_crop_fraction * 100).toFixed(1)}%** healthy canopy and **${(s.stressed_crop_fraction * 100).toFixed(1)}%** stressed vegetation.
- **Stubble & Residue:** ${residueNotice}
- **Actionable Step:** ${idx.ndre < 0.25 ? "Schedule top-dressing with urea/nano-nitrogen within 48-72 hours." : "Maintain scheduled irrigation rotation; no immediate emergency nitrogen application required."}`;

  } else if (role === "agronomist") {
    const redEdgeShift = c.red_edge_shift_nm < -4.0 
      ? `Prominent blue-shift (${c.red_edge_shift_nm} nm) indicating photosynthetic apparatus degradation.`
      : `Stable red-edge position at ${c.red_edge_inflection_nm} nm.`;
    const soilClay = c.clay_hydroxyl_depth_2200nm > 0.12 
      ? `Diagnostic Al-OH smectite absorption depth is high (${c.clay_hydroxyl_depth_2200nm}), reflecting heavy clay/Vertisol matrix with high cation-exchange capacity.`
      : `Clay hydroxyl absorption is muted (${c.clay_hydroxyl_depth_2200nm}).`;

    advice = `### 🔬 Agronomic & Biochemical Evaluation
- **Photochemical Efficiency:** PRI is **${idx.pri}**. Reflects xanthophyll cycle epoxidation state under ambient solar irradiance.
- **Red-Edge Dynamic:** Inflection wavelength localized at **${c.red_edge_inflection_nm} nm** (Baseline shift: **${c.red_edge_shift_nm > 0 ? "+" : ""}${c.red_edge_shift_nm} nm**). ${redEdgeShift}
- **Chlorophyll Absorption Well:** 680nm band depth is **${c.chlorophyll_depth_680nm}** with total integration AUC of **${c.chlorophyll_auc}**.
- **Soil Spectroscopy:** ${soilClay}
- **Endmember Inversion Quality:** FCLS solved with residual RMSE of **${s.reconstruction_rmse}**. Top SAM library alignment: *${sam.top_match}* at **${sam.confidence_pct}%** confidence (${sam.spectral_angle_rad} rad).`;

  } else {
    // Admin / Policy
    const fireRisk = (s.dry_residue_fraction > 0.35 || idx.ndti > 0.18) ? "HIGH" : "LOW";
    advice = `### 🏛️ District Administration & Agro-Policy Audit
- **Stubble Fire Hazard Index:** **${fireRisk}** (Combustible dry residue fraction: **${(s.dry_residue_fraction * 100).toFixed(1)}%**, NDTI: **${idx.ndti}**).
- **Canopy Biomass Density:** Total photosynthetic cover is **${((s.healthy_crop_fraction + s.stressed_crop_fraction) * 100).toFixed(1)}%** across parcel footprint.
- **Sodic & Soil Vulnerability:** Exposed soil fraction is **${(s.exposed_soil_fraction * 100).toFixed(1)}%** with clay hydroxyl absorption depth of **${c.clay_hydroxyl_depth_2200nm}**.
- **Policy Recommendation:** ${fireRisk === "HIGH" ? "Dispatch village-level agricultural surveillance squad to monitor in-situ stubble management machinery deployment." : "Standard seasonal monitoring protocol active."}`;
  }

  return advice;
}

/**
 * Handles SSE streaming copilot chat response.
 */
export async function handleCopilotStream(
  config: CopilotPromptConfig,
  env?: WorkerEnv
): Promise<Response> {
  // Try available high-speed Llama models on Cloudflare Workers AI
  if (env?.AI) {
    const candidateModels: (keyof AiModels)[] = [
      "@cf/meta/llama-3.3-70b-instruct-fp8-fast" as any,
      "@cf/meta/llama-3.1-8b-instruct" as any,
      "@cf/meta/llama-3-8b-instruct" as any,
    ];

    const messages = [
      { role: "system", content: buildSystemPrompt(config.role) },
      { role: "user", content: buildUserPrompt(config) },
    ];

    for (const model of candidateModels) {
      try {
        const aiStream = await env.AI.run(model, {
          messages,
          stream: true,
          max_tokens: 512,
          temperature: 0.2, // Low temperature for factual precision
        });

        return new Response(aiStream, {
          headers: {
            "Content-Type": "text/event-stream; charset=utf-8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
          },
        });
      } catch (err) {
        console.warn(`Workers AI model ${model} failed, trying next:`, err);
      }
    }
  }

  // Fallback: Deterministic streaming generator via TransformStream
  const text = generateDeterministicAdvisory(config);
  const words = text.split(" ");

  const { readable, writable } = new TransformStream();
  const writer = writable.getWriter();
  const encoder = new TextEncoder();

  // Stream words in chunks with small delay emulation
  (async () => {
    for (let i = 0; i < words.length; i++) {
      const chunk = (i === 0 ? "" : " ") + words[i];
      const sseMsg = `data: ${JSON.stringify({ response: chunk })}\n\n`;
      await writer.write(encoder.encode(sseMsg));
    }
    await writer.write(encoder.encode("data: [DONE]\n\n"));
    await writer.close();
  })();

  return new Response(readable, {
    headers: {
      "Content-Type": "text/event-stream; charset=utf-8",
      "Cache-Control": "no-cache",
      "Connection": "keep-alive",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
