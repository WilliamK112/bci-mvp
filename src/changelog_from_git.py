"""
Generate/update docs/CHANGELOG_AUTO.md from recent git history.
"""
from pathlib import Path
import subprocess
from datetime import datetime, timezone


def run(cmd):
    p = subprocess.run(cmd, check=False, capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def main(limit=25):
    code, out, err = run(["git", "log", f"--pretty=format:%h|%ad|%s", "--date=short", f"-n{limit}"])
    if code != 0:
        raise RuntimeError(err or 'git log failed')

    rows = [r for r in out.splitlines() if r.strip()]
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    lines = [
        '# Auto Changelog',
        '',
        f'Generated: {ts}',
        '',
        '| Commit | Date | Message |',
        '|---|---|---|',
    ]

    for r in rows:
        parts = r.split('|', 2)
        if len(parts) != 3:
            continue
        h, d, s = parts
        lines.append(f'| `{h}` | {d} | {s} |')

    outp = Path('docs/CHANGELOG_AUTO.md')
    outp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {outp}')


if __name__ == '__main__':
    main()
