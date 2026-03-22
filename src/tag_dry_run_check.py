"""
Dry-run check for v1.0.0 tagging preconditions.
"""
from pathlib import Path
from datetime import datetime, timezone


def main(tag='v1.0.0'):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    checks = [
        ('Release ready signal is READY', Path('docs/RELEASE_READY_SIGNAL.md').exists() and 'SIGNAL: READY' in Path('docs/RELEASE_READY_SIGNAL.md').read_text(encoding='utf-8', errors='ignore')),
        ('Release checklist exists', Path('docs/RELEASE_CHECKLIST.md').exists()),
        ('Release notes latest exists', Path('docs/RELEASE_NOTES_LATEST.md').exists()),
        ('Tag not already in local refs', not Path('.git/refs/tags/' + tag).exists()),
    ]

    lines = ['# Tag Dry-Run Check', '', f'Generated: {ts}', f'- Target tag: `{tag}`', '', '| Check | Status |', '|---|---|']
    for name, ok in checks:
        lines.append(f'| {name} | {"✅" if ok else "❌"} |')

    ok_count = sum(int(v) for _, v in checks)
    lines += ['', f'**Dry-run status:** {ok_count}/{len(checks)}']
    lines += ['','## Suggested command','```bash',f'git tag -a {tag} -m "BCI MVP {tag}" && git push origin {tag}','```']

    out = Path('docs/TAG_DRY_RUN.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
