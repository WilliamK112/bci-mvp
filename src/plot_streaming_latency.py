"""Generate visualization for streaming latency benchmark."""
from pathlib import Path
import json


def main():
    p = Path('outputs/streaming_latency.json')
    if not p.exists():
        print('Missing outputs/streaming_latency.json')
        return
    d = json.loads(p.read_text(encoding='utf-8'))
    lat = d.get('latency_ms', {})
    mean = float(lat.get('mean', 0.0) or 0.0)
    p50 = float(lat.get('p50', 0.0) or 0.0)
    p95 = float(lat.get('p95', 0.0) or 0.0)
    p99 = float(lat.get('p99', 0.0) or 0.0)
    mx = float(lat.get('max', 0.0) or 0.0)

    labels = ['mean', 'p50', 'p95', 'p99', 'max']
    vals = [mean, p50, p95, p99, mx]
    vmax = max(vals) if max(vals) > 0 else 1.0

    W, H, m = 980, 460, 70
    n = len(labels)
    bw = (W - 2*m) / n * 0.55

    def y(v):
        return H - m - (v / vmax) * (H - 2*m)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="490" y="34" text-anchor="middle" font-size="24" font-family="Arial">Streaming Inference Latency (ms)</text>',
        f'<line x1="{m}" y1="{H-m}" x2="{W-m}" y2="{H-m}" stroke="#111"/>',
        f'<line x1="{m}" y1="{m}" x2="{m}" y2="{H-m}" stroke="#111"/>'
    ]

    for i, (lab, v) in enumerate(zip(labels, vals)):
        gx = m + (i + 0.5) * (W - 2*m) / n
        x = gx - bw / 2
        yy = y(v)
        hh = (H - m) - yy
        color = '#2563eb' if lab in ('mean', 'p50') else ('#f59e0b' if lab in ('p95', 'p99') else '#dc2626')
        parts.append(f'<rect x="{x}" y="{yy}" width="{bw}" height="{hh}" fill="{color}"/>')
        parts.append(f'<text x="{gx}" y="{yy-8}" text-anchor="middle" font-size="12" font-family="Arial">{v:.2f}</text>')
        parts.append(f'<text x="{gx}" y="{H-m+20}" text-anchor="middle" font-size="12" font-family="Arial">{lab}</text>')

    parts.append(f'<text x="{W-m}" y="{m+18}" text-anchor="end" font-size="12" font-family="Arial" fill="#374151">throughput={d.get("throughput_windows_per_sec",0):.2f} windows/s</text>')
    parts.append('</svg>')

    out = Path('assets/streaming_latency.svg')
    out.write_text('\n'.join(parts), encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
