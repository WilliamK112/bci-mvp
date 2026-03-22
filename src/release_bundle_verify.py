"""
Verify latest release bundle exists and emit checksum report.
"""
from pathlib import Path
import hashlib


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    latest_ptr = Path('dist/latest-bundle.txt')
    if not latest_ptr.exists():
        raise SystemExit('Missing dist/latest-bundle.txt')
    name = latest_ptr.read_text(encoding='utf-8').strip()
    bundle = Path('dist') / name
    if not bundle.exists():
        raise SystemExit(f'Bundle file not found: {bundle}')

    digest = sha256(bundle)
    out = Path('docs/RELEASE_BUNDLE_VERIFY.md')
    out.write_text(
        '\n'.join([
            '# Release Bundle Verify',
            '',
            f'- Bundle: `{bundle}`',
            f'- SHA256: `{digest}`',
            '- Status: PASS',
        ]) + '\n',
        encoding='utf-8'
    )
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
