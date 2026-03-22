# Real-Data Gap Report

Generated: 2026-03-22 15:03 UTC

| Item | Status | Path |
|---|---|---|
| Benchmark results | READY | `outputs/benchmark_results.csv` |
| Unified model results | READY | `outputs/all_model_results.csv` |
| Cross-dataset single-pair results | READY | `outputs/cross_dataset_results.json` |
| Cross-dataset matrix results | READY | `outputs/cross_dataset_matrix.json` |
| Permutation explainability summary | MISSING_REAL_RUN | `outputs/permutation_importance_summary.json` |
| Calibration results | MISSING_REAL_RUN | `outputs/calibration_results.json` |
| Robustness results | MISSING_REAL_RUN | `outputs/robustness_results.json` |
| Ablation results | MISSING_REAL_RUN | `outputs/ablation_results.json` |
| Bootstrap CI results | MISSING_REAL_RUN | `outputs/bootstrap_ci_results.json` |

**Coverage:** 4/9

## Action Plan
1. Place real EDF data into required folders.
2. Run `python src/run_full_pipeline.py`.
3. Re-run `python src/final_release_candidate.py` and `python src/release_readiness.py`.
