"""
Generate a reviewer-friendly minimal pack index (3 docs + 3 visuals).
"""
from pathlib import Path
from datetime import datetime, timezone

DOCS = [
    'docs/ONE_PAGER.md',
    'docs/TECHNICAL_REPORT.md',
    'docs/RESULTS.md',
]
VIS = [
    'assets/cross_dataset_matrix.svg',
    'assets/all_model_comparison.svg',
    'assets/calibration_curve.svg',
]


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# Reviewer Pack', '', f'Generated: {ts}', '', '## Core Docs (3)']
    for d in DOCS:
        lines.append(f"- {'✅' if Path(d).exists() else '⬜'} `{d}`")

    lines += ['', '## Core Visuals (3)']
    for v in VIS:
        lines.append(f"- {'✅' if Path(v).exists() else '⬜'} `{v}`")

    lines += ['', '## Share Links', '- Repo: https://github.com/WilliamK112/bci-mvp', '- Demo: https://huggingface.co/spaces/williamKang112/bci-mvp-demo']

    out = Path('docs/REVIEWER_PACK.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
