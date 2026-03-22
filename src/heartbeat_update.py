"""
Generate a heartbeat-friendly compact update from latest status artifacts.
"""
from pathlib import Path
from datetime import datetime, timezone


def read(path):
    p=Path(path)
    return p.read_text(encoding='utf-8', errors='ignore').strip() if p.exists() else ''


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    snap = read('docs/STATUS_SNAPSHOT.txt')
    signal = read('docs/RELEASE_READY_SIGNAL.md')
    ready = 'READY' if 'SIGNAL: READY' in signal else 'NOT_READY'

    msg = f"[{ts}] heartbeat_update ready={ready} | {snap}"

    out = Path('docs/HEARTBEAT_UPDATE.txt')
    out.write_text(msg + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
