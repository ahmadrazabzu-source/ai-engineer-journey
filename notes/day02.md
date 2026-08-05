# Day 2 Learning Log

## Concepts completed

- Variables and assignment
- Primitive data types (`str`, `int`, `bool`)
- Type conversion (`int()`, `type()`)
- Boolean expressions (`==`, `>=`, `<=`, `in`)
- Conditions (`if`, `elif`, `else`)
- For loops (`for char in string:`)
- While loops (`while True:` input validation loops)
- Functions (defining signatures with type hints `-> str` and docstrings)
- Input validation (cleaning strings before validating)
- Refactoring (extracting inline script logic into modular, testable functions)

## Three functions I created

1. `normalize_record_id(raw_record_id: str) -> str`
   - *Purpose:* Trims leading/trailing whitespace and converts ID to uppercase.
2. `is_valid_age_text(age_text: str) -> bool`
   - *Purpose:* Validates if string input represents a whole number integer between 0 and 120.
3. `classify_age_group(age: int) -> str`
   - *Purpose:* Categorizes a validated age integer into `"minor"`, `"adult"`, or `"older_adult"`.

## Boundary cases tested

Below are the exact values used when testing `is_valid_age_text()` and their resulting outputs:

| Test Input | Input Representation (`!r`) | Expected Result | Actual Output | Reason |
| :--- | :--- | :---: | :---: | :--- |
| `"42"` | `'42'` | `True` | `True` | Standard valid integer |
| `"0"` | `'0'` | `True` | `True` | Lower valid range boundary |
| `"120"` | `'120'` | `True` | `True` | Upper valid range boundary |
| `"121"` | `'121'` | `False` | `False` | Exceeds max age range (>120) |
| `"-1"` | `'-1'` | `False` | `False` | Negative number (fails `.isdigit()`) |
| `"42.5"` | `'42.5'` | `False` | `False` | Decimal float (fails `.isdigit()`) |
| `"forty"` | `'forty'` | `False` | `False` | Non-numeric word (fails `.isdigit()`) |
| `""` | `''` | `False` | `False` | Empty string check |
| `" 42 "` | `' 42 '` | `True` | `True` | Valid integer padded with whitespace |

## Real error or confusion

Confusing the loop variable (`char`) inside a `for char in record_id:` loop with the total string (`record_id`), and expecting character inspection methods like `char.isdigit()` or `char.isalpha()` to return total occurrence counts (e.g., `7` or `3`) instead of boolean values (`True`/`False`).

## Root cause

In Python, a `for` loop iterates through a string **one character at a time**. On every turn of the loop, `char` holds a single character (`"S"`, `"-"`, `"2"`, etc.), not the entire string `"SYN-2026-015"`. Therefore, methods like `char.isdigit()` evaluate to `True` or `False` for that single character on each pass. The numbers (`3`, `7`, `2`) came from incrementing separate counter variables (`letter_count`, `digit_count`, `hyphen_count`), not from calling `.isdigit()` directly.

## Fix

1. Understood that `char` holds single individual characters sequentially during loop iteration.
2. Used string methods directly on the complete string variable `record_id` when inspecting the entire record (e.g., `record_id.count("-")`).
3. Used generator expressions and `sum()` to perform single-line counting across the full string: `sum(1 for c in record_id if c.isdigit())`.

## What I can now explain without help

1. **Difference between `str` methods and integer counters:** How `.isdigit()` returns a boolean for single character checks versus accumulating integer counts across a string.
2. **Input normalization sequence:** Why applying `.strip().lower()` before validation prevents edge-case failures caused by unexpected whitespace or mixed capitalization (`" YES "` $\rightarrow$ `"yes"`).
3. **Difference between `print()` and `return` in functions:** How `return` passes data back to the caller for variable assignment, whereas `print()` only displays text to standard output.
4. **Safe integer parsing without `try/except`:** Using `.strip().isdigit()` to verify string contents before executing `int()`, avoiding unexpected `ValueError` runtime crashes.
5. **The role of `if __name__ == "__main__":`:** How entry-point guards prevent script execution code inside `main()` from running automatically when importing helper functions into other modules.

## Next smallest action

Begin Day 3 data structures (lists, dictionaries, sets) and build the synthetic record summarizer module.