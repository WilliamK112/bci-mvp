"""Plot trend lines from docs/STATUS_HISTORY.csv."""
from pathlib import Path
import csv


def parse_ratio(s):
    try:
        a,b=s.split('/')
        a=float(a); b=float(b)
        return a/b if b else 0.0
    except Exception:
        return None


def main():
    src = Path('docs/STATUS_HISTORY.csv')
    if not src.exists():
        print('Missing docs/STATUS_HISTORY.csv')
        return

    rows = []
    with src.open('r', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append(r)
    if not rows:
        print('No rows')
        return

    labels = [r.get('recorded_at_utc','')[-8:] for r in rows]
    qvals = []
    pvals = []
    cvals = []
    for r in rows:
        try:
            qvals.append(float(r.get('quality','0') or 0))
        except Exception:
            qvals.append(0.0)
        pvals.append(parse_ratio(r.get('pipeline','')) or 0.0)
        cvals.append(parse_ratio(r.get('coverage','')) or 0.0)

    W,H=1024,480
    m=70
    n=max(len(rows),2)

    def x(i):
        return m + i*(W-2*m)/(n-1)
    def y(v):
        return H-m - v*(H-2*m)

    def poly(vals,color,name,offset=0):
        pts=' '.join(f"{x(i)},{y(max(0,min(1,v)))}" for i,v in enumerate(vals))
        return [
            f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3"/>',
            f'<text x="{W-m}" y="{m+18+offset}" text-anchor="end" font-size="12" font-family="Arial" fill="{color}">{name}</text>'
        ]

    parts=[
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="512" y="34" text-anchor="middle" font-size="24" font-family="Arial">Release Readiness Trend</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>',
        f'<line x1="{m}" y1="{m}" x2="{m}" y2="{H-m}" stroke="#111"/>'
    ]

    for i,lab in enumerate(labels):
        if i % max(1, len(labels)//6) == 0 or i==len(labels)-1:
            parts.append(f'<text x="{x(i)}" y="{H-m+18}" text-anchor="middle" font-size="10" font-family="Arial">{lab}</text>')

    for v in [0.0,0.25,0.5,0.75,1.0]:
        yy=y(v)
        parts.append(f'<line x1="{m}" y1="{yy}" x2="{W-m}" y2="{yy}" stroke="#e5e7eb"/>')
        parts.append(f'<text x="{m-10}" y="{yy+4}" text-anchor="end" font-size="10" font-family="Arial">{v:.2f}</text>')

    parts += poly(qvals, '#2563eb', 'quality', 0)
    parts += poly(pvals, '#16a34a', 'pipeline completion', 16)
    parts += poly(cvals, '#dc2626', 'coverage completion', 32)

    parts.append('</svg>')

    out = Path('assets/status_history_trend.svg')
    out.write_text('\n'.join(parts), encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
