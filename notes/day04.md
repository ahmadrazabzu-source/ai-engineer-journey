# Day 4 Learning Log

## Purpose

Learn to build a reliable data-ingestion program that reads files, validates
structure and values, reports failures clearly, and produces a machine-readable
audit report.

## Concepts completed

- Path handling with `pathlib`
- File context managers
- CSV reading with `DictReader`
- JSON serialization
- Exceptions
- Custom exceptions
- Logging
- Docstrings
- Type hints
- Row-level validation
- File-level validation
- Failure testing

## Required-column validation

To verify that the CSV file contained all required headers, I converted the list of expected required columns into a `set` and subtracted the set of actual CSV header fieldnames extracted by `csv.DictReader`. 

$$\text{Missing Columns} = \text{Set}(\text{Required Columns}) - \text{Set}(\text{Actual Headers})$$

If the resulting set was non-empty, the loader raised a custom `MissingColumnsError` detailing every header that was missing.

## Row validation

Each row in `mixed_records.csv` was subjected to five column validation rules:

- **`record_id`**: Required field; cannot be empty or contain only whitespace.
- **`age`**: Required whole number (`int`). Must be an integer bounded between `0` and `120` inclusive.
- **`department`**: Required text field; cannot be empty after trimming whitespace.
- **`consent`**: Must be convertible to a boolean value (accepting values like `true`, `false`, `1`, `0`, `yes`, `no`).
- **`encounter_date`**: Must parse as a valid ISO-8601 date string (`YYYY-MM-DD`).

## Valid versus rejected rows

A bad individual row did not terminate the entire loader because row-level validation is wrapped inside a row-by-row `try/except` loop. When a specific row failed validation rules, the loader caught the validation error, logged a `WARNING` with the exact CSV line number and reason, appended the row details to a `rejected_records` list, and continued parsing the next row. This prevents bad data from crashing an entire batch job while still preserving data integrity.

## Exceptions

- **`FileNotFoundError`**: Triggered when attempting to load a non-existent CSV path (e.g., `does_not_exist.csv`).
- **`MissingColumnsError`**: Triggered when mandatory CSV headers (such as `department`) were missing from the header row.
- **`InvalidRecordError` / `ValueError`**: Triggered during row iteration when field values failed data-type parsing or boundary limits (e.g., age as a decimal, age outside `0–120`, or invalid consent string).

## Logging

- **`INFO`**: Used for normal, expected operational milestones (e.g., starting CSV load, successful completion summary counts).
- **`WARNING`**: Used for non-fatal row-level validation failures where a single record was rejected but overall batch processing continued.
- **`ERROR`**: Used for fatal, file-level execution failures (e.g., missing file or missing required header columns) that prematurely halted processing.

## JSON report

JSON is a lightweight, language-agnostic data format. Writing the ingestion results to `day04_load_report.json` allows downstream automated programs, web dashboards, or data pipelines to consume structured metadata (such as timestamps, input paths, total row counts, valid record lists, and error logs) without having to scrape unformatted log text.

## Failure test 1

- **Test Description**: Ingesting a non-existent file path (`...does_not_exist.csv`).
- **Observed Log Output**:
  ```text
  ERROR | Input file was not found: ...does_not_exist.csv
  PASS: missing-file failure test