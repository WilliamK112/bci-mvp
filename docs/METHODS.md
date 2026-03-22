# Methods (Paper-Style)

## 1. Problem Setup
We study binary EEG state classification from short windows:
- label 0: relaxed
- label 1: focused

Given preprocessed epoch feature vector $\mathbf{z}\in\mathbb{R}^{d}$, learn
$\hat{p}=P(y=1\mid\mathbf{z})$ and decision $\hat{y}=\mathbb{1}[\hat{p}\ge0.5]$.

## 2. Signal Processing Pipeline
1. Load EDF and select EEG channels
2. Band-pass filter (default 1–40 Hz)
3. Resample to unified rate (default 128 Hz)
4. Epoch with fixed window and overlap
5. Extract bandpower via Welch PSD

## 3. Feature Representation
For each channel and each band (delta/theta/alpha/beta), compute integrated PSD bandpower.
All channel-band values are concatenated into a tabular feature vector.

## 4. Models
Primary baselines:
- RandomForest (class_weight balanced)
- SVM (RBF kernel)
- MLP baseline

## 5. Streaming Stabilization
Raw frame-level probability is stabilized by:
- EMA smoothing
- Hysteresis thresholds (high/low)
This reduces oscillation around a single threshold.

## 6. Evaluation Protocol
- In-distribution split: stratified train/test
- Cross-dataset evaluation: train on dataset A, test on B
- Matrix evaluation for multiple datasets

Metrics:
- Accuracy, F1, AUC
- Calibration via Brier score
- Robustness via perturbation tests
- Uncertainty via bootstrap confidence intervals

## 7. Explainability
- Feature importance aggregation by channel/band
- Permutation importance
- Band ablation impact

## 8. Reproducibility
- CI checks
- Dockerized runtime
- One-command full pipeline
- Release candidate report and readiness scorecards
