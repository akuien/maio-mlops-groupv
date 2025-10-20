import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from app.models import DiabetesFeatures
from app.version import _version_


# Load the model artifact at startup
MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/model.joblib")
model = None

app = FastAPI(
    title="Diabetes Progression Prediction API",
    description="Predicts a quantitative measure of diabetes disease progression.",
    version=_version_,
)

@app.on_event("startup")
def load_model():
    """Load the model from disk when the application starts."""
    global model
    try:
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded successfully from {MODEL_PATH}")
    except FileNotFoundError:
        print(f"Error: Model file not found at {MODEL_PATH}")
        model = None # Ensure model is None if loading fails

@app.get("/health")
def health_check():
    """Health check endpoint to ensure service is running."""
    model_version = os.getenv("MODEL_VERSION", "v0.0.0-dev")
    return {"status": "ok", "model_version": model_version}

@app.post("/predict")
def predict_progression(features: DiabetesFeatures):
    """Predicts disease progression from input features."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Service is unavailable.")
    
    try:
        # Convert Pydantic model to a pandas DataFrame
        feature_df = pd.DataFrame([features.dict()])
        
        # Ensure column order matches training
        feature_df = feature_df[model.feature_names_in_]
        
        # Get prediction
        prediction = model.predict(feature_df)
        
        return {"prediction": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")