# BCI MVP Technical Report

Generated: 2026-03-22 13:59 UTC

## 1) Benchmark Summary

| Model | Accuracy | F1 | AUC |
|---|---:|---:|---:|
| RF | 0.842 | 0.836 | 0.901 |
| SVM | 0.818 | 0.812 | 0.874 |

## 2) Cross-Dataset Generalization

- Train dataset: **dataset_a**
- Test dataset: **dataset_b**
- Train samples: 1200
- Test samples: 900

| Model | Accuracy | F1 | AUC |
|---|---:|---:|---:|
| RF | 0.741 | 0.732 | 0.801 |
| SVM | 0.703 | 0.695 | 0.766 |

## 3) Explainability Summary

No `outputs/permutation_importance_summary.json` found.

## 4) Visual Artifacts

- ![Benchmark](../assets/benchmark_scores.svg)
- ![Cross Dataset](../assets/cross_dataset_scores.svg)
