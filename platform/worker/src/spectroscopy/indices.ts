/**
 * indices.ts - Deterministic Narrowband Hyperspectral Indices
 * Evaluates physiological and biochemical indices without saturation.
 */

import { NarrowbandIndices } from "../types";

/**
 * Finds the index of the closest wavelength in a sorted array.
 */
export function findClosestBandIndex(wavelengths: number[], targetNm: number): number {
  let closestIdx = 0;
  let minDiff = Math.abs(wavelengths[0] - targetNm);

  for (let i = 1; i < wavelengths.length; i++) {
    const diff = Math.abs(wavelengths[i] - targetNm);
    if (diff < minDiff) {
      minDiff = diff;
      closestIdx = i;
    }
  }
  return closestIdx;
}

/**
 * Linearly interpolates reflectance at a target wavelength.
 */
export function getReflectanceAt(wavelengths: number[], reflectance: number[], targetNm: number): number {
  if (wavelengths.length === 0 || reflectance.length === 0) return 0;
  if (targetNm <= wavelengths[0]) return reflectance[0];
  if (targetNm >= wavelengths[wavelengths.length - 1]) return reflectance[reflectance.length - 1];

  const idx = findClosestBandIndex(wavelengths, targetNm);
  if (wavelengths[idx] === targetNm) return reflectance[idx];

  const lowerIdx = wavelengths[idx] < targetNm ? idx : Math.max(0, idx - 1);
  const upperIdx = lowerIdx + 1 < wavelengths.length ? lowerIdx + 1 : lowerIdx;

  if (lowerIdx === upperIdx) return reflectance[lowerIdx];

  const x0 = wavelengths[lowerIdx];
  const x1 = wavelengths[upperIdx];
  const y0 = reflectance[lowerIdx];
  const y1 = reflectance[upperIdx];

  const dx = x1 - x0;
  if (Math.abs(dx) < 1e-6) return y0;

  const t = (targetNm - x0) / dx;
  return y0 + t * (y1 - y0);
}

/**
 * Computes all 5 narrowband hyperspectral indices.
 */
export function computeNarrowbandIndices(
  wavelengths: number[],
  reflectance: number[]
): NarrowbandIndices {
  const r531 = getReflectanceAt(wavelengths, reflectance, 531.0);
  const r570 = getReflectanceAt(wavelengths, reflectance, 570.0);
  const r681 = getReflectanceAt(wavelengths, reflectance, 681.0);
  const r708 = getReflectanceAt(wavelengths, reflectance, 708.0);
  const r720 = getReflectanceAt(wavelengths, reflectance, 720.0);
  const r753 = getReflectanceAt(wavelengths, reflectance, 753.0);
  const r790 = getReflectanceAt(wavelengths, reflectance, 790.0);
  const r900 = getReflectanceAt(wavelengths, reflectance, 900.0);
  const r970 = getReflectanceAt(wavelengths, reflectance, 970.0);
  const r1660 = getReflectanceAt(wavelengths, reflectance, 1660.0);
  const r2330 = getReflectanceAt(wavelengths, reflectance, 2330.0);

  // 1. NDRE = (R790 - R720) / (R790 + R720)
  const ndreDenom = r790 + r720;
  const ndre = ndreDenom !== 0 ? (r790 - r720) / ndreDenom : 0.0;

  // 2. PRI = (R531 - R570) / (R531 + R570)
  const priDenom = r531 + r570;
  const pri = priDenom !== 0 ? (r531 - r570) / priDenom : 0.0;

  // 3. WBI = R900 / R970
  const wbi = r970 > 0.001 ? r900 / r970 : 1.0;

  // 4. NDTI = (R1660 - R2330) / (R1660 + R2330)
  const ndtiDenom = r1660 + r2330;
  const ndti = ndtiDenom !== 0 ? (r1660 - r2330) / ndtiDenom : 0.0;

  // 5. MTCI = (R753 - R708) / (R708 - R681)
  const mtciDenom = r708 - r681;
  const mtci = Math.abs(mtciDenom) > 0.001 ? (r753 - r708) / mtciDenom : 1.0;

  return {
    ndre: Math.round(ndre * 1000) / 1000,
    pri: Math.round(pri * 1000) / 1000,
    wbi: Math.round(wbi * 1000) / 1000,
    ndti: Math.round(ndti * 1000) / 1000,
    mtci: Math.round(Math.min(10.0, Math.max(-5.0, mtci)) * 100) / 100,
  };
}
