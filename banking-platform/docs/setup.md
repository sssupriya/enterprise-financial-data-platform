# Machine Setup
Install Python 3.11 (python.org), Git, and VS Code with the Python and GitLens extensions.
Install Docker Desktop and verify with: docker run hello-world.
Install DBeaver (free database GUI) and Power BI Desktop.
Create a GitHub account (if needed) and set up SSH keys.

# Create the mono-repo that will hold the whole platform.
Repo name: enterprise-financial-data-platform.
Create folders: banking-platform/, markets-platform/, shared/, docs/, infra/.
Add a root README.md with one paragraph describing the platform (copy from the Overview doc).
Add .gitignore (Python template) and commit: 'chore: initial repo structure'.

# Run PostgreSQL in Docker — this is the warehouse for the whole program.
docker run --name fincore_db -e POSTGRES_PASSWORD=fincore -p 5450:5432 -d postgres:16
Connect with DBeaver, create database fincore_dev.

- py --version
- py -m pip --version
- py -m pip install faker pandas sqlalchemy psycopg2-binary
- py -m pip install pytest
- py -m pytest --version

# My first ETL pipeline:
customers.csv
     ↓
   pandas
     ↓
clean column names
     ↓
remove missing emails
     ↓
 SQLAlchemy
     ↓
PostgreSQL: fincore_dev
     ↓
raw.customers
     ↓
SELECT COUNT(*)
     ↓
100


### I created 100 fake customer records using Faker, read the CSV with pandas, cleaned the column names, removed records with missing emails, and loaded the cleaned data into the raw.customers PostgreSQL table using SQLAlchemy. I verified the load in DBeaver with SELECT COUNT(*) FROM raw.customers, which returned 100.

# All customer Data using SQL
    SELECT *
    FROM raw.customers
    LIMIT 10;


### 27-08-2026 I ran those commands for actual Syenthetic banking data designing
py -m pip install faker pandas pyyaml pytest sqlalchemy psycopg2-binary
py  generators/master_data.py   
py -c "from faker import Faker; print('Faker is working')"
py -c "import pandas as pd; print(pd.read_csv('data/customers.csv').shape); print(pd.read_csv('data/branches.csv').shape); print(pd.read_csv('data/merchants.csv').shape)"
py -c "import pandas as pd; df=pd.read_csv('data/accounts.csv'); print(df.shape); print(df.head())"

banking-platform/
│
├── data/
│   ├── customers.csv       ✅ 5,000
│   ├── branches.csv        ✅ 50
│   └── merchants.csv       ✅ 300
│
├── docs/
│   └── design/
│       └── master-data.md  ✅
│
├── generators/
│   └── master_data.py      ✅
│
├── config/
├── tests/
├── README.md
├── requirements.txt
└── .gitignore


## Master Data part is working:

✅ master-data.md
✅ master_data.py
✅ generator_config.yaml
✅ Faker
✅ PyYAML
✅ 5,000 customers
✅ 50 branches
✅ 300 merchants
✅ Seed = 42


## Accounts:
5,000 customers
       ↓
   7,000 accounts
       ↓
customer_id links accounts to customers
       ↓
branch_code links accounts to branches

# Very important validation:
## Make sure every account belongs to a real customer
- py -c "import pandas as pd; a=pd.read_csv('data/accounts.csv'); c=pd.read_csv('data/customers.csv'); print(a['customer_id'].isin(c['customer_id']).all())"

## check branches
- py -c "import pandas as pd; a=pd.read_csv('data/accounts.csv'); b=pd.read_csv('data/branches.csv'); print(a['branch_code'].isin(b['branch_code']).all())"

## check duplicate account numbers
- py -c "import pandas as pd; a=pd.read_csv('data/accounts.csv'); print(a['account_number'].is_unique)"

## Verify all 4 CSVs
- py -c "import pandas as pd; print('Customers:', len(pd.read_csv('data/customers.csv'))); print('Accounts:', len(pd.read_csv('data/accounts.csv'))); print('Branches:', len(pd.read_csv('data/branches.csv'))); print('Merchants:', len(pd.read_csv('data/merchants.csv')))"



# 28-08-2026

### 🎯 Our implementation plan

#### We'll do Mobile in small pieces, just like Master Data:

* Part 1 — Configuration

- generator_config.yaml

⬇️

* Part 2 — Command-line arguments
- py -m generators.mobile --date 2026-07-01 --count 20000

⬇️

* Part 3 — Load master CSVs
- customers
- accounts
- merchants

⬇️

* Part 4 — Generate timestamps

- Evening/weekend patterns.

⬇️

* Part 5 — Generate transaction types

- Salary / EMI / Utility / Normal.

⬇️

* Part 6 — Generate amounts

- 70% small transactions.

⬇️

* Part 7 — Generate IDs and status

⬇️

* Part 8 — Save CSV
data/mobile/2026-07-01.csv

⬇️

* Part 9 — Test
- pytest -v


## 🚀 Mobile Banking Generator
- generators/mobile.py
     - transaction_id
     - customer_id
     - account_number
     - amount
     - merchant
     - device_id
     - gps_city
     - timestamp
     - status
     
## Final output Look like:
Mobile Generator
│
├── Command line arguments       ✅
├── Load customers               ✅
├── Load accounts                ✅
├── Load merchants               ✅
├── Requested date               ✅
├── Requested count              ✅
├── Evening activity             ✅
└── Weekend activity             ✅


## Transaction type/business pattern.

### We need to handle:

- 1st of month → salary credits
- 5th → EMI debits
- 15th–20th → utility bills
- Other dates → normal transactions

## Amount generation 
### 70% of transactions should be small amounts: ₹100–₹2,000.

## What we've completed in mobile.py
Command-line arguments          ✅
Load customers/accounts         ✅
Load merchants                  ✅
Date-specific generation        ✅
Evening timestamps              ✅
Weekend behavior                ✅
Salary pattern                  ✅
EMI pattern                     ✅
Utility pattern                 ✅
Amount generation               ✅
YAML configuration              ✅
Status generation               ✅
Device ID generation            ✅
Utility → utility merchant      ✅
CSV output                      ✅

##### I weighted the hourly distribution so that transaction activity peaks around 6 PM–9 PM, which creates a realistic evening-heavy mobile banking pattern.

## ATM generator
✅ ATM generator is working.

- Sample satisfies the main requirements:

- atm_id → ✅ generated
- withdrawal_amount → ✅ multiples of ₹100
- balance_after → ✅ calculated
- city → ✅ from configured cities
- pin_attempts → ✅ includes 3 occasionally
- atm_health → ✅ HEALTHY / DEGRADED
- CSV → ✅ generated

## 🎉 6/6 pytest tests passed. This is a major milestone for your assignment.
### output means:

- Mobile amount positive          ✅
- Transaction IDs unique          ✅
- Timestamps correct              ✅
- Required columns present        ✅
- ATM amounts multiple of ₹100    ✅
- PIN attempts valid              ✅

## Createated generate_day.py for One command generates a full day of Mobile + ATM data.


<!-- 
⚠️ One important thing

The ATM data itself currently doesn't use the date. That's okay for the moment because the assignment mainly requires the ATM generator and date-runnable pipeline. We can add an ATM timestamp later if we decide it's useful. -->

#### "I created a parameterized full-day generator. I can generate Mobile and ATM banking data for any business date with one command."