"""
Generate a model card for public release from available artifacts.
"""
from pathlib import Path
import json
from datetime import datetime, timezone


def load_json(p: Path):
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def main():
    out = Path('outputs')
    docs = Path('docs')
    docs.mkdir(exist_ok=True)

    metrics = load_json(out / 'cross_dataset_results.json')
    explain = load_json(out / 'permutation_importance_summary.json')

    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    perf = '- Performance metrics pending real run.'
    if metrics:
        rf = (metrics.get('models') or {}).get('RF', {})
        perf = (
            f"- Cross-dataset RF accuracy: {rf.get('accuracy')}\n"
            f"- Cross-dataset RF f1: {rf.get('f1')}\n"
            f"- Cross-dataset RF auc: {rf.get('auc')}"
        )

    exp = '- Explainability summary pending.'
    if explain:
        exp = f"- Top band/channel signals: band={explain.get('top_band')}, channel={explain.get('top_channel')}"

    text = f"""# Model Card — BCI MVP Classifier

Generated: {ts}

## Model Details
- Type: Classical ML baseline (RF/SVM/MLP pipeline variants)
- Task: Binary EEG state classification (`relaxed` vs `focused`)
- Input: 32-dim handcrafted EEG feature vector (bandpower by channel)
- Output: Class label + probability

## Intended Use
- Educational demos
- Benchmarking preprocessing and inference pipelines
- Prototype validation before real-time hardware integration

## Performance
{perf}

## Explainability
{exp}

## Limitations
- Not validated for clinical/medical diagnosis.
- Sensitive to dataset shift and recording setup differences.
- Current public figures may include demo placeholders until full real-data runs complete.

## Ethical Considerations
- Do not use as medical advice.
- Respect participant consent and data governance.
- Evaluate fairness across populations and devices before deployment.
"""

    (docs / 'MODEL_CARD.md').write_text(text, encoding='utf-8')

    # HF Space README scaffold
    hf = Path('docs/HF_SPACE_README.md')
    hf.write_text(
        """---
title: BCI MVP Demo
emoji: 🧠
colorFrom: indigo
colorTo: blue
sdk: streamlit
sdk_version: "1.38.0"
app_file: app.py
pinned: false
---

# BCI MVP Demo

Lightweight EEG BCI demo with:
- Single inference mode
- Streaming stability mode (EMA + hysteresis)
- Reproducible benchmark/evaluation scripts

## Repo
https://github.com/WilliamK112/bci-mvp
""",
        encoding='utf-8'
    )

    print('Generated docs/MODEL_CARD.md and docs/HF_SPACE_README.md')


if __name__ == '__main__':
    main()
