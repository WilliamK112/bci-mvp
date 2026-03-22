# BCI MVP（中文说明）

![BCI MVP Banner](assets/readme_banner.svg)

这是一个轻量级脑机接口（BCI）MVP 项目，用 EEG 数据实现放松/专注状态识别，并提供可复现评估、可解释分析与在线演示。

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Space](https://img.shields.io/badge/HuggingFace-Space-yellow)

一个轻量级 EEG 脑机接口 MVP，核心能力：
- EEG 预处理（EDF）
- relaxed / focused 二分类
- 实时稳定推理（EMA + Hysteresis）
- 可复现评估与发布流程

## 在线演示
- Hugging Face Space: https://huggingface.co/spaces/williamKang112/bci-mvp-demo

## 快速开始
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/check_data.py
python src/train.py

uvicorn api.main:app --reload --port 8000
streamlit run app/dashboard.py
```

## 常用命令
```bash
python src/run_full_pipeline.py
python src/final_release_candidate.py
python src/hf_space_status.py --space williamKang112/bci-mvp-demo
python src/space_smoke_test.py
```

## 关键文档
- 技术报告：`docs/TECHNICAL_REPORT.md`
- 质量评分：`docs/QUALITY_SCORECARD.md`
- 发布就绪：`docs/RELEASE_READINESS.md`
- Space 就绪：`docs/HF_SPACE_READINESS.md`
- 最终发布摘要：`docs/FINAL_RELEASE_CANDIDATE.md`
- 文档索引：`docs/DOCS_BUNDLE_INDEX.md`

## 许可证
MIT

## 结果简报
- `docs/RESULTS_BRIEF_ZH.md`

## 状态快照
- `docs/STATUS_SNAPSHOT_ZH.md`

## v1 发布说明
- `docs/V1_RELEASE_NOTES.md`
