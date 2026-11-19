import { describe, it, expect } from "vitest";
import { computeNarrowbandIndices, findClosestBandIndex, getReflectanceAt } from "../src/spectroscopy/indices";
import { computeContinuumRemoval, computeUpperConvexHull } from "../src/spectroscopy/continuum";
import { projectOntoSimplex, solveFCLS, computeSubpixelAbundances } from "../src/spectroscopy/unmixing";
import { computeSAMClassification } from "../src/spectroscopy/sam";
import { isBandMasked, getValidBandIndices } from "../src/spectroscopy/masking";
import worker from "../src/index";

describe("Deterministic Spectroscopy Math Suite", () => {
  it("Atmospheric Masking flags water vapor windows correctly", () => {
    expect(isBandMasked(1400)).toBe(true);
    expect(isBandMasked(1850)).toBe(true);
    expect(isBandMasked(680)).toBe(false);
    expect(isBandMasked(850)).toBe(false);
    expect(isBandMasked(2200)).toBe(false);
  });

  it("Wavelength interpolation and band index finding", () => {
    const wls = [400, 500, 600, 700, 800];
    const r = [0.1, 0.2, 0.3, 0.4, 0.5];

    expect(findClosestBandIndex(wls, 510)).toBe(1);
    expect(findClosestBandIndex(wls, 690)).toBe(3);
    expect(getReflectanceAt(wls, r, 550)).toBeCloseTo(0.25, 4);
  });

  it("Narrowband Indices calculation", () => {
    const wls = [531, 570, 681, 708, 720, 753, 790, 900, 970, 1660, 2330];
    // Realistic green canopy sample values
    const r = [0.08, 0.12, 0.05, 0.20, 0.28, 0.45, 0.50, 0.48, 0.42, 0.22, 0.10];

    const idx = computeNarrowbandIndices(wls, r);
    // NDRE = (0.50 - 0.28) / (0.50 + 0.28) = 0.22 / 0.78 = 0.282
    expect(idx.ndre).toBeCloseTo(0.282, 2);
    // PRI = (0.08 - 0.12) / (0.08 + 0.12) = -0.04 / 0.20 = -0.200
    expect(idx.pri).toBeCloseTo(-0.200, 2);
    // WBI = 0.48 / 0.42 = 1.143
    expect(idx.wbi).toBeCloseTo(1.143, 2);
    // NDTI = (0.22 - 0.10) / (0.22 + 0.10) = 0.12 / 0.32 = 0.375
    expect(idx.ndti).toBeCloseTo(0.375, 2);
  });

  it("Upper Convex Hull & Continuum Removal", () => {
    // Dip at 680nm between peaks at 550nm and 750nm
    const wls = [500, 550, 600, 680, 750, 850];
    const r =   [0.10, 0.20, 0.15, 0.05, 0.50, 0.52];

    const res = computeContinuumRemoval(wls, r);
    expect(res.hull_reflectance.length).toBe(wls.length);
    expect(res.continuum_removed.length).toBe(wls.length);

    // Continuum at 680nm should be above 0.05, so absorption depth > 0
    expect(res.diagnostics.chlorophyll_depth_680nm).toBeGreaterThan(0.5);
    // Hull should never be below original reflectance
    for (let i = 0; i < wls.length; i++) {
      expect(res.hull_reflectance[i]).toBeGreaterThanOrEqual(r[i] - 1e-6);
    }
  });

  it("Simplex Projection satisfies sum-to-one and non-negativity", () => {
    const rawVectors = [
      [0.8, 0.4, 0.1],
      [-0.5, 1.2, 0.3, 0.0],
      [10.0, 5.0, 0.0],
      [0.2, 0.2, 0.2, 0.2, 0.2],
    ];

    for (const vec of rawVectors) {
      const proj = projectOntoSimplex(vec);
      const sum = proj.reduce((a, b) => a + b, 0);
      expect(sum).toBeCloseTo(1.0, 4);
      for (const val of proj) {
        expect(val).toBeGreaterThanOrEqual(0.0);
      }
    }
  });

  it("FCLS Unmixing accurately recovers synthetic mixed abundances", () => {
    const bands = 50;
    const em1 = new Array(bands).fill(0).map((_, i) => 0.1 + 0.01 * i);
    const em2 = new Array(bands).fill(0).map((_, i) => 0.5 - 0.005 * i);

    // Create 70% em1 + 30% em2 mixture
    const mixed = new Array(bands).fill(0).map((_, i) => 0.7 * em1[i] + 0.3 * em2[i]);

    const res = solveFCLS(mixed, { em1, em2 });
    expect(res.abundances.em1).toBeCloseTo(0.7, 2);
    expect(res.abundances.em2).toBeCloseTo(0.3, 2);
    expect(res.rmse).toBeLessThan(0.001);
  });

  it("Spectral Angle Mapper gives 0 rad angle for identical spectrum", () => {
    const spec = [0.1, 0.2, 0.4, 0.5, 0.3];
    const refs = [
      { id: "mat1", label: "Material 1", reflectance: [0.1, 0.2, 0.4, 0.5, 0.3] },
      { id: "mat2", label: "Material 2", reflectance: [0.5, 0.4, 0.2, 0.1, 0.1] },
    ];

    const result = computeSAMClassification(spec, refs);
    expect(result.top_match).toBe("Material 1");
    expect(result.spectral_angle_rad).toBe(0);
    expect(result.confidence_pct).toBe(100);
  });
});

