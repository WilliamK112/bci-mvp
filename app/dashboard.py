import streamlit as st
from src.infer import predict_state

st.set_page_config(page_title="BCI MVP", layout="wide")
st.title("🧠 BCI MVP Dashboard")
st.caption("输入特征向量，预测 relaxed/focused")

default = ",".join(["0.0"] * 32)
text = st.text_area("32维特征，逗号分隔", value=default, height=120)

if st.button("Run"):
    vals = [float(x.strip()) for x in text.split(",") if x.strip()]
    if len(vals) != 32:
        st.error(f"需要32维，当前{len(vals)}维")
    else:
        out = predict_state(vals)
        st.json(out)
