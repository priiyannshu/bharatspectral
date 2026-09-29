"""
evaluate_cross_scene.py - Cross-Domain Evaluation Engine
Evaluates zero-shot transfer from Western source domain (Indian Pines)
to Indian agricultural target scenes (AVIRIS-NG / EMIT).
"""

import os
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BharatSpectral.CrossSceneEval")

def load_benchmark_summary(summary_path="outputs/tables/gis_vs_ai_summary.json"):
    """
    Loads empirical cross-domain benchmark results.
    """
    if os.path.exists(summary_path):
        with open(summary_path, "r") as f:
            data = json.load(f)
        logger.info("Successfully loaded benchmark summary from %s", summary_path)
        return data
    else:
        logger.warning("Summary file not found at %s", summary_path)
        return None

def print_evaluation_report(summary_data):
    if not summary_data:
        return
    print("\n" + "=" * 65)
    print("🚀 BHARATSPECTRAL CROSS-DOMAIN BENCHMARK SUMMARY (Pi 5 Grounded)")
    print("=" * 65)
    drops = summary_data.get("cross_domain_drop_summary", {})
    print(f"{'Model':<24} | {'Source OA':<10} | {'Target OA':<10} | {'OA Drop':<10}")
    print("-" * 65)
    for model_name, metrics in drops.items():
        s_oa = f"{metrics.get('source_oa', 0.0):.1f}%"
        t_oa = f"{metrics.get('target_zero_shot_oa', 0.0):.1f}%"
        drop = f"-{metrics.get('abs_drop', 0.0):.1f}%"
        print(f"{model_name:<24} | {s_oa:<10} | {t_oa:<10} | {drop:<10}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    summary = load_benchmark_summary()
    print_evaluation_report(summary)
