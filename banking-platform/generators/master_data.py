
from faker import Faker
import pandas as pd
import random
import yaml


from datetime import datetime, timedelta
from pathlib import Path
from shared.logger import get_logger

logger = get_logger("master_data")


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "generator_config.yaml"
DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)

# Load configuration
with open(CONFIG_FILE, "r") as file:
    config = yaml.safe_load(file)


# Seed randomness
SEED = config["seed"]

Faker.seed(SEED)
random.seed(SEED)

fake = Faker()


# Master data configuration
master_config = config["master_data"]

CUSTOMER_COUNT = master_config["customers"]
ACCOUNT_COUNT = master_config["accounts"]
BRANCH_COUNT = master_config["branches"]
MERCHANT_COUNT = master_config["merchants"]


CITIES = master_config["cities"]
CUSTOMER_SEGMENTS = master_config["customer_segments"]
KYC_STATUS = master_config["kyc_status"]
MERCHANT_CATEGORIES = master_config["merchant_categories"]

ACCOUNT_TYPES = master_config["account_types"]

BALANCE_MIN = master_config["balance"]["min"]
BALANCE_MAX = master_config["balance"]["max"]

CUSTOMER_CREATION_START = datetime.strptime(
    master_config["customer_creation"]["earliest_date"],
    "%Y-%m-%d"
).date()

CUSTOMER_CREATION_END = datetime.strptime(
    master_config["customer_creation"]["latest_date"],
    "%Y-%m-%d"
).date()

ACCOUNT_OPENING_START = datetime.strptime(
    master_config["account_opening"]["earliest_date"],
    "%Y-%m-%d"
).date()

ACCOUNT_OPENING_END = datetime.strptime(
    master_config["account_opening"]["latest_date"],
    "%Y-%m-%d"
).date()




def random_date(start_date, end_date):
    days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days))

### CUSTOMERS GENERATION FUNCTION
def generate_customers(count):

    customers = []

    for i in range(1, count + 1):

        customers.append({
            "customer_id": f"C{i:06d}",
            "name": fake.name(),
            "dob": fake.date_of_birth(
                minimum_age=18,
                maximum_age=80
            ),
            "city": random.choice(CITIES),
            "kyc_status": random.choice(KYC_STATUS),
            "created_date": random_date(
                CUSTOMER_CREATION_START,
                CUSTOMER_CREATION_END
            ),
            "segment": random.choice(CUSTOMER_SEGMENTS)
        })

    df = pd.DataFrame(customers)

    df.to_csv(
        DATA_DIR / "customers.csv",
        index=False
    )

    logger.info(
    "Customers created",
    extra={
        "channel": "master_data",
        "rows": len(df)
    }
)

### BRANCHES GENERATION FUNCTION
def generate_branches(count):

    branches = []

    for i in range(1, count + 1):

        city = random.choice(CITIES)

        branches.append({
            "branch_code": f"BR{i:04d}",
            "branch_name": f"{city} Branch {i}",
            "city": city,
            "ifsc": f"BANK{i:07d}"
        })

    df = pd.DataFrame(branches)

    df.to_csv(
        DATA_DIR / "branches.csv",
        index=False
    )

    logger.info(
        "Branches created",
        extra={
            "channel": "master_data",
            "rows": len(df)
        }
)

### MERCHANTS GENERATION FUNCTION
def generate_merchants(count):

    merchants = []

    for i in range(1, count + 1):

        city = random.choice(CITIES)

        merchants.append({
            "merchant_id": f"M{i:06d}",
            "merchant_name": fake.company(),
            "category": random.choice(MERCHANT_CATEGORIES),
            "city": city
        })

    df = pd.DataFrame(merchants)

    df.to_csv(
        DATA_DIR / "merchants.csv",
        index=False
    )

    logger.info(
        "Merchants created",
        extra={
            "channel": "master_data",
            "rows": len(df)
        }
)

### ACCOUNTS GENERATION FUNCTION
def generate_accounts(count, customers_file, branches_file):

    customers = pd.read_csv(customers_file)
    branches = pd.read_csv(branches_file)

    accounts = []

    for i in range(1, count + 1):

        customer = customers.sample(
            n=1,
            random_state=SEED + i
        ).iloc[0]

        branch = branches.sample(
            n=1,
            random_state=SEED + i
        ).iloc[0]

        account_type = random.choice(ACCOUNT_TYPES)

        balance = round(
            random.uniform(BALANCE_MIN, BALANCE_MAX),
            2
        )
        customer_created_date = pd.to_datetime(
            customer["created_date"]
        ).date()

        earliest_opening_date = max(
            customer_created_date,
            ACCOUNT_OPENING_START
        )

        opened_date = random_date(
            earliest_opening_date,
            ACCOUNT_OPENING_END
        )

        accounts.append({
            "account_number": f"{1000000000 + i}",
            "customer_id": customer["customer_id"],
            "account_type": account_type,
            "ifsc": branch["ifsc"],
            "branch_code": branch["branch_code"],
            "opened_date": opened_date,
            "balance": balance
        })

    df = pd.DataFrame(accounts)

    df.to_csv(
        DATA_DIR / "accounts.csv",
        index=False
    )

    logger.info(
        "Accounts created",
        extra={
            "channel": "master_data",
            "rows": len(df)
        }
)



if __name__ == "__main__":

    generate_customers(CUSTOMER_COUNT)
    generate_branches(BRANCH_COUNT)
    generate_merchants(MERCHANT_COUNT)
    generate_accounts(
        ACCOUNT_COUNT,
        DATA_DIR / "customers.csv",
        DATA_DIR / "branches.csv"
    )

    
    logger.info(
        "Master data generation completed",
        extra={
            "channel": "master_data"
        }
)
