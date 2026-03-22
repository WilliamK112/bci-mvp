---
title: BCI MVP Demo
emoji: 🧠
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 8000
pinned: false
---

# BCI MVP (Low-Hardware Personal Project)

A lightweight brain-computer interface MVP focused on EEG preprocessing, state classification (relaxed vs focused), API serving, and interactive visualization.

## Features
- EDF EEG loading and preprocessing (MNE)
- Band-power feature extraction (delta/theta/alpha/beta)
- RandomForest baseline with CV + test metrics
- FastAPI inference service
- Streamlit dashboard demo

## Project Structure
```text
bci-mvp/
  src/                # preprocessing, training, inference, data checks
  api/                # FastAPI app
  app/                # Streamlit app
  data/relaxed/       # place relaxed EDF files
  data/focused/       # place focused EDF files
  outputs/            # model + metrics
```

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/check_data.py
python src/train.py

uvicorn api.main:app --reload --port 8000
streamlit run app/dashboard.py
```

## Data Notes
Use public datasets such as:
- PhysioNet EEGMMI
- BCI Competition IV
- Sleep-EDF (for signal pipeline validation)

## Publish Plan
- Code: GitHub
- Live demo: Hugging Face Spaces (Streamlit)
- Video demo: Bilibili / YouTube
- Community posts: Reddit / Zhihu


## Impressive Upgrades (In Progress)
- ✅ Multi-model benchmarking (`src/benchmark.py`)
- ✅ Simulated real-time streaming demo (`app/streaming_demo.py`)
- ⏳ Cross-dataset evaluation
- ⏳ Explainability (SHAP)
- ⏳ Hugging Face Spaces deployment

## Benchmark Run
```bash
python src/benchmark.py
```

## Streaming Demo Run
```bash
streamlit run app/streaming_demo.py
```


## Cross-Dataset Evaluation (Train A -> Test B)
```bash
python src/cross_dataset_eval.py --train dataset_a --test dataset_b
```
Expected layout:
```text
data/
  dataset_a/{relaxed,focused}/*.edf
  dataset_b/{relaxed,focused}/*.edf
```
Results are saved to `outputs/cross_dataset_results.json`.

## Hugging Face Spaces (Public Demo)
- App file: `app/hf_app.py`
- Deployment notes: `app/README_SPACES.md`


## Explainability
```bash
python src/explainability.py
```
Generates:
- `outputs/feature_importance_detailed.csv`
- `outputs/feature_importance_by_band.csv`
- `outputs/feature_importance_by_channel.csv`

## Reproducibility & Engineering
- Dockerized API service (`Dockerfile`)
- CI checks (`.github/workflows/ci.yml`)
- Makefile commands for consistent local runs


## Publication-Ready Visuals
Generate benchmark figures for README/posts:
```bash
python src/plot_results.py
```
Outputs:
- `outputs/benchmark_scores.png`
- `outputs/cross_dataset_scores.png` (if cross-dataset json exists)


## Result Figures

### Benchmark Comparison
![Benchmark Scores](assets/benchmark_scores.svg)

### Cross-Dataset Generalization (Train A -> Test B)
![Cross-Dataset Scores](assets/cross_dataset_scores.svg)

> Note: current figures are demo placeholders. Replace with real experiment outputs after running full evaluations.


## Model-Agnostic Explainability (Permutation Importance)
```bash
python src/permutation_explain.py
```
Outputs:
- `outputs/permutation_importance_detailed.csv`
- `outputs/permutation_importance_by_band.csv`
- `outputs/permutation_importance_by_channel.csv`
- `outputs/permutation_importance_summary.json`


<!-- LATEST_PROGRESS_START -->
## Latest Progress
- 2026-03-22 15:26:25 UTC — Added report consistency checker for documentation quality
- Full log: `logs/progress.md`
<!-- LATEST_PROGRESS_END -->


## Streaming Stability Upgrade
Added `src/streaming.py`:
- EMA smoothing for focused probability
- Hysteresis thresholds for stable state transitions

This reduces flicker in real-time prediction UIs.


## Stronger Nonlinear Baseline
Added `src/deep_baseline.py` (MLP baseline) and `src/merge_results.py` to combine classical + deep results.

Run:
```bash
python src/deep_baseline.py
python src/merge_results.py
```


### Unified Model Comparison
![All Model Comparison](assets/all_model_comparison.svg)

Generate it with:
```bash
python src/merge_results.py
python src/plot_all_models.py
```


## Cross-Dataset Matrix Evaluation
For multiple datasets, run all train→test pairs:
```bash
python src/cross_dataset_matrix.py
```
Output: `outputs/cross_dataset_matrix.json`


### Cross-Dataset Matrix Heatmap
![Cross Dataset Matrix](assets/cross_dataset_matrix.svg)

Generate:
```bash
python src/cross_dataset_matrix.py
python src/plot_cross_matrix.py
```


## Release Pack (Auto-generated)
Generate platform-ready announcement drafts:
```bash
python src/generate_release_pack.py
```
Outputs:
- `docs/release/release_en.md`
- `docs/release/release_zh.md`
- `docs/release/reddit_post.md`
- `docs/release/bilibili_post.md`


## Model Card & HF Space Metadata
Generate public-facing model docs:
```bash
python src/generate_model_card.py
```
Outputs:
- `docs/MODEL_CARD.md`
- `docs/HF_SPACE_README.md`


## Artifact Validation (Repro Readiness)
Run a quick consistency check before public release:
```bash
python src/validate_artifacts.py
```
Output:
- `outputs/artifact_validation_report.txt`


## One-Command Full Pipeline
Run the full reproducible workflow and generate a run manifest:
```bash
python src/run_full_pipeline.py
# or
make full
```
Output:
- `outputs/pipeline_manifest.json`


## Probability Calibration
Evaluate reliability of predicted probabilities:
```bash
python src/calibration_eval.py
python src/plot_calibration.py
```
Outputs:
- `outputs/calibration_results.json`
- `assets/calibration_curve.svg`


## Robustness Evaluation
Stress-test model under synthetic perturbations (noise/dropout):
```bash
python src/robustness_eval.py
python src/plot_robustness.py
```
Outputs:
- `outputs/robustness_results.json`
- `assets/robustness_accuracy.svg`


## Release Readiness Dashboard
Generate release readiness checklist:
```bash
python src/release_readiness.py
```
Output:
- `docs/RELEASE_READINESS.md`


## HF Space Readiness Check
```bash
python src/hf_space_readiness.py
```
Output:
- `docs/HF_SPACE_READINESS.md`


## Model Leaderboard
Generate ranked comparison table:
```bash
python src/leaderboard.py
```
Output:
- `docs/MODEL_LEADERBOARD.md`


## Auto Changelog
Generate changelog from recent git commits:
```bash
python src/changelog_from_git.py
```
Output:
- `docs/CHANGELOG_AUTO.md`


## Ablation Study
Quantify contribution of each EEG band by zeroing it out:
```bash
python src/ablation_eval.py
python src/plot_ablation.py
```
Outputs:
- `outputs/ablation_results.json`
- `assets/ablation_accuracy.svg`


## Figure Gallery
Generate a browsable gallery of all visual artifacts:
```bash
python src/generate_figure_gallery.py
```
Output:
- `docs/FIGURE_GALLERY.md`


## Docs Bundle Index
Generate a single navigation page for all major docs:
```bash
python src/update_docs_bundle.py
```
Output:
- `docs/DOCS_BUNDLE_INDEX.md`


## Status Badges (Local)
![Release Readiness](assets/badge_release_readiness.svg)
![HF Readiness](assets/badge_hf_readiness.svg)

Refresh badges:
```bash
python src/generate_status_badges.py
```


## Command Center
Generate a single command reference page:
```bash
python src/command_center.py
```
Output:
- `docs/COMMAND_CENTER.md`


## Risk Register
Generate technical risk and mitigation table:
```bash
python src/risk_register.py
```
Output:
- `docs/RISK_REGISTER.md`


## Final Release Candidate
Generate one-shot release bundle summary:
```bash
python src/final_release_candidate.py
```
Output:
- `docs/FINAL_RELEASE_CANDIDATE.md`

- Release readiness now includes risk-register coverage (`docs/RISK_REGISTER.md`).


## Executive Summary
Generate a management-level snapshot:
```bash
python src/executive_summary.py
```
Output:
- `docs/EXECUTIVE_SUMMARY.md`


## Next Milestones
Generate a focused next-step execution plan:
```bash
python src/next_milestones.py
```
Output:
- `docs/NEXT_MILESTONES.md`


## Bootstrap Confidence Intervals
Estimate uncertainty of key metrics:
```bash
python src/bootstrap_ci.py
```
Output:
- `outputs/bootstrap_ci_results.json`

- Release readiness now includes bootstrap CI artifact coverage (`outputs/bootstrap_ci_results.json`).


## Reproducibility Snapshot
Generate environment + file-hash snapshot:
```bash
python src/repro_snapshot.py
```
Output:
- `docs/REPRO_SNAPSHOT.md`


## HF Publish Helper
Generate exact commands for Hugging Face Space publishing:
```bash
python src/hf_publish_helper.py
```
Output:
- `docs/HF_PUBLISH_HELPER.md`


## Real-Data Gap Report
Track what still needs real-data reruns (vs placeholders):
```bash
python src/real_data_gap_report.py
```
Output:
- `docs/REAL_DATA_GAP_REPORT.md`


## Release Packet
Generate a concise share-ready release packet index:
```bash
python src/release_packet.py
```
Output:
- `docs/RELEASE_PACKET.md`


## HF Safe Publish Script
Token-safe Space publish flow:
```bash
export HF_TOKEN=hf_xxx
python src/hf_publish_safe.py
```


## HF Space Status Check
Fetch and persist current Space status:
```bash
python src/hf_space_status.py --space williamKang112/bci-mvp-demo
```
Output:
- `docs/HF_SPACE_STATUS.md`


## Deployment Diagnostics
Generate quick deployment troubleshooting guide:
```bash
python src/deployment_diagnose.py
```
Output:
- `docs/DEPLOYMENT_DIAGNOSE.md`


## Demo Reliability Fallback
Space demo now supports model fallback mode:
- If `outputs/model_rf_real.joblib` is missing, inference returns deterministic mock probabilities.
- Response includes `mode` = `mock_fallback` or `real_model`.


## Space Smoke Test
Quickly verify deployed Space reachability:
```bash
python src/space_smoke_test.py
```
Output:
- `docs/SPACE_SMOKE_TEST.md`


## Environment Compatibility Check
Validate runtime compatibility before full dependency install:
```bash
python src/env_compat_check.py
```
Output:
- `docs/ENV_COMPAT.md`


## Mathematical Model (明确的数学公式章节)

This section formalizes the core mathematical components used in this BCI MVP.

### 1) Bandpower Feature Extraction (Welch PSD)
For each EEG channel signal \(x_c(t)\), we estimate power spectral density (PSD) via Welch:

\[
P_c(f) = 	ext{Welch}(x_c(t))
\]

For each frequency band \(b=[f_1,f_2]\), bandpower is:

\[
	ext{BP}_{c,b} = \int_{f_1}^{f_2} P_c(f)\,df
\]

Bands used:
- delta: \([1,4)\) Hz
- theta: \([4,8)\) Hz
- alpha: \([8,13)\) Hz
- beta: \([13,30)\) Hz

Feature vector (for \(C\) channels):

\[
\mathbf{z} = [	ext{BP}_{1,\delta},	ext{BP}_{1,	heta},	ext{BP}_{1,lpha},	ext{BP}_{1,eta},\dots,	ext{BP}_{C,eta}] \in \mathbb{R}^{4C}
\]

### 2) Classification Objective
Given feature vector \(\mathbf{z}\), predict binary label \(y\in\{0,1\}\):
- \(0\): relaxed
- \(1\): focused

Model outputs posterior probability:

\[
\hat{p} = P(y=1\mid \mathbf{z})
\]

Decision rule:

\[
\hat{y} = \mathbb{1}[\hat{p} \ge 0.5]
\]

### 3) Streaming Stability (EMA + Hysteresis)
For real-time smoothing of focused probability \(p_t\):

\[
	ilde{p}_t = lpha p_t + (1-lpha)	ilde{p}_{t-1}, \quad lpha\in(0,1]
\]

Hysteresis state transition:
- if current state is relaxed and \(	ilde{p}_t \ge 	au_h\), switch to focused
- if current state is focused and \(	ilde{p}_t \le 	au_l\), switch to relaxed
- with \(	au_l < 	au_h\)

This reduces state flicker in streaming predictions.

### 4) Calibration Metric
Reliability of predicted probabilities is measured by Brier score:

\[
	ext{Brier} = rac{1}{N}\sum_{i=1}^{N}(\hat{p}_i - y_i)^2
\]

Lower is better.

### 5) Robustness Perturbation Model
We test robustness by synthetic perturbation:

\[
\mathbf{z}' = (\mathbf{z} + \epsilon) \odot \mathbf{m}
\]

where:
- \(\epsilon \sim \mathcal{N}(0,\sigma^2 I)\) is Gaussian noise
- \(\mathbf{m}\in\{0,1\}^{d}\) is dropout mask with dropout rate \(r\)

Then evaluate metrics on \(\mathbf{z}'\).

### 6) Bootstrap Confidence Intervals
For metric \(M\), bootstrap \(B\) resamples produce \(\{M^{(b)}\}_{b=1}^{B}\).
95% CI is estimated via empirical quantiles:

\[
	ext{CI}_{95\%} = [Q_{0.025}(M^{(b)}),\ Q_{0.975}(M^{(b)})]
\]

---

If needed, this section can be expanded into a paper-style "Methods" chapter with notation table and assumptions.

### Notation & Assumptions
For a concise symbol table, assumptions, and complexity notes, see:
- `docs/MATH_NOTATION.md`



## Report Consistency Check
Validate key generated docs for required sections:
```bash
python src/report_consistency_check.py
```
Output:
- `docs/REPORT_CONSISTENCY.md`
