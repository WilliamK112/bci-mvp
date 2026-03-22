# BCI MVP Technical Report

Generated: 2026-03-22 14:26 UTC

## 1) Benchmark Summary

| Model | Accuracy | F1 | AUC |
|---|---:|---:|---:|
| RF | 0.842 | 0.836 | 0.901 |
| SVM | 0.818 | 0.812 | 0.874 |

## 2) Unified Model Table

| Model | Accuracy | F1 | AUC |
|---|---:|---:|---:|
| RF | 0.842 | 0.836 | 0.901 |
| SVM | 0.818 | 0.812 | 0.874 |

## 3) Cross-Dataset Generalization

- Train dataset: **dataset_a**
- Test dataset: **dataset_b**
- Train samples: 1200
- Test samples: 900

| Model | Accuracy | F1 | AUC |
|---|---:|---:|---:|
| RF | 0.741 | 0.732 | 0.801 |
| SVM | 0.703 | 0.695 | 0.766 |

## 4) Explainability Summary

No `outputs/permutation_importance_summary.json` found.

## 5) Probability Calibration

No `outputs/calibration_results.json` found.

## 6) Robustness under Perturbations

No `outputs/robustness_results.json` found.

## 7) Visual Artifacts

- ![All Model](../assets/all_model_comparison.svg)
- ![Cross Matrix](../assets/cross_dataset_matrix.svg)
- ![Calibration](../assets/calibration_curve.svg)
- ![Robustness](../assets/robustness_accuracy.svg)

## 8) Release Readiness

- Pipeline status: `docs/PIPELINE_STATUS.md`
- Artifact validation: `outputs/artifact_validation_report.txt`
- Model card: `docs/MODEL_CARD.md`
