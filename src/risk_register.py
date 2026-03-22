"""
Generate and refresh a technical risk register for BCI MVP releases.
"""
from pathlib import Path
from datetime import datetime, timezone

RISKS = [
    ("Dataset shift", "Cross-dataset generalization drops on unseen acquisition setups", "High", "Cross-dataset matrix eval + report confidence intervals"),
    ("Probability miscalibration", "Predicted probabilities may be over/under-confident", "Medium", "Run calibration_eval + monitor Brier score"),
    ("Noise sensitivity", "Performance degradation under perturbations", "Medium", "Run robustness_eval and include robustness chart"),
    ("Feature dependency bias", "Overreliance on specific EEG band/channel", "Medium", "Run ablation + permutation explainability"),
    ("Reproducibility drift", "Outputs diverge across environments", "High", "Use run_full_pipeline + validation + Docker + CI"),
    ("Demo credibility", "Placeholder/demo figures mistaken as final evidence", "Medium", "Label placeholders and prioritize real-data reruns"),
]


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        '# BCI MVP Risk Register',
        '',
        f'Generated: {ts}',
        '',
        '| Risk | Description | Severity | Mitigation |',
        '|---|---|---|---|',
    ]
    for r in RISKS:
        lines.append(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} |')

    out = Path('docs/RISK_REGISTER.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
