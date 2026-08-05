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
    
    # Exercise 1 & 11 Refactored
    print_section(1, "String Cleaning & Formatting (Refactored)")
    print(normalize_record_id(" syn-001 "))
    print(normalize_record_id("SYN-002"))
    print(normalize_record_id("  syn-003"))

    # Exercise 7 & 12 Refactored
    print_section(12, "Age Validation & Classification (Refactored)")
    test_inputs = ["42", "0", "120", "121", "-1", "42.5", "forty", "", " 42 "]
    for tc in test_inputs:
        valid = is_valid_age_text(tc)
        group = classify_age_group(int(tc.strip())) if valid else "N/A"
        print(f"Input: {tc!r:<10} -> Valid: {valid:<5} | Group: {group}")


if __name__ == "__main__":
    main()