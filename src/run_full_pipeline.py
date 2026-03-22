"""
Run full reproducible pipeline (best-effort orchestration).
This script chains major steps and records a run manifest.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess

STEPS = [
    ["python3", "src/benchmark.py"],
    ["python3", "src/deep_baseline.py"],
    ["python3", "src/merge_results.py"],
    ["python3", "src/plot_all_models.py"],
    ["python3", "src/plot_results.py"],
    ["python3", "src/build_report.py"],
    ["python3", "src/generate_release_pack.py"],
    ["python3", "src/generate_model_card.py"],
    ["python3", "src/validate_artifacts.py"],
]


def run_step(cmd):
    try:
        p = subprocess.run(cmd, check=False, capture_output=True, text=True)
        return {
            "cmd": " ".join(cmd),
            "code": p.returncode,
            "stdout": p.stdout[-1500:],
            "stderr": p.stderr[-1500:],
        }
    except Exception as e:
        return {
            "cmd": " ".join(cmd),
            "code": -1,
            "stdout": "",
            "stderr": str(e),
        }


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    results = []
    ok = True

    for step in STEPS:
        r = run_step(step)
        results.append(r)
        if r["code"] != 0:
            ok = False

    out = Path("outputs")
    out.mkdir(exist_ok=True)
    manifest = {
        "timestamp_utc": ts,
        "overall_ok": ok,
        "steps": results,
    }
    fp = out / "pipeline_manifest.json"
    fp.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Saved {fp}")
    print(f"overall_ok={ok}")


if __name__ == "__main__":
    main()
