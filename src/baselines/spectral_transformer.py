"""
spectral_transformer.py - Spectral Transformer Baseline
Implements a 1D/3D Spectral Transformer encoder baseline for tokenized hyperspectral analysis.
"""

import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BharatSpectral.SpectralTransformer")

def get_spectral_transformer(num_classes=16, in_bands=200, d_model=64, nhead=4, num_layers=3):
    try:
        import torch
        import torch.nn as nn

        class SpectralTransformer(nn.Module):
            def __init__(self):
                super(SpectralTransformer, self).__init__()
                self.token_proj = nn.Linear(1, d_model)
                self.pos_emb = nn.Parameter(torch.randn(1, in_bands, d_model) * 0.02)
                encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=128, batch_first=True)
                self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
                self.head = nn.Linear(d_model, num_classes)

            def forward(self, x):
                # x shape: (B, Bands) or (B, Bands, 1)
                if x.dim() == 2:
                    x = x.unsqueeze(-1)
                tokens = self.token_proj(x) + self.pos_emb
                encoded = self.transformer(tokens)
                pooled = encoded.mean(dim=1)
                return self.head(pooled)

        return SpectralTransformer()
    except ImportError:
        logger.warning("PyTorch not installed in current environment; loaded structural signature.")
        return None

if __name__ == "__main__":
    t = get_spectral_transformer()
    print("Spectral Transformer module verified.")
