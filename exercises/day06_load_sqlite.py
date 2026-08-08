"""Load the cleaned Day 5 dataset into SQLite for SQL practice."""

### Step 1 — Imports

import sqlite3
from pathlib import Path

import pandas as pd


### Step 2 — Define paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_PATH = (
    PROJECT_ROOT
    / "data"
    / "day05"
    / "processed"
    / "heart_failure_cleaned.csv"
)


DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "day06"
    / "healthcare_analytics.db"
)

### Step 3 — Load the cleaned dataset
df = pd.read_csv(CSV_PATH)

print("CSV shape:", df.shape)
print(df.columns.tolist())

### Step 4 — Connect to SQLite
connection = sqlite3.connect(DATABASE_PATH)

### Step 5 — Load the dataset/dataframe into SQLite
df.to_sql(
    name="heart_failure_records",
    con=connection,
    if_exists="replace",
    index=False,
)

### Step 6 — Create the lookup table
# This gives you second table for JOIN.
connection.execute(
    """
    CREATE TABLE IF NOT EXISTS outcome_lookup (
        death_event INTEGER PRIMARY KEY,
        outcome_label TEXT NOT NULL
    )
    """
)

# Then clean its current contents:
connection.execute(
    "DELETE FROM outcome_lookup"
)

# Insert:
connection.executemany(
    """
    INSERT INTO outcome_lookup (
        death_event,
        outcome_label
    )
    VALUES (?, ?)
    """,
    [
        (0, "event_not_recorded"),
        (1, "event_recorded"),
    ],
)

# Commit:
connection.commit()

# close
connection.close()

### Step 7 — Verify the database programmatically
connection = sqlite3.connect(DATABASE_PATH)

row_count = connection.execute(
    """
    SELECT COUNT(*)
    FROM heart_failure_records
    """
).fetchone()[0]

print("Rows in SQLite:", row_count)

connection.close()

# Add an assertion to verify that the number of rows in the SQLite table matches the number of rows in the original DataFrame
assert row_count == len(df)