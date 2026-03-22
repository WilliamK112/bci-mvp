"""
Build/refresh a documentation bundle index for quick navigation.
"""
from pathlib import Path
from datetime import datetime, timezone

DOCS = [
    ('docs/TECHNICAL_REPORT.md', 'Technical report'),
    ('docs/RELEASE_READINESS.md', 'Release readiness dashboard'),
    ('docs/HF_SPACE_READINESS.md', 'HF Space readiness'),
    ('docs/SPACE_USER_GUIDE.md', 'Space user guide'),
    ('docs/MODEL_CARD.md', 'Model card'),
    ('docs/MATH_NOTATION.md', 'Mathematical model'),
    ('docs/METHODS.md', 'Methods (paper-style)'),
    ('docs/RESULTS.md', 'Results summary'),
    ('docs/MODEL_LEADERBOARD.md', 'Model leaderboard'),
    ('docs/FIGURE_GALLERY.md', 'Figure gallery'),
    ('docs/CHANGELOG_AUTO.md', 'Auto changelog'),
    ('docs/release/release_en.md', 'Release pack EN'),
    ('docs/release/release_zh.md', 'Release pack ZH'),
    ('docs/release/reddit_post.md', 'Reddit post draft'),
    ('docs/release/bilibili_post.md', 'Bilibili post draft'),
]


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# Documentation Bundle Index', '', f'Generated: {ts}', '', '## Core']

    for path, desc in DOCS:
        p = Path(path)
        mark = '✅' if p.exists() else '⬜'
        lines.append(f'- {mark} [{desc}]({p.name if p.parent.name=="docs" else path}) — `{path}`')

    lines += [
        '',
        '- ✅ [Citation metadata](../CITATION.cff) — `CITATION.cff`',
        '',
        '## One-command refresh sequence',
        '```bash',
        'python src/build_report.py',
        'python src/release_readiness.py',
        'python src/hf_space_readiness.py',
        'python src/leaderboard.py',
        'python src/generate_figure_gallery.py',
        'python src/changelog_from_git.py',
        'python src/generate_release_pack.py',
        'python src/generate_model_card.py',
        '```',
    ]

    out = Path('docs/DOCS_BUNDLE_INDEX.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
