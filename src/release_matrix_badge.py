"""Generate badge from release readiness matrix overall pass/score."""
from pathlib import Path
import json


def main():
    p = Path('outputs/release_readiness_matrix.json')
    if not p.exists():
        raise SystemExit('Missing outputs/release_readiness_matrix.json')
    obj = json.loads(p.read_text(encoding='utf-8'))
    ok = bool(obj.get('all_pass', False))
    score = float(obj.get('avg_score', 0.0))

    label = 'release-matrix'
    value = f"{'PASS' if ok else 'FAIL'} {score:.2f}"
    color = '#16a34a' if ok else '#dc2626'

    W, H = 320, 28
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" role="img" aria-label="{label}: {value}">',
        '<linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#fff" stop-opacity=".7"/><stop offset=".1" stop-opacity=".1"/><stop offset=".9" stop-opacity=".3"/><stop offset="1" stop-opacity=".5"/></linearGradient>',
        '<clipPath id="r"><rect width="320" height="28" rx="4" fill="#fff"/></clipPath>',
        '<g clip-path="url(#r)">',
        '<rect width="170" height="28" fill="#555"/>',
        f'<rect x="170" width="150" height="28" fill="{color}"/>',
        '<rect width="320" height="28" fill="url(#s)"/></g>',
        '<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="12">',
        f'<text x="85" y="19">{label}</text>',
        f'<text x="245" y="19">{value}</text>',
        '</g></svg>'
    ]

    out = Path('assets/badge_release_matrix.svg')
    out.write_text(''.join(parts), encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
