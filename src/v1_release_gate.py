"""
Final v1.0.0 release gate from top-level decision artifacts.
Outputs:
- outputs/v1_release_gate.json
- docs/V1_RELEASE_GATE.md
"""
from pathlib import Path
import json


def read_json(path):
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def main():
    decision = read_json('outputs/release_decision_gate.json') or {}
    matrix = read_json('outputs/release_readiness_matrix.json') or {}
    master = read_json('outputs/project_master_scorecard.json') or {}

    checks = {
        'decision_go': str(decision.get('decision', 'HOLD')).upper() == 'GO',
        'suggested_tag_v1': str(decision.get('suggested_tag', '')).startswith('v1.0.0'),
        'matrix_all_pass': bool(matrix.get('all_pass', False)),
        'matrix_all_present': bool(matrix.get('all_present', False)),
        'master_overall_pass': bool(master.get('overall_pass', False)),
        'master_score_ge_0_95': float(master.get('overall_score', 0.0) or 0.0) >= 0.95,
    }

    go = all(checks.values())
    out = {
        'release': 'v1.0.0',
        'go': go,
        'checks': checks,
        'next_action': 'Create v1.0.0 tag/release' if go else 'Hold and fix failed checks',
    }

    op = Path('outputs/v1_release_gate.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# V1 Release Gate',
        '',
        f"- Target release: **v1.0.0**",
        f"- Gate result: **{'GO' if go else 'HOLD'}**",
        f"- Next action: **{out['next_action']}**",
        '',
        '| Check | Result |',
        '|---|---:|',
    ]
    for k, v in checks.items():
        lines.append(f"| {k} | {'✅' if v else '❌'} |")

    if go:
        lines += [
            '',
            '## Suggested Commands',
            '```bash',
            'git tag -a v1.0.0 -m "v1.0.0"',
            'git push origin v1.0.0',
            '```',
        ]

    dp = Path('docs/V1_RELEASE_GATE.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')


if __name__ == '__main__':
    main()
