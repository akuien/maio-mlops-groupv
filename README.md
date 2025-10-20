# Assigment 3 – MLOps

## Virtual Diabetes Clinic Triage

### Description
The project is based on developing a small machine learning (ML) service that can predict how a disease will change in the short term and provide a continuous risk score. The risk score allows users to quickly and easily prioritize follow-ups. In other words, this model makes it easier for users to determine which patients need to be given priority.

---

### Project main objectives
1. Develop a machine learning model that estimates risks and automatically assesses short-term disease progression.
2. Create an API service that allows users to request risk predictions for patient data.
3. The system will be implemented in a pipeline through Github Actions to automate testing, development, and launch of the service

---

### 📁 Project Structure 
```
│
├── .github/workflows/             # Pipelines
│  ├─ ci.yaml
│  └── release.yml
│
├── app/                           # API application
│  ├─ __init__.py
│  ├─ main.py
│  ├─ models.py
│  ├─ patients.py
│  └── version.py
│
├── scripts/                       # Training model
│  └── train.py
│
├── tests/                         # Test package
│  ├─ conftest.py
│  └── test_api.py
│
├── .dockerignore                  # Docker build ignore list
├── .gitignore                     # Git ignore list
├── Dockerfile                     # Docker image definition
├── smoke-test.sh                  # Check the app or built container
├── requirements.txt               # Python dependencies
├── CHANGELOG.md
└── README.md
```

### Installation
#### Prerequisites
-	Python 3.10 or above is installed
-	Git is installed
-	Docker is installed

#### Steps for reproducibility 
1. Clone the repository:
  ```bash
  https://github.com/akuien/maio-mlops-groupv.git
  cd maio-mlops-groupv/
  ```

2. Create python virtual environment
``` bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
```

3. Install required dependencies:
  ```bash
  pip install -r requirements.txt
  ```

4. Training the ML model:
  ```bash
  python scripts/train.py 
  ```

5. Run API locally:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```

6. Build the image:
  ```bash
  docker build -t virtual-triage:latest . 
  ```

7. Run the container:
  ```bash
  docker run -p 8000:8000 virtual-triage  
  ```

8. View Triage Dashboard
   ```
   follow the link: http://0.0.0.0:8000/
   ```
 <img width="1005" height="464" alt="image" src="https://github.com/user-attachments/assets/d4c7b426-0cc0-409b-9b74-79a0bd90e61a" />
  

9. Test /health endpoint
  ```
curl -s http://localhost:8000/health
```
output: ``` {"status":"ok","model_version":"0.1.0"} ```
   
10. Test /predict endpoint 
```
  curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'

   ```
output: ``` {"prediction":210.03174809971358} ```

output incase of wrong input: ``` {"detail":"Method Not Allowed"} ```

