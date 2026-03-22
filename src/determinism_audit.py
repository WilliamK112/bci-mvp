"""
Audit determinism hygiene across core training/eval scripts.
Checks for explicit random_state/seed usage in key files.
Outputs docs/DETERMINISM_AUDIT.md
"""
from pathlib import Path
import re

TARGETS = [
    'src/train.py',
    'src/benchmark.py',
    'src/cross_dataset_eval.py',
    'src/cross_subject_eval.py',
    'src/cross_subject_model_benchmark.py',
    'src/bootstrap_ci.py',
    'src/cross_subject_ci.py',
    'src/permutation_explain.py',
    'src/validate_streaming_latency.py',
    'src/streaming_stability_test.py',
]

PATTERNS = [
    r'\brandom_state\s*=\s*\d+',
    r'\bseed\s*=\s*\d+',
    r'np\.random\.seed\(',
    r'random\.seed\(',
]


def file_check(path: Path):
    if not path.exists():
        return {'exists': False, 'deterministic': False, 'matches': []}
    txt = path.read_text(encoding='utf-8', errors='ignore')
    matches = []
    for p in PATTERNS:
        if re.search(p, txt):
            matches.append(p)
    return {
        'exists': True,
        'deterministic': len(matches) > 0,
        'matches': matches,
    }


def main():
    rows = []
    for t in TARGETS:
        info = file_check(Path(t))
        rows.append((t, info))

    existing = [r for r in rows if r[1]['exists']]
    passed = all(info['deterministic'] for _, info in existing)

    lines = [
        '# Determinism Audit',
        '',
        f'- Checked files: **{len(TARGETS)}**',
        f'- Existing files: **{len(existing)}**',
        f'- Overall: **{"PASS" if passed else "FAIL"}**',
        '',
        '| File | Exists | Determinism Signal | Evidence |',
        '|---|---:|---:|---|',
    ]

    for fp, info in rows:
        ev = ', '.join(info['matches']) if info['matches'] else '-'
        lines.append(f"| {fp} | {'✅' if info['exists'] else '❌'} | {'✅' if info['deterministic'] else '❌'} | {ev} |")

    lines += [
        '',
        'Interpretation:',
        '- PASS means every existing target file has at least one explicit seed/random_state signal.',
        '- This is a static hygiene audit; it complements runtime reproducibility checks.',
    ]

    out = Path('docs/DETERMINISM_AUDIT.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out} (overall={"PASS" if passed else "FAIL"})')

    if not passed:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
