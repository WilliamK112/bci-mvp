"""
Generate operator quick-links for day-2 maintenance.
"""
from pathlib import Path
from datetime import datetime, timezone


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        '# Operator Quick Links',
        '',
        f'Generated: {ts}',
        '',
        '- Launch status: `docs/LAUNCH_STATUS.md`',
        '- Release dashboard: `docs/RELEASE_DASHBOARD.md`',
        '- Ready signal: `docs/RELEASE_READY_SIGNAL.md`',
        '- Ready diagnose: `docs/RELEASE_READY_DIAGNOSE.md`',
        '- Status snapshot (EN): `docs/STATUS_SNAPSHOT.txt`',
        '- Status snapshot (ZH): `docs/STATUS_SNAPSHOT_ZH.md`',
        '- Space status: `docs/HF_SPACE_STATUS.md`',
        '- Space smoke test: `docs/SPACE_SMOKE_TEST.md`',
        '- Final RC: `docs/FINAL_RELEASE_CANDIDATE.md`',
    ]

    out = Path('docs/OPERATOR_QUICKLINKS.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
