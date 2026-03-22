from pathlib import Path
import json


def main():
    fp = Path('outputs/calibration_results.json')
    if not fp.exists():
        print('Missing outputs/calibration_results.json')
        return
    d = json.loads(fp.read_text(encoding='utf-8'))
    xs = d.get('mean_predicted_value', [])
    ys = d.get('fraction_of_positives', [])
    if not xs or not ys:
        print('No calibration points')
        return

    W, H = 700, 520
    m = 70

    def px(v): return m + v * (W - 2*m)
    def py(v): return H - m - v * (H - 2*m)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="350" y="36" text-anchor="middle" font-size="24" font-family="Arial">Calibration Curve</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>',
        f'<line x1="{m}" y1="{m}" x2="{m}" y2="{H-m}" stroke="#111"/>',
        f'<line x1="{px(0)}" y1="{py(0)}" x2="{px(1)}" y2="{py(1)}" stroke="#9ca3af" stroke-dasharray="5,5"/>',
    ]

    # polyline
    pts = ' '.join([f"{px(x)},{py(y)}" for x, y in zip(xs, ys)])
    parts.append(f'<polyline fill="none" stroke="#2563eb" stroke-width="3" points="{pts}"/>')
    for x, y in zip(xs, ys):
      parts.append(f'<circle cx="{px(x)}" cy="{py(y)}" r="4" fill="#2563eb"/>')

    # labels
    parts.append(f'<text x="{W/2}" y="{H-20}" text-anchor="middle" font-size="13" font-family="Arial">Mean Predicted Probability</text>')
    parts.append(f'<text x="18" y="{H/2}" text-anchor="middle" font-size="13" font-family="Arial" transform="rotate(-90,18,{H/2})">Fraction of Positives</text>')
    parts.append(f'<text x="{W-m}" y="{m+15}" text-anchor="end" font-size="12" font-family="Arial">Brier={d.get("brier_score"):.4f}</text>')
    parts.append('</svg>')

    out = Path('assets')
    out.mkdir(exist_ok=True)
    target = out / 'calibration_curve.svg'
    target.write_text('\n'.join(parts), encoding='utf-8')
    print(f'Generated {target}')


if __name__ == '__main__':
    main()
