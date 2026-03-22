from pathlib import Path
import numpy as np
import joblib


def predict_state(feature_vector, model_path="outputs/model_rf_real.joblib"):
    model = Path(model_path)
    if not model.exists():
        raise FileNotFoundError("Model not found. Run training first.")

    clf = joblib.load(model)
    x = np.array(feature_vector, dtype=float).reshape(1, -1)
    proba = clf.predict_proba(x)[0]
    pred = int(np.argmax(proba))

    return {
        "label": "focused" if pred == 1 else "relaxed",
        "focused_prob": float(proba[1]),
        "relaxed_prob": float(proba[0]),
    }
