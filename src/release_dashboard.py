"""
Generate a compact release dashboard from ready-signal + diagnose + checklist.
"""
from pathlib import Path
from datetime import datetime, timezone


def read(path):
    p=Path(path)
    return p.read_text(encoding='utf-8', errors='ignore') if p.exists() else ''


def main():
    ts=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    sig=read('docs/RELEASE_READY_SIGNAL.md')
    diag=read('docs/RELEASE_READY_DIAGNOSE.md')
    chk=read('docs/RELEASE_CHECKLIST.md')

    ready='READY' if 'SIGNAL: READY' in sig else 'NOT_READY'
    failed='0' if '- Failed steps: 0' in diag else 'non-zero'
    missing='0' if '- Missing outputs: 0' in diag else 'non-zero'

    checklist_done = chk.count('- [x]')
    checklist_total = chk.count('- [x]') + chk.count('- [ ]')

    lines=[
        '# Release Dashboard','',f'Generated: {ts}','',
        f'- Ready signal: **{ready}**',
        f'- Failed steps: **{failed}**',
        f'- Missing outputs: **{missing}**',
        f'- Checklist completion: **{checklist_done}/{checklist_total}**',
        '',
        '## Links',
        '- `docs/RELEASE_READY_SIGNAL.md`',
        '- `docs/RELEASE_READY_DIAGNOSE.md`',
        '- `docs/RELEASE_CHECKLIST.md`',
        '- `docs/FINAL_RELEASE_CANDIDATE.md`',
    ]

    out=Path('docs/RELEASE_DASHBOARD.md')
    out.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__=='__main__':
    main()
