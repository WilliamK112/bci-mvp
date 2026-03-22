"""
Hugging Face Spaces entrypoint (Streamlit).
Keeps deployment simple by using root-level app.py.
"""
import streamlit as st
import numpy as np
from src.infer import predict_state
from src.model_fallback import has_real_model
from src.streaming import StreamingStateFilter, StreamingConfig

st.set_page_config(page_title="BCI MVP Space", layout="wide")
st.title("🧠 BCI MVP — Public Space Demo")
st.caption("Low-hardware EEG BCI prototype: feature inference + streaming stability.")

st.info("If trained model is unavailable in Space, app uses stable mock-fallback predictions so demo remains interactive.")

model_mode = "REAL_MODEL" if has_real_model("outputs/model_rf_real.joblib") else "MOCK_FALLBACK"
st.markdown(f"**Demo Runtime Mode:** `{model_mode}`")

mode = st.radio("Mode", ["Single Prediction", "Streaming (Simulated)"], horizontal=True)

if mode == "Single Prediction":
    txt = st.text_area("32-dim feature vector", value=",".join(["0.0"] * 32), height=120)
    if st.button("Predict"):
        vals = [float(x.strip()) for x in txt.split(",") if x.strip()]
        if len(vals) != 32:
            st.error(f"Need 32 values, got {len(vals)}")
        else:
            out = predict_state(vals)
            st.success(f"Prediction: {out['label']}")
            st.json(out)
else:
    alpha = st.slider("EMA alpha", 0.05, 0.80, 0.25, 0.05)
    high = st.slider("High threshold", 0.50, 0.90, 0.60, 0.01)
    low = st.slider("Low threshold", 0.10, 0.50, 0.40, 0.01)
    if low >= high:
        st.error("low must be smaller than high")
        st.stop()

    filt = StreamingStateFilter(StreamingConfig(alpha=alpha, high_threshold=high, low_threshold=low))
    run = st.toggle("Start", value=False)
    met = st.empty(); info = st.empty(); ch = st.empty()
    if "raw" not in st.session_state:
        st.session_state.raw = []
    if "smooth" not in st.session_state:
        st.session_state.smooth = []

    if run:
        for _ in range(120):
            x = np.random.normal(0.2, 1.0, size=(32,))
            out = predict_state(x.tolist())
            s = filt.update(out["focused_prob"])
            st.session_state.raw.append(s["raw_focused_prob"])
            st.session_state.smooth.append(s["smoothed_focused_prob"])
            st.session_state.raw = st.session_state.raw[-160:]
            st.session_state.smooth = st.session_state.smooth[-160:]

            met.metric("Smoothed Focused Prob", f"{s['smoothed_focused_prob']:.3f}")
            info.info(f"Stable state: **{s['state']}**")
            ch.line_chart({"raw": st.session_state.raw, "smoothed": st.session_state.smooth})
