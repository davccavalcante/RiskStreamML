import logging
import json
import os
from src.config import LOG_FILE_PATH

class JsonFormatter(logging.Formatter):
    """Formats logs as JSON."""
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
        }
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def setup_logger():
    """Configures and returns a structured logger."""
    # Create the logs directory if it doesn't exist
    log_dir = os.path.dirname(LOG_FILE_PATH)
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers if the logger is already configured
    if not logger.handlers:
        handler = logging.FileHandler(LOG_FILE_PATH)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

        # Add a console handler for real-time visualisation
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(console_handler)

    return logger
