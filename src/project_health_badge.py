"""
Generate overall project health badge from quality + compliance indexes.
"""
from pathlib import Path
import re


def extract(path, pattern):
    p = Path(path)
    if not p.exists():
        return None
    txt = p.read_text(encoding='utf-8', errors='ignore')
    m = re.search(pattern, txt)
    return float(m.group(1)) if m else None


def color(v):
    if v >= 0.9: return '#16a34a'
    if v >= 0.75: return '#2563eb'
    if v >= 0.6: return '#d97706'
    return '#dc2626'


def main():
    q = extract('docs/QUALITY_SCORECARD.md', r'\*\*Overall quality index:\*\*\s*([0-9.]+)')
    c = extract('docs/COMPLIANCE_SCORECARD.md', r'\*\*Compliance index:\*\*\s*([0-9.]+)')
    vals = [x for x in [q, c] if x is not None]
    h = sum(vals)/len(vals) if vals else 0.0

    W, H = 280, 28
    col = color(h)
    val = f"{h:.3f}" if vals else 'n/a'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">
<rect x="0" y="0" width="150" height="28" fill="#374151"/>
<rect x="150" y="0" width="130" height="28" fill="{col}"/>
<text x="75" y="19" text-anchor="middle" font-size="12" font-family="Arial" fill="white">project health</text>
<text x="215" y="19" text-anchor="middle" font-size="12" font-family="Arial" fill="white">{val}</text>
</svg>'''

    out = Path('assets/badge_project_health.svg')
    out.write_text(svg, encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
