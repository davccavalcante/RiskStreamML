import os
import pandas as pd
from src.config import DB_PATH, INIT_DB_SQL
from src.db import get_db_connection, execute_sql_from_file, insert_data
from src.etl import read_payments_data, find_and_report_duplicates
from src.graphs import (
    generate_payment_distribution_chart,
    generate_monthly_trend_chart,
    generate_stats_summary_table
)
from src.llm_analysis import get_llm_prompt, get_llm_interpretation
from src.ml_analysis import detect_anomalies
from src.kafka_producer import emulate_kafka_producer
from src.kafka_consumer import consume_events
from src.flink_processor import FlinkJobSimulator
from src.llm_analysis import get_llm_prompt, get_llm_interpretation
from src.reporting import generate_comprehensive_report
from src.logger import setup_logger
from src.data_validation import validate_payments_data
from src.monitoring import monitor_pipeline_logs
from src.api_simulator import simulate_rest_api
from src.dashboard_generator import generate_interactive_dashboard

def main():
    """Main function that orchestrates the entire project flow."""
    logger = setup_logger()
    logger.info("Risk analysis pipeline started.")

    # --- 1. Database Initialisation ---
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        logger.info(f"Old database removed: {DB_PATH}")

    conn = get_db_connection()
    execute_sql_from_file(conn, INIT_DB_SQL)
    logger.info("Database and 'payments' table initialised.")

    # --- 2. ETL Process (Extract, Transform, Load) ---
    raw_data_df = read_payments_data()
    logger.info(f"Read {len(raw_data_df)} records from CSV.")

    # --- 2.1. Data Quality Validation ---
    is_data_valid = validate_payments_data(raw_data_df.copy(), logger)
    if not is_data_valid:
        logger.error("Data validation failed. Aborting pipeline.")
        return # Abort if data is not valid

    raw_data_df['payment_month'] = pd.to_datetime(raw_data_df['payment_date']).dt.to_period('M')
    duplicates_df = raw_data_df[raw_data_df.duplicated(subset=['ssn', 'payment_month'], keep=False)]
    raw_data_df.drop(columns=['payment_month'], inplace=True)

    cleaned_df = find_and_report_duplicates(raw_data_df)
    logger.info(f"{len(duplicates_df)} duplicates found and reported.")

    insert_data(conn, cleaned_df, 'payments')
    logger.info(f"{len(cleaned_df)} clean records inserted into database.")

    # --- 3. Analysis and Visualisation ---
    db_df = pd.read_sql_query("SELECT * FROM payments", conn)
    conn.close()
    logger.info("Data read from database for analysis.")

    generate_payment_distribution_chart(db_df)
    generate_monthly_trend_chart(db_df)
    generate_stats_summary_table(db_df)
    logger.info("Analysis charts generated.")

    # --- 4. Machine Learning - Anomaly Detection ---
    anomalies_df = detect_anomalies(db_df, logger)

    # --- 5. Streaming Simulation with Kafka and Flink ---
    # The producer returns events so the simulated consumer/flink can use them
    kafka_events = emulate_kafka_producer(db_df, logger=logger)

    # Simulates Flink job consuming and processing events
    flink_job = FlinkJobSimulator(kafka_events, logger)
    consume_events('payment_events', flink_job.process_stream, logger)
    logger.info("Streaming simulation with Kafka and Flink completed.")

    # --- 6. LLM Analysis and Final Report ---
    stats = db_df['amount'].describe()
    total_amount = db_df['amount'].sum()

    llm_prompt = get_llm_prompt(stats, duplicates_df, anomalies_df)
    llm_interpretation = get_llm_interpretation(llm_prompt, logger)

    generate_comprehensive_report(stats, total_amount, duplicates_df, anomalies_df, llm_interpretation, logger)

    # --- 7. Results Exposure (API and Dashboard) ---
    simulate_rest_api(stats, duplicates_df, anomalies_df, llm_interpretation, logger)
    generate_interactive_dashboard(db_df, duplicates_df, anomalies_df, logger)

    # --- 8. Monitoring and Alerts ---
    monitor_pipeline_logs(logger)

    logger.info("Risk analysis pipeline completed successfully!")

if __name__ == "__main__":
    main()
