"""
test_spectroscopy_engine.py - End-to-End Test Suite for Deterministic Spectroscopy

Verifies mathematical rigor, physical constraints, multi-sensor alignment,
and schema parity with Cloudflare Worker engine JSON contract:
- FCLS physical validity: sum-to-one (1.000 +- 0.001) & non-negativity (>= 0)
- Simplex projection exactness
- Absorption depth physical bounds & convex hull baseline
- SAM angle calculation and magnitude blindness verification
- VCA endmember extraction and automated labeling
- Real seed flightline integration (Vidarbha, Punjab, Gujarat, Godavari)
- Single-pixel execution latency benchmark (< 5.0 ms)
"""

import os
import json
import time
import pytest
import numpy as np

from src.gis_spectroscopy.wavelength_utils import (
    DEFAULT_AAM_WINDOWS,
    AVIRIS_NG_WAVELENGTHS,
    EMIT_WAVELENGTHS,
    HYSIS_WAVELENGTHS,
    SENTINEL2_WAVELENGTHS,
    is_band_masked,
    get_valid_band_indices,
    clamp_reflectance,
    find_closest_band_index,
    get_reflectance_at,
    resample_spectrum,
    resample_cube,
)

from src.gis_spectroscopy.indices import (
    compute_narrowband_indices,
    compute_cube_indices,
    INDEX_REGISTRY,
)

from src.gis_spectroscopy.continuum_removal import (
    compute_upper_convex_hull_1d,
    compute_local_feature_depth,
    compute_continuum_diagnostics,
    compute_cube_continuum_diagnostics,
    extract_band_depths,
)

from src.gis_spectroscopy.linear_unmixing import (
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
    HyperspectralDiagnosticEngine,
    DiagnosticPayload,
)


class TestWavelengthAndMasking:
    def test_atmospheric_masking_windows(self):
        # Window 1 (1350-1440 nm)
        assert is_band_masked(1350.0) is True
        assert is_band_masked(1400.0) is True
        assert is_band_masked(1440.0) is True

        # Window 2 (1800-1950 nm)
        assert is_band_masked(1800.0) is True
        assert is_band_masked(1850.0) is True
        assert is_band_masked(1950.0) is True

        # Clean biological diagnostic bands
        assert is_band_masked(550.0) is False   # Green peak
        assert is_band_masked(680.0) is False   # Chlorophyll well
        assert is_band_masked(720.0) is False   # Red-edge
        assert is_band_masked(850.0) is False   # NIR plateau
        assert is_band_masked(2100.0) is False  # Cellulose
        assert is_band_masked(2200.0) is False  # Clay mineral

    def test_clamping(self):
        raw = np.array([-0.05, 0.0, 0.45, 1.0, 1.35])
        clamped = clamp_reflectance(raw, 0.0, 1.0)
        assert clamped[0] == 0.0
        assert clamped[-1] == 1.0
        assert np.all((clamped >= 0.0) & (clamped <= 1.0))

    def test_nan_and_inf_clamping(self):
        raw = np.array([-0.5, np.nan, 0.45, np.inf, -np.inf, 1.5])
        clamped = clamp_reflectance(raw, 0.0, 1.0)
        assert not np.isnan(clamped).any()
        assert not np.isinf(clamped).any()
        assert np.all((clamped >= 0.0) & (clamped <= 1.0))
        assert clamped[1] == 0.0
        assert clamped[3] == 1.0
        assert clamped[4] == 0.0

    def test_band_interpolation(self):
        wls = np.array([400.0, 500.0, 600.0, 700.0, 800.0])
        r = np.array([0.1, 0.2, 0.3, 0.4, 0.5])

        assert find_closest_band_index(wls, 510.0) == 1
        assert find_closest_band_index(wls, 690.0) == 3

        interp_val = get_reflectance_at(wls, r, 550.0)
        assert pytest.approx(interp_val, rel=1e-4) == 0.25

        # Multi-dimensional interpolation
        cube_sample = np.zeros((2, 2, 5))
        cube_sample[:, :] = r
        cube_interp = get_reflectance_at(wls, cube_sample, 550.0)
        assert cube_interp.shape == (2, 2)
        assert np.allclose(cube_interp, 0.25)

    def test_resample_sensors(self):
        aviris_r = np.sin(np.linspace(0, np.pi, len(AVIRIS_NG_WAVELENGTHS)))
        emit_r = resample_spectrum(AVIRIS_NG_WAVELENGTHS, aviris_r, EMIT_WAVELENGTHS)
        assert len(emit_r) == len(EMIT_WAVELENGTHS)
        assert not np.isnan(emit_r).any()


