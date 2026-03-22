"""
Generate simple local SVG status badges from docs/readiness scores.
"""
from pathlib import Path
import re


def extract_score(path: Path):
    if not path.exists():
        return None
    txt = path.read_text(encoding='utf-8')
    m = re.search(r'\*\*Score:\*\*\s*(\d+)/(\d+)', txt)
    if not m:
        return None
    a, b = int(m.group(1)), int(m.group(2))
    return a, b


def badge(label, value, color, out):
    W, H = 260, 28
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect x="0" y="0" width="130" height="28" fill="#374151"/>',
        f'<rect x="130" y="0" width="130" height="28" fill="{color}"/>',
        f'<text x="65" y="19" text-anchor="middle" font-size="12" font-family="Arial" fill="white">{label}</text>',
        f'<text x="195" y="19" text-anchor="middle" font-size="12" font-family="Arial" fill="white">{value}</text>',
        '</svg>'
    ]
    out.write_text('\n'.join(parts), encoding='utf-8')


def color_for_ratio(a, b):
    r = a / b if b else 0
    if r >= 0.9:
        return '#16a34a'
    if r >= 0.7:
        return '#2563eb'
    if r >= 0.5:
        return '#d97706'
    return '#dc2626'


def main():
    assets = Path('assets'); assets.mkdir(exist_ok=True)
    pairs = [
        ('release readiness', Path('docs/RELEASE_READINESS.md'), assets / 'badge_release_readiness.svg'),
        ('hf space readiness', Path('docs/HF_SPACE_READINESS.md'), assets / 'badge_hf_readiness.svg'),
    ]

    for label, src, out in pairs:
        sc = extract_score(src)
        if sc is None:
            badge(label, 'n/a', '#6b7280', out)
        else:
            a, b = sc
            badge(label, f'{a}/{b}', color_for_ratio(a, b), out)
        print(f'Generated {out}')


if __name__ == '__main__':
    main()
