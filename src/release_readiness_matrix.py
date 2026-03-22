"""
Build a concise release-readiness matrix from core scorecards.
Outputs:
- outputs/release_readiness_matrix.json
- docs/RELEASE_READINESS_MATRIX.md
"""
from pathlib import Path
import json

SOURCES = {
    'streaming': 'outputs/streaming_scorecard.json',
    'generalization': 'outputs/generalization_scorecard.json',
    'reproducibility': 'outputs/reproducibility_scorecard.json',
    'master': 'outputs/project_master_scorecard.json',
    'overview': 'outputs/scorecards_overview.json',
}


def load(path):
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def main():
    rows = []
    for name, path in SOURCES.items():
        obj = load(path)
        if obj is None:
            rows.append({'name': name, 'present': False, 'pass': False, 'score': 0.0})
            continue
        rows.append({
            'name': name,
            'present': True,
            'pass': bool(obj.get('overall_pass', False)),
            'score': float(obj.get('score', obj.get('overall_score', obj.get('average_score', 0.0))) or 0.0),
        })

    all_present = all(r['present'] for r in rows)
    all_pass = all(r['pass'] for r in rows)
    avg_score = sum(r['score'] for r in rows) / len(rows)

    out = {
        'all_present': all_present,
        'all_pass': all_pass,
        'avg_score': avg_score,
        'rows': rows,
    }
    op = Path('outputs/release_readiness_matrix.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Release Readiness Matrix',
        '',
        f"- All artifacts present: **{'YES' if all_present else 'NO'}**",
        f"- All gates pass: **{'YES' if all_pass else 'NO'}**",
        f"- Average score: **{avg_score:.2f}**",
        '',
        '| Pillar | Present | Pass | Score |',
        '|---|---:|---:|---:|',
    ]
    for r in rows:
        lines.append(f"| {r['name']} | {'✅' if r['present'] else '❌'} | {'✅' if r['pass'] else '❌'} | {r['score']:.2f} |")

    dp = Path('docs/RELEASE_READINESS_MATRIX.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')


if __name__ == '__main__':
    main()