class TestNarrowbandIndices:
    def test_known_values_parity_with_worker(self):
        # Match test case from TypeScript test suite
        wls = [531.0, 570.0, 681.0, 708.0, 720.0, 753.0, 790.0, 900.0, 970.0, 1660.0, 2330.0]
        r = [0.08, 0.12, 0.05, 0.20, 0.28, 0.45, 0.50, 0.48, 0.42, 0.22, 0.10]

        idx = compute_narrowband_indices(wls, r)
        # NDRE = (0.50 - 0.28) / (0.50 + 0.28) = 0.22 / 0.78 = 0.282
        assert pytest.approx(idx.ndre, abs=0.005) == 0.282
        # PRI = (0.08 - 0.12) / (0.08 + 0.12) = -0.04 / 0.20 = -0.200
        assert pytest.approx(idx.pri, abs=0.005) == -0.200
        # WBI = 0.48 / 0.42 = 1.143
        assert pytest.approx(idx.wbi, abs=0.005) == 1.143
        # NDTI = (0.22 - 0.10) / (0.22 + 0.10) = 0.12 / 0.32 = 0.375
        assert pytest.approx(idx.ndti, abs=0.005) == 0.375

    def test_index_masking_detection(self):
        # PRI and NDRE use clean bands
        assert INDEX_REGISTRY["ndre"].is_masked() is False
        assert INDEX_REGISTRY["pri"].is_masked() is False

        # If a custom window overlaps
        overlap_window = [(715.0, 725.0)]
        assert INDEX_REGISTRY["ndre"].is_masked(overlap_window) is True
        assert len(INDEX_REGISTRY["ndre"].get_masked_bands(overlap_window)) == 1

    def test_cube_indices(self):
        wls = np.linspace(400.0, 2400.0, 200)
        cube = np.random.uniform(0.1, 0.6, (5, 5, 200))
        maps = compute_cube_indices(wls, cube)
        for key in ["ndre", "pri", "wbi", "ndti", "mtci", "ndvi", "cai"]:
            assert key in maps
            assert maps[key].shape == (5, 5)
            assert not np.isnan(maps[key]).any()


class TestContinuumRemoval:
    def test_upper_convex_hull_properties(self):
        wls = np.array([500.0, 550.0, 600.0, 680.0, 750.0, 850.0])
        r = np.array([0.10, 0.20, 0.15, 0.05, 0.50, 0.52])

        hull, cr = compute_upper_convex_hull_1d(wls, r)
        assert len(hull) == len(wls)
        assert len(cr) == len(wls)

        # Baseline must be strictly >= reflectance everywhere
        for i in range(len(wls)):
            assert hull[i] >= r[i] - 1e-6
            assert 0.0 <= cr[i] <= 1.0 + 1e-6

        # Deep dip at 680 nm (r=0.05 vs baseline ~0.395)
        res = compute_continuum_diagnostics(wls, r)
        assert res.diagnostics.chlorophyll_depth_680nm > 0.5
        assert res.diagnostics.chlorophyll_auc > 0.0

    def test_dual_mode_local_vs_hull(self):
        wls = np.linspace(400.0, 2400.0, 425)
        r = np.sin(np.linspace(0.1, 3.0, 425)) * 0.4 + 0.1
        res_hull = compute_continuum_diagnostics(wls, r, mode="hull")
        res_local = compute_continuum_diagnostics(wls, r, mode="local")
        assert res_hull.diagnostics.chlorophyll_depth_680nm >= 0.0
        assert res_local.diagnostics.chlorophyll_depth_680nm >= 0.0

    def test_compute_local_feature_depth_cube(self):
        wls = np.linspace(400.0, 2400.0, 100)
        cube = np.random.uniform(0.1, 0.5, (3, 4, 100))
        depth_map = compute_local_feature_depth(wls, cube, (550.0, 600.0), 680.0, (740.0, 780.0))
        assert depth_map.shape == (3, 4)
        assert np.all(depth_map >= 0.0)

    def test_cube_continuum_diagnostics(self):
        wls = np.linspace(500.0, 2400.0, 100)
        cube = np.random.uniform(0.1, 0.5, (3, 3, 100))
        maps = compute_cube_continuum_diagnostics(wls, cube)
        assert "chlorophyll_depth_680nm" in maps
        assert maps["chlorophyll_depth_680nm"].shape == (3, 3)
        assert "red_edge_inflection_nm" in maps
        assert np.all(maps["red_edge_inflection_nm"] >= 700.0)


