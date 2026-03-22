# Cross-Dataset Bidirectional Validation

- Overall: **PASS**

| Gate | Result | Observed |
|---|---:|---:|
| A->B RF accuracy >= 0.50 | ✅ | 0.7335 |
| B->A RF accuracy >= 0.50 | ✅ | 0.5136 |
| A->B RF AUC >= 0.60 | ✅ | 0.6713 |
| B->A RF AUC >= 0.60 | ✅ | 0.7034 |
| Symmetry gap accuracy <= 0.25 | ✅ | 0.2199 |
| Symmetry gap f1 <= 0.35 | ✅ | 0.3242 |
| Symmetry gap auc <= 0.20 | ✅ | 0.0321 |
