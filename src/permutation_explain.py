"""
Permutation-based explainability (model-agnostic).
Generates robust feature importance on held-out data.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from src.preprocess import build_dataset_from_folder

BANDS = ["delta", "theta", "alpha", "beta"]


def main():
    # Load data
    X0, y0 = build_dataset_from_folder("data/relaxed", label=0)
    X1, y1 = build_dataset_from_folder("data/focused", label=1)
    X = np.vstack([X0, X1])
    y = np.concatenate([y0, y1])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model_path = Path("outputs/model_rf_real.joblib")
    if not model_path.exists():
        raise FileNotFoundError("Model missing: run python src/train.py first")
    model = joblib.load(model_path)

    # Evaluate baseline
    pred = model.predict(X_test)
    base_acc = accuracy_score(y_test, pred)

    # Permutation importance
    pi = permutation_importance(
        model, X_test, y_test,
        n_repeats=10,
        random_state=42,
        n_jobs=-1,
        scoring="accuracy",
    )

    means = pi.importances_mean
    stds = pi.importances_std

    rows = []
    for i, (m, s) in enumerate(zip(means, stds)):
        rows.append({"feature_idx": i, "importance_mean": float(m), "importance_std": float(s)})
    df = pd.DataFrame(rows).sort_values("importance_mean", ascending=False)

    # Aggregate by band/channel (expects channel*4 layout)
    if len(df) % 4 == 0:
        agg_rows = []
        n_channels = len(df) // 4
        for ch in range(n_channels):
            for bi, b in enumerate(BANDS):
                idx = ch * 4 + bi
                row = rows[idx]
                agg_rows.append({"channel": ch, "band": b, "importance_mean": row["importance_mean"]})
        agg = pd.DataFrame(agg_rows)
        by_band = agg.groupby("band", as_index=False)["importance_mean"].sum().sort_values("importance_mean", ascending=False)
        by_channel = agg.groupby("channel", as_index=False)["importance_mean"].sum().sort_values("importance_mean", ascending=False)
    else:
        by_band = pd.DataFrame(columns=["band", "importance_mean"])
        by_channel = pd.DataFrame(columns=["channel", "importance_mean"])

    out = Path("outputs")
    out.mkdir(exist_ok=True)
    df.to_csv(out / "permutation_importance_detailed.csv", index=False)
    by_band.to_csv(out / "permutation_importance_by_band.csv", index=False)
    by_channel.to_csv(out / "permutation_importance_by_channel.csv", index=False)

    summary = {
        "base_test_accuracy": float(base_acc),
        "num_features": int(len(rows)),
        "top_feature": df.head(1).to_dict(orient="records"),
        "top_band": by_band.head(1).to_dict(orient="records") if len(by_band) else [],
        "top_channel": by_channel.head(1).to_dict(orient="records") if len(by_channel) else [],
    }
    (out / "permutation_importance_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print("Saved permutation importance artifacts to outputs/")


if __name__ == "__main__":
    main()
