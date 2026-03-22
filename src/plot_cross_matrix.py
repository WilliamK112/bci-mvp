"""
Render cross-dataset matrix heatmap SVG from outputs/cross_dataset_matrix.json.
"""
from pathlib import Path
import json


def to_color(v: float) -> str:
    # blue gradient from light to deep
    v = max(0.0, min(1.0, v))
    c = int(255 - 140 * v)
    return f"rgb({c},{c+10},{255})"


def main():
    fp = Path('outputs/cross_dataset_matrix.json')
    if not fp.exists():
        print('Missing outputs/cross_dataset_matrix.json')
        return

    data = json.loads(fp.read_text(encoding='utf-8'))
    ds = data.get('datasets', [])
    rows = data.get('results', [])
    if not ds or not rows:
        print('No data in matrix json')
        return

    idx = {d: i for i, d in enumerate(ds)}
    n = len(ds)
    mat = [[None for _ in range(n)] for _ in range(n)]
    for r in rows:
        i = idx[r['train']]
        j = idx[r['test']]
        mat[i][j] = float(r.get('accuracy', 0.0))

    cell = 80
    margin = 140
    W = margin + n * cell + 60
    H = margin + n * cell + 80

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
         '<rect width="100%" height="100%" fill="white"/>',
         f'<text x="{W/2}" y="40" text-anchor="middle" font-size="24" font-family="Arial">Cross-Dataset Accuracy Matrix</text>',
         f'<text x="{W/2}" y="66" text-anchor="middle" font-size="14" font-family="Arial" fill="#555">rows=train, cols=test</text>']

    # labels
    for i, d in enumerate(ds):
        x = margin + i * cell + cell / 2
        y = margin - 10
        s.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-size="12" font-family="Arial">{d}</text>')
        y2 = margin + i * cell + cell / 2 + 4
        s.append(f'<text x="{margin-10}" y="{y2}" text-anchor="end" font-size="12" font-family="Arial">{d}</text>')

    # cells
    for i in range(n):
        for j in range(n):
            x = margin + j * cell
            y = margin + i * cell
            val = mat[i][j]
            if i == j:
                fill = '#f3f4f6'
                txt = '—'
            elif val is None:
                fill = '#fee2e2'
                txt = 'NA'
            else:
                fill = to_color(val)
                txt = f'{val:.2f}'
            s.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{fill}" stroke="#d1d5db"/>')
            s.append(f'<text x="{x+cell/2}" y="{y+cell/2+4}" text-anchor="middle" font-size="14" font-family="Arial">{txt}</text>')

    s.append('</svg>')

    out = Path('assets')
    out.mkdir(exist_ok=True)
    target = out / 'cross_dataset_matrix.svg'
    target.write_text('\n'.join(s), encoding='utf-8')
    print(f'Generated {target}')


if __name__ == '__main__':
    main()
