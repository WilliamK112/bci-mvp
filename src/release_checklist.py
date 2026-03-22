"""
Generate actionable release checklist with checkboxes from current artifacts.
"""
from pathlib import Path
from datetime import datetime, timezone

ITEMS = [
    ('docs/RELEASE_READY_SIGNAL.md', 'Release-ready signal generated'),
    ('docs/FINAL_RELEASE_CANDIDATE.md', 'Final RC report generated'),
    ('docs/REVIEWER_PACK.md', 'Reviewer pack prepared'),
    ('docs/RELEASE_NOTES_LATEST.md', 'Latest release notes generated'),
    ('docs/RELEASE_TAG_PLAN.md', 'Tag plan generated'),
    ('docs/SPACE_SMOKE_TEST.md', 'Space smoke test report generated'),
]


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# Release Checklist', '', f'Generated: {ts}', '']
    for path, desc in ITEMS:
        ok = Path(path).exists()
        lines.append(f'- [{"x" if ok else " "}] {desc} (`{path}`)')

    lines += [
        '',
        '## Final step',
        '- [ ] Create and push tag `v1.0.0` (see `docs/RELEASE_TAG_PLAN.md`)',
    ]

    out = Path('docs/RELEASE_CHECKLIST.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
