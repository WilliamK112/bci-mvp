"""
Generate docs/RESULTS.md from available output artifacts.
"""
from pathlib import Path
import json
import csv
from datetime import datetime, timezone


def read_json(path):
    p=Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def read_csv(path):
    p=Path(path)
    if not p.exists():
        return []
    with p.open('r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    all_models = read_csv('outputs/all_model_results.csv')
    cross = read_json('outputs/cross_dataset_results.json')
    calib = read_json('outputs/calibration_results.json')
    robust = read_json('outputs/robustness_results.json')
    boot = read_json('outputs/bootstrap_ci_results.json')

    lines=["# Results","",f"Generated: {ts}",""]

    lines += ["## Model Comparison", ""]
    if all_models:
        lines += ["| Model | Accuracy | F1 | AUC |","|---|---:|---:|---:|"]
        for r in all_models:
            lines.append(f"| {r.get('model')} | {r.get('accuracy')} | {r.get('f1')} | {r.get('auc')} |")
    else:
        lines.append("No `outputs/all_model_results.csv` found.")

    lines += ["", "## Cross-Dataset", ""]
    if cross:
        lines += [f"- Train: **{cross.get('train_dataset')}**", f"- Test: **{cross.get('test_dataset')}**", ""]
        lines += ["| Model | Accuracy | F1 | AUC |","|---|---:|---:|---:|"]
        for m,v in (cross.get('models') or {}).items():
            lines.append(f"| {m} | {v.get('accuracy')} | {v.get('f1')} | {v.get('auc')} |")
    else:
        lines.append("No `outputs/cross_dataset_results.json` found.")

    lines += ["", "## Calibration & Uncertainty", ""]
    if calib:
        lines.append(f"- Brier score: **{calib.get('brier_score')}**")
    else:
        lines.append("- Brier score: n/a")
    if boot:
        lines.append(f"- Accuracy CI95: {boot.get('accuracy_ci95')}")
        lines.append(f"- F1 CI95: {boot.get('f1_ci95')}")
        lines.append(f"- AUC CI95: {boot.get('auc_ci95')}")
    else:
        lines.append("- Bootstrap CI: n/a")

    lines += ["", "## Robustness", ""]
    if robust:
        lines += ["| Setting | Accuracy | F1 |", "|---|---:|---:|"]
        for r in robust:
            lines.append(f"| {r.get('name')} | {r.get('accuracy')} | {r.get('f1')} |")
    else:
        lines.append("No `outputs/robustness_results.json` found.")

    lines += ["", "## Visuals", "", "- ![All Models](../assets/all_model_comparison.svg)", "- ![Cross Matrix](../assets/cross_dataset_matrix.svg)", "- ![Calibration](../assets/calibration_curve.svg)", "- ![Robustness](../assets/robustness_accuracy.svg)"]

    out=Path('docs/RESULTS.md')
    out.write_text('\n'.join(lines)+"\n", encoding='utf-8')
    print(f"Generated {out}")


if __name__=='__main__':
    main()
