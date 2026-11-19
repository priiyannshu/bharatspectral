/**
 * spectroscopy.ts - Frontend Type Definitions
 */

export interface SensorMetadata {
  name: string;
  platform: string;
  total_bands: number;
  valid_bands_used: number;
  wavelength_range_nm: [number, number];
  ground_sampling_distance_m: number;
}

export interface CoordinateMetadata {
  latitude: number;
  longitude: number;
  agro_ecological_zone: string;
  flightline_id: string;
  flightline_name: string;
}

export interface SpectralCurvePayload {
  wavelengths: number[];
  reflectance: number[];
  hull_reflectance: number[];
  continuum_removed: number[];
  masked_windows: Array<[number, number]>;
  reference_curves?: {
    healthy?: number[];
    soil?: number[];
    residue?: number[];
  };
}

export interface NarrowbandIndices {
  ndre: number;
  pri: number;
  wbi: number;
  ndti: number;
  mtci: number;
}

export interface ContinuumDiagnostics {
  chlorophyll_depth_680nm: number;
  chlorophyll_auc: number;
  red_edge_inflection_nm: number;
  red_edge_shift_nm: number;
  cellulose_depth_2100nm: number;
  clay_hydroxyl_depth_2200nm: number;
  water_depth_970nm: number;
}

export interface SubpixelAbundances {
  healthy_crop_fraction: number;
  stressed_crop_fraction: number;
  exposed_soil_fraction: number;
  dry_residue_fraction: number;
  standing_water_fraction: number;
  reconstruction_rmse: number;
}

export interface SamCandidate {
  id: string;
  label: string;
  spectral_angle_rad: number;
  confidence_pct: number;
}

export interface SamClassification {
  top_match: string;
  spectral_angle_rad: number;
  confidence_pct: number;
  candidates: SamCandidate[];
}

export interface DiagnosticPayload {
  sensor: SensorMetadata;
  coordinates: CoordinateMetadata;
  spectral_curve: SpectralCurvePayload;
  narrowband_indices: NarrowbandIndices;
  continuum_diagnostics: ContinuumDiagnostics;
  subpixel_abundances: SubpixelAbundances;
  sam_classification: SamClassification;
}

export interface FlightlineFeature {
  type: "Feature";
  id: string;
  geometry: {
    type: "Polygon";
    coordinates: number[][][];
  };
  properties: {
    id: string;
    name: string;
    sensor: string;
    platform: string;
    total_bands: number;
    gsd_m: number;
    wavelength_range_nm: [number, number];
    center: [number, number];
    bbox: [number, number, number, number];
    agro_zone: string;
    primary_diagnostic: string;
    file: string;
  };
}

export interface FlightlinesManifest {
  type: "FeatureCollection";
  description: string;
  total_flightlines: number;
  features: FlightlineFeature[];
}

export type BandRenderingMode = "rgb" | "cir" | "ndre" | "ndti";
export type SpecialistRole = "farmer" | "agronomist" | "admin";
export type BasemapMode = "dark" | "satellite";
