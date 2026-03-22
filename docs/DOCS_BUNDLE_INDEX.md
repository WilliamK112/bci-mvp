# Documentation Bundle Index

Generated: 2026-03-22 15:28 UTC

## Core
- ✅ [Technical report](TECHNICAL_REPORT.md) — `docs/TECHNICAL_REPORT.md`
- ✅ [Release readiness dashboard](RELEASE_READINESS.md) — `docs/RELEASE_READINESS.md`
- ✅ [HF Space readiness](HF_SPACE_READINESS.md) — `docs/HF_SPACE_READINESS.md`
- ✅ [Model card](MODEL_CARD.md) — `docs/MODEL_CARD.md`
- ✅ [Model leaderboard](MODEL_LEADERBOARD.md) — `docs/MODEL_LEADERBOARD.md`
- ✅ [Figure gallery](FIGURE_GALLERY.md) — `docs/FIGURE_GALLERY.md`
- ✅ [Auto changelog](CHANGELOG_AUTO.md) — `docs/CHANGELOG_AUTO.md`
- ✅ [Release pack EN](docs/release/release_en.md) — `docs/release/release_en.md`
- ✅ [Release pack ZH](docs/release/release_zh.md) — `docs/release/release_zh.md`
- ✅ [Reddit post draft](docs/release/reddit_post.md) — `docs/release/reddit_post.md`
- ✅ [Bilibili post draft](docs/release/bilibili_post.md) — `docs/release/bilibili_post.md`

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
