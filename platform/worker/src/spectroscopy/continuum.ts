/**
 * continuum.ts - Upper Convex Hull & Diagnostic Absorption Depth Analysis
 * Isolates diagnostic absorption features (Chlorophyll, Red-Edge, Cellulose, Clay minerals).
 */

import { ContinuumDiagnostics } from "../types";
import { getReflectanceAt } from "./indices";

export interface ContinuumRemovalResult {
  hull_reflectance: number[];
  continuum_removed: number[];
  diagnostics: ContinuumDiagnostics;
}

interface Point {
  x: number;
  y: number;
  idx: number;
}

/**
 * Computes 2D upper convex hull for monotonic x coordinates (Monotone Chain).
 */
export function computeUpperConvexHull(x: number[], y: number[]): Point[] {
  const n = x.length;
  if (n === 0) return [];
  if (n === 1) return [{ x: x[0], y: y[0], idx: 0 }];

  const points: Point[] = [];
  for (let i = 0; i < n; i++) {
    points.push({ x: x[i], y: y[i], idx: i });
  }

  const hull: Point[] = [];

  for (let i = 0; i < n; i++) {
    const p = points[i];
    while (hull.length >= 2) {
      const p1 = hull[hull.length - 2];
      const p2 = hull[hull.length - 1];
      // Cross product (p2.x - p1.x)*(p.y - p1.y) - (p2.y - p1.y)*(p.x - p1.x)
      // If cross >= 0, point p2 creates an inward concavity from above -> remove it
      const cross = (p2.x - p1.x) * (p.y - p1.y) - (p2.y - p1.y) * (p.x - p1.x);
      if (cross >= 0) {
        hull.pop();
      } else {
        break;
      }
    }
    hull.push(p);
  }

  return hull;
}

/**
 * Evaluates continuum removal and calculates diagnostic parameters.
 */
export function computeContinuumRemoval(
  wavelengths: number[],
  reflectance: number[]
): ContinuumRemovalResult {
  const n = wavelengths.length;
  const hullVertices = computeUpperConvexHull(wavelengths, reflectance);

  const hullReflectance = new Array<number>(n);
  const continuumRemoved = new Array<number>(n);

  let vIdx = 0;
  for (let i = 0; i < n; i++) {
    const wl = wavelengths[i];

    // Advance to matching hull segment
    while (vIdx < hullVertices.length - 2 && wl > hullVertices[vIdx + 1].x) {
      vIdx++;
    }

    const pA = hullVertices[vIdx];
    const pB = hullVertices[Math.min(vIdx + 1, hullVertices.length - 1)];

    let baseline = pA.y;
    if (pB.x > pA.x) {
      const slope = (pB.y - pA.y) / (pB.x - pA.x);
      baseline = pA.y + slope * (wl - pA.x);
    }
    // Baseline cannot be lower than actual reflectance
    baseline = Math.max(baseline, reflectance[i]);
    hullReflectance[i] = Math.round(baseline * 10000) / 10000;

    const cr = baseline > 0.001 ? reflectance[i] / baseline : 1.0;
    continuumRemoved[i] = Math.round(Math.min(1.0, Math.max(0.0, cr)) * 10000) / 10000;
  }

  // 1. Diagnostic Absorption Depths: D = 1 - CR
  const crAt = (targetNm: number) => {
    const r = getReflectanceAt(wavelengths, reflectance, targetNm);
    const h = getReflectanceAt(wavelengths, hullReflectance, targetNm);
    return h > 0.001 ? Math.min(1.0, r / h) : 1.0;
  };

  const chlDepth = Math.max(0.0, 1.0 - crAt(680.0));
  const waterDepth = Math.max(0.0, 1.0 - crAt(970.0));
  const celluloseDepth = Math.max(0.0, 1.0 - crAt(2100.0));
  const clayDepth = Math.max(0.0, 1.0 - crAt(2200.0));

  // 2. Area Under Curve (AUC) for Chlorophyll (650 to 700 nm)
  let chlAuc = 0.0;
  for (let i = 0; i < n - 1; i++) {
    const w1 = wavelengths[i];
    const w2 = wavelengths[i + 1];
    if (w2 >= 650.0 && w1 <= 700.0) {
      const d1 = 1.0 - continuumRemoved[i];
      const d2 = 1.0 - continuumRemoved[i + 1];
      const dw = w2 - w1;
      chlAuc += 0.5 * (d1 + d2) * dw;
    }
  }

  // 3. Red-Edge Inflection Point lambda_re (First derivative peak in 700-745 nm)
  let maxSlope = -Infinity;
  let reInflection = 718.0;

  for (let i = 1; i < n - 1; i++) {
    const wl = wavelengths[i];
    if (wl >= 700.0 && wl <= 745.0) {
      const slope = (reflectance[i + 1] - reflectance[i - 1]) / (wavelengths[i + 1] - wavelengths[i - 1]);
      if (slope > maxSlope) {
        maxSlope = slope;
        reInflection = wl;
      }
    }
  }
  if (maxSlope <= 0) {
    reInflection = 720.0;
  }

  const redEdgeShift = reInflection - 720.0;

  return {
    hull_reflectance: hullReflectance,
    continuum_removed: continuumRemoved,
    diagnostics: {
      chlorophyll_depth_680nm: Math.round(chlDepth * 1000) / 1000,
      chlorophyll_auc: Math.round(chlAuc * 100) / 100,
      red_edge_inflection_nm: Math.round(reInflection * 10) / 10,
      red_edge_shift_nm: Math.round(redEdgeShift * 10) / 10,
      cellulose_depth_2100nm: Math.round(celluloseDepth * 1000) / 1000,
      clay_hydroxyl_depth_2200nm: Math.round(clayDepth * 1000) / 1000,
      water_depth_970nm: Math.round(waterDepth * 1000) / 1000,
    },
  };
}
