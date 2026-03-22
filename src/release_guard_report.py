"""
Generate report for release guard execution result.
"""
from pathlib import Path
from datetime import datetime, timezone


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    sig = Path('docs/RELEASE_READY_SIGNAL.md').read_text(encoding='utf-8', errors='ignore') if Path('docs/RELEASE_READY_SIGNAL.md').exists() else ''
    ready = 'SIGNAL: READY' in sig

    lines = [
        '# Release Guard Report',
        '',
        f'Generated: {ts}',
        f'- Guard status: {"PASS" if ready else "FAIL"}',
        f'- Condition: RELEASE_READY_SIGNAL == READY',
    ]

    out = Path('docs/RELEASE_GUARD_REPORT.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
