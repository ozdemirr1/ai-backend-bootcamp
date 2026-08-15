# Python Engineering Fundamentals

## Goal

This note covers Python features that improve readability, communication, and maintainability in backend code.

## List Comprehensions

A list comprehension creates a new list by transforming or filtering values from an existing iterable.

### Transformation

```python
raw_priorities = [" HIGH ", "medium", "CRITICAL", "low "]

normalized_priorities = [priority.strip().lower() for priority in raw_priorities]
```

The original list is not modified. A new list is created after whitespace removal and lowercase conversion.

### Filtering

```python
urgent_priorities = [
    priority for priority in normalized_priorities if priority in ("high", "critical")
]
```

A comprehension is useful when the transformation or filter remains simple and readable. A normal `for` loop is usually clearer when the logic contains several operations, nested conditions, or complex error handling.

## Type Hints

Type hints document the values a function expects and returns.

```python
def is_urgent_priority(priority: str) -> bool:
    return priority in ("high", "critical")
```

In this example:

- `priority: str` describes the expected parameter type.
- `-> bool` describes the expected return type.

Type hints improve communication, editor support, static analysis, and maintainability.

## Collection Type Hints

Use `list[element_type]` to describe list elements:

```python
def normalize_priorities(raw_priorities: list[str]) -> list[str]:
    return [priority.strip().lower() for priority in raw_priorities]
```

Use `dict[key_type, value_type]` to describe dictionary keys and values:

```python
sla_hours_by_priority: dict[str, int] = {
    "critical": 1,
    "high": 4,
}
```

These hints describe the expected types. They do not enforce them at runtime by default.

## Optional Values

Python 3.9 uses `Optional` to describe a value that can have a specific type or be `None`:

```python
from typing import Optional


def get_assignee_label(assigned_user: Optional[str]) -> str:
    if assigned_user is None:
        return "Unassigned"

    return assigned_user
```

`Optional[str]` means `str` or `None`. It does not mean that the function argument can be omitted.

A dictionary lookup can also return an optional value:

```python
def get_sla_hours(
    priority: str,
    sla_hours_by_priority: dict[str, int],
) -> Optional[int]:
    return sla_hours_by_priority.get(priority)
```

The return type is `Optional[int]` because `dict.get()` returns `None` when the key does not exist.

## Type Hints Are Not Runtime Validation

Python stores annotation information, but it does not enforce type hints at runtime by default.

```python
def is_urgent_priority(priority: str) -> bool:
    return priority in ("high", "critical")


result = is_urgent_priority(123)
```

The call uses the wrong type, but Python can still execute it and produce `False`. Runtime validation requires explicit checks or a validation library.

## Constants

Names written in uppercase communicate that a module-level value is not intended to change during normal execution:

```python
SLA_HOURS_BY_PRIORITY: dict[str, int] = {
    "critical": 1,
    "high": 4,
    "medium": 8,
    "low": 24,
}
```

Uppercase naming is a convention. Python does not make the dictionary immutable.

## Raising Exceptions

An exception communicates that a function cannot complete its operation normally.

```python
def validate_priority(priority: str) -> str:
    normalized_priority = priority.strip().lower()

    if normalized_priority not in SLA_HOURS_BY_PRIORITY:
        raise ValueError(f"Unsupported priority: {priority}")

    return normalized_priority
```

`ValueError` is appropriate when the input has an acceptable type but its value violates a rule.

Returning `None` can represent an expected absence when the function contract defines that behavior. Raising an exception reports invalid input or another condition that the caller must handle. An exception interrupts the current flow, but the whole program does not have to stop if the exception is caught safely.

## Handling Specific Exceptions

Use `try` for an operation that can fail and catch only exceptions the code can handle meaningfully.

```python
try:
    validated_priority = validate_priority("archived")
except ValueError as error:
    print(f"Priority validation failed: {error}")
else:
    print(f"Validated priority: {validated_priority}")
finally:
    print("Priority validation finished.")
```

- `try` contains the operation that can fail.
- `except ValueError` handles the expected validation error.
- `else` runs only when the `try` block succeeds.
- `finally` runs whether the operation succeeds or fails.

A bare `except:` can hide unrelated programming errors and make debugging difficult. Specific exception handlers allow unexpected failures to remain visible.

## Modules and Imports

