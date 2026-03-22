# Mathematical Model (Full) — BCI MVP

This document provides a complete mathematical specification of the current BCI MVP pipeline.

## 1) Notation

| Symbol | Meaning |
|---|---|
| $x_c(t)$ | EEG time series of channel $c$ |
| $f_s$ | Sampling frequency |
| $w$ | Window length (samples) |
| $b=[f_1,f_2]$ | Frequency band interval |
| $P_c(f)$ | PSD (power spectral density) of channel $c$ |
| $\text{BP}_{c,b}$ | Bandpower of channel $c$ in band $b$ |
| $C$ | Number of channels |
| $\mathbf{z}\in\mathbb{R}^{4C}$ | Feature vector (delta/theta/alpha/beta per channel) |
| $y\in\{0,1\}$ | Label: 0 relaxed, 1 focused |
| $\hat{p}=P(y=1\mid\mathbf{z})$ | Predicted focused probability |
| $\hat{y}$ | Predicted label |
| $p_t$ | Raw focused probability at time step $t$ |
| $\tilde{p}_t$ | EMA-smoothed probability |
| $\alpha$ | EMA coefficient |
| $\tau_h,\tau_l$ | Hysteresis thresholds ($\tau_l<\tau_h$) |
| $\epsilon$ | Gaussian perturbation |
| $\mathbf{m}$ | Dropout mask |
| $M$ | Generic metric (Accuracy/F1/AUC etc.) |

---

## 2) Signal preprocessing

Given raw EEG channel $x_c(t)$, preprocessing applies:

1. Band-pass filtering in $[f_{low}, f_{high}]$ (default approx. $[1,40]$ Hz)
2. Resampling to unified $f_s$ (default 128 Hz)
3. Sliding-window epoching

Let epoch index be $k$, then epoch segment for channel $c$ is:

\[
\mathbf{x}_{c}^{(k)} = [x_c(t_k), x_c(t_k+1), \dots, x_c(t_k+w-1)]
\]

with overlap ratio $r$ and stride $s = w(1-r)$.

---

## 3) Bandpower feature extraction (Welch PSD)

For each epoch/channel, PSD is estimated via Welch:

\[
P_c^{(k)}(f) = \text{Welch}(\mathbf{x}_{c}^{(k)})
\]

For each canonical band $b=[f_1,f_2]$, bandpower is:

\[
\text{BP}_{c,b}^{(k)} = \int_{f_1}^{f_2} P_c^{(k)}(f)\,df
\]

Bands used:
- delta: $[1,4)$ Hz
- theta: $[4,8)$ Hz
- alpha: $[8,13)$ Hz
- beta: $[13,30)$ Hz

Feature vector per epoch:

\[
\mathbf{z}^{(k)} = [\text{BP}_{1,\delta}^{(k)},\text{BP}_{1,\theta}^{(k)},\text{BP}_{1,\alpha}^{(k)},\text{BP}_{1,\beta}^{(k)},\dots,\text{BP}_{C,\beta}^{(k)}]
\in \mathbb{R}^{4C}
\]

---

## 4) Classification model

The model learns mapping:

\[
f_\theta: \mathbf{z} \mapsto \hat{p}=P(y=1\mid\mathbf{z})
\]

Binary decision rule:

\[
\hat{y}=\mathbb{1}[\hat{p}\ge 0.5]
\]

In codebase, $f_\theta$ is instantiated by classical ML baselines (RF/SVM/MLP).

---

## 5) Streaming stability model (EMA + Hysteresis)

To stabilize real-time predictions:

### 5.1 Exponential moving average
\[
\tilde{p}_t = \alpha p_t + (1-\alpha)\tilde{p}_{t-1},\quad \alpha\in(0,1]
\]

### 5.2 Hysteresis state machine
Let state $s_t\in\{\text{relaxed},\text{focused}\}$:

- If $s_{t-1}=\text{relaxed}$ and $\tilde{p}_t\ge\tau_h$, then $s_t=\text{focused}$
- If $s_{t-1}=\text{focused}$ and $\tilde{p}_t\le\tau_l$, then $s_t=\text{relaxed}$
- Else $s_t=s_{t-1}$

