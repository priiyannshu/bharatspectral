/**
 * unmixing.ts - Fully Constrained Linear Spectral Unmixing (FCLS)
 * Solves convex quadratic programming subject to Non-Negativity (ANC)
 * and Sum-to-One (ASC) constraints via Projected Gradient Descent on the Simplex.
 */

import { SubpixelAbundances } from "../types";

/**
 * Projects an arbitrary vector onto the probability simplex:
 * Delta = { x in R^p | x >= 0 and sum(x) = 1 }
 * Exact O(p log p) algorithm by Wang & Carreira-Perpinan.
 */
export function projectOntoSimplex(v: number[]): number[] {
  const p = v.length;
  if (p === 0) return [];
  if (p === 1) return [1.0];

  const u = [...v].sort((a, b) => b - a);
  let cumulativeSum = 0;
  let rho = 0;

  for (let j = 0; j < p; j++) {
    cumulativeSum += u[j];
    const condition = u[j] - (cumulativeSum - 1.0) / (j + 1);
    if (condition > 0) {
      rho = j;
    }
  }

  let finalSum = 0;
  for (let j = 0; j <= rho; j++) {
    finalSum += u[j];
  }

  const theta = (finalSum - 1.0) / (rho + 1);
  const projected = v.map((val) => Math.max(0.0, val - theta));

  // Normalize for slight floating point precision artifacts
  const sumProj = projected.reduce((acc, val) => acc + val, 0);
  return sumProj > 0 ? projected.map((val) => val / sumProj) : v.map(() => 1 / p);
}

export interface EndmemberMatrix {
  labels: string[];
  keys: string[];
  matrix: number[][]; // [num_bands][num_endmembers]
}

/**
 * Computes FCLS subpixel fractional abundances.
 */
export function solveFCLS(
  pixelReflectance: number[],
  endmembers: { [key: string]: number[] },
  validBandIndices?: number[],
  maxIterations = 100
): { abundances: { [key: string]: number }; rmse: number } {
  const keys = Object.keys(endmembers);
  const p = keys.length;
  const bands = validBandIndices || pixelReflectance.map((_, i) => i);
  const B = bands.length;

  if (p === 0 || B === 0) {
    return { abundances: {}, rmse: 0 };
  }

  // Precompute Gram matrix M = E^T * E and trace for Lipschitz step size
  const E: number[][] = []; // [B][p]
  for (let b = 0; b < B; b++) {
    const bandIdx = bands[b];
    const row = new Array<number>(p);
    for (let j = 0; j < p; j++) {
      row[j] = endmembers[keys[j]][bandIdx] || 0.0;
    }
    E.push(row);
  }

  const y: number[] = bands.map((b) => pixelReflectance[b]);

  // b_vec = E^T * y (size p)
  const bVec = new Array<number>(p).fill(0);
  for (let j = 0; j < p; j++) {
    let sum = 0;
    for (let b = 0; b < B; b++) {
      sum += E[b][j] * y[b];
    }
    bVec[j] = sum;
  }

  // M = E^T * E (size p x p)
  const M: number[][] = Array.from({ length: p }, () => new Array<number>(p).fill(0));
  let traceM = 0;
  for (let i = 0; i < p; i++) {
    for (let j = 0; j < p; j++) {
      let sum = 0;
      for (let b = 0; b < B; b++) {
        sum += E[b][i] * E[b][j];
      }
      M[i][j] = sum;
      if (i === j) traceM += sum;
    }
  }

  const stepSize = 1.0 / Math.max(1e-4, traceM);

  // Initialize alpha uniformly on the simplex
  let alpha = new Array<number>(p).fill(1.0 / p);

  // Projected Gradient Descent
  for (let iter = 0; iter < maxIterations; iter++) {
    // grad = M * alpha - b_vec
    const grad = new Array<number>(p).fill(0);
    for (let i = 0; i < p; i++) {
      let sum = 0;
      for (let j = 0; j < p; j++) {
        sum += M[i][j] * alpha[j];
      }
      grad[i] = sum - bVec[i];
    }

    // Step: v = alpha - stepSize * grad
    const v = alpha.map((a, i) => a - stepSize * grad[i]);

    // Project onto simplex
    alpha = projectOntoSimplex(v);
  }

  // Calculate reconstruction RMSE
  let sse = 0;
  for (let b = 0; b < B; b++) {
    let reconstructed = 0;
    for (let j = 0; j < p; j++) {
      reconstructed += E[b][j] * alpha[j];
    }
    const err = y[b] - reconstructed;
    sse += err * err;
  }
  const rmse = Math.sqrt(sse / B);

  const abundanceMap: { [key: string]: number } = {};
  for (let j = 0; j < p; j++) {
    abundanceMap[keys[j]] = Math.round(alpha[j] * 1000) / 1000;
  }

  return {
    abundances: abundanceMap,
    rmse: Math.round(rmse * 10000) / 10000,
  };
}

/**
 * Standard unmixing mapper returning typed SubpixelAbundances.
 */
export function computeSubpixelAbundances(
  pixelReflectance: number[],
  referenceEndmembers: { [key: string]: number[] },
  validBandIndices?: number[]
): SubpixelAbundances {
  const result = solveFCLS(pixelReflectance, referenceEndmembers, validBandIndices);
  const a = result.abundances;

  return {
    healthy_crop_fraction: a["green_healthy_canopy"] ?? 0.0,
    stressed_crop_fraction: a["stressed_crop"] ?? 0.0,
    exposed_soil_fraction: a["black_cotton_soil"] ?? 0.0,
    dry_residue_fraction: a["dry_crop_residue"] ?? 0.0,
    standing_water_fraction: a["standing_water"] ?? 0.0,
    reconstruction_rmse: result.rmse,
  };
}
