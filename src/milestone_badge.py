"""
Generate milestone badge from docs/MILESTONE_STAMP.md.
"""
from pathlib import Path


def main():
    txt = Path('docs/MILESTONE_STAMP.md').read_text(encoding='utf-8', errors='ignore') if Path('docs/MILESTONE_STAMP.md').exists() else ''
    v1 = 'MILESTONE: V1_READY' in txt
    label = 'V1_READY' if v1 else 'IN_PROGRESS'
    color = '#16a34a' if v1 else '#d97706'

    W,H = 280,28
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">
<rect x="0" y="0" width="150" height="28" fill="#374151"/>
<rect x="150" y="0" width="130" height="28" fill="{color}"/>
<text x="75" y="19" text-anchor="middle" font-size="12" font-family="Arial" fill="white">milestone</text>
<text x="215" y="19" text-anchor="middle" font-size="12" font-family="Arial" fill="white">{label}</text>
</svg>'''
    out=Path('assets/badge_milestone.svg')
    out.write_text(svg,encoding='utf-8')
    print(f'Generated {out}')

if __name__=='__main__':
    main()
