# Results

Generated: 2026-03-22 15:58 UTC

## Model Comparison

| Model | Accuracy | F1 | AUC |
|---|---:|---:|---:|
| RF | 0.842 | 0.836 | 0.901 |
| SVM | 0.818 | 0.812 | 0.874 |

## Cross-Dataset

- Train: **dataset_a**
- Test: **dataset_b**

| Model | Accuracy | F1 | AUC |
|---|---:|---:|---:|
| RF | 0.741 | 0.732 | 0.801 |
| SVM | 0.703 | 0.695 | 0.766 |

## Calibration & Uncertainty

- Brier score: n/a
- Bootstrap CI: n/a

## Robustness

No `outputs/robustness_results.json` found.

## Visuals

- ![All Models](../assets/all_model_comparison.svg)
- ![Cross Matrix](../assets/cross_dataset_matrix.svg)
- ![Calibration](../assets/calibration_curve.svg)
- ![Robustness](../assets/robustness_accuracy.svg)
