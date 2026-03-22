"""
Generate a markdown leaderboard from all_model_results.csv.
"""
from pathlib import Path
import csv


def to_float(x):
    try:
        return float(x)
    except Exception:
        return -1.0


def main():
    src = Path('outputs/all_model_results.csv')
    if not src.exists():
        print('Missing outputs/all_model_results.csv')
        return

    rows = []
    with src.open('r', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append(r)

    rows.sort(key=lambda r: (to_float(r.get('accuracy')), to_float(r.get('auc'))), reverse=True)

    lines = [
        '# Model Leaderboard',
        '',
        '| Rank | Model | Accuracy | F1 | AUC |',
        '|---:|---|---:|---:|---:|',
    ]
    for i, r in enumerate(rows, 1):
        lines.append(f"| {i} | {r.get('model','-')} | {r.get('accuracy','-')} | {r.get('f1','-')} | {r.get('auc','-')} |")

    out = Path('docs/MODEL_LEADERBOARD.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
