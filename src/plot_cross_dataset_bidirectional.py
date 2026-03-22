"""Visualize bidirectional cross-dataset RF metrics."""
from pathlib import Path
import json


def main():
    p = Path('outputs/cross_dataset_bidirectional.json')
    if not p.exists():
        print('Missing outputs/cross_dataset_bidirectional.json')
        return
    d = json.loads(p.read_text(encoding='utf-8'))

    a = d.get('A_to_B', {}).get('models', {}).get('RF', {})
    b = d.get('B_to_A', {}).get('models', {}).get('RF', {})

    labels = ['A→B acc', 'B→A acc', 'A→B f1', 'B→A f1', 'A→B auc', 'B→A auc']
    vals = [
        float(a.get('accuracy', 0.0)), float(b.get('accuracy', 0.0)),
        float(a.get('f1', 0.0)), float(b.get('f1', 0.0)),
        float(a.get('auc', 0.0)), float(b.get('auc', 0.0)),
    ]

    W, H, m = 1080, 500, 70
    n = len(vals)
    bw = (W - 2*m) / n * 0.6

    def y(v):
        return H - m - max(0, min(1, v)) * (H - 2*m)

    colors = ['#2563eb', '#1d4ed8', '#16a34a', '#15803d', '#f59e0b', '#d97706']

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="540" y="34" text-anchor="middle" font-size="24" font-family="Arial">Cross-Dataset Bidirectional (RF)</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>',
        f'<line x1="{m}" y1="{m}" x2="{m}" y2="{H-m}" stroke="#111"/>'
    ]

    for t in [0, 0.25, 0.5, 0.75, 1.0]:
        yy = y(t)
        parts.append(f'<line x1="{m}" y1="{yy}" x2="{W-m}" y2="{yy}" stroke="#e5e7eb"/>')
        parts.append(f'<text x="{m-8}" y="{yy+4}" text-anchor="end" font-size="10" font-family="Arial">{t:.2f}</text>')

    for i, (lab, v) in enumerate(zip(labels, vals)):
        gx = m + (i + 0.5) * (W - 2*m) / n
        x = gx - bw/2
        yy = y(v)
        hh = (H - m) - yy
        parts.append(f'<rect x="{x}" y="{yy}" width="{bw}" height="{hh}" fill="{colors[i]}"/>')
        parts.append(f'<text x="{gx}" y="{yy-8}" text-anchor="middle" font-size="11" font-family="Arial">{v:.3f}</text>')
        parts.append(f'<text x="{gx}" y="{H-m+18}" text-anchor="middle" font-size="11" font-family="Arial">{lab}</text>')

    parts.append('</svg>')

    out = Path('assets/cross_dataset_bidirectional.svg')
    out.write_text('\n'.join(parts), encoding='utf-8')

    doc = Path('docs/CROSS_DATASET_BIDIRECTIONAL_VISUAL.md')
    doc.write_text('\n'.join([
        '# Cross-Dataset Bidirectional Visual',
        '',
        '- Source: `outputs/cross_dataset_bidirectional.json`',
        '- Visual: `assets/cross_dataset_bidirectional.svg`',
        '',
        '![Cross-Dataset Bidirectional](../assets/cross_dataset_bidirectional.svg)'
    ]) + '\n', encoding='utf-8')
    print(f'Generated {out} and {doc}')


if __name__ == '__main__':
    main()
