"""
Hard release guard: fails if release signal is not READY.
"""
from pathlib import Path


def main():
    p = Path('docs/RELEASE_READY_SIGNAL.md')
    if not p.exists():
        raise SystemExit('Missing docs/RELEASE_READY_SIGNAL.md')
    txt = p.read_text(encoding='utf-8', errors='ignore')
    if 'SIGNAL: READY' not in txt:
        raise SystemExit('Release guard failed: signal is NOT_READY')
    print('Release guard passed: READY')


if __name__ == '__main__':
    main()
