import json
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from src.cross_dataset_eval import load_split
from src.domain_adaptation import CORAL

def evaluate_model(clf, X_train, y_train, X_test, y_test):
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    if hasattr(clf, "predict_proba"):
        proba = clf.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, proba)
    else:
        auc = np.nan
    return {
        "accuracy": float(accuracy_score(y_test, pred)),
        "f1": float(f1_score(y_test, pred)),
        "auc": float(auc)
    }

def main():
    root = Path("data")
    
    print("[1] Loading cross-dataset partitions...")
    X_A, y_A = load_split(root, "dataset_a")
    X_B, y_B = load_split(root, "dataset_b")
    
    # Scale first since CORAL assumes centered/scaled features typically
    scaler_A = StandardScaler().fit(X_A)
    scaler_B = StandardScaler().fit(X_B)
    
    X_A_scaled = scaler_A.transform(X_A)
    X_B_scaled = scaler_B.transform(X_B)
    
    print("[2] Aligning domain A -> B using CORAL...")
    coral_A_to_B = CORAL()
    X_A_aligned_B = coral_A_to_B.fit_transform(X_A_scaled, X_B_scaled)
    
    print("[3] Aligning domain B -> A using CORAL...")
    coral_B_to_A = CORAL()
    X_B_aligned_A = coral_B_to_A.fit_transform(X_B_scaled, X_A_scaled)

    # Base models
    models = {
        "RF": RandomForestClassifier(n_estimators=400, class_weight="balanced", random_state=42, n_jobs=-1),
        "SVM": SVC(C=2.0, kernel="rbf", probability=True, class_weight="balanced", random_state=42)
    }

    results = []

    print("[4] Evaluating Zero-Shot vs Domain Adaptation...")
    for model_name, model in models.items():
        # A -> B Zero-Shot
        res_A_B_baseline = evaluate_model(model, X_A_scaled, y_A, X_B_scaled, y_B)
        # A -> B CORAL
        res_A_B_coral = evaluate_model(model, X_A_aligned_B, y_A, X_B_scaled, y_B)
        
        # B -> A Zero-Shot
        res_B_A_baseline = evaluate_model(model, X_B_scaled, y_B, X_A_scaled, y_A)
        # B -> A CORAL
        res_B_A_coral = evaluate_model(model, X_B_aligned_A, y_B, X_A_scaled, y_A)

        results.extend([
            {"Model": model_name, "Direction": "A -> B", "Method": "Zero-Shot", **res_A_B_baseline},
            {"Model": model_name, "Direction": "A -> B", "Method": "CORAL DA", **res_A_B_coral},
            {"Model": model_name, "Direction": "B -> A", "Method": "Zero-Shot", **res_B_A_baseline},
            {"Model": model_name, "Direction": "B -> A", "Method": "CORAL DA", **res_B_A_coral},
        ])

    df = pd.DataFrame(results)
    print("\n--- Domain Adaptation Results ---")
    print(df.to_string(index=False))

    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    df.to_csv(out_dir / "coral_domain_adaptation.csv", index=False)
    
    # Save a markdown digest
    md_lines = [
        "# Cross-Dataset Generalization with Domain Adaptation",
        "",
        "| Model | Direction | Method | Accuracy | F1 | AUC |",
        "|---|---|---|---:|---:|---:|",
    ]
    for r in results:
        md_lines.append(f"| {r['Model']} | {r['Direction']} | {r['Method']} | {r['accuracy']:.4f} | {r['f1']:.4f} | {r['auc']:.4f} |")
        
    Path("docs/CORAL_DOMAIN_ADAPTATION.md").write_text("\n".join(md_lines), encoding="utf-8")
    print("\nSaved artifacts to outputs/coral_domain_adaptation.csv and docs/CORAL_DOMAIN_ADAPTATION.md")

if __name__ == "__main__":
    main()
