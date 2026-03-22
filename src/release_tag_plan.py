"""
Generate release tag plan from current v1 readiness artifacts.
"""
from pathlib import Path
from datetime import datetime, timezone


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    ready = False
    sig = Path('docs/RELEASE_READY_SIGNAL.md')
    if sig.exists():
        ready = 'SIGNAL: READY' in sig.read_text(encoding='utf-8', errors='ignore')

    lines = [
        '# Release Tag Plan',
        '',
        f'Generated: {ts}',
        f'- Ready signal: {"READY" if ready else "NOT_READY"}',
        '',
        '## Planned Tag',
        '- `v1.0.0`',
        '',
        '## Commands',
        '```bash',
        'git tag -a v1.0.0 -m "BCI MVP v1.0.0"',
        'git push origin v1.0.0',
        '```',
        '',
        '## Preconditions',
        '- `docs/RELEASE_READY_SIGNAL.md` is READY',
        '- `docs/FINAL_RELEASE_CANDIDATE.md` is up to date',
        '- Demo link is accessible',
    ]

    out = Path('docs/RELEASE_TAG_PLAN.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
