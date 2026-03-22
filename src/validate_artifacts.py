"""
Validate key output artifacts for reproducibility/reporting readiness.
Checks presence + minimal schema consistency.
"""
from pathlib import Path
import json
import csv

REQUIRED = [
    'outputs/benchmark_results.csv',
    'outputs/all_model_results.csv',
    'assets/all_model_comparison.svg',
    'assets/cross_dataset_matrix.svg',
    'docs/TECHNICAL_REPORT.md',
    'docs/MODEL_CARD.md',
]


def check_csv(path: Path, required_cols):
    if not path.exists():
        return False, f"missing: {path}"
    with path.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
    miss = [c for c in required_cols if c not in cols]
    if miss:
        return False, f"{path} missing columns: {miss}"
    return True, f"ok: {path}"


def check_json(path: Path, keys):
    if not path.exists():
        return False, f"missing: {path}"
    try:
        obj = json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        return False, f"{path} invalid json: {e}"
    miss = [k for k in keys if k not in obj]
    if miss:
        return False, f"{path} missing keys: {miss}"
    return True, f"ok: {path}"


def main():
    logs = []
    ok_all = True

    for p in REQUIRED:
        path = Path(p)
        if path.exists():
            logs.append(f"ok: {p}")
        else:
            logs.append(f"missing: {p}")
            ok_all = False

    ok, msg = check_csv(Path('outputs/benchmark_results.csv'), ['model', 'accuracy', 'f1', 'auc'])
    logs.append(msg); ok_all &= ok

    ok, msg = check_csv(Path('outputs/all_model_results.csv'), ['model', 'accuracy', 'f1', 'auc'])
    logs.append(msg); ok_all &= ok

    ok, msg = check_json(Path('outputs/cross_dataset_results.json'), ['train_dataset', 'test_dataset', 'models'])
    logs.append(msg)

    out = Path('outputs')
    out.mkdir(exist_ok=True)
    report = out / 'artifact_validation_report.txt'
    report.write_text('\n'.join(logs) + '\n', encoding='utf-8')

    print('\n'.join(logs))
    print(f"Saved {report}")

    if not ok_all:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
