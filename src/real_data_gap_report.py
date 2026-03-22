"""
Generate a gap report between demo placeholders and real-data required artifacts.
"""
from pathlib import Path
from datetime import datetime, timezone

CHECKS = [
    ('outputs/benchmark_results.csv', 'Benchmark results'),
    ('outputs/all_model_results.csv', 'Unified model results'),
    ('outputs/cross_dataset_results.json', 'Cross-dataset single-pair results'),
    ('outputs/cross_dataset_matrix.json', 'Cross-dataset matrix results'),
    ('outputs/permutation_importance_summary.json', 'Permutation explainability summary'),
    ('outputs/calibration_results.json', 'Calibration results'),
    ('outputs/robustness_results.json', 'Robustness results'),
    ('outputs/ablation_results.json', 'Ablation results'),
    ('outputs/bootstrap_ci_results.json', 'Bootstrap CI results'),
]


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# Real-Data Gap Report', '', f'Generated: {ts}', '', '| Item | Status | Path |', '|---|---|---|']
    present = 0
    for p, name in CHECKS:
        ok = Path(p).exists()
        status = 'READY' if ok else 'MISSING_REAL_RUN'
        lines.append(f'| {name} | {status} | `{p}` |')
        present += int(ok)

    lines += [
        '',
        f'**Coverage:** {present}/{len(CHECKS)}',
        '',
        '## Action Plan',
        '1. Place real EDF data into required folders.',
        '2. Run `python src/run_full_pipeline.py`.',
        '3. Re-run `python src/final_release_candidate.py` and `python src/release_readiness.py`.',
    ]

    out = Path('docs/REAL_DATA_GAP_REPORT.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
