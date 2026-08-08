# Day 6 Learning Log

## Purpose

Learn how to store cleaned tabular data in a relational database and answer analytical questions using SQL instead of pandas.

---

## Database

Database file:

`data/day06/healthcare_analytics.db`

SQLite version:

`3.51.0`

Tables:

* `heart_failure_records`
* `outcome_lookup`

Total records stored in the main table:

`299`

---

## Q1 — Total records

### SQL concept

* `SELECT`
* `COUNT`
* alias

### Query

```sql
SELECT
    COUNT(*) AS total_records
FROM heart_failure_records;
```

### Actual result

`299`

### Interpretation

The `heart_failure_records` table contains 299 records. This should match the number of rows in the cleaned Day 5 dataset, confirming that the cleaned CSV was loaded into SQLite without losing rows.

---

## Q2 — Death-event distribution

### SQL concept

* `GROUP BY`
* `COUNT`
* `ORDER BY`

### Query

```sql
SELECT
    death_event,
    COUNT(*) AS record_count
FROM heart_failure_records
GROUP BY death_event
ORDER BY death_event;
```

### Actual result

| death_event | record_count |
| ----------: | -----------: |
|           0 |          203 |
|           1 |           96 |

### Interpretation

There are two result rows because `death_event` contains two categories: `0` and `1`.

Of the 299 records:

* 203 have `death_event = 0`
* 96 have `death_event = 1`

The query describes the frequency distribution of the two outcome categories.

---

## Q3 — Mean age by death-event category

### SQL concept

* `GROUP BY`
* `COUNT`
* `AVG`
* `ROUND`

### Query

```sql
SELECT
    death_event,
    COUNT(*) AS record_count,
    ROUND(AVG(age), 2) AS mean_age
FROM heart_failure_records
GROUP BY death_event
ORDER BY death_event;
```

### Actual result

| death_event | record_count | mean_age |
| ----------: | -----------: | -------: |
|           0 |          203 |    58.76 |
|           1 |           96 |    65.22 |

### Interpretation

Records with `death_event = 0` had a mean age of 58.76 years, while records with `death_event = 1` had a mean age of 65.22 years.

`AVG(age)` calculates the mean age within each death-event group.

`ROUND(AVG(age), 2)` displays that mean to two decimal places.

This is a descriptive comparison and does not establish that age caused the recorded outcome.

---

## Q4 — Records aged 65 or above with diabetes recorded

### SQL concept

* `WHERE`
* `AND`
* `ORDER BY`
* `LIMIT`

### Query

```sql
SELECT
    age,
    diabetes,
    ejection_fraction,
    serum_creatinine,
    death_event
FROM heart_failure_records
WHERE age >= 65
  AND diabetes = 1
ORDER BY age DESC
LIMIT 10;
```

### Actual result

|  age | diabetes | ejection_fraction | serum_creatinine | death_event |
| ---: | -------: | ----------------: | ---------------: | ----------: |
| 94.0 |        1 |                38 |             1.83 |           1 |
| 90.0 |        1 |                50 |              1.0 |           1 |
| 82.0 |        1 |                30 |              1.2 |           1 |
| 82.0 |        1 |                50 |              1.0 |           1 |
| 80.0 |        1 |                38 |              1.9 |           1 |
| 80.0 |        1 |                38 |              1.3 |           1 |
| 80.0 |        1 |                35 |              2.1 |           0 |
| 75.0 |        1 |                30 |             1.83 |           1 |
| 75.0 |        1 |                38 |              0.6 |           0 |
| 75.0 |        1 |                60 |              1.4 |           0 |

### Interpretation

The query first selected records with:

* age greater than or equal to 65
* `diabetes = 1`

The filtered records were then sorted from highest age to lowest age, and only the first 10 records were returned.

These records should be described only as observations meeting the specified filtering conditions. They should not automatically be described as high-risk patients.

---

## Q5 — Five highest serum-creatinine observations

### SQL concept

* `SELECT`
* `ORDER BY`
* `DESC`
* `LIMIT`

### Query

```sql
SELECT
    age,
    serum_creatinine,
    serum_sodium,
    ejection_fraction,
    death_event
FROM heart_failure_records
ORDER BY serum_creatinine DESC
LIMIT 5;
```

### Actual result

|  age | serum_creatinine | serum_sodium | ejection_fraction | death_event |
| ---: | ---------------: | -----------: | ----------------: | ----------: |
| 80.0 |              9.4 |          133 |                35 |           1 |
| 54.0 |              9.0 |          137 |                70 |           1 |
| 60.0 |              6.8 |          146 |                62 |           1 |
| 60.0 |              6.1 |          131 |                45 |           0 |
| 58.0 |              5.8 |          134 |                38 |           1 |

### Interpretation

The query sorted all observations by `serum_creatinine` from highest to lowest and returned the first five.

