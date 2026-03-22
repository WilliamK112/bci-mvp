"""
Generate Chinese ops digest from current status artifacts.
"""
from pathlib import Path
from datetime import datetime, timezone


def read(path):
    p=Path(path)
    return p.read_text(encoding='utf-8', errors='ignore') if p.exists() else ''


def main():
    ts=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    sig='READY' if 'SIGNAL: READY' in read('docs/RELEASE_READY_SIGNAL.md') else 'NOT_READY'
    launch='GREEN' if 'State:** GREEN' in read('docs/LAUNCH_STATUS.md') else 'YELLOW'
    guard='PASS' if 'Guard status: PASS' in read('docs/RELEASE_GUARD_REPORT.md') else 'FAIL'

    lines=[
        '# 运维摘要（中文）','',f'生成时间：{ts}','',
        f'- 发布就绪信号：**{sig}**',
        f'- 上线状态：**{launch}**',
        f'- 发布守卫：**{guard}**',
        '',
        '## 快速入口',
        '- `docs/OPERATOR_QUICKLINKS.md`',
        '- `docs/RELEASE_DASHBOARD.md`',
        '- `docs/STATUS_SNAPSHOT_ZH.md`',
    ]

    out=Path('docs/OPS_DIGEST_ZH.md')
    out.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__=='__main__':
    main()
