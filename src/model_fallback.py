"""
Model fallback utilities for demo reliability.
If trained model is missing, return deterministic mock probabilities so UI stays usable.
"""
from pathlib import Path
import numpy as np


def has_real_model(path: str = 'outputs/model_rf_real.joblib') -> bool:
    return Path(path).exists()


def mock_predict(feature_vector):
    x = np.array(feature_vector, dtype=float)
    # stable deterministic score from feature mean
    z = float(np.tanh(np.mean(x) / 3.0))
    focused = 0.5 + 0.35 * z
    focused = max(0.01, min(0.99, focused))
    relaxed = 1.0 - focused
    return {
        'label': 'focused' if focused >= 0.5 else 'relaxed',
        'focused_prob': float(focused),
        'relaxed_prob': float(relaxed),
        'mode': 'mock_fallback',
    }
