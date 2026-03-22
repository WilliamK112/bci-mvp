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
        for r in csv.DictReader(f):
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
    all_models = read_benchmark(out / "all_model_results.csv")
    cross = read_json(out / "cross_dataset_results.json")
    explain = read_json(out / "permutation_importance_summary.json")
    calib = read_json(out / "calibration_results.json")
    robust = read_json(out / "robustness_results.json")
    loso = read_json(out / "cross_subject_results.json")
    cs_bench = read_json(out / "cross_subject_model_benchmark.json")
    boot = read_json(out / "bootstrap_ci_results.json")

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

    lines += ["", "## 2) Unified Model Table"]
    if all_models:
        lines += ["", "| Model | Accuracy | F1 | AUC |", "|---|---:|---:|---:|"]
        for r in all_models:
            lines.append(f"| {r.get('model','-')} | {r.get('accuracy','-')} | {r.get('f1','-')} | {r.get('auc','-')} |")
    else:
        lines += ["", "No `outputs/all_model_results.csv` found."]

    lines += ["", "## 3) Cross-Dataset Generalization"]
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
        lines += ["", "- `docs/CROSS_DATASET_BIDIRECTIONAL.md`"]
    else:
        lines += ["", "No `outputs/cross_dataset_results.json` found."]

    lines += ["", "## 4) Explainability Summary"]
    if explain:
        lines += [
            "",
            f"- Base test accuracy: {explain.get('base_test_accuracy')}",
            f"- Num features: {explain.get('num_features')}",
            f"- Top band: {explain.get('top_band')}",
            f"- Top channel: {explain.get('top_channel')}",
        ]
        lines += ["", "- ![Explainability Heatmap](../assets/explainability_heatmap.svg)", "- Validation: `docs/EXPLAINABILITY_VALIDATION.md`"]
    else:
        lines += ["", "No `outputs/permutation_importance_summary.json` found."]

    lines += ["", "## 5) Probability Calibration"]
    if calib:
        lines += ["", f"- Brier score: {calib.get('brier_score')}", f"- Bins: {calib.get('n_bins')}"]
    else:
        lines += ["", "No `outputs/calibration_results.json` found."]

    lines += ["", "## 6) Robustness under Perturbations"]
    if robust:
        lines += ["", "| Setting | Accuracy | F1 |", "|---|---:|---:|"]
        for r in robust:
            lines.append(f"| {r.get('name')} | {r.get('accuracy')} | {r.get('f1')} |")
    else:
        lines += ["", "No `outputs/robustness_results.json` found."]

    lines += ["", "## 7) Cross-Subject Generalization (LOSO)"]
    if loso:
        lines += [
            "",
            f"- Subjects: {loso.get('subjects')}",
            f"- Mean Accuracy: {loso.get('mean_accuracy')}",
            f"- Mean F1: {loso.get('mean_f1')}",
            f"- Mean AUC: {loso.get('mean_auc')}",
        ]
    else:
        lines += ["", "No `outputs/cross_subject_results.json` found."]

    if cs_bench:
        lines += ["", "### Cross-Subject Model Benchmark", "", "| Model | Mean Accuracy | Mean F1 | Mean AUC |", "|---|---:|---:|---:|", "", "- ![Cross-Subject Benchmark](../assets/cross_subject_benchmark.svg)"]
        for r in (cs_bench.get('ranking') or []):
            lines.append(f"| {r.get('model')} | {r.get('mean_accuracy')} | {r.get('mean_f1')} | {r.get('mean_auc')} |")

    lines += ["", "### Cross-Subject Significance", "", "- `docs/CROSS_SUBJECT_SIGNIFICANCE.md`"]

    lines += [
        "",
        "## 8) Visual Artifacts",
        "",
        "- ![All Model](../assets/all_model_comparison.svg)",
        "- ![Cross Matrix](../assets/cross_dataset_matrix.svg)",
        "- ![Cross Subject LOSO](../assets/cross_subject_loso.svg)",
        "- ![Calibration](../assets/calibration_curve.svg)",
        "- ![Robustness](../assets/robustness_accuracy.svg)",
        "",
        "## 10) Release Readiness",
        "",
        "- Pipeline status: `docs/PIPELINE_STATUS.md`",
        "- Artifact validation: `outputs/artifact_validation_report.txt`",
        "- Model card: `docs/MODEL_CARD.md`",
    ]

    report = docs / "TECHNICAL_REPORT.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated {report}")


if __name__ == "__main__":
    main()
