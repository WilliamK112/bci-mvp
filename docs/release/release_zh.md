# 发布包（中文）

生成时间：2026-03-22 14:13 UTC

## 一句话介绍
这是一个轻硬件 EEG 脑机接口 MVP，覆盖预处理、模型基准、跨数据集泛化、可解释性和在线演示部署。

## 核心亮点
- 多模型基准（RF/SVM/MLP）
- Cross-dataset RF accuracy: 0.741 (train=dataset_a -> test=dataset_b)
- 实时稳定推理（EMA + 双阈值滞回）
- Explainability: pending real run
- 工程可复现（CI + Docker + Makefile）

## 链接
- 仓库：https://github.com/WilliamK112/bci-mvp
- 技术报告：../TECHNICAL_REPORT.md
- 图表：../../assets/
