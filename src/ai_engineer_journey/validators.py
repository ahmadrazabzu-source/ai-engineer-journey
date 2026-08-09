"""Reusable validation helpers developed during Week 1."""


def normalize_record_id(raw_record_id: str) -> str:
    """Return a trimmed uppercase synthetic record identifier."""
    return raw_record_id.strip().upper()


def classify_age_group(age: int) -> str:
    """Return a broad age category for a validated age."""
    if age < 0 or age > 120:
        raise ValueError("age must be between 0 and 120")

    if age < 18:
        return "minor"

    if age < 65:
        return "adult"

    return "older_adult"


def parse_consent(value: str) -> bool:
    """Convert accepted consent text into a Boolean value."""
    normalized_value = value.strip().lower()

    true_values = {"yes", "y", "true", "1"}
    false_values = {"no", "n", "false", "0"}

    if normalized_value in true_values:
        return True

    if normalized_value in false_values:
        return False

    raise ValueError(
        "consent value must be yes/no, true/false, 1/0, y/n"
    )