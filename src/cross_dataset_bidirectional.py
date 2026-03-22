"""
Bidirectional cross-dataset generalization evaluation.
Runs A->B and B->A with RF/SVM metrics.
Outputs:
- outputs/cross_dataset_bidirectional.json
- docs/CROSS_DATASET_BIDIRECTIONAL.md
"""
from pathlib import Path
import json

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from src.cross_dataset_eval import load_split, evaluate


def run_once(root: Path, train_name: str, test_name: str):
    X_train, y_train = load_split(root, train_name)
    X_test, y_test = load_split(root, test_name)

    models = {
        "RF": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(n_estimators=400, class_weight="balanced", random_state=42, n_jobs=-1)),
        ]),
        "SVM": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", SVC(C=2.0, kernel="rbf", probability=True, class_weight="balanced", random_state=42)),
        ]),
    }

    return {
        "train_dataset": train_name,
        "test_dataset": test_name,
        "train_samples": int(len(y_train)),
        "test_samples": int(len(y_test)),
        "models": {k: evaluate(m, X_train, y_train, X_test, y_test) for k, m in models.items()},
    }


def main():
    root = Path("data")
    a, b = 'dataset_a', 'dataset_b'

    d1 = run_once(root, a, b)
    d2 = run_once(root, b, a)

    rf1 = d1['models']['RF']
    rf2 = d2['models']['RF']

    out = {
        'A_to_B': d1,
        'B_to_A': d2,
        'symmetry_gap_accuracy': abs(float(rf1['accuracy']) - float(rf2['accuracy'])),
        'symmetry_gap_f1': abs(float(rf1['f1']) - float(rf2['f1'])),
        'symmetry_gap_auc': abs(float(rf1['auc']) - float(rf2['auc'])),
    }

    op = Path('outputs/cross_dataset_bidirectional.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Cross-Dataset Bidirectional Evaluation',
        '',
        '| Direction | RF Accuracy | RF F1 | RF AUC |',
        '|---|---:|---:|---:|',
        f"| A -> B | {rf1['accuracy']:.4f} | {rf1['f1']:.4f} | {rf1['auc']:.4f} |",
        f"| B -> A | {rf2['accuracy']:.4f} | {rf2['f1']:.4f} | {rf2['auc']:.4f} |",
        '',
        f"- Symmetry gap (accuracy): **{out['symmetry_gap_accuracy']:.4f}**",
        f"- Symmetry gap (f1): **{out['symmetry_gap_f1']:.4f}**",
        f"- Symmetry gap (auc): **{out['symmetry_gap_auc']:.4f}**",
    ]
    dp = Path('docs/CROSS_DATASET_BIDIRECTIONAL.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')


if __name__ == '__main__':
    main()
