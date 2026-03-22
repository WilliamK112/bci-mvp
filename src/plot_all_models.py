"""
Plot unified model comparison from outputs/all_model_results.csv.
"""
from pathlib import Path
import csv


def read_rows(path: Path):
    if not path.exists():
        return []
    with path.open('r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def to_float(v, default=0.0):
    try:
        return float(v)
    except Exception:
        return default


def generate_svg(labels, accs, f1s, aucs, outpath: Path):
    W, H = 1100, 520
    margin = 80
    chart_h = H - 2 * margin
    chart_w = W - 2 * margin

    n = len(labels)
    group_w = chart_w / max(n, 1)
    bar_w = min(40, group_w / 5)

    def y(v):
        return H - margin - v * chart_h

    colors = {
        'ACC': '#2563eb',
        'F1': '#16a34a',
        'AUC': '#dc2626',
    }

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{W/2}" y="40" text-anchor="middle" font-size="28" font-family="Arial">Unified Model Comparison</text>',
        f'<line x1="{margin}" y1="{H-margin}" x2="{W-margin}" y2="{H-margin}" stroke="#111"/>',
        f'<line x1="{margin}" y1="{margin}" x2="{margin}" y2="{H-margin}" stroke="#111"/>',
    ]

    # y ticks
    for t in [0, 0.25, 0.5, 0.75, 1.0]:
        yy = y(t)
        parts.append(f'<line x1="{margin-5}" y1="{yy}" x2="{W-margin}" y2="{yy}" stroke="#eee"/>')
        parts.append(f'<text x="{margin-10}" y="{yy+5}" text-anchor="end" font-size="12" font-family="Arial">{t:.2f}</text>')

    for i, label in enumerate(labels):
        gx = margin + i * group_w + group_w * 0.2
        vals = [('ACC', accs[i]), ('F1', f1s[i]), ('AUC', aucs[i])]
        for j, (name, val) in enumerate(vals):
            bx = gx + j * (bar_w + 6)
            by = y(val)
            bh = (H - margin) - by
            parts.append(f'<rect x="{bx}" y="{by}" width="{bar_w}" height="{bh}" fill="{colors[name]}"/>')
        parts.append(f'<text x="{gx+bar_w+8}" y="{H-margin+22}" text-anchor="middle" font-size="12" font-family="Arial">{label}</text>')

    # legend
    lx = W - margin - 180
    ly = margin + 10
    for k, name in enumerate(['ACC', 'F1', 'AUC']):
        parts.append(f'<rect x="{lx}" y="{ly + k*24}" width="14" height="14" fill="{colors[name]}"/>')
        parts.append(f'<text x="{lx+22}" y="{ly + 12 + k*24}" font-size="13" font-family="Arial">{name}</text>')

    parts.append('</svg>')
    outpath.write_text('\n'.join(parts), encoding='utf-8')


def main():
    out = Path('outputs/all_model_results.csv')
    rows = read_rows(out)
    if not rows:
        print('Missing outputs/all_model_results.csv')
        return

    labels = [r.get('model', 'M') for r in rows]
    accs = [to_float(r.get('accuracy')) for r in rows]
    f1s = [to_float(r.get('f1')) for r in rows]
    aucs = [to_float(r.get('auc')) for r in rows]

    assets = Path('assets')
    assets.mkdir(exist_ok=True)
    target = assets / 'all_model_comparison.svg'
    generate_svg(labels, accs, f1s, aucs, target)
    print(f'Generated {target}')


if __name__ == '__main__':
    main()
