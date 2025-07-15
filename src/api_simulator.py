import json
import os
import pandas as pd
from src.config import API_OUTPUT_PATH, OUTPUT_DIR

def simulate_rest_api(data_summary, duplicates_df, anomalies_df, llm_interpretation, logger):
    """Simulates a REST API that exposes the analysis results in a JSON file."""
    logger.info("Simulating REST API for results exposure.")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Ensures that date/period columns are serialisable
    duplicates_df_copy = duplicates_df.copy()
    for col in duplicates_df_copy.select_dtypes(include=['datetime64']).columns:
        duplicates_df_copy[col] = duplicates_df_copy[col].astype(str)
    if 'payment_month' in duplicates_df_copy.columns:
        duplicates_df_copy['payment_month'] = duplicates_df_copy['payment_month'].astype(str)

    anomalies_df_copy = anomalies_df.copy()
    for col in anomalies_df_copy.select_dtypes(include=['datetime64']).columns:
        anomalies_df_copy[col] = anomalies_df_copy[col].astype(str)
    if 'payment_month' in anomalies_df_copy.columns:
        anomalies_df_copy['payment_month'] = anomalies_df_copy['payment_month'].astype(str)

    # Ensures that statistics are serialisable
    serializable_stats = {k: str(v) for k, v in data_summary.to_dict().items()}

    api_response = {
        "status": "success",
        "timestamp": pd.Timestamp.now().isoformat(),
        "summary_statistics": serializable_stats,
        "duplicates": duplicates_df_copy.to_dict(orient='records'),
        "anomalies": anomalies_df_copy.to_dict(orient='records'),
        "llm_interpretation": llm_interpretation,
        "message": "Risk analysis data available."
    }

    with open(API_OUTPUT_PATH, 'w') as f:
        json.dump(api_response, f, indent=4)

    logger.info(f"Simulated API results saved to: {API_OUTPUT_PATH}")
