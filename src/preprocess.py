from pathlib import Path
import numpy as np
import mne
from scipy.signal import welch

BANDS = {
    "delta": (1, 4),
    "theta": (4, 8),
    "alpha": (8, 13),
    "beta": (13, 30),
}


def bandpower_1d(x, sfreq, bands=BANDS):
    freqs, psd = welch(x, fs=sfreq, nperseg=min(len(x), int(2 * sfreq)))
    feat = []
    for _, (fmin, fmax) in bands.items():
        idx = (freqs >= fmin) & (freqs < fmax)
        bp = np.trapezoid(psd[idx], freqs[idx]) if np.any(idx) else 0.0
        feat.append(bp)
    return np.array(feat, dtype=float)


def epoch_to_features(epoch_data, sfreq, bands=BANDS):
    ch_feats = []
    for ch in range(epoch_data.shape[0]):
        ch_feats.append(bandpower_1d(epoch_data[ch], sfreq, bands))
    return np.concatenate(ch_feats, axis=0)


def load_edf_extract_features(
    edf_path: str,
    epoch_sec: float = 2.0,
    overlap: float = 0.5,
    l_freq: float = 1.0,
    h_freq: float = 40.0,
    max_channels: int = 8,
):
    raw = mne.io.read_raw_edf(edf_path, preload=True, verbose=False)
    raw.pick_types(eeg=True, exclude="bads")

    if len(raw.ch_names) > max_channels:
        raw.pick(raw.ch_names[:max_channels])

    raw.filter(l_freq=l_freq, h_freq=h_freq, verbose=False)
    raw.resample(128, npad="auto", verbose=False)

    sfreq = raw.info["sfreq"]
    data = raw.get_data()

    win = int(epoch_sec * sfreq)
    step = int(win * (1 - overlap))
    if step <= 0:
        raise ValueError("overlap too large, step<=0")

    X = []
    n_times = data.shape[1]
    for start in range(0, n_times - win + 1, step):
        seg = data[:, start:start + win]
        feat = epoch_to_features(seg, sfreq)
        X.append(feat)

    if not X:
        raise ValueError("No valid epochs extracted")

    return np.array(X, dtype=float)


def build_dataset_from_folder(folder: str, label: int):
    folder = Path(folder)
    edfs = sorted(folder.glob("*.edf"))
    if not edfs:
        raise FileNotFoundError(f"No EDF files found: {folder}")

    X_list, y_list = [], []
    for f in edfs:
        try:
            X = load_edf_extract_features(str(f))
            y = np.full((len(X),), label, dtype=int)
            X_list.append(X)
            y_list.append(y)
            print(f"[OK] {f.name}: epochs={len(X)}, feat_dim={X.shape[1]}")
        except Exception as e:
            print(f"[SKIP] {f.name}: {e}")

    if not X_list:
        raise RuntimeError("No usable EDF data")

    X_all = np.vstack(X_list)
    y_all = np.concatenate(y_list)
    return X_all, y_all
