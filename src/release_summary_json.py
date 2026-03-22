"""
Generate machine-readable release summary JSON for integrations.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import re


def extract(pattern, text, default=None):
    m = re.search(pattern, text)
    return m.group(1) if m else default


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    rc_txt = Path('docs/FINAL_RELEASE_CANDIDATE.md').read_text(encoding='utf-8', errors='ignore') if Path('docs/FINAL_RELEASE_CANDIDATE.md').exists() else ''
    sig_txt = Path('docs/RELEASE_READY_SIGNAL.md').read_text(encoding='utf-8', errors='ignore') if Path('docs/RELEASE_READY_SIGNAL.md').exists() else ''

    data = {
        'generated_at_utc': ts,
        'ready': 'SIGNAL: READY' in sig_txt,
        'pipeline_success': extract(r'\*\*Pipeline success:\*\*\s*([^\n]+)', rc_txt, 'n/a'),
        'output_coverage': extract(r'\*\*Output coverage:\*\*\s*([^\n]+)', rc_txt, 'n/a'),
        'demo_url': 'https://huggingface.co/spaces/williamKang112/bci-mvp-demo',
        'repo_url': 'https://github.com/WilliamK112/bci-mvp',
    }

    out = Path('docs/RELEASE_SUMMARY.json')
    out.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
