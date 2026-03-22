"""
Generate ready-to-send short status message templates (EN/ZH) from latest snapshot.
"""
from pathlib import Path
from datetime import datetime, timezone


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    snap = Path('docs/STATUS_SNAPSHOT.txt').read_text(encoding='utf-8', errors='ignore').strip() if Path('docs/STATUS_SNAPSHOT.txt').exists() else 'status=n/a'
    ready = 'READY' if 'ready=READY' in snap else 'NOT_READY'

    en = f"[BCI MVP] {ready} | {snap} | Demo: https://huggingface.co/spaces/williamKang112/bci-mvp-demo"
    zh = f"【BCI MVP】当前状态：{ready}｜{snap}｜演示链接：https://huggingface.co/spaces/williamKang112/bci-mvp-demo"

    lines = [
        '# Status Message Templates',
        '',
        f'Generated: {ts}',
        '',
        '## EN',
        en,
        '',
        '## ZH',
        zh,
    ]

    out = Path('docs/STATUS_MESSAGE_TEMPLATES.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
