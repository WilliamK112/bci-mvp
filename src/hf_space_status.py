"""
Check Hugging Face Space runtime/build status and write a tracked report.
Usage:
  python src/hf_space_status.py --space williamKang112/bci-mvp-demo
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
from huggingface_hub import HfApi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--space', default='williamKang112/bci-mvp-demo')
    args = ap.parse_args()

    api = HfApi()
    info = api.space_info(repo_id=args.space)

    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        '# HF Space Status',
        '',
        f'Generated: {ts}',
        f'- Space: `{args.space}`',
        f'- URL: https://huggingface.co/spaces/{args.space}',
        '',
        '## Runtime',
        f'- sdk: `{getattr(info, "sdk", None)}`',
        f'- likes: `{getattr(info, "likes", None)}`',
        f'- private: `{getattr(info, "private", None)}`',
        f'- disabled: `{getattr(info, "disabled", None)}`',
        '',
        '## Build/Stage (if available)',
        f'- stage: `{getattr(info, "stage", None)}`',
        f'- sha: `{getattr(info, "sha", None)}`',
        f'- last_modified: `{getattr(info, "last_modified", None)}`',
    ]

    out = Path('docs/HF_SPACE_STATUS.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
