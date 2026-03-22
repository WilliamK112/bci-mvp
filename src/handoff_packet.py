"""
Generate a concise handoff packet for another operator/agent.
"""
from pathlib import Path
from datetime import datetime, timezone


def main():
    ts=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines=[
        '# Handoff Packet',
        '',
        f'Generated: {ts}',
        '',
        '## Current State',
        '- Release signal: see `docs/RELEASE_READY_SIGNAL.md`',
        '- Launch state: see `docs/LAUNCH_STATUS.md`',
        '- Final gate: see `docs/FINAL_RELEASE_CANDIDATE.md`',
        '',
        '## Where to start',
        '- Operational links: `docs/OPERATOR_QUICKLINKS.md`',
        '- One-page summary: `docs/ONE_PAGER.md`',
        '- Reviewer pack: `docs/REVIEWER_PACK.md`',
        '',
        '## Immediate Commands',
        '```bash',
        'python src/run_full_pipeline.py',
        'python src/final_release_candidate.py',
        'python src/release_dashboard.py',
        '```',
    ]
    out=Path('docs/HANDOFF_PACKET.md')
    out.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(f'Generated {out}')

if __name__=='__main__':
    main()
