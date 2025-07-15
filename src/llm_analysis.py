import pandas as pd

# Prompt Versioning - LLMOps Practice
PROMPT_VERSION = "1.1"

def get_llm_prompt(stats, duplicates_df, anomalies_df):
    """Generates a versioned prompt for the LLM based on all analyses."""

    prompt = f"""[PROMPT_VERSION: {PROMPT_VERSION}]

    **Payment Risk Analysis - Request for Insights**

    **Context:** You are a financial risk analyst. Analyse the following data, which consists of payment statistics, a list of duplicate transactions and a list of anomalies detected by a Machine Learning model (Isolation Forest).

    **1. Descriptive Statistics:**
    - Mean: {stats['mean']:.2f}
    - Standard Deviation: {stats['std']:.2f}
    - Minimum: {stats['min']:.2f}
    - Maximum: {stats['max']:.2f}
    - Total Count: {int(stats['count'])}

    **2. Duplicates Report:**
    {duplicates_df.to_string() if not duplicates_df.empty else "No duplicates found."}

    **3. Anomalies Report (Machine Learning):**
    {anomalies_df.to_string() if not anomalies_df.empty else "No ML anomalies found."}

    **Task:**
    Based on ALL the data provided, provide a comprehensive risk analysis. Identify the main points of concern, suggest possible causes for the anomalies and recommend next steps for investigation.
    """

    return prompt

def get_llm_interpretation(prompt, logger):
    """Simulates an LLM response to the prompt analysis."""
    logger.info(f"Sending prompt (version {PROMPT_VERSION}) to LLM (simulated).")

    # Just for console visualisation
    print("\n--- LLM Analysis (Simulated) ---")
    print(prompt)

    interpretation = """
    **Comprehensive Risk Analysis:**

    **Points of Concern:**
    1.  **Critical Duplicates:** The presence of duplicate SSNs in the same month is a strong indicator of fraud or serious systemic error. Requires immediate action.
    2.  **Value Anomalies:** The ML model flagged payments with values that, whilst not duplicated, deviate significantly from the pattern. The payment of $2100.00 to SSN 666-00-6666 is a clear example, being much higher than the average.
    3.  **High Variability:** The elevated standard deviation relative to the mean suggests that there are different payment categories or significant outliers, which may complicate the detection of subtle fraud.

    **Recommended Next Steps:**
    - **Immediate Investigation:** Contact the beneficiaries associated with duplicate SSNs to validate the transactions.
    - **Anomaly Audit:** Review the payments flagged by the ML model to determine if they are legitimate (e.g. backdated payments) or fraudulent.
    - **Model Refinement:** Consider adding more features to the ML model (e.g. beneficiary history, location) to improve anomaly detection accuracy.
    """

    logger.info("LLM interpretation (simulated) received.")
    print("\n--- LLM Interpretation (Simulated) ---")
    print(interpretation)
    return interpretation
