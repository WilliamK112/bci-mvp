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
