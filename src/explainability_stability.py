"""
Explainability stability check across repeated permutation runs.
Outputs:
- outputs/explainability_stability.json
- docs/EXPLAINABILITY_STABILITY.md
"""
from pathlib import Path
import json
import subprocess
import pandas as pd


def run_once(tag: str):
    subprocess.run(['python', 'src/permutation_explain.py'], check=True)
    src = Path('outputs/permutation_importance_detailed.csv')
    df = pd.read_csv(src).sort_values('importance_mean', ascending=False)
    top5 = df.head(5)['feature_idx'].astype(int).tolist()
    band = None
    bpath = Path('outputs/permutation_importance_by_band.csv')
    if bpath.exists():
        bdf = pd.read_csv(bpath).sort_values('importance_mean', ascending=False)
        if len(bdf):
            band = str(bdf.iloc[0]['band'])
    return {'tag': tag, 'top5': top5, 'top_band': band}


def jaccard(a, b):
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / max(1, len(sa | sb))


def main():
    r1 = run_once('run1')
    r2 = run_once('run2')

    jac = jaccard(r1['top5'], r2['top5'])
    band_same = (r1['top_band'] == r2['top_band']) and (r1['top_band'] is not None)

    out = {
        'run1': r1,
        'run2': r2,
        'top5_jaccard': jac,
        'top_band_consistent': band_same,
        'pass': bool(jac >= 0.5 and band_same),
    }

    op = Path('outputs/explainability_stability.json')
    op.write_text(json.dumps(out, indent=2), encoding='utf-8')

    lines = [
        '# Explainability Stability',
        '',
        f"- Top-5 feature Jaccard: **{jac:.3f}**",
        f"- Top band consistency: **{'YES' if band_same else 'NO'}**",
        f"- Gate (`Jaccard >= 0.5` and top band consistent): **{'PASS' if out['pass'] else 'FAIL'}**",
        '',
        f"- Run1 top5: `{r1['top5']}`",
        f"- Run2 top5: `{r2['top5']}`",
        f"- Run1 top band: `{r1['top_band']}`",
        f"- Run2 top band: `{r2['top_band']}`",
    ]

    dp = Path('docs/EXPLAINABILITY_STABILITY.md')
    dp.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {op} and {dp}')

    if not out['pass']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
