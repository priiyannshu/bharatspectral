/**
 * sam.ts - Spectral Angle Mapper (SAM) Similarity Classifier
 * Evaluates n-dimensional spectral angle between pixel vector and endmember signatures.
 */

import { SamCandidate, SamClassification } from "../types";

export interface ReferenceSignature {
  id: string;
  label: string;
  reflectance: number[];
}

export function computeSAMClassification(
  pixelReflectance: number[],
  references: ReferenceSignature[],
  validBandIndices?: number[]
): SamClassification {
  const bands = validBandIndices || pixelReflectance.map((_, i) => i);
  const B = bands.length;

  if (references.length === 0 || B === 0) {
    return {
      top_match: "Unknown Material",
      spectral_angle_rad: 0,
      confidence_pct: 0,
      candidates: [],
    };
  }

  // Pixel norm over valid bands
  let normY2 = 0;
  for (let b = 0; b < B; b++) {
    const val = pixelReflectance[bands[b]];
    normY2 += val * val;
  }
  const normY = Math.sqrt(normY2);

  const candidates: SamCandidate[] = [];

  for (const ref of references) {
    let dot = 0;
    let normRef2 = 0;

    for (let b = 0; b < B; b++) {
      const idx = bands[b];
      const yVal = pixelReflectance[idx];
      const rVal = ref.reflectance[idx] || 0;
      dot += yVal * rVal;
      normRef2 += rVal * rVal;
    }

    const normRef = Math.sqrt(normRef2);
    const denom = normY * normRef;

    let cosTheta = denom > 1e-6 ? dot / denom : 0;
    cosTheta = Math.max(-1.0, Math.min(1.0, cosTheta));

    const angleRad = Math.acos(cosTheta);
    // Confidence is 100% at 0 rad, 0% at pi/2 rad (90 deg)
    const confidencePct = Math.max(0.0, Math.min(100.0, (1.0 - angleRad / (Math.PI / 2)) * 100));

    candidates.push({
      id: ref.id,
      label: ref.label,
      spectral_angle_rad: Math.round(angleRad * 1000) / 1000,
      confidence_pct: Math.round(confidencePct * 10) / 10,
    });
  }

  // Sort candidates by smallest spectral angle (highest similarity)
  candidates.sort((a, b) => a.spectral_angle_rad - b.spectral_angle_rad);

  const top = candidates[0];

  return {
    top_match: top ? top.label : "Unknown Material",
    spectral_angle_rad: top ? top.spectral_angle_rad : 0,
    confidence_pct: top ? top.confidence_pct : 0,
    candidates,
  };
}
