"""Visualize repro run-proof artifact existence and signatures."""
from pathlib import Path
import json


def main():
    p = Path('outputs/repro_run_proof.json')
    if not p.exists():
        print('Missing outputs/repro_run_proof.json')
        return
    obj = json.loads(p.read_text(encoding='utf-8'))
    arts = obj.get('artifacts', [])
    if not arts:
        print('No artifacts in repro run proof')
        return

    W, H, m = 1080, 440, 60
    n = len(arts)
    bw = (W - 2*m) / n * 0.6

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{W//2}" y="34" text-anchor="middle" font-size="24" font-family="Arial">Repro Run Proof ({obj.get("status","-")})</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>'
    ]

    for i, r in enumerate(arts):
        ok = bool(r.get('exists', False))
        gx = m + (i + 0.5) * (W - 2*m) / n
        x = gx - bw/2
        val = 1.0 if ok else 0.0
        hh = val * (H - 2*m)
        y = H - m - hh
        color = '#16a34a' if ok else '#dc2626'
        label = str(r.get('file', f'artifact{i}')).split('/')[-1]
        parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{hh}" fill="{color}"/>')
        parts.append(f'<text x="{gx}" y="{H-m+16}" text-anchor="middle" font-size="9" font-family="Arial">{label}</text>')
        parts.append(f'<text x="{gx}" y="{y-8}" text-anchor="middle" font-size="11" font-family="Arial">{"OK" if ok else "MISS"}</text>')

    parts.append('</svg>')

    out = Path('assets/repro_run_proof.svg')
    out.write_text('\n'.join(parts), encoding='utf-8')

    doc = Path('docs/REPRO_RUN_PROOF_VISUAL.md')
    doc.write_text('\n'.join([
        '# Repro Run Proof Visual',
        '',
        '- Source: `outputs/repro_run_proof.json`',
        '- Visual: `assets/repro_run_proof.svg`',
        '',
        '![Repro Run Proof](../assets/repro_run_proof.svg)'
    ]) + '\n', encoding='utf-8')

    print(f'Generated {out} and {doc}')


if __name__ == '__main__':
    main()
