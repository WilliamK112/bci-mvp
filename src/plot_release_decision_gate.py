"""Visualize release decision gate checks."""
from pathlib import Path
import json


def main():
    p = Path('outputs/release_decision_gate.json')
    if not p.exists():
        print('Missing outputs/release_decision_gate.json')
        return
    obj = json.loads(p.read_text(encoding='utf-8'))
    checks = obj.get('checks', {})
    items = list(checks.items())
    if not items:
        print('No checks')
        return

    W, H, m = 1080, 420, 60
    n = len(items)
    bw = (W - 2*m) / n * 0.65

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{W//2}" y="34" text-anchor="middle" font-size="24" font-family="Arial">Release Decision Gate ({obj.get("decision","-")})</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>'
    ]

    for i, (k, v) in enumerate(items):
        gx = m + (i + 0.5) * (W - 2*m) / n
        x = gx - bw/2
        val = 1.0 if v else 0.0
        hh = val * (H - 2*m)
        y = H - m - hh
        color = '#16a34a' if v else '#dc2626'
        parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{hh}" fill="{color}"/>')
        parts.append(f'<text x="{gx}" y="{H-m+18}" text-anchor="middle" font-size="10" font-family="Arial">{k}</text>')
        parts.append(f'<text x="{gx}" y="{y-8}" text-anchor="middle" font-size="12" font-family="Arial">{"PASS" if v else "FAIL"}</text>')

    parts.append('</svg>')

    out = Path('assets/release_decision_gate.svg')
    out.write_text('\n'.join(parts), encoding='utf-8')

    doc = Path('docs/RELEASE_DECISION_GATE_VISUAL.md')
    doc.write_text('\n'.join([
        '# Release Decision Gate Visual',
        '',
        '- Source: `outputs/release_decision_gate.json`',
        '- Visual: `assets/release_decision_gate.svg`',
        '',
        '![Release Decision Gate](../assets/release_decision_gate.svg)'
    ]) + '\n', encoding='utf-8')

    print(f'Generated {out} and {doc}')


if __name__ == '__main__':
    main()
