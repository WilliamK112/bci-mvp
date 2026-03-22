"""
Cross-dataset generalization evaluation.

Expected structure:
  data/
    dataset_a/
      relaxed/*.edf
      focused/*.edf
    dataset_b/
      relaxed/*.edf
      focused/*.edf

Usage:
  python src/cross_dataset_eval.py --train dataset_a --test dataset_b
"""

from pathlib import Path
import argparse
import json
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from src.preprocess import build_dataset_from_folder


def load_split(root: Path, name: str):
    base = root / name
    x0, y0 = build_dataset_from_folder(str(base / "relaxed"), label=0)
    x1, y1 = build_dataset_from_folder(str(base / "focused"), label=1)
    X = np.vstack([x0, x1])
    y = np.concatenate([y0, y1])
    return X, y


def evaluate(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    result = {
        "accuracy": float(accuracy_score(y_test, pred)),
        "f1": float(f1_score(y_test, pred)),
    }
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X_test)[:, 1]
        result["auc"] = float(roc_auc_score(y_test, proba))
    else:
        result["auc"] = None
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", default="data")
    parser.add_argument("--train", required=True, help="train dataset folder name under data/")
    parser.add_argument("--test", required=True, help="test dataset folder name under data/")
    parser.add_argument("--out", default="outputs/cross_dataset_results.json")
    args = parser.parse_args()

    root = Path(args.data_root)
    X_train, y_train = load_split(root, args.train)
    X_test, y_test = load_split(root, args.test)

    models = {
        "RF": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(n_estimators=400, class_weight="balanced", random_state=42, n_jobs=-1)),
        ]),
        "SVM": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", SVC(C=2.0, kernel="rbf", probability=True, class_weight="balanced", random_state=42)),
        ]),
    }

    results = {
        "train_dataset": args.train,
        "test_dataset": args.test,
        "train_samples": int(len(y_train)),
        "test_samples": int(len(y_test)),
        "models": {},
    }

    for name, model in models.items():
        results["models"][name] = evaluate(model, X_train, y_train, X_test, y_test)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
