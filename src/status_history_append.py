"""
Append latest STATUS_SNAPSHOT into a rolling history log for trend tracking.
"""
from pathlib import Path
from datetime import datetime, timezone


def main():
    snap_path = Path('docs/STATUS_SNAPSHOT.txt')
    if not snap_path.exists():
        raise SystemExit('Missing docs/STATUS_SNAPSHOT.txt')

    snap = snap_path.read_text(encoding='utf-8', errors='ignore').strip()
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    out = Path('docs/STATUS_HISTORY.log')
    line = f"{ts} | {snap}\n"
    if out.exists():
        out.write_text(out.read_text(encoding='utf-8', errors='ignore') + line, encoding='utf-8')
    else:
        out.write_text(line, encoding='utf-8')

    print(f'Updated {out}')


if __name__ == '__main__':
    main()
