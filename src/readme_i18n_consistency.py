"""
Check consistency between README.md and README.zh-CN.md branding essentials.
"""
from pathlib import Path


def has(s, x):
    return x in s


def main():
    en = Path('README.md').read_text(encoding='utf-8', errors='ignore') if Path('README.md').exists() else ''
    zh = Path('README.zh-CN.md').read_text(encoding='utf-8', errors='ignore') if Path('README.zh-CN.md').exists() else ''

    checks = [
        ('banner', 'assets/readme_banner.svg'),
        ('python_badge', 'img.shields.io/badge/Python'),
        ('license_badge', 'img.shields.io/badge/License-MIT'),
        ('space_link', 'huggingface.co/spaces/williamKang112/bci-mvp-demo'),
    ]

    lines=['# README I18N Consistency','','| Item | EN | ZH |','|---|---|---|']
    fail=0
    for name, token in checks:
        en_ok=has(en, token); zh_ok=has(zh, token)
        lines.append(f"| {name} | {'✅' if en_ok else '❌'} | {'✅' if zh_ok else '❌'} |")
        if not (en_ok and zh_ok):
            fail += 1

    status='PASS' if fail==0 else 'FAIL'
    lines += ['', f'**Status:** {status}', f'**Missing items:** {fail}']
    out=Path('docs/README_I18N_CONSISTENCY.md')
    out.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(f'Generated {out} ({status})')
    if fail:
        raise SystemExit(2)

if __name__=='__main__':
    main()
