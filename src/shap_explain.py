import json
from pathlib import Path

import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import shap

from src.preprocess import build_dataset_from_folder

BANDS = ["delta", "theta", "alpha", "beta"]


def get_feature_names(n_features):
    n_channels = n_features // 4
    names = []
    for ch in range(n_channels):
        for b in BANDS:
            names.append(f"Ch{ch}_{b}")
    return names


def main():
    print("[1] Loading data...")
    X0, y0 = build_dataset_from_folder("data/relaxed", label=0)
    X1, y1 = build_dataset_from_folder("data/focused", label=1)

    X = np.vstack([X0, X1])
    y = np.concatenate([y0, y1])

    # Reproduce test set from train.py
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("[2] Loading model...")
    model_path = Path("outputs/model_rf_real.joblib")
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}. Run train.py first.")
    
    clf = joblib.load(model_path)
    # the pipeline has ("scaler", StandardScaler()), ("rf", RandomForestClassifier(...))
    scaler = clf.named_steps["scaler"]
    rf = clf.named_steps["rf"]
    
    # Scale test set
    X_test_scaled = scaler.transform(X_test)
    
    feature_names = get_feature_names(X_test.shape[1])
    
    # Optional: sub-sample test set for faster SHAP computation if it's too large,
    # but since it's an RF and our dataset is small (a few hundred epochs), we can use the whole test set.
    print("[3] Computing SHAP values...")
    explainer = shap.TreeExplainer(rf)
    
    # TreeExplainer on RandomForest can return SHAP values of shape (n_samples, n_features, n_classes)
    # We want the values for the positive class (class 1)
    shap_values = explainer.shap_values(X_test_scaled)
    
    # Handle older/newer SHAP versions returning list or array
    if isinstance(shap_values, list):
        shap_values_pos = shap_values[1]
    elif len(shap_values.shape) == 3:
        shap_values_pos = shap_values[:, :, 1]
    else:
        shap_values_pos = shap_values

    print("[4] Generating SHAP summary plot...")
    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values_pos, X_test_scaled, feature_names=feature_names, show=False)
    plt.tight_layout()
    plt.savefig(out_dir / "shap_summary_plot.png", dpi=300, bbox_inches="tight")
    plt.close()
    
    print("[5] Generating SHAP bar plot...")
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values_pos, X_test_scaled, feature_names=feature_names, plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig(out_dir / "shap_bar_plot.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Mean absolute SHAP values per feature
    mean_abs_shap = np.mean(np.abs(shap_values_pos), axis=0)
    shap_df = pd.DataFrame({
        "feature": feature_names,
        "mean_abs_shap": mean_abs_shap
    }).sort_values(by="mean_abs_shap", ascending=False)
    
    shap_df.to_csv(out_dir / "shap_feature_importance.csv", index=False)
    
    top_5_features = shap_df.head(5).to_dict(orient="records")
    summary = {
        "n_test_samples": len(X_test),
        "n_features": len(feature_names),
        "top_5_shap_features": top_5_features
    }
    
    with open(out_dir / "shap_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\nTop 5 features by mean |SHAP|:")
    for row in top_5_features:
        print(f"  {row['feature']}: {row['mean_abs_shap']:.4f}")
        
    print("\n[6] SHAP evaluation complete. Artifacts saved to outputs/")


if __name__ == "__main__":
    main()