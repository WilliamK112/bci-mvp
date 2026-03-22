"""
Generate a single launch-status snapshot for quick operator checks.
"""
from pathlib import Path
from datetime import datetime, timezone


def has(path, token=None):
    p=Path(path)
    if not p.exists():
        return False
    if token is None:
        return True
    txt=p.read_text(encoding='utf-8', errors='ignore')
    return token in txt


def main():
    ts=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    checks=[
        ('Ready signal is READY', has('docs/RELEASE_READY_SIGNAL.md','SIGNAL: READY')),
        ('Final RC exists', has('docs/FINAL_RELEASE_CANDIDATE.md')),
        ('Release dashboard exists', has('docs/RELEASE_DASHBOARD.md')),
        ('Space smoke test exists', has('docs/SPACE_SMOKE_TEST.md')),
        ('Release-ready badge exists', has('assets/badge_release_ready.svg')),
    ]
    ok=sum(int(v) for _,v in checks)
    total=len(checks)

    lines=['# Launch Status','',f'Generated: {ts}','','| Check | Status |','|---|---|']
    for k,v in checks:
        lines.append(f'| {k} | {"✅" if v else "❌"} |')
    lines += ['', f'**Launch status:** {ok}/{total}', f'**State:** {"GREEN" if ok==total else "YELLOW"}']

    out=Path('docs/LAUNCH_STATUS.md')
    out.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__=='__main__':
    main()
