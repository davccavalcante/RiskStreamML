import json
import os
from src.config import LOG_FILE_PATH, ALERT_LOG_PATH, OUTPUT_DIR

def monitor_pipeline_logs(logger):
    """Simulates pipeline log monitoring for critical events and generates alerts."""
    logger.info("Starting pipeline log monitoring.")
    alerts_generated = []

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(LOG_FILE_PATH):
        logger.warning(f"Log file not found at {LOG_FILE_PATH}. Skipping monitoring.")
        return

    with open(LOG_FILE_PATH, 'r') as f_log, open(ALERT_LOG_PATH, 'w') as f_alert:
        f_alert.write("Generated Alerts Log:\n")
        f_alert.write("="*70 + "\n")
        for line in f_log:
            try:
                log_entry = json.loads(line)
                message = log_entry.get('message', '').lower()
                level = log_entry.get('level', '').lower()

                # Alert Rules (examples)
                if "duplicates found" in message:
                    alert_msg = f"ALERT: Duplicates detected in ETL! Details: {log_entry}"
                    alerts_generated.append(alert_msg)
                    f_alert.write(alert_msg + "\n")
                elif "payment anomalies" in message:
                    alert_msg = f"ALERT: ML anomalies detected! Details: {log_entry}"
                    alerts_generated.append(alert_msg)
                    f_alert.write(alert_msg + "\n")
                elif "validation issues" in message or level == "warning":
                    alert_msg = f"ALERT: Data validation issues or warning in pipeline! Details: {log_entry}"
                    alerts_generated.append(alert_msg)
                    f_alert.write(alert_msg + "\n")

            except json.JSONDecodeError:
                # Ignores lines that are not valid JSON (e.g. console logs)
                pass

    if alerts_generated:
        logger.warning(f"Log monitoring completed. {len(alerts_generated)} alerts generated. See {ALERT_LOG_PATH}")
    else:
        logger.info("Log monitoring completed. No critical alerts generated.")
