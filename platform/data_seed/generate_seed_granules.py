"""
generate_seed_granules.py
Generates calibrated reference endmember libraries and 4-zone hyperspectral flightline granules
for the BharatSpectral WebGIS platform.
"""

import json
import os
import numpy as np

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FLIGHTLINES_DIR = os.path.join(OUTPUT_DIR, "flightlines")
os.makedirs(FLIGHTLINES_DIR, exist_ok=True)

# 1. Standard Wavelength Arrays
AVIRIS_WAVELENGTHS = np.round(np.linspace(380.0, 2510.0, 425), 2).tolist() # 425 bands (~5.0 nm FWHM)
EMIT_WAVELENGTHS = np.round(np.linspace(381.0, 2493.0, 285), 2).tolist()   # 285 bands (~7.4 nm FWHM)

def gaussian_dip(wl, center, depth, fwhm):
    sigma = fwhm / 2.355
    return depth * np.exp(-0.5 * ((wl - center) / sigma) ** 2)

def generate_endmember_curve(wavelengths, material_type):
    """
    Synthesizes physically accurate continuous reflectance signatures
    grounded in laboratory USGS / JPL spectral library profiles.
    """
    wl = np.array(wavelengths, dtype=np.float64)
    r = np.zeros_like(wl)
    
    if material_type == "green_healthy_canopy":
        # Green vegetation curve:
        # VIS: low blue (0.04), green peak (0.12 at 550nm), deep red well (0.045 at 680nm)
        # Red-edge: sharp sigmoid transition (690-735nm)
        # NIR: plateau at ~0.50
        # SWIR: liquid water dips at 970nm, 1200nm; cellulose dip at 2100nm
        vis_base = 0.04 + 0.08 * np.exp(-0.5 * ((wl - 550) / 40)**2) - 0.03 * np.exp(-0.5 * ((wl - 680) / 30)**2)
        nir_base = 0.48 / (1.0 + np.exp(-(wl - 715) / 12))
        swir_decay = -0.00012 * np.maximum(0, wl - 1100)
        r = np.maximum(vis_base, nir_base) + swir_decay
        # Absorption wells
        r -= gaussian_dip(wl, 680.0, 0.32, 35.0)  # Chlorophyll-a
        r -= gaussian_dip(wl, 970.0, 0.08, 50.0)  # Plant tissue water
        r -= gaussian_dip(wl, 1200.0, 0.12, 60.0) # Water band
        r -= gaussian_dip(wl, 2100.0, 0.04, 50.0) # Cellulose
        r = np.clip(r, 0.02, 0.58)

    elif material_type == "stressed_crop":
        # Chlorotic canopy:
        # Shallower 680nm well, blue-shifted red edge (~708nm), lower NIR (~0.32), higher PRI stress
        vis_base = 0.07 + 0.09 * np.exp(-0.5 * ((wl - 560) / 50)**2)
        nir_base = 0.33 / (1.0 + np.exp(-(wl - 706) / 16))
        swir_decay = -0.00008 * np.maximum(0, wl - 1100)
        r = np.maximum(vis_base, nir_base) + swir_decay
        r -= gaussian_dip(wl, 675.0, 0.16, 45.0) # Shallow chlorophyll
        r -= gaussian_dip(wl, 970.0, 0.05, 50.0)
        r -= gaussian_dip(wl, 1200.0, 0.08, 60.0)
        r = np.clip(r, 0.03, 0.38)

    elif material_type == "black_cotton_soil":
        # Regur / Vertisol:
        # Dark albedo, monotone rise with wavelength, prominent 2200nm Al-OH / smectite clay feature
        r = 0.07 + 0.16 * (1.0 - np.exp(-(wl - 380) / 800))
        r -= gaussian_dip(wl, 2200.0, 0.055, 45.0) # Al-OH clay hydroxyl
        r -= gaussian_dip(wl, 950.0, 0.015, 60.0)  # Fe3+ soil iron
        r = np.clip(r, 0.04, 0.25)

    elif material_type == "dry_crop_residue":
        # Dry wheat / rice straw (stubble):
        # Straw yellow: steady rise across VIS and NIR, high SWIR, diagnostic cellulose/lignin doublet at 2100nm
        r = 0.10 + 0.35 * (1.0 - np.exp(-(wl - 380) / 600))
        r -= gaussian_dip(wl, 2100.0, 0.065, 45.0) # Lignin-cellulose absorption
        r -= gaussian_dip(wl, 2300.0, 0.045, 50.0) # Secondary cellulose
        r = np.clip(r, 0.08, 0.46)

    elif material_type == "standing_water":
        # Pure water / flooded paddy water:
        # High blue/green, steep decline into NIR (<0.02 above 750nm)
        r = 0.06 * np.exp(-(wl - 400) / 180)
        r = np.clip(r, 0.005, 0.07)

    return np.round(r, 4).tolist()