The largest observed serum-creatinine value was 9.4, followed by 9.0, 6.8, 6.1, and 5.8.

These are simply the five observations with the largest serum-creatinine values in the dataset.

---

## Q6 — Group-level averages by death event

### SQL concept

* `GROUP BY`
* multiple aggregate functions
* aliases
* `COUNT`
* `AVG`
* `ROUND`

### Query

```sql
SELECT
    death_event,
    COUNT(*) AS n,
    ROUND(AVG(age), 2) AS mean_age,
    ROUND(AVG(ejection_fraction), 2) AS mean_ejection_fraction,
    ROUND(AVG(serum_creatinine), 2) AS mean_serum_creatinine,
    ROUND(AVG(serum_sodium), 2) AS mean_serum_sodium
FROM heart_failure_records
GROUP BY death_event
ORDER BY death_event;
```

### Actual result

| death_event |   n | mean_age | mean_ejection_fraction | mean_serum_creatinine | mean_serum_sodium |
| ----------: | --: | -------: | ---------------------: | --------------------: | ----------------: |
|           0 | 203 |    58.76 |                  40.27 |                  1.18 |            137.22 |
|           1 |  96 |    65.22 |                  33.47 |                  1.84 |            135.38 |

### Interpretation

The two death-event categories show different descriptive averages.

For `death_event = 0`:

* number of records = 203
* mean age = 58.76
* mean ejection fraction = 40.27
* mean serum creatinine = 1.18
* mean serum sodium = 137.22

For `death_event = 1`:

* number of records = 96
* mean age = 65.22
* mean ejection fraction = 33.47
* mean serum creatinine = 1.84
* mean serum sodium = 135.38

This SQL query performs the same general type of grouped descriptive analysis as a pandas `groupby().agg(...)` operation.

These are descriptive group differences and do not establish causation.

---

## Q7 — Diabetes and death-event distribution

### SQL concept

* multi-column `GROUP BY`
* `COUNT`
* `ORDER BY`

### Query

```sql
SELECT
    diabetes,
    death_event,
    COUNT(*) AS record_count
FROM heart_failure_records
GROUP BY
    diabetes,
    death_event
ORDER BY
    diabetes,
    death_event;
```

### Actual result

| diabetes | death_event | record_count |
| -------: | ----------: | -----------: |
|        0 |           0 |          118 |
|        0 |           1 |           56 |
|        1 |           0 |           85 |
|        1 |           1 |           40 |

### Interpretation

The query grouped the data using both `diabetes` and `death_event`.

The four observed combinations were:

* `diabetes = 0`, `death_event = 0`: 118 records
* `diabetes = 0`, `death_event = 1`: 56 records
* `diabetes = 1`, `death_event = 0`: 85 records
* `diabetes = 1`, `death_event = 1`: 40 records

The four group counts sum to 299, matching the total dataset size.

This demonstrates how SQL can group observations using more than one categorical variable.

---

## Q8 — JOIN with descriptive outcome labels

### SQL concept

* `INNER JOIN`
* table aliases
* `ON`
* `GROUP BY`

### Query

```sql
SELECT
    o.outcome_label,
    COUNT(*) AS record_count,
    ROUND(AVG(h.age), 2) AS mean_age
FROM heart_failure_records AS h
INNER JOIN outcome_lookup AS o
    ON h.death_event = o.death_event
GROUP BY o.outcome_label
ORDER BY o.outcome_label;
```

### Actual result

| outcome_label      | record_count | mean_age |
| ------------------ | -----------: | -------: |
| event_not_recorded |          203 |    58.76 |
| event_recorded     |           96 |    65.22 |

### Interpretation

The query joined two tables:

* `heart_failure_records`
* `outcome_lookup`

The aliases were:

* `h` = `heart_failure_records`
* `o` = `outcome_lookup`

The join condition was:

```sql
ON h.death_event = o.death_event
```

This means rows from the two tables were matched when their `death_event` values were equal.

`INNER JOIN` returned records for which a matching `death_event` existed in both tables.

The numeric values were therefore mapped to descriptive labels:

* `0` → `event_not_recorded`
* `1` → `event_recorded`

The resulting counts and mean ages remained consistent with the earlier grouped queries.

This demonstrates how a relational lookup table can add descriptive metadata to another table.

---

## Q9 — Records above the overall mean serum creatinine

### SQL concept

* subquery
* `AVG`
* `WHERE`
* `COUNT`

### Query

```sql
SELECT
    COUNT(*) AS records_above_mean_creatinine
FROM heart_failure_records
WHERE serum_creatinine >
    (
        SELECT AVG(serum_creatinine)
        FROM heart_failure_records
    );
```

### Actual result

`81`

### Interpretation

There are 81 records with serum-creatinine values greater than the overall mean serum-creatinine value of the dataset.

The inner query:

```sql
SELECT AVG(serum_creatinine)
FROM heart_failure_records
```

