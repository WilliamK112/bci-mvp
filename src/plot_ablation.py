from pathlib import Path
import json


def main():
    fp = Path('outputs/ablation_results.json')
    if not fp.exists():
        print('Missing outputs/ablation_results.json')
        return
    rows = json.loads(fp.read_text(encoding='utf-8'))
    labels = [r['setting'] for r in rows]
    vals = [float(r['accuracy']) for r in rows]

    W, H = 980, 460
    m = 70
    n = len(labels)
    bw = (W - 2*m) / max(n, 1) * 0.6
    def y(v): return H - m - v * (H - 2*m)

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">', '<rect width="100%" height="100%" fill="white"/>',
             '<text x="490" y="36" text-anchor="middle" font-size="24" font-family="Arial">Ablation Study (Accuracy)</text>',
             f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>', f'<line x1="{m}" y1="{m}" x2="{m}" y2="{H-m}" stroke="#111"/>']

    for i, (lab, v) in enumerate(zip(labels, vals)):
        gx = m + (i + 0.5) * (W - 2*m) / n
        x = gx - bw/2
        yy = y(v)
        hh = (H - m) - yy
        color = '#2563eb' if lab == 'all_features' else '#94a3b8'
        parts.append(f'<rect x="{x}" y="{yy}" width="{bw}" height="{hh}" fill="{color}"/>')
        parts.append(f'<text x="{gx}" y="{yy-8}" text-anchor="middle" font-size="11" font-family="Arial">{v:.3f}</text>')
        parts.append(f'<text x="{gx}" y="{H-m+18}" text-anchor="middle" font-size="10" font-family="Arial">{lab}</text>')

    parts.append('</svg>')
    out = Path('assets')
    out.mkdir(exist_ok=True)
    target = out / 'ablation_accuracy.svg'
    target.write_text('\n'.join(parts), encoding='utf-8')
    print(f'Generated {target}')


if __name__ == '__main__':
    main()
