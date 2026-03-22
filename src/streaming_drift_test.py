"""
Streaming drift resilience test.
Simulates gradual feature scaling drift and tracks prediction stability.
Outputs:
- outputs/streaming_drift.json
- docs/STREAMING_DRIFT.md
"""
from pathlib import Path
import json
import numpy as np

from src.preprocess import build_dataset_from_folder
from src.infer import predict_state


def main():
    X0, _ = build_dataset_from_folder('data/relaxed', label=0)
    X1, _ = build_dataset_from_folder('data/focused', label=1)
    X = np.vstack([X0, X1])
    if len(X) == 0:
        raise SystemExit('No samples found for streaming drift test')

    n = min(400, len(X))
    base_probs = []
    drift_probs = []

    for i in range(n):
        x = X[i]
        b = float(predict_state(x).get('focused_prob', 0.5))
        # gradual multiplicative drift: 1.00 -> 1.20
        scale = 1.0 + 0.20 * (i / max(1, n - 1))
        xd = x * scale
        d = float(predict_state(xd).get('focused_prob', 0.5))
        base_probs.append(b)
        drift_probs.append(d)

    base = np.array(base_probs, dtype=float)
    drift = np.array(drift_probs, dtype=float)
    delta = np.abs(drift - base)

    out = {
        'n_windows': int(n),
        'drift_scale_start': 1.0,
        'drift_scale_end': 1.2,
        'mean_abs_prob_shift': float(delta.mean()),
        'p95_abs_prob_shift': float(np.percentile(delta, 95)),
        'max_abs_prob_shift': float(delta.max()),
        'pass': bool(np.percentile(delta, 95) <= 0.30),
    }

    op = Path('outputs/streaming_drift.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Streaming Drift Resilience',
        '',
        f"- Windows: **{out['n_windows']}**",
        f"- Drift scale: **{out['drift_scale_start']} -> {out['drift_scale_end']}**",
        f"- Mean |Δprob|: **{out['mean_abs_prob_shift']:.4f}**",
        f"- P95 |Δprob|: **{out['p95_abs_prob_shift']:.4f}**",
        f"- Max |Δprob|: **{out['max_abs_prob_shift']:.4f}**",
        f"- Gate (P95 <= 0.30): **{'PASS' if out['pass'] else 'FAIL'}**",
    ]
    dp = Path('docs/STREAMING_DRIFT.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')

    if not out['pass']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
