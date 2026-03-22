"""
Seed sensitivity analysis for LOSO benchmarks.
Outputs:
- outputs/cross_subject_seed_sensitivity.json
- docs/CROSS_SUBJECT_SEED_SENSITIVITY.md
"""
from pathlib import Path
import json
import re
from collections import defaultdict
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from src.preprocess import load_edf_extract_features


def sid(name):
    m = re.search(r"sub(\d+)", name)
    return int(m.group(1)) if m else None


def grouped(folder, label):
    g = defaultdict(list)
    for f in sorted(Path(folder).glob('*.edf')):
        s = sid(f.name)
        if s is None:
            continue
        X = load_edf_extract_features(str(f))
        y = np.full((len(X),), label, dtype=int)
        g[s].append((X, y))
    out = {}
    for s, chunks in g.items():
        out[s] = (np.vstack([c[0] for c in chunks]), np.concatenate([c[1] for c in chunks]))
    return out


def eval_model(seed, model_name, g0, g1, subjects):
    if model_name == 'rf':
        clf = Pipeline([('scaler', StandardScaler()), ('clf', RandomForestClassifier(n_estimators=400, class_weight='balanced', random_state=seed, n_jobs=-1))])
    else:
        clf = Pipeline([('scaler', StandardScaler()), ('clf', MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=600, random_state=seed))])

    vals = []
    for test_sid in subjects:
        X_test = np.vstack([g0[test_sid][0], g1[test_sid][0]])
        y_test = np.concatenate([g0[test_sid][1], g1[test_sid][1]])
        tx, ty = [], []
        for s in subjects:
            if s == test_sid:
                continue
            tx += [g0[s][0], g1[s][0]]
            ty += [g0[s][1], g1[s][1]]
        X_train = np.vstack(tx); y_train = np.concatenate(ty)
        clf.fit(X_train, y_train)
        pred = clf.predict(X_test)
        vals.append(float(accuracy_score(y_test, pred)))
    return float(np.mean(vals))


def main():
    g0 = grouped('data/relaxed', 0)
    g1 = grouped('data/focused', 1)
    subjects = sorted(set(g0.keys()) & set(g1.keys()))
    seeds = [7, 21, 42, 84, 126]
    out = {'subjects': subjects, 'seeds': seeds, 'models': {}}

    for m in ['rf', 'mlp']:
        scores = [eval_model(s, m, g0, g1, subjects) for s in seeds]
        out['models'][m] = {
            'seed_scores': scores,
            'mean_accuracy': float(np.mean(scores)),
            'std_accuracy': float(np.std(scores)),
            'min_accuracy': float(np.min(scores)),
            'max_accuracy': float(np.max(scores)),
        }

    op = Path('outputs/cross_subject_seed_sensitivity.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = ['# Cross-Subject Seed Sensitivity', '', '| Model | Mean Acc | Std | Min | Max |', '|---|---:|---:|---:|---:|']
    for m, v in out['models'].items():
        lines.append(f"| {m} | {v['mean_accuracy']:.4f} | {v['std_accuracy']:.4f} | {v['min_accuracy']:.4f} | {v['max_accuracy']:.4f} |")
    Path('docs/CROSS_SUBJECT_SEED_SENSITIVITY.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and docs/CROSS_SUBJECT_SEED_SENSITIVITY.md')


if __name__ == '__main__':
    main()
