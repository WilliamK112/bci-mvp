"""
Cross-subject LOSO benchmark across multiple models.
Outputs:
- outputs/cross_subject_model_benchmark.json
- docs/CROSS_SUBJECT_MODEL_BENCHMARK.md
"""
from pathlib import Path
import json
import re
from collections import defaultdict
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from src.preprocess import load_edf_extract_features


def subject_id_from_name(name: str):
    m = re.search(r"sub(\d+)", name)
    return int(m.group(1)) if m else None


def load_subject_grouped(folder: str, label: int):
    grouped = defaultdict(list)
    for f in sorted(Path(folder).glob("*.edf")):
        sid = subject_id_from_name(f.name)
        if sid is None:
            continue
        X = load_edf_extract_features(str(f))
        y = np.full((len(X),), label, dtype=int)
        grouped[sid].append((X, y))
    out = {}
    for sid, chunks in grouped.items():
        out[sid] = (np.vstack([c[0] for c in chunks]), np.concatenate([c[1] for c in chunks]))
    return out


def model_zoo():
    return {
        'rf': Pipeline([
            ('scaler', StandardScaler()),
            ('clf', RandomForestClassifier(n_estimators=400, class_weight='balanced', random_state=42, n_jobs=-1)),
        ]),
        'svm_rbf': Pipeline([
            ('scaler', StandardScaler()),
            ('clf', SVC(C=2.0, kernel='rbf', gamma='scale', probability=True, class_weight='balanced', random_state=42)),
        ]),
        'logreg': Pipeline([
            ('scaler', StandardScaler()),
            ('clf', LogisticRegression(max_iter=2000, class_weight='balanced', random_state=42)),
        ]),
        'mlp': Pipeline([
            ('scaler', StandardScaler()),
            ('clf', MLPClassifier(hidden_layer_sizes=(64, 32), activation='relu', alpha=1e-4, learning_rate_init=1e-3, max_iter=600, random_state=42)),
        ]),
    }


def main():
    g0 = load_subject_grouped('data/relaxed', 0)
    g1 = load_subject_grouped('data/focused', 1)
    subjects = sorted(set(g0.keys()) & set(g1.keys()))
    if len(subjects) < 2:
        raise SystemExit('Need >=2 shared subjects for LOSO benchmark')

    results = {}
    for mname, clf in model_zoo().items():
        rows = []
        for test_sid in subjects:
            X_test = np.vstack([g0[test_sid][0], g1[test_sid][0]])
            y_test = np.concatenate([g0[test_sid][1], g1[test_sid][1]])

            train_X_parts, train_y_parts = [], []
            for sid in subjects:
                if sid == test_sid:
                    continue
                train_X_parts += [g0[sid][0], g1[sid][0]]
                train_y_parts += [g0[sid][1], g1[sid][1]]

            X_train = np.vstack(train_X_parts)
            y_train = np.concatenate(train_y_parts)

            clf.fit(X_train, y_train)
            pred = clf.predict(X_test)
            proba = clf.predict_proba(X_test)[:, 1]

            rows.append({
                'test_subject': int(test_sid),
                'accuracy': float(accuracy_score(y_test, pred)),
                'f1': float(f1_score(y_test, pred)),
                'auc': float(roc_auc_score(y_test, proba)),
            })

        results[mname] = {
            'mean_accuracy': float(np.mean([r['accuracy'] for r in rows])),
            'mean_f1': float(np.mean([r['f1'] for r in rows])),
            'mean_auc': float(np.mean([r['auc'] for r in rows])),
            'per_subject': rows,
        }

    ranking = sorted(
        [{'model': k, **v} for k, v in results.items()],
        key=lambda x: (x['mean_accuracy'], x['mean_f1'], x['mean_auc']),
        reverse=True,
    )

    out = {
        'subjects': subjects,
        'models': results,
        'ranking': [{'model': r['model'], 'mean_accuracy': r['mean_accuracy'], 'mean_f1': r['mean_f1'], 'mean_auc': r['mean_auc']} for r in ranking],
        'winner': ranking[0]['model'] if ranking else None,
    }

    op = Path('outputs/cross_subject_model_benchmark.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Cross-Subject Model Benchmark (LOSO)',
        '',
        f'- Subjects: `{subjects}`',
        f'- Winner: **{out["winner"]}**',
        '',
        '| Model | Mean Accuracy | Mean F1 | Mean AUC |',
        '|---|---:|---:|---:|',
    ]
    for r in out['ranking']:
        lines.append(f"| {r['model']} | {r['mean_accuracy']:.4f} | {r['mean_f1']:.4f} | {r['mean_auc']:.4f} |")

    dp = Path('docs/CROSS_SUBJECT_MODEL_BENCHMARK.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(json.dumps(out['ranking'], indent=2))
    print(f'Generated {op} and {dp}')


if __name__ == '__main__':
    main()
