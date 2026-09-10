import argparse
import subprocess
import sys
import time

from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
)

from shared.logger import get_logger


logger = get_logger("runner")


CHANNELS = [
    "mobile",
    "atm",
    "upi",
    "credit_card",
    "internet_banking",
    "branch",
]

GENERATOR_COUNTS = {
    "mobile": 20000,
    "atm": 100,
    "upi": 50000,
    "credit_card": 10000,
    "internet_banking": 5000,
    "branch": 500,
}

results = []


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run all banking data generators"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="Business date in YYYY-MM-DD format"
    )

    return parser.parse_args()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),
    reraise=True
)
def run_generator(channel, business_date):
    logger.info(
        "Generator attempt started",
        extra={
            "channel": channel
        }
    )

    count = GENERATOR_COUNTS[channel]

    command = [
        sys.executable,
        "-m",
        f"generators.{channel}",
        "--date",
        business_date,
        "--count",
        str(count),
    ]

    subprocess.run(
        command,
        check=True
    )


if __name__ == "__main__":
    args = parse_args()

    for channel in CHANNELS:
        start_time = time.perf_counter()

        try:
            run_generator(
                channel,
                args.date
            )

            duration = round(
                time.perf_counter() - start_time,
                3
            )

            results.append({
                "channel": channel,
                "status": "SUCCESS",
                "rows": GENERATOR_COUNTS[channel],
                "duration_seconds": duration,
            })

        except Exception:
            duration = round(
                time.perf_counter() - start_time,
                3
            )

            results.append({
                "channel": channel,
                "status": "FAILED",
                "rows": 0,
                "duration_seconds": duration,
            })

            logger.exception(
                "Generator failed after retries",
                extra={
                    "channel": channel,
                    "duration_seconds": duration,
                }
            )



    for result in results:
        logger.info(
            "Generation summary",
            extra={
                "channel": result["channel"],
                "rows": result["rows"],
                "duration_seconds": result["duration_seconds"],
            }
        )

    failed_channels = [
        result["channel"]
        for result in results
        if result["status"] == "FAILED"
    ]

    if failed_channels:
        logger.error(
            f"Generation completed with failures: {failed_channels}"
        )
        sys.exit(1)

    logger.info(
        "All generators completed successfully"
    )

    sys.exit(0)