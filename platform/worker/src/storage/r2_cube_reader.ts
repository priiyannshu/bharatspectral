/**
 * r2_cube_reader.ts - High-Performance R2 Storage & Seed Fallback Loader
 * Loads calibrated hyperspectral flightline cubes and reference endmember libraries.
 */

import { FlightlineSummary, WorkerEnv } from "../types";

// Static fallback seed data imports for zero-dependency local dev / testing
import manifestData from "../../../data_seed/flightlines_manifest.json";
import endmembersData from "../../../data_seed/endmembers_india.json";
import vidarbhaData from "../../../data_seed/flightlines/vidarbha_wardha_cotton.json";
import punjabData from "../../../data_seed/flightlines/punjab_ludhiana_residue.json";
import anandData from "../../../data_seed/flightlines/gujarat_anand_canopy.json";
import godavariData from "../../../data_seed/flightlines/godavari_delta_wetland.json";

const STATIC_FLIGHTLINES: Record<string, any> = {
  vidarbha_wardha_cotton: vidarbhaData,
  punjab_ludhiana_residue: punjabData,
  gujarat_anand_canopy: anandData,
  godavari_delta_wetland: godavariData,
};

// In-memory cache for fast repeated queries
const cache = new Map<string, any>();

/**
 * Loads flightlines manifest from R2 or fallback seed.
 */
export async function getFlightlinesManifest(env?: WorkerEnv): Promise<any> {
  const cacheKey = "manifest";
  if (cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }

  if (env?.CUBES_BUCKET) {
    try {
      const obj = await env.CUBES_BUCKET.get("metadata/flightlines_manifest.geojson");
      if (obj) {
        const text = await obj.text();
        const parsed = JSON.parse(text);
        cache.set(cacheKey, parsed);
        return parsed;
      }
    } catch (err) {
      console.warn("R2 manifest fetch fallback:", err);
    }
  }

  cache.set(cacheKey, manifestData);
  return manifestData;
}

/**
 * Loads reference endmembers library from R2 or fallback seed.
 */
export async function getReferenceEndmembers(env?: WorkerEnv): Promise<any> {
  const cacheKey = "endmembers";
  if (cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }

  if (env?.CUBES_BUCKET) {
    try {
      const obj = await env.CUBES_BUCKET.get("metadata/endmembers_india.json");
      if (obj) {
        const text = await obj.text();
        const parsed = JSON.parse(text);
        cache.set(cacheKey, parsed);
        return parsed;
      }
    } catch (err) {
      console.warn("R2 endmembers fetch fallback:", err);
    }
  }

  cache.set(cacheKey, endmembersData);
  return endmembersData;
}

/**
 * Loads a flightline cube by ID from R2 or fallback seed.
 */
export async function getFlightlineCube(flightlineId: string, env?: WorkerEnv): Promise<any | null> {
  const cacheKey = `cube:${flightlineId}`;
  if (cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }

  if (env?.CUBES_BUCKET) {
    try {
      const obj = await env.CUBES_BUCKET.get(`flightlines/${flightlineId}.json`);
      if (obj) {
        const text = await obj.text();
        const parsed = JSON.parse(text);
        cache.set(cacheKey, parsed);
        return parsed;
      }
    } catch (err) {
      console.warn(`R2 cube fetch fallback for ${flightlineId}:`, err);
    }
  }

  if (STATIC_FLIGHTLINES[flightlineId]) {
    const data = STATIC_FLIGHTLINES[flightlineId];
    cache.set(cacheKey, data);
    return data;
  }

  return null;
}

/**
 * Finds the nearest spatial pixel parcel in a flightline cube for given (lat, lon).
 */
export function findNearestPixel(cube: any, lat: number, lon: number): any {
  const pixels = cube.pixels;
  if (!pixels || pixels.length === 0) return null;

  let nearest = pixels[0];
  let minDist2 = Infinity;

  for (let i = 0; i < pixels.length; i++) {
    const p = pixels[i];
    const dLat = p.lat - lat;
    const dLon = p.lon - lon;
    const dist2 = dLat * dLat + dLon * dLon;
    if (dist2 < minDist2) {
      minDist2 = dist2;
      nearest = p;
    }
  }

  return nearest;
}