class TestLinearSpectralUnmixing:
    def test_simplex_projection_1d(self):
        test_vectors = [
            np.array([0.8, 0.4, 0.1]),
            np.array([-0.5, 1.2, 0.3, 0.0]),
            np.array([10.0, 5.0, 0.0]),
            np.array([0.2, 0.2, 0.2, 0.2, 0.2]),
        ]
        for v in test_vectors:
            proj = project_onto_simplex_1d(v)
            assert pytest.approx(float(np.sum(proj)), abs=1e-5) == 1.0
            assert np.all(proj >= -1e-7)

    def test_simplex_projection_batch(self):
        V = np.random.randn(20, 5)
        proj_batch = project_onto_simplex_batch(V)
        assert proj_batch.shape == (20, 5)
        assert np.allclose(np.sum(proj_batch, axis=1), 1.0, atol=1e-5)
        assert np.all(proj_batch >= -1e-7)

        # Verify batch agrees with 1D
        for i in range(20):
            proj_1d = project_onto_simplex_1d(V[i])
            assert np.allclose(proj_batch[i], proj_1d, atol=1e-5)

    def test_fcls_synthetic_recovery(self):
        bands = 60
        em1 = np.linspace(0.05, 0.55, bands)
        em2 = np.linspace(0.40, 0.10, bands)
        em3 = np.sin(np.linspace(0.1, 1.5, bands))
        E = np.column_stack([em1, em2, em3])

        # 60% em1 + 30% em2 + 10% em3
        true_alpha = np.array([0.60, 0.30, 0.10])
        mixed = E @ true_alpha

        # Test PGD solver
        alpha_pgd, rmse_pgd = solve_fcls_pgd(mixed, E)
        assert pytest.approx(float(np.sum(alpha_pgd)), abs=1e-4) == 1.0
        assert np.all(alpha_pgd >= 0.0)
        assert np.allclose(alpha_pgd, true_alpha, atol=0.01)
        assert rmse_pgd < 0.001

        # Test SciPy solver (SLSQP)
        alpha_scipy, rmse_scipy = solve_fcls_scipy(mixed, E)
        assert pytest.approx(float(np.sum(alpha_scipy)), abs=1e-4) == 1.0
        assert np.all(alpha_scipy >= 0.0)
        assert np.allclose(alpha_scipy, true_alpha, atol=0.01)
        assert rmse_scipy < 0.001

        # Test SciPy solver (Augmented NNLS)
        alpha_nnls, rmse_nnls = solve_fcls_nnls_augmented(mixed, E)
        assert pytest.approx(float(np.sum(alpha_nnls)), abs=1e-3) == 1.0
        assert np.all(alpha_nnls >= 0.0)
        assert np.allclose(alpha_nnls, true_alpha, atol=0.02)
        assert rmse_nnls < 0.01

        # Solvers must agree closely
        assert np.allclose(alpha_pgd, alpha_scipy, atol=0.005)

    def test_fcls_empty_batch(self):
        E = np.random.uniform(0.1, 0.5, (10, 3))
        A_empty, rmses_empty = solve_fcls_batch_pgd(np.empty((0, 10)), E)
        assert A_empty.shape == (0, 3)
        assert rmses_empty.shape == (0,)

    def test_cube_unmixing(self):
        bands = 30
        em1 = np.linspace(0.1, 0.6, bands)
        em2 = np.linspace(0.5, 0.2, bands)
        endmembers = {"canopy": em1, "soil": em2}

        # 4x4 spatial grid
        cube = np.zeros((4, 4, bands))
        # Top half 80% canopy + 20% soil; bottom half 20% canopy + 80% soil
        cube[:2, :] = 0.8 * em1 + 0.2 * em2
        cube[2:, :] = 0.2 * em1 + 0.8 * em2

        abundances, rmse_map, keys = compute_cube_unmixing(cube, endmembers)
        assert abundances.shape == (4, 4, 2)
        assert rmse_map.shape == (4, 4)

        # Physical acceptance: sum == 1 everywhere
        sum_map = np.sum(abundances, axis=-1)
        assert np.allclose(sum_map, 1.0, atol=1e-3)
        assert np.all(abundances >= 0.0)

        # Check top half vs bottom half
        assert np.allclose(abundances[:2, :, 0], 0.8, atol=0.02)
        assert np.allclose(abundances[2:, :, 0], 0.2, atol=0.02)


