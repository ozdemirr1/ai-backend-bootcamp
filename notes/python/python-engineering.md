# Python Engineering Fundamentals

## Goal

This note covers Python features that improve readability, communication, and maintainability in backend code.

## List Comprehensions

A list comprehension creates a new list by transforming or filtering values from an existing iterable.

### Transformation

```python
raw_priorities = [" HIGH ", "medium", "CRITICAL", "low "]

normalized_priorities = [
    priority.strip().lower()
    for priority in raw_priorities
]
```

The original list is not modified. A new list is created after whitespace removal and lowercase conversion.

### Filtering

```python
urgent_priorities = [
    priority
    for priority in normalized_priorities
    if priority in ("high", "critical")
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
