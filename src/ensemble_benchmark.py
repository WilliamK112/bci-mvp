"""
Ensemble model benchmark for superior classification performance.
Combines RF, SVM, and MLP into a Stacking Classifier to exceed baseline accuracy.
Outputs metrics to outputs/ensemble_results.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd
from time import perf_counter

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
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
    print("[1] Loading data...")
    X0, y0 = build_dataset_from_folder("data/relaxed", label=0)
    X1, y1 = build_dataset_from_folder("data/focused", label=1)
    X = np.vstack([X0, X1])
    y = np.concatenate([y0, y1])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    rf = RandomForestClassifier(n_estimators=400, class_weight="balanced", random_state=42, n_jobs=-1)
    svm = SVC(C=2.0, kernel="rbf", probability=True, class_weight="balanced", random_state=42)
    mlp = MLPClassifier(hidden_layer_sizes=(128, 64), activation="relu", early_stopping=True, random_state=42)
    
    estimators = [
        ('rf', rf),
        ('svm', svm),
        ('mlp', mlp)
    ]

    stacking = StackingClassifier(
        estimators=estimators,
        final_estimator=LogisticRegression(),
        cv=5,
        n_jobs=-1
    )

    models = {
        "RF_Baseline": Pipeline([("scaler", StandardScaler()), ("clf", rf)]),
        "SVM_Baseline": Pipeline([("scaler", StandardScaler()), ("clf", svm)]),
        "MLP_Baseline": Pipeline([("scaler", StandardScaler()), ("clf", mlp)]),
        "Stacking_Ensemble": Pipeline([("scaler", StandardScaler()), ("clf", stacking)]),
    }

    print("[2] Evaluating models...")
    rows = []
    for name, clf in models.items():
        print(f"    -> Training {name}...")
        rows.append(evaluate_model(name, clf, X_train, y_train, X_test, y_test))

    df = pd.DataFrame(rows).sort_values("accuracy", ascending=False)
    
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    out_csv = out_dir / "ensemble_benchmark_results.csv"
    df.to_csv(out_csv, index=False)

    print("\n[3] Results:")
    print(df.to_string(index=False))
    print(f"\nSaved results to {out_csv}")

if __name__ == "__main__":
    main()
