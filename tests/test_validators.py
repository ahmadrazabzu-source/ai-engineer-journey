"""Tests for reusable Week 1 validation helpers."""

import pytest

from ai_engineer_journey.validators import (
    classify_age_group,
    normalize_record_id,
    parse_consent,
)


### Test 1 — Normalization
def test_normalize_record_id() -> None:
    """Record identifiers should be trimmed and uppercased."""
    assert normalize_record_id(" syn-001 ") == "SYN-001"


### Test 2 — Age category boundaries
def test_classify_age_group_boundaries() -> None:
    """Age classification should respect category boundaries."""
    assert classify_age_group(17) == "minor"
    assert classify_age_group(18) == "adult"
    assert classify_age_group(64) == "adult"
    assert classify_age_group(65) == "older_adult"


### Test 3 — Consent parsing and failure
def test_parse_consent() -> None:
    """Consent parsing should normalize valid input and reject invalid input."""
    assert parse_consent(" YES ") is True
    assert parse_consent("false") is False

    with pytest.raises(ValueError):
        parse_consent("maybe")
