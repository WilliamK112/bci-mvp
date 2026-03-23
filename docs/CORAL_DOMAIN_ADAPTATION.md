# Cross-Dataset Generalization with Domain Adaptation

| Model | Direction | Method | Accuracy | F1 | AUC |
|---|---|---|---:|---:|---:|
| RF | A -> B | Zero-Shot | 0.7665 | 0.8387 | 0.7293 |
| RF | A -> B | CORAL DA | 0.7582 | 0.8327 | 0.7359 |
| RF | B -> A | Zero-Shot | 0.7092 | 0.8120 | 0.6839 |
| RF | B -> A | CORAL DA | 0.7228 | 0.8204 | 0.6480 |
| SVM | A -> B | Zero-Shot | 0.7115 | 0.7921 | 0.7099 |
| SVM | A -> B | CORAL DA | 0.6456 | 0.7318 | 0.6628 |
| SVM | B -> A | Zero-Shot | 0.7011 | 0.7948 | 0.6920 |
| SVM | B -> A | CORAL DA | 0.6848 | 0.7828 | 0.6625 |