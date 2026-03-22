from pathlib import Path
import numpy as np
import joblib
from src.model_fallback import has_real_model, mock_predict


def predict_state(feature_vector, model_path="outputs/model_rf_real.joblib"):
    model = Path(model_path)
    if not has_real_model(str(model)):
        return mock_predict(feature_vector)

    clf = joblib.load(model)
    x = np.array(feature_vector, dtype=float).reshape(1, -1)
    proba = clf.predict_proba(x)[0]
    pred = int(np.argmax(proba))

    return {
        "label": "focused" if pred == 1 else "relaxed",
        "focused_prob": float(proba[1]),
        "relaxed_prob": float(proba[0]),
        "mode": "real_model",
    }
