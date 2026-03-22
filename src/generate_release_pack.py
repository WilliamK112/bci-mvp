"""
Generate public release pack (EN/ZH) from latest artifacts.
Outputs markdown files under docs/release/.
"""
from pathlib import Path
import json
from datetime import datetime, timezone


def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    docs = Path('docs/release')
    docs.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    cross = load_json(Path('outputs/cross_dataset_results.json'))
    perm = load_json(Path('outputs/permutation_importance_summary.json'))

    cross_line = '- Cross-dataset: pending real run'
    if cross:
        m = cross.get('models', {}).get('RF', {})
        cross_line = f"- Cross-dataset RF accuracy: {m.get('accuracy')} (train={cross.get('train_dataset')} -> test={cross.get('test_dataset')})"

    explain_line = '- Explainability: pending real run'
    if perm:
        explain_line = f"- Permutation explainability top band: {perm.get('top_band')}"

    en = f"""# Release Pack (EN)

Generated: {ts}

## Short pitch
A lightweight EEG BCI MVP that supports preprocessing, benchmark evaluation, cross-dataset generalization, explainability, and online demo deployment.

## Key points
- Multi-model benchmarks (RF/SVM/MLP)
{cross_line}
- Streaming stability (EMA + hysteresis)
{explain_line}
- Reproducible engineering (CI + Docker + Makefile)

## Links
- Repo: https://github.com/WilliamK112/bci-mvp
- Technical report: ../TECHNICAL_REPORT.md
- Figures: ../../assets/
"""

    zh = f"""# 发布包（中文）

生成时间：{ts}

## 一句话介绍
这是一个轻硬件 EEG 脑机接口 MVP，覆盖预处理、模型基准、跨数据集泛化、可解释性和在线演示部署。

## 核心亮点
- 多模型基准（RF/SVM/MLP）
{cross_line}
- 实时稳定推理（EMA + 双阈值滞回）
{explain_line}
- 工程可复现（CI + Docker + Makefile）

## 链接
- 仓库：https://github.com/WilliamK112/bci-mvp
- 技术报告：../TECHNICAL_REPORT.md
- 图表：../../assets/
"""

    reddit = """# Reddit Post Draft

Built a low-hardware EEG BCI MVP with cross-dataset evaluation, explainability, and streaming-stable inference.

Repo: https://github.com/WilliamK112/bci-mvp
Would love feedback on generalization strategy and benchmark rigor.
"""

    bilibili = """# B站发布文案草稿

我做了一个轻硬件脑机接口（EEG）MVP：
- 预处理 + 特征提取
- 多模型对比（RF/SVM/MLP）
- 跨数据集泛化评估
- 可解释性分析
- 实时稳定推理演示

源码：https://github.com/WilliamK112/bci-mvp
"""

    (docs / 'release_en.md').write_text(en, encoding='utf-8')
    (docs / 'release_zh.md').write_text(zh, encoding='utf-8')
    (docs / 'reddit_post.md').write_text(reddit, encoding='utf-8')
    (docs / 'bilibili_post.md').write_text(bilibili, encoding='utf-8')
    print('Generated release pack in docs/release/')


if __name__ == '__main__':
    main()
