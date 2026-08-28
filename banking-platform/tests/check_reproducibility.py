##  Test if mobile transaction generation is reproducible
def test_mobile_generation_is_reproducible():
    from generators.mobile import (
        load_master_data,
        generate_transactions
    )
    from datetime import datetime

    customers, accounts, merchants = load_master_data()

    test_date = datetime.strptime(
        "2026-07-10",
        "%Y-%m-%d"
    ).date()

    df1 = generate_transactions(
        10,
        test_date,
        customers,
        accounts,
        merchants
    )

    # Reset the random seed
    import random
    from faker import Faker

    random.seed(42)
    Faker.seed(42)

    df2 = generate_transactions(
        10,
        test_date,
        customers,
        accounts,
        merchants
    )

    assert df1.equals(df2)