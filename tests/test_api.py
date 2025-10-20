import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.patients import PATIENT_RECORDS


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "model_version": app.version}


def test_predict_endpoint_success(client: TestClient):
    valid_payload = {
        "age": 0.038,
        "sex": 0.05,
        "bmi": 0.061,
        "bp": 0.021,
        "s1": -0.044,
        "s2": -0.034,
        "s3": -0.043,
        "s4": -0.002,
        "s5": 0.019,
        "s6": -0.017,
    }

    response = client.post("/predict", json=valid_payload)

    assert response.status_code == 200

    response_data = response.json()
    assert "prediction" in response_data
    assert isinstance(response_data["prediction"], float)


def test_predict_endpoint_invalid_payload(client: TestClient):
    invalid_payload = {
        "sex": 0.05,
        "bmi": 0.061,
        "bp": 0.021,
        "s1": -0.044,
        "s2": -0.034,
        "s3": -0.043,
        "s4": -0.002,
        "s5": 0.019,
        "s6": -0.017,
    }

    response = client.post("/predict", json=invalid_payload)

    assert response.status_code == 422


def test_dashboard_orders_patients_by_prediction(client: TestClient):
    response = client.get("/dashboard")
    assert response.status_code == 200

    body = response.text

    predictions = []
    for patient in PATIENT_RECORDS:
        prediction_response = client.post("/predict", json=patient["features"])
        assert prediction_response.status_code == 200
        prediction_value = prediction_response.json()["prediction"]
        predictions.append((patient["name"], prediction_value))

    predictions.sort(key=lambda item: item[1], reverse=True)

    last_position = -1
    for name, _ in predictions:
        position = body.find(name)
        assert position != -1
        assert position > last_position
        last_position = position
