"""
Generate concise operations digest for quick periodic checks.
"""
from pathlib import Path
from datetime import datetime, timezone


def read(path):
    p=Path(path)
    return p.read_text(encoding='utf-8', errors='ignore') if p.exists() else ''


def main():
    ts=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    sig='READY' if 'SIGNAL: READY' in read('docs/RELEASE_READY_SIGNAL.md') else 'NOT_READY'
    launch='GREEN' if 'State:** GREEN' in read('docs/LAUNCH_STATUS.md') else 'YELLOW'
    guard='PASS' if 'Guard status: PASS' in read('docs/RELEASE_GUARD_REPORT.md') else 'FAIL'

    lines=[
        '# Ops Digest','',f'Generated: {ts}','',
        f'- Release signal: **{sig}**',
        f'- Launch state: **{launch}**',
        f'- Release guard: **{guard}**',
        '',
        '## Quick links',
        '- `docs/OPERATOR_QUICKLINKS.md`',
        '- `docs/RELEASE_DASHBOARD.md`',
        '- `docs/STATUS_SNAPSHOT.txt`',
    ]

    out=Path('docs/OPS_DIGEST.md')
    out.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__=='__main__':
    main()
