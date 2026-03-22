"""
Basic secrets hygiene scan for common token patterns in tracked text files.
"""
from pathlib import Path
import re

PATTERNS = [
    (r'hf_[A-Za-z0-9]{20,}', 'HuggingFace token-like string'),
    (r'ghp_[A-Za-z0-9]{20,}', 'GitHub token-like string'),
    (r'sk-[A-Za-z0-9]{20,}', 'OpenAI-like key string'),
]

TEXT_EXT = {'.md', '.py', '.txt', '.yml', '.yaml', '.json', '.toml', '.cff'}
IGNORE_DIRS = {'.git', '.venv', 'node_modules'}


def main():
    root = Path('.')
    findings = []

    for p in root.rglob('*'):
        if not p.is_file():
            continue
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        if p.suffix.lower() not in TEXT_EXT:
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for pat, label in PATTERNS:
            for m in re.finditer(pat, text):
                findings.append((str(p), label, m.group(0)[:8] + '...'))

    lines = ['# Secrets Hygiene Check', '', '| File | Type | Preview |', '|---|---|---|']
    for f in findings:
        lines.append(f'| `{f[0]}` | {f[1]} | `{f[2]}` |')
    if not findings:
        lines.append('| - | - | No findings |')

    out = Path('docs/SECRETS_HYGIENE.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out} with {len(findings)} findings')

    if findings:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
