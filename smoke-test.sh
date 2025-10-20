#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the base URL of the API
BASE_URL="http://localhost:8000"

echo "--- Running Smoke Test ---"

# --- Test 1: Check the /health endpoint ---
echo "Testing /health endpoint..."
# Use curl to get the health status and grep to check for the "ok" status
if curl -s "${BASE_URL}/health" | grep -q '"status":"ok"'; then
  echo "/health endpoint is OK."
else
  echo "/health endpoint failed."
  exit 1
fi

# --- Test 2: Check the /predict endpoint ---
echo "Testing /predict endpoint..."
# Use curl to send a sample payload and check for the "prediction" key in the response
if curl -s -X POST "${BASE_URL}/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "age": 0.02, "sex": -0.044, "bmi": 0.06, "bp": -0.03, "s1": -0.02,
       "s2": 0.03, "s3": -0.02, "s4": 0.02, "s5": 0.02, "s6": -0.001
     }' | grep -q '"prediction"'; then
  echo "/predict endpoint is OK."
else
  echo "/predict endpoint failed."
  exit 1
fi

echo "--- Smoke Test Passed ---"
exit 0