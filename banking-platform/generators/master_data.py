# print("MASTER DATA SCRIPT1 STARTED")
# print("MASTER DATA SCRIPT2 STARTED")

from faker import Faker
import pandas as pd
import random
import yaml
from datetime import datetime, timedelta
from pathlib import Path


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
BRANCH_COUNT = master_config["branches"]
MERCHANT_COUNT = master_config["merchants"]

CITIES = master_config["cities"]
CUSTOMER_SEGMENTS = master_config["customer_segments"]
KYC_STATUS = master_config["kyc_status"]
MERCHANT_CATEGORIES = master_config["merchant_categories"]




def random_date(start_date, end_date):
    days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, days))


def generate_customers(count=5000):

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
                datetime(2020, 1, 1),
                datetime(2026, 7, 1)
            ).date(),
            "segment": random.choice(CUSTOMER_SEGMENTS)
        })

    df = pd.DataFrame(customers)

    df.to_csv(
        DATA_DIR / "customers.csv",
        index=False
    )

    print(f"Created {len(df)} customers")


def generate_branches(count=50):

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

    print(f"Created {len(df)} branches")


def generate_merchants(count=300):

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

    print(f"Created {len(df)} merchants")


if __name__ == "__main__":

    generate_customers(CUSTOMER_COUNT)
    generate_branches(BRANCH_COUNT)
    generate_merchants(MERCHANT_COUNT)

    print("Master data generation completed.")
