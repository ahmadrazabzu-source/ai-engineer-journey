"""Validate synthetic CSV records and write a JSON ingestion report.

This educational program contains no real patient information and must not be used for clinical decisions.
"""

import csv
import json
import logging
from pathlib import Path
from typing import Any

# Initialize a module-level logger named after the current file ('exercises.day04').
logger = logging.getLogger(__name__)

# Type aliases for enhanced code readability
Record = dict[str, Any]       # Represents a clean, validated dictionary record
RejectedRow = dict[str, Any]  # Represents a dictionary containing line-level error details

# Immutable tuple of mandatory CSV headers.
REQUIRED_COLUMNS = (
    "record_id",
    "age",
    "department",
    "consent_confirmed",
    "completed_visits",
)

# Project Pathing Configuration
# Locates project root dynamically (handles script execution AND interactive REPL)
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    # Fallback for interactive Python REPL where __file__ is undefined
    SCRIPT_DIR = Path.cwd()

PROJECT_ROOT = SCRIPT_DIR.parent if SCRIPT_DIR.name == "exercises" else SCRIPT_DIR

# Dedicated Day 04 Output Directory
DAY04_OUTPUT_DIR = PROJECT_ROOT / "output" / "day04"

# Input / Output File Targets
DEFAULT_INPUT_PATH = PROJECT_ROOT / "data" / "day04" / "mixed_records.csv"
DEFAULT_REPORT_PATH = DAY04_OUTPUT_DIR / "day04_load_report.json"
DEFAULT_LOG_PATH = DAY04_OUTPUT_DIR / "day04_loader.log"


# Custom Exceptions
class CSVLoaderError(Exception):
    """Base exception for general CSV ingestion failures."""


class CSVSchemaError(CSVLoaderError):
    """Raised when required CSV columns are missing or structural header errors occur."""


def configure_logging(log_path: Path) -> None:
    """Configure dual logging: outputs formatted events to both terminal and output/day04/day04_loader.log."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),                         # Console output
            logging.FileHandler(log_path, encoding="utf-8"), # Log file
        ],
    )


def validate_required_columns(
    fieldnames: list[str] | None,
    required_columns: tuple[str, ...],
) -> None:
    """Check whether the CSV file header contains all mandatory columns."""
    if fieldnames is None:
        raise CSVSchemaError("CSV file is completely empty or missing a header row.")

    available_columns = set(fieldnames)
    required_set = set(required_columns)
    
    missing = required_set - available_columns

    if missing:
        missing_str = ", ".join(sorted(missing))
        raise CSVSchemaError(f"Missing required columns: {missing_str}")


def parse_consent(value: str) -> bool:
    """Normalize user text inputs into standard Boolean values (True / False)."""
    cleaned = value.strip().lower()
    
    if cleaned in ("yes", "y", "true", "1"):
        return True
    if cleaned in ("no", "n", "false", "0"):
        return False
        
    raise ValueError(f"Invalid consent value: '{value}'")


def validate_row(
    raw_row: dict[str, str],
    csv_line_number: int,
) -> tuple[Record | None, RejectedRow | None]:
    """Validate and clean a single raw CSV row against domain business rules."""
    errors: list[str] = []
    
    raw_id = raw_row.get("record_id", "").strip()
    raw_age = raw_row.get("age", "").strip()
    raw_dept = raw_row.get("department", "").strip()
    raw_consent = raw_row.get("consent_confirmed", "").strip()
    raw_visits = raw_row.get("completed_visits", "").strip()

    # Rule 1: Validate Record ID
    if not raw_id:
        errors.append("record_id is required")
    elif not raw_id.upper().startswith("SYN-"):
        errors.append("record_id must begin with SYN-")

    # Rule 2: Validate Age
    parsed_age = None
    if not raw_age:
        errors.append("age is required")
    else:
        try:
            parsed_age = int(raw_age)
            if not (0 <= parsed_age <= 120):
                errors.append("age must be between 0 and 120")
        except ValueError:
            errors.append("age must be a whole number")

    # Rule 3: Validate Department
    if not raw_dept:
        errors.append("department is required")

    # Rule 4: Validate Consent
    parsed_consent = None
    try:
        parsed_consent = parse_consent(raw_consent)
    except ValueError:
        errors.append("consent_confirmed must be yes/no or true/false")

    # Rule 5: Validate Completed Visits
    parsed_visits = None
    try:
        parsed_visits = int(raw_visits)
        if parsed_visits < 0:
            errors.append("completed_visits cannot be negative")
    except ValueError:
        errors.append("completed_visits must be a whole number")

    if errors:
        rejected_report: RejectedRow = {
            "csv_line_number": csv_line_number,
            "record_id": raw_id if raw_id else None,
            "errors": errors,
        }
        return None, rejected_report

    cleaned_record: Record = {
        "record_id": raw_id.upper(),
        "age": parsed_age,
        "department": raw_dept.title(),
        "consent_confirmed": parsed_consent,
        "completed_visits": parsed_visits,
    }
    return cleaned_record, None


def load_csv_records(
    csv_path: Path,
) -> tuple[list[Record], list[RejectedRow]]:
    """Stream a CSV file, validate individual records, and separate valid rows from rejections."""
    logger.info("Starting ingestion for file: %s", csv_path)

    valid_records: list[Record] = []
    rejected_rows: list[RejectedRow] = []

    try:
        with csv_path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            
            validate_required_columns(reader.fieldnames, REQUIRED_COLUMNS) # type: ignore

            for line_number, raw_row in enumerate(reader, start=2):
                record, rejection = validate_row(raw_row, line_number)
                
                if record:
                    valid_records.append(record)
                elif rejection:
                    rejected_rows.append(rejection)
                    logger.warning(
                        "Line %d rejected (Record ID: %s): %s",
                        line_number,
                        rejection["record_id"],
                        ", ".join(rejection["errors"]),
                    )

    except FileNotFoundError:
        logger.exception("Input file was not found: %s", csv_path)
        raise
    except PermissionError:
        logger.exception("Permission denied: %s", csv_path)
        raise
    except UnicodeDecodeError as error:
        logger.exception("Input file is not valid UTF-8: %s", csv_path)
        raise CSVLoaderError("Unable to decode CSV as UTF-8") from error
    except csv.Error as error:
        logger.exception("CSV parsing failed: %s", csv_path)
        raise CSVLoaderError("Invalid CSV structure") from error

    logger.info(
        "Ingestion complete. Total processed: %d | Valid: %d | Rejected: %d",
        len(valid_records) + len(rejected_rows),
        len(valid_records),
        len(rejected_rows),
    )

    return valid_records, rejected_rows


def build_load_report(
    input_path: Path,
    valid_records: list[Record],
    rejected_rows: list[RejectedRow],
) -> dict[str, Any]:
    """Build a structured dictionary summarizing ingestion results for export to JSON."""
    total_rows = len(valid_records) + len(rejected_rows)
    
    if len(valid_records) == 0 and total_rows > 0:
        status = "failed_validation"
    elif len(rejected_rows) > 0:
        status = "completed_with_rejections"
    else:
        status = "completed"

    return {
        "input_file": input_path.name,
        "total_rows": total_rows,
        "valid_row_count": len(valid_records),
        "rejected_row_count": len(rejected_rows),
        "status": status,
        "valid_records": valid_records,
        "rejected_rows": rejected_rows,
    }


def write_json_report(
    report: dict[str, Any],
    output_path: Path,
) -> None:
    """Save the report dictionary to a human-readable, indented JSON file in output/day04/."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(report, json_file, indent=2)
        
    logger.info("JSON ingestion report saved to: %s", output_path)


