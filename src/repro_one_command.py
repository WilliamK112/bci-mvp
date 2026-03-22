"""One-command reproducibility runner for core release artifacts."""
import subprocess

COMMANDS = [
    ['python', 'src/run_full_pipeline.py'],
    ['python', 'src/quick_regression_suite.py'],
    ['python', 'src/final_release_candidate.py'],
]


def main():
    for cmd in COMMANDS:
        print('$', ' '.join(cmd))
        subprocess.run(cmd, check=True)
    print('REPRO ONE-COMMAND: PASS')


if __name__ == '__main__':
    main()
