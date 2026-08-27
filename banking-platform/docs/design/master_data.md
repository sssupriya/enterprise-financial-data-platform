# Banking Master Data Model

## 1. Customer

The customer table stores information about bank customers.

| Column | Type | Description | Example |
|---|---|---|---|
| customer_id | VARCHAR | Unique customer identifier | C000001 |
| name | VARCHAR | Customer full name | Amit Sharma |
| dob | DATE | Date of birth | 1992-05-10 |
| city | VARCHAR | Customer city | Bangalore |
| kyc_status | VARCHAR | KYC verification status | verified |
| created_date | DATE | Customer creation date | 2024-06-15 |
| segment | VARCHAR | Customer segment | salaried |

### Customer segments

- salaried
- self-employed
- student
- senior

---

## 2. Account

The account table stores bank accounts belonging to customers.

| Column | Type | Description | Example |
|---|---|---|---|
| account_number | VARCHAR | Unique account number | 1000000001 |
| customer_id | VARCHAR | Customer who owns the account | C000001 |
| account_type | VARCHAR | Type of bank account | savings |
| ifsc | VARCHAR | Branch IFSC code | BANK0001234 |
| branch_code | VARCHAR | Branch identifier | BR0001 |
| opened_date | DATE | Account opening date | 2024-07-01 |
| balance | DECIMAL | Current account balance | 45000.50 |

### Account types

- savings
- current

### Relationships

One customer can have multiple accounts.

Customer:

    customer_id
          |
          | 1
          |
          |------< Account
                    |
                    | many

---

## 3. Branch

The branch table stores bank branch information.

| Column | Type | Description | Example |
|---|---|---|---|
| branch_code | VARCHAR | Unique branch identifier | BR0001 |
| branch_name | VARCHAR | Branch name | Bangalore Main |
| city | VARCHAR | Branch city | Bangalore |
| ifsc | VARCHAR | Branch IFSC code | BANK0000001 |

There will be 50 branches.

---

## 4. Merchant

The merchant table stores businesses where customers can make transactions.

| Column | Type | Description | Example |
|---|---|---|---|
| merchant_id | VARCHAR | Unique merchant identifier | M000001 |
| merchant_name | VARCHAR | Merchant name | Fresh Mart |
| category | VARCHAR | Merchant category | grocery |
| city | VARCHAR | Merchant city | Bangalore |

### Merchant categories

- grocery
- fuel
- dining
- utilities
- jewellery
- pharmacy
- travel
- shopping

There will be 300 merchants.

---

# Entity Relationships

```text
                    CUSTOMER
                       |
                       | 1
                       |
                       | many
                    ACCOUNT
                       |
                       |
                       +-------- BRANCH


                    MERCHANT
                       |
                       |
                       | used by
                       |
                    TRANSACTION