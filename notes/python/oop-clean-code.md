# Python OOP and Clean Code

## Goal

This note covers object-oriented Python and clean-code principles used to model backend domain behavior.

## Classes and Objects

A class defines the structure and behavior shared by a type of object.

An object is an independent instance created from that class.

```python
class Ticket:
    pass


first_ticket = Ticket()
second_ticket = Ticket()
```

`Ticket` is the class. `first_ticket` and `second_ticket` are separate objects, not copies of the class.

## Initializing an Object

`__init__` initializes the state of a newly created object.

```python
class Ticket:
    def __init__(self, ticket_id: int, title: str, status: str):
        self.ticket_id = ticket_id
        self.title = title
        self.status = status
```

The parameters receive values during object creation. The instance attributes store those values on the object.

```python
ticket = Ticket(1001, "Password reset problem", "open")
```

In everyday explanations, `__init__` is often called a constructor. More precisely, it initializes an object after Python creates it.

## Understanding `self`

`self` refers to the object currently receiving a method call.

```python
first_ticket.change_status("in_progress")
```

During this call, `self` refers to `first_ticket`. Other `Ticket` objects keep their own independent state.

Instance attributes remain in memory while the object exists. They are not automatically persisted to a file or database.

## Instance Methods and State

An instance method can read or change the state of one object.

```python
def change_status(self, new_status: str) -> None:
    self.status = new_status
```

This method changes state and does not need to return a value.

```python
def get_summary(self) -> str:
    return f"Ticket {self.ticket_id}: {self.title} | Status: {self.status}"
```

This method reads state and returns a string for the caller to use.

## Dictionary or Class?

A dictionary is suitable for simple structured data.

```python
ticket = {
    "id": 1001,
    "title": "Password reset problem",
    "status": "open",
}
```

A class becomes useful when related data and behavior should be modeled together. Not every dictionary needs to become a class.

## Small Responsibilities

Methods should have clear responsibilities:

- `change_status()` changes ticket state.
- `get_summary()` creates and returns a summary.
- `print()` displays a returned value at the application boundary.

Keeping these responsibilities separate makes behavior easier to understand and test.

## Current Limitation

The introductory `Ticket` class accepts status values as unrestricted strings. The domain model improves this design with enums, a dataclass, and runtime validation.

## Dataclasses

A dataclass reduces boilerplate for data-focused models.

```python
from dataclasses import dataclass


@dataclass
class Product:
    product_id: int
    name: str
    price: float
```

By default, a dataclass generates useful methods such as `__init__`, `__repr__`, and `__eq__`. Domain methods can still be added when they belong to the model.

Dataclasses do not enforce type hints at runtime.

## Enums

An enum defines a controlled collection of named values.

```python
from enum import Enum


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
```

- `.name` returns the Python member name, such as `IN_PROGRESS`.
- `.value` returns the external value, such as `"in_progress"`.

Enums improve readability, discoverability, and consistency. They reduce uncontrolled strings but do not force a dataclass to reject raw strings automatically.

## Dataclass Validation

`__post_init__` runs after the generated dataclass `__init__` assigns the fields. It can protect rules that must be true for every model instance.

```python
def __post_init__(self) -> None:
    if self.ticket_id <= 0:
        raise ValueError("ticket_id must be positive")

    if not self.title.strip():
        raise ValueError("title cannot be empty")
```

Use exception types intentionally:

- `TypeError`: the input has the wrong type, such as a raw string instead of `TicketPriority`.
- `ValueError`: the type is acceptable, but the value violates a rule, such as an empty title.

Validation belonging to every Ticket instance can live in the model. Rules involving storage, duplicate records, or multi-object workflows will belong in repository or service layers.

## TDD: Red and Green

Test-driven development can begin with a test that describes behavior before the implementation exists.

- Red: the test runs and fails because the required behavior is missing.
- Green: the smallest suitable implementation makes the test pass.

A collection error is different from Red. A collection error means Pytest could not finish discovering tests, often because setup code ran at module import time or an import failed.

## Static Checks and Behavior Tests

Ruff performs static lint checks without executing application behavior. Pytest runs code and checks expectations.

A function accidentally moved outside a class can still be valid Python and pass Ruff. A behavior test calling the missing instance method can reveal the mistake with `AttributeError`. Linting and tests provide different kinds of evidence, so both are needed.
