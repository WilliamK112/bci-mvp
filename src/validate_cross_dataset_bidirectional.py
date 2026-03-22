"""
Validate bidirectional cross-dataset transfer quality gates.
Outputs docs/CROSS_DATASET_BIDIRECTIONAL_VALIDATION.md
"""
from pathlib import Path
import json


def main():
    p = Path('outputs/cross_dataset_bidirectional.json')
    if not p.exists():
        raise SystemExit('Missing outputs/cross_dataset_bidirectional.json')
    d = json.loads(p.read_text(encoding='utf-8'))

    a = d.get('A_to_B', {}).get('models', {}).get('RF', {})
    b = d.get('B_to_A', {}).get('models', {}).get('RF', {})
    gap_acc = float(d.get('symmetry_gap_accuracy', 1e9))
    gap_f1 = float(d.get('symmetry_gap_f1', 1e9))
    gap_auc = float(d.get('symmetry_gap_auc', 1e9))

    checks = [
        ('A->B RF accuracy >= 0.50', float(a.get('accuracy', 0.0)) >= 0.50, float(a.get('accuracy', 0.0))),
        ('B->A RF accuracy >= 0.50', float(b.get('accuracy', 0.0)) >= 0.50, float(b.get('accuracy', 0.0))),
        ('A->B RF AUC >= 0.60', float(a.get('auc', 0.0)) >= 0.60, float(a.get('auc', 0.0))),
        ('B->A RF AUC >= 0.60', float(b.get('auc', 0.0)) >= 0.60, float(b.get('auc', 0.0))),
        ('Symmetry gap accuracy <= 0.25', gap_acc <= 0.25, gap_acc),
        ('Symmetry gap f1 <= 0.35', gap_f1 <= 0.35, gap_f1),
        ('Symmetry gap auc <= 0.20', gap_auc <= 0.20, gap_auc),
    ]

    passed = all(ok for _, ok, _ in checks)

    lines = [
        '# Cross-Dataset Bidirectional Validation',
        '',
        f"- Overall: **{'PASS' if passed else 'FAIL'}**",
        '',
        '| Gate | Result | Observed |',
        '|---|---:|---:|',
    ]
    for name, ok, obs in checks:
        lines.append(f"| {name} | {'✅' if ok else '❌'} | {obs:.4f} |")

    out = Path('docs/CROSS_DATASET_BIDIRECTIONAL_VALIDATION.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out} (overall={"PASS" if passed else "FAIL"})')

    if not passed:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
