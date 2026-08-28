import pandas as pd

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