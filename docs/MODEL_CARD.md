# Model Card — BCI MVP Classifier

Generated: 2026-03-22 14:15 UTC

## Model Details
- Type: Classical ML baseline (RF/SVM/MLP pipeline variants)
- Task: Binary EEG state classification (`relaxed` vs `focused`)
- Input: 32-dim handcrafted EEG feature vector (bandpower by channel)
- Output: Class label + probability

## Intended Use
- Educational demos
- Benchmarking preprocessing and inference pipelines
- Prototype validation before real-time hardware integration

## Performance
- Cross-dataset RF accuracy: 0.741
- Cross-dataset RF f1: 0.732
- Cross-dataset RF auc: 0.801

## Explainability
- Explainability summary pending.

## Limitations
- Not validated for clinical/medical diagnosis.
- Sensitive to dataset shift and recording setup differences.
- Current public figures may include demo placeholders until full real-data runs complete.

## Ethical Considerations
- Do not use as medical advice.
- Respect participant consent and data governance.
- Evaluate fairness across populations and devices before deployment.
