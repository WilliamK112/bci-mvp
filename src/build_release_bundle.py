"""
Build a distributable release bundle zip from manifest-defined assets.
"""
from pathlib import Path
from datetime import datetime, timezone
import zipfile

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
    'docs/V1_RELEASE_NOTES.md',
    'docs/RELEASE_SUMMARY.json',
    'docs/RELEASE_SUMMARY_VALIDATION.md',
    'assets/readme_banner.svg',
    'assets/cross_dataset_matrix.svg',
    'assets/cross_subject_loso.svg',
    'assets/all_model_comparison.svg',
    'assets/calibration_curve.svg',
]


def main():
    ts = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    dist = Path('dist')
    dist.mkdir(exist_ok=True)
    out = dist / f'bci-mvp-v1-bundle-{ts}.zip'

    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for f in FILES:
            p = Path(f)
            if p.exists():
                zf.write(p, arcname=f)

    latest = dist / 'latest-bundle.txt'
    latest.write_text(str(out.name) + '\n', encoding='utf-8')

    report = Path('docs/RELEASE_BUNDLE_BUILD.md')
    report.write_text(
        '\n'.join([
            '# Release Bundle Build',
            '',
            f'- Output: `{out}`',
            f'- Latest pointer: `dist/latest-bundle.txt`',
        ]) + '\n',
        encoding='utf-8'
    )

    print(f'Built {out}')


if __name__ == '__main__':
    main()
