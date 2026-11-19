/**
 * index.ts - Cloudflare Worker Edge Spectroscopy Engine & Copilot API
 */

import { DiagnosticPayload, WorkerEnv } from "./types";
import { getFlightlinesManifest, getFlightlineCube, getReferenceEndmembers, findNearestPixel } from "./storage/r2_cube_reader";
import { ATMOSPHERIC_MASK_WINDOWS, getValidBandIndices } from "./spectroscopy/masking";
import { computeNarrowbandIndices, getReflectanceAt } from "./spectroscopy/indices";
import { computeContinuumRemoval } from "./spectroscopy/continuum";
import { computeSubpixelAbundances } from "./spectroscopy/unmixing";
import { computeSAMClassification, ReferenceSignature } from "./spectroscopy/sam";
import { handleCopilotStream } from "./ai/copilot";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

function jsonResponse(data: any, status = 200, cacheSeconds = 0): Response {
  const headers: Record<string, string> = {
    "Content-Type": "application/json; charset=utf-8",
    ...CORS_HEADERS,
  };
  if (cacheSeconds > 0) {
    headers["Cache-Control"] = `public, max-age=${cacheSeconds}`;
  } else {
    headers["Cache-Control"] = "no-store";
  }
  return new Response(JSON.stringify(data), { status, headers });
}

export default {
  async fetch(request: Request, env: WorkerEnv, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    try {
      // 1. Health check
      if (url.pathname === "/api/health") {
        return jsonResponse({
          status: "healthy",
          engine: "BharatSpectral-Deterministic-Spectroscopy",
          timestamp: new Date().toISOString(),
        });
      }

      // 2. Flightlines Manifest
      if (url.pathname === "/api/flightlines") {
        const manifest = await getFlightlinesManifest(env);
        return jsonResponse(manifest, 200, 3600);
      }

      // 3. Coordinate Spectrum & Spectroscopy Analysis
      if (url.pathname === "/api/spectrum") {
        const flId = url.searchParams.get("flightline_id") || "vidarbha_wardha_cotton";
        const latStr = url.searchParams.get("lat");
        const lonStr = url.searchParams.get("lon");

        const cube = await getFlightlineCube(flId, env);
        if (!cube) {
          return jsonResponse({ error: `Flightline '${flId}' not found.` }, 404);
        }

        const reqLat = latStr !== null ? parseFloat(latStr) : cube.center[1];
        const reqLon = lonStr !== null ? parseFloat(lonStr) : cube.center[0];

        const pixel = findNearestPixel(cube, reqLat, reqLon);
        if (!pixel) {
          return jsonResponse({ error: "Failed to locate pixel in flightline grid." }, 404);
        }

        const endmembersData = await getReferenceEndmembers(env);
        const wavelengths: number[] = cube.wavelengths;
        const reflectance: number[] = pixel.reflectance;
        const validBandIndices = getValidBandIndices(wavelengths);

        // 1. Narrowband Indices
        const narrowbandIndices = computeNarrowbandIndices(wavelengths, reflectance);

        // 2. Continuum Removal & Diagnostics
        const continuumResult = computeContinuumRemoval(wavelengths, reflectance);

        // 3. Resample reference endmembers to match target sensor's physical wavelengths
        const emWavelengths: number[] = endmembersData.wavelengths || wavelengths;
        const resampledEndmembers: { [key: string]: number[] } = {};
        const isIdenticalGrid =
          emWavelengths.length === wavelengths.length &&
          Math.abs(emWavelengths[0] - wavelengths[0]) < 0.1 &&
          Math.abs(emWavelengths[emWavelengths.length - 1] - wavelengths[wavelengths.length - 1]) < 0.1;

        for (const [key, val] of Object.entries(endmembersData.endmembers as Record<string, any>)) {
          if (isIdenticalGrid) {
            resampledEndmembers[key] = val.reflectance;
          } else {
            resampledEndmembers[key] = wavelengths.map((wl) =>
              getReflectanceAt(emWavelengths, val.reflectance, wl)
            );
          }
        }

        // 4. FCLS Subpixel Abundances
        const subpixelAbundances = computeSubpixelAbundances(reflectance, resampledEndmembers, validBandIndices);

        // 5. SAM Classification
        const refSignatures: ReferenceSignature[] = Object.entries(
          endmembersData.endmembers as Record<string, any>
        ).map(([k, v]) => ({
          id: k,
          label: v.label,
          reflectance: resampledEndmembers[k],
        }));
        const samClassification = computeSAMClassification(reflectance, refSignatures, validBandIndices);

        const payload: DiagnosticPayload = {
          sensor: {
            name: cube.sensor,
            platform: cube.platform,
            total_bands: cube.total_bands,
            valid_bands_used: validBandIndices.length,
            wavelength_range_nm: [wavelengths[0], wavelengths[wavelengths.length - 1]],
            ground_sampling_distance_m: cube.gsd_m,
          },
          coordinates: {
            latitude: pixel.lat,
            longitude: pixel.lon,
            agro_ecological_zone: cube.agro_zone,
            flightline_id: cube.id,
            flightline_name: cube.name,
          },
          spectral_curve: {
            wavelengths,
            reflectance,
            hull_reflectance: continuumResult.hull_reflectance,
            continuum_removed: continuumResult.continuum_removed,
            masked_windows: ATMOSPHERIC_MASK_WINDOWS,
            reference_curves: {
              healthy: resampledEndmembers["green_healthy_canopy"],
              soil: resampledEndmembers["black_cotton_soil"],
              residue: resampledEndmembers["dry_crop_residue"],
            },
          },
          narrowband_indices: narrowbandIndices,
          continuum_diagnostics: continuumResult.diagnostics,
          subpixel_abundances: subpixelAbundances,
          sam_classification: samClassification,
        };

        return jsonResponse(payload, 200, 60);
      }

      // 4. Copilot Chat (SSE Stream)
      if (url.pathname === "/api/copilot/chat" && request.method === "POST") {
        const body = await request.json();
        return await handleCopilotStream(body as any, env);
      }

      return jsonResponse({ error: "Route not found" }, 404);
    } catch (err: any) {
      console.error("Worker Execution Error:", err);
      return jsonResponse({ error: "Internal Spectroscopy Engine Error", details: err?.message }, 500);
    }
  },
};
