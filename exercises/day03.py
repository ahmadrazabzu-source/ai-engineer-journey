"""Day 3 data structures using synthetic healthcare records.

This program is educational only. It contains no real patient information and
must not be used for clinical decisions.
"""

from collections import deque
import timeit
from typing import Any

Record = dict[str, Any]

REQUIRED_FIELDS = (
    "record_id",
    "age",
    "department",
    "consent_confirmed",
    "completed_visits",
    "review_status",
)

SYNTHETIC_RECORDS: list[Record] = [
    {
        "record_id": "SYN-001",
        "age": 42,
        "department": "Cardiology",
        "consent_confirmed": True,
        "completed_visits": 3,
        "review_status": "complete",
    },
    {
        "record_id": "SYN-002",
        "age": 57,
        "department": "Neurology",
        "consent_confirmed": True,
        "completed_visits": 2,
        "review_status": "pending",
    },
    {
        "record_id": "SYN-003",
        "age": 35,
        "department": "Pharmacy",
        "consent_confirmed": False,
        "completed_visits": 1,
        "review_status": "excluded",
    },
    {
        "record_id": "SYN-004",
        "age": 68,
        "department": "Cardiology",
        "consent_confirmed": True,
        "completed_visits": 4,
        "review_status": "complete",
    },
    {
        "record_id": "SYN-005",
        "age": 29,
        "department": "Pharmacy",
        "consent_confirmed": True,
        "completed_visits": 2,
        "review_status": "pending",
    },
    {
        "record_id": "SYN-006",
        "age": 73,
        "department": "Neurology",
        "consent_confirmed": True,
        "completed_visits": 3,
        "review_status": "complete",
    },
    {
        "record_id": "SYN-007",
        "age": 51,
        "department": "Cardiology",
        "consent_confirmed": True,
        "completed_visits": 1,
        "review_status": "pending",
    },
    {
        "record_id": "SYN-007",
        "age": 51,
        "department": "Cardiology",
        "consent_confirmed": True,
        "completed_visits": 1,
        "review_status": "pending",
    },
]


def has_required_fields(
    record: Record,
    required_fields: tuple[str, ...],
) -> bool:
    """Return whether the record contains every required field."""
    return all(field in record for field in required_fields)


def find_record_in_list(
    records: list[Record],
    target_id: str,
) -> Record | None:
    """Return the first matching record using sequential search."""
    for record in records:
        if record.get("record_id") == target_id:
            return record
    return None


def find_duplicate_ids(records: list[Record]) -> set[str]:
    """Return duplicate record identifiers."""
    seen_ids = set()
    duplicate_ids = set()

    for record in records:
        rec_id = record["record_id"]
        if rec_id in seen_ids:
            duplicate_ids.add(rec_id)
        else:
            seen_ids.add(rec_id)

    return duplicate_ids


def build_record_index(records: list[Record]) -> dict[str, Record]:
    """Return a record-ID dictionary index."""
    record_index = {}
    for record in records:
        rec_id = record["record_id"]
        record_index[rec_id] = record
    return record_index


def get_unique_departments(records: list[Record]) -> set[str]:
    """Return unique departments."""
    unique_departments = set()
    for record in records:
        unique_departments.add(record["department"])
    return unique_departments


def count_records_by_department(
    records: list[Record],
) -> dict[str, int]:
    """Return department counts."""
    dept_counts = {}
    for record in records:
        dept = record["department"]
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
    return dept_counts


def summarize_records(records: list[Record]) -> dict[str, Any]:
    """Return summary values."""
    total_records = len(records)
    seen_ids = set()
    duplicate_ids = find_duplicate_ids(records)

    total_age = 0
    total_completed_visits = 0
    consent_confirmed_count = 0
    review_status_counts = {}
    department_counts = count_records_by_department(records)

    for record in records:
        seen_ids.add(record["record_id"])
        total_age += record["age"]
        total_completed_visits += record["completed_visits"]

        if record["consent_confirmed"]:
            consent_confirmed_count += 1

        status = record["review_status"]
        review_status_counts[status] = review_status_counts.get(status, 0) + 1

    average_age = total_age / total_records if total_records > 0 else 0.0

    return {
        "total_records": total_records,
        "unique_record_ids": len(seen_ids),
        "duplicate_ids": duplicate_ids,
        "average_age": average_age,
        "total_completed_visits": total_completed_visits,
        "consent_confirmed_count": consent_confirmed_count,
        "review_status_counts": review_status_counts,
        "department_counts": department_counts,
    }


def demonstrate_review_stack() -> None:
    """Demonstrate LIFO behavior."""
    stack = []
    stack.append("Load records")
    stack.append("Check required fields")
    stack.append("Detect duplicates")
    stack.append("Generate summary")

    last_action = stack.pop()
    print(f"Most recently completed action: {last_action}")
    print(f"Remaining stack: {stack}")


