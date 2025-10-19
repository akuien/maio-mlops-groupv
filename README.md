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
├── src/                                # Optional support scripts
│
├── .dockerignore                    # Docker build ignore list
├── .gitignore                       # Git ignore list
├── Dockerfile                       # Docker image definition
├── app.py                           # API application
├── docker-compose.yaml              # Build and run the container
├── pythonscript.py                  # Training model
├── requirements.txt                 # Python dependencies
└── README.md
```

### Installation
#### Prerequisites
-	Python 3.10 or above is installed
-	Git is installed
-	Docker is installed

#### Steps
1. Clone the repository:
  ```bash
  git clone https://github.com/Akuien/maio-mlops.git
  cd maio-mlops
  ```

2. Install required dependencies:
  ```bash
  pip install -r requirements.txt
  ```

3. Training the ML model:
  ```bash
  python pythonscript.py
  ```

4. Run API locally:
  ```bash
  python app.py
  ```

5. Build the image:
  ```bash
  docker build -t maio-mlops:v0.1 .
  ```

6. Run the container:
  ```bash
  docker-compose up --build
  ```
