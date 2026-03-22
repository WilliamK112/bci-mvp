# Determinism Audit

- Checked files: **10**
- Existing files: **10**
- Overall: **PASS**

| File | Exists | Determinism Signal | Evidence |
|---|---:|---:|---|
| src/train.py | ✅ | ✅ | \brandom_state\s*=\s*\d+ |
| src/benchmark.py | ✅ | ✅ | \brandom_state\s*=\s*\d+ |
| src/cross_dataset_eval.py | ✅ | ✅ | \brandom_state\s*=\s*\d+ |
| src/cross_subject_eval.py | ✅ | ✅ | \brandom_state\s*=\s*\d+ |
| src/cross_subject_model_benchmark.py | ✅ | ✅ | \brandom_state\s*=\s*\d+ |
| src/bootstrap_ci.py | ✅ | ✅ | \brandom_state\s*=\s*\d+, \bseed\s*=\s*\d+ |
| src/cross_subject_ci.py | ✅ | ✅ | \bseed\s*=\s*\d+ |
| src/permutation_explain.py | ✅ | ✅ | \brandom_state\s*=\s*\d+ |
| src/validate_streaming_latency.py | ✅ | ✅ | \bseed\s*=\s*\d+ |
| src/streaming_stability_test.py | ✅ | ✅ | \bseed\s*=\s*\d+ |

Interpretation:
- PASS means every existing target file has at least one explicit seed/random_state signal.
- This is a static hygiene audit; it complements runtime reproducibility checks.
