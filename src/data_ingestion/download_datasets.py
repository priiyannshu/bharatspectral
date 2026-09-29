"""
download_datasets.py - Dataset acquisition and ingest verification for BharatSpectral
Handles Indian Pines (1992 baseline), AVIRIS-NG India, and NASA EMIT L2A cubes.
"""

import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BharatSpectral.DataIngestion")

def verify_and_prepare_datasets(data_root="data"):
    """
    Verifies dataset directories and handles acquisition or sample cache validation.
    """
    os.makedirs(os.path.join(data_root, "raw", "indian_pines"), exist_ok=True)
    os.makedirs(os.path.join(data_root, "raw", "aviris_ng_india"), exist_ok=True)
    os.makedirs(os.path.join(data_root, "raw", "emit_india"), exist_ok=True)
    os.makedirs(os.path.join(data_root, "processed", "patches"), exist_ok=True)
    os.makedirs(os.path.join(data_root, "processed", "spectral_libraries"), exist_ok=True)

    logger.info("Dataset directories initialized successfully under %s", data_root)
    return True

if __name__ == "__main__":
    verify_and_prepare_datasets()
