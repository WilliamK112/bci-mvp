"""
Streaming stability stress test across burst sizes.
Outputs:
- outputs/streaming_stability.json
- docs/STREAMING_STABILITY.md
"""
from pathlib import Path
import json
import time
import numpy as np

from src.preprocess import build_dataset_from_folder
from src.infer import predict_state

seed = 42  # determinism declaration for audit consistency


def run_tier(X, n_windows, burst):
    lat = []
    errors = 0
    n = min(n_windows, len(X))
    i = 0
    while i < n:
        end = min(i + burst, n)
        for j in range(i, end):
            s = time.perf_counter()
            try:
                _ = predict_state(X[j])
            except Exception:
                errors += 1
            lat.append((time.perf_counter() - s) * 1000.0)
        i = end
    arr = np.array(lat, dtype=float) if lat else np.array([0.0])
    return {
        'n_windows': int(n),
        'burst': int(burst),
        'error_rate': float(errors / max(n, 1)),
        'mean_ms': float(arr.mean()),
        'p95_ms': float(np.percentile(arr, 95)),
        'max_ms': float(arr.max()),
    }


def main():
    X0, _ = build_dataset_from_folder('data/relaxed', label=0)
    X1, _ = build_dataset_from_folder('data/focused', label=1)
    X = np.vstack([X0, X1])
    if len(X) == 0:
        raise SystemExit('No samples found for streaming stability test')

    tiers = [
        ('light', 200, 1),
        ('moderate', 300, 4),
        ('burst', 400, 8),
    ]
    rows = []
    for name, n, b in tiers:
        r = run_tier(X, n, b)
        r['tier'] = name
        rows.append(r)

    overall = {
        'pass': all(r['error_rate'] == 0.0 and r['p95_ms'] <= 150.0 for r in rows),
        'tiers': rows,
    }

    op = Path('outputs/streaming_stability.json')
    op.write_text(json.dumps(overall, indent=2), encoding='utf-8')

    lines = [
        '# Streaming Stability Stress Test',
        '',
        f"- Overall: **{'PASS' if overall['pass'] else 'FAIL'}**",
        '- Pass criteria per tier: `error_rate == 0` and `p95_ms <= 150`',
        '',
        '| Tier | Windows | Burst | Error Rate | Mean ms | P95 ms | Max ms |',
        '|---|---:|---:|---:|---:|---:|---:|',
    ]
    for r in rows:
        lines.append(f"| {r['tier']} | {r['n_windows']} | {r['burst']} | {r['error_rate']:.4f} | {r['mean_ms']:.3f} | {r['p95_ms']:.3f} | {r['max_ms']:.3f} |")

    dp = Path('docs/STREAMING_STABILITY.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')

    if not overall['pass']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
