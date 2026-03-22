"""
Validate machine-readable release summary JSON schema.
"""
from pathlib import Path
import json

REQUIRED = ['generated_at_utc', 'ready', 'pipeline_success', 'output_coverage', 'demo_url', 'repo_url']


def main():
    p = Path('docs/RELEASE_SUMMARY.json')
    if not p.exists():
        raise SystemExit('Missing docs/RELEASE_SUMMARY.json')
    obj = json.loads(p.read_text(encoding='utf-8'))

    missing = [k for k in REQUIRED if k not in obj]
    lines = ['# Release Summary Validation', '', '| Field | Status |', '|---|---|']
    for k in REQUIRED:
        lines.append(f"| `{k}` | {'✅' if k in obj else '❌'} |")

    # optional LOSO block validation
    loso_ok = True
    loso = obj.get('cross_subject_loso')
    loso_fields = ['subjects', 'mean_accuracy', 'mean_f1', 'mean_auc']
    if loso is not None:
        for k in loso_fields:
            if k not in loso:
                loso_ok = False

    lines.append(f"| `cross_subject_loso` schema | {'✅' if loso_ok else '❌'} |")

    out = Path('docs/RELEASE_SUMMARY_VALIDATION.md')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Generated {out}')

    if missing or not loso_ok:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
