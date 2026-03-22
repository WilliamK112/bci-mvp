"""
Generate an executive summary from readiness/report artifacts.
"""
from pathlib import Path
import re
from datetime import datetime, timezone


def read_text(path):
    p = Path(path)
    return p.read_text(encoding='utf-8') if p.exists() else ''


def extract_score(text):
    m = re.search(r'\*\*Score:\*\*\s*(\d+)/(\d+)', text)
    if not m:
        return 'n/a'
    return f"{m.group(1)}/{m.group(2)}"


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    rr = read_text('docs/RELEASE_READINESS.md')
    hf = read_text('docs/HF_SPACE_READINESS.md')
    rc = read_text('docs/FINAL_RELEASE_CANDIDATE.md')

    rel_score = extract_score(rr)
    hf_score = extract_score(hf)

    pipeline = 'n/a'
    m = re.search(r'\*\*Pipeline success:\*\*\s*([^\n]+)', rc)
    if m:
        pipeline = m.group(1).strip()

    coverage = 'n/a'
    m2 = re.search(r'\*\*Output coverage:\*\*\s*([^\n]+)', rc)
    if m2:
        coverage = m2.group(1).strip()

    lines = [
        '# Executive Summary',
        '',
        f'Generated: {ts}',
        '',
        '## Topline Status',
        f'- Release readiness score: **{rel_score}**',
        f'- HF Space readiness score: **{hf_score}**',
        f'- Final RC pipeline success: **{pipeline}**',
        f'- Final RC output coverage: **{coverage}**',
        '',
        '## Deliverables (high impact)',
        '- Cross-dataset evaluation (single-pair + matrix + heatmap)',
        '- Multi-model benchmark + leaderboard + unified visual comparisons',
        '- Explainability (feature importance + permutation + ablation)',
        '- Reliability checks (calibration + robustness)',
        '- End-to-end reproducibility (CI + Docker + full-pipeline + validation)',
        '- Release assets (model card, release drafts, docs bundle, status badges)',
        '',
        '## Key Docs',
        '- `docs/TECHNICAL_REPORT.md`',
        '- `docs/FINAL_RELEASE_CANDIDATE.md`',
        '- `docs/RELEASE_READINESS.md`',
        '- `docs/HF_SPACE_READINESS.md`',
        '- `docs/MODEL_CARD.md`',
    ]

    out = Path('docs/EXECUTIVE_SUMMARY.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
