# Reproducibility Check: Release Signature

- Overall: **PASS**
- Method: run `src/final_release_candidate.py` twice and compare SHA256 per key artifact.

| Artifact | Run1 SHA256 | Run2 SHA256 | Stable |
|---|---|---|---:|
| docs/RELEASE_SUMMARY.json | `84416fbed4d5e2e8d5711f91520f7328f66c5abdaf29bd22eab4a4c403e6aaf5` | `84416fbed4d5e2e8d5711f91520f7328f66c5abdaf29bd22eab4a4c403e6aaf5` | ✅ |
| docs/FINAL_RELEASE_CANDIDATE.md | `3b9c259463808e59cc0ab97ea0dd16fed4b03fed8668adb79c7b0642d80eb4fe` | `3b9c259463808e59cc0ab97ea0dd16fed4b03fed8668adb79c7b0642d80eb4fe` | ✅ |
| docs/TECHNICAL_REPORT.md | `93557c6402e45ab915ca9cedb474cd6d90ea56e7b7da1050be99e4db0fbec829` | `93557c6402e45ab915ca9cedb474cd6d90ea56e7b7da1050be99e4db0fbec829` | ✅ |
| docs/RESULTS.md | `b789f3642b1701d4010628935e8a0f19582853a07692a7a3372ec514291a314b` | `b789f3642b1701d4010628935e8a0f19582853a07692a7a3372ec514291a314b` | ✅ |
| docs/ONE_PAGER.md | `661b3faaff1b6f7c6628f6b5f5425f379cb777fc4d34abb4c8ea178c6f5378f5` | `661b3faaff1b6f7c6628f6b5f5425f379cb777fc4d34abb4c8ea178c6f5378f5` | ✅ |
| outputs/cross_subject_model_benchmark.json | `19a2a71872ed8d538fb64e6f6684817aeb441940b9111152b387cb14b09f9762` | `19a2a71872ed8d538fb64e6f6684817aeb441940b9111152b387cb14b09f9762` | ✅ |
| outputs/cross_subject_ci.json | `138d4b71567418245a8d72202b09ae79cd430dbc87b25b3d8a8dd494ab196801` | `138d4b71567418245a8d72202b09ae79cd430dbc87b25b3d8a8dd494ab196801` | ✅ |
| outputs/streaming_latency.json | `54867373b343b0528b2147497fda1879d81cfaa954e3f765ff1cfbf0a341b8e5` | `54867373b343b0528b2147497fda1879d81cfaa954e3f765ff1cfbf0a341b8e5` | ✅ |
| outputs/streaming_stability.json | `574be7167871df77767cab0771eeeff722293bd4b2058d4c072bd725db16a5d1` | `574be7167871df77767cab0771eeeff722293bd4b2058d4c072bd725db16a5d1` | ✅ |
