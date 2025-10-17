import joblib
import pandas as pd

print("LOADING MODEL")
model = joblib.load('artifacts/model.joblib')


def predict(data):
    if isinstance(data, dict):
        data = [data]

    data = pd.DataFrame(data)
    
    return model.predict(data)
