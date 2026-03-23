---
title: BCI MVP Demo
emoji: 🧠
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 8000
pinned: false
---

# 🧠 BCI MVP

![BCI MVP Banner](assets/readme_banner.svg)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Space](https://img.shields.io/badge/HuggingFace-Space-yellow)
![Project Health](assets/badge_project_health.svg)
![Release Ready](assets/badge_release_ready.svg)
![Release Matrix](assets/badge_release_matrix.svg)
![Release Decision](assets/badge_release_decision.svg)
![Milestone](assets/badge_milestone.svg)

## 🌐 Language
- English (this file)
- 中文: `README.zh-CN.md`

A lightweight EEG brain-computer interface MVP focused on:
- EEG preprocessing (EDF)
- relaxed vs focused classification
- real-time stable inference (EMA + hysteresis)
- reproducible evaluation and release workflow

## 🚀 Live Demo
- Hugging Face Space: https://huggingface.co/spaces/williamKang112/bci-mvp-demo

## ⚡ Quick Start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/check_data.py
python src/train.py

# API
uvicorn api.main:app --reload --port 8000

# Dashboard
streamlit run app/dashboard.py
```

## 📁 Project Structure
```text
bci-mvp/
  src/            # preprocessing, training, eval, reports, release tooling
  app/            # streamlit apps
  api/            # fastapi service
  docs/           # reports / readiness / release artifacts
  assets/         # generated charts/badges
  tests/          # unit tests
```

## 🧩 Core Commands
```bash
# Full pipeline
python src/run_full_pipeline.py
# or
make full

# Final release candidate summary
python src/final_release_candidate.py
python src/quick_health_cli.py

# Space status + smoke test
python src/hf_space_status.py --space williamKang112/bci-mvp-demo
python src/space_smoke_test.py
```

## 📐 Model & Math
- Mathematical model: `docs/MATH_NOTATION.md`
- Limitations: `docs/LIMITATIONS.md`
- Methods (paper-style): `docs/METHODS.md`
- Results summary: `docs/RESULTS.md`
- Technical report: `docs/TECHNICAL_REPORT.md`
- Model card: `docs/MODEL_CARD.md`

## ✅ Quality & Readiness
- Quality scorecard: `docs/QUALITY_SCORECARD.md`
- Compliance scorecard: `docs/COMPLIANCE_SCORECARD.md`
- Release readiness: `docs/RELEASE_READINESS.md`
- HF Space readiness: `docs/HF_SPACE_READINESS.md`
- Final RC summary: `docs/FINAL_RELEASE_CANDIDATE.md`
- Release dashboard: `docs/RELEASE_DASHBOARD.md`
- Launch status: `docs/LAUNCH_STATUS.md`
- Release guard report: `docs/RELEASE_GUARD_REPORT.md`
- v1 release notes: `docs/V1_RELEASE_NOTES.md`
- release archive manifest: `docs/RELEASE_ARCHIVE_MANIFEST.md`

## 🔥 Cross-Dataset Heatmap
![Cross Dataset Matrix](assets/cross_dataset_matrix.svg)

## 📚 Documentation Index
- Docs home: `docs/HOME.md`
- One pager: `docs/ONE_PAGER.md`
- Space user guide: `docs/SPACE_USER_GUIDE.md`
- Docs bundle index: `docs/DOCS_BUNDLE_INDEX.md`
- Command center: `docs/COMMAND_CENTER.md`
- Figure gallery: `docs/FIGURE_GALLERY.md`
- Release packet: `docs/RELEASE_PACKET.md`

## 📄 License
MIT

## 📚 Citation
If this project helps your work, please cite using `CITATION.cff`.


<!-- LATEST_PROGRESS_START -->
## Latest Progress
- 2026-03-23 00:13:58 UTC — Added v1-release-gate regression test and CI coverage
- Full log: `logs/progress.md`
<!-- LATEST_PROGRESS_END -->


## Public EEG Data Bootstrap (Auto Fetch)
```bash
python src/fetch_public_eeg_data.py
```
This fetches EEGBCI public data and prepares:
- `data/relaxed/*.edf`
- `data/focused/*.edf`

## 📝 Results Brief
- `docs/RESULTS_BRIEF_EN.md`


## 👥 Cross-Subject Evaluation
Measure subject-level generalization (Leave-One-Subject-Out):
```bash
python src/cross_subject_eval.py
```
Output:
- `outputs/cross_subject_results.json`


## 🧪 Cross-Subject LOSO Visual
```bash
python src/plot_cross_subject.py
```
Output:
- `assets/cross_subject_loso.svg`


## 👤 Subject-Holdout Evaluation
Test generalization by holding out one subject at a time:
```bash
python src/subject_holdout_eval.py
```
Output:
- `outputs/subject_holdout_results.json`


## 🔁 One-command Repro
```bash
python src/repro_one_command.py
```

## 🧾 Real Data Evidence
See: `docs/REAL_DATA_EVIDENCE.md`
