"""
Bootstrap confidence intervals for key metrics (accuracy, f1, auc) on test predictions.
"""
from pathlib import Path
import json
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from src.preprocess import build_dataset_from_folder


def ci(arr, alpha=0.95):
    lo = (1 - alpha) / 2
    hi = 1 - lo
    return float(np.quantile(arr, lo)), float(np.quantile(arr, hi))


def main(model_path='outputs/model_rf_real.joblib', n_boot=300, seed=42):
    X0, y0 = build_dataset_from_folder('data/relaxed', label=0)
    X1, y1 = build_dataset_from_folder('data/focused', label=1)
    X = np.vstack([X0, X1])
    y = np.concatenate([y0, y1])

    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    mp = Path(model_path)
    if not mp.exists():
        raise FileNotFoundError(f'Model not found: {mp}')
    clf = joblib.load(mp)

    pred = clf.predict(X_test)
    proba = clf.predict_proba(X_test)[:, 1]

    rng = np.random.default_rng(seed)
    n = len(y_test)
    accs, f1s, aucs = [], [], []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        yt = y_test[idx]
        yp = pred[idx]
        pp = proba[idx]
        accs.append(accuracy_score(yt, yp))
        f1s.append(f1_score(yt, yp))
        try:
            aucs.append(roc_auc_score(yt, pp))
        except Exception:
            pass

    out = {
        'n_bootstrap': int(n_boot),
        'accuracy_mean': float(np.mean(accs)),
        'accuracy_ci95': ci(np.array(accs)),
        'f1_mean': float(np.mean(f1s)),
        'f1_ci95': ci(np.array(f1s)),
        'auc_mean': float(np.mean(aucs)) if aucs else None,
        'auc_ci95': ci(np.array(aucs)) if aucs else None,
    }

    od = Path('outputs'); od.mkdir(exist_ok=True)
    fp = od / 'bootstrap_ci_results.json'
    fp.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out, indent=2))
    print(f'Saved {fp}')


if __name__ == '__main__':
    main()
