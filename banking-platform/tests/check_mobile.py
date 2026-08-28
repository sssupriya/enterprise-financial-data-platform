import pandas as pd

file = "data/mobile/2026-07-01.csv"

df = pd.read_csv(file)

print("Total transactions:", len(df))

print("\nTransaction status:")
print(df["status"].value_counts())

print("\nTransaction amount statistics:")
print(df["amount"].describe())

print("\nTransactions by hour:")
df["timestamp"] = pd.to_datetime(df["timestamp"])
print(df["timestamp"].dt.hour.value_counts().sort_index())

print("\nSalary credits:")
print((df["amount"] >= 25000).sum())