"""Visualize LOSO seed sensitivity for RF/MLP."""
from pathlib import Path
import json


def main():
    p = Path('outputs/cross_subject_seed_sensitivity.json')
    if not p.exists():
        print('Missing outputs/cross_subject_seed_sensitivity.json')
        return
    obj = json.loads(p.read_text(encoding='utf-8'))
    seeds = obj.get('seeds', [])
    models = obj.get('models', {})
    rf = (models.get('rf') or {}).get('seed_scores', [])
    mlp = (models.get('mlp') or {}).get('seed_scores', [])
    n = min(len(seeds), len(rf), len(mlp))
    if n == 0:
        print('No seed-score data')
        return

    W, H, m = 980, 460, 70
    def x(i):
        return m + i * (W - 2*m) / max(1, n-1)
    def y(v):
        return H - m - max(0.0, min(1.0, v)) * (H - 2*m)

    pts_rf = ' '.join(f"{x(i)},{y(float(rf[i]))}" for i in range(n))
    pts_mlp = ' '.join(f"{x(i)},{y(float(mlp[i]))}" for i in range(n))

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="490" y="34" text-anchor="middle" font-size="24" font-family="Arial">Cross-Subject Seed Sensitivity</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>',
        f'<line x1="{m}" y1="{m}" x2="{m}" y2="{H-m}" stroke="#111"/>',
        f'<polyline points="{pts_rf}" fill="none" stroke="#2563eb" stroke-width="3"/>',
        f'<polyline points="{pts_mlp}" fill="none" stroke="#16a34a" stroke-width="3"/>'
    ]

    for i in range(n):
        parts.append(f'<text x="{x(i)}" y="{H-m+18}" text-anchor="middle" font-size="10" font-family="Arial">{seeds[i]}</text>')

    parts += [
        '<rect x="760" y="52" width="12" height="12" fill="#2563eb"/>',
        '<text x="778" y="62" font-size="11" font-family="Arial">RF</text>',
        '<rect x="820" y="52" width="12" height="12" fill="#16a34a"/>',
        '<text x="838" y="62" font-size="11" font-family="Arial">MLP</text>',
        '</svg>'
    ]

    out = Path('assets/cross_subject_seed_sensitivity.svg')
    out.write_text('\n'.join(parts), encoding='utf-8')

    doc = Path('docs/CROSS_SUBJECT_SEED_SENSITIVITY_VISUAL.md')
    doc.write_text('\n'.join([
        '# Cross-Subject Seed Sensitivity Visual',
        '',
        '- Source: `outputs/cross_subject_seed_sensitivity.json`',
        '- Visual: `assets/cross_subject_seed_sensitivity.svg`',
        '',
        '![Seed Sensitivity](../assets/cross_subject_seed_sensitivity.svg)'
    ]) + '\n', encoding='utf-8')
    print(f'Generated {out} and {doc}')


if __name__ == '__main__':
    main()
