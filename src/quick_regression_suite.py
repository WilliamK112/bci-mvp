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
]


def main():
    for t in TESTS:
        print(f'Running {t}...')
        subprocess.run(['python', '-m', 'unittest', t], check=True)
    print('Quick regression suite PASS')


if __name__ == '__main__':
    main()
