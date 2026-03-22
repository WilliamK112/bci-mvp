"""
Auto-refresh docs/HOME.md with current top-level navigation and generated timestamp.
"""
from pathlib import Path
from datetime import datetime, timezone

SECTIONS = {
    'Project Status': [
        'docs/EXECUTIVE_SUMMARY.md',
        'docs/QUALITY_SCORECARD.md',
        'docs/COMPLIANCE_SCORECARD.md',
        'docs/FINAL_RELEASE_CANDIDATE.md',
        'docs/V1_RELEASE_READY.md',
        'docs/RELEASE_READY_SIGNAL.md',
        'docs/RELEASE_READY_DIAGNOSE.md',
    ],
    'Technical Core': [
        'docs/TECHNICAL_REPORT.md',
        'docs/LIMITATIONS.md',
        'docs/MODEL_CARD.md',
        'docs/MATH_NOTATION.md',
        'docs/METHODS.md',
    ],
    'Readiness & Reliability': [
        'docs/RELEASE_READINESS.md',
        'docs/HF_SPACE_READINESS.md',
        'docs/README_QUALITY.md',
        'docs/REPORT_CONSISTENCY.md',
        'docs/ENV_COMPAT.md',
        'docs/REPRO_SNAPSHOT.md',
        'docs/ARTIFACT_HASH_MANIFEST.md',
        'docs/DOCS_FRESHNESS.md',
    ],
    'Deployment': [
        'docs/HF_PUBLISH_HELPER.md',
        'docs/HF_SPACE_STATUS.md',
        'docs/SPACE_SMOKE_TEST.md',
        'docs/DEPLOYMENT_DIAGNOSE.md',
    ],
    'Release Assets': [
        'docs/RELEASE_PACKET.md',
        'docs/FIGURE_GALLERY.md',
        'docs/release/release_en.md',
        'docs/release/release_zh.md',
    ],
}


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# BCI MVP Docs Home', '', f'Generated: {ts}', '']
    for sec, files in SECTIONS.items():
        lines += [f'## {sec}', '']
        for fp in files:
            p = Path(fp)
            mark = '✅' if p.exists() else '⬜'
            label = fp.replace('docs/', '')
            lines.append(f'- {mark} `{label}`')
        lines += ['']

    out = Path('docs/HOME.md')
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
