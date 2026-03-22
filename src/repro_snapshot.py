"""
Generate reproducibility snapshot: python version, key file hashes, and git revision.
"""
from pathlib import Path
import hashlib
import platform
import subprocess
from datetime import datetime, timezone

KEY_FILES = [
    'requirements.txt',
    'src/train.py',
    'src/preprocess.py',
    'src/run_full_pipeline.py',
    'src/final_release_candidate.py',
    'README.md',
]


def sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def git_rev():
    p = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else 'unknown'


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        '# Reproducibility Snapshot',
        '',
        f'Generated: {ts}',
        f'- Git revision: `{git_rev()}`',
        f'- Python: `{platform.python_version()}`',
        f'- Platform: `{platform.platform()}`',
        '',
        '## File Hashes (SHA256)',
        '',
        '| File | SHA256 |',
        '|---|---|',
    ]

    for fp in KEY_FILES:
        p = Path(fp)
        if p.exists():
            lines.append(f'| `{fp}` | `{sha256_file(p)}` |')
        else:
            lines.append(f'| `{fp}` | `MISSING` |')

    out = Path('docs/REPRO_SNAPSHOT.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
