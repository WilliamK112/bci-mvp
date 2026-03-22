"""
Generate a one-page project brief for fast external sharing.
"""
from pathlib import Path
from datetime import datetime, timezone
import re


def grab(path, pattern, default='n/a'):
    p = Path(path)
    if not p.exists():
        return default
    txt = p.read_text(encoding='utf-8', errors='ignore')
    m = re.search(pattern, txt)
    return m.group(1).strip() if m else default


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    qidx = grab('docs/QUALITY_SCORECARD.md', r'\*\*Overall quality index:\*\*\s*([0-9.]+)')
    cidx = grab('docs/COMPLIANCE_SCORECARD.md', r'\*\*Compliance index:\*\*\s*([0-9.]+)')
    rc_ok = grab('docs/FINAL_RELEASE_CANDIDATE.md', r'\*\*Pipeline success:\*\*\s*([^\n]+)')
    rc_cov = grab('docs/FINAL_RELEASE_CANDIDATE.md', r'\*\*Output coverage:\*\*\s*([^\n]+)')

    lines = [
        '# BCI MVP — One Pager',
        '',
        f'Generated: {ts}',
        '',
        '## What it is',
        'A lightweight EEG BCI MVP with preprocessing, binary state inference, streaming stabilization, and reproducible evaluation/release tooling.',
        '',
        '## Why it matters',
        '- Low hardware barrier for prototyping',
        '- Strong engineering/reproducibility surface',
        '- Public demo + structured quality controls',
        '',
        '## Current status (headline metrics)',
        f'- Quality index: **{qidx}**',
        f'- Compliance index: **{cidx}**',
        f'- RC pipeline success: **{rc_ok}**',
        f'- RC output coverage: **{rc_cov}**',
        '',
        '## Core capabilities',
        '- Cross-dataset generalization evaluation',
        '- Explainability + ablation',
        '- Calibration + robustness + uncertainty (bootstrap CI)',
        '- HF Space deployment + health checks',
        '',
        '## Links',
        '- Repo: https://github.com/WilliamK112/bci-mvp',
        '- Demo: https://huggingface.co/spaces/williamKang112/bci-mvp-demo',
        '- Technical report: `docs/TECHNICAL_REPORT.md`',
        '- Release packet: `docs/RELEASE_PACKET.md`',
        '- Limitations: `docs/LIMITATIONS.md`',
    ]

    out = Path('docs/ONE_PAGER.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
