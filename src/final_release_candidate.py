"""
Build a final release-candidate bundle by orchestrating all key doc/report generators.
Writes a tracked summary: docs/FINAL_RELEASE_CANDIDATE.md
"""
from pathlib import Path
from datetime import datetime, timezone
import subprocess

STEPS = [
    ["python3", "src/build_report.py"],
    ["python3", "src/limitations_report.py"],
    ["python3", "src/generate_results_md.py"],
    ["python3", "src/metrics_registry.py"],
    ["python3", "src/data_provenance.py"],
    ["python3", "src/results_brief_zh.py"],
    ["python3", "src/results_brief_en.py"],
    ["python3", "src/release_readiness.py"],
    ["python3", "src/hf_space_readiness.py"],
    ["python3", "src/leaderboard.py"],
    ["python3", "src/generate_figure_gallery.py"],
    ["python3", "src/changelog_from_git.py"],
    ["python3", "src/generate_release_pack.py"],
    ["python3", "src/generate_model_card.py"],
    ["python3", "src/update_docs_bundle.py"],
    ["python3", "src/update_docs_home.py"],
    ["python3", "src/generate_status_badges.py"],
    ["python3", "src/risk_register.py"],
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
    ["python3", "src/release_ready_badge.py"],
    ["python3", "src/v1_release_ready.py"],
    ["python3", "src/release_tag_plan.py"],
    ["python3", "src/release_checklist.py"],
    ["python3", "src/release_dashboard.py"],
    ["python3", "src/release_ready_diagnose.py"],
]

OUTPUTS = [
    "docs/TECHNICAL_REPORT.md",
    "docs/LIMITATIONS.md",
    "docs/RELEASE_READINESS.md",
    "docs/HF_SPACE_READINESS.md",
    "docs/HF_SPACE_STATUS.md",
    "docs/SPACE_SMOKE_TEST.md",
    "docs/SPACE_USER_GUIDE.md",
    "docs/MODEL_LEADERBOARD.md",
    "docs/FIGURE_GALLERY.md",
    "docs/CHANGELOG_AUTO.md",
    "docs/MODEL_CARD.md",
    "docs/MATH_NOTATION.md",
    "docs/METHODS.md",
    "docs/RESULTS.md",
    "docs/METRICS_REGISTRY.md",
    "docs/DATA_PROVENANCE.md",
    "docs/RESULTS_BRIEF_ZH.md",
    "docs/RESULTS_BRIEF_EN.md",
    "docs/DOCS_BUNDLE_INDEX.md",
    "docs/RISK_REGISTER.md",
    "docs/EXECUTIVE_SUMMARY.md",
    "docs/RELEASE_PACKET.md",
    "docs/REPORT_CONSISTENCY.md",
    "docs/ENV_COMPAT.md",
    "docs/REPRO_SNAPSHOT.md",
    "docs/ARTIFACT_HASH_MANIFEST.md",
    "docs/README_QUALITY.md",
    "docs/README_I18N_CONSISTENCY.md",
    "docs/DOCS_FRESHNESS.md",
    "docs/NAVIGATION_HEALTH.md",
    "docs/VISUALS_PRESENCE.md",
    "docs/TAGLINE_CHECK.md",
    "docs/SECRETS_HYGIENE.md",
    "docs/COMPLIANCE_SCORECARD.md",
    "assets/badge_project_health.svg",
    "docs/ONE_PAGER.md",
    "docs/REVIEWER_PACK.md",
    "docs/RELEASE_NOTES_LATEST.md",
    "docs/RELEASE_READY_SIGNAL.md",
    "assets/badge_release_ready.svg",
    "docs/V1_RELEASE_READY.md",
    "docs/RELEASE_TAG_PLAN.md",
    "docs/RELEASE_CHECKLIST.md",
    "docs/RELEASE_DASHBOARD.md",
    "docs/RELEASE_READY_DIAGNOSE.md",
    "docs/release/release_en.md",
    "docs/release/release_zh.md",
    "docs/release/reddit_post.md",
    "docs/release/bilibili_post.md",
    "CITATION.cff",
]


def run(cmd):
    p = subprocess.run(cmd, check=False, capture_output=True, text=True)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = ["# Final Release Candidate", "", f"Generated: {ts}", "", "## Step Results"]
    ok = 0
    for s in STEPS:
        code, out, err = run(s)
        status = "OK" if code == 0 else f"FAIL({code})"
        lines.append(f"- [{status}] `{' '.join(s)}`")
        if code == 0:
            ok += 1
        if err:
            lines.append(f"  - stderr: `{err[:220]}`")

    lines += ["", "## Output Inventory"]
    present = 0
    for p in OUTPUTS:
        exists = Path(p).exists()
        lines.append(f"- [{'x' if exists else ' '}] `{p}`")
        present += int(exists)

    lines += ["", f"**Pipeline success:** {ok}/{len(STEPS)}", f"**Output coverage:** {present}/{len(OUTPUTS)}"]

    out = Path("docs/FINAL_RELEASE_CANDIDATE.md")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated {out}")


if __name__ == '__main__':
    main()
