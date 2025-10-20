import argparse
import json
import os
import joblib
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from numpy import sqrt



# Create artifacts directory if it doesn't exist
os.makedirs("artifacts", exist_ok=True)

def train(model_name: str = "linear_regression", random_seed: int = 42):
    """Trains a model and saves it along with metrics."""
    print(f"Starting training for model: {model_name}")

    # Load data
    X, y = load_diabetes(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_seed
    )

    # Define model, v0.2 should automatically go to ridge
    if model_name == "ridge":
        model = Ridge(alpha=0.1, random_state=random_seed)
    else:
        model = LinearRegression()

    # Create a preprocessing and training pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', model)
    ])

    # Train the model
    pipeline.fit(X_train, y_train)
    print("Model training complete.")

    # Evaluate the model
    y_pred = pipeline.predict(X_test)
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    print(f"Evaluation complete. RMSE: {rmse:.4f}")

    # Save model artifact
    model_path = "artifacts/model.joblib"
    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")

    # Save metrics
    metrics = {"rmse": rmse}
    metrics_path = "artifacts/metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"Metrics saved to {metrics_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model-name", type=str, default="linear_regression",
        help="Model to train (linear_regression or ridge)"
    )
    parser.add_argument(
        "--random-seed", type=int, default=42, help="Random seed for reproducibility"
    )
    args = parser.parse_args()
    train(model_name=args.model_name, random_seed=args.random_seed)