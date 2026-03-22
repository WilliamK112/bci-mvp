# Streaming Latency Validation

- Source: `outputs/streaming_latency.json`
- Overall: **PASS**

| Gate | Result | Observed |
|---|---:|---:|
| mean_latency_ms <= 100 | ✅ | 78.6370 |
| p95_latency_ms <= 120 | ✅ | 99.9906 |
| p99_latency_ms <= 180 | ✅ | 112.2772 |
| throughput >= 8 windows/s | ✅ | 12.7165 |
