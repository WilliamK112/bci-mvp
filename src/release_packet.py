"""
Generate a concise release packet index for fast sharing.
"""
from pathlib import Path
from datetime import datetime, timezone

ITEMS = [
    ('docs/EXECUTIVE_SUMMARY.md', 'Executive summary'),
    ('docs/TECHNICAL_REPORT.md', 'Technical report'),
    ('docs/FINAL_RELEASE_CANDIDATE.md', 'Final release candidate'),
    ('docs/RELEASE_READINESS.md', 'Release readiness'),
    ('docs/HF_SPACE_READINESS.md', 'HF Space readiness'),
    ('docs/SPACE_USER_GUIDE.md', 'Space user guide'),
    ('docs/REAL_DATA_GAP_REPORT.md', 'Real-data gap report'),
    ('docs/MODEL_CARD.md', 'Model card'),
    ('docs/MATH_NOTATION.md', 'Mathematical model'),
    ('docs/METHODS.md', 'Methods (paper-style)'),
    ('docs/RESULTS.md', 'Results summary'),
    ('docs/MODEL_LEADERBOARD.md', 'Model leaderboard'),
    ('docs/FIGURE_GALLERY.md', 'Figure gallery'),
    ('docs/release/release_en.md', 'Release post (EN)'),
    ('docs/release/release_zh.md', 'Release post (ZH)'),
    ('CITATION.cff', 'Citation metadata'),
]


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# Release Packet', '', f'Generated: {ts}', '', '## Share this packet']
    for p, name in ITEMS:
        ok = Path(p).exists()
        lines.append(f"- {'✅' if ok else '⬜'} {name}: `{p}`")

    lines += ['', '## Quick Refresh', '```bash', 'python src/final_release_candidate.py', 'python src/release_packet.py', '```']

    out = Path('docs/RELEASE_PACKET.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
