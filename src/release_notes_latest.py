"""
Generate latest release notes from recent commits + key artifact links.
"""
from pathlib import Path
import subprocess
from datetime import datetime, timezone


def git_lines(n=12):
    p = subprocess.run(['git', 'log', f'-n{n}', '--pretty=format:%h %s'], capture_output=True, text=True)
    return p.stdout.splitlines() if p.returncode == 0 else []


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    commits = git_lines(12)
    lines = [
        '# Latest Release Notes',
        '',
        f'Generated: {ts}',
        '',
        '## Highlights',
        '- Project health badge + compliance/quality scorecards',
        '- Full RC pipeline with deployment, consistency, and security checks',
        '- Bilingual concise README + hero banner + docs home navigation',
        '',
        '## Recent Commits',
    ]
    lines += [f'- `{c}`' for c in commits] if commits else ['- n/a']

    lines += [
        '',
        '## Key Links',
        '- Repo: https://github.com/WilliamK112/bci-mvp',
        '- Demo: https://huggingface.co/spaces/williamKang112/bci-mvp-demo',
        '- One pager: `docs/ONE_PAGER.md`',
        '- Final RC: `docs/FINAL_RELEASE_CANDIDATE.md`',
    ]

    out = Path('docs/RELEASE_NOTES_LATEST.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
