import pandas as pd
from src.config import PAYMENTS_CSV, DUPLICATES_REPORT_PATH, OUTPUT_DIR
import os

def read_payments_data():
    """Reads payment data from CSV file."""
    return pd.read_csv(PAYMENTS_CSV)

def find_and_report_duplicates(df):
    """Finds duplicate SSNs, generates a report and returns a clean DataFrame."""
    df['payment_month'] = pd.to_datetime(df['payment_date']).dt.to_period('M')

    # Finds duplicates based on SSN and payment month
    duplicates = df[df.duplicated(subset=['ssn', 'payment_month'], keep=False)]

    if not duplicates.empty:
        # Creates output directory if it doesn't exist
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Saves duplicates report
        with open(DUPLICATES_REPORT_PATH, 'w') as f:
            f.write("Duplicate SSNs Detected Report:\n")
            f.write("="*40 + "\n")
            f.write(duplicates.to_string())
        print(f"Duplicates report saved at: {DUPLICATES_REPORT_PATH}")

    # Removes duplicates to return a clean DataFrame
    cleaned_df = df.drop_duplicates(subset=['ssn', 'payment_month'], keep='first')
    return cleaned_df.drop(columns=['payment_month'])
