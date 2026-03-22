from pathlib import Path
import numpy as np
import pandas as pd
from time import perf_counter

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from src.preprocess import build_dataset_from_folder


def evaluate_model(name, clf, X_train, y_train, X_test, y_test):
    t0 = perf_counter()
    clf.fit(X_train, y_train)
    train_time = perf_counter() - t0

    t1 = perf_counter()
    pred = clf.predict(X_test)
    infer_time = (perf_counter() - t1) / len(X_test)

    if hasattr(clf, "predict_proba"):
        proba = clf.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, proba)
    else:
        auc = np.nan

    return {
        "model": name,
        "accuracy": accuracy_score(y_test, pred),
        "f1": f1_score(y_test, pred),
        "auc": auc,
        "train_sec": train_time,
        "infer_sec_per_sample": infer_time,
    }


def main():
    X0, y0 = build_dataset_from_folder("data/relaxed", label=0)
    X1, y1 = build_dataset_from_folder("data/focused", label=1)
    X = np.vstack([X0, X1])
    y = np.concatenate([y0, y1])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

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

    rows = []
    for name, clf in models.items():
        rows.append(evaluate_model(name, clf, X_train, y_train, X_test, y_test))

    df = pd.DataFrame(rows).sort_values("accuracy", ascending=False)
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    out_csv = out_dir / "benchmark_results.csv"
    df.to_csv(out_csv, index=False)

    print(df.to_string(index=False))
    print(f"Saved: {out_csv}")


if __name__ == "__main__":
    main()
