---
title: BCI MVP Demo
emoji: 🧠
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 8000
pinned: false
---

# BCI MVP

## Language
- English (this file)
- 中文: `README.zh-CN.md`

A lightweight EEG brain-computer interface MVP focused on:
- preprocessing EEG (EDF)
- relaxed vs focused classification
- real-time stable inference (EMA + hysteresis)
- reproducible evaluation + release workflow

## Live Demo
- Hugging Face Space: https://huggingface.co/spaces/williamKang112/bci-mvp-demo

## Quick Start
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

## Project Structure
```text
bci-mvp/
  src/            # preprocessing, training, eval, reports, release tooling
  app/            # streamlit apps
  api/            # fastapi service
  docs/           # reports / readiness / release artifacts
  assets/         # generated charts/badges
  tests/          # unit tests
```

## Core Commands
```bash
# Full pipeline
python src/run_full_pipeline.py
# or
make full

# Final release candidate summary
python src/final_release_candidate.py

# Space status + smoke test
python src/hf_space_status.py --space williamKang112/bci-mvp-demo
python src/space_smoke_test.py
```

## Model & Math
- Mathematical model section: `docs/MATH_NOTATION.md`
- Technical report: `docs/TECHNICAL_REPORT.md`
- Model card: `docs/MODEL_CARD.md`

## Quality & Readiness
- Quality scorecard: `docs/QUALITY_SCORECARD.md`
- Release readiness: `docs/RELEASE_READINESS.md`
- HF Space readiness: `docs/HF_SPACE_READINESS.md`
- Final RC summary: `docs/FINAL_RELEASE_CANDIDATE.md`

## Documentation Index
- Docs home: `docs/HOME.md`
- Docs bundle index: `docs/DOCS_BUNDLE_INDEX.md`
- Command center: `docs/COMMAND_CENTER.md`
- Figure gallery: `docs/FIGURE_GALLERY.md`
- Release packet: `docs/RELEASE_PACKET.md`

## License
MIT


<!-- LATEST_PROGRESS_START -->
## Latest Progress
- 2026-03-22 15:47:24 UTC — Added docs freshness monitor
- Full log: `logs/progress.md`
<!-- LATEST_PROGRESS_END -->


## Docs Freshness Check
Check whether key docs are recently updated:
```bash
python src/docs_freshness_check.py
```
Output:
- `docs/DOCS_FRESHNESS.md`
