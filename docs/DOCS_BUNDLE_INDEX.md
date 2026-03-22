# Documentation Bundle Index

Generated: 2026-03-22 18:10 UTC

## Core
- ✅ [Technical report](TECHNICAL_REPORT.md) — `docs/TECHNICAL_REPORT.md`
- ✅ [Limitations report](LIMITATIONS.md) — `docs/LIMITATIONS.md`
- ✅ [Release readiness dashboard](RELEASE_READINESS.md) — `docs/RELEASE_READINESS.md`
- ✅ [HF Space readiness](HF_SPACE_READINESS.md) — `docs/HF_SPACE_READINESS.md`
- ✅ [Space user guide](SPACE_USER_GUIDE.md) — `docs/SPACE_USER_GUIDE.md`
- ✅ [Model card](MODEL_CARD.md) — `docs/MODEL_CARD.md`
- ✅ [Mathematical model](MATH_NOTATION.md) — `docs/MATH_NOTATION.md`
- ✅ [Methods (paper-style)](METHODS.md) — `docs/METHODS.md`
- ✅ [Results summary](RESULTS.md) — `docs/RESULTS.md`
- ✅ [Metrics registry](METRICS_REGISTRY.md) — `docs/METRICS_REGISTRY.md`
- ✅ [Data provenance](DATA_PROVENANCE.md) — `docs/DATA_PROVENANCE.md`
- ✅ [Results brief (EN)](RESULTS_BRIEF_EN.md) — `docs/RESULTS_BRIEF_EN.md`
- ✅ [Results brief (ZH)](RESULTS_BRIEF_ZH.md) — `docs/RESULTS_BRIEF_ZH.md`
- ✅ [Model leaderboard](MODEL_LEADERBOARD.md) — `docs/MODEL_LEADERBOARD.md`
- ✅ [Figure gallery](FIGURE_GALLERY.md) — `docs/FIGURE_GALLERY.md`
- ✅ [Auto changelog](CHANGELOG_AUTO.md) — `docs/CHANGELOG_AUTO.md`
- ✅ [Release pack EN](docs/release/release_en.md) — `docs/release/release_en.md`
- ✅ [Release pack ZH](docs/release/release_zh.md) — `docs/release/release_zh.md`
- ✅ [Reddit post draft](docs/release/reddit_post.md) — `docs/release/reddit_post.md`
- ✅ [Bilibili post draft](docs/release/bilibili_post.md) — `docs/release/bilibili_post.md`

- ✅ [Citation metadata](../CITATION.cff) — `CITATION.cff`

## One-command refresh sequence
```bash
python src/build_report.py
python src/release_readiness.py
python src/hf_space_readiness.py
python src/leaderboard.py
python src/generate_figure_gallery.py
python src/changelog_from_git.py
python src/generate_release_pack.py
python src/generate_model_card.py
```
