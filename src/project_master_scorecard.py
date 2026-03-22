"""
Master project scorecard aggregating major pillars.
Inputs:
- outputs/streaming_scorecard.json
- outputs/generalization_scorecard.json
- outputs/reproducibility_scorecard.json
Outputs:
- outputs/project_master_scorecard.json
- docs/PROJECT_MASTER_SCORECARD.md
"""
from pathlib import Path
import json


def read_json(path):
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def main():
    streaming = read_json('outputs/streaming_scorecard.json') or {}
    generalization = read_json('outputs/generalization_scorecard.json') or {}
    reproducibility = read_json('outputs/reproducibility_scorecard.json') or {}

    pillars = {
        'streaming': bool(streaming.get('overall_pass', False)),
        'generalization': bool(generalization.get('overall_pass', False)),
        'reproducibility': bool(reproducibility.get('overall_pass', False)),
    }

    scores = {
        'streaming': float(streaming.get('score', 0.0) or 0.0),
        'generalization': float(generalization.get('score', 0.0) or 0.0),
        'reproducibility': float(reproducibility.get('score', 0.0) or 0.0),
    }

    overall_pass = all(pillars.values())
    overall_score = sum(scores.values()) / len(scores)

    out = {
        'overall_pass': overall_pass,
        'overall_score': overall_score,
        'pillars': pillars,
        'pillar_scores': scores,
    }

    op = Path('outputs/project_master_scorecard.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Project Master Scorecard',
        '',
        f"- Overall: **{'PASS' if overall_pass else 'FAIL'}**",
        f"- Overall score: **{overall_score:.2f}**",
        '',
        '| Pillar | Pass | Score |',
        '|---|---:|---:|',
    ]
    for k in ['streaming', 'generalization', 'reproducibility']:
        lines.append(f"| {k} | {'✅' if pillars[k] else '❌'} | {scores[k]:.2f} |")

    dp = Path('docs/PROJECT_MASTER_SCORECARD.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')

    if not overall_pass:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
