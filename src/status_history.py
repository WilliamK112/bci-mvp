"""
Append current status snapshot into historical CSV for trend tracking.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv
import re


def parse_snapshot(line: str):
    # expected: [ts] ready=READY pipeline=47/47 coverage=52/52 quality=0.938
    ready = re.search(r"ready=([^\s]+)", line)
    pipe = re.search(r"pipeline=([^\s]+)", line)
    cov = re.search(r"coverage=([^\s]+)", line)
    qual = re.search(r"quality=([^\s]+)", line)
    return {
        "ready": ready.group(1) if ready else "n/a",
        "pipeline": pipe.group(1) if pipe else "n/a",
        "coverage": cov.group(1) if cov else "n/a",
        "quality": qual.group(1) if qual else "n/a",
    }


def main():
    snap_file = Path('docs/STATUS_SNAPSHOT.txt')
    if not snap_file.exists():
        raise SystemExit('Missing docs/STATUS_SNAPSHOT.txt; run status_snapshot first.')

    line = snap_file.read_text(encoding='utf-8', errors='ignore').strip()
    parsed = parse_snapshot(line)

    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    row = {
        "recorded_at_utc": ts,
        "ready": parsed["ready"],
        "pipeline": parsed["pipeline"],
        "coverage": parsed["coverage"],
        "quality": parsed["quality"],
    }

    out = Path('docs/STATUS_HISTORY.csv')
    existed = out.exists()
    with out.open('a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=["recorded_at_utc", "ready", "pipeline", "coverage", "quality"])
        if not existed:
            w.writeheader()
        w.writerow(row)

    print(f'Updated {out}')


if __name__ == '__main__':
    main()
