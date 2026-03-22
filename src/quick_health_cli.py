"""
Quick terminal health summary for operators.
"""
from pathlib import Path


def read(path):
    p=Path(path)
    return p.read_text(encoding='utf-8', errors='ignore') if p.exists() else ''


def main():
    ready = 'READY' if 'SIGNAL: READY' in read('docs/RELEASE_READY_SIGNAL.md') else 'NOT_READY'
    launch = 'GREEN' if 'State:** GREEN' in read('docs/LAUNCH_STATUS.md') else 'YELLOW'
    guard = 'PASS' if 'Guard status: PASS' in read('docs/RELEASE_GUARD_REPORT.md') else 'FAIL'
    print(f"ready={ready} launch={launch} guard={guard}")


if __name__ == '__main__':
    main()
