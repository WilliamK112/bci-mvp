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

## 2026-03-22 14:08:05 UTC — Prepared Hugging Face Space one-click deployment

Added root app entrypoint and .streamlit config for Space runtime compatibility.

## 2026-03-22 14:09:52 UTC — Added cross-dataset matrix evaluator

Implemented `src/cross_dataset_matrix.py` to run all dataset pair evaluations and export `outputs/cross_dataset_matrix.json`.

## 2026-03-22 14:12:02 UTC — Added cross-dataset heatmap visualization

Implemented `src/plot_cross_matrix.py` and generated `assets/cross_dataset_matrix.svg` for matrix-style generalization reporting.

## 2026-03-22 14:13:58 UTC — Added auto-generated public release pack

Implemented `src/generate_release_pack.py` to create EN/ZH release notes and platform post drafts under `docs/release/`.

## 2026-03-22 14:15:55 UTC — Added model card generation for public trust and deployment

Implemented `src/generate_model_card.py` to create `docs/MODEL_CARD.md` and HF Space README metadata scaffold.

## 2026-03-22 14:17:54 UTC — Added artifact validation for release quality gate

Implemented `src/validate_artifacts.py` to check critical outputs/docs and emit `outputs/artifact_validation_report.txt`.

## 2026-03-22 14:19:52 UTC — Added one-command full pipeline orchestrator

Implemented `src/run_full_pipeline.py` to chain benchmark/report/release/validation steps and emit `outputs/pipeline_manifest.json`.

## 2026-03-22 14:22:07 UTC — Added probability calibration evaluation

Implemented calibration metrics (`brier_score`) and reliability visualization scripts (`src/calibration_eval.py`, `src/plot_calibration.py`).

## 2026-03-22 14:24:08 UTC — Added robustness stress testing pipeline

Implemented perturbation-based robustness evaluation (`src/robustness_eval.py`) and visualization (`src/plot_robustness.py`).

## 2026-03-22 14:26:16 UTC — Upgraded technical report + added release readiness dashboard

Extended `src/build_report.py` with calibration/robustness sections and added `src/release_readiness.py` to generate `docs/RELEASE_READINESS.md`.

## 2026-03-22 14:27:49 UTC — Added HF Space readiness checker

Implemented `src/hf_space_readiness.py` to generate `docs/HF_SPACE_READINESS.md` with deployment checklist and score.

## 2026-03-22 14:29:53 UTC — Added model leaderboard generation

Implemented `src/leaderboard.py` to rank models by accuracy/AUC and generate `docs/MODEL_LEADERBOARD.md`.

## 2026-03-22 14:31:47 UTC — Added auto changelog generation from git history

Implemented `src/changelog_from_git.py` to produce `docs/CHANGELOG_AUTO.md` for transparent project evolution tracking.

## 2026-03-22 14:34:04 UTC — Added feature ablation study pipeline

Implemented band-level ablation evaluation (`src/ablation_eval.py`) and visualization (`src/plot_ablation.py`) to quantify feature-group contributions.

## 2026-03-22 14:35:50 UTC — Added auto figure gallery generation

Implemented `src/generate_figure_gallery.py` to auto-build `docs/FIGURE_GALLERY.md` from all assets for easier release packaging and review.

## 2026-03-22 14:37:57 UTC — Added docs bundle index + integrated full pipeline doc refresh

Implemented `src/update_docs_bundle.py` and integrated it into `src/run_full_pipeline.py` with leaderboard/gallery/changelog refresh steps.

## 2026-03-22 14:39:53 UTC — Added readiness status badges

Implemented `src/generate_status_badges.py` to produce local SVG badges for release and HF Space readiness, embedded in README.
