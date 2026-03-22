"""
Generate Hugging Face Space publish commands for this repo.
No credentials required; prints exact commands for user-run publish.
"""
from pathlib import Path
from datetime import datetime, timezone


def main(username='williamKang112', space_name='bci-mvp-demo'):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

    lines = [
        '# Hugging Face Publish Helper',
        '',
        f'Generated: {ts}',
        '',
        '## Prerequisites',
        '- Install: `pip install -U huggingface_hub`',
        '- Login: `huggingface-cli login`',
        '',
        '## Create Space (if not exists)',
        f'`huggingface-cli repo create {space_name} --type space --space_sdk streamlit --organization {username}`',
        '',
        '## Add remote and push',
        f'`git remote add hf https://huggingface.co/spaces/{username}/{space_name}`',
        '`git push hf main`',
        '',
        '## Required files checklist',
        '- app.py',
        '- requirements.txt',
        '- .streamlit/config.toml',
        '- src/',
        '- docs/HF_SPACE_QUICKSTART.md',
        '',
        '## Notes',
        '- If model file is large, use a lightweight demo model for Space runtime.',
        '- Keep API keys out of repo and use Space Secrets when needed.',
    ]

    out = Path('docs/HF_PUBLISH_HELPER.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
