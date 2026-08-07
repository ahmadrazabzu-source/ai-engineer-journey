# Day 5 Learning Log

## Purpose

Learn how an AI engineer takes a raw tabular dataset, inspects its quality,
cleans it reproducibly, analyzes it using NumPy/pandas, and produces evidence
that downstream ML can safely consume.

## Dataset

Heart Failure Clinical Records — UCI Machine Learning Repository.

## Dataset shape

Rows: 299
Columns: 13

## NumPy concepts learned

- ndarray: Contiguous N-dimensional array object used for high-performance vector math.
- shape: Tuple representing the dimensions of an array (e.g., `(299,)`).
- dtype: The underlying memory data type of array elements (e.g., `float64`, `int64`).
- indexing: Accessing specific elements by zero-based integer index.
- slicing: Extracting subarrays using range notation `[start:stop:step]`.
- boolean masking: Filtering elements based on conditional truth arrays (e.g., `arr[arr > 60]`).
- vectorization: Executing element-wise mathematical operations across entire arrays without Python for-loops.
- mean: `np.mean()` — calculating the arithmetic average.
- median: `np.median()` — finding the 50th percentile robust to extreme outliers.
- standard deviation: `np.std()` — measuring spread around the mean.
- percentiles: `np.percentile()` — computing arbitrary distribution thresholds (25th, 50th, 75th).
- NaN: `np.nan` — representing missing or IEEE floating-point undefined numerical values.

## pandas concepts learned

- Series: 1D labeled array capable of holding any data type.
- DataFrame: 2D tabular data structure with labeled axes (rows and columns).
- read_csv: Ingesting delimiter-separated text files into memory as DataFrames.
- head: Previewing the first $N$ rows (default 5).
- tail: Previewing the last $N$ rows to check for tail truncation or corruption.
- info: Outputting concise structural summary (dtypes, non-null counts, memory usage).
- describe: Generating five-number summary statistics for numerical columns.
- loc: Label-based indexing for selecting rows/columns by names.
- iloc: Integer-position based indexing for selecting rows/columns by position.
- isna: Detecting missing/NaN elements across Series or DataFrames.
- duplicated: Identifying duplicate rows across the entire dataset.
- value_counts: Computing frequency distributions for categorical or discrete features.
- groupby: Splitting data into groups based on criteria for aggregation.
- agg: Applying multiple statistical aggregation functions across grouped axes.
- merge: Relational join operations between two DataFrames based on keys.
- to_csv: Exporting in-memory DataFrames back to CSV format on disk.

## Missing-value audit

The missing-value audit using `df.isna().sum()` revealed **0 missing values** across all 13 columns. The original UCI dataset arrived 100% complete.

## Duplicate audit

The duplicate-row audit using `df.duplicated().sum()` revealed **0 duplicate rows**. Every patient record in the dataset is unique.

## Cleaning decisions

1. **Explicit Defensive Copying:** Created `clean_df = df.copy()` to preserve raw input data and prevent silent mutation errors.
2. **Column Header Standardization:** Normalized all column names using `clean_df.columns.str.strip().str.lower()`. This converted uppercase target names (e.g., `DEATH_EVENT` → `death_event`) and stripped whitespace to make programmatic column selection robust and predictable.
3. **Preservation of Clinical Ranges:** No extreme values (e.g., high `serum_creatinine` or low `ejection_fraction`) were removed or capped, as domain context confirms these represent valid clinical extremes rather than measurement errors.

## GroupBy analysis

Grouped the dataset by the target variable `death_event` (0 = Survived, 1 = Deceased) and computed aggregate statistics using `.agg()`:
- **`record_count`**: Total patient count per outcome (`size`).
- **`mean_age`**: Average age per group (`mean`).
- **`median_ejection_fraction`**: Median heart pump efficiency percentage (`median`).
- **`mean_serum_creatinine`**: Average kidney efficiency marker level (`mean`).
- **`median_followup_days`**: Median observation period in days (`median`).

*Key Outcome:* Deceased patients (`death_event = 1`) exhibited higher mean age, higher serum creatinine levels, lower ejection fraction, and significantly shorter follow-up time (`time`).

## Merge

- **Left DataFrame:** `numeric_summary` (Transposed `describe()` output containing feature summary statistics, key = `feature`).
- **Right DataFrame:** `feature_dictionary` (External metadata CSV defining feature categories like `demographic`, `laboratory`, `measurement`, key = `feature`).
- **Merge Key:** `feature`
- **Join Type:** `left` (Ensured all original dataset features were retained regardless of match status).

## Cleaned CSV

- **Output Path:** `data/day05/processed/heart_failure_cleaned.csv`
- **Dimensions:** 299 rows × 13 columns

## Cleaned schema

The schema files (`day05_cleaned_schema.csv` and `day05_cleaned_schema.json`) act as explicit contracts for downstream data consumers. They contain:
- Column names
- Extracted data types (`dtypes`)
- Nullability status (`is_nullable` / `missing_count`)
- Unique value counts (`unique_count`)
- Expected min and max value boundaries (`min_val`, `max_val`)

## Real error encountered

`FileNotFoundError` when executing file output operations from inside the Jupyter Notebook.

## Root cause

Jupyter Lab was launched from the `notebooks/day05` directory rather than the repository root (`ai-engineer-journey`), causing relative path operations like `data/day05/processed` to resolve against the wrong parent folder.

## Fix

Implemented dynamic path resolution using `pathlib.Path.cwd()` and conditional traversal logic to identify `PROJECT_ROOT`, combined with `.mkdir(parents=True, exist_ok=True)` to guarantee directory existence prior to file writes.

## One thing I still find confusing

How to systematically establish threshold rules for when an extreme numerical value should be treated as a valid clinical outlier vs. when it should be clipped/capped for machine learning models without introducing domain bias.

## Next smallest action

Day 6: load cleaned data into SQLite and answer analytical questions with SQL.