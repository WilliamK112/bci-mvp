"""Create channel x band explainability heatmap SVG from permutation outputs."""
from pathlib import Path
import pandas as pd

BANDS = ["delta", "theta", "alpha", "beta"]


def main():
    src = Path('outputs/permutation_importance_detailed.csv')
    if not src.exists():
        print('Missing outputs/permutation_importance_detailed.csv')
        return

    df = pd.read_csv(src)
    if df.empty:
        print('Empty permutation importance file')
        return

    n_features = len(df)
    if n_features % 4 != 0:
        print('Feature count not divisible by 4; skip heatmap')
        return

    n_channels = n_features // 4
    vals = [[0.0 for _ in BANDS] for __ in range(n_channels)]

    for _, r in df.iterrows():
        idx = int(r['feature_idx'])
        ch = idx // 4
        bi = idx % 4
        if ch < n_channels and bi < 4:
            vals[ch][bi] = float(r['importance_mean'])

    flat = [v for row in vals for v in row]
    vmin, vmax = min(flat), max(flat)
    span = (vmax - vmin) if vmax != vmin else 1.0

    def color(v):
        t = (v - vmin) / span
        # blue -> cyan -> yellow
        r = int(20 + 235 * t)
        g = int(70 + 170 * t)
        b = int(180 - 150 * t)
        return f'#{r:02x}{g:02x}{b:02x}'

    cw, chh = 95, 36
    left, top = 120, 80
    W = left + 4 * cw + 120
    H = top + n_channels * chh + 90

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="50%" y="34" text-anchor="middle" font-size="24" font-family="Arial">Explainability Heatmap (Permutation Importance)</text>',
    ]

    for j, b in enumerate(BANDS):
        x = left + j * cw + cw/2
        parts.append(f'<text x="{x}" y="{top-16}" text-anchor="middle" font-size="13" font-family="Arial">{b}</text>')

    for i in range(n_channels):
        y = top + i * chh
        parts.append(f'<text x="{left-10}" y="{y+24}" text-anchor="end" font-size="12" font-family="Arial">ch{i}</text>')
        for j in range(4):
            x = left + j * cw
            v = vals[i][j]
            parts.append(f'<rect x="{x}" y="{y}" width="{cw-2}" height="{chh-2}" fill="{color(v)}"/>')
            parts.append(f'<text x="{x+cw/2}" y="{y+23}" text-anchor="middle" font-size="10" font-family="Arial" fill="#111">{v:.3f}</text>')

    parts.append(f'<text x="{left}" y="{H-24}" font-size="12" font-family="Arial" fill="#444">min={vmin:.4f} max={vmax:.4f}</text>')
    parts.append('</svg>')

    out = Path('assets/explainability_heatmap.svg')
    out.write_text('\n'.join(parts), encoding='utf-8')

    doc = Path('docs/EXPLAINABILITY_HEATMAP.md')
    doc.write_text('\n'.join([
        '# Explainability Heatmap',
        '',
        '- Source: `outputs/permutation_importance_detailed.csv`',
        '- Visualization: `assets/explainability_heatmap.svg`',
        '',
        '![Explainability Heatmap](../assets/explainability_heatmap.svg)',
    ]) + '\n', encoding='utf-8')

    print(f'Generated {out} and {doc}')


if __name__ == '__main__':
    main()
