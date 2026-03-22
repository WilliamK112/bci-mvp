"""
Generate release-ready badge from docs/RELEASE_READY_SIGNAL.md.
"""
from pathlib import Path


def main():
    sig = Path('docs/RELEASE_READY_SIGNAL.md').read_text(encoding='utf-8', errors='ignore') if Path('docs/RELEASE_READY_SIGNAL.md').exists() else ''
    ready = 'SIGNAL: READY' in sig
    val = 'READY' if ready else 'NOT_READY'
    color = '#16a34a' if ready else '#dc2626'

    W, H = 300, 28
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">
<rect x="0" y="0" width="170" height="28" fill="#374151"/>
<rect x="170" y="0" width="130" height="28" fill="{color}"/>
<text x="85" y="19" text-anchor="middle" font-size="12" font-family="Arial" fill="white">release ready</text>
<text x="235" y="19" text-anchor="middle" font-size="12" font-family="Arial" fill="white">{val}</text>
</svg>'''

    out = Path('assets/badge_release_ready.svg')
    out.write_text(svg, encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
