"""
Environment compatibility check for reliable local setup.
Focus: Python version and scientific stack installability constraints.
"""
from pathlib import Path
import platform
from datetime import datetime, timezone


def main():
    py = platform.python_version()
    major_minor = tuple(map(int, py.split('.')[:2]))

    issues = []
    recs = []

    if major_minor >= (3, 14):
        issues.append('Python 3.14 may fail building scipy from source on some macOS setups (Fortran toolchain missing).')
        recs.append('Use Python 3.11/3.12 for smoother scientific package installation.')
    else:
        recs.append('Python version is compatible with common scipy wheels.')

    recs.append('Prefer virtualenv: `python3 -m venv .venv && source .venv/bin/activate`')
    recs.append('Install base test deps for lightweight checks: `pip install numpy joblib`')

    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        '# Environment Compatibility Check',
        '',
        f'Generated: {ts}',
        f'- Python: `{py}`',
        f'- Platform: `{platform.platform()}`',
        '',
        '## Issues',
    ]
    if issues:
        lines += [f'- {x}' for x in issues]
    else:
        lines += ['- None detected.']

    lines += ['', '## Recommendations']
    lines += [f'- {x}' for x in recs]

    out = Path('docs/ENV_COMPAT.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
