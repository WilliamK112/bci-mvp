"""
Validate explainability artifacts and basic signal quality gates.
Outputs docs/EXPLAINABILITY_VALIDATION.md
"""
from pathlib import Path
import json
import pandas as pd


def main():
    summary_p = Path('outputs/permutation_importance_summary.json')
    detail_p = Path('outputs/permutation_importance_detailed.csv')
    heatmap_p = Path('assets/explainability_heatmap.svg')

    checks = []

    checks.append(('summary exists', summary_p.exists(), 1.0 if summary_p.exists() else 0.0))
    checks.append(('detailed csv exists', detail_p.exists(), 1.0 if detail_p.exists() else 0.0))
    checks.append(('heatmap exists', heatmap_p.exists(), 1.0 if heatmap_p.exists() else 0.0))

    top_importance = None
    base_acc = None
    if summary_p.exists():
        obj = json.loads(summary_p.read_text(encoding='utf-8'))
        base_acc = float(obj.get('base_test_accuracy', 0.0))
        top = obj.get('top_feature') or []
        if top:
            top_importance = float(top[0].get('importance_mean', 0.0))

    if detail_p.exists():
        df = pd.read_csv(detail_p)
        nonzero = int((df['importance_mean'] != 0).sum()) if 'importance_mean' in df.columns else 0
        checks.append(('nonzero feature importances >= 4', nonzero >= 4, float(nonzero)))
    else:
        checks.append(('nonzero feature importances >= 4', False, 0.0))

    checks.append(('base test accuracy >= 0.70', (base_acc is not None and base_acc >= 0.70), float(base_acc or 0.0)))
    checks.append(('top feature importance > 0', (top_importance is not None and top_importance > 0.0), float(top_importance or 0.0)))

    passed = all(ok for _, ok, _ in checks)

    lines = [
        '# Explainability Validation',
        '',
        f"- Overall: **{'PASS' if passed else 'FAIL'}**",
        '',
        '| Gate | Result | Observed |',
        '|---|---:|---:|',
    ]
    for name, ok, obs in checks:
        lines.append(f"| {name} | {'✅' if ok else '❌'} | {obs:.4f} |")

    out = Path('docs/EXPLAINABILITY_VALIDATION.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out} (overall={"PASS" if passed else "FAIL"})')

    if not passed:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
