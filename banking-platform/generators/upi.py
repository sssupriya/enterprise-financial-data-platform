import argparse
import random
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

import time
from shared.logger import get_logger

from shared.landing import get_landing_path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "generator_config.yaml"
DATA_DIR = PROJECT_ROOT / "data"


with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)


logger = get_logger("upi")


SEED = config["seed"]
random.seed(SEED)

upi_config = config["upi"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate UPI transactions"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="Business date in YYYY-MM-DD format"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=50000,
        help="Number of UPI transactions"
    )

    return parser.parse_args()


def load_master_data():
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    accounts = pd.read_csv(DATA_DIR / "accounts.csv")
    merchants = pd.read_csv(DATA_DIR / "merchants.csv")

    return customers, accounts, merchants


def generate_amount():
    if random.random() < upi_config["small_amount_probability"]:
        return round(
            random.uniform(
                upi_config["small_amount"]["min"],
                upi_config["small_amount"]["max"]
            ),
            2
        )

    return round(
        random.uniform(
            upi_config["large_amount"]["min"],
            upi_config["large_amount"]["max"]
        ),
        2
    )


def generate_transaction(
    transaction_number,
    business_date,
    customers,
    accounts,
    merchants
):
    account = accounts.iloc[
        random.randrange(len(accounts))
    ]

    customer = customers[
        customers["customer_id"] == account["customer_id"]
    ].iloc[0]

    merchant = merchants.iloc[
        random.randrange(len(merchants))
    ]

    hour = random.randint(6, 23)
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

    banks = upi_config["counterparty_banks"]

    upi_handle = (
        customer["name"]
        .lower()
        .replace(" ", "")
        [:12]
    )

    vpa = f"{upi_handle}@upi"

    return {
        "transaction_id": (
            f"UPI{timestamp.strftime('%Y%m%d')}"
            f"-{transaction_number:08d}"
        ),
        "customer_id": customer["customer_id"],
        "account_number": account["account_number"],
        "amount": generate_amount(),
        "timestamp": timestamp,
        "status": random.choices(
            ["SUCCESS", "FAILED", "PENDING"],
            weights=[0.96, 0.03, 0.01],
            k=1
        )[0],
        "upi_handle": upi_handle,
        "vpa": vpa,
        "merchant": merchant["merchant_name"],
        "device": f"DEV{random.randint(100000, 999999)}",
        "counterparty_bank": random.choice(banks),
    }


def generate_upi_transactions(
    count,
    business_date,
    customers,
    accounts,
    merchants
):
    transactions = []

    for i in range(1, count + 1):
        transactions.append(
            generate_transaction(
                i,
                business_date,
                customers,
                accounts,
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
            "channel": "upi"
        }
    )

    try:
        customers, accounts, merchants = load_master_data()

        df = generate_upi_transactions(
            args.count,
            args.date,
            customers,
            accounts,
            merchants
        )

        output_path = get_landing_path(
            "upi",
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
                "channel": "upi",
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
                "channel": "upi",
                "duration_seconds": duration,
            }
        )

        raise


if __name__ == "__main__":
    main()  