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
    ["python3", "src/limitations_report.py"],
    ["python3", "src/generate_results_md.py"],
    ["python3", "src/metrics_registry.py"],
    ["python3", "src/data_provenance.py"],
    ["python3", "src/results_brief_zh.py"],
    ["python3", "src/results_brief_en.py"],
    ["python3", "src/generate_release_pack.py"],
    ["python3", "src/generate_model_card.py"],
    ["python3", "src/leaderboard.py"],
    ["python3", "src/generate_figure_gallery.py"],
    ["python3", "src/changelog_from_git.py"],
    ["python3", "src/update_docs_bundle.py"],
    ["python3", "src/update_docs_home.py"],
    ["python3", "src/executive_summary.py"],
    ["python3", "src/release_packet.py"],
    ["python3", "src/hf_space_status.py", "--space", "williamKang112/bci-mvp-demo"],
    ["python3", "src/space_smoke_test.py"],
    ["python3", "src/report_consistency_check.py"],
    ["python3", "src/env_compat_check.py"],
    ["python3", "src/repro_snapshot.py"],
    ["python3", "src/artifact_hash_manifest.py"],
    ["python3", "src/readme_quality_check.py"],
    ["python3", "src/readme_i18n_consistency.py"],
    ["python3", "src/docs_freshness_check.py"],
    ["python3", "src/navigation_health_check.py"],
    ["python3", "src/visuals_presence_check.py"],
    ["python3", "src/tagline_check.py"],
    ["python3", "src/secrets_hygiene_check.py"],
    ["python3", "src/compliance_scorecard.py"],
    ["python3", "src/project_health_badge.py"],
    ["python3", "src/one_pager.py"],
    ["python3", "src/reviewer_pack.py"],
    ["python3", "src/release_notes_latest.py"],
    ["python3", "src/release_ready_signal.py"],
    ["python3", "src/v1_release_ready.py"],
    ["python3", "src/release_tag_plan.py"],
    ["python3", "src/release_checklist.py"],
    ["python3", "src/release_dashboard.py"],
    ["python3", "src/release_ready_diagnose.py"],
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
