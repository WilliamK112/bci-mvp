# Public Results Checklist

Before posting benchmarks publicly:
- [ ] Include dataset names and split strategy
- [ ] Report at least Accuracy, F1, AUC
- [ ] Include cross-dataset result (train A -> test B)
- [ ] Add reproducibility command used
- [ ] Add model limitations and failure modes

## Commands
```bash
python src/benchmark.py
python src/cross_dataset_eval.py --train dataset_a --test dataset_b
python src/plot_results.py
```

## Artifacts to publish
- `outputs/benchmark_results.csv`
- `outputs/cross_dataset_results.json`
- `outputs/benchmark_scores.png`
- `outputs/cross_dataset_scores.png`
