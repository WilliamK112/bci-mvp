# Results

Generated: 2026-03-22 16:41 UTC

## Model Comparison

| Model | Accuracy | F1 | AUC |
|---|---:|---:|---:|
| SVM | 0.8435374149659864 | 0.8855721393034826 | 0.8928872053872055 |
| RF | 0.8231292517006803 | 0.8773584905660378 | 0.8470117845117845 |

## Cross-Dataset

- Train: **dataset_a**
- Test: **dataset_b**

| Model | Accuracy | F1 | AUC |
|---|---:|---:|---:|
| RF | 0.741 | 0.732 | 0.801 |
| SVM | 0.703 | 0.695 | 0.766 |

## Calibration & Uncertainty

- Brier score: **0.1400096513605442**
- Accuracy CI95: [0.7619047619047619, 0.8775510204081632]
- F1 CI95: [0.8304644412191583, 0.9199156985278698]
- AUC CI95: [0.7620890335392764, 0.9069376262459021]

## Robustness

| Setting | Accuracy | F1 |
|---|---:|---:|
| clean | 0.8231292517006803 | 0.8773584905660378 |
| noise_0.05 | 0.6802721088435374 | 0.8081632653061225 |
| noise_0.10 | 0.6802721088435374 | 0.8081632653061225 |
| dropout_0.05 | 0.8231292517006803 | 0.8773584905660378 |
| dropout_0.10 | 0.8231292517006803 | 0.8773584905660378 |
| mixed | 0.673469387755102 | 0.8032786885245902 |

## Visuals

- ![All Models](../assets/all_model_comparison.svg)
- ![Cross Matrix](../assets/cross_dataset_matrix.svg)
- ![Calibration](../assets/calibration_curve.svg)
- ![Robustness](../assets/robustness_accuracy.svg)