def process_review_queue(record_ids: list[str]) -> list[str]:
    """Demonstrate FIFO behavior using deque."""
    queue = deque()
    processed = []

    for rec_id in record_ids:
        queue.append(rec_id)

    while queue:
        item = queue.popleft()
        processed.append(item)

    return processed


def generate_lookup_records(count: int) -> list[Record]:
    """Generate minimal synthetic records."""
    large_records: list[Record] = []
    for number in range(1, count + 1):
        record_id = f"SYN-{number:05d}"
        record: Record = {
            "record_id": record_id,
            "age": 18 + (number % 83),
            "department": "Synthetic",
        }
        large_records.append(record)
    return large_records


def compare_lookup_times(
    records: list[Record],
    record_index: dict[str, Record],
    target_id: str,
) -> dict[str, float]:
    """Compare list and dictionary lookup timings."""
    list_measurements = timeit.repeat(
        lambda: find_record_in_list(records, target_id),
        repeat=5,
        number=1_000,
    )
    dictionary_measurements = timeit.repeat(
        lambda: record_index.get(target_id),
        repeat=5,
        number=1_000,
    )

    return {
        "best_list_time": min(list_measurements),
        "best_dictionary_time": min(dictionary_measurements),
    }


def main() -> None:
    """Run the Day 3 demonstrations."""
    print("=== DAY 3 DATA STRUCTURES DEMO ===\n")

    # 1. Validate records schema
    all_valid = all(
        has_required_fields(r, REQUIRED_FIELDS) for r in SYNTHETIC_RECORDS
    )
    print(f"1. Schema Validation (Required Fields Present): {all_valid}")

    # 2. Detect duplicates
    duplicates = find_duplicate_ids(SYNTHETIC_RECORDS)
    print(f"2. Duplicate Record IDs Detected: {duplicates}")

    # 3. Print summary
    summary = summarize_records(SYNTHETIC_RECORDS)
    print("\n3. Dataset Summary:")
    print(f"   - Total records: {summary['total_records']}")
    print(f"   - Unique record IDs: {summary['unique_record_ids']}")
    print(f"   - Duplicate IDs: {summary['duplicate_ids']}")
    print(f"   - Average age: {summary['average_age']:.2f}")
    print(f"   - Total completed visits: {summary['total_completed_visits']}")
    print(f"   - Consent confirmed count: {summary['consent_confirmed_count']}")
    print(f"   - Review status counts: {summary['review_status_counts']}")
    print(f"   - Department counts: {summary['department_counts']}")

    # 4. Unique departments check
    depts = get_unique_departments(SYNTHETIC_RECORDS)
    print(f"\n4. Unique Departments ({len(depts)}):")
    for dept in sorted(depts):
        print(f"   - {dept}")

    # 5. Demonstrate stack (LIFO)
    print("\n5. Stack Demonstration (LIFO):")
    demonstrate_review_stack()

    # 6. Demonstrate queue (FIFO)
    print("\n6. Queue Demonstration (FIFO):")
    sample_ids = ["SYN-001", "SYN-002", "SYN-003"]
    processed_queue = process_review_queue(sample_ids)
    print(f"   Processed queue in FIFO order: {processed_queue}")

    # 7. Generate 10,000 lookup records & Index
    print("\n7. Generating 10,000 synthetic records for benchmarking...")
    large_records = generate_lookup_records(10_000)
    large_index = build_record_index(large_records)
    print(f"   First Record: {large_records[0]['record_id']}")
    print(f"   Last Record:  {large_records[-1]['record_id']}")

    # 8. Benchmark beginning, end, and missing IDs
    print("\n8. Benchmarking List Search O(n) vs. Dict Lookup O(1) [1,000 runs]:")
    targets = {
        "Beginning": "SYN-00001",
        "End": "SYN-10000",
        "Missing": "SYN-99999",
    }

    print(
        f"   {'Position':<12} | {'Target ID':<10} | {'List Time (s)':<15} | {'Dict Time (s)':<15}"
    )
    print("   " + "-" * 60)

    for position, target_id in targets.items():
        timings = compare_lookup_times(large_records, large_index, target_id)
        list_t = timings["best_list_time"]
        dict_t = timings["best_dictionary_time"]
        print(
            f"   {position:<12} | {target_id:<10} | {list_t:.6f} s       | {dict_t:.6f} s"
        )

    print("   " + "-" * 60)
    print(
        "   CONCLUSION: Dictionary lookup remained approximately constant in this experiment,\n"
        "   while list search became more expensive when the target was late or missing.\n"
    )


if __name__ == "__main__":
    main()