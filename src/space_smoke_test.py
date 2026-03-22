"""
Smoke test for deployed Hugging Face Space endpoints.
Checks page and direct hf.space URL reachability and records status.
"""
from pathlib import Path
from datetime import datetime, timezone
import urllib.request

URLS = [
    'https://huggingface.co/spaces/williamKang112/bci-mvp-demo',
    'https://williamkang112-bci-mvp-demo.hf.space',
]


def check(url: str, timeout=15):
    req = urllib.request.Request(url, headers={'User-Agent': 'bci-mvp-smoke-test/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return True, r.getcode(), ''
    except Exception as e:
        return False, None, str(e)


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# Space Smoke Test', '', f'Generated: {ts}', '', '| URL | OK | HTTP | Note |', '|---|---|---|---|']
    ok_count = 0
    for u in URLS:
        ok, code, note = check(u)
        ok_count += int(ok)
        lines.append(f"| {u} | {'✅' if ok else '❌'} | {code if code is not None else '-'} | {note[:120]} |")

    lines += ['', f'**Summary:** {ok_count}/{len(URLS)} endpoints reachable']

    out = Path('docs/SPACE_SMOKE_TEST.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
