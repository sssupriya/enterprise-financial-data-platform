import argparse
import random
import pandas as pd
import yaml

from datetime import datetime, date, timedelta
from pathlib import Path


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "generator_config.yaml"
DATA_DIR = PROJECT_ROOT / "data"

## Create data directory if it doesn't exist
MOBILE_DATA_DIR = DATA_DIR / "mobile"
MOBILE_DATA_DIR.mkdir(exist_ok=True)


# Load configuration
with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)


# Seed
SEED = config["seed"]

# Master data configuration
master_config = config["master_data"]

# Mobile banking configuration
mobile_config = config["mobile"]

SMALL_AMOUNT_PROBABILITY = mobile_config["small_amount_probability"]

NORMAL_SMALL_MIN = mobile_config["normal_amount"]["small"]["min"]
NORMAL_SMALL_MAX = mobile_config["normal_amount"]["small"]["max"]

NORMAL_LARGE_MIN = mobile_config["normal_amount"]["large"]["min"]
NORMAL_LARGE_MAX = mobile_config["normal_amount"]["large"]["max"]

SALARY_DAY = mobile_config["salary"]["day"]
SALARY_PROBABILITY = mobile_config["salary"]["probability"]
SALARY_MIN = mobile_config["salary"]["amount"]["min"]
SALARY_MAX = mobile_config["salary"]["amount"]["max"]

EMI_DAY = mobile_config["emi"]["day"]
EMI_PROBABILITY = mobile_config["emi"]["probability"]
EMI_MIN = mobile_config["emi"]["amount"]["min"]
EMI_MAX = mobile_config["emi"]["amount"]["max"]

UTILITY_START_DAY = mobile_config["utility"]["start_day"]
UTILITY_END_DAY = mobile_config["utility"]["end_day"]
UTILITY_PROBABILITY = mobile_config["utility"]["probability"]
UTILITY_MIN = mobile_config["utility"]["amount"]["min"]
UTILITY_MAX = mobile_config["utility"]["amount"]["max"]

STATUS_SUCCESS_PROBABILITY = mobile_config["status"]["success_probability"]
STATUS_FAILED_PROBABILITY = mobile_config["status"]["failed_probability"]
STATUS_PENDING_PROBABILITY = mobile_config["status"]["pending_probability"]

DEVICE_ID_MIN = mobile_config["device_id"]["min"]
DEVICE_ID_MAX = mobile_config["device_id"]["max"]

## Argument parsing parse_args()
def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate mobile banking transactions"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="Transaction date in YYYY-MM-DD format"
    )

    parser.add_argument(
        "--count",
        required=True,
        type=int,
        help="Number of transactions to generate"
    )

    return parser.parse_args()

## Load master data
def load_master_data():
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    accounts = pd.read_csv(DATA_DIR / "accounts.csv")
    merchants = pd.read_csv(DATA_DIR / "merchants.csv")

    return customers, accounts, merchants

## Generate timestamp for a transaction
## The function generates a timestamp for a transaction on a given date, with a higher likelihood of transactions occurring during evening hours.
def generate_timestamp(transaction_date):
    # Evening hours are more likely
    hour_weights = {
        0: 1,
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 2,
        7: 2,
        8: 3,
        9: 3,
        10: 3,
        11: 3,
        12: 4,
        13: 4,
        14: 4,
        15: 4,
        16: 5,
        17: 6,
        18: 8,
        19: 10,
        20: 10,
        21: 8,
        22: 5,
        23: 3
    }

    hours = list(hour_weights.keys())
    weights = list(hour_weights.values())

    hour = random.choices(hours, weights=weights, k=1)[0]

    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return datetime.combine(
        transaction_date,
        datetime.min.time()
    ).replace(
        hour=hour,
        minute=minute,
        second=second
    )

## Generate timestamp for a transaction
## The function generates a timestamp for a transaction on a given date, with a higher likelihood of transactions occurring during evening hours. 
## Additionally, it increases the likelihood of transactions occurring on weekends.  
def generate_timestamp(transaction_date):
    # Normal weekday activity
    hour_weights = {
        0: 1,
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 2,
        7: 2,
        8: 3,
        9: 3,
        10: 3,
        11: 3,
        12: 4,
        13: 4,
        14: 4,
        15: 4,
        16: 5,
        17: 6,
        18: 8,
        19: 10,
        20: 10,
        21: 8,
        22: 5,
        23: 3
    }

    # Increase activity on Saturday and Sunday
    if transaction_date.weekday() in [5, 6]:
       for hour in [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]:
            hour_weights[hour] *= 2

    hours = list(hour_weights.keys())
    weights = list(hour_weights.values())

    hour = random.choices(
        hours,
        weights=weights,
        k=1
    )[0]

    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return datetime.combine(
        transaction_date,
        datetime.min.time()
    ).replace(
        hour=hour,
        minute=minute,
        second=second
    )

