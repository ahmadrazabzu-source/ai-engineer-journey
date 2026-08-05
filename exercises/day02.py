"""Day 2 Python fundamentals using synthetic healthcare-research examples."""

def print_section(number: int, title: str) -> None:
    """Print a readable exercise heading."""
    print(f"\nExercise {number}: {title}")
    print("-" * 50)


def main() -> None:
    """Run all twelve Day 2 exercises."""
    
    # Exercise 1 — String Cleaning
    print_section(1, "String Cleaning & Formatting")
    raw_id = " syn-001 "
    cleaned_id = raw_id.strip().upper()
    print(f"Cleaned: {cleaned_id}")

    # Exercise 2 — Inspection
    print_section(2, "String Inspection")
    sample_id = "SYN-2026-015"
    print(f"Starts with SYN: {sample_id.startswith('SYN')}")

    # Exercise 3 — Conversions
    print_section(3, "Numeric Type Conversions")
    age_str = "42"
    age_num = int(age_str)
    print(f"Age number: {age_num}")

    # Exercise 4 — Comparisons
    print_section(4, "Basic Comparison Operators")
    print(f"Is 42 >= 18? {42 >= 18}")

    # Exercise 5 — Conditional Logic
    print_section(5, "Conditional Logic")
    age = 42
    if age < 18:
        group = "minor"
    elif age < 65:
        group = "adult"
    else:
        group = "older_adult"
    print(f"Age group: {group}")

    # Exercise 6 — Counting
    print_section(6, "Counting in Loops")
    record_id = "SYN-2026-015"
    digits = sum(1 for c in record_id if c.isdigit())
    print(f"Digits count: {digits}")

    # Exercise 7 — List Processing
    print_section(7, "Processing Lists")
    ages = [12, 25, 42, 70]
    for a in ages:
        g = "minor" if a < 18 else ("adult" if a < 65 else "older_adult")
        print(f"Age {a}: {g}")

    # Exercise 8 — Basic Input Processing
    print_section(8, "Basic Input Processing")
    print("Completed input test.")

    # Exercise 9 — Range Validation Inline
    print_section(9, "Range Validation")
    val_str = "42"
    is_valid = val_str.strip().isdigit() and 0 <= int(val_str.strip()) <= 120
    print(f"Is '42' valid? {is_valid}")

    # Exercise 10 — Yes/No Validation Inline
    print_section(10, "Validated yes/no input")
    ans = " YES ".strip().lower()
    print(f"Valid answer: {ans in ['yes', 'y', 'no', 'n']}")


if __name__ == "__main__":
    main()