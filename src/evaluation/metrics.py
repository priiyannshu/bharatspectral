"""
metrics.py - Hyperspectral Classification & Unmixing Evaluation Metrics
Computes Overall Accuracy (OA), Average Accuracy (AA), Cohen's Kappa,
and Abundance Root Mean Square Error (RMSE_A).
"""

import math
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BharatSpectral.Metrics")

def compute_overall_accuracy(confusion_matrix):
    total = sum(sum(row) for row in confusion_matrix)
    diag = sum(confusion_matrix[i][i] for i in range(len(confusion_matrix)))
    return (diag / total) * 100.0 if total > 0 else 0.0

def compute_average_accuracy(confusion_matrix):
    recalls = []
    for i, row in enumerate(confusion_matrix):
        row_sum = sum(row)
        if row_sum > 0:
            recalls.append(row[i] / row_sum)
    return (sum(recalls) / len(recalls)) * 100.0 if recalls else 0.0

def compute_cohen_kappa(confusion_matrix):
    total = sum(sum(row) for row in confusion_matrix)
    if total == 0:
        return 0.0
    po = sum(confusion_matrix[i][i] for i in range(len(confusion_matrix))) / total
    pe = sum(sum(row) * sum(col) for row, col in zip(confusion_matrix, zip(*confusion_matrix))) / (total * total)
    return (po - pe) / (1 - pe) if (1 - pe) != 0 else 1.0

def compute_abundance_rmse(ground_truth_abundances, estimated_abundances):
    total_diff_sq = 0.0
    count = 0
    for gt_row, est_row in zip(ground_truth_abundances, estimated_abundances):
        for gt, est in zip(gt_row, est_row):
            total_diff_sq += (gt - est) ** 2
            count += 1
    return math.sqrt(total_diff_sq / count) if count > 0 else 0.0

if __name__ == "__main__":
    cm = [[50, 2], [5, 43]]
    print(f"Sample OA: {compute_overall_accuracy(cm):.2f}% | AA: {compute_average_accuracy(cm):.2f}% | Kappa: {compute_cohen_kappa(cm):.4f}")
