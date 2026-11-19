"""
BharatSpectral GIS Spectroscopy Suite
Deterministic Physical Hyperspectral Processing Engine
"""

from src.gis_spectroscopy.wavelength_utils import (
    DEFAULT_AAM_WINDOWS,
    AVIRIS_NG_WAVELENGTHS,
    EMIT_WAVELENGTHS,
    HYSIS_WAVELENGTHS,
    HYSIS_VNIR_WAVELENGTHS,
    HYSIS_SWIR_WAVELENGTHS,
    SENTINEL2_WAVELENGTHS,
    SENSOR_METADATA,
    is_band_masked,
    get_valid_band_indices,
    clamp_reflectance,
    find_closest_band_index,
    get_reflectance_at,
    resample_spectrum,
    resample_cube,
)

from src.gis_spectroscopy.indices import (
    NarrowbandIndices,
    IndexDefinition,
    INDEX_REGISTRY,
    register_index,
    compute_ndre,
    compute_pri,
    compute_wbi,
    compute_ndti,
    compute_mtci,
    compute_ndvi,
    compute_cai,
    compute_narrowband_indices,
    compute_cube_indices,
)

from src.gis_spectroscopy.continuum_removal import (
    ContinuumDiagnostics,
    ContinuumRemovalResult,
    compute_upper_convex_hull_1d,
    compute_local_feature_depth,
    compute_continuum_diagnostics,
    compute_cube_continuum_diagnostics,
    extract_band_depths,
)

from src.gis_spectroscopy.linear_unmixing import (
    SubpixelAbundances,
    project_onto_simplex_1d,
    project_onto_simplex_batch,
    solve_fcls_pgd,
    solve_fcls_scipy,
    solve_fcls_nnls_augmented,
    solve_fcls_batch_pgd,
    unmix_pixel,
    compute_standard_subpixel_abundances,
    compute_cube_unmixing,
    compute_unmixing_residuals,
)

from src.gis_spectroscopy.sam_classifier import (
    SamCandidate,
    SamClassification,
    compute_spectral_angle,
    compute_sam_classification,
    compute_cube_sam,
    evaluate_sam_magnitude_blindness,
)

from src.gis_spectroscopy.endmember_vca import (
    vertex_component_analysis,
    load_reference_library,
    label_endmembers_with_sam,
    run_vca,
)

from src.gis_spectroscopy.pipeline import (
    SensorMetadataPayload,
    CoordinateMetadataPayload,
    SpectralCurvePayload,
    DiagnosticPayload,
    HyperspectralDiagnosticEngine,
)

__all__ = [
    # Wavelength & Masking
    "DEFAULT_AAM_WINDOWS",
    "AVIRIS_NG_WAVELENGTHS",
    "EMIT_WAVELENGTHS",
    "HYSIS_WAVELENGTHS",
    "HYSIS_VNIR_WAVELENGTHS",
    "HYSIS_SWIR_WAVELENGTHS",
    "SENTINEL2_WAVELENGTHS",
    "SENSOR_METADATA",
    "is_band_masked",
    "get_valid_band_indices",
    "clamp_reflectance",
    "find_closest_band_index",
    "get_reflectance_at",
    "resample_spectrum",
    "resample_cube",
    # Indices
    "NarrowbandIndices",
    "IndexDefinition",
    "INDEX_REGISTRY",
    "register_index",
    "compute_ndre",
    "compute_pri",
    "compute_wbi",
    "compute_ndti",
    "compute_mtci",
    "compute_ndvi",
    "compute_cai",
    "compute_narrowband_indices",
    "compute_cube_indices",
    # Continuum Removal
    "ContinuumDiagnostics",
    "ContinuumRemovalResult",
    "compute_upper_convex_hull_1d",
    "compute_local_feature_depth",
    "compute_continuum_diagnostics",
    "compute_cube_continuum_diagnostics",
    "extract_band_depths",
    # Linear Unmixing
    "SubpixelAbundances",
    "project_onto_simplex_1d",
    "project_onto_simplex_batch",
    "solve_fcls_pgd",
    "solve_fcls_scipy",
    "solve_fcls_nnls_augmented",
    "solve_fcls_batch_pgd",
    "unmix_pixel",
    "compute_standard_subpixel_abundances",
    "compute_cube_unmixing",
    "compute_unmixing_residuals",
    # SAM Classifier
    "SamCandidate",
    "SamClassification",
    "compute_spectral_angle",
    "compute_sam_classification",
    "compute_cube_sam",
    "evaluate_sam_magnitude_blindness",
    # VCA
    "vertex_component_analysis",
    "load_reference_library",
    "label_endmembers_with_sam",
    "run_vca",
    # Pipeline & Engine
    "SensorMetadataPayload",
    "CoordinateMetadataPayload",
    "SpectralCurvePayload",
    "DiagnosticPayload",
    "HyperspectralDiagnosticEngine",
]