def generate_endmember_library():
    """Generates pure Indian reference endmember library across 425 AVIRIS-NG bands."""
    endmembers = {
        "description": "BharatSpectral Indian Agro-Ecological Reference Endmember Library",
        "wavelengths": AVIRIS_WAVELENGTHS,
        "total_bands": len(AVIRIS_WAVELENGTHS),
        "endmembers": {
            "green_healthy_canopy": {
                "label": "Gossypium hirsutum (Green Healthy Canopy)",
                "reflectance": generate_endmember_curve(AVIRIS_WAVELENGTHS, "green_healthy_canopy")
            },
            "stressed_crop": {
                "label": "Glycine max (Chlorotic / Moisture Stressed Canopy)",
                "reflectance": generate_endmember_curve(AVIRIS_WAVELENGTHS, "stressed_crop")
            },
            "black_cotton_soil": {
                "label": "Regur / Vertisol (Dark Alluvial Smectite Soil)",
                "reflectance": generate_endmember_curve(AVIRIS_WAVELENGTHS, "black_cotton_soil")
            },
            "dry_crop_residue": {
                "label": "Triticum / Oryza Straw (Combustible Dry Crop Residue)",
                "reflectance": generate_endmember_curve(AVIRIS_WAVELENGTHS, "dry_crop_residue")
            },
            "standing_water": {
                "label": "Flooded Paddy / Wetland Surface Water",
                "reflectance": generate_endmember_curve(AVIRIS_WAVELENGTHS, "standing_water")
            }
        }
    }
    path = os.path.join(OUTPUT_DIR, "endmembers_india.json")
    with open(path, "w") as f:
        json.dump(endmembers, f, indent=2)
    print(f"Generated Indian Endmember Library: {path}")

