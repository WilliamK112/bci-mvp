"""
Check Hugging Face Space deployment readiness and emit a checklist report.
"""
from pathlib import Path
from datetime import datetime, timezone

CHECKS = [
    ('app.py', 'Root Streamlit entrypoint'),
    ('requirements.txt', 'Python dependencies'),
    ('.streamlit/config.toml', 'Streamlit runtime config'),
    ('docs/HF_SPACE_QUICKSTART.md', 'Space deployment guide'),
    ('docs/HF_SPACE_README.md', 'Space metadata README scaffold'),
    ('docs/MODEL_CARD.md', 'Model card for trust/compliance'),
]


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ['# HF Space Readiness', '', f'Generated: {ts}', '']
    score = 0
    for path, name in CHECKS:
        ok = Path(path).exists()
        lines.append(f"- [{'x' if ok else ' '}] {name} (`{path}`)")
        score += int(ok)

    lines += ['', f'**Score:** {score}/{len(CHECKS)}', '', '## Next Actions', '- If model file is not bundled, upload a lightweight demo model.', '- Verify Space app boots with `app.py` and shows both modes.']

    out = Path('docs/HF_SPACE_READINESS.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')


if __name__ == '__main__':
    main()
