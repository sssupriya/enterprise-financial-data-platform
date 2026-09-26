import pandas as pd

from generators.upi import generate_upi_transactions, load_master_data

from generators.credit_card import (
    generate_credit_card_transactions,
    load_master_data as load_credit_card_master_data,
)

from generators.internet_banking import (
    generate_internet_transactions,
    load_master_data as load_internet_master_data,
)

from generators.branch import (
    generate_branch_transactions,
    load_master_data as load_branch_master_data,
)

## Test 1 — Mobile amounts positive
def test_mobile_amounts_positive():
    

    file = "data/mobile/2026-07-01.csv"

    df = pd.read_csv(file)

    assert (df["amount"] > 0).all(), "Some mobile transaction amounts are not positive"

##  Test 2 — Mobile transaction IDs are unique
def test_mobile_transaction_ids_are_unique():
    df = pd.read_csv("data/mobile/2026-07-01.csv")

    assert df["transaction_id"].is_unique, "Some mobile transaction IDs are not unique"

###  Test 3 — Mobile timestamps match requested date    
def test_mobile_timestamps_match_requested_date():
    df = pd.read_csv("data/mobile/2026-07-01.csv")

    timestamps = pd.to_datetime(df["timestamp"])

    assert (timestamps.dt.date == pd.Timestamp("2026-07-01").date()).all(), "Some mobile transaction timestamps do not match the requested date"

###  Test 4 — Mobile required columns   
def test_mobile_required_columns():
    df = pd.read_csv("data/mobile/2026-07-01.csv")

    expected_columns = {
        "transaction_id",
        "customer_id",
        "account_number",
        "amount",
        "merchant",
        "device_id",
        "gps_city",
        "timestamp",
        "status"
    }

    assert expected_columns.issubset(df.columns), "Some required columns are missing from the mobile data"

##  Test 5 — ATM withdrawal amounts are multiples of 100
def test_atm_withdrawals_are_multiples_of_100():
    df = pd.read_csv("data/atm/atm_transactions.csv")

    assert (df["withdrawal_amount"] % 100 == 0).all()

##  Test 6 — ATM pin attempts are valid
def test_atm_pin_attempts_are_valid():
    df = pd.read_csv("data/atm/atm_transactions.csv")

    assert df["pin_attempts"].isin([1, 2, 3]).all()

###  Test 7 — UPI transaction IDs are unique
def test_upi_required_columns():
    customers, accounts, merchants = load_master_data()

    df = generate_upi_transactions(
        100,
        "2026-07-01",
        customers,
        accounts,
        merchants
    )

    required_columns = {
        "transaction_id",
        "customer_id",
        "account_number",
        "amount",
        "timestamp",
        "status",
        "upi_handle",
        "vpa",
        "merchant",
        "device",
        "counterparty_bank",
    }

    assert required_columns.issubset(df.columns)


def test_upi_amounts_positive():
    customers, accounts, merchants = load_master_data()

    df = generate_upi_transactions(
        100,
        "2026-07-01",
        customers,
        accounts,
        merchants
    )

    assert (df["amount"] > 0).all()

###  Test 8 — UPI transaction IDs are unique
def test_upi_transaction_ids_unique():
    customers, accounts, merchants = load_master_data()

    df = generate_upi_transactions(
        100,
        "2026-07-01",
        customers,
        accounts,
        merchants
    )

    assert df["transaction_id"].is_unique

###  Test 9 — Credit card transaction IDs are unique
def test_credit_card_required_columns():
    customers, merchants = load_credit_card_master_data()

    df = generate_credit_card_transactions(
        100,
        "2026-07-01",
        customers,
        merchants
    )

    required_columns = {
        "transaction_id",
        "customer_id",
        "amount",
        "timestamp",
        "status",
        "merchant",
        "merchant_category",
        "terminal_id",
        "card_type",
        "credit_limit",
        "reward_points",
    }

    assert required_columns.issubset(df.columns)

def test_credit_card_amounts_positive():
    customers, merchants = load_credit_card_master_data()

    df = generate_credit_card_transactions(
        100,
        "2026-07-01",
        customers,
        merchants
    )

    assert (df["amount"] > 0).all()

