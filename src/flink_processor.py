import pandas as pd
import os
from src.config import FLINK_OUTPUT_PATH, HDFS_SIMULATION_DIR

class FlinkJobSimulator:
    def __init__(self, events, logger):
        """Initialises the Flink job simulator.

        Args:
            events (list): A list of dictionaries, each representing a payment event.
            logger (Logger): The application logger.
        """
        self.events = events
        self.logger = logger
        self.beneficiary_counts = {}

    def process_stream(self):
        """Processes the event stream, performing aggregations."""
        self.logger.info("Flink job (simulated) started: processing event stream.")

        for event in self.events:
            beneficiary = event.get('beneficiary_name')
            if beneficiary:
                # Real-time aggregation: counts payments per beneficiary
                self.beneficiary_counts[beneficiary] = self.beneficiary_counts.get(beneficiary, 0) + 1

        self.logger.info("Real-time aggregation completed.")
        self._write_to_hdfs_sink()

    def _write_to_hdfs_sink(self):
        """Simulates writing the aggregated results to an HDFS sink."""
        self.logger.info(f"Writing Flink results to simulated HDFS at: {FLINK_OUTPUT_PATH}")

        # Creates the simulated HDFS directory if it doesn't exist
        os.makedirs(os.path.dirname(FLINK_OUTPUT_PATH), exist_ok=True)

        with open(FLINK_OUTPUT_PATH, 'w') as f:
            f.write("Flink Aggregation Result (Payment Count per Beneficiary):\n")
            f.write("="*70 + "\n")
            for beneficiary, count in self.beneficiary_counts.items():
                f.write(f"{beneficiary}: {count}\n")

        self.logger.info("Flink results saved successfully.")
