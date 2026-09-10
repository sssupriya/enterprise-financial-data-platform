import argparse
import random
import pandas as pd
import yaml
import time

from datetime import datetime, timedelta
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

internet_config = config["internet_banking"]

logger = get_logger("internet_banking")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Internet Banking transactions"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="Business date in YYYY-MM-DD format"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=5000,
        help="Number of Internet Banking transactions"
    )

    return parser.parse_args()


def load_master_data():
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    accounts = pd.read_csv(DATA_DIR / "accounts.csv")

    return customers, accounts


def generate_ip():
    return ".".join(
        str(random.randint(1, 254))
        for _ in range(4)
    )


def generate_transaction(
    transaction_number,
    business_date,
    customers,
    accounts
):
    # Pick an existing bank account
    account = accounts.iloc[
        random.randrange(len(accounts))
    ]

    # Find the customer who owns that account
    customer = customers[
        customers["customer_id"] == account["customer_id"]
    ].iloc[0]

    # Decide whether this is a new beneficiary
    is_new_beneficiary = (
        random.random()
        < internet_config["new_beneficiary_probability"]
    )

    # New beneficiaries get a large-transfer scenario
    if is_new_beneficiary:
        amount = round(
            random.uniform(
                internet_config["amount"]["large_min"],
                internet_config["amount"]["large_max"]
            ),
            2
        )

        beneficiary_type = "NEW"

    else:
        amount = round(
            random.uniform(
                internet_config["amount"]["normal_min"],
                internet_config["amount"]["normal_max"]
            ),
            2
        )

        beneficiary_type = "EXISTING"

    # Generate transaction time
    hour = random.randint(
        internet_config["transaction_hours"]["start"],
        internet_config["transaction_hours"]["end"]
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

    # Login should happen before the transfer
    login_time = timestamp - timedelta(
        minutes=random.randint(1, 30)
    )

    browser = random.choice(
        internet_config["browsers"]
    )

    operating_system = random.choice(
        internet_config["operating_systems"]
    )

    beneficiary = (
        f"BEN{random.randint(100000, 999999)}"
    )

    return {
        "transaction_id": (
            f"IB{timestamp.strftime('%Y%m%d')}"
            f"-{transaction_number:08d}"
        ),
        "customer_id": customer["customer_id"],
        "account_number": account["account_number"],
        "amount": amount,
        "timestamp": timestamp,
        "status": random.choices(
            ["SUCCESS", "FAILED", "PENDING"],
            weights=internet_config["status_weights"],
            k=1
        )[0],
        "browser": browser,
        "ip": generate_ip(),
        "os": operating_system,
        "login_time": login_time,
        "beneficiary": beneficiary,
        "beneficiary_type": beneficiary_type,
    }


def generate_internet_transactions(
    count,
    business_date,
    customers,
    accounts
):
    transactions = []

    for i in range(1, count + 1):
        transactions.append(
            generate_transaction(
                i,
                business_date,
                customers,
                accounts
            )
        )

    return pd.DataFrame(transactions)


def main():
    args = parse_args()

    start_time = time.perf_counter()

    logger.info(
        "Generation started",
        extra={
            "channel": "internet_banking"
        }
    )

    try:
        customers, accounts = load_master_data()

        df = generate_internet_transactions(
            args.count,
            args.date,
            customers,
            accounts
        )

        output_path = get_landing_path(
            "internet_banking",
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
                "channel": "internet_banking",
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
                "channel": "internet_banking",
                "duration_seconds": duration,
            }
        )

        raise


if __name__ == "__main__":
    main()