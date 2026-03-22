"""
Generate concise English results brief from latest artifacts.
"""
from pathlib import Path
import json, csv
from datetime import datetime, timezone


def read_csv(path):
    p=Path(path)
    if not p.exists(): return []
    with p.open('r',encoding='utf-8') as f:
        return list(csv.DictReader(f))


def read_json(path):
    p=Path(path)
    if not p.exists(): return None
    return json.loads(p.read_text(encoding='utf-8'))


def main():
    ts=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    bench=read_csv('outputs/benchmark_results.csv')
    calib=read_json('outputs/calibration_results.json')
    boot=read_json('outputs/bootstrap_ci_results.json')

    top='n/a'
    if bench:
        best=sorted(bench,key=lambda r: float(r.get('accuracy',0)), reverse=True)[0]
        top=f"{best.get('model')} (Acc={best.get('accuracy')}, AUC={best.get('auc')})"

    lines=[
        '# Results Brief (EN)','',f'Generated: {ts}','',
        '## One-line takeaway',
        f'- Current best model: **{top}**.',
        '',
        '## Key metrics',
        f"- Calibration Brier score: **{calib.get('brier_score')}**" if calib else '- Calibration Brier score: n/a',
    ]
    if boot:
        lines += [
            f"- Accuracy 95% CI: {boot.get('accuracy_ci95')}",
            f"- F1 95% CI: {boot.get('f1_ci95')}",
            f"- AUC 95% CI: {boot.get('auc_ci95')}",
        ]

    lines += ['', '## References', '- `docs/RESULTS.md`', '- `docs/TECHNICAL_REPORT.md`', '- `docs/ONE_PAGER.md`']

    out=Path('docs/RESULTS_BRIEF_EN.md')
    out.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(f'Generated {out}')

if __name__=='__main__':
    main()
