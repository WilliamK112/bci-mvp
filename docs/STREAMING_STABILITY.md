# Streaming Stability Stress Test

- Overall: **PASS**
- Pass criteria per tier: `error_rate == 0` and `p95_ms <= 150`

| Tier | Windows | Burst | Error Rate | Mean ms | P95 ms | Max ms |
|---|---:|---:|---:|---:|---:|---:|
| light | 200 | 1 | 0.0000 | 83.191 | 100.138 | 955.905 |
| moderate | 300 | 4 | 0.0000 | 84.444 | 106.631 | 924.704 |
| burst | 400 | 8 | 0.0000 | 79.286 | 99.520 | 340.754 |
