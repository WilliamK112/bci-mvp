"""
Bootstrap confidence intervals for LOSO cross-subject benchmark metrics.
Inputs:
- outputs/cross_subject_model_benchmark.json
Outputs:
- outputs/cross_subject_ci.json
- docs/CROSS_SUBJECT_CI.md
"""
from pathlib import Path
import json
import random
import numpy as np


def bootstrap_ci(vals, n_boot=5000, alpha=0.05, seed=42):
    rng = random.Random(seed)
    arr = list(vals)
    if not arr:
        return {'mean': None, 'ci_low': None, 'ci_high': None}
    boots = []
    n = len(arr)
    for _ in range(n_boot):
        sample = [arr[rng.randrange(n)] for __ in range(n)]
        boots.append(float(np.mean(sample)))
    boots = np.array(boots, dtype=float)
    return {
        'mean': float(np.mean(arr)),
        'ci_low': float(np.quantile(boots, alpha / 2)),
        'ci_high': float(np.quantile(boots, 1 - alpha / 2)),
    }


def main():
    src = Path('outputs/cross_subject_model_benchmark.json')
    if not src.exists():
        raise SystemExit('Missing outputs/cross_subject_model_benchmark.json')

    data = json.loads(src.read_text(encoding='utf-8'))
    models = data.get('models', {})
    out = {'models': {}, 'winner': data.get('winner')}

    for m, info in models.items():
        rows = info.get('per_subject', [])
        acc = [float(r.get('accuracy', 0.0)) for r in rows]
        f1 = [float(r.get('f1', 0.0)) for r in rows]
        auc = [float(r.get('auc', 0.0)) for r in rows]
        out['models'][m] = {
            'accuracy_ci': bootstrap_ci(acc),
            'f1_ci': bootstrap_ci(f1),
            'auc_ci': bootstrap_ci(auc),
            'n_subjects': len(rows),
        }

    op = Path('outputs/cross_subject_ci.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Cross-Subject Bootstrap Confidence Intervals',
        '',
        f"- Winner model: **{out.get('winner')}**",
        '',
        '| Model | Metric | Mean | 95% CI |',
        '|---|---|---:|---:|',
    ]
    for m, info in out['models'].items():
        for metric, key in [('Accuracy', 'accuracy_ci'), ('F1', 'f1_ci'), ('AUC', 'auc_ci')]:
            ci = info.get(key, {})
            lines.append(f"| {m} | {metric} | {ci.get('mean'):.4f} | [{ci.get('ci_low'):.4f}, {ci.get('ci_high'):.4f}] |")

    dp = Path('docs/CROSS_SUBJECT_CI.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')


if __name__ == '__main__':
    main()
