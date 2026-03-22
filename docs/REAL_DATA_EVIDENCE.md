# Real Data Evidence

This project uses real EEG EDF recordings present in the repository workspace and in evaluation runs.

- Relaxed EDF files: **4**
- Focused EDF files: **4**
- Relaxed subjects: **[1, 2]**
- Focused subjects: **[1, 2]**
- Shared subjects across classes: **[1, 2]**

## Per-subject file counts (shared subjects)

| Subject | Relaxed files | Focused files |
|---:|---:|---:|
| 1 | 2 | 2 |
| 2 | 2 | 2 |

## Evidence trail in pipelines
- Cross-subject LOSO benchmark consumes EDF-derived feature matrices.
- Cross-dataset bidirectional evaluation is computed from dataset_a/dataset_b EDF splits.
- Streaming latency/stability/drift tests run inference over EDF-derived windows.

## Note
- This report confirms on-disk real EDF assets and subject coverage; it does not claim clinical validity.
