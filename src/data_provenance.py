"""
Generate dataset provenance summary from local data folders.
"""
from pathlib import Path
from datetime import datetime, timezone


def count_files(path):
    p=Path(path)
    return len(list(p.glob('*.edf'))) if p.exists() else 0


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    relaxed = count_files('data/relaxed')
    focused = count_files('data/focused')
    da_r = count_files('data/dataset_a/relaxed')
    da_f = count_files('data/dataset_a/focused')
    db_r = count_files('data/dataset_b/relaxed')
    db_f = count_files('data/dataset_b/focused')

    lines = [
        '# Data Provenance',
        '',
        f'Generated: {ts}',
        '',
        '## Sources',
        '- Public bootstrap source: EEGBCI / PhysioNet (via MNE dataset fetch script)',
        '- Conversion script: `src/fetch_public_eeg_data.py`',
        '',
        '## Local Dataset Inventory',
        f'- `data/relaxed`: {relaxed} EDF files',
        f'- `data/focused`: {focused} EDF files',
        f'- `data/dataset_a/relaxed`: {da_r} EDF files',
        f'- `data/dataset_a/focused`: {da_f} EDF files',
        f'- `data/dataset_b/relaxed`: {db_r} EDF files',
        f'- `data/dataset_b/focused`: {db_f} EDF files',
        '',
        '## Notes',
        '- Current relaxed/focused labels are pragmatic task-mapping for MVP verification, not clinical labels.',
        '- Replace with task-validated labels for production-grade claims.',
    ]

    out = Path('docs/DATA_PROVENANCE.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
