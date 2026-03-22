import streamlit as st
import numpy as np
from src.infer import predict_state

st.set_page_config(page_title="BCI MVP Online Demo", layout="wide")
st.title("🧠 BCI MVP — Online Demo")
st.caption("Public demo for relaxed vs focused inference (feature-input mode).")

st.markdown("""
**How to use:**
1. Keep 32 values or edit them.
2. Click **Predict**.
3. Inspect probability output.
""")

default = ",".join(["0.0"] * 32)
text = st.text_area("32-dim feature vector (comma-separated)", value=default, height=120)

if st.button("Predict"):
    try:
        vals = [float(x.strip()) for x in text.split(",") if x.strip()]
        if len(vals) != 32:
            st.error(f"Expected 32 values, got {len(vals)}")
        else:
            out = predict_state(vals)
            st.success(f"Prediction: {out['label']}")
            st.json(out)
            st.line_chart(np.array([out["relaxed_prob"], out["focused_prob"]]))
    except Exception as e:
        st.exception(e)
