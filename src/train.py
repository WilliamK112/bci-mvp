from pathlib import Path
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_auc_score
from src.preprocess import build_dataset_from_folder


def main():
    X0, y0 = build_dataset_from_folder("data/relaxed", label=0)
    X1, y1 = build_dataset_from_folder("data/focused", label=1)

    X = np.vstack([X0, X1])
    y = np.concatenate([y0, y1])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(
            n_estimators=400,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        ))
    ])

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(clf, X_train, y_train, cv=cv, scoring="accuracy", n_jobs=-1)

    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    proba = clf.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, pred)
    auc = roc_auc_score(y_test, proba)

    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, out_dir / "model_rf_real.joblib")

    metrics = {
        "cv_mean": float(cv_scores.mean()),
        "cv_std": float(cv_scores.std()),
        "test_accuracy": float(acc),
        "test_auc": float(auc),
    }
    (out_dir / "metrics.json").write_text(str(metrics), encoding="utf-8")

    print(f"CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"Test Accuracy: {acc:.4f}")
    print(f"Test ROC-AUC: {auc:.4f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, pred))
    print(classification_report(y_test, pred, target_names=["relaxed", "focused"]))


if __name__ == "__main__":
    main()
