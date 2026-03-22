"""Visualize unified scorecards overview."""
from pathlib import Path
import json


def main():
    p = Path('outputs/scorecards_overview.json')
    if not p.exists():
        print('Missing outputs/scorecards_overview.json')
        return
    d = json.loads(p.read_text(encoding='utf-8'))
    rows = d.get('rows', [])
    if not rows:
        print('No rows found')
        return

    W, H, m = 980, 430, 60
    n = len(rows)
    bw = (W - 2*m) / n * 0.65

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="490" y="34" text-anchor="middle" font-size="24" font-family="Arial">Unified Scorecards Overview</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>',
        f'<line x1="{m}" y1="{m}" x2="{m}" y2="{H-m}" stroke="#111"/>'
    ]

    for i, r in enumerate(rows):
        name = r.get('name', f'row{i}')
        score = float(r.get('score', 0.0))
        gx = m + (i + 0.5) * (W - 2*m) / n
        x = gx - bw/2
        hh = max(0.0, min(1.0, score)) * (H - 2*m)
        y = H - m - hh
        color = '#16a34a' if r.get('pass') else '#f59e0b'
        parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{hh}" fill="{color}"/>')
        parts.append(f'<text x="{gx}" y="{y-8}" text-anchor="middle" font-size="12" font-family="Arial">{score:.2f}</text>')
        parts.append(f'<text x="{gx}" y="{H-m+18}" text-anchor="middle" font-size="11" font-family="Arial">{name}</text>')

    parts.append('</svg>')

    out = Path('assets/scorecards_overview.svg')
    out.write_text('\n'.join(parts), encoding='utf-8')

    doc = Path('docs/SCORECARDS_OVERVIEW_VISUAL.md')
    doc.write_text('\n'.join([
        '# Scorecards Overview Visual',
        '',
        '- Source: `outputs/scorecards_overview.json`',
        '- Visual: `assets/scorecards_overview.svg`',
        '',
        '![Scorecards Overview](../assets/scorecards_overview.svg)'
    ]) + '\n', encoding='utf-8')

    print(f'Generated {out} and {doc}')


if __name__ == '__main__':
    main()
