#import pytest
from fastapi.testclient import TestClient

# Adjust the import path based on your project structure.
# This assumes your FastAPI app instance is named 'app' in 'app/main.py'

#try:
#    from app.main import app
#except ModuleNotFoundError:
    # Handle cases where the app might be in a different location
    # This can happen in different testing setups.
    # For this project, the above 'try' block should work.
#    from ..app.main import app 

#from app.main import app

from app.main import app

# Create a TestClient instance for your application
client = TestClient(app)

def test_health_check():
    """
    Tests the /health endpoint to ensure it's running and returns the correct status.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "model_version": app.version}

def test_predict_endpoint_success():
    """
    Tests the /predict endpoint with a valid payload to ensure it returns a successful prediction.
    """
    # Define a valid sample payload that matches your Pydantic model
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
        "s6": -0.017
    }

    response = client.post("/predict", json=valid_payload)
    
    # Assert that the request was successful
    assert response.status_code == 200
    
    # Assert that the response body contains the "prediction" key
    response_data = response.json()
    assert "prediction" in response_data
    
    # Assert that the prediction value is a float
    assert isinstance(response_data["prediction"], float)

def test_predict_endpoint_invalid_payload():
    """
    Tests the /predict endpoint with an invalid payload to ensure it handles errors correctly.
    FastAPI and Pydantic should automatically return a 422 Unprocessable Entity status.
    """
    # This payload is missing the 'age' field
    invalid_payload = {
        "sex": 0.05,
        "bmi": 0.061,
        "bp": 0.021,
        "s1": -0.044,
        "s2": -0.034,
        "s3": -0.043,
        "s4": -0.002,
        "s5": 0.019,
        "s6": -0.017
    }

    response = client.post("/predict", json=invalid_payload)
    
    # Assert that the application correctly identifies the invalid data
    assert response.status_code == 422