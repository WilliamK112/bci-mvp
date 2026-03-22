from pathlib import Path
import json


def main():
    fp = Path('outputs/robustness_results.json')
    if not fp.exists():
        print('Missing outputs/robustness_results.json')
        return

    rows = json.loads(fp.read_text(encoding='utf-8'))
    labels = [r['name'] for r in rows]
    acc = [float(r['accuracy']) for r in rows]

    W, H = 1000, 480
    m = 70
    n = len(labels)
    bw = (W - 2*m) / max(n, 1) * 0.6

    def y(v): return H - m - v * (H - 2*m)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="500" y="38" text-anchor="middle" font-size="24" font-family="Arial">Robustness under Perturbations (Accuracy)</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>',
        f'<line x1="{m}" y1="{m}" x2="{m}" y2="{H-m}" stroke="#111"/>'
    ]

    for i, (lab, v) in enumerate(zip(labels, acc)):
        gx = m + (i + 0.5) * (W - 2*m) / n
        x = gx - bw/2
        yy = y(v)
        hh = (H - m) - yy
        color = '#2563eb' if i == 0 else '#64748b'
        parts.append(f'<rect x="{x}" y="{yy}" width="{bw}" height="{hh}" fill="{color}"/>')
        parts.append(f'<text x="{gx}" y="{yy-8}" text-anchor="middle" font-size="11" font-family="Arial">{v:.3f}</text>')
        parts.append(f'<text x="{gx}" y="{H-m+18}" text-anchor="middle" font-size="11" font-family="Arial">{lab}</text>')

    parts.append('</svg>')
    out = Path('assets')
    out.mkdir(exist_ok=True)
    target = out / 'robustness_accuracy.svg'
    target.write_text('\n'.join(parts), encoding='utf-8')
    print(f'Generated {target}')


if __name__ == '__main__':
    main()
