"""
Generate a milestone stamp summarizing current release maturity.
"""
from pathlib import Path
from datetime import datetime, timezone


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    ready = Path('docs/RELEASE_READY_SIGNAL.md').exists() and 'SIGNAL: READY' in Path('docs/RELEASE_READY_SIGNAL.md').read_text(encoding='utf-8', errors='ignore')
    stamp = 'MILESTONE: V1_READY' if ready else 'MILESTONE: IN_PROGRESS'

    lines = [
        '# Milestone Stamp',
        '',
        f'Generated: {ts}',
        f'- {stamp}',
        '- Source: docs/RELEASE_READY_SIGNAL.md',
    ]
    out = Path('docs/MILESTONE_STAMP.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
