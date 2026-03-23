"""
Automated Hyperparameter Tuning for the Random Forest model.
Uses RandomizedSearchCV to find the optimal hyperparameters for the BCI classifier.
Outputs:
- outputs/tuning_results.json
- outputs/model_rf_tuned.joblib
"""
import json
import joblib
from pathlib import Path
import numpy as np
import pandas as pd
from time import perf_counter

from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, make_scorer

from src.preprocess import build_dataset_from_folder

def main():
    print("[1] Loading and preprocessing data...")
    X0, y0 = build_dataset_from_folder("data/relaxed", label=0)
    X1, y1 = build_dataset_from_folder("data/focused", label=1)
    
    X = np.vstack([X0, X1])
    y = np.concatenate([y0, y1])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("[2] Setting up RandomizedSearchCV pipeline...")
    # Base pipeline
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(class_weight="balanced", random_state=42))
    ])

    # Hyperparameter grid space
    param_dist = {
        "rf__n_estimators": [100, 200, 400, 600, 800],
        "rf__max_depth": [None, 5, 10, 15, 20],
        "rf__min_samples_split": [2, 5, 10],
        "rf__min_samples_leaf": [1, 2, 4],
        "rf__max_features": ["sqrt", "log2", None]
    }

    # Cross-validation strategy
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    # We optimize for ROC AUC as it balances False Positives and False Negatives well
    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=param_dist,
        n_iter=20,  # Number of parameter settings that are sampled
        scoring="roc_auc",
        cv=cv,
        n_jobs=-1,
        random_state=42,
        verbose=1
    )

    print("[3] Running Hyperparameter Tuning (this may take a minute)...")
    t0 = perf_counter()
    search.fit(X_train, y_train)
    tuning_time = perf_counter() - t0

    print(f"\n[4] Tuning Complete in {tuning_time:.2f} seconds!")
    print("Best Parameters Found:")
    for k, v in search.best_params_.items():
        print(f"  {k.replace('rf__', '')}: {v}")
    
    print(f"Best CV ROC-AUC Score: {search.best_score_:.4f}")

    print("\n[5] Evaluating Best Model on Holdout Test Set...")
    best_model = search.best_estimator_
    pred = best_model.predict(X_test)
    proba = best_model.predict_proba(X_test)[:, 1]

    metrics = {
        "test_accuracy": float(accuracy_score(y_test, pred)),
        "test_f1": float(f1_score(y_test, pred)),
        "test_auc": float(roc_auc_score(y_test, proba)),
        "best_params": search.best_params_,
        "tuning_time_seconds": float(tuning_time)
    }

    print(f"  Test Accuracy: {metrics['test_accuracy']:.4f}")
    print(f"  Test F1 Score: {metrics['test_f1']:.4f}")
    print(f"  Test ROC-AUC:  {metrics['test_auc']:.4f}")

    print("\n[6] Saving artifacts...")
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    
    with open(out_dir / "tuning_results.json", "w") as f:
        json.dump(metrics, f, indent=2)
        
    joblib.dump(best_model, out_dir / "model_rf_tuned.joblib")
    
    print("Saved outputs/tuning_results.json and outputs/model_rf_tuned.joblib")

if __name__ == "__main__":
    main()