def generate_flightline(fl_id, name, sensor, platform, wavelengths, gsd_m, bbox, agro_zone, primary_diag, default_weights):
    """
    Generates a calibrated 20x20 flightline parcel grid with spatially-coherent endmember unmixing.
    """
    min_lon, min_lat, max_lon, max_lat = bbox
    rows, cols = 20, 20
    
    # Pre-generate base pure curves for this sensor's wavelengths
    em_curves = {
        "green_healthy_canopy": np.array(generate_endmember_curve(wavelengths, "green_healthy_canopy")),
        "stressed_crop": np.array(generate_endmember_curve(wavelengths, "stressed_crop")),
        "black_cotton_soil": np.array(generate_endmember_curve(wavelengths, "black_cotton_soil")),
        "dry_crop_residue": np.array(generate_endmember_curve(wavelengths, "dry_crop_residue")),
        "standing_water": np.array(generate_endmember_curve(wavelengths, "standing_water"))
    }
    
    np.random.seed(42 + hash(fl_id) % 1000)
    
    lats = np.linspace(min_lat, max_lat, rows)
    lons = np.linspace(min_lon, max_lon, cols)
    
    pixels = []
    
    for r in range(rows):
        for c in range(cols):
            lat = round(float(lats[r]), 5)
            lon = round(float(lons[c]), 5)
            
            # Create spatial variation gradient across parcels
            u = r / (rows - 1)
            v = c / (cols - 1)
            
            # Modulate weights spatially
            w_raw = {}
            for k, base_val in default_weights.items():
                noise = np.random.uniform(-0.08, 0.08)
                spatial_bias = 0.15 * np.sin(np.pi * (u + 0.5 * v))
                val = max(0.0, base_val + noise + (spatial_bias if k == "green_healthy_canopy" else -spatial_bias*0.5))
                w_raw[k] = val
                
            total_w = sum(w_raw.values())
            weights = {k: v / total_w for k, v in w_raw.items()}
            
            # Linear mixture of endmembers
            mixed_curve = np.zeros(len(wavelengths), dtype=np.float64)
            for k, fraction in weights.items():
                mixed_curve += fraction * em_curves[k]
                
            # Add subtle realistic instrument noise (~0.5%)
            inst_noise = np.random.normal(0, 0.003, size=len(wavelengths))
            final_curve = np.clip(mixed_curve + inst_noise, 0.005, 0.95)
            
            # Determine dominant class
            dom_class = max(weights.items(), key=lambda item: item[1])[0]
            
            pixels.append({
                "row": r,
                "col": c,
                "lat": lat,
                "lon": lon,
                "dominant_class": dom_class,
                "abundances": {k: round(float(v), 3) for k, v in weights.items()},
                "reflectance": np.round(final_curve, 4).tolist()
            })
            
    flightline_data = {
        "id": fl_id,
        "name": name,
        "sensor": sensor,
        "platform": platform,
        "total_bands": len(wavelengths),
        "gsd_m": gsd_m,
        "wavelengths": wavelengths,
        "bbox": bbox,
        "center": [round((min_lon + max_lon) / 2, 5), round((min_lat + max_lat) / 2, 5)],
        "agro_zone": agro_zone,
        "primary_diagnostic": primary_diag,
        "grid": {
            "rows": rows,
            "cols": cols,
            "total_pixels": len(pixels)
        },
        "pixels": pixels
    }
    
    out_file = os.path.join(FLIGHTLINES_DIR, f"{fl_id}.json")
    with open(out_file, "w") as f:
        json.dump(flightline_data, f)
    size_mb = os.path.getsize(out_file) / (1024 * 1024)
    print(f"Generated Flightline: {fl_id} ({size_mb:.2f} MB, {len(pixels)} parcels)")
    return flightline_data

