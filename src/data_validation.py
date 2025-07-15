import pandas as pd
import os
from src.config import DATA_VALIDATION_REPORT_PATH, OUTPUT_DIR

def validate_payments_data(df, logger):
    """Performs basic validations on payment data and generates a report."""
    logger.info("Starting data quality validation.")
    validation_issues = []

    # Validation 1: Check essential columns
    required_columns = ['ssn', 'payment_date', 'amount', 'beneficiary_name']
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        validation_issues.append(f"Essential columns missing: {missing_cols}")
        # If essential columns are missing, we cannot proceed with validations that depend on them
        return_status = False
    else:
        return_status = True

    # Validation 2: Check null values in present essential columns
    for col in required_columns:
        if col in df.columns and df[col].isnull().any():
            validation_issues.append(f"Null values found in column '{col}'.")
            return_status = False

    # Validation 3: Check if 'amount' is numeric and positive (only if column exists)
    if 'amount' in df.columns:
        if not pd.api.types.is_numeric_dtype(df['amount']):
            validation_issues.append("Column 'amount' is not numeric.")
            return_status = False
        elif (df['amount'] < 0).any():
            validation_issues.append("Negative values found in column 'amount'.")
            return_status = False

    # Validation 4: Check date format (only if column exists)
    if 'payment_date' in df.columns:
        try:
            pd.to_datetime(df['payment_date'])
        except Exception:
            validation_issues.append("Invalid format in column 'payment_date'.")
            return_status = False

    # Generate validation report
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(DATA_VALIDATION_REPORT_PATH, 'w') as f:
        f.write("Data Quality Validation Report:\n")
        f.write("="*70 + "\n")
        if validation_issues:
            for issue in validation_issues:
                f.write(f"- {issue}\n")
            logger.warning(f"Data validation completed with {len(validation_issues)} issues.")
        else:
            f.write("No data validation issues found. Quality OK.\n")
            logger.info("Data validation completed without issues.")

    return return_status # Returns True if there are no issues
