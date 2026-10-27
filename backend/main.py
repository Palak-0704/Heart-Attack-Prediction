import warnings
from pathlib import Path

import joblib
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from preprocess import FEATURES, ROOT, Preprocessor

warnings.filterwarnings("ignore")
FRONTEND = ROOT / "frontend"

app = FastAPI(title="Heart Attack Risk Prediction API")
model = joblib.load(ROOT / "final_model_catboost.pkl")
pre = Preprocessor()


class Patient(BaseModel):
    age: int = Field(ge=1, le=120)
    sex: int = Field(ge=0, le=1)
    cp: int = Field(ge=0, le=3)
    trestbps: float = Field(ge=50, le=250)
    chol: float = Field(ge=80, le=700)
    fbs: int = Field(ge=0, le=1)
    restecg: int = Field(ge=0, le=2)
    thalach: float = Field(ge=40, le=250)
    exang: int = Field(ge=0, le=1)
    oldpeak: float = Field(ge=0, le=10)
    slope: int = Field(ge=0, le=2)
    ca: int = Field(ge=0, le=4)
    thal: int = Field(ge=0, le=3)


@app.get("/api/health")
def health():
    return {"status": "ok", "model": type(model).__name__}


@app.post("/api/predict")
def predict(p: Patient):
    x = pre.transform(p.model_dump())
    proba = float(model.predict_proba(x)[0][1])
    importances = dict(zip(FEATURES, map(float, model.feature_importances_)))
    top = sorted(importances.items(), key=lambda kv: -kv[1])[:5]
    return {
        "prediction": int(proba >= 0.5),
        "probability": proba,
        "label": "High risk of heart disease" if proba >= 0.5 else "Low risk of heart disease",
        "top_factors": [{"feature": k, "importance": v} for k, v in top],
    }


app.mount("/static", StaticFiles(directory=FRONTEND), name="static")


@app.get("/")
def index():
    return FileResponse(FRONTEND / "index.html")
