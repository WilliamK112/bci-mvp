from pathlib import Path
from datetime import datetime, timezone

CHECKS = [
    ('docs/TECHNICAL_REPORT.md', 'Technical report'),
    ('docs/MODEL_CARD.md', 'Model card'),
    ('docs/PIPELINE_STATUS.md', 'Pipeline status'),
    ('outputs/artifact_validation_report.txt', 'Artifact validation report'),
    ('assets/all_model_comparison.svg', 'All model chart'),
    ('assets/cross_dataset_matrix.svg', 'Cross-dataset matrix chart'),
    ('assets/calibration_curve.svg', 'Calibration chart'),
    ('assets/robustness_accuracy.svg', 'Robustness chart'),
    ('docs/release/release_en.md', 'Release EN'),
    ('docs/release/release_zh.md', 'Release ZH'),
    ('docs/RISK_REGISTER.md', 'Risk register'),
    ('outputs/bootstrap_ci_results.json', 'Bootstrap CI results'),
]


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# Release Readiness', '', f'Generated: {ts}', '']
    ok = 0
    for p, name in CHECKS:
        exists = Path(p).exists()
        lines.append(f"- [{'x' if exists else ' '}] {name} (`{p}`)")
        ok += int(exists)

    lines += ['', f'**Score:** {ok}/{len(CHECKS)}']
    out = Path('docs/RELEASE_READINESS.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
