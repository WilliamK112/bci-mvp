"""
Generate archive manifest listing files to include in a release bundle zip.
"""
from pathlib import Path
from datetime import datetime, timezone

FILES = [
    'README.md',
    'README.zh-CN.md',
    'CITATION.cff',
    'docs/ONE_PAGER.md',
    'docs/TECHNICAL_REPORT.md',
    'docs/RESULTS.md',
    'docs/REVIEWER_PACK.md',
    'docs/FINAL_RELEASE_CANDIDATE.md',
    'docs/RELEASE_DASHBOARD.md',
    'docs/RELEASE_READY_SIGNAL.md',
    'docs/V1_RELEASE_NOTES.md',
    'assets/readme_banner.svg',
    'assets/cross_dataset_matrix.svg',
    'assets/all_model_comparison.svg',
    'assets/calibration_curve.svg',
]


def main():
    ts=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines=['# Release Archive Manifest','',f'Generated: {ts}','']
    for f in FILES:
        lines.append(f"- {'✅' if Path(f).exists() else '⬜'} `{f}`")

    lines += ['', '## Packaging command (example)', '```bash', 'zip -r bci-mvp-v1-release.zip README.md README.zh-CN.md CITATION.cff docs assets', '```']

    out=Path('docs/RELEASE_ARCHIVE_MANIFEST.md')
    out.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__=='__main__':
    main()
