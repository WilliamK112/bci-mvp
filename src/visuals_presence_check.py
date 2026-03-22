"""
Ensure key visual artifacts used in README are present.
"""
from pathlib import Path

KEY = [
    'assets/readme_banner.svg',
    'assets/cross_dataset_matrix.svg',
    'assets/badge_project_health.svg',
]


def main():
    lines=['# Visuals Presence Check','','| Asset | Status |','|---|---|']
    missing=0
    for fp in KEY:
        ok=Path(fp).exists()
        lines.append(f"| `{fp}` | {'✅' if ok else '❌'} |")
        if not ok:
            missing += 1
    lines += ['', f'**Missing visuals:** {missing}']
    out=Path('docs/VISUALS_PRESENCE.md')
    out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'Generated {out}')
    if missing:
        raise SystemExit(2)

if __name__=='__main__':
    main()
