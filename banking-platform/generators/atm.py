import argparse
import pandas as pd
import random
import yaml
import time

from pathlib import Path

from shared.landing import get_landing_path
from shared.logger import get_logger

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "generator_config.yaml"
DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)

# Load configuration
with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)

logger = get_logger("atm")

# Seed randomness
SEED = config["seed"]

random.seed(SEED)

##  Master Data
CITIES = config["master_data"]["cities"]

##  ATM Configuration
atm_config = config["atm"]

WITHDRAWAL_MIN = atm_config["withdrawal"]["min"]
WITHDRAWAL_MAX = atm_config["withdrawal"]["max"]
WITHDRAWAL_MULTIPLE = atm_config["withdrawal"]["multiple"]

PIN_NORMAL_PROBABILITY = atm_config["pin_attempts"]["normal_probability"]
PIN_FAILURE_PROBABILITY = atm_config["pin_attempts"]["failure_probability"]

BALANCE_MIN = atm_config["balance"]["min"]
BALANCE_MAX = atm_config["balance"]["max"]

HEALTH_HEALTHY_PROBABILITY = atm_config["health"]["healthy_probability"]
HEALTH_DEGRADED_PROBABILITY = atm_config["health"]["degraded_probability"]
HEALTH_DOWN_PROBABILITY = atm_config["health"]["down_probability"]

ATM_ID_MIN = atm_config["atm_id"]["start"]
ATM_ID_MAX = atm_config["atm_id"]["end"]

## ATM Functions
def generate_withdrawal_amount():
    amount = random.randint(
        WITHDRAWAL_MIN // WITHDRAWAL_MULTIPLE,
        WITHDRAWAL_MAX // WITHDRAWAL_MULTIPLE
    )

    return amount * WITHDRAWAL_MULTIPLE

## Generate PIN attempts
def generate_pin_attempts():

    if random.random() < PIN_FAILURE_PROBABILITY:
        return 3

    return random.choice([1, 1, 1, 2])

##  Generate ATM health status
def generate_atm_health():

    return random.choices(
        ["HEALTHY", "DEGRADED", "DOWN"],
        weights=[
            HEALTH_HEALTHY_PROBABILITY,
            HEALTH_DEGRADED_PROBABILITY,
            HEALTH_DOWN_PROBABILITY
        ],
        k=1
    )[0]

## Generate one ATM transaction 
def generate_atm_transaction(transaction_number, cities):

    balance_before = round(
        random.uniform(BALANCE_MIN, BALANCE_MAX),
        2
    )

    withdrawal_amount = generate_withdrawal_amount()

    balance_after = round(
        max(0, balance_before - withdrawal_amount),
        2
    )

    return {
        "atm_id": f"ATM{random.randint(ATM_ID_MIN, ATM_ID_MAX)}",
        "withdrawal_amount": withdrawal_amount,
        "balance_after": balance_after,
        "city": random.choice(cities),
        "pin_attempts": generate_pin_attempts(),
        "atm_health": generate_atm_health()
    }

##  Generate multiple ATM transactions
def generate_atm_transactions(count):

    transactions = []

    for i in range(1, count + 1):

        transaction = generate_atm_transaction(
            i,
            CITIES
        )

        transactions.append(transaction)

    return pd.DataFrame(transactions)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate ATM transactions"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="Business date in YYYY-MM-DD format"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Number of ATM transactions"
    )

    return parser.parse_args()

##  Main execution
if __name__ == "__main__":
    args = parse_args()

    start_time = time.perf_counter()

    logger.info(
        "Generation started",
        extra={
            "channel": "atm"
        }
    )

    try:
        df = generate_atm_transactions(
            args.count,
        )

        output_file = get_landing_path(
            "atm",
            args.date
        )

        df.to_csv(
            output_file,
            index=False
        )

        duration = round(
            time.perf_counter() - start_time,
            3
        )

        logger.info(
            "Generation completed",
            extra={
                "channel": "atm",
                "rows": len(df),
                "output_path": str(output_file),
                "duration_seconds": duration,
            }
        )

    except Exception:
        duration = round(
            time.perf_counter() - start_time,
            3
        )

        logger.exception(
            "Generation failed",
            extra={
                "channel": "atm",
                "duration_seconds": duration,
            }
        )

        raise