"""
Generate a single 'command center' markdown with all high-value commands.
"""
from pathlib import Path
from datetime import datetime, timezone

SECTIONS = {
    "Data & Training": [
        "python src/check_data.py",
        "python src/train.py",
        "python src/deep_baseline.py",
    ],
    "Evaluation": [
        "python src/benchmark.py",
        "python src/cross_dataset_eval.py --train dataset_a --test dataset_b",
        "python src/cross_dataset_matrix.py",
        "python src/calibration_eval.py",
        "python src/robustness_eval.py",
        "python src/ablation_eval.py",
    ],
    "Visualization": [
        "python src/plot_results.py",
        "python src/plot_all_models.py",
        "python src/plot_cross_matrix.py",
        "python src/plot_calibration.py",
        "python src/plot_robustness.py",
        "python src/plot_ablation.py",
    ],
    "Explainability": [
        "python src/explainability.py",
        "python src/permutation_explain.py",
    ],
    "Docs & Release": [
        "python src/build_report.py",
        "python src/release_readiness.py",
        "python src/hf_space_readiness.py",
        "python src/leaderboard.py",
        "python src/generate_figure_gallery.py",
        "python src/changelog_from_git.py",
        "python src/generate_release_pack.py",
        "python src/generate_model_card.py",
        "python src/update_docs_bundle.py",
        "python src/generate_status_badges.py",
    ],
    "One-command": [
        "python src/run_full_pipeline.py",
        "make full",
    ],
}


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# BCI MVP Command Center', '', f'Generated: {ts}', '']
    for sec, cmds in SECTIONS.items():
        lines += [f'## {sec}', '']
        lines += [f'- `{c}`' for c in cmds]
        lines += ['']

    out = Path('docs/COMMAND_CENTER.md')
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
