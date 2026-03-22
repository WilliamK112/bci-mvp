"""
Run cross-dataset matrix evaluation:
for each dataset_i != dataset_j, train on i and test on j.

Expected data layout:
  data/<dataset_name>/{relaxed,focused}/*.edf
"""
from pathlib import Path
import json
import numpy as np
from itertools import permutations
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

from src.preprocess import build_dataset_from_folder


def load_dataset(root: Path, name: str):
    base = root / name
    x0, y0 = build_dataset_from_folder(str(base / "relaxed"), label=0)
    x1, y1 = build_dataset_from_folder(str(base / "focused"), label=1)
    X = np.vstack([x0, x1])
    y = np.concatenate([y0, y1])
    return X, y


def main():
    root = Path("data")
    datasets = sorted([p.name for p in root.iterdir() if p.is_dir() and (p / "relaxed").exists() and (p / "focused").exists()])
    if len(datasets) < 2:
        print("Need at least 2 datasets in data/<name>/{relaxed,focused}")
        return

    cache = {}
    for d in datasets:
        cache[d] = load_dataset(root, d)

    rows = []
    for train_name, test_name in permutations(datasets, 2):
        Xtr, ytr = cache[train_name]
        Xte, yte = cache[test_name]

        model = Pipeline([
            ("scaler", StandardScaler()),
            ("rf", RandomForestClassifier(n_estimators=400, class_weight="balanced", random_state=42, n_jobs=-1)),
        ])
        model.fit(Xtr, ytr)
        pred = model.predict(Xte)
        rows.append({
            "train": train_name,
            "test": test_name,
            "train_n": int(len(ytr)),
            "test_n": int(len(yte)),
            "accuracy": float(accuracy_score(yte, pred)),
            "f1": float(f1_score(yte, pred)),
        })

    out = Path("outputs")
    out.mkdir(exist_ok=True)
    fp = out / "cross_dataset_matrix.json"
    fp.write_text(json.dumps({"datasets": datasets, "results": rows}, indent=2), encoding="utf-8")
    print(f"Saved {fp}")


if __name__ == "__main__":
    main()
