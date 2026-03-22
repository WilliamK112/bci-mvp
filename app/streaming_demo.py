import time
import numpy as np
import streamlit as st
from src.infer import predict_state
from src.streaming import StreamingStateFilter, StreamingConfig

st.set_page_config(page_title="BCI Streaming Demo", layout="wide")
st.title("🧠 BCI Streaming Demo (Smoothed)")
st.caption("Rolling predictions with EMA + hysteresis for stable state output.")

alpha = st.slider("EMA alpha", 0.05, 0.80, 0.25, 0.05)
high = st.slider("Focused switch threshold", 0.50, 0.90, 0.60, 0.01)
low = st.slider("Relaxed switch threshold", 0.10, 0.50, 0.40, 0.01)

if low >= high:
    st.error("low threshold must be smaller than high threshold")
    st.stop()

run = st.toggle("Start streaming", value=False)
placeholder = st.empty()
chart_placeholder = st.empty()
state_placeholder = st.empty()

if "hist_raw" not in st.session_state:
    st.session_state.hist_raw = []
if "hist_smooth" not in st.session_state:
    st.session_state.hist_smooth = []

filt = StreamingStateFilter(StreamingConfig(alpha=alpha, high_threshold=high, low_threshold=low))

if run:
    for _ in range(120):
        x = np.random.normal(0.2, 1.0, size=(32,))
        out = predict_state(x.tolist())
        s = filt.update(out["focused_prob"])

        st.session_state.hist_raw.append(s["raw_focused_prob"])
        st.session_state.hist_smooth.append(s["smoothed_focused_prob"])
        st.session_state.hist_raw = st.session_state.hist_raw[-200:]
        st.session_state.hist_smooth = st.session_state.hist_smooth[-200:]

        placeholder.metric("Focused Prob (Smoothed)", f"{s['smoothed_focused_prob']:.3f}")
        state_placeholder.info(f"Current Stable State: **{s['state']}**")
        chart_placeholder.line_chart({
            "raw": st.session_state.hist_raw,
            "smoothed": st.session_state.hist_smooth,
        })
        time.sleep(0.15)
