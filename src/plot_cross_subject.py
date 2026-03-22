"""
Plot LOSO cross-subject results from outputs/cross_subject_results.json.
"""
from pathlib import Path
import json


def main():
    src = Path('outputs/cross_subject_results.json')
    if not src.exists():
        print('Missing outputs/cross_subject_results.json')
        return

    d = json.loads(src.read_text(encoding='utf-8'))
    rows = d.get('per_subject', [])
    if not rows:
        print('No per_subject rows')
        return

    labels = [f"sub{r['test_subject']}" for r in rows]
    vals = [float(r['accuracy']) for r in rows]

    W, H = 980, 460
    m = 70
    n = len(labels)
    bw = (W - 2*m) / max(n, 1) * 0.6

    def y(v):
        return H - m - v * (H - 2*m)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="490" y="36" text-anchor="middle" font-size="24" font-family="Arial">Cross-Subject LOSO Accuracy</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>',
        f'<line x1="{m}" y1="{m}" x2="{m}" y2="{H-m}" stroke="#111"/>'
    ]

    for i, (lab, v) in enumerate(zip(labels, vals)):
        gx = m + (i + 0.5) * (W - 2*m) / n
        x = gx - bw/2
        yy = y(v)
        hh = (H - m) - yy
        parts.append(f'<rect x="{x}" y="{yy}" width="{bw}" height="{hh}" fill="#2563eb"/>')
        parts.append(f'<text x="{gx}" y="{yy-8}" text-anchor="middle" font-size="11" font-family="Arial">{v:.3f}</text>')
        parts.append(f'<text x="{gx}" y="{H-m+18}" text-anchor="middle" font-size="11" font-family="Arial">{lab}</text>')

    mean_acc = float(d.get('mean_accuracy', 0.0))
    ymean = y(mean_acc)
    parts.append(f'<line x1="{m}" y1="{ymean}" x2="{W-m}" y2="{ymean}" stroke="#dc2626" stroke-dasharray="6,4"/>')
    parts.append(f'<text x="{W-m}" y="{ymean-6}" text-anchor="end" font-size="12" font-family="Arial" fill="#dc2626">mean={mean_acc:.3f}</text>')

    parts.append('</svg>')

    out = Path('assets/cross_subject_loso.svg')
    out.write_text('\n'.join(parts), encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
