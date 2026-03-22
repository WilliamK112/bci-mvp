"""
Reproducibility check: run release candidate flow twice and compare key artifact signatures.
Outputs docs/REPRO_RELEASE_SIGNATURE.md
"""
from pathlib import Path
import hashlib
import subprocess

KEY_FILES = [
    'docs/RELEASE_SUMMARY.json',
    'docs/FINAL_RELEASE_CANDIDATE.md',
    'docs/TECHNICAL_REPORT.md',
    'docs/RESULTS.md',
    'docs/ONE_PAGER.md',
    'outputs/cross_subject_model_benchmark.json',
    'outputs/cross_subject_ci.json',
    'outputs/streaming_latency.json',
    'outputs/streaming_stability.json',
]


def sha256_file(p: Path):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def snapshot():
    sig = {}
    for f in KEY_FILES:
        p = Path(f)
        if not p.exists():
            sig[f] = None
            continue
        if f.endswith('docs/RELEASE_SUMMARY.json'):
            try:
                import json
                obj = json.loads(p.read_text(encoding='utf-8'))
                obj.pop('generated_at_utc', None)
                canonical = json.dumps(obj, sort_keys=True)
                sig[f] = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
                continue
            except Exception:
                pass
        sig[f] = sha256_file(p)
    return sig


def main():
    subprocess.run(['python', 'src/final_release_candidate.py'], check=True)
    s1 = snapshot()
    subprocess.run(['python', 'src/final_release_candidate.py'], check=True)
    s2 = snapshot()

    rows = []
    stable = True
    for f in KEY_FILES:
        a, b = s1.get(f), s2.get(f)
        ok = (a == b) and (a is not None)
        stable = stable and ok
        rows.append((f, a, b, ok))

    lines = [
        '# Reproducibility Check: Release Signature',
        '',
        f'- Overall: **{"PASS" if stable else "FAIL"}**',
        '- Method: run `src/final_release_candidate.py` twice and compare SHA256 per key artifact.',
        '',
        '| Artifact | Run1 SHA256 | Run2 SHA256 | Stable |',
        '|---|---|---|---:|',
    ]
    for f, a, b, ok in rows:
        lines.append(f"| {f} | `{a}` | `{b}` | {'✅' if ok else '❌'} |")

    out = Path('docs/REPRO_RELEASE_SIGNATURE.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out} (overall={"PASS" if stable else "FAIL"})')

    if not stable:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
