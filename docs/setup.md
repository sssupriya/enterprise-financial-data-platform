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

py --version
py -m pip --version
py -m pip install faker pandas sqlalchemy psycopg2-binary

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