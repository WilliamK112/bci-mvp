"""
Generate publication-style visuals from benchmark/cross-dataset outputs.
"""
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt


def plot_benchmark(csv_path: Path, out_dir: Path):
    df = pd.read_csv(csv_path)
    metrics = ["accuracy", "f1", "auc"]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = range(len(df))
    width = 0.22

    for i, m in enumerate(metrics):
        vals = df[m].fillna(0).values
        ax.bar([p + (i - 1) * width for p in x], vals, width=width, label=m.upper())

    ax.set_xticks(list(x))
    ax.set_xticklabels(df["model"].tolist())
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Score")
    ax.set_title("Model Benchmark Comparison")
    ax.legend()
    fig.tight_layout()

    out = out_dir / "benchmark_scores.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


def plot_cross_dataset(json_path: Path, out_dir: Path):
    data = json.loads(json_path.read_text(encoding="utf-8"))
    models = data["models"]
    rows = []
    for m, vals in models.items():
        rows.append({"model": m, **vals})
    df = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.bar(df["model"], df["accuracy"], label="Accuracy")
    if "auc" in df.columns and df["auc"].notna().any():
        ax.plot(df["model"], df["auc"], marker="o", label="AUC")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Score")
    ax.set_title(f"Cross-dataset: {data['train_dataset']} -> {data['test_dataset']}")
    ax.legend()
    fig.tight_layout()

    out = out_dir / "cross_dataset_scores.png"
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


def main():
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)

    generated = []
    bench = out_dir / "benchmark_results.csv"
    cross = out_dir / "cross_dataset_results.json"

    if bench.exists():
        generated.append(plot_benchmark(bench, out_dir))
    if cross.exists():
        generated.append(plot_cross_dataset(cross, out_dir))

    if not generated:
        print("No benchmark_results.csv or cross_dataset_results.json found in outputs/")
        return

    print("Generated:")
    for g in generated:
        print(f"- {g}")


if __name__ == "__main__":
    main()