Every Python file can be used as a module. Moving related rules into a separate module keeps responsibilities clearer and avoids repeating code.

```python
from ticket_rules import validate_priority
```

In the practice project:

- `ticket_rules.py` contains priority constants and business rules.
- `python_engineering_practice.py` imports those rules and runs example flows.

Standard-library imports and local imports should be separated into groups:

```python
from typing import Optional

from ticket_rules import validate_priority
```

Python executes top-level module code during the first import. Functions and constants are safe to define at the module level, but application startup code should be protected from import side effects.

## Main Guard

The main guard runs the application flow only when the file is executed directly:

```python
def main() -> None:
    print("Application started.")


if __name__ == "__main__":
    main()
```

When the file is imported, `__name__` contains the module name instead of `"__main__"`, so `main()` does not run automatically. This prevents CLI menus, file operations, and other startup behavior from running during imports or tests.

## Pytest Basics

Pytest discovers test files matching `test_*.py` or `*_test.py`. Test function names begin with `test`.

```python
def test_normalize_priorities_cleans_values() -> None:
    raw_priorities = [" HIGH ", "medium", "CRITICAL"]

    result = normalize_priorities(raw_priorities)

    assert result == ["high", "medium", "critical"]
```

A test can be understood as three steps:

- Arrange: Prepare the input and required state.
- Act: Run the behavior being tested.
- Assert: Compare the actual result with the expected result.

Tests use `assert` to report whether an expectation is true. Returning a value from a test function does not verify behavior.

## Testing Exceptions

Use `pytest.raises()` when an exception is the expected behavior:

```python
import pytest


def test_validate_priority_rejects_unsupported_value() -> None:
    with pytest.raises(
        ValueError,
        match="Unsupported priority: archived",
    ):
        validate_priority("archived")
```

The test fails when the expected exception is not raised, a different exception is raised, or the message does not match.

## Test Isolation With `tmp_path`

Pytest provides the `tmp_path` fixture as an isolated `Path` object managed for a test run.

```python
from pathlib import Path


def test_missing_file_returns_empty_list(tmp_path: Path) -> None:
    tickets_file_path = tmp_path / "tickets.json"

    assert load_tickets(tickets_file_path) == []
```

Using a temporary path prevents tests from reading or changing the real application data. Each test should create the state it needs instead of depending on another test.

## Collection Errors and Test Failures

A collection error happens before a test can run. Common causes include import errors, syntax errors, and executable top-level code that fails while Pytest imports a test module.

A test failure happens after Pytest successfully discovers and starts a test, but an assertion or another expected condition is not satisfied.

Run all discovered tests from the repository root:

```bash
python -m pytest -v
```

## Ruff Basics

Ruff performs static analysis without running the application flow.

```bash
ruff check .
```

Ruff can report problems such as:

- Unused imports
- Undefined names
- Unorganized import blocks
- Selected syntax and style violations

Pytest and Ruff answer different questions:

- Pytest checks whether tested behavior matches expectations.
- Ruff checks code against enabled static-analysis and style rules.

Passing one tool does not guarantee passing the other.

## Ruff Configuration

The repository configures Ruff in `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py39"
line-length = 88

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I"]

[tool.ruff.lint.isort]
known-first-party = ["app", "ticket_rules"]
```

The Python target prevents Ruff from recommending syntax that is unavailable in Python 3.9. First-party module configuration helps Ruff distinguish local modules from third-party packages when organizing imports.

Automatic fixes must be reviewed with `git diff`. A fix can be correct according to an enabled rule while still being inappropriate for the project context. Tests should run again after lint fixes.

## Dependency Types

Runtime dependencies are required for the application to operate. Development dependencies support activities such as testing and linting but are not required by the current application flow.

The current exercises use only the Python standard library at runtime. Development tools are recorded in `requirements-dev.txt`:

```text
pytest==8.4.2
ruff==0.16.1
```

Install them with the active virtual environment:

```bash
python -m pip install -r requirements-dev.txt
```

Only the direct development dependencies are listed manually. Pip resolves their transitive dependencies, such as `pluggy` and `iniconfig` for Pytest.

Pinned direct dependencies improve repeatability, but `requirements-dev.txt` is not a complete lock file because transitive versions are not pinned. A dedicated locking workflow can be introduced when the projects require stronger reproducibility.

Check the installed dependency set for conflicts:

```bash
python -m pip check
```