describe("Cloudflare Worker API Routes", () => {
  const mockCtx = {} as any;

  it("GET /api/health returns healthy status", async () => {
    const req = new Request("http://localhost/api/health");
    const res = await worker.fetch(req, {}, mockCtx);
    expect(res.status).toBe(200);
    const json = await res.json() as any;
    expect(json.status).toBe("healthy");
    expect(json.engine).toBe("BharatSpectral-Deterministic-Spectroscopy");
  });

  it("GET /api/flightlines returns manifest with 4 corridors", async () => {
    const req = new Request("http://localhost/api/flightlines");
    const res = await worker.fetch(req, {}, mockCtx);
    expect(res.status).toBe(200);
    const json = await res.json() as any;
    expect(json.type).toBe("FeatureCollection");
    expect(json.features.length).toBe(4);
  });

  it("GET /api/spectrum returns complete diagnostic payload", async () => {
    const req = new Request("http://localhost/api/spectrum?flightline_id=vidarbha_wardha_cotton&lat=20.75&lon=78.60");
    const res = await worker.fetch(req, {}, mockCtx);
    expect(res.status).toBe(200);
    const data = await res.json() as any;

    expect(data.sensor.name).toBe("AVIRIS-NG India");
    expect(data.sensor.total_bands).toBe(425);
    expect(data.spectral_curve.reflectance.length).toBe(425);
    expect(data.spectral_curve.hull_reflectance.length).toBe(425);

    // Narrowband indices present
    expect(data.narrowband_indices.ndre).toBeDefined();
    expect(data.narrowband_indices.pri).toBeDefined();
    expect(data.narrowband_indices.wbi).toBeDefined();

    // Continuum diagnostics present
    expect(data.continuum_diagnostics.chlorophyll_depth_680nm).toBeDefined();
    expect(data.continuum_diagnostics.red_edge_inflection_nm).toBeGreaterThan(700);

    // FCLS Abundances sum to 1.0
    const sumFcls =
      data.subpixel_abundances.healthy_crop_fraction +
      data.subpixel_abundances.stressed_crop_fraction +
      data.subpixel_abundances.exposed_soil_fraction +
      data.subpixel_abundances.dry_residue_fraction +
      data.subpixel_abundances.standing_water_fraction;
    expect(sumFcls).toBeCloseTo(1.0, 2);

    // SAM classification present
    expect(data.sam_classification.top_match).toBeDefined();
    expect(data.sam_classification.confidence_pct).toBeGreaterThan(0);

    // Reference curves present for overlays
    expect(data.spectral_curve.reference_curves).toBeDefined();
    expect(data.spectral_curve.reference_curves.healthy.length).toBe(425);
    expect(data.spectral_curve.reference_curves.soil.length).toBe(425);
    expect(data.spectral_curve.reference_curves.residue.length).toBe(425);
  });

  it("GET /api/spectrum correctly resamples endmembers for NASA EMIT (285 bands)", async () => {
    const req = new Request("http://localhost/api/spectrum?flightline_id=punjab_ludhiana_residue&lat=30.9&lon=75.86");
    const res = await worker.fetch(req, {}, mockCtx);
    expect(res.status).toBe(200);
    const data = await res.json() as any;

    expect(data.sensor.name).toBe("NASA EMIT");
    expect(data.sensor.total_bands).toBe(285);
    expect(data.spectral_curve.reflectance.length).toBe(285);
    expect(data.spectral_curve.hull_reflectance.length).toBe(285);

    // Endmember reference curves must be resampled to exactly 285 bands matching EMIT
    expect(data.spectral_curve.reference_curves.healthy.length).toBe(285);
    expect(data.spectral_curve.reference_curves.residue.length).toBe(285);

    // Stubble residue corridor should identify combustible residue
    const sumFcls =
      data.subpixel_abundances.healthy_crop_fraction +
      data.subpixel_abundances.stressed_crop_fraction +
      data.subpixel_abundances.exposed_soil_fraction +
      data.subpixel_abundances.dry_residue_fraction +
      data.subpixel_abundances.standing_water_fraction;
    expect(sumFcls).toBeCloseTo(1.0, 2);
    expect(data.subpixel_abundances.dry_residue_fraction).toBeGreaterThan(0.2);
    expect(data.subpixel_abundances.reconstruction_rmse).toBeLessThan(0.05);

    // SAM match
    expect(data.sam_classification.top_match).toBeDefined();
    expect(data.sam_classification.confidence_pct).toBeGreaterThan(60);
  });

  it("GET /api/spectrum handles all 4 curated flightline zones", async () => {
    const zones = [
      { id: "vidarbha_wardha_cotton", expectedBands: 425 },
      { id: "punjab_ludhiana_residue", expectedBands: 285 },
      { id: "gujarat_anand_canopy", expectedBands: 425 },
      { id: "godavari_delta_wetland", expectedBands: 285 },
    ];

    for (const z of zones) {
      const req = new Request(`http://localhost/api/spectrum?flightline_id=${z.id}`);
      const res = await worker.fetch(req, {}, mockCtx);
      expect(res.status).toBe(200);
      const data = await res.json() as any;
      expect(data.sensor.total_bands).toBe(z.expectedBands);
      expect(data.spectral_curve.reflectance.length).toBe(z.expectedBands);
      expect(data.spectral_curve.reference_curves.healthy.length).toBe(z.expectedBands);
    }
  });

  it("GET /api/spectrum returns 404 for non-existent flightline ID", async () => {
    const req = new Request("http://localhost/api/spectrum?flightline_id=non_existent_zone");
    const res = await worker.fetch(req, {}, mockCtx);
    expect(res.status).toBe(404);
    const json = await res.json() as any;
    expect(json.error).toContain("not found");
  });

  it("POST /api/copilot/chat streams diagnostic advisory", async () => {
    const samplePayload = {
      role: "farmer",
      telemetry: {
        sensor: { name: "AVIRIS-NG India", total_bands: 425, ground_sampling_distance_m: 4.8 },
        coordinates: { agro_ecological_zone: "Deccan Plateau", latitude: 20.75, longitude: 78.60 },
        narrowband_indices: { ndre: 0.32, pri: -0.04, wbi: 0.91, ndti: 0.08, mtci: 1.5 },
        continuum_diagnostics: {
          chlorophyll_depth_680nm: 0.38,
          chlorophyll_auc: 14.2,
          red_edge_inflection_nm: 719.5,
          red_edge_shift_nm: -0.5,
          cellulose_depth_2100nm: 0.03,
          clay_hydroxyl_depth_2200nm: 0.18,
          water_depth_970nm: 0.11,
        },
        subpixel_abundances: {
          healthy_crop_fraction: 0.65,
          stressed_crop_fraction: 0.15,
          exposed_soil_fraction: 0.20,
          dry_residue_fraction: 0.0,
          standing_water_fraction: 0.0,
          reconstruction_rmse: 0.008,
        },
        sam_classification: {
          top_match: "Gossypium hirsutum (Green Healthy Canopy)",
          spectral_angle_rad: 0.045,
          confidence_pct: 97.1,
          candidates: [],
        },
      },
    };

    const req = new Request("http://localhost/api/copilot/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(samplePayload),
    });

    const res = await worker.fetch(req, {}, mockCtx);
    expect(res.status).toBe(200);
    expect(res.headers.get("Content-Type")).toContain("text/event-stream");
    const text = await res.text();
    expect(text).toContain("data:");
    expect(text).toContain("[DONE]");
  });
});
