import pandas as pd
from sklearn.ensemble import IsolationForest
from src.config import ANOMALY_REPORT_PATH, OUTPUT_DIR
import os

# Model parameters (for experiment tracking)
ISOLATION_FOREST_PARAMS = {
    'n_estimators': 100,
    'contamination': 'auto',
    'random_state': 42
}

def detect_anomalies(df, logger):
    """Detects anomalies in payment values using Isolation Forest."""
    logger.info("Starting anomaly detection with Isolation Forest.")

    model = IsolationForest(**ISOLATION_FOREST_PARAMS)

    # The model expects a 2D array, so we use .values.reshape(-1, 1)
    predictions = model.fit_predict(df[['amount']])

    # -1 indicates an anomaly
    anomalies_df = df[predictions == -1]

    logger.info(f"Found {len(anomalies_df)} payment anomalies.")

    # Saves the anomaly report
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(ANOMALY_REPORT_PATH, 'w') as f:
        f.write("Anomaly Report Detected by Machine Learning (Isolation Forest):\n")
        f.write("="*70 + "\n")
        f.write(anomalies_df.to_string())
    logger.info(f"ML anomaly report saved to: {ANOMALY_REPORT_PATH}")

    return anomalies_df
