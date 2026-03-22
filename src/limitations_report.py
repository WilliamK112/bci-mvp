"""
Generate limitations report from current artifacts and known assumptions.
"""
from pathlib import Path
import json
from datetime import datetime, timezone


def read_json(path):
    p=Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding='utf-8'))


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    cross = read_json('outputs/cross_dataset_results.json')
    robust = read_json('outputs/robustness_results.json')

    lines = ['# Limitations Report', '', f'Generated: {ts}', '', '## Known Limitations']
    lines += [
        '- Labels in current public-data bootstrap are pragmatic task-mapping, not clinical ground truth.',
        '- Binary relaxed/focused framing does not capture full cognitive-state spectrum.',
        '- Current feature representation is handcrafted bandpower; end-to-end deep temporal features are not fully explored.',
        '- Cross-dataset evidence is still constrained by small public bootstrap subset size.',
    ]

    if robust:
        lines += ['', '## Robustness Caveat']
        lines.append('- Noise perturbation can significantly reduce performance; refer to `outputs/robustness_results.json`.')

    if cross:
        lines += ['', '## Generalization Caveat']
        lines.append('- Cross-dataset transfer quality depends strongly on acquisition/protocol alignment.')

    lines += ['', '## Mitigation Plan',
              '- Expand real labeled datasets and subject diversity.',
              '- Add stricter cross-session/cross-subject protocols.',
              '- Introduce stronger deep baselines (e.g., EEGNet).',
              '- Add domain adaptation / calibration by device/session.',
    ]

    out = Path('docs/LIMITATIONS.md')
    out.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__=='__main__':
    main()
