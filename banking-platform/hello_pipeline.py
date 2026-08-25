import pandas as pd
from sqlalchemy import create_engine

# Read the CSV
df = pd.read_csv("customers.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Remove rows where email is missing
df = df.dropna(subset=["email"])

print("Rows to load:", len(df))
print(df.head())

# PostgreSQL connection
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5450/fincore_dev"

engine = create_engine(DATABASE_URL)

# Load into raw.customers
df.to_sql(
    "customers",
    engine,
    schema="raw",
    if_exists="replace",
    index=False
)

print("Data loaded successfully!")