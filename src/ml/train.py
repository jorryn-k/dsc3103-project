
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


DATA_PATH = Path("data/processed/prices_with_rainfall.parquet")
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "model.joblib"
METADATA_PATH = MODEL_DIR / "model_metadata.json"

FEATURES = ["market", "commodity", "rainfall_mm"]
TARGET = "price"


def main():
    print("Loading dataset...")
    df = pd.read_parquet(DATA_PATH)

    print("Dataset shape:", df.shape)
    print("Columns:", df.columns.tolist())

    required = FEATURES + [TARGET]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[required].copy()

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["rainfall_mm"] = pd.to_numeric(
        df["rainfall_mm"], errors="coerce"
    )

    df = df.dropna(subset=["price", "market", "commodity"])

    if len(df) < 10:
        raise ValueError("Not enough valid rows to train a model.")

    X = df[FEATURES]
    y = df[TARGET]

    categorical_features = ["market", "commodity"]
    numeric_features = ["rainfall_mm"]

    preprocessing = ColumnTransformer(
        transformers=[
            (
                "categorical",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OneHotEncoder(handle_unknown="ignore"))
                ]),
                categorical_features
            ),
            (
                "numeric",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="median"))
                ]),
                numeric_features
            )
        ]
    )

    model = Pipeline([
        ("preprocessing", preprocessing),
        ("regression", LinearRegression())
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    print("Training model...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5

    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    metadata = {
        "model_type": "LinearRegression",
        "features": FEATURES,
        "target": TARGET,
        "training_rows": len(X_train),
        "testing_rows": len(X_test),
        "mae": round(float(mae), 2),
        "rmse": round(float(rmse), 2),
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "sklearn_version": __import__("sklearn").__version__,
        "preprocessing": "OneHotEncoder for categories; median imputation for rainfall",
    }

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    print("\nTraining completed successfully!")
    print("Model saved to:", MODEL_PATH)
    print("Metadata saved to:", METADATA_PATH)


if __name__ == "__main__":
    main()