def run_loader(
    input_path: Path,
    report_path: Path,
) -> int:
    """Execute loader pipeline and return exit code (0=Success, 1=Missing File, 2=Schema Error, 3=Parsing Error)."""
    try:
        valid_records, rejected_rows = load_csv_records(input_path)
    except FileNotFoundError:
        logger.error("Input file not found: %s", input_path)
        return 1
    except CSVSchemaError as error:
        logger.error("CSV schema error: %s", error)
        return 2
    except CSVLoaderError as error:
        logger.error("CSV loading failed: %s", error)
        return 3

    report = build_load_report(input_path, valid_records, rejected_rows)
    write_json_report(report, report_path)

    print("\nCSV loading completed")
    print(f"Input rows:    {report['total_rows']}")
    print(f"Valid rows:    {report['valid_row_count']}")
    print(f"Rejected rows: {report['rejected_row_count']}")
    print(f"Report:        {report_path}\n")

    return 0


def run_failure_tests() -> None:
    """Automated assertions testing critical failure paths with test outputs saved in output/day04/."""
    print("--- Running Failure Test 1: Missing File ---")
    missing_path = PROJECT_ROOT / "data" / "day04" / "does_not_exist.csv"
    status_code_1 = run_loader(
        missing_path,
        DAY04_OUTPUT_DIR / "missing_file_report.json",
    )
    assert status_code_1 == 1, f"Expected exit status 1, got {status_code_1}"
    print("PASS: missing-file failure test\n")

    print("--- Running Failure Test 2: Missing Required Column ---")
    missing_columns_path = PROJECT_ROOT / "data" / "day04" / "missing_columns.csv"
    status_code_2 = run_loader(
        missing_columns_path,
        DAY04_OUTPUT_DIR / "missing_columns_report.json",
    )
    assert status_code_2 == 2, f"Expected exit status 2, got {status_code_2}"
    print("PASS: missing-column failure test\n")


def main() -> None:
    """Primary execution entry point."""
    configure_logging(DEFAULT_LOG_PATH)
    
    print("==========================================")
    print("RUNNING MAIN INGESTION PIPELINE")
    print("==========================================")
    status = run_loader(DEFAULT_INPUT_PATH, DEFAULT_REPORT_PATH)
    print(f"Main Pipeline Exit Code: {status}\n")

    print("==========================================")
    print("RUNNING AUTOMATED FAILURE TESTS")
    print("==========================================")
    run_failure_tests()


if __name__ == "__main__":
    main()


