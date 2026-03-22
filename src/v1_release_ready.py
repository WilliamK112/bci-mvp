"""
Generate v1.0.0 release readiness summary from current READY signal.
"""
from pathlib import Path
from datetime import datetime, timezone


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    signal = Path('docs/RELEASE_READY_SIGNAL.md').read_text(encoding='utf-8', errors='ignore') if Path('docs/RELEASE_READY_SIGNAL.md').exists() else ''
    ready = 'SIGNAL: READY' in signal

    lines = [
        '# v1.0.0 Release Readiness',
        '',
        f'Generated: {ts}',
        '',
        f'- Ready signal: **{"READY" if ready else "NOT_READY"}**',
        '- Core docs: `docs/ONE_PAGER.md`, `docs/TECHNICAL_REPORT.md`, `docs/RESULTS.md`',
        '- Final gate: `docs/FINAL_RELEASE_CANDIDATE.md`',
        '- Reviewer pack: `docs/REVIEWER_PACK.md`',
        '- Demo: https://huggingface.co/spaces/williamKang112/bci-mvp-demo',
        '',
        '## Suggested release steps',
        '1. Create git tag `v1.0.0`',
        '2. Publish GitHub release notes from `docs/RELEASE_NOTES_LATEST.md`',
        '3. Share `docs/ONE_PAGER.md` + `docs/REVIEWER_PACK.md` externally',
    ]

    out = Path('docs/V1_RELEASE_READY.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
