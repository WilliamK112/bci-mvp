"""Run critical regression tests quickly."""
import subprocess

TESTS = [
    'tests/test_infer_fallback_unittest.py',
    'tests/test_streaming_drift_and_bidirectional_unittest.py',
    'tests/test_explainability_stability_unittest.py',
    'tests/test_streaming_scorecard_unittest.py',
    'tests/test_streaming_scorecard_visual_unittest.py',
    'tests/test_generalization_scorecard_unittest.py',
    'tests/test_generalization_scorecard_visual_unittest.py',
    'tests/test_reproducibility_scorecard_unittest.py',
    'tests/test_reproducibility_scorecard_visual_unittest.py',
    'tests/test_project_master_scorecard_unittest.py',
    'tests/test_project_master_scorecard_visual_unittest.py',
    'tests/test_scorecards_overview_unittest.py',
    'tests/test_scorecards_overview_visual_unittest.py',
    'tests/test_real_data_evidence_unittest.py',
    'tests/test_repro_one_command_entrypoint_unittest.py',
    'tests/test_release_readiness_matrix_unittest.py',
    'tests/test_release_readiness_matrix_visual_unittest.py',
    'tests/test_release_matrix_badge_unittest.py',
    'tests/test_release_decision_badge_unittest.py',
    'tests/test_release_decision_gate_unittest.py',
    'tests/test_repro_run_proof_unittest.py',
    'tests/test_release_decision_gate_visual_unittest.py',
    'tests/test_repro_run_proof_visual_unittest.py',
]


def main():
    for t in TESTS:
        print(f'Running {t}...')
        subprocess.run(['python', '-m', 'unittest', t], check=True)
    print('Quick regression suite PASS')


if __name__ == '__main__':
    main()
