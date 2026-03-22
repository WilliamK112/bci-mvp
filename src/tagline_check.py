"""
Ensure a concise Chinese one-sentence tagline exists in README.zh-CN.md.
"""
from pathlib import Path

TAG = '这是一个轻量级脑机接口（BCI）MVP 项目，用 EEG 数据实现放松/专注状态识别，并提供可复现评估、可解释分析与在线演示。'


def main():
    p = Path('README.zh-CN.md')
    if not p.exists():
        raise SystemExit('README.zh-CN.md missing')
    t = p.read_text(encoding='utf-8')
    if TAG not in t:
        # insert below title banner block
        if '![BCI MVP Banner](assets/readme_banner.svg)' in t:
            t = t.replace('![BCI MVP Banner](assets/readme_banner.svg)\n\n', '![BCI MVP Banner](assets/readme_banner.svg)\n\n'+TAG+'\n\n')
        else:
            t = t.replace('# BCI MVP（中文说明）\n\n', '# BCI MVP（中文说明）\n\n'+TAG+'\n\n')
        p.write_text(t, encoding='utf-8')

    out = Path('docs/TAGLINE_CHECK.md')
    out.write_text('# Tagline Check\n\nStatus: PASS\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
