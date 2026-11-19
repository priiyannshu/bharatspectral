/**
 * masking.ts - Atmospheric Absorption Masking (AAM)
 * Flags and handles opaque atmospheric water vapor and CO2 bands.
 */

export const ATMOSPHERIC_MASK_WINDOWS: Array<[number, number]> = [
  [1350, 1450], // Atmospheric water vapor absorption
  [1800, 1950], // Atmospheric water vapor & CO2 absorption
];

export function isBandMasked(wavelength: number): boolean {
  for (const [start, end] of ATMOSPHERIC_MASK_WINDOWS) {
    if (wavelength >= start && wavelength <= end) {
      return true;
    }
  }
  return false;
}

export function getValidBandIndices(wavelengths: number[]): number[] {
  const valid: number[] = [];
  for (let i = 0; i < wavelengths.length; i++) {
    if (!isBandMasked(wavelengths[i])) {
      valid.push(i);
    }
  }
  return valid;
}
