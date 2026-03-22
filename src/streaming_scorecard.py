"""
Aggregate streaming latency/stability/drift into one scorecard.
Outputs:
- outputs/streaming_scorecard.json
- docs/STREAMING_SCORECARD.md
"""
from pathlib import Path
import json


def read_json(path):
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def main():
    lat = read_json('outputs/streaming_latency.json') or {}
    stb = read_json('outputs/streaming_stability.json') or {}
    drf = read_json('outputs/streaming_drift.json') or {}

    p95 = float((lat.get('latency_ms') or {}).get('p95', 1e9))
    tps = float(lat.get('throughput_windows_per_sec', 0.0))
    stability_pass = bool(stb.get('pass', False))
    drift_p95 = float(drf.get('p95_abs_prob_shift', 1e9))

    gates = {
        'latency_p95_le_120ms': p95 <= 120.0,
        'throughput_ge_8': tps >= 8.0,
        'stability_pass': stability_pass,
        'drift_p95_le_0_30': drift_p95 <= 0.30,
    }

    overall = all(gates.values())
    score = sum(1 for v in gates.values() if v) / len(gates)

    out = {
        'overall_pass': overall,
        'score': score,
        'metrics': {
            'latency_p95_ms': p95,
            'throughput_windows_per_sec': tps,
            'stability_pass': stability_pass,
            'drift_p95_abs_prob_shift': drift_p95,
        },
        'gates': gates,
    }

    op = Path('outputs/streaming_scorecard.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Streaming Scorecard',
        '',
        f"- Overall: **{'PASS' if overall else 'FAIL'}**",
        f"- Score: **{score:.2f}**",
        '',
        '| Gate | Result |',
        '|---|---:|',
    ]
    for k, v in gates.items():
        lines.append(f"| {k} | {'✅' if v else '❌'} |")

    lines += [
        '',
        f"- Latency p95: **{p95:.3f} ms**",
        f"- Throughput: **{tps:.2f} windows/s**",
        f"- Drift p95 |Δprob|: **{drift_p95:.4f}**",
    ]

    dp = Path('docs/STREAMING_SCORECARD.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')

    if not overall:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
