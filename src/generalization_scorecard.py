"""
Aggregate cross-dataset and cross-subject generalization into one scorecard.
Outputs:
- outputs/generalization_scorecard.json
- docs/GENERALIZATION_SCORECARD.md
"""
from pathlib import Path
import json


def read_json(path):
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def main():
    cs = read_json('outputs/cross_subject_model_benchmark.json') or {}
    cd = read_json('outputs/cross_dataset_bidirectional.json') or {}

    winner = cs.get('winner')
    ranking = cs.get('ranking') or []
    best_acc = float(ranking[0].get('mean_accuracy', 0.0)) if ranking else 0.0

    a_rf = ((cd.get('A_to_B') or {}).get('models') or {}).get('RF') or {}
    b_rf = ((cd.get('B_to_A') or {}).get('models') or {}).get('RF') or {}
    a_acc = float(a_rf.get('accuracy', 0.0))
    b_acc = float(b_rf.get('accuracy', 0.0))
    gap_acc = float(cd.get('symmetry_gap_accuracy', 1e9)) if cd else 1e9

    gates = {
        'cross_subject_best_acc_ge_0_60': best_acc >= 0.60,
        'cross_dataset_A_to_B_acc_ge_0_50': a_acc >= 0.50,
        'cross_dataset_B_to_A_acc_ge_0_50': b_acc >= 0.50,
        'cross_dataset_symmetry_gap_acc_le_0_25': gap_acc <= 0.25,
    }
    overall = all(gates.values())
    score = sum(1 for v in gates.values() if v) / len(gates)

    out = {
        'overall_pass': overall,
        'score': score,
        'winner_model_loso': winner,
        'metrics': {
            'cross_subject_best_mean_accuracy': best_acc,
            'cross_dataset_A_to_B_rf_accuracy': a_acc,
            'cross_dataset_B_to_A_rf_accuracy': b_acc,
            'cross_dataset_symmetry_gap_accuracy': gap_acc,
        },
        'gates': gates,
    }

    op = Path('outputs/generalization_scorecard.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Generalization Scorecard',
        '',
        f"- Overall: **{'PASS' if overall else 'FAIL'}**",
        f"- Score: **{score:.2f}**",
        f"- LOSO winner: **{winner}**",
        '',
        '| Gate | Result |',
        '|---|---:|',
    ]
    for k, v in gates.items():
        lines.append(f"| {k} | {'✅' if v else '❌'} |")

    lines += [
        '',
        f"- LOSO best mean accuracy: **{best_acc:.4f}**",
        f"- A->B RF accuracy: **{a_acc:.4f}**",
        f"- B->A RF accuracy: **{b_acc:.4f}**",
        f"- Symmetry gap (accuracy): **{gap_acc:.4f}**",
    ]

    dp = Path('docs/GENERALIZATION_SCORECARD.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')

    if not overall:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
