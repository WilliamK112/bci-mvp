"""
Generate compliance/security scorecard from hygiene/readiness artifacts.
"""
from pathlib import Path
import re
from datetime import datetime, timezone


def parse_missing_count(path, label):
    p = Path(path)
    if not p.exists():
        return None
    txt = p.read_text(encoding='utf-8', errors='ignore')
    m = re.search(label + r'\*\*:\s*(\d+)', txt)
    return int(m.group(1)) if m else None


def parse_zero_findings(path):
    p = Path(path)
    if not p.exists():
        return False
    txt = p.read_text(encoding='utf-8', errors='ignore')
    return 'No findings' in txt


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    nav_missing = parse_missing_count('docs/NAVIGATION_HEALTH.md', 'Missing links: ')
    readme_missing = parse_missing_count('docs/README_I18N_CONSISTENCY.md', 'Missing items: ')
    secrets_ok = parse_zero_findings('docs/SECRETS_HYGIENE.md')

    checks = [
        ('Navigation links complete', nav_missing == 0 if nav_missing is not None else False),
        ('README i18n consistency clean', readme_missing == 0 if readme_missing is not None else False),
        ('Secrets hygiene clean', secrets_ok),
        ('Citation metadata exists', Path('CITATION.cff').exists()),
    ]

    passed = sum(int(ok) for _, ok in checks)
    total = len(checks)

    lines = ['# Compliance Scorecard', '', f'Generated: {ts}', '', '| Check | Status |', '|---|---|']
    for name, ok in checks:
        lines.append(f'| {name} | {"✅" if ok else "❌"} |')

    lines += ['', f'**Compliance score:** {passed}/{total}', f'**Compliance index:** {passed/total:.3f}']

    out = Path('docs/COMPLIANCE_SCORECARD.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
