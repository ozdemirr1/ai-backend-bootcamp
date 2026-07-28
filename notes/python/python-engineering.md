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
