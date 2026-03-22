# Hugging Face Publish Helper

Generated: 2026-03-22 15:01 UTC

## Prerequisites
- Install: `pip install -U huggingface_hub`
- Login: `huggingface-cli login`

## Create Space (if not exists)
`huggingface-cli repo create bci-mvp-demo --type space --space_sdk streamlit --organization williamKang112`

## Add remote and push
`git remote add hf https://huggingface.co/spaces/williamKang112/bci-mvp-demo`
`git push hf main`

## Required files checklist
- app.py
- requirements.txt
- .streamlit/config.toml
- src/
- docs/HF_SPACE_QUICKSTART.md

## Notes
- If model file is large, use a lightweight demo model for Space runtime.
- Keep API keys out of repo and use Space Secrets when needed.
