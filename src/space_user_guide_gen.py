"""
Generate concise end-user guide for the public Space demo.
"""
from pathlib import Path
from datetime import datetime, timezone


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        '# Space User Guide',
        '',
        f'Generated: {ts}',
        '',
        '## Access',
        '- https://huggingface.co/spaces/williamKang112/bci-mvp-demo',
        '',
        '## Modes',
        '- **Single Prediction**: input 32-dim feature vector and get class probabilities.',
        '- **Streaming (Simulated)**: view real-time probability curve with EMA+hysteresis stabilization.',
        '',
        '## Runtime Indicator',
        '- `REAL_MODEL`: using trained model file',
        '- `MOCK_FALLBACK`: model not present; deterministic fallback for demo continuity',
        '',
        '## Troubleshooting',
        '- If blank or unavailable, wait for Space rebuild and refresh.',
        '- If connection resets, retry both page URL and direct `hf.space` URL.',
        '- Use project diagnostics docs: `docs/HF_SPACE_STATUS.md`, `docs/SPACE_SMOKE_TEST.md`.',
    ]
    out = Path('docs/SPACE_USER_GUIDE.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
