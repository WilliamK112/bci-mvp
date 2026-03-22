# BCI MVP Risk Register

Generated: 2026-03-22 14:43 UTC

| Risk | Description | Severity | Mitigation |
|---|---|---|---|
| Dataset shift | Cross-dataset generalization drops on unseen acquisition setups | High | Cross-dataset matrix eval + report confidence intervals |
| Probability miscalibration | Predicted probabilities may be over/under-confident | Medium | Run calibration_eval + monitor Brier score |
| Noise sensitivity | Performance degradation under perturbations | Medium | Run robustness_eval and include robustness chart |
| Feature dependency bias | Overreliance on specific EEG band/channel | Medium | Run ablation + permutation explainability |
| Reproducibility drift | Outputs diverge across environments | High | Use run_full_pipeline + validation + Docker + CI |
| Demo credibility | Placeholder/demo figures mistaken as final evidence | Medium | Label placeholders and prioritize real-data reruns |