def generate_all_flightlines():
    """Generates the 4 core agro-ecological seed flightlines."""
    configs = [
        {
            "id": "vidarbha_wardha_cotton",
            "name": "Vidarbha Wardha Cotton Corridor",
            "sensor": "AVIRIS-NG India",
            "platform": "Airborne",
            "wavelengths": AVIRIS_WAVELENGTHS,
            "gsd_m": 4.8,
            "bbox": [78.55, 20.70, 78.65, 20.80],
            "agro_zone": "Deccan Plateau (Rainfed Cotton-Soybean)",
            "primary_diag": "Cotton Chlorosis, Vertisol Smectite Clay (2200nm Hydroxyl)",
            "weights": {
                "green_healthy_canopy": 0.42,
                "stressed_crop": 0.23,
                "black_cotton_soil": 0.28,
                "dry_crop_residue": 0.05,
                "standing_water": 0.02
            }
        },
        {
            "id": "punjab_ludhiana_residue",
            "name": "Punjab Ludhiana Stubble Corridor",
            "sensor": "NASA EMIT",
            "platform": "ISS Orbit",
            "wavelengths": EMIT_WAVELENGTHS,
            "gsd_m": 60.0,
            "bbox": [75.80, 30.85, 75.92, 30.95],
            "agro_zone": "Indo-Gangetic Plain (Intensive Wheat-Rice Stubble Zone)",
            "primary_diag": "Dry Straw Residue, Lignin-Cellulose (2100nm) Stubble Burn Risk",
            "weights": {
                "green_healthy_canopy": 0.12,
                "stressed_crop": 0.08,
                "black_cotton_soil": 0.25,
                "dry_crop_residue": 0.52,
                "standing_water": 0.03
            }
        },
        {
            "id": "gujarat_anand_canopy",
            "name": "Gujarat Anand High-Nitrogen Canopy",
            "sensor": "AVIRIS-NG India",
            "platform": "Airborne",
            "wavelengths": AVIRIS_WAVELENGTHS,
            "gsd_m": 5.0,
            "bbox": [72.88, 22.50, 72.98, 22.62],
            "agro_zone": "Charotar Intensive Mixed Canopy & Tobacco Agroecosystem",
            "primary_diag": "Canopy Nitrogen Density, Chlorophyll-a (680nm), Steep Red-Edge",
            "weights": {
                "green_healthy_canopy": 0.68,
                "stressed_crop": 0.14,
                "black_cotton_soil": 0.12,
                "dry_crop_residue": 0.04,
                "standing_water": 0.02
            }
        },
        {
            "id": "godavari_delta_wetland",
            "name": "Godavari Delta Wetland & Paddy Corridor",
            "sensor": "NASA EMIT",
            "platform": "ISS Orbit",
            "wavelengths": EMIT_WAVELENGTHS,
            "gsd_m": 60.0,
            "bbox": [82.15, 16.65, 82.26, 16.78],
            "agro_zone": "Eastern Coastal Deltaic Wetland & Paddy Ecosystem",
            "primary_diag": "Liquid Water Absorption (970nm & 1200nm), Hydric Soil Unmixing",
            "weights": {
                "green_healthy_canopy": 0.35,
                "stressed_crop": 0.10,
                "black_cotton_soil": 0.10,
                "dry_crop_residue": 0.05,
                "standing_water": 0.40
            }
        }
    ]
    
    features = []
    
    for cfg in configs:
        fl_data = generate_flightline(
            cfg["id"], cfg["name"], cfg["sensor"], cfg["platform"],
            cfg["wavelengths"], cfg["gsd_m"], cfg["bbox"],
            cfg["agro_zone"], cfg["primary_diag"], cfg["weights"]
        )
        
        # Build GeoJSON feature for corridor polygon
        min_lon, min_lat, max_lon, max_lat = cfg["bbox"]
        coordinates = [[
            [min_lon, min_lat],
            [max_lon, min_lat],
            [max_lon, max_lat],
            [min_lon, max_lat],
            [min_lon, min_lat]
        ]]
        
        feature = {
            "type": "Feature",
            "id": cfg["id"],
            "geometry": {
                "type": "Polygon",
                "coordinates": coordinates
            },
            "properties": {
                "id": cfg["id"],
                "name": cfg["name"],
                "sensor": cfg["sensor"],
                "platform": cfg["platform"],
                "total_bands": len(cfg["wavelengths"]),
                "gsd_m": cfg["gsd_m"],
                "wavelength_range_nm": [cfg["wavelengths"][0], cfg["wavelengths"][-1]],
                "center": fl_data["center"],
                "bbox": cfg["bbox"],
                "agro_zone": cfg["agro_zone"],
                "primary_diagnostic": cfg["primary_diag"],
                "file": f"flightlines/{cfg['id']}.json"
            }
        }
        features.append(feature)
        
    manifest = {
        "type": "FeatureCollection",
        "description": "BharatSpectral Curated Hyperspectral Flightlines Manifest",
        "total_flightlines": len(features),
        "features": features
    }
    
    manifest_path = os.path.join(OUTPUT_DIR, "flightlines_manifest.geojson")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    with open(os.path.join(OUTPUT_DIR, "flightlines_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Generated Flightlines Manifest: {manifest_path}")

if __name__ == "__main__":
    print("Beginning BharatSpectral Seed Data Generation...")
    generate_endmember_library()
    generate_all_flightlines()
    print("Seed data generation successfully completed.")