class TestSpectralAngleMapper:
    def test_sam_identical_and_orthogonal(self):
        s1 = [0.1, 0.2, 0.4, 0.5, 0.3]
        s_identical = [0.1, 0.2, 0.4, 0.5, 0.3]
        assert pytest.approx(compute_spectral_angle(s1, s_identical), abs=1e-6) == 0.0

        # Orthogonal signatures
        s_ortho1 = [1.0, 0.0, 0.0]
        s_ortho2 = [0.0, 1.0, 0.0]
        assert pytest.approx(compute_spectral_angle(s_ortho1, s_ortho2), abs=1e-6) == np.pi / 2

    def test_sam_classification_ranking(self):
        spec = [0.1, 0.2, 0.4, 0.5, 0.3]
        refs = [
            {"id": "mat1", "label": "Material 1", "reflectance": [0.1, 0.2, 0.4, 0.5, 0.3]},
            {"id": "mat2", "label": "Material 2", "reflectance": [0.5, 0.4, 0.2, 0.1, 0.1]},
        ]
        res = compute_sam_classification(spec, refs)
        assert res.top_match == "Material 1"
        assert res.spectral_angle_rad == 0.0
        assert res.confidence_pct == 100.0
        assert len(res.candidates) == 2
        assert res.candidates[0].id == "mat1"

    def test_sam_magnitude_blindness(self):
        # Academic proof: SAM is invariant to brightness scaling
        angle = evaluate_sam_magnitude_blindness()
        assert pytest.approx(angle, abs=1e-6) == 0.0

    def test_sam_zero_norm_vector(self):
        s1 = np.zeros(10)
        s2 = np.ones(10)
        angle = compute_spectral_angle(s1, s2)
        assert pytest.approx(angle, abs=1e-5) == np.pi / 2

        refs = [{"id": "mat", "label": "Material", "reflectance": s2}]
        res = compute_sam_classification(s1, refs)
        assert pytest.approx(res.spectral_angle_rad, abs=1e-3) == round(np.pi / 2, 4)
        assert res.confidence_pct == 0.0


class TestEndmemberVCA:
    def test_vca_empty_input_validation(self):
        with pytest.raises(ValueError, match="0 pixels"):
            vertex_component_analysis(np.empty((0, 20)), n_endmembers=3)

    def test_vca_simplex_extraction(self):
        bands = 20
        e1 = np.zeros(bands); e1[0] = 1.0
        e2 = np.zeros(bands); e2[5] = 1.0
        e3 = np.zeros(bands); e3[10] = 1.0

        # Create mixture data
        N = 100
        weights = np.random.dirichlet((1, 1, 1), size=N)
        data = weights @ np.array([e1, e2, e3])
        # Add the pure vertices into the data
        data = np.vstack([e1, e2, e3, data])

        extracted, indices = vertex_component_analysis(data, n_endmembers=3, seed=42)
        assert extracted.shape == (3, bands)
        assert len(indices) == 3

    def test_reference_library_loading(self):
        lib = load_reference_library()
        assert len(lib) >= 5
        em_ids = [ref["id"] for ref in lib]
        assert "green_healthy_canopy" in em_ids
        assert "black_cotton_soil" in em_ids
        assert "dry_crop_residue" in em_ids


