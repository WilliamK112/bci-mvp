"""
Generate an actionable next-milestones plan from current project status.
"""
from pathlib import Path
from datetime import datetime, timezone

MILESTONES = [
    ("Run real-data full pipeline", "Replace placeholder/demo artifacts with real experiment outputs", "High"),
    ("Cross-dataset matrix on >=3 real datasets", "Publish generalization heatmap with real numbers", "High"),
    ("HF Space public launch", "Deploy app.py demo and verify public interaction flow", "High"),
    ("Benchmark deep model extension", "Add stronger deep baseline (EEGNet/PyTorch) for credibility", "Medium"),
    ("Quantify uncertainty", "Add confidence intervals/bootstrapping to key metrics", "Medium"),
]


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        '# Next Milestones',
        '',
        f'Generated: {ts}',
        '',
        '| Priority | Milestone | Goal |',
        '|---|---|---|',
    ]
    for m, g, p in MILESTONES:
        lines.append(f'| {p} | {m} | {g} |')

    lines += [
        '',
        '## Immediate Commands',
        '- `python src/run_full_pipeline.py`',
        '- `python src/final_release_candidate.py`',
        '- `python src/hf_space_readiness.py`',
    ]

    out = Path('docs/NEXT_MILESTONES.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
