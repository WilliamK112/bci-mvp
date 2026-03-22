"""
Release decision gate based on top-level readiness artifacts.
Outputs:
- outputs/release_decision_gate.json
- docs/RELEASE_DECISION_GATE.md
"""
from pathlib import Path
import json


def read_json(path):
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def main():
    master = read_json('outputs/project_master_scorecard.json') or {}
    matrix = read_json('outputs/release_readiness_matrix.json') or {}
    overview = read_json('outputs/scorecards_overview.json') or {}

    checks = {
        'master_overall_pass': bool(master.get('overall_pass', False)),
        'matrix_all_pass': bool(matrix.get('all_pass', False)),
        'matrix_all_present': bool(matrix.get('all_present', False)),
        'overview_overall_pass': bool(overview.get('overall_pass', False)),
        'overview_sources_present': bool(overview.get('all_sources_present', False)),
    }

    avg_score = float(matrix.get('avg_score', 0.0) or 0.0)
    checks['matrix_avg_score_ge_0_90'] = avg_score >= 0.90

    decision = 'GO' if all(checks.values()) else 'HOLD'
    suggested_tag = 'v1.0.0' if decision == 'GO' else 'v1.0.0-rc'

    out = {
        'decision': decision,
        'suggested_tag': suggested_tag,
        'checks': checks,
        'matrix_avg_score': avg_score,
    }

    op = Path('outputs/release_decision_gate.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Release Decision Gate',
        '',
        f"- Decision: **{decision}**",
        f"- Suggested tag: **{suggested_tag}**",
        f"- Matrix avg score: **{avg_score:.2f}**",
        '',
        '| Check | Result |',
        '|---|---:|',
    ]
    for k, v in checks.items():
        lines.append(f"| {k} | {'✅' if v else '❌'} |")

    dp = Path('docs/RELEASE_DECISION_GATE.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')


if __name__ == '__main__':
    main()
