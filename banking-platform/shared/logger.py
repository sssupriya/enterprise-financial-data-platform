import json
import logging
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)


class JsonFormatter(logging.Formatter):

    def format(self, record):

        log_record = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if hasattr(record, "channel"):
            log_record["channel"] = record.channel

        if hasattr(record, "rows"):
            log_record["rows"] = record.rows

        if hasattr(record, "output_path"):
            log_record["output_path"] = record.output_path

        if hasattr(record, "duration_seconds"):
            log_record["duration_seconds"] = record.duration_seconds

        if record.exc_info:
            log_record["exception"] = self.formatException(
                record.exc_info
            )

        return json.dumps(log_record)


def get_logger(name):

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        JsonFormatter()
    )

    log_file = (
        LOG_DIR
        / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    file_handler.setFormatter(
        JsonFormatter()
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger