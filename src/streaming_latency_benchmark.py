"""
Benchmark real-time inference latency for chunked EEG windows.
Outputs:
- outputs/streaming_latency.json
- docs/STREAMING_LATENCY.md
"""
from pathlib import Path
import json
import time
import numpy as np

from src.preprocess import build_dataset_from_folder
from src.infer import predict_state


def percentile(arr, q):
    if len(arr) == 0:
        return None
    return float(np.percentile(np.asarray(arr, dtype=float), q))


def main():
    X0, y0 = build_dataset_from_folder('data/relaxed', label=0)
    X1, y1 = build_dataset_from_folder('data/focused', label=1)
    X = np.vstack([X0, X1])
    y = np.concatenate([y0, y1])
    if len(X) == 0:
        raise SystemExit('No samples found in data/relaxed and data/focused')

    # simulate streaming: fixed chunk sequence
    n = min(400, len(X))
    times_ms = []
    probs = []
    t0 = time.perf_counter()
    for i in range(n):
        x = X[i]
        s = time.perf_counter()
        state = predict_state(x)
        p = float(state.get('focused_prob', 0.5))
        e = time.perf_counter()
        times_ms.append((e - s) * 1000.0)
        probs.append(p)
    t1 = time.perf_counter()

    total_s = max(t1 - t0, 1e-9)
    throughput = float(n / total_s)

    out = {
        'n_windows': int(n),
        'latency_ms': {
            'mean': float(np.mean(times_ms)),
            'p50': percentile(times_ms, 50),
            'p95': percentile(times_ms, 95),
            'p99': percentile(times_ms, 99),
            'max': float(np.max(times_ms)),
        },
        'throughput_windows_per_sec': throughput,
        'probability_range': {
            'min': float(np.min(probs)),
            'max': float(np.max(probs)),
            'mean': float(np.mean(probs)),
        },
    }

    op = Path('outputs/streaming_latency.json')
    op.parent.mkdir(exist_ok=True)
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    doc = Path('docs/STREAMING_LATENCY.md')
    doc.write_text(
        '\n'.join([
            '# Streaming Latency Benchmark',
            '',
            f"- Windows benchmarked: **{out['n_windows']}**",
            f"- Mean latency: **{out['latency_ms']['mean']:.3f} ms**",
            f"- P50 latency: **{out['latency_ms']['p50']:.3f} ms**",
            f"- P95 latency: **{out['latency_ms']['p95']:.3f} ms**",
            f"- P99 latency: **{out['latency_ms']['p99']:.3f} ms**",
            f"- Max latency: **{out['latency_ms']['max']:.3f} ms**",
            f"- Throughput: **{out['throughput_windows_per_sec']:.2f} windows/s**",
            '',
            'Raw output: `outputs/streaming_latency.json`',
        ]) + '\n',
        encoding='utf-8'
    )

    print(json.dumps(out, indent=2))
    print('Generated outputs/streaming_latency.json and docs/STREAMING_LATENCY.md')


if __name__ == '__main__':
    main()
