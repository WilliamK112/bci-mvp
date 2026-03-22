"""
Generate governance matrix mapping checks to owning artifacts.
"""
from pathlib import Path
from datetime import datetime, timezone

ROWS = [
    ('Release readiness', 'docs/RELEASE_READY_SIGNAL.md', 'src/release_ready_signal.py'),
    ('Release guard', 'docs/RELEASE_GUARD_REPORT.md', 'src/release_guard_report.py'),
    ('Launch status', 'docs/LAUNCH_STATUS.md', 'src/launch_status.py'),
    ('Secrets hygiene', 'docs/SECRETS_HYGIENE.md', 'src/secrets_hygiene_check.py'),
    ('Compliance', 'docs/COMPLIANCE_SCORECARD.md', 'src/compliance_scorecard.py'),
    ('Quality', 'docs/QUALITY_SCORECARD.md', 'src/quality_scorecard.py'),
    ('Data provenance', 'docs/DATA_PROVENANCE.md', 'src/data_provenance.py'),
]


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# Governance Matrix', '', f'Generated: {ts}', '', '| Control Area | Artifact | Generator | Status |', '|---|---|---|---|']
    for area, art, gen in ROWS:
        status = '✅' if Path(art).exists() else '⬜'
        lines.append(f'| {area} | `{art}` | `{gen}` | {status} |')

    out = Path('docs/GOVERNANCE_MATRIX.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
