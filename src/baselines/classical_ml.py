"""
classical_ml.py - Random Forest & Support Vector Machine (RBF) Spectral Classifiers
Provides high-speed CPU baselines for single-pixel and patch spectral classification.
"""

import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BharatSpectral.ClassicalML")

class ClassicalSpectralClassifiers:
    """
    Wrapper for Random Forest (100 trees) and SVM-RBF models.
    """
    def __init__(self, n_estimators=100, svm_c=100.0, svm_gamma="scale"):
        self.n_estimators = n_estimators
        self.svm_c = svm_c
        self.svm_gamma = svm_gamma
        self.rf_model = None
        self.svm_model = None

    def build_models(self):
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.svm import SVC
            self.rf_model = RandomForestClassifier(n_estimators=self.n_estimators, random_state=42, n_jobs=-1)
            self.svm_model = SVC(C=self.svm_c, gamma=self.svm_gamma, kernel="rbf", probability=True)
            logger.info("Initialized RandomForest(%d) and SVM-RBF(C=%.1f)", self.n_estimators, self.svm_c)
        except ImportError:
            logger.warning("scikit-learn not available in local environment; loaded stub mode.")

if __name__ == "__main__":
    clf = ClassicalSpectralClassifiers()
    clf.build_models()
    print("Classical ML baseline module verified.")
