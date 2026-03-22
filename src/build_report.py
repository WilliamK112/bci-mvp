"""
Build a single markdown technical report from generated artifacts.
"""
from pathlib import Path
import json
import csv
from datetime import datetime, timezone


def read_benchmark(path: Path):
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for i, r in enumerate(csv.DictReader(f)):
            rows.append(r)
    return rows


def read_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    out = Path("outputs")
    docs = Path("docs")
    docs.mkdir(exist_ok=True)

    bench = read_benchmark(out / "benchmark_results.csv")
    cross = read_json(out / "cross_dataset_results.json")
    explain = read_json(out / "permutation_importance_summary.json")

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# BCI MVP Technical Report",
        "",
        f"Generated: {ts}",
        "",
        "## 1) Benchmark Summary",
    ]

    if bench:
        lines += ["", "| Model | Accuracy | F1 | AUC |", "|---|---:|---:|---:|"]
        for r in bench:
            lines.append(f"| {r.get('model','-')} | {r.get('accuracy','-')} | {r.get('f1','-')} | {r.get('auc','-')} |")
    else:
        lines += ["", "No `outputs/benchmark_results.csv` found."]

    lines += ["", "## 2) Cross-Dataset Generalization"]
    if cross:
        lines += [
            "",
            f"- Train dataset: **{cross.get('train_dataset')}**",
            f"- Test dataset: **{cross.get('test_dataset')}**",
            f"- Train samples: {cross.get('train_samples')}",
            f"- Test samples: {cross.get('test_samples')}",
            "",
            "| Model | Accuracy | F1 | AUC |",
            "|---|---:|---:|---:|",
        ]
        for m, v in (cross.get("models") or {}).items():
            lines.append(f"| {m} | {v.get('accuracy')} | {v.get('f1')} | {v.get('auc')} |")
    else:
        lines += ["", "No `outputs/cross_dataset_results.json` found."]

    lines += ["", "## 3) Explainability Summary"]
    if explain:
        lines += [
            "",
            f"- Base test accuracy: {explain.get('base_test_accuracy')}",
            f"- Num features: {explain.get('num_features')}",
            f"- Top band: {explain.get('top_band')}",
            f"- Top channel: {explain.get('top_channel')}",
        ]
    else:
        lines += ["", "No `outputs/permutation_importance_summary.json` found."]

    lines += [
        "",
        "## 4) Visual Artifacts",
        "",
        "- ![Benchmark](../assets/benchmark_scores.svg)",
        "- ![Cross Dataset](../assets/cross_dataset_scores.svg)",
    ]

    report = docs / "TECHNICAL_REPORT.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated {report}")


if __name__ == "__main__":
    main()
