"""
Build a compact overview across Streaming/Generalization/Reproducibility/Master scorecards.
Outputs:
- outputs/scorecards_overview.json
- docs/SCORECARDS_OVERVIEW.md
"""
from pathlib import Path
import json

SOURCES = {
    'streaming': 'outputs/streaming_scorecard.json',
    'generalization': 'outputs/generalization_scorecard.json',
    'reproducibility': 'outputs/reproducibility_scorecard.json',
    'master': 'outputs/project_master_scorecard.json',
}


def read_json(path):
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def row_for(name, obj):
    if not obj:
        return {'name': name, 'pass': False, 'score': 0.0, 'source_exists': False}
    score = obj.get('score', obj.get('overall_score', 0.0))
    passed = obj.get('overall_pass', False)
    return {'name': name, 'pass': bool(passed), 'score': float(score), 'source_exists': True}


def main():
    rows = []
    for name, src in SOURCES.items():
        rows.append(row_for(name, read_json(src)))

    all_exist = all(r['source_exists'] for r in rows)
    overall_pass = all(r['pass'] for r in rows)
    avg_score = sum(r['score'] for r in rows) / len(rows)

    out = {
        'overall_pass': overall_pass,
        'all_sources_present': all_exist,
        'average_score': avg_score,
        'rows': rows,
    }

    op = Path('outputs/scorecards_overview.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Scorecards Overview',
        '',
        f"- Overall pass: **{'PASS' if overall_pass else 'FAIL'}**",
        f"- All sources present: **{'YES' if all_exist else 'NO'}**",
        f"- Average score: **{avg_score:.2f}**",
        '',
        '| Scorecard | Pass | Score | Source Exists |',
        '|---|---:|---:|---:|',
    ]
    for r in rows:
        lines.append(f"| {r['name']} | {'✅' if r['pass'] else '❌'} | {r['score']:.2f} | {'✅' if r['source_exists'] else '❌'} |")

    dp = Path('docs/SCORECARDS_OVERVIEW.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')


if __name__ == '__main__':
    main()
