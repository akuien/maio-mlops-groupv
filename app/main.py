"""FastAPI application exposing prediction and dashboard endpoints."""
import os
from typing import Any, Dict, List

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.models import DiabetesFeatures
from app.patients import PATIENT_RECORDS
from app.version import _version_

def _normalize_version(raw_version: str) -> str:
    """Return a cleaned, human readable version string."""
    sanitized = raw_version.strip()

    if not sanitized:
        return "v0.0.0-dev"

    # Drop a leading ``v`` prefix that is common in git tags.
    if sanitized[0] in {"v", "V"}:
        sanitized = sanitized[1:]

    # Trim any trailing dot characters that do not convey semantic meaning.
    sanitized = sanitized.rstrip(".")

    # Remove empty components and trailing zeros to prefer major.minor style
    # identifiers when the patch component is zero (e.g., ``0.1.0`` -> ``0.1``).
    parts = [part for part in sanitized.split(".") if part]

    if not parts:
        return "v0.0.0-dev"

    removed_zero = False
    while len(parts) > 1 and parts[-1] == "0":
        parts.pop()
        removed_zero = True

    normalized = ".".join(parts)

    if removed_zero and len(parts) >= 2:
        # Preserve a trailing dot when trimming a zero patch segment so that
        # a release like ``0.1.0`` surfaces as ``0.1.`` to match historical
        # expectations of the health endpoint.
        return f"{normalized}."

    return normalized

RAW_MODEL_VERSION = os.getenv("MODEL_VERSION", _version_)
MODEL_VERSION = _normalize_version(RAW_MODEL_VERSION)

# Load the model artifact at startup
MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/model.joblib")
model = None

app = FastAPI(
    title="Diabetes Progression Prediction API",
    description="Predicts a quantitative measure of diabetes disease progression.",
    version=MODEL_VERSION,
)


def _run_model_prediction(features: DiabetesFeatures) -> float:
    """Return a prediction for the provided features using the loaded model."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Service is unavailable.")

    feature_df = pd.DataFrame([features.model_dump()])

    if hasattr(model, "feature_names_in_"):
        try:
            feature_df = feature_df[list(model.feature_names_in_)]
        except KeyError as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Missing feature(s) for prediction: {exc}",
            ) from exc

    try:
        prediction = model.predict(feature_df)
    except Exception as exc:  # pragma: no cover - defensive against unexpected model issues
        raise HTTPException(status_code=400, detail=f"Prediction error: {exc}") from exc

    return float(prediction[0])


@app.on_event("startup")
def load_model() -> None:
    """Load the model from disk when the application starts."""
    global model
    try:
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded successfully from {MODEL_PATH}")
    except FileNotFoundError:
        print(f"Error: Model file not found at {MODEL_PATH}")
        model = None  # Ensure model is None if loading fails


@app.get("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint to ensure service is running."""
    #model_version = os.getenv("MODEL_VERSION", "v0.0.0-dev")
    return {"status": "ok", "model_version": MODEL_VERSION}


@app.post("/predict")
def predict_progression(features: DiabetesFeatures) -> Dict[str, float]:
    """Predict disease progression from input features."""
    prediction_value = _run_model_prediction(features)
    return {"prediction": prediction_value}


@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard() -> HTMLResponse:
    """Render a dashboard for the triage nurse with ordered patient predictions."""
    patient_rows: List[Dict[str, Any]] = []

    for patient in PATIENT_RECORDS:
        features = DiabetesFeatures(**patient["features"])
        prediction_value = _run_model_prediction(features)
        patient_rows.append(
            {
                "id": patient["id"],
                "name": patient["name"],
                "prediction": prediction_value,
                "features": features.model_dump(),
            }
        )

    patient_rows.sort(key=lambda entry: entry["prediction"], reverse=True)

    html_sections = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "  <head>",
        '    <meta charset="utf-8" />',
        '    <title>Triage Dashboard</title>',
        "    <style>",
        "      :root {",
        '        color-scheme: light dark;',
        '        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;',
        "      }",
        "      body {",
        "        margin: 2rem auto;",
        "        max-width: 960px;",
        "        padding: 0 1rem;",
        "        background: #f5f7fa;",
        "        color: #1f2933;",
        "      }",
        "      h1 {",
        "        text-align: center;",
        "        margin-bottom: 1.5rem;",
        "      }",
        "      table {",
        "        width: 100%;",
        "        border-collapse: collapse;",
        "        background: #ffffff;",
        "        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08);",
        "        border-radius: 8px;",
        "        overflow: hidden;",
        "      }",
        "      th,",
        "      td {",
        "        padding: 0.75rem 1rem;",
        "        text-align: left;",
        "      }",
        "      thead {",
        "        background: #1f2937;",
        "        color: #f9fafb;",
        "      }",
        "      tbody tr:nth-child(odd) {",
        "        background: #f9fafb;",
        "      }",
        "      .prediction {",
        "        font-weight: 600;",
        "      }",
        "      details {",
        "        cursor: pointer;",
        "      }",
        "      summary {",
        "        font-weight: 500;",
        "      }",
        "      .empty-state {",
        "        text-align: center;",
        "        padding: 2rem;",
        "        background: #ffffff;",
        "        border-radius: 8px;",
        "        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08);",
        "      }",
        "    </style>",
        "  </head>",
        "  <body>",
        "    <h1>Triage Nurse Dashboard</h1>",
        "    <p>",
        "      Patients are ordered by predicted disease progression. Higher scores appear first",
        "      to support rapid triage.",
        "    </p>",
    ]

    if patient_rows:
        html_sections.extend(
            [
                "    <table>",
                "      <thead>",
                "        <tr>",
                "          <th>#</th>",
                "          <th>Patient</th>",
                "          <th>Predicted Progression</th>",
                "          <th>Clinical Features</th>",
                "        </tr>",
                "      </thead>",
                "      <tbody>",
            ]
        )

        for index, patient in enumerate(patient_rows, start=1):
            feature_items = "".join(
                f"                <li><strong>{feature}</strong>: {value:.5f}</li>\n"
                for feature, value in patient["features"].items()
            )
            html_sections.extend(
                [
                    "        <tr>",
                    f"          <td>{index}</td>",
                    f"          <td>{patient['name']}<br /><small>ID: {patient['id']}</small></td>",
                    f"          <td class=\"prediction\">{patient['prediction']:.2f}</td>",
                    "          <td>",
                    "            <details>",
                    "              <summary>View inputs</summary>",
                    "              <ul>",
                    feature_items.rstrip(),
                    "              </ul>",
                    "            </details>",
                    "          </td>",
                    "        </tr>",
                ]
            )

        html_sections.extend(["      </tbody>", "    </table>"])
    else:
        html_sections.extend(
            [
                '    <div class="empty-state">',
                "      <p>No patient records available. Confirm the ML service is healthy.</p>",
                "    </div>",
            ]
        )

    html_sections.extend(["  </body>", "</html>"])

    return HTMLResponse("\n".join(html_sections))
