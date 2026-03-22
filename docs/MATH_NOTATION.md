# Mathematical Notation & Assumptions

## Notation

| Symbol | Meaning |
|---|---|
| $x_c(t)$ | EEG time-series of channel $c$ |
| $P_c(f)$ | Power spectral density (PSD) of channel $c$ |
| $\text{BP}_{c,b}$ | Bandpower of channel $c$ in band $b$ |
| $\mathbf{z}$ | Feature vector concatenating all channel-band powers |
| $y$ | Ground-truth label ($0$ relaxed, $1$ focused) |
| $\hat{p}$ | Predicted probability $P(y=1\mid\mathbf{z})$ |
| $\hat{y}$ | Predicted class label |
| $p_t$ | Raw focused probability at time step $t$ |
| $\tilde{p}_t$ | Smoothed probability (EMA) |
| $\alpha$ | EMA smoothing coefficient |
| $\tau_h,\tau_l$ | High/low hysteresis thresholds with $\tau_l<\tau_h$ |
| $\epsilon$ | Additive Gaussian noise term |
| $\mathbf{m}$ | Dropout mask in robustness perturbation |
| $M$ | Generic evaluation metric (Accuracy/F1/AUC) |

## Core Assumptions

1. **Stationarity in short windows**: within each epoch window, EEG statistics are approximately stable enough for PSD estimation.
2. **Bandpower sufficiency for MVP**: handcrafted bandpower features provide a practical baseline representation.
3. **Binary task framing**: current classifier assumes two states (relaxed vs focused).
4. **Independent bootstrap samples**: CI estimates use empirical resampling approximations on held-out predictions.
5. **Perturbation realism (approx.)**: Gaussian noise + feature dropout are used as proxy stress tests, not full physiological simulation.

## Computational Complexity (high-level)

- **Feature extraction**: approximately linear in number of windows/channels and FFT cost per window.
- **Inference**: lightweight (tree/MLP forward pass over $d=4C$ features), suitable for near real-time usage.
- **Streaming filter**: $O(1)$ per time step for EMA + hysteresis update.

