from pathlib import Path
from datetime import datetime, timezone


def append_progress(title: str, details: str):
    log = Path("logs/progress.md")
    log.parent.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    block = f"\n## {ts} — {title}\n\n{details}\n"
    if log.exists():
        log.write_text(log.read_text(encoding="utf-8") + block, encoding="utf-8")
    else:
        log.write_text("# BCI MVP Progress Log\n" + block, encoding="utf-8")


def update_readme_latest():
    readme = Path("README.md")
    log = Path("logs/progress.md")
    if not readme.exists() or not log.exists():
        return

    entries = log.read_text(encoding="utf-8").strip().split("\n## ")
    if not entries:
        return
    latest = entries[-1]
    latest_header = latest.splitlines()[0].strip()

    marker_start = "<!-- LATEST_PROGRESS_START -->"
    marker_end = "<!-- LATEST_PROGRESS_END -->"
    section = (
        f"{marker_start}\n"
        f"## Latest Progress\n"
        f"- {latest_header}\n"
        f"- Full log: `logs/progress.md`\n"
        f"{marker_end}"
    )

    text = readme.read_text(encoding="utf-8")
    if marker_start in text and marker_end in text:
        pre = text.split(marker_start)[0]
        post = text.split(marker_end)[1]
        new_text = pre + section + post
    else:
        new_text = text + "\n\n" + section + "\n"

    readme.write_text(new_text, encoding="utf-8")


if __name__ == "__main__":
    append_progress(
        "Added continuous progress logging utility",
        "Created `src/progress_log.py` to append UTC-stamped progress entries and sync latest update into README."
    )
    update_readme_latest()
    print("progress log updated")
