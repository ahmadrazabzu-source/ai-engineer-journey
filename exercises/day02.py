"""Day 2 Python fundamentals using synthetic healthcare-research examples."""


def print_section(number: int, title: str) -> None:
    """Print a readable exercise heading."""
    print(f"\nExercise {number}: {title}")
    print("-" * 50)


def normalize_record_id(raw_record_id: str) -> str:
    """Return a trimmed, uppercase synthetic record identifier."""
    return raw_record_id.strip().upper()


def is_valid_age_text(age_text: str) -> bool:
    """Return whether text represents a whole age from 0 through 120."""
    cleaned = age_text.strip()
    if not cleaned or not cleaned.isdigit():
        return False
    age_int = int(cleaned)
    return 0 <= age_int <= 120


def classify_age_group(age: int) -> str:
    """Return minor, adult, or older_adult for a validated age."""
    if age < 18:
        return "minor"
    elif age < 65:
        return "adult"
    else:
        return "older_adult"


def main() -> None:
    """Run all twelve Day 2 exercises."""

    # Exercise 1 — String Cleaning & Formatting
    print_section(1, "String Cleaning & Formatting")
    raw_id = " syn-001 "
    print(f"Original: {raw_id!r} -> Cleaned: {raw_id.strip().upper()!r}")

    # Exercise 2 — String Inspection
    print_section(2, "String Inspection")
    record_id = "SYN-2026-015"
    print(f"Record ID: {record_id}")
    print(f"Starts with 'SYN': {record_id.startswith('SYN')}")
    print(f"Contains '2026':   {'2026' in record_id}")

    # Exercise 3 — Numeric Type Conversions
    print_section(3, "Numeric Type Conversions")
    age_str = "42"
    age_num = int(age_str)
    print(f"String '{age_str}' -> Integer {age_num} (Type: {type(age_num).__name__})")

    # Exercise 4 — Basic Comparison Operators
    print_section(4, "Basic Comparison Operators")
    print(f"Is {age_num} >= 18? {age_num >= 18}")
    print(f"Is {age_num} < 65?  {age_num < 65}")

    # Exercise 5 — Conditional Logic (if/elif/else)
    print_section(5, "Conditional Logic")
    if age_num < 18:
        group = "minor"
    elif age_num < 65:
        group = "adult"
    else:
        group = "older_adult"
    print(f"Age {age_num} classified as: {group}")

    # Exercise 6 — Counting in Loops
    print_section(6, "Counting in Loops")
    sample_id = "SYN-2026-015"
    letter_count = sum(1 for c in sample_id if c.isalpha())
    hyphen_count = sample_id.count("-")
    digit_count = sum(1 for c in sample_id if c.isdigit())
    print(f"String: {sample_id}")
    print(f"Letters: {letter_count} | Hyphens: {hyphen_count} | Digits: {digit_count}")

    # Exercise 7 — Processing Lists
    print_section(7, "Processing Lists")
    ages = [12, 25, 42, 70]
    for a in ages:
        print(f"Age {a:<2} -> Group: {classify_age_group(a)}")

    # Exercise 8 — Basic Input Processing
    print_section(8, "Basic Input Processing")
    sample_input = " 42 "
    cleaned_input = sample_input.strip()
    print(f"Raw Input: {sample_input!r} -> Cleaned: {cleaned_input!r}")

    # Exercise 9 — Range Validation
    print_section(9, "Range Validation")
    test_val = "42"
    print(f"Is '{test_val}' a valid age (0-120)? {is_valid_age_text(test_val)}")

    # Exercise 10 — Validated yes/no input
    print_section(10, "Validated yes/no input")
    sample_yn = " YES "
    cleaned_yn = sample_yn.strip().lower()
    is_valid_yn = cleaned_yn in ["yes", "y", "no", "n"]
    print(f"Input: {sample_yn!r} -> Cleaned: {cleaned_yn!r} -> Valid: {is_valid_yn}")

    # Exercise 11 — Refactor record-ID normalization into a function
    print_section(11, "Refactor record-ID normalization into a function")
    print(normalize_record_id(" syn-001 "))
    print(normalize_record_id("SYN-002"))
    print(normalize_record_id("  syn-003"))

    # Exercise 12 — Refactor age validation and classification
    print_section(12, "Refactor age validation and classification")
    test_inputs = ["42", "0", "120", "121", "-1", "42.5", "forty", "", " 42 "]
    for tc in test_inputs:
        valid = is_valid_age_text(tc)
        group = classify_age_group(int(tc.strip())) if valid else "N/A"
        print(f"Input: {tc!r:<10} -> Valid: {valid:<5} | Group: {group}")


if __name__ == "__main__":
    main()