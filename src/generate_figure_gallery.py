"""
Generate docs/FIGURE_GALLERY.md from available assets/*.svg|png.
"""
from pathlib import Path
from datetime import datetime, timezone


def title_from_name(name: str) -> str:
    return name.replace('_', ' ').replace('-', ' ').rsplit('.', 1)[0].title()


def main():
    assets = Path('assets')
    docs = Path('docs')
    docs.mkdir(exist_ok=True)

    figs = []
    if assets.exists():
        for ext in ('*.svg', '*.png', '*.jpg', '*.jpeg', '*.webp'):
            figs.extend(sorted(assets.glob(ext)))

    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# Figure Gallery', '', f'Generated: {ts}', '']

    if not figs:
        lines += ['No figures found in `assets/`.']
    else:
        lines += ['Auto-collected visual artifacts for report/release usage.', '']
        for f in figs:
            rel = f.as_posix()
            lines += [f'## {title_from_name(f.name)}', '', f'![{f.name}]({"../"+rel})', '', f'- Path: `{rel}`', '']

    out = docs / 'FIGURE_GALLERY.md'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
