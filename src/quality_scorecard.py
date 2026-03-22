"""
Generate a compact quality scorecard from key project checks.
"""
from pathlib import Path
import re
from datetime import datetime, timezone


def extract_score(path: Path):
    if not path.exists():
        return None
    txt = path.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'\*\*Score:\*\*\s*(\d+)/(\d+)', txt)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    rr = extract_score(Path('docs/RELEASE_READINESS.md'))
    hf = extract_score(Path('docs/HF_SPACE_READINESS.md'))

    rc_ok = None
    rc_cov = None
    rc = Path('docs/FINAL_RELEASE_CANDIDATE.md')
    if rc.exists():
        txt = rc.read_text(encoding='utf-8', errors='ignore')
        m1 = re.search(r'\*\*Pipeline success:\*\*\s*(\d+)/(\d+)', txt)
        m2 = re.search(r'\*\*Output coverage:\*\*\s*(\d+)/(\d+)', txt)
        if m1: rc_ok = (int(m1.group(1)), int(m1.group(2)))
        if m2: rc_cov = (int(m2.group(1)), int(m2.group(2)))

    def ratio(x):
        return (x[0] / x[1]) if x else 0.0

    dims = {
        'release_readiness': ratio(rr),
        'hf_space_readiness': ratio(hf),
        'pipeline_success': ratio(rc_ok),
        'artifact_coverage': ratio(rc_cov),
    }
    overall = sum(dims.values()) / len(dims)

    lines = [
        '# Quality Scorecard',
        '',
        f'Generated: {ts}',
        '',
        '| Dimension | Score |',
        '|---|---:|',
        f"| Release readiness | {rr[0]}/{rr[1] if rr else 1} |" if rr else '| Release readiness | n/a |',
        f"| HF Space readiness | {hf[0]}/{hf[1] if hf else 1} |" if hf else '| HF Space readiness | n/a |',
        f"| Pipeline success | {rc_ok[0]}/{rc_ok[1] if rc_ok else 1} |" if rc_ok else '| Pipeline success | n/a |',
        f"| Artifact coverage | {rc_cov[0]}/{rc_cov[1] if rc_cov else 1} |" if rc_cov else '| Artifact coverage | n/a |',
        '',
        f"**Overall quality index:** {overall:.3f}",
    ]

    out = Path('docs/QUALITY_SCORECARD.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
