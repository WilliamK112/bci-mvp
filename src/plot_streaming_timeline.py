"""
Simulates a real-time BCI streaming session by concatenating a Relaxed and Focused run,
and visualizes the effect of Hysteresis, Debounce, and Dynamic Alpha smoothing.
Outputs:
- outputs/streaming_timeline_comparison.png
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from pathlib import Path

from src.preprocess import load_edf_extract_features
from src.streaming import StreamingStateFilter, StreamingConfig

def simulate_stream():
    print("[1] Loading model and building simulated EEG timeline (Relaxed -> Focused)...")
    model_path = Path("outputs/model_rf_tuned.joblib")
    if not model_path.exists():
        model_path = Path("outputs/model_rf_real.joblib")
        
    clf = joblib.load(model_path)
    
    # Load one relaxed run and one focused run
    try:
        X_relax = load_edf_extract_features("data/dataset_a/relaxed/sub01_run01_000.edf")
        X_focus = load_edf_extract_features("data/dataset_a/focused/sub01_run02_001.edf")
    except Exception as e:
        print(f"Fallback to generic load: {e}")
        from src.preprocess import build_dataset_from_folder
        X_relax, _ = build_dataset_from_folder("data/relaxed", 0)
        X_focus, _ = build_dataset_from_folder("data/focused", 1)
        X_relax = X_relax[:60]
        X_focus = X_focus[:60]

    # Concatenate to simulate a state transition over time
    X_stream = np.vstack([X_relax, X_focus])
    n_epochs = len(X_stream)
    time_axis = np.arange(n_epochs)

    print(f"  Total epochs in stream: {n_epochs}")

    # Generate raw probabilities from the classifier
    print("[2] Generating raw ML probabilities...")
    # The pipeline handles scaling internally
    raw_probs = clf.predict_proba(X_stream)[:, 1]

    print("[3] Filtering through StreamingStateFilter (Standard vs Advanced)...")
    # Config 1: Basic EMA (Old behavior)
    cfg_basic = StreamingConfig(alpha=0.3, high_threshold=0.65, low_threshold=0.35, debounce_ticks=1, dynamic_alpha=False)
    filter_basic = StreamingStateFilter(cfg_basic)
    
    # Config 2: Advanced (Debounce + Dynamic Alpha)
    cfg_adv = StreamingConfig(alpha=0.3, high_threshold=0.65, low_threshold=0.35, debounce_ticks=3, dynamic_alpha=True)
    filter_adv = StreamingStateFilter(cfg_adv)

    res_basic = {"smoothed": [], "state": []}
    res_adv = {"smoothed": [], "state": []}

    for p in raw_probs:
        out_b = filter_basic.update(p)
        res_basic["smoothed"].append(out_b["smoothed_focused_prob"])
        res_basic["state"].append(1.0 if out_b["state"] == "focused" else 0.0)
        
        out_a = filter_adv.update(p)
        res_adv["smoothed"].append(out_a["smoothed_focused_prob"])
        res_adv["state"].append(1.0 if out_a["state"] == "focused" else 0.0)

    print("[4] Generating Timeline Visualization...")
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Truth background shading
    for ax in axes:
        ax.axvspan(0, len(X_relax), color='green', alpha=0.1, label='True State: Relaxed')
        ax.axvspan(len(X_relax), n_epochs, color='red', alpha=0.1, label='True State: Focused')
        ax.axhline(0.65, color='gray', linestyle='--', alpha=0.5, label='High Threshold (0.65)')
        ax.axhline(0.35, color='gray', linestyle='--', alpha=0.5, label='Low Threshold (0.35)')

    # Plot 1: Standard EMA
    axes[0].set_title("Standard EMA Streaming (Prone to Flicker)", fontsize=14)
    axes[0].plot(time_axis, raw_probs, color='black', alpha=0.2, label='Raw RF Probability')
    axes[0].plot(time_axis, res_basic["smoothed"], color='blue', linewidth=2, label='EMA Smoothed Prob')
    axes[0].step(time_axis, res_basic["state"], color='orange', linewidth=2, label='Discrete State Output')
    axes[0].set_ylabel("Probability / State")
    axes[0].set_ylim([-0.1, 1.1])
    axes[0].legend(loc='upper left', bbox_to_anchor=(1.02, 1))

    # Plot 2: Advanced EMA
    axes[1].set_title("Advanced Streaming (Debounce=3, Dynamic Alpha=True)", fontsize=14)
    axes[1].plot(time_axis, raw_probs, color='black', alpha=0.2, label='Raw RF Probability')
    axes[1].plot(time_axis, res_adv["smoothed"], color='blue', linewidth=2, label='Dynamic Smoothed Prob')
    axes[1].step(time_axis, res_adv["state"], color='orange', linewidth=2, label='Discrete State Output')
    axes[1].set_ylabel("Probability / State")
    axes[1].set_xlabel("Time (Epochs)")
    axes[1].set_ylim([-0.1, 1.1])
    axes[1].legend(loc='upper left', bbox_to_anchor=(1.02, 1))

    plt.tight_layout()
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    
    out_path = out_dir / "streaming_timeline_comparison.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"[5] Saved high-res visualization to {out_path}")

if __name__ == "__main__":
    simulate_stream()
