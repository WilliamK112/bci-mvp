import time
import numpy as np
import streamlit as st
from src.infer import predict_state

st.set_page_config(page_title="BCI Streaming Demo", layout="wide")
st.title("🧠 BCI Streaming Demo (Simulated)")
st.caption("Simulates rolling-window EEG features and live state probability.")

run = st.toggle("Start streaming", value=False)
placeholder = st.empty()
chart_placeholder = st.empty()

if "hist" not in st.session_state:
    st.session_state.hist = []

if run:
    for _ in range(80):
        # Simulated 32-dim feature vector (replace with real stream later)
        x = np.random.normal(0.2, 1.0, size=(32,))
        out = predict_state(x.tolist())
        st.session_state.hist.append(out["focused_prob"])
        st.session_state.hist = st.session_state.hist[-120:]

        placeholder.metric("Focused Probability", f"{out['focused_prob']:.3f}")
        chart_placeholder.line_chart(st.session_state.hist)
        time.sleep(0.2)
