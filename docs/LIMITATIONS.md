# Limitations Report

Generated: 2026-03-22 16:52 UTC

## Known Limitations
- Labels in current public-data bootstrap are pragmatic task-mapping, not clinical ground truth.
- Binary relaxed/focused framing does not capture full cognitive-state spectrum.
- Current feature representation is handcrafted bandpower; end-to-end deep temporal features are not fully explored.
- Cross-dataset evidence is still constrained by small public bootstrap subset size.

## Robustness Caveat
- Noise perturbation can significantly reduce performance; refer to `outputs/robustness_results.json`.

## Generalization Caveat
- Cross-dataset transfer quality depends strongly on acquisition/protocol alignment.

## Mitigation Plan
- Expand real labeled datasets and subject diversity.
- Add stricter cross-session/cross-subject protocols.
- Introduce stronger deep baselines (e.g., EEGNet).
- Add domain adaptation / calibration by device/session.
