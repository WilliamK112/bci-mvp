"""
Generate SHA256 manifest for key published artifacts.
"""
from pathlib import Path
import hashlib
from datetime import datetime, timezone

FILES = [
    'README.md',
    'README.zh-CN.md',
    'docs/TECHNICAL_REPORT.md',
    'docs/RESULTS.md',
    'docs/ONE_PAGER.md',
    'docs/FINAL_RELEASE_CANDIDATE.md',
    'docs/QUALITY_SCORECARD.md',
    'docs/COMPLIANCE_SCORECARD.md',
    'docs/LIMITATIONS.md',
    'docs/MATH_NOTATION.md',
    'CITATION.cff',
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(8192)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# Artifact Hash Manifest', '', f'Generated: {ts}', '', '| File | SHA256 |', '|---|---|']
    for fp in FILES:
        p = Path(fp)
        if p.exists():
            lines.append(f'| `{fp}` | `{sha256(p)}` |')
        else:
            lines.append(f'| `{fp}` | `MISSING` |')

    out = Path('docs/ARTIFACT_HASH_MANIFEST.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
