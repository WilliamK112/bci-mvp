"""Visualize release readiness matrix pillars."""
from pathlib import Path
import json


def main():
    p = Path('outputs/release_readiness_matrix.json')
    if not p.exists():
        print('Missing outputs/release_readiness_matrix.json')
        return

    obj = json.loads(p.read_text(encoding='utf-8'))
    rows = obj.get('rows', [])
    if not rows:
        print('No rows in release_readiness_matrix')
        return

    W, H, m = 1020, 430, 60
    n = len(rows)
    bw = (W - 2*m) / n * 0.62

    def y(v):
        return H - m - max(0.0, min(1.0, v)) * (H - 2*m)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="510" y="34" text-anchor="middle" font-size="24" font-family="Arial">Release Readiness Matrix</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>',
        f'<line x1="{m}" y1="{m}" x2="{m}" y2="{H-m}" stroke="#111"/>'
    ]

    for i, r in enumerate(rows):
        name = r.get('name', f'row{i}')
        score = float(r.get('score', 0.0))
        passed = bool(r.get('pass', False))
        gx = m + (i + 0.5) * (W - 2*m) / n
        x = gx - bw/2
        yy = y(score)
        hh = (H - m) - yy
        color = '#16a34a' if passed else '#f59e0b'
        parts.append(f'<rect x="{x}" y="{yy}" width="{bw}" height="{hh}" fill="{color}"/>')
        parts.append(f'<text x="{gx}" y="{yy-8}" text-anchor="middle" font-size="11" font-family="Arial">{score:.2f}</text>')
        parts.append(f'<text x="{gx}" y="{H-m+18}" text-anchor="middle" font-size="10" font-family="Arial">{name}</text>')

    parts.append('</svg>')

    out = Path('assets/release_readiness_matrix.svg')
    out.write_text('\n'.join(parts), encoding='utf-8')

    doc = Path('docs/RELEASE_READINESS_MATRIX_VISUAL.md')
    doc.write_text('\n'.join([
        '# Release Readiness Matrix Visual',
        '',
        '- Source: `outputs/release_readiness_matrix.json`',
        '- Visual: `assets/release_readiness_matrix.svg`',
        '',
        '![Release Readiness Matrix](../assets/release_readiness_matrix.svg)'
    ]) + '\n', encoding='utf-8')

    print(f'Generated {out} and {doc}')


if __name__ == '__main__':
    main()
