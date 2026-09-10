import argparse
import random
import pandas as pd
import yaml
import time

from datetime import datetime
from pathlib import Path


from shared.landing import get_landing_path
from shared.logger import get_logger


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "generator_config.yaml"
DATA_DIR = PROJECT_ROOT / "data"


with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)


SEED = config["seed"]
random.seed(SEED)

credit_card_config = config["credit_card"]
logger = get_logger("credit_card")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate credit card transactions"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="Business date in YYYY-MM-DD format"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=10000,
        help="Number of credit card transactions"
    )

    return parser.parse_args()


def load_master_data():
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    merchants = pd.read_csv(DATA_DIR / "merchants.csv")

    return customers, merchants


def generate_transaction(
    transaction_number,
    business_date,
    customers,
    merchants
):
    customer = customers.iloc[
        random.randrange(len(customers))
    ]

    merchant = merchants.iloc[
        random.randrange(len(merchants))
    ]

    hour = random.randint(
        credit_card_config["transaction_hours"]["start"],
        credit_card_config["transaction_hours"]["end"]
    )

    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    timestamp = datetime.strptime(
        business_date,
        "%Y-%m-%d"
    ).replace(
        hour=hour,
        minute=minute,
        second=second
    )

    card_type = random.choice(
        credit_card_config["card_types"]
    )

    credit_limit = random.choice(
        credit_card_config["credit_limits"]
    )

    amount = round(
        random.uniform(
            credit_card_config["amount"]["min"],
            credit_card_config["amount"]["max"]
        ),
        2
    )

    reward_points = int(
        amount
        * credit_card_config["reward_points_per_rupee"]
    )

    return {
        "transaction_id": (
            f"CC{timestamp.strftime('%Y%m%d')}"
            f"-{transaction_number:08d}"
        ),
        "customer_id": customer["customer_id"],
        "amount": amount,
        "timestamp": timestamp,
        "status": random.choices(
            ["SUCCESS", "FAILED", "PENDING"],
            weights=credit_card_config["status_weights"],
            k=1
        )[0],
        "merchant": merchant["merchant_name"],
        "merchant_category": merchant["category"],
        "terminal_id": (
            f"TERM{random.randint(100000, 999999)}"
        ),
        "card_type": card_type,
        "credit_limit": credit_limit,
        "reward_points": reward_points,
    }


def generate_credit_card_transactions(
    count,
    business_date,
    customers,
    merchants
):
    transactions = []

    for i in range(1, count + 1):
        transactions.append(
            generate_transaction(
                i,
                business_date,
                customers,
                merchants
            )
        )

    return pd.DataFrame(transactions)


def main():
    args = parse_args()

    start_time = time.perf_counter()

    logger.info(
        "Generation started",
        extra={
            "channel": "credit_card"
        }
    )

    try:
        customers, merchants = load_master_data()

        df = generate_credit_card_transactions(
            args.count,
            args.date,
            customers,
            merchants
        )

        output_path = get_landing_path(
            "credit_card",
            args.date
        )

        df.to_csv(
            output_path,
            index=False
        )

        duration = round(
            time.perf_counter() - start_time,
            3
        )

        logger.info(
            "Generation completed",
            extra={
                "channel": "credit_card",
                "rows": len(df),
                "output_path": str(output_path),
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
                "channel": "credit_card",
                "duration_seconds": duration,
            }
        )

        raise


if __name__ == "__main__":
    main()