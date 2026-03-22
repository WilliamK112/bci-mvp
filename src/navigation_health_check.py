"""
Navigation health check:
verify key index docs reference each other for discoverability.
"""
from pathlib import Path

CHECKS = [
    ('README.md', 'docs/HOME.md'),
    ('docs/HOME.md', 'QUALITY_SCORECARD.md'),
    ('docs/HOME.md', 'TECHNICAL_REPORT.md'),
    ('docs/HOME.md', 'FINAL_RELEASE_CANDIDATE.md'),
    ('docs/DOCS_BUNDLE_INDEX.md', 'TECHNICAL_REPORT.md'),
    ('docs/RELEASE_PACKET.md', 'EXECUTIVE_SUMMARY.md'),
]


def main():
    lines = ['# Navigation Health Check', '', '| Source | Target token | OK |', '|---|---|---|']
    fail = 0
    for src, token in CHECKS:
        p = Path(src)
        if not p.exists():
            lines.append(f'| `{src}` | `{token}` | ❌ missing source |')
            fail += 1
            continue
        txt = p.read_text(encoding='utf-8', errors='ignore')
        ok = token in txt
        lines.append(f'| `{src}` | `{token}` | {"✅" if ok else "❌"} |')
        if not ok:
            fail += 1

    lines += ['', f'**Missing links:** {fail}']
    out = Path('docs/NAVIGATION_HEALTH.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')
    if fail:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
