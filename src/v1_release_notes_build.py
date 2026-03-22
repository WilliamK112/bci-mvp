"""
Build v1.0.0 release notes draft from latest artifacts.
"""
from pathlib import Path
from datetime import datetime, timezone


def read(path):
    p=Path(path)
    return p.read_text(encoding='utf-8', errors='ignore') if p.exists() else ''


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    snap = read('docs/STATUS_SNAPSHOT.txt').strip()
    ready = 'READY' if 'ready=READY' in snap else 'NOT_READY'

    lines = [
        '# BCI MVP v1.0.0 Release Notes (Draft)',
        '',
        f'Generated: {ts}',
        '',
        f'- Release readiness: **{ready}**',
        f'- Status snapshot: `{snap}`',
        '',
        '## Highlights',
        '- Real-data pipeline run and artifact refresh',
        '- End-to-end release automation with RC gating',
        '- Space deployment reliability + status/smoke checks',
        '- Rich documentation surfaces (methods/results/limitations/provenance)',
        '',
        '## Key Assets',
        '- `docs/FINAL_RELEASE_CANDIDATE.md`',
        '- `docs/ONE_PAGER.md`',
        '- `docs/REVIEWER_PACK.md`',
        '- `docs/RELEASE_DASHBOARD.md`',
        '',
        '## Demo & Repo',
        '- Demo: https://huggingface.co/spaces/williamKang112/bci-mvp-demo',
        '- Repo: https://github.com/WilliamK112/bci-mvp',
    ]

    out = Path('docs/V1_RELEASE_NOTES.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