This reduces flicker around threshold boundaries.

---

## 6) Calibration model

Probability calibration quality is measured by Brier score:

\[
\text{Brier} = \frac{1}{N}\sum_{i=1}^{N}(\hat{p}_i-y_i)^2
\]

Lower is better.

Reliability curve uses bin-wise comparison of predicted confidence vs observed positive frequency.

---

## 7) Robustness perturbation model

To simulate noisy deployment conditions, perturb features as:

\[
\mathbf{z}' = (\mathbf{z}+\epsilon)\odot\mathbf{m}
\]

where:
- $\epsilon\sim\mathcal{N}(0,\sigma^2 I)$ (Gaussian noise)
- $\mathbf{m}\in\{0,1\}^d$ with Bernoulli dropout rate $r$

Metrics are evaluated on perturbed inputs $\mathbf{z}'$.

---

## 8) Ablation model

Band-level ablation zeros one band group at a time:

\[
\mathbf{z}_{\setminus b} = \mathcal{A}_b(\mathbf{z})
\]

where operator $\mathcal{A}_b$ sets all coordinates corresponding to band $b$ to zero.

Importance proxy:

\[
\Delta M_b = M(\mathbf{z}) - M(\mathbf{z}_{\setminus b})
\]

Larger $\Delta M_b$ implies stronger contribution of band $b$.

---

## 9) Bootstrap uncertainty model

For metric $M$, bootstrap resampling yields:

\[
\{M^{(1)},M^{(2)},\dots,M^{(B)}\}
\]

95% CI:

\[
\text{CI}_{95\%}(M)=\left[Q_{0.025}(M^{(b)}),\ Q_{0.975}(M^{(b)})\right]
\]

---

## 10) Cross-dataset generalization objective

Given dataset $D_A$ for training and $D_B$ for testing, we evaluate:

\[
\mathcal{G}(A\to B)=M\big(f_{\theta_A}, D_B\big)
\]

where $\theta_A$ is learned only from $D_A$. The cross-dataset matrix reports $\mathcal{G}(i\to j)$ for all dataset pairs.

---

## 11) Assumptions

1. Local short-window quasi-stationarity for PSD validity.
2. Bandpower features are sufficient for MVP-level discrimination.
3. Binary state framing (relaxed vs focused) is meaningful for current tasks.
4. Synthetic perturbations approximate, but do not fully represent, real physiological artifacts.
5. Bootstrap CI approximates metric uncertainty under finite held-out samples.

---

## 12) Complexity (high-level)

- Feature extraction: approximately linear in (#epochs × #channels × PSD cost)
- Inference: low-latency for tabular baselines
- Streaming stabilization: $O(1)$ per time step

This formulation is designed for practical prototyping and can be extended to deep end-to-end models (e.g., EEGNet) in future versions.


## 13) Formula-to-Code Mapping

| Math Component | Code Location |
|---|---|
| Welch PSD + bandpower $	ext{BP}_{c,b}$ | `src/preprocess.py` (`bandpower_1d`, `epoch_to_features`) |
| Feature vector $\mathbf{z}\in\mathbb{R}^{4C}$ | `src/preprocess.py` (`epoch_to_features`) |
| Binary classifier $\hat{p}=P(y=1\mid\mathbf{z})$ | `src/train.py`, `src/infer.py` |
| EMA update $	ilde{p}_t$ | `src/streaming.py` (`StreamingStateFilter.update`) |
| Hysteresis state machine | `src/streaming.py` (`StreamingStateFilter.update`) |
| Brier score calibration | `src/calibration_eval.py` |
| Robustness perturbation $\mathbf{z}'=(\mathbf{z}+\epsilon)\odot\mathbf{m}$ | `src/robustness_eval.py` |
| Band ablation $\Delta M_b$ | `src/ablation_eval.py` |
| Bootstrap CI quantiles | `src/bootstrap_ci.py` |
| Cross-dataset objective $\mathcal{G}(A	o B)$ | `src/cross_dataset_eval.py`, `src/cross_dataset_matrix.py` |
