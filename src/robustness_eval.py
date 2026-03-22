"""
Robustness evaluation via synthetic perturbations on feature vectors.
Tests sensitivity to Gaussian noise and feature dropout.
"""
from pathlib import Path
import json
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

from src.preprocess import build_dataset_from_folder


def eval_under_perturbation(clf, X, y, noise_std=0.0, dropout_rate=0.0, seed=42):
    rng = np.random.default_rng(seed)
    Xp = X.copy()

    if noise_std > 0:
        Xp += rng.normal(0, noise_std, size=Xp.shape)

    if dropout_rate > 0:
        mask = rng.random(Xp.shape) < dropout_rate
        Xp[mask] = 0.0

    pred = clf.predict(Xp)
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "f1": float(f1_score(y, pred)),
    }


def main(model_path='outputs/model_rf_real.joblib'):
    X0, y0 = build_dataset_from_folder('data/relaxed', label=0)
    X1, y1 = build_dataset_from_folder('data/focused', label=1)
    X = np.vstack([X0, X1])
    y = np.concatenate([y0, y1])

    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Path(model_path)
    if not model.exists():
        raise FileNotFoundError(f'Model missing: {model}')
    clf = joblib.load(model)

    settings = [
        {"name": "clean", "noise_std": 0.0, "dropout_rate": 0.0},
        {"name": "noise_0.05", "noise_std": 0.05, "dropout_rate": 0.0},
        {"name": "noise_0.10", "noise_std": 0.10, "dropout_rate": 0.0},
        {"name": "dropout_0.05", "noise_std": 0.0, "dropout_rate": 0.05},
        {"name": "dropout_0.10", "noise_std": 0.0, "dropout_rate": 0.10},
        {"name": "mixed", "noise_std": 0.05, "dropout_rate": 0.05},
    ]

    rows = []
    for s in settings:
        m = eval_under_perturbation(
            clf, X_test, y_test,
            noise_std=s['noise_std'],
            dropout_rate=s['dropout_rate'],
        )
        rows.append({**s, **m})

    out = Path('outputs')
    out.mkdir(exist_ok=True)
    fp = out / 'robustness_results.json'
    fp.write_text(json.dumps(rows, indent=2), encoding='utf-8')
    print(json.dumps(rows, indent=2))
    print(f'Saved {fp}')


if __name__ == '__main__':
    main()