## Determine transaction type based on the day of the month
def determine_transaction_type(transaction_date):
    day = transaction_date.day

    if day == SALARY_DAY:
        return random.choices(
            ["SALARY_CREDIT", "NORMAL"],
            weights=[
                SALARY_PROBABILITY,
                1 - SALARY_PROBABILITY
            ],
            k=1
        )[0]

    if day == EMI_DAY:
        return random.choices(
            ["EMI_DEBIT", "NORMAL"],
            weights=[
                EMI_PROBABILITY,
                1 - EMI_PROBABILITY
            ],
            k=1
        )[0]

    if UTILITY_START_DAY <= day <= UTILITY_END_DAY:
        return random.choices(
            ["UTILITY", "NORMAL"],
            weights=[
                UTILITY_PROBABILITY,
                1 - UTILITY_PROBABILITY
            ],
            k=1
        )[0]

    return "NORMAL"

## Generate transaction amount based on the transaction type
def generate_amount(transaction_type):

    if transaction_type == "SALARY_CREDIT":
        return round(
            random.uniform(SALARY_MIN, SALARY_MAX),
            2
        )

    if transaction_type == "EMI_DEBIT":
        return round(
            random.uniform(EMI_MIN, EMI_MAX),
            2
        )

    if transaction_type == "UTILITY":
        return round(
            random.uniform(UTILITY_MIN, UTILITY_MAX),
            2
        )

    # Normal transactions
    if random.random() < SMALL_AMOUNT_PROBABILITY:
        return round(
            random.uniform(
                NORMAL_SMALL_MIN,
                NORMAL_SMALL_MAX
            ),
            2
        )

    return round(
        random.uniform(
            NORMAL_LARGE_MIN,
            NORMAL_LARGE_MAX
        ),
        2
    )

## Generate transaction status based on predefined probabilities
def generate_status():
    return random.choices(
        ["SUCCESS", "FAILED", "PENDING"],
        weights=[
            STATUS_SUCCESS_PROBABILITY,
            STATUS_FAILED_PROBABILITY,
            STATUS_PENDING_PROBABILITY
        ],
        k=1
    )[0]

## Generate a single transaction
def generate_transaction(
    transaction_number,
    transaction_date,
    customers,
    accounts,
    merchants
):
    account = accounts.sample(n=1).iloc[0]

    customer = customers[
        customers["customer_id"] == account["customer_id"]
    ].iloc[0]


    transaction_type = determine_transaction_type(
        transaction_date
    )

    if transaction_type == "UTILITY":
        utility_merchants = merchants[
            merchants["category"] == "utilities"
        ]

        merchant = utility_merchants.sample(n=1).iloc[0]

    else:
        merchant = merchants.sample(n=1).iloc[0]

    timestamp = generate_timestamp(
        transaction_date
    )

    amount = generate_amount(
        transaction_type
    )

    return {
        "transaction_id": (
            f"MOB{transaction_date.strftime('%Y%m%d')}"
            f"-{transaction_number:08d}"
        ),
        "customer_id": customer["customer_id"],
        "account_number": account["account_number"],
        "amount": amount,
        "merchant": merchant["merchant_name"],
        "device_id": f"DEV{random.randint(DEVICE_ID_MIN, DEVICE_ID_MAX)}",
        "gps_city": customer["city"],
        "timestamp": timestamp,
        "status": generate_status()
    }

## Generate multiple transactions
def generate_transactions(
    count,
    transaction_date,
    customers,
    accounts,
    merchants
):
    transactions = []

    for i in range(1, count + 1):
        transaction = generate_transaction(
            i,
            transaction_date,
            customers,
            accounts,
            merchants
        )

        transactions.append(transaction)

    return pd.DataFrame(transactions)

## Main execution
if __name__ == "__main__":
    args = parse_args()

    ## Load master data
    customers, accounts, merchants = load_master_data()

    ## Parse transaction date
    transaction_date = datetime.strptime(
        args.date,
        "%Y-%m-%d"
    ).date()

    print("Date:", args.date)
    print("Count:", args.count)
    print("Customers loaded:", len(customers))
    print("Accounts loaded:", len(accounts))
    print("Merchants loaded:", len(merchants))

    df = generate_transactions(
        args.count,
        transaction_date,
        customers,
        accounts,
        merchants
    )

    output_file = MOBILE_DATA_DIR / f"{transaction_date}.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print(f"Created {len(df)} mobile transactions")
    print(f"Saved to: {output_file}")

    print(df.head(10))

    # for _ in range(10):
    #     transaction_type = determine_transaction_type(
    #         transaction_date
    #     )

    #     timestamp = generate_timestamp(
    #         transaction_date
    #     )

    #     amount = generate_amount(transaction_type)

    #     print(timestamp, transaction_type, amount)