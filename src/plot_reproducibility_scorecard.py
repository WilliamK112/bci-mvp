"""Visualize reproducibility scorecard checks."""
from pathlib import Path
import json


def main():
    p = Path('outputs/reproducibility_scorecard.json')
    if not p.exists():
        print('Missing outputs/reproducibility_scorecard.json')
        return
    d = json.loads(p.read_text(encoding='utf-8'))
    checks = d.get('checks', {})
    items = list(checks.items())
    if not items:
        print('No checks found')
        return

    W, H, m = 980, 420, 60
    n = len(items)
    bw = (W - 2*m) / n * 0.65

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="490" y="34" text-anchor="middle" font-size="24" font-family="Arial">Reproducibility Scorecard Checks</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>'
    ]

    for i, (k, v) in enumerate(items):
        gx = m + (i + 0.5) * (W - 2*m) / n
        x = gx - bw/2
        val = 1.0 if v else 0.0
        hh = val * (H - 2*m)
        y = H - m - hh
        color = '#16a34a' if v else '#dc2626'
        parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{hh}" fill="{color}"/>')
        parts.append(f'<text x="{gx}" y="{H-m+18}" text-anchor="middle" font-size="10" font-family="Arial">{k}</text>')
        parts.append(f'<text x="{gx}" y="{y-8}" text-anchor="middle" font-size="12" font-family="Arial">{"PASS" if v else "FAIL"}</text>')

    parts.append('</svg>')

    out = Path('assets/reproducibility_scorecard.svg')
    out.write_text('\n'.join(parts), encoding='utf-8')

    doc = Path('docs/REPRODUCIBILITY_SCORECARD_VISUAL.md')
    doc.write_text('\n'.join([
        '# Reproducibility Scorecard Visual',
        '',
        '- Source: `outputs/reproducibility_scorecard.json`',
        '- Visual: `assets/reproducibility_scorecard.svg`',
        '',
        '![Reproducibility Scorecard](../assets/reproducibility_scorecard.svg)'
    ]) + '\n', encoding='utf-8')

    print(f'Generated {out} and {doc}')


if __name__ == '__main__':
    main()