def test_credit_card_types_valid():
    customers, merchants = load_credit_card_master_data()

    df = generate_credit_card_transactions(
        100,
        "2026-07-01",
        customers,
        merchants
    )

    valid_card_types = {
        "VISA",
        "MASTERCARD",
        "RUPAY",
    }

    assert df["card_type"].isin(valid_card_types).all()

def test_credit_card_reward_points_non_negative():
    customers, merchants = load_credit_card_master_data()

    df = generate_credit_card_transactions(
        100,
        "2026-07-01",
        customers,
        merchants
    )

    assert (df["reward_points"] >= 0).all()

###  Test 10 — Internet banking required columns
def test_internet_banking_required_columns():
    customers, accounts = load_internet_master_data()

    df = generate_internet_transactions(
        100,
        "2026-07-01",
        customers,
        accounts
    )

    required_columns = {
        "transaction_id",
        "customer_id",
        "account_number",
        "amount",
        "timestamp",
        "status",
        "browser",
        "ip",
        "os",
        "login_time",
        "beneficiary",
        "beneficiary_type",
    }

    assert required_columns.issubset(df.columns)

def test_internet_banking_amounts_positive():
    customers, accounts = load_internet_master_data()

    df = generate_internet_transactions(
        100,
        "2026-07-01",
        customers,
        accounts
    )

    assert (df["amount"] > 0).all()

def test_internet_banking_beneficiary_types_valid():
    customers, accounts = load_internet_master_data()

    df = generate_internet_transactions(
        100,
        "2026-07-01",
        customers,
        accounts
    )

    valid_types = {
        "NEW",
        "EXISTING",
    }

    assert df["beneficiary_type"].isin(valid_types).all()

def test_internet_banking_new_beneficiary_has_large_transfer():
    customers, accounts = load_internet_master_data()

    df = generate_internet_transactions(
        1000,
        "2026-07-01",
        customers,
        accounts
    )

    new_beneficiary_transactions = df[
        df["beneficiary_type"] == "NEW"
    ]

    assert not new_beneficiary_transactions.empty

    assert (
        new_beneficiary_transactions["amount"] >= 50000
    ).all()

### test-11 branch required column 
def test_branch_required_columns():
    customers, accounts, branches = load_branch_master_data()

    df = generate_branch_transactions(
        100,
        "2026-07-01",
        customers,
        accounts,
        branches
    )

    required_columns = {
        "transaction_id",
        "customer_id",
        "account_number",
        "branch_code",
        "teller_id",
        "transaction_type",
        "cash_deposit",
        "cheque_number",
        "timestamp",
        "status",
    }

    assert required_columns.issubset(df.columns)


def test_branch_transaction_types_valid():
    customers, accounts, branches = load_branch_master_data()

    df = generate_branch_transactions(
        100,
        "2026-07-01",
        customers,
        accounts,
        branches
    )

    valid_types = {
        "CASH_DEPOSIT",
        "CHEQUE_DEPOSIT",
    }

    assert df["transaction_type"].isin(valid_types).all()


def test_branch_transactions_within_business_hours():
    customers, accounts, branches = load_branch_master_data()

    df = generate_branch_transactions(
        100,
        "2026-07-01",
        customers,
        accounts,
        branches
    )

    timestamps = pd.to_datetime(df["timestamp"])

    assert (timestamps.dt.hour >= 9).all()
    assert (timestamps.dt.hour < 17).all()


def test_branch_deposit_rules():
    customers, accounts, branches = load_branch_master_data()

    df = generate_branch_transactions(
        500,
        "2026-07-01",
        customers,
        accounts,
        branches
    )

    cash_transactions = df[
        df["transaction_type"] == "CASH_DEPOSIT"
    ]

    cheque_transactions = df[
        df["transaction_type"] == "CHEQUE_DEPOSIT"
    ]

    assert not cash_transactions.empty
    assert not cheque_transactions.empty

    assert (cash_transactions["cash_deposit"] > 0).all()

    assert (cheque_transactions["cash_deposit"] == 0).all()

    assert (
        cheque_transactions["cheque_number"]
        .astype(str)
        .str.len()
        .gt(0)
        .all()
    )