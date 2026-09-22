from datetime import date, timedelta
from pathlib import Path
import subprocess
import sys
import time


# Project root: banking-platform/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Allows this script to import shared.logger
sys.path.insert(0, str(PROJECT_ROOT))

from shared.logger import get_logger


logger = get_logger("backfill")

START_DATE = date(2026, 7, 1)

# Keep 2 while testing logging.
NUMBER_OF_DAYS = 30


logger.info(
    "Backfill started",
    extra={
        "rows": NUMBER_OF_DAYS
    }
)

backfill_start = time.perf_counter()


for day_offset in range(NUMBER_OF_DAYS):

    business_date = START_DATE + timedelta(days=day_offset)

    logger.info(
        f"Business date started: {business_date}"
    )

    command = [
        sys.executable,
        str(PROJECT_ROOT / "run_generation.py"),
        "--date",
        business_date.isoformat(),
    ]

    try:
        subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            check=True,
        )

        logger.info(
            f"Business date completed: {business_date}"
        )

    except subprocess.CalledProcessError:
        logger.exception(
            f"Business date failed: {business_date}"
        )
        raise


duration = round(
    time.perf_counter() - backfill_start,
    3
)

logger.info(
    "Backfill completed",
    extra={
        "duration_seconds": duration
    }
)