"""
Generate a concise real-data evidence report from local EDF assets.
Outputs: docs/REAL_DATA_EVIDENCE.md
"""
from pathlib import Path
import re
from collections import defaultdict


def collect(folder):
    root = Path(folder)
    files = sorted(root.glob('*.edf'))
    subjects = set()
    runs = defaultdict(int)
    for f in files:
        m = re.search(r'sub(\d+)', f.name)
        if m:
            sid = int(m.group(1))
            subjects.add(sid)
            runs[sid] += 1
    return files, subjects, runs


def main():
    relaxed_files, relaxed_subs, relaxed_runs = collect('data/relaxed')
    focused_files, focused_subs, focused_runs = collect('data/focused')

    shared = sorted(relaxed_subs & focused_subs)
    lines = [
        '# Real Data Evidence',
        '',
        'This project uses real EEG EDF recordings present in the repository workspace and in evaluation runs.',
        '',
        f'- Relaxed EDF files: **{len(relaxed_files)}**',
        f'- Focused EDF files: **{len(focused_files)}**',
        f'- Relaxed subjects: **{sorted(relaxed_subs)}**',
        f'- Focused subjects: **{sorted(focused_subs)}**',
        f'- Shared subjects across classes: **{shared}**',
        '',
        '## Per-subject file counts (shared subjects)',
        '',
        '| Subject | Relaxed files | Focused files |',
        '|---:|---:|---:|',
    ]
    for sid in shared:
        lines.append(f'| {sid} | {relaxed_runs.get(sid,0)} | {focused_runs.get(sid,0)} |')

    lines += [
        '',
        '## Evidence trail in pipelines',
        '- Cross-subject LOSO benchmark consumes EDF-derived feature matrices.',
        '- Cross-dataset bidirectional evaluation is computed from dataset_a/dataset_b EDF splits.',
        '- Streaming latency/stability/drift tests run inference over EDF-derived windows.',
        '',
        '## Note',
        '- This report confirms on-disk real EDF assets and subject coverage; it does not claim clinical validity.',
    ]

    out = Path('docs/REAL_DATA_EVIDENCE.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