class TestHyperspectralDiagnosticEngine:
    @pytest.fixture
    def engine(self):
        return HyperspectralDiagnosticEngine()

    def test_analyze_pixel_schema_parity(self, engine):
        wls = np.linspace(380.0, 2510.0, 425)
        spec = np.clip(0.05 + 0.35 / (1.0 + np.exp(-(wls - 720) / 15)), 0.0, 1.0)

        payload = engine.analyze_pixel(
            wavelengths=wls,
            reflectance=spec,
            sensor_name="AVIRIS-NG India",
            latitude=21.1458,
            longitude=79.0882,
            agro_ecological_zone="Deccan Plateau (Rainfed Cotton-Soybean)",
            flightline_id="vidarbha_wardha_cotton",
            flightline_name="Vidarbha Wardha Cotton Corridor"
        )

        d = payload.to_dict()

        # Strict Section 3 schema keys check
        assert set(d.keys()) == {
            "sensor", "coordinates", "spectral_curve", "narrowband_indices",
            "continuum_diagnostics", "subpixel_abundances", "sam_classification"
        }

        # Sensor schema
        assert d["sensor"]["name"] == "AVIRIS-NG India"
        assert d["sensor"]["total_bands"] == 425
        assert d["sensor"]["valid_bands_used"] > 350
        assert len(d["sensor"]["wavelength_range_nm"]) == 2

        # Coordinates schema
        assert d["coordinates"]["latitude"] == 21.1458
        assert d["coordinates"]["longitude"] == 79.0882
        assert d["coordinates"]["flightline_id"] == "vidarbha_wardha_cotton"

        # Narrowband indices
        for idx_key in ["ndre", "pri", "wbi", "ndti", "mtci"]:
            assert idx_key in d["narrowband_indices"]
            assert isinstance(d["narrowband_indices"][idx_key], float)

        # Continuum diagnostics
        for diag_key in ["chlorophyll_depth_680nm", "chlorophyll_auc", "red_edge_inflection_nm",
                         "red_edge_shift_nm", "cellulose_depth_2100nm", "clay_hydroxyl_depth_2200nm", "water_depth_970nm"]:
            assert diag_key in d["continuum_diagnostics"]
            assert isinstance(d["continuum_diagnostics"][diag_key], float)

        # Subpixel abundances physical validity
        abundances = d["subpixel_abundances"]
        sum_frac = (
            abundances["healthy_crop_fraction"] +
            abundances["stressed_crop_fraction"] +
            abundances["exposed_soil_fraction"] +
            abundances["dry_residue_fraction"] +
            abundances["standing_water_fraction"]
        )
        assert pytest.approx(sum_frac, abs=0.002) == 1.0
        for f_name, f_val in abundances.items():
            if f_name != "reconstruction_rmse":
                assert f_val >= 0.0

        # SAM classification
        assert d["sam_classification"]["top_match"] != ""
        assert d["sam_classification"]["confidence_pct"] >= 0.0
        assert len(d["sam_classification"]["candidates"]) > 0

    def test_seed_flightline_vidarbha_cotton(self, engine):
        path = "platform/data_seed/flightlines/vidarbha_wardha_cotton.json"
        assert os.path.exists(path)
        with open(path, "r", encoding="utf-8") as f:
            fl = json.load(f)

        assert fl["total_bands"] == 425
        p0 = fl["pixels"][0]
        payload = engine.analyze_pixel(
            wavelengths=fl["wavelengths"],
            reflectance=p0["reflectance"],
            sensor_name=fl["sensor"],
            flightline_id=fl["id"]
        )

        d = payload.to_dict()
        assert d["sensor"]["total_bands"] == 425
        assert d["sam_classification"]["top_match"] != ""
        assert d["subpixel_abundances"]["healthy_crop_fraction"] > 0.0

    def test_seed_flightline_punjab_residue(self, engine):
        # NASA EMIT sensor (285 bands)
        path = "platform/data_seed/flightlines/punjab_ludhiana_residue.json"
        assert os.path.exists(path)
        with open(path, "r", encoding="utf-8") as f:
            fl = json.load(f)

        assert fl["total_bands"] == 285
        p0 = fl["pixels"][0]
        payload = engine.analyze_pixel(
            wavelengths=fl["wavelengths"],
            reflectance=p0["reflectance"],
            sensor_name=fl["sensor"],
            flightline_id=fl["id"]
        )

        d = payload.to_dict()
        assert d["sensor"]["total_bands"] == 285
        assert d["spectral_curve"]["reference_curves"]["residue"] is not None
        assert len(d["spectral_curve"]["reference_curves"]["residue"]) == 285
        # Residue fraction must be prominent in Ludhiana stubble burning corridor
        assert d["subpixel_abundances"]["dry_residue_fraction"] > 0.20

    def test_seed_flightline_godavari_wetland(self, engine):
        path = "platform/data_seed/flightlines/godavari_delta_wetland.json"
        assert os.path.exists(path)
        with open(path, "r", encoding="utf-8") as f:
            fl = json.load(f)

        p0 = fl["pixels"][0]
        payload = engine.analyze_pixel(
            wavelengths=fl["wavelengths"],
            reflectance=p0["reflectance"],
            sensor_name=fl["sensor"],
            flightline_id=fl["id"]
        )
        d = payload.to_dict()
        assert d["subpixel_abundances"]["standing_water_fraction"] > 0.10

    def test_single_pixel_latency_benchmark(self, engine):
        """
        Acceptance Criteria #3: Single-pixel evaluation completes in < 5.0 ms.
        """
        path = "platform/data_seed/flightlines/vidarbha_wardha_cotton.json"
        with open(path, "r", encoding="utf-8") as f:
            fl = json.load(f)

        wavelengths = fl["wavelengths"]
        pixels = fl["pixels"][:100]

        # Warm-up call
        engine.analyze_pixel(wavelengths, pixels[0]["reflectance"])

        start_time = time.perf_counter()
        for p in pixels:
            _ = engine.analyze_pixel(wavelengths, p["reflectance"])
        total_time = time.perf_counter() - start_time

        avg_latency_ms = (total_time / len(pixels)) * 1000.0
        print(f"\n[LATENCY BENCHMARK] Average latency over {len(pixels)} pixels: {avg_latency_ms:.2f} ms/pixel")
        assert avg_latency_ms < 5.0, f"Single-pixel latency ({avg_latency_ms:.2f} ms) exceeded 5.0 ms threshold!"

    def test_analyze_pixel_nan_resilience_and_valid_json(self, engine):
        wls = np.linspace(380.0, 2510.0, 425)
        spec = np.full(425, 0.3)
        spec[10] = np.nan
        spec[20] = np.inf
        spec[30] = -np.inf

        payload = engine.analyze_pixel(wls, spec)
        json_str = payload.to_json()
        assert "NaN" not in json_str
        assert "Infinity" not in json_str

        # Strict RFC 8259 JSON deserialization
        parsed = json.loads(json_str)
        assert parsed["subpixel_abundances"]["reconstruction_rmse"] >= 0.0
        assert parsed["sam_classification"]["spectral_angle_rad"] >= 0.0
        assert parsed["spectral_curve"]["reflectance"][10] == 0.0
        assert parsed["spectral_curve"]["reflectance"][20] == 1.0

    def test_cube_analysis_and_tiff_export(self, engine, tmp_path):
        wls = np.linspace(400.0, 2400.0, 50)
        cube = np.random.uniform(0.1, 0.6, (4, 4, 50))
        out_tif = str(tmp_path / "test_cube.tif")

        bundle = engine.analyze_cube(wls, cube, output_file=out_tif)
        assert "indices" in bundle
        assert "abundances" in bundle
        assert os.path.exists(out_tif)
        assert os.path.getsize(out_tif) > 0