calculates the overall mean serum creatinine.

The outer query then uses that calculated value as the threshold in:

```sql
WHERE serum_creatinine > (...)
```

and counts how many observations exceed it.

This demonstrates how the output of one SQL query can be used inside another query.

---

## Q10 — Death-event counts below the overall mean ejection fraction

### SQL concept

* subquery
* `WHERE`
* `GROUP BY`
* `COUNT`
* `AVG`
* `ROUND`

### Query

```sql
SELECT
    death_event,
    COUNT(*) AS record_count,
    ROUND(AVG(ejection_fraction), 2) AS mean_ejection_fraction
FROM heart_failure_records
WHERE ejection_fraction <
    (
        SELECT AVG(ejection_fraction)
        FROM heart_failure_records
    )
GROUP BY death_event
ORDER BY death_event;
```

### Actual result

| death_event | record_count | mean_ejection_fraction |
| ----------: | -----------: | ---------------------: |
|           0 |          109 |                  32.63 |
|           1 |           73 |                  27.89 |

### Interpretation

The inner query calculated the overall mean ejection fraction.

The outer query selected only observations whose ejection fraction was below that overall dataset mean.

Among those observations:

* 109 had `death_event = 0`
* 73 had `death_event = 1`

The average ejection fraction within these filtered groups was:

* 32.63 for `death_event = 0`
* 27.89 for `death_event = 1`

A total of 182 observations were below the overall mean ejection fraction.

This is descriptive analysis only. The overall dataset mean should not be interpreted as a clinical threshold, and the results do not establish causation.

---

# SQL Concepts Practiced

During Day 6, I used:

* `SELECT`
* `FROM`
* `WHERE`
* `AND`
* `ORDER BY`
* `ASC`
* `DESC`
* `LIMIT`
* `COUNT`
* `AVG`
* `ROUND`
* `GROUP BY`
* aliases with `AS`
* multi-column grouping
* `INNER JOIN`
* `ON`
* table aliases
* scalar subqueries

---

# pandas vs SQL Connection

I learned that many operations performed with pandas have equivalent relational SQL concepts.

| pandas                       | SQL          |
| ---------------------------- | ------------ |
| DataFrame                    | Table        |
| DataFrame column             | Table column |
| DataFrame row                | Table row    |
| `df[["age"]]`                | `SELECT age` |
| Boolean filtering            | `WHERE`      |
| `.sort_values()`             | `ORDER BY`   |
| `.head()`                    | `LIMIT`      |
| `.mean()`                    | `AVG()`      |
| `.shape[0]`                  | `COUNT(*)`   |
| `.groupby()`                 | `GROUP BY`   |
| `.merge()`                   | `JOIN`       |
| nested filtering/calculation | subquery     |

---

# Verification

Main SQLite table row count:

`299`

Q2 group-count verification:

`203 + 96 = 299`

Q7 multi-group verification:

`118 + 56 + 85 + 40 = 299`

The grouped counts therefore agree with the total number of records in the SQLite table.

The JOIN results also preserved the same group counts:

* `event_not_recorded = 203`
* `event_recorded = 96`

This confirms that the lookup JOIN matched the two death-event categories as expected.

---

# Key Findings

1. The SQLite table contains 299 records.
2. `death_event = 0` contains 203 observations and `death_event = 1` contains 96 observations.
3. The mean age was 58.76 for `death_event = 0` and 65.22 for `death_event = 1`.
4. The `death_event = 1` group had a lower mean ejection fraction and higher mean serum creatinine than the `death_event = 0` group in this dataset.
5. There were 81 records with serum creatinine above the overall dataset mean.
6. There were 182 records with ejection fraction below the overall dataset mean.
7. SQL grouping results were internally consistent with the total dataset size.
8. The lookup-table JOIN correctly converted numeric outcome categories into descriptive labels.

---

# Limitations

The analyses performed today are descriptive.

They do not establish:

* causality
* clinical risk
* treatment recommendations
* diagnostic thresholds
* predictive performance

Filtering a group does not automatically make that group high risk.

Likewise, using a dataset mean as a SQL filtering threshold does not make that value a clinically validated threshold.

---

# Day 6 Reflection

Today I learned how to move cleaned tabular data from a CSV file into an SQLite relational database and analyze it using SQL.

I practiced selecting columns, filtering rows, sorting records, limiting results, calculating aggregate statistics, grouping records, joining related tables, and using subqueries.

I also learned that SQL and pandas can perform many comparable analytical operations, but SQL works directly with relational database tables.

The most important conceptual progression was:

```text
Cleaned Day 5 CSV
        ↓
SQLite database
        ↓
Relational tables
        ↓
SQL queries
        ↓
Verified analytical results
```

Day 6 established the database and SQL foundation needed for later work with larger relational systems, application backends, analytics pipelines, and machine-learning workflows.
