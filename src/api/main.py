
import json
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


MODEL_PATH = Path("models/model.joblib")
METADATA_PATH = Path("models/model_metadata.json")

model = None
metadata = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, metadata

    if not MODEL_PATH.exists():
        raise RuntimeError("Trained model file not found.")

    if not METADATA_PATH.exists():
        raise RuntimeError("Model metadata file not found.")

    model = joblib.load(MODEL_PATH)

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print("Model loaded successfully.")

    yield


app = FastAPI(
    title="Market Price Prediction API",
    description="Predicts market prices using a trained ML model.",
    version="1.0.0",
    lifespan=lifespan,
)


class PriceRequest(BaseModel):
    market: str = Field(min_length=1)
    commodity: str = Field(min_length=1)
    rainfall_mm: float = Field(ge=0, le=500)
    date: date


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "model_type": metadata["model_type"],
        "features": metadata["features"],
        "trained_at": metadata["trained_at"],
        "mae": metadata["mae"],
        "rmse": metadata["rmse"],
    }


@app.post("/predict")
def predict(request: PriceRequest):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not available."
        )

    input_data = pd.DataFrame([{
        "market": request.market,
        "commodity": request.commodity,
        "rainfall_mm": request.rainfall_mm,
    }])

    try:
        predicted_price = float(model.predict(input_data)[0])
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed."
        ) from exc

    return {
        "market": request.market,
        "commodity": request.commodity,
        "date": request.date.isoformat(),
        "rainfall_mm": request.rainfall_mm,
        "predicted_price": round(predicted_price, 2),
        "model_type": metadata["model_type"],
    }

