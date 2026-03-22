"""
Generate a binary release-ready signal from RC metrics.
"""
from pathlib import Path
import re
from datetime import datetime, timezone


def parse_pair(text, pattern):
    m = re.search(pattern, text)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def main():
    rc = Path('docs/FINAL_RELEASE_CANDIDATE.md')
    if not rc.exists():
        raise SystemExit('Missing docs/FINAL_RELEASE_CANDIDATE.md')
    txt = rc.read_text(encoding='utf-8', errors='ignore')

    p = parse_pair(txt, r'\*\*Pipeline success:\*\*\s*(\d+)/(\d+)')
    c = parse_pair(txt, r'\*\*Output coverage:\*\*\s*(\d+)/(\d+)')

    ready = bool(p and c and p[0] == p[1] and c[0] == c[1])

    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        '# Release Ready Signal',
        '',
        f'Generated: {ts}',
        f'- Pipeline success: {p[0]}/{p[1]}' if p else '- Pipeline success: n/a',
        f'- Output coverage: {c[0]}/{c[1]}' if c else '- Output coverage: n/a',
        '',
        f'## SIGNAL: {"READY" if ready else "NOT_READY"}',
    ]

    out = Path('docs/RELEASE_READY_SIGNAL.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out} -> {"READY" if ready else "NOT_READY"}')


if __name__ == '__main__':
    main()
