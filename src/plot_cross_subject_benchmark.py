"""Plot LOSO multi-model benchmark as grouped bar chart."""
from pathlib import Path
import json


def main():
    src = Path('outputs/cross_subject_model_benchmark.json')
    if not src.exists():
        print('Missing outputs/cross_subject_model_benchmark.json')
        return
    obj = json.loads(src.read_text(encoding='utf-8'))
    ranking = obj.get('ranking', [])
    if not ranking:
        print('No ranking data')
        return

    models = [r['model'] for r in ranking]
    acc = [float(r.get('mean_accuracy', 0.0)) for r in ranking]
    f1 = [float(r.get('mean_f1', 0.0)) for r in ranking]
    auc = [float(r.get('mean_auc', 0.0)) for r in ranking]

    W, H, m = 1100, 520, 70
    n = len(models)
    group_w = (W - 2*m) / max(n, 1)
    bw = group_w * 0.22

    def y(v):
        return H - m - max(0.0, min(1.0, v)) * (H - 2*m)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="550" y="34" text-anchor="middle" font-size="24" font-family="Arial">Cross-Subject Model Benchmark (LOSO)</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>',
        f'<line x1="{m}" y1="{m}" x2="{m}" y2="{H-m}" stroke="#111"/>'
    ]

    for v in [0, 0.25, 0.5, 0.75, 1.0]:
        yy = y(v)
        parts.append(f'<line x1="{m}" y1="{yy}" x2="{W-m}" y2="{yy}" stroke="#e5e7eb"/>')
        parts.append(f'<text x="{m-8}" y="{yy+4}" text-anchor="end" font-size="10" font-family="Arial">{v:.2f}</text>')

    for i, name in enumerate(models):
        gx = m + i * group_w + group_w/2
        x0 = gx - 1.5*bw
        vals = [('acc', acc[i], '#2563eb'), ('f1', f1[i], '#16a34a'), ('auc', auc[i], '#f59e0b')]
        for k, (_, v, c) in enumerate(vals):
            x = x0 + k*bw
            yy = y(v)
            hh = (H - m) - yy
            parts.append(f'<rect x="{x}" y="{yy}" width="{bw-4}" height="{hh}" fill="{c}"/>')
            parts.append(f'<text x="{x+(bw-4)/2}" y="{yy-7}" text-anchor="middle" font-size="10" font-family="Arial">{v:.3f}</text>')
        parts.append(f'<text x="{gx}" y="{H-m+18}" text-anchor="middle" font-size="12" font-family="Arial">{name}</text>')

    parts += [
        '<rect x="760" y="52" width="12" height="12" fill="#2563eb"/>',
        '<text x="778" y="62" font-size="11" font-family="Arial">mean accuracy</text>',
        '<rect x="900" y="52" width="12" height="12" fill="#16a34a"/>',
        '<text x="918" y="62" font-size="11" font-family="Arial">mean f1</text>',
        '<rect x="990" y="52" width="12" height="12" fill="#f59e0b"/>',
        '<text x="1008" y="62" font-size="11" font-family="Arial">mean auc</text>',
        '</svg>'
    ]

    out = Path('assets/cross_subject_benchmark.svg')
    out.write_text('\n'.join(parts), encoding='utf-8')

    doc = Path('docs/CROSS_SUBJECT_BENCHMARK_VISUAL.md')
    doc.write_text('\n'.join([
        '# Cross-Subject Benchmark Visual',
        '',
        '- Source: `outputs/cross_subject_model_benchmark.json`',
        '- Visual: `assets/cross_subject_benchmark.svg`',
        '',
        '![Cross-Subject Benchmark](../assets/cross_subject_benchmark.svg)'
    ]) + '\n', encoding='utf-8')
    print(f'Generated {out} and {doc}')


if __name__ == '__main__':
    main()
