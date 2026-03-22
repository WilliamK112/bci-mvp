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
