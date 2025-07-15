import os

# Project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data paths
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'payments.db')
PAYMENTS_CSV = os.path.join(DATA_DIR, 'payments_sample.csv')

# SQL paths
SQL_DIR = os.path.join(ROOT_DIR, 'sql')
INIT_DB_SQL = os.path.join(SQL_DIR, 'init_db.sql')

# Output directory for reports and charts
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')

# Output file names
DUPLICATES_REPORT_PATH = os.path.join(OUTPUT_DIR, 'duplicate_ssns_report.txt')
COMPREHENSIVE_REPORT_PATH = os.path.join(OUTPUT_DIR, 'comprehensive_analysis_report.md')

# Chart file names
PAYMENT_DISTRIBUTION_CHART = os.path.join(OUTPUT_DIR, 'payment_distribution.png')
MONTHLY_TREND_CHART = os.path.join(OUTPUT_DIR, 'monthly_payment_trend.png')
STATS_SUMMARY_TABLE = os.path.join(OUTPUT_DIR, 'statistical_summary.png')
ANOMALY_REPORT_PATH = os.path.join(OUTPUT_DIR, 'ml_anomaly_report.txt')

# Log files
LOG_FILE_PATH = os.path.join(ROOT_DIR, 'logs/pipeline.log')

# Big Data simulation
HDFS_SIMULATION_DIR = os.path.join(ROOT_DIR, 'hdfs_simulation')
FLINK_OUTPUT_PATH = os.path.join(HDFS_SIMULATION_DIR, 'user/data/flink_processed_results.txt')

# Data quality reports
DATA_VALIDATION_REPORT_PATH = os.path.join(OUTPUT_DIR, 'data_validation_report.txt')

# Monitoring and alert logs
ALERT_LOG_PATH = os.path.join(OUTPUT_DIR, 'alerts.log')

# API simulation
API_OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'api_results.json')

# Interactive dashboard
INTERACTIVE_DASHBOARD_PATH = os.path.join(OUTPUT_DIR, 'interactive_dashboard.html')
