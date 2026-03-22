"""
Diagnose why RELEASE_READY_SIGNAL is NOT_READY using FINAL_RELEASE_CANDIDATE details.
"""
from pathlib import Path
import re
from datetime import datetime, timezone


def main():
    rc = Path('docs/FINAL_RELEASE_CANDIDATE.md')
    if not rc.exists():
        raise SystemExit('Missing docs/FINAL_RELEASE_CANDIDATE.md')
    txt = rc.read_text(encoding='utf-8', errors='ignore')

    steps = re.findall(r'- \[(OK|FAIL\(\d+\))\] `([^`]+)`', txt)
    outputs = re.findall(r'- \[(x| )\] `([^`]+)`', txt)

    failed_steps = [cmd for status, cmd in steps if status != 'OK']
    missing_outputs = [path for mark, path in outputs if mark != 'x']

    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# Release Ready Diagnose', '', f'Generated: {ts}', '']
    lines += [f'- Failed steps: {len(failed_steps)}', f'- Missing outputs: {len(missing_outputs)}', '']

    lines += ['## Failed Steps']
    if failed_steps:
        lines += [f'- `{s}`' for s in failed_steps]
    else:
        lines += ['- None']

    lines += ['', '## Missing Outputs']
    if missing_outputs:
        lines += [f'- `{o}`' for o in missing_outputs]
    else:
        lines += ['- None']

    lines += ['', '## Suggested Next Actions']
    if failed_steps:
        lines += ['- Re-run failed generators individually and fix root errors.']
    if missing_outputs:
        lines += ['- Generate missing artifacts and rerun final RC.']
    if not failed_steps and not missing_outputs:
        lines += ['- RC appears complete; rerun `src/release_ready_signal.py`.']

    out = Path('docs/RELEASE_READY_DIAGNOSE.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
