from fastapi import FastAPI
from pydantic import BaseModel, conlist
from src.infer import predict_state

app = FastAPI(title="BCI MVP API", version="1.0.0")


class PredictRequest(BaseModel):
    features: conlist(float, min_length=32, max_length=32)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/predict")
def predict(req: PredictRequest):
    return predict_state(req.features)
