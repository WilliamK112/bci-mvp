"""
Reproducibility check for LOSO cross-subject benchmark.
Runs benchmark twice and verifies ranking + winner consistency.
Outputs:
- docs/REPRO_CROSS_SUBJECT.md
"""
from pathlib import Path
import json
import subprocess
import hashlib
import os


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def run_benchmark():
    env = os.environ.copy()
    env['PYTHONPATH'] = env.get('PYTHONPATH', '.')
    subprocess.run(['python', 'src/cross_subject_model_benchmark.py'], check=True, env=env)
    p = Path('outputs/cross_subject_model_benchmark.json')
    raw = p.read_text(encoding='utf-8')
    obj = json.loads(raw)
    ranking = obj.get('ranking', [])
    winner = obj.get('winner')
    compact = json.dumps({'winner': winner, 'ranking': ranking}, sort_keys=True)
    return winner, ranking, sha256_text(compact)


def main():
    w1, r1, h1 = run_benchmark()
    w2, r2, h2 = run_benchmark()

    same_winner = (w1 == w2)
    same_ranking = (r1 == r2)
    same_hash = (h1 == h2)
    passed = same_winner and same_ranking and same_hash

    lines = [
        '# Reproducibility Check: Cross-Subject Benchmark',
        '',
        f'- Run1 winner: **{w1}**',
        f'- Run2 winner: **{w2}**',
        f'- Winner consistent: **{"YES" if same_winner else "NO"}**',
        f'- Ranking consistent: **{"YES" if same_ranking else "NO"}**',
        f'- Signature consistent: **{"YES" if same_hash else "NO"}**',
        f'- Overall: **{"PASS" if passed else "FAIL"}**',
        '',
        f'- Signature run1: `{h1}`',
        f'- Signature run2: `{h2}`',
    ]

    out = Path('docs/REPRO_CROSS_SUBJECT.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out} (overall={"PASS" if passed else "FAIL"})')

    if not passed:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
