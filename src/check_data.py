from pathlib import Path
import numpy as np
import mne


def inspect_one_edf(edf_path: Path, epoch_sec=2.0, overlap=0.5):
    info = {"file": edf_path.name, "ok": False, "error": "", "n_channels": 0, "sfreq": 0.0, "duration_sec": 0.0, "est_epochs": 0}
    try:
        raw = mne.io.read_raw_edf(str(edf_path), preload=False, verbose=False)
        raw.pick(picks="eeg", exclude="bads")

        sfreq = float(raw.info["sfreq"])
        duration_sec = raw.n_times / sfreq if sfreq > 0 else 0.0
        win = int(epoch_sec * sfreq)
        step = int(win * (1 - overlap))
        if step <= 0:
            raise ValueError("Invalid overlap")
        est_epochs = max(0, (raw.n_times - win) // step + 1)

        info.update({"ok": True, "n_channels": len(raw.ch_names), "sfreq": sfreq, "duration_sec": duration_sec, "est_epochs": est_epochs})
    except Exception as e:
        info["error"] = f"{type(e).__name__}: {e}"
    return info


def scan(folder):
    edfs = sorted(Path(folder).glob("*.edf"))
    return [inspect_one_edf(f) for f in edfs]


def main():
    groups = {"relaxed": "data/relaxed", "focused": "data/focused"}
    all_r = []
    for name, path in groups.items():
        rs = scan(path)
        print(f"[{name}] files={len(rs)}")
        for r in rs:
            print(r)
        all_r.extend(rs)

    ok = [x for x in all_r if x["ok"]]
    bad = [x for x in all_r if not x["ok"]]
    print(f"Total={len(all_r)} Readable={len(ok)} Failed={len(bad)}")
    if ok:
        print("Median sfreq", float(np.median([x["sfreq"] for x in ok])))


if __name__ == "__main__":
    main()
