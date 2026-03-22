"""
Run one-command repro flow and emit compact proof artifact.
Outputs:
- outputs/repro_run_proof.json
- docs/REPRO_RUN_PROOF.md
"""
from pathlib import Path
import json
import hashlib
import subprocess

KEY_FILES = [
    'docs/FINAL_RELEASE_CANDIDATE.md',
    'docs/PROJECT_MASTER_SCORECARD.md',
    'docs/RELEASE_DECISION_GATE.md',
    'outputs/project_master_scorecard.json',
    'outputs/release_decision_gate.json',
]


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    subprocess.run(['python', 'src/repro_one_command.py'], check=True)

    rows = []
    for f in KEY_FILES:
        p = Path(f)
        rows.append({
            'file': f,
            'exists': p.exists(),
            'sha256': sha256(p) if p.exists() else None,
        })

    ok = all(r['exists'] for r in rows)
    out = {
        'repro_command': 'python src/repro_one_command.py',
        'status': 'PASS' if ok else 'FAIL',
        'artifacts': rows,
    }

    op = Path('outputs/repro_run_proof.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Repro Run Proof',
        '',
        f"- Command: `python src/repro_one_command.py`",
        f"- Status: **{out['status']}**",
        '',
        '| Artifact | Exists | SHA256 |',
        '|---|---:|---|',
    ]
    for r in rows:
        lines.append(f"| {r['file']} | {'✅' if r['exists'] else '❌'} | `{r['sha256']}` |")

    dp = Path('docs/REPRO_RUN_PROOF.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')

    if not ok:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
