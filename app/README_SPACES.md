# Hugging Face Spaces Deployment

## Option A: Streamlit Space (recommended)
1. Create a new **Streamlit** Space on Hugging Face.
2. Upload these files/folders:
   - `app/hf_app.py` (rename to `app.py` in Space root)
   - `src/`
   - `outputs/model_rf_real.joblib` (or train and include)
   - `requirements.txt`
3. Ensure `requirements.txt` includes streamlit + scikit-learn + joblib.
4. Space will auto-build and expose a public URL.

## Option B: Git-based sync
- Push this repo to GitHub.
- In Space settings, link GitHub repository and set app file to `app/hf_app.py`.
