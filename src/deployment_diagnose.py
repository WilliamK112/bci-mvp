"""
Generate deployment diagnostics summary (GitHub + HF Space pointers).
"""
from pathlib import Path
from datetime import datetime, timezone


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        '# Deployment Diagnostics',
        '',
        f'Generated: {ts}',
        '',
        '## Endpoints',
        '- GitHub repo: https://github.com/WilliamK112/bci-mvp',
        '- HF Space page: https://huggingface.co/spaces/williamKang112/bci-mvp-demo',
        '- HF Space direct URL: https://williamkang112-bci-mvp-demo.hf.space',
        '',
        '## Common Failure Checks',
        '- Docker app port mismatch (Space metadata `app_port` vs container exposed port)',
        '- Missing Space metadata YAML header in README',
        '- Build cache stale after force-push (retry/restart Space build)',
        '- Network/proxy blocks causing `ERR_CONNECTION_RESET` on client side',
        '',
        '## Fast Recovery Steps',
        '1. Verify README frontmatter has `sdk: docker` and `app_port: 8000`',
        '2. Push latest commit to HF Space remote',
        '3. Check Space status using `python src/hf_space_status.py --space williamKang112/bci-mvp-demo`',
        '4. Re-test both HF page URL and hf.space direct URL',
    ]

    out = Path('docs/DEPLOYMENT_DIAGNOSE.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
