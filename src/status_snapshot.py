"""
Generate a single-line status snapshot for quick chat updates.
"""
from pathlib import Path
import re
from datetime import datetime, timezone


def extract(path, pattern, default='n/a'):
    p=Path(path)
    if not p.exists():
        return default
    txt=p.read_text(encoding='utf-8', errors='ignore')
    m=re.search(pattern, txt)
    return m.group(1) if m else default


def main():
    ts=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    ready='READY' if 'SIGNAL: READY' in Path('docs/RELEASE_READY_SIGNAL.md').read_text(encoding='utf-8', errors='ignore') else 'NOT_READY'
    pipe=extract('docs/FINAL_RELEASE_CANDIDATE.md', r'\*\*Pipeline success:\*\*\s*([^\n]+)')
    cov=extract('docs/FINAL_RELEASE_CANDIDATE.md', r'\*\*Output coverage:\*\*\s*([^\n]+)')
    q=extract('docs/QUALITY_SCORECARD.md', r'\*\*Overall quality index:\*\*\s*([0-9.]+)')

    line=f"[{ts}] ready={ready} pipeline={pipe} coverage={cov} quality={q}"
    out=Path('docs/STATUS_SNAPSHOT.txt')
    out.write_text(line+'\n', encoding='utf-8')
    print(line)
    print(f'Generated {out}')


if __name__=='__main__':
    main()
