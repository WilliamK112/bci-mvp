# BCI MVP Progress Log

## 2026-03-22 13:59:14 UTC — Added continuous progress logging utility

Created `src/progress_log.py` to append UTC-stamped progress entries and sync latest update into README.

## 2026-03-22 13:59:57 UTC — Generated unified technical report

Added `src/build_report.py` to aggregate benchmark, cross-dataset, and explainability outputs into `docs/TECHNICAL_REPORT.md`.

## 2026-03-22 14:02:11 UTC — Upgraded real-time streaming stability

Added EMA+hysteresis streaming filter (`src/streaming.py`), integrated in `app/streaming_demo.py`, and added unit test `tests/test_streaming_unittest.py`.

## 2026-03-22 14:03:58 UTC — Added stronger nonlinear baseline for benchmark depth

Implemented `src/deep_baseline.py` (MLP) and `src/merge_results.py` to produce unified model comparison outputs.

## 2026-03-22 14:06:09 UTC — Added unified multi-model visualization

Implemented `src/plot_all_models.py` to render ACC/F1/AUC comparison chart from `outputs/all_model_results.csv` into `assets/all_model_comparison.svg`.
