"""
README quality guard:
- ensures bilingual switch exists
- keeps main README concise (line-count threshold)
"""
from pathlib import Path


def main(max_lines=120):
    readme = Path('README.md')
    zh = Path('README.zh-CN.md')

    issues = []
    if not readme.exists():
        issues.append('README.md missing')
    else:
        text = readme.read_text(encoding='utf-8', errors='ignore')
        lines = text.splitlines()
        if len(lines) > max_lines:
            issues.append(f'README too long: {len(lines)} lines > {max_lines}')
        if '## Language' not in text:
            issues.append('Missing "## Language" section in README.md')
        if 'README.zh-CN.md' not in text:
            issues.append('Missing zh README link in README.md')

    if not zh.exists():
        issues.append('README.zh-CN.md missing')

    out = Path('docs/README_QUALITY.md')
    if issues:
        out.write_text('# README Quality Check\n\nStatus: FAIL\n\n' + '\n'.join(f'- {i}' for i in issues) + '\n', encoding='utf-8')
        print(f'Generated {out} (FAIL)')
        raise SystemExit(2)

    out.write_text('# README Quality Check\n\nStatus: PASS\n\n- Main README is concise and bilingual link is present.\n', encoding='utf-8')
    print(f'Generated {out} (PASS)')


if __name__ == '__main__':
    main()
