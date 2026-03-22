"""
Safe Hugging Face Space publish helper.
- Uses HF_TOKEN from environment (never hardcode in repo)
- Creates/updates Space and pushes current branch
"""
from pathlib import Path
import os
import subprocess


def run(cmd):
    p = subprocess.run(cmd, check=False, capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def main(username='williamKang112', space_name='bci-mvp-demo', private=False):
    token = os.getenv('HF_TOKEN')
    if not token:
        raise SystemExit('HF_TOKEN not set. Export token in shell first.')

    # login non-interactive
    code, out, err = run(['huggingface-cli', 'login', '--token', token])
    if code != 0:
        raise SystemExit(f'huggingface-cli login failed: {err or out}')

    # create space (ignore if exists)
    args = [
        'huggingface-cli', 'repo', 'create', space_name,
        '--type', 'space', '--space_sdk', 'streamlit',
        '--organization', username,
    ]
    if private:
        args.append('--private')
    run(args)

    remote = f'https://huggingface.co/spaces/{username}/{space_name}'
    run(['git', 'remote', 'remove', 'hf'])
    code, out, err = run(['git', 'remote', 'add', 'hf', remote])
    if code != 0 and 'already exists' not in (err + out):
        raise SystemExit(f'git remote add failed: {err or out}')

    code, out, err = run(['git', 'push', '-u', 'hf', 'main'])
    if code != 0:
        raise SystemExit(f'git push hf failed: {err or out}')

    Path('docs/HF_PUBLISH_RESULT.md').write_text(
        f'# HF Publish Result\n\n- Space: https://huggingface.co/spaces/{username}/{space_name}\n- Status: pushed from current main\n',
        encoding='utf-8'
    )
    print(f'Published: https://huggingface.co/spaces/{username}/{space_name}')


if __name__ == '__main__':
    main()
