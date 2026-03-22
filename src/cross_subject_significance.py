"""
Paired significance-style comparison on LOSO per-subject accuracies.
Input: outputs/cross_subject_model_benchmark.json
Outputs:
- outputs/cross_subject_significance.json
- docs/CROSS_SUBJECT_SIGNIFICANCE.md
"""
from pathlib import Path
import json
import math


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def paired_t_approx(a, b):
    # Normal approximation over paired deltas (small-n caveat documented)
    d = [x - y for x, y in zip(a, b)]
    n = len(d)
    if n < 2:
        return {"n": n, "delta_mean": None, "z": None, "p_two_sided": None}
    mean = sum(d) / n
    var = sum((x - mean) ** 2 for x in d) / (n - 1)
    sd = math.sqrt(max(var, 1e-12))
    se = sd / math.sqrt(n)
    z = mean / se if se > 0 else 0.0
    p = max(0.0, min(1.0, 2 * (1 - norm_cdf(abs(z)))))
    return {"n": n, "delta_mean": mean, "z": z, "p_two_sided": p}


def main():
    src = Path('outputs/cross_subject_model_benchmark.json')
    if not src.exists():
        raise SystemExit('Missing outputs/cross_subject_model_benchmark.json')

    obj = json.loads(src.read_text(encoding='utf-8'))
    models = obj.get('models', {})
    winner = obj.get('winner')
    if not winner or winner not in models:
        raise SystemExit('Winner missing in benchmark file')

    w_rows = sorted(models[winner].get('per_subject', []), key=lambda r: r.get('test_subject'))
    w_acc = [float(r.get('accuracy', 0.0)) for r in w_rows]

    comparisons = []
    for m, info in models.items():
        if m == winner:
            continue
        rows = sorted(info.get('per_subject', []), key=lambda r: r.get('test_subject'))
        acc = [float(r.get('accuracy', 0.0)) for r in rows]
        n = min(len(w_acc), len(acc))
        stat = paired_t_approx(w_acc[:n], acc[:n])
        comparisons.append({
            'winner': winner,
            'challenger': m,
            **stat,
            'winner_mean_acc': float(sum(w_acc[:n]) / n) if n else None,
            'challenger_mean_acc': float(sum(acc[:n]) / n) if n else None,
        })

    out = {
        'winner': winner,
        'method': 'paired delta normal-approx (small-n caution)',
        'comparisons': comparisons,
    }

    op = Path('outputs/cross_subject_significance.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Cross-Subject Significance Checks',
        '',
        f'- Winner: **{winner}**',
        f'- Method: `{out["method"]}`',
        '- Note: subject count is small; use as directional evidence, not strict hypothesis testing.',
        '',
        '| Winner vs Challenger | N | Δmean(acc) | z | p(two-sided) |',
        '|---|---:|---:|---:|---:|',
    ]
    for c in comparisons:
        lines.append(
            f"| {c['winner']} vs {c['challenger']} | {c['n']} | {c['delta_mean']:.4f} | {c['z']:.4f} | {c['p_two_sided']:.4f} |"
        )

    dp = Path('docs/CROSS_SUBJECT_SIGNIFICANCE.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')


if __name__ == '__main__':
    main()
