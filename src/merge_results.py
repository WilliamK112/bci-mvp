from pathlib import Path
import csv


def read_csv(path):
    if not path.exists():
        return []
    with path.open('r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    out = Path('outputs')
    base = read_csv(out / 'benchmark_results.csv')
    deep = read_csv(out / 'deep_baseline_results.csv')

    rows = []
    for r in base + deep:
        rows.append({
            'model': r.get('model', ''),
            'accuracy': r.get('accuracy', ''),
            'f1': r.get('f1', ''),
            'auc': r.get('auc', ''),
        })

    if rows:
        write_csv(out / 'all_model_results.csv', rows, ['model', 'accuracy', 'f1', 'auc'])
        print(f"Saved {out / 'all_model_results.csv'} with {len(rows)} rows")
    else:
        print('No rows to merge')


if __name__ == '__main__':
    main()
