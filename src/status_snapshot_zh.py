"""
Generate Chinese status snapshot from STATUS_SNAPSHOT.txt and key docs.
"""
from pathlib import Path
from datetime import datetime, timezone


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    src = Path('docs/STATUS_SNAPSHOT.txt')
    line = src.read_text(encoding='utf-8', errors='ignore').strip() if src.exists() else 'n/a'

    ready = 'READY' if 'ready=READY' in line else 'NOT_READY'

    lines = [
        '# 状态快照（中文）',
        '',
        f'生成时间：{ts}',
        '',
        f'- 发布就绪信号：**{ready}**',
        f'- 原始快照：`{line}`',
        '',
        '## 参考',
        '- `docs/STATUS_SNAPSHOT.txt`',
        '- `docs/RELEASE_DASHBOARD.md`',
        '- `docs/FINAL_RELEASE_CANDIDATE.md`',
    ]

    out = Path('docs/STATUS_SNAPSHOT_ZH.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
