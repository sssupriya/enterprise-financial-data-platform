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

branch_config = config["branch"]
logger = get_logger("branch")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Branch transactions"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="Business date in YYYY-MM-DD format"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=500,
        help="Number of Branch transactions"
    )

    return parser.parse_args()


def load_master_data():
    customers = pd.read_csv(
        DATA_DIR / "customers.csv"
    )

    accounts = pd.read_csv(
        DATA_DIR / "accounts.csv"
    )

    branches = pd.read_csv(
        DATA_DIR / "branches.csv"
    )

    return customers, accounts, branches


def generate_cheque_number():
    return f"CHQ{random.randint(10000000, 99999999)}"


def generate_transaction(
    transaction_number,
    business_date,
    customers,
    accounts,
    branches
):
    account = accounts.iloc[
        random.randrange(len(accounts))
    ]

    customer = customers[
        customers["customer_id"]
        == account["customer_id"]
    ].iloc[0]

    branch = branches.iloc[
        random.randrange(len(branches))
    ]

    hour = random.randint(
        branch_config["business_hours"]["start"],
        branch_config["business_hours"]["end"] - 1
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

    cash_deposit = round(
        random.uniform(
            branch_config["cash_deposit"]["min"],
            branch_config["cash_deposit"]["max"]
        ),
        2
    )

    transaction_type = random.choice(
        ["CASH_DEPOSIT", "CHEQUE_DEPOSIT"]
    )

    amount = round(
    random.uniform(
        branch_config["cash_deposit"]["min"],
        branch_config["cash_deposit"]["max"]
    ),
    2
)

    if transaction_type == "CHEQUE_DEPOSIT":
        cash_deposit = 0
        cheque_number = generate_cheque_number()
    else:
        cash_deposit = amount
        cheque_number = ""

    return {
        "transaction_id": (
            f"BR{timestamp.strftime('%Y%m%d')}"
            f"-{transaction_number:08d}"
        ),
        "customer_id": customer["customer_id"],
        "account_number": account["account_number"],
        "branch_code": branch["branch_code"],
        "teller_id": (
            f"TEL{random.randint(
                branch_config['teller_id']['min'],
                branch_config['teller_id']['max']
            )}"
        ),
        "transaction_type": transaction_type,
        "cash_deposit": cash_deposit,
        "cheque_number": cheque_number,
        "timestamp": timestamp,
        "status": random.choices(
            ["SUCCESS", "FAILED"],
            weights=branch_config["status_weights"],
            k=1
        )[0],
    }


def generate_branch_transactions(
    count,
    business_date,
    customers,
    accounts,
    branches
):
    transactions = []

    for i in range(1, count + 1):
        transactions.append(
            generate_transaction(
                i,
                business_date,
                customers,
                accounts,
                branches
            )
        )

    return pd.DataFrame(transactions)


def main():
    args = parse_args()

    start_time = time.perf_counter()

    logger.info(
        "Generation started",
        extra={
            "channel": "branch"
        }
    )

    try:
        customers, accounts, branches = load_master_data()

        df = generate_branch_transactions(
            args.count,
            args.date,
            customers,
            accounts,
            branches
        )

        output_path = get_landing_path(
            "branch",
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
                "channel": "branch",
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
                "channel": "branch",
                "duration_seconds": duration,
            }
        )

        raise


if __name__ == "__main__":
    main()