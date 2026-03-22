"""
Check whether key docs are fresh relative to latest commit timestamp.
"""
from pathlib import Path
from datetime import datetime, timezone
import subprocess

KEY_DOCS = [
    'README.md',
    'README.zh-CN.md',
    'docs/HOME.md',
    'docs/TECHNICAL_REPORT.md',
    'docs/FINAL_RELEASE_CANDIDATE.md',
    'docs/QUALITY_SCORECARD.md',
]


def git_head_time():
    p = subprocess.run(['git', 'log', '-1', '--format=%ct'], capture_output=True, text=True)
    if p.returncode != 0:
        return None
    return int(p.stdout.strip())


def main(max_age_hours=24):
    head_ts = git_head_time()
    now_ts = int(datetime.now(timezone.utc).timestamp())

    lines = ['# Docs Freshness Check', '', f'Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}', '', '| File | Fresh? | Age (hours) |', '|---|---|---:|']

    stale = 0
    for fp in KEY_DOCS:
        p = Path(fp)
        if not p.exists():
            lines.append(f'| `{fp}` | ❌ missing | - |')
            stale += 1
            continue

        age_h = (now_ts - int(p.stat().st_mtime)) / 3600.0
        fresh = age_h <= max_age_hours
        lines.append(f'| `{fp}` | {"✅" if fresh else "❌"} | {age_h:.1f} |')
        stale += (0 if fresh else 1)

    lines += ['', f'**Stale/Missing count:** {stale}']
    out = Path('docs/DOCS_FRESHNESS.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
