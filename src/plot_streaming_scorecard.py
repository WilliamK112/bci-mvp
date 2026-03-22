"""Visualize streaming scorecard gates."""
from pathlib import Path
import json


def main():
    p = Path('outputs/streaming_scorecard.json')
    if not p.exists():
        print('Missing outputs/streaming_scorecard.json')
        return
    d = json.loads(p.read_text(encoding='utf-8'))
    gates = d.get('gates', {})
    items = list(gates.items())
    if not items:
        print('No gates found')
        return

    W, H, m = 980, 420, 60
    n = len(items)
    bw = (W - 2*m) / n * 0.65

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="490" y="34" text-anchor="middle" font-size="24" font-family="Arial">Streaming Scorecard Gates</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>',
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

    out = Path('assets/streaming_scorecard.svg')
    out.write_text('\n'.join(parts), encoding='utf-8')

    doc = Path('docs/STREAMING_SCORECARD_VISUAL.md')
    doc.write_text('\n'.join([
        '# Streaming Scorecard Visual',
        '',
        '- Source: `outputs/streaming_scorecard.json`',
        '- Visual: `assets/streaming_scorecard.svg`',
        '',
        '![Streaming Scorecard](../assets/streaming_scorecard.svg)'
    ]) + '\n', encoding='utf-8')

    print(f'Generated {out} and {doc}')


if __name__ == '__main__':
    main()
