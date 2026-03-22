"""
Aggregate reproducibility checks into one scorecard.
Outputs:
- outputs/reproducibility_scorecard.json
- docs/REPRODUCIBILITY_SCORECARD.md
"""
from pathlib import Path
import json
import re


def read_text(p):
    fp = Path(p)
    return fp.read_text(encoding='utf-8', errors='ignore') if fp.exists() else ''


def parse_pass_from_md(path, token='Overall'):
    txt = read_text(path)
    m = re.search(rf"{token}:\s*\*\*(PASS|FAIL)\*\*", txt, re.IGNORECASE)
    if m:
        return m.group(1).upper() == 'PASS'
    return False


def main():
    checks = {
        'repro_cross_subject_pass': parse_pass_from_md('docs/REPRO_CROSS_SUBJECT.md'),
        'repro_release_signature_pass': parse_pass_from_md('docs/REPRO_RELEASE_SIGNATURE.md'),
        'determinism_audit_pass': parse_pass_from_md('docs/DETERMINISM_AUDIT.md'),
        'explainability_stability_pass': parse_pass_from_md('docs/EXPLAINABILITY_STABILITY.md', token='Gate'),
    }

    # fallback for explainability stability using json flag if markdown pattern differs
    est = Path('outputs/explainability_stability.json')
    if est.exists():
        try:
            checks['explainability_stability_pass'] = bool(json.loads(est.read_text()).get('pass', False))
        except Exception:
            pass

    score = sum(1 for v in checks.values() if v) / len(checks)
    overall = all(checks.values())

    out = {
        'overall_pass': overall,
        'score': score,
        'checks': checks,
    }

    op = Path('outputs/reproducibility_scorecard.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Reproducibility Scorecard',
        '',
        f"- Overall: **{'PASS' if overall else 'FAIL'}**",
        f"- Score: **{score:.2f}**",
        '',
        '| Check | Result |',
        '|---|---:|',
    ]
    for k, v in checks.items():
        lines.append(f"| {k} | {'✅' if v else '❌'} |")

    dp = Path('docs/REPRODUCIBILITY_SCORECARD.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')

    if not overall:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
