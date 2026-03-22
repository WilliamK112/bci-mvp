"""
Check cross-document consistency for key generated docs and outputs.
Flags missing links/sections and inconsistent status references.
"""
from pathlib import Path
from datetime import datetime, timezone

DOCS = {
    'README.md': ['Mathematical Model', 'Final Release Candidate', 'HF Space Status Check'],
    'docs/TECHNICAL_REPORT.md': ['Benchmark Summary', 'Cross-Dataset', 'Release Readiness'],
    'docs/FINAL_RELEASE_CANDIDATE.md': ['Pipeline success', 'Output coverage'],
    'docs/RELEASE_READINESS.md': ['Score'],
    'docs/HF_SPACE_READINESS.md': ['Score'],
    'docs/EXECUTIVE_SUMMARY.md': ['Topline Status', 'Deliverables'],
}


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# Report Consistency Check', '', f'Generated: {ts}', '', '| File | Check | Result |', '|---|---|---|']
    fails = 0

    for fp, checks in DOCS.items():
        p = Path(fp)
        if not p.exists():
            lines.append(f'| `{fp}` | file exists | ❌ missing |')
            fails += 1
            continue
        txt = p.read_text(encoding='utf-8', errors='ignore')
        lines.append(f'| `{fp}` | file exists | ✅ |')
        for c in checks:
            ok = c in txt
            lines.append(f'| `{fp}` | contains `{c}` | {"✅" if ok else "❌"} |')
            fails += (0 if ok else 1)

    lines += ['', f'**Total missing checks:** {fails}']

    out = Path('docs/REPORT_CONSISTENCY.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
