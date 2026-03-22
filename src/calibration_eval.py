"""
Probability calibration evaluation for binary classifier.
Computes Brier score + reliability curve points and saves artifacts.
"""
from pathlib import Path
import json
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import brier_score_loss
from sklearn.calibration import calibration_curve

from src.preprocess import build_dataset_from_folder


def main(model_path='outputs/model_rf_real.joblib', n_bins=10):
    X0, y0 = build_dataset_from_folder('data/relaxed', label=0)
    X1, y1 = build_dataset_from_folder('data/focused', label=1)
    X = np.vstack([X0, X1])
    y = np.concatenate([y0, y1])

    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Path(model_path)
    if not model.exists():
        raise FileNotFoundError(f'Model not found: {model}')

    clf = joblib.load(model)
    proba = clf.predict_proba(X_test)[:, 1]

    brier = float(brier_score_loss(y_test, proba))
    frac_pos, mean_pred = calibration_curve(y_test, proba, n_bins=n_bins, strategy='uniform')

    out = Path('outputs')
    out.mkdir(exist_ok=True)
    data = {
        'brier_score': brier,
        'n_bins': int(n_bins),
        'mean_predicted_value': [float(x) for x in mean_pred],
        'fraction_of_positives': [float(x) for x in frac_pos],
    }
    (out / 'calibration_results.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
