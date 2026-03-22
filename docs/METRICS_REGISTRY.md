# Metrics Registry

Generated: 2026-03-22 16:48 UTC

| Metric | Definition | Source Artifact(s) |
|---|---|---|
| Accuracy | Classification correctness ratio | `outputs/benchmark_results.csv; outputs/all_model_results.csv` |
| F1 | Harmonic mean of precision/recall | `outputs/benchmark_results.csv; outputs/all_model_results.csv` |
| AUC | ROC area under curve | `outputs/benchmark_results.csv; outputs/bootstrap_ci_results.json` |
| Brier score | Probability calibration error (lower is better) | `outputs/calibration_results.json` |
| Robustness Accuracy | Accuracy under synthetic perturbations | `outputs/robustness_results.json` |
| Ablation Delta | Performance change when dropping band groups | `outputs/ablation_results.json` |
| Bootstrap CI95 | Empirical uncertainty interval from resampling | `outputs/bootstrap_ci_results.json` |
| Cross-dataset score | Generalization from train dataset A to test dataset B | `outputs/cross_dataset_results.json; outputs/cross_dataset_matrix.json` |
