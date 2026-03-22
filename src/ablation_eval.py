"""
Feature-group ablation study for EEG bandpower features.
Assumes feature layout: per-channel [delta, theta, alpha, beta] repeated.
"""
from pathlib import Path
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

from src.preprocess import build_dataset_from_folder

BANDS = ['delta', 'theta', 'alpha', 'beta']


def mask_band(X, band_idx):
    X2 = X.copy()
    X2[:, band_idx::4] = 0.0
    return X2


def train_eval(X_train, y_train, X_test, y_test):
    clf = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestClassifier(n_estimators=300, class_weight='balanced', random_state=42, n_jobs=-1)),
    ])
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    return {
        'accuracy': float(accuracy_score(y_test, pred)),
        'f1': float(f1_score(y_test, pred)),
    }


def main():
    X0, y0 = build_dataset_from_folder('data/relaxed', label=0)
    X1, y1 = build_dataset_from_folder('data/focused', label=1)
    X = np.vstack([X0, X1])
    y = np.concatenate([y0, y1])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    results = []
    base = train_eval(X_train, y_train, X_test, y_test)
    results.append({'setting': 'all_features', **base})

    for i, b in enumerate(BANDS):
        Xtr = mask_band(X_train, i)
        Xte = mask_band(X_test, i)
        m = train_eval(Xtr, y_train, Xte, y_test)
        results.append({'setting': f'without_{b}', **m})

    out = Path('outputs')
    out.mkdir(exist_ok=True)
    fp = out / 'ablation_results.json'
    fp.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(json.dumps(results, indent=2))
    print(f'Saved {fp}')


if __name__ == '__main__':
    main()
