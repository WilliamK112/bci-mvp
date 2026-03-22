"""
Generate a central registry of metrics, definitions, and artifact sources.
"""
from pathlib import Path
from datetime import datetime, timezone

ROWS = [
    ('Accuracy', 'Classification correctness ratio', 'outputs/benchmark_results.csv; outputs/all_model_results.csv'),
    ('F1', 'Harmonic mean of precision/recall', 'outputs/benchmark_results.csv; outputs/all_model_results.csv'),
    ('AUC', 'ROC area under curve', 'outputs/benchmark_results.csv; outputs/bootstrap_ci_results.json'),
    ('Brier score', 'Probability calibration error (lower is better)', 'outputs/calibration_results.json'),
    ('Robustness Accuracy', 'Accuracy under synthetic perturbations', 'outputs/robustness_results.json'),
    ('Ablation Delta', 'Performance change when dropping band groups', 'outputs/ablation_results.json'),
    ('Bootstrap CI95', 'Empirical uncertainty interval from resampling', 'outputs/bootstrap_ci_results.json'),
    ('Cross-dataset score', 'Generalization from train dataset A to test dataset B', 'outputs/cross_dataset_results.json; outputs/cross_dataset_matrix.json'),
    ('LOSO Mean Accuracy', 'Cross-subject leave-one-subject-out mean accuracy', 'outputs/cross_subject_results.json'),
]


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# Metrics Registry', '', f'Generated: {ts}', '', '| Metric | Definition | Source Artifact(s) |', '|---|---|---|']
    for r in ROWS:
        lines.append(f'| {r[0]} | {r[1]} | `{r[2]}` |')

    out = Path('docs/METRICS_REGISTRY.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
