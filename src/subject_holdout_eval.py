"""
Subject-holdout evaluation for stronger generalization testing.
Uses subject id parsed from EDF filename pattern: subXX_...
"""
from pathlib import Path
import re
import json
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from src.preprocess import load_edf_extract_features


def subject_id_from_name(name: str):
    m = re.search(r'sub(\d+)_', name)
    return int(m.group(1)) if m else None


def load_labeled(folder: Path, label: int):
    rows = []
    for f in sorted(folder.glob('*.edf')):
        sid = subject_id_from_name(f.name)
        if sid is None:
            continue
        X = load_edf_extract_features(str(f))
        y = np.full((len(X),), label, dtype=int)
        sid_arr = np.full((len(X),), sid, dtype=int)
        rows.append((X, y, sid_arr))
    if not rows:
        raise RuntimeError(f'No usable EDF in {folder}')
    X = np.vstack([r[0] for r in rows])
    y = np.concatenate([r[1] for r in rows])
    s = np.concatenate([r[2] for r in rows])
    return X, y, s


def main():
    X0, y0, s0 = load_labeled(Path('data/relaxed'), 0)
    X1, y1, s1 = load_labeled(Path('data/focused'), 1)
    X = np.vstack([X0, X1])
    y = np.concatenate([y0, y1])
    s = np.concatenate([s0, s1])

    subjects = sorted(set(s.tolist()))
    results = []

    for sid in subjects:
        tr = s != sid
        te = s == sid
        if te.sum() == 0 or tr.sum() == 0:
            continue

        clf = Pipeline([
            ('scaler', StandardScaler()),
            ('rf', RandomForestClassifier(n_estimators=300, class_weight='balanced', random_state=42, n_jobs=-1)),
        ])
        clf.fit(X[tr], y[tr])
        pred = clf.predict(X[te])
        proba = clf.predict_proba(X[te])[:, 1]

        row = {
            'subject_holdout': int(sid),
            'test_samples': int(te.sum()),
            'accuracy': float(accuracy_score(y[te], pred)),
            'f1': float(f1_score(y[te], pred)),
            'auc': float(roc_auc_score(y[te], proba)),
        }
        results.append(row)

    out = Path('outputs')
    out.mkdir(exist_ok=True)
    fp = out / 'subject_holdout_results.json'
    fp.write_text(json.dumps({'results': results}, indent=2), encoding='utf-8')
    print(json.dumps({'results': results}, indent=2))
    print(f'Saved {fp}')


if __name__ == '__main__':
    main()
