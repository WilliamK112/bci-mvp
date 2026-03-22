"""Generate GO/HOLD badge from release decision gate."""
from pathlib import Path
import json


def main():
    p = Path('outputs/release_decision_gate.json')
    if not p.exists():
        raise SystemExit('Missing outputs/release_decision_gate.json')
    obj = json.loads(p.read_text(encoding='utf-8'))

    decision = str(obj.get('decision', 'HOLD')).upper()
    tag = str(obj.get('suggested_tag', 'v1.0.0-rc'))
    label = 'release-decision'
    value = f'{decision} {tag}'
    color = '#16a34a' if decision == 'GO' else '#dc2626'

    W, H = 380, 28
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" role="img" aria-label="{label}: {value}">
<linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#fff" stop-opacity=".7"/><stop offset=".1" stop-opacity=".1"/><stop offset=".9" stop-opacity=".3"/><stop offset="1" stop-opacity=".5"/></linearGradient>
<clipPath id="r"><rect width="{W}" height="{H}" rx="4" fill="#fff"/></clipPath>
<g clip-path="url(#r)"><rect width="180" height="{H}" fill="#555"/><rect x="180" width="{W-180}" height="{H}" fill="{color}"/><rect width="{W}" height="{H}" fill="url(#s)"/></g>
<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="12">
<text x="90" y="19">{label}</text><text x="280" y="19">{value}</text></g></svg>'''

    out = Path('assets/badge_release_decision.svg')
    out.write_text(svg, encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
