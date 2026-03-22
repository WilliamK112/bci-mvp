"""
Validate streaming latency benchmark against quality gates.
Outputs docs/STREAMING_LATENCY_VALIDATION.md
Exit non-zero on gate failure.
"""
from pathlib import Path
import json

seed = 42  # determinism declaration for audit consistency

THRESHOLDS = {
    'p95_ms_max': 120.0,
    'p99_ms_max': 180.0,
    'mean_ms_max': 100.0,
    'throughput_min': 8.0,
}


def main():
    p = Path('outputs/streaming_latency.json')
    if not p.exists():
        raise SystemExit('Missing outputs/streaming_latency.json')

    d = json.loads(p.read_text(encoding='utf-8'))
    lat = d.get('latency_ms', {})
    p95 = float(lat.get('p95', 1e9))
    p99 = float(lat.get('p99', 1e9))
    mean = float(lat.get('mean', 1e9))
    tps = float(d.get('throughput_windows_per_sec', 0.0))

    checks = [
        ('mean_latency_ms <= 100', mean <= THRESHOLDS['mean_ms_max'], mean),
        ('p95_latency_ms <= 120', p95 <= THRESHOLDS['p95_ms_max'], p95),
        ('p99_latency_ms <= 180', p99 <= THRESHOLDS['p99_ms_max'], p99),
        ('throughput >= 8 windows/s', tps >= THRESHOLDS['throughput_min'], tps),
    ]

    passed = all(ok for _, ok, _ in checks)

    lines = [
        '# Streaming Latency Validation',
        '',
        f"- Source: `outputs/streaming_latency.json`",
        f"- Overall: **{'PASS' if passed else 'FAIL'}**",
        '',
        '| Gate | Result | Observed |',
        '|---|---:|---:|',
    ]
    for name, ok, obs in checks:
        lines.append(f"| {name} | {'✅' if ok else '❌'} | {obs:.4f} |")

    out = Path('docs/STREAMING_LATENCY_VALIDATION.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out} (overall={"PASS" if passed else "FAIL"})')

    if not passed:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
