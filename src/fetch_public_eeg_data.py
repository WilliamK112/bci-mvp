"""
Fetch public EEG data (MNE EEGBCI) and convert to EDF files for existing pipeline.
Creates:
  data/relaxed/*.edf
  data/focused/*.edf

Label mapping (proxy for MVP demo):
- relaxed  <- runs 1/2 (baseline eyes open/closed style resting-like)
- focused  <- runs 3/4 (motor/execution-like task runs)

Note: This is a pragmatic public-data bootstrap for pipeline verification.
"""
from pathlib import Path
import mne
from mne.datasets import eegbci


def export_edf(raw: mne.io.BaseRaw, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # mne export API
    raw.export(str(out_path), fmt="edf", overwrite=True)


def main(subjects=(1, 2), max_files_per_class=6):
    out_relaxed = Path("data/relaxed")
    out_focused = Path("data/focused")
    out_relaxed.mkdir(parents=True, exist_ok=True)
    out_focused.mkdir(parents=True, exist_ok=True)

    # EEGBCI run IDs (pragmatic mapping)
    relaxed_runs = [1, 2]
    focused_runs = [3, 4]

    relaxed_count = 0
    focused_count = 0

    for subj in subjects:
        # relaxed
        for run in relaxed_runs:
            if relaxed_count >= max_files_per_class:
                break
            files = eegbci.load_data(subj, [run])
            for f in files:
                if relaxed_count >= max_files_per_class:
                    break
                raw = mne.io.read_raw_edf(f, preload=True, verbose=False)
                raw.pick_types(eeg=True)
                out = out_relaxed / f"sub{subj:02d}_run{run:02d}_{relaxed_count:03d}.edf"
                export_edf(raw, out)
                relaxed_count += 1

        # focused
        for run in focused_runs:
            if focused_count >= max_files_per_class:
                break
            files = eegbci.load_data(subj, [run])
            for f in files:
                if focused_count >= max_files_per_class:
                    break
                raw = mne.io.read_raw_edf(f, preload=True, verbose=False)
                raw.pick_types(eeg=True)
                out = out_focused / f"sub{subj:02d}_run{run:02d}_{focused_count:03d}.edf"
                export_edf(raw, out)
                focused_count += 1

        if relaxed_count >= max_files_per_class and focused_count >= max_files_per_class:
            break

    print(f"Exported relaxed={relaxed_count}, focused={focused_count}")
    print("Done: data/relaxed and data/focused")


if __name__ == "__main__":
    main()
