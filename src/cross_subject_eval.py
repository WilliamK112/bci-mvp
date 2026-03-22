"""
Cross-subject generalization (Leave-One-Subject-Out) on local EDF folders.
Subject id is parsed from filename pattern: subXX_...

Outputs:
- outputs/cross_subject_results.json
"""
from pathlib import Path
import json
import re
import numpy as np
from collections import defaultdict

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from src.preprocess import load_edf_extract_features


def subject_id_from_name(name: str):
    m = re.search(r"sub(\d+)", name)
    return int(m.group(1)) if m else None


def load_subject_grouped(folder: str, label: int):
    grouped = defaultdict(list)
    for f in sorted(Path(folder).glob("*.edf")):
        sid = subject_id_from_name(f.name)
        if sid is None:
            continue
        X = load_edf_extract_features(str(f))
        y = np.full((len(X),), label, dtype=int)
        grouped[sid].append((X, y))
    out = {}
    for sid, chunks in grouped.items():
        X = np.vstack([c[0] for c in chunks])
        y = np.concatenate([c[1] for c in chunks])
        out[sid] = (X, y)
    return out


def main():
    g0 = load_subject_grouped("data/relaxed", 0)
    g1 = load_subject_grouped("data/focused", 1)

    subjects = sorted(set(g0.keys()) & set(g1.keys()))
    if len(subjects) < 2:
        raise SystemExit("Need at least 2 subjects present in both relaxed and focused sets")

    rows = []
    for test_sid in subjects:
        X_test = np.vstack([g0[test_sid][0], g1[test_sid][0]])
        y_test = np.concatenate([g0[test_sid][1], g1[test_sid][1]])

        train_X_parts, train_y_parts = [], []
        for sid in subjects:
            if sid == test_sid:
                continue
            train_X_parts += [g0[sid][0], g1[sid][0]]
            train_y_parts += [g0[sid][1], g1[sid][1]]

        X_train = np.vstack(train_X_parts)
        y_train = np.concatenate(train_y_parts)

        clf = Pipeline([
            ("scaler", StandardScaler()),
            ("rf", RandomForestClassifier(n_estimators=400, class_weight="balanced", random_state=42, n_jobs=-1)),
        ])
        clf.fit(X_train, y_train)
        pred = clf.predict(X_test)
        proba = clf.predict_proba(X_test)[:, 1]

        rows.append({
            "test_subject": int(test_sid),
            "train_samples": int(len(y_train)),
            "test_samples": int(len(y_test)),
            "accuracy": float(accuracy_score(y_test, pred)),
            "f1": float(f1_score(y_test, pred)),
            "auc": float(roc_auc_score(y_test, proba)),
        })

    summary = {
        "n_subjects": len(subjects),
        "subjects": subjects,
        "mean_accuracy": float(np.mean([r["accuracy"] for r in rows])),
        "mean_f1": float(np.mean([r["f1"] for r in rows])),
        "mean_auc": float(np.mean([r["auc"] for r in rows])),
        "per_subject": rows,
    }

    out = Path("outputs/cross_subject_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
