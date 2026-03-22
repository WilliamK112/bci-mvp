"""
Model explainability for RF baseline.
- Computes feature importances
- Aggregates by frequency band and channel
- Saves csv/json summaries
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import joblib

BANDS = ["delta", "theta", "alpha", "beta"]


def main(model_path="outputs/model_rf_real.joblib", max_channels=8):
    model = joblib.load(model_path)
    rf = model.named_steps.get("rf") or model.named_steps.get("clf")
    if rf is None or not hasattr(rf, "feature_importances_"):
        raise RuntimeError("Loaded model does not expose feature_importances_")

    imp = rf.feature_importances_
    n_features = len(imp)
    # expected features = channels * 4 bands
    if n_features % 4 != 0:
        raise RuntimeError(f"Unexpected feature dim {n_features}, not divisible by 4")

    n_channels = n_features // 4
    rows = []
    for ch in range(n_channels):
        for bi, b in enumerate(BANDS):
            idx = ch * 4 + bi
            rows.append({"channel": ch, "band": b, "importance": float(imp[idx])})

    df = pd.DataFrame(rows)
    by_band = df.groupby("band", as_index=False)["importance"].sum().sort_values("importance", ascending=False)
    by_channel = df.groupby("channel", as_index=False)["importance"].sum().sort_values("importance", ascending=False)

    out = Path("outputs")
    out.mkdir(exist_ok=True)
    df.to_csv(out / "feature_importance_detailed.csv", index=False)
    by_band.to_csv(out / "feature_importance_by_band.csv", index=False)
    by_channel.to_csv(out / "feature_importance_by_channel.csv", index=False)

    summary = {
        "n_features": int(n_features),
        "n_channels": int(n_channels),
        "top_band": by_band.iloc[0].to_dict() if len(by_band) else None,
        "top_channel": by_channel.iloc[0].to_dict() if len(by_channel) else None,
    }
    (out / "explainability_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("Top bands:")
    print(by_band.to_string(index=False))
    print("\nTop channels:")
    print(by_channel.head(10).to_string(index=False))
    print("\nSaved explainability artifacts in outputs/")


if __name__ == "__main__":
    main()
