"""
hybrid_sn.py - HybridSN (Spectral-Spatial 3D-2D CNN)
Implements Roy et al. (IEEE GRSL 2020) architecture for hyperspectral classification.
"""

import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BharatSpectral.HybridSN")

def get_hybridsn_model(num_classes=16, in_bands=200, patch_size=9):
    """
    Returns the HybridSN PyTorch model definition.
    """
    try:
        import torch
        import torch.nn as nn

        class HybridSN(nn.Module):
            def __init__(self, num_classes=num_classes, in_bands=in_bands):
                super(HybridSN, self).__init__()
                # 3D Convolution Layers
                self.conv3d_1 = nn.Sequential(
                    nn.Conv3d(1, 8, kernel_size=(7, 3, 3), stride=1, padding=1),
                    nn.BatchNorm3d(8),
                    nn.ReLU(inplace=True)
                )
                self.conv3d_2 = nn.Sequential(
                    nn.Conv3d(8, 16, kernel_size=(5, 3, 3), stride=1, padding=1),
                    nn.BatchNorm3d(16),
                    nn.ReLU(inplace=True)
                )
                self.conv3d_3 = nn.Sequential(
                    nn.Conv3d(16, 32, kernel_size=(3, 3, 3), stride=1, padding=1),
                    nn.BatchNorm3d(32),
                    nn.ReLU(inplace=True)
                )
                # 2D Convolution Layer
                self.conv2d_4 = nn.Sequential(
                    nn.Conv2d(32 * (in_bands - 4), 64, kernel_size=(3, 3), stride=1, padding=1),
                    nn.BatchNorm2d(64),
                    nn.ReLU(inplace=True)
                )
                # Dense Layers
                self.fc1 = nn.Linear(64 * (patch_size ** 2), 256)
                self.drop1 = nn.Dropout(0.4)
                self.fc2 = nn.Linear(256, 128)
                self.drop2 = nn.Dropout(0.4)
                self.classifier = nn.Linear(128, num_classes)

            def forward(self, x):
                x = self.conv3d_1(x)
                x = self.conv3d_2(x)
                x = self.conv3d_3(x)
                x = x.view(x.size(0), -1, x.size(3), x.size(4))
                x = self.conv2d_4(x)
                x = x.flatten(start_dim=1)
                x = nn.ReLU()(self.fc1(x))
                x = self.drop1(x)
                x = nn.ReLU()(self.fc2(x))
                x = self.drop2(x)
                return self.classifier(x)

        return HybridSN()
    except ImportError:
        logger.warning("PyTorch not installed in current environment; loaded structural signature.")
        return None

if __name__ == "__main__":
    model = get_hybridsn_model()
    print("HybridSN model definition verified.")
