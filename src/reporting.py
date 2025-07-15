import os
from src.config import COMPREHENSIVE_REPORT_PATH, OUTPUT_DIR
from src.ml_analysis import ISOLATION_FOREST_PARAMS
from src.llm_analysis import PROMPT_VERSION

def generate_comprehensive_report(stats, total_amount, duplicates_df, anomalies_df, llm_interpretation, logger):
    """Generates a comprehensive analysis report in Markdown format."""
    logger.info("Generating comprehensive analysis report.")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_payments = int(stats.loc['count'])
    mean_amount = stats.loc['mean']
    median_amount = stats.loc['50%']
    std_dev = stats.loc['std']

    with open(COMPREHENSIVE_REPORT_PATH, 'w') as f:
        f.write("# Risk Analysis and LLMOps Report\n\n")
        f.write(f"*This report was generated to track the execution of the risk analysis pipeline.*\n\n")
        f.write("## 1. Execution Parameters (LLMOps & MLOps)\n\n")
        f.write("### 1.1. Machine Learning Model\n")
        f.write(f"- **Model:** Isolation Forest\n")
        f.write(f"- **Parameters:** `{ISOLATION_FOREST_PARAMS}`\n\n")
        f.write("### 1.2. LLM Analysis\n")
        f.write(f"- **Prompt Version:** `{PROMPT_VERSION}`\n\n")

        f.write("## 2. General Summary\n\n")
        f.write(f"- **Total Processed Payments:** {total_payments}\n")
        f.write(f"- **Total Amount Paid:** ${total_amount:,.2f}\n")
        f.write(f"- **Average Payment Amount:** ${mean_amount:,.2f}\n")
        f.write(f"- **Payment Median:** ${median_amount:,.2f}\n")
        f.write(f"- **Standard Deviation:** ${std_dev:,.2f}\n\n")

        f.write("## 3. Duplicate Detection\n\n")
        if not duplicates_df.empty:
            f.write(f"**{len(duplicates_df)}** suspicious duplicate transactions were found.\n\n")
            f.write("```\n")
            f.write(duplicates_df.to_string())
            f.write("\n```\n")
        else:
            f.write("No duplicates were found.\n")

        f.write("\n## 4. Anomaly Detection (Machine Learning)\n\n")
        if not anomalies_df.empty:
            f.write(f"The ML model found **{len(anomalies_df)}** anomalous payments.\n\n")
            f.write("```\n")
            f.write(anomalies_df.to_string())
            f.write("\n```\n")
        else:
            f.write("No ML anomalies were found.\n")

        f.write("\n## 5. LLM Analysis and Interpretation\n\n")
        f.write("> " + llm_interpretation.replace('\n', '\n> ') + "\n")

        f.write("\n## 6. Visualisations\n\n")
        f.write("### Value Distribution\n")
        f.write("![Payment Distribution](payment_distribution.png)\n\n")
        f.write("### Monthly Trend\n")
        f.write("![Monthly Trend](monthly_payment_trend.png)\n\n")
        f.write("### Statistical Summary\n")
        f.write("![Statistical Summary](statistical_summary.png)\n")

    logger.info(f"Comprehensive report saved to: {COMPREHENSIVE_REPORT_PATH}")
