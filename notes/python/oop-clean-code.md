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

## Model, Repository, and Service Responsibilities

The domain model represents one valid ticket and protects rules that apply to every ticket instance.

The repository manages a collection of tickets. The current implementation stores data only in memory and provides operations for saving, listing, and finding tickets. A future repository could use JSON or PostgreSQL without moving storage logic into the model.

The service coordinates application use cases. It creates a valid `Ticket`, checks rules involving other records, and delegates storage operations to the repository.

```text
TicketService -> TicketRepository -> Ticket
```

The layers have different reasons to change:

- The model changes when ticket data or instance invariants change.
- The repository changes when storage or query behavior changes.
- The service changes when an application workflow or multi-record rule changes.

## Encapsulation in the Repository

Returning the repository's internal list directly would allow external code to change stored data without using repository methods.

```python
def list_all(self) -> list[Ticket]:
    return list(self._tickets)
```

Returning a shallow copy protects the repository's list structure. It does not create copies of the individual `Ticket` objects inside the list.

## Dependency Injection

`TicketService` receives its repository through the constructor:

```python
class TicketService:
    def __init__(self, repository: TicketRepository) -> None:
        self._repository = repository
```

This makes the dependency explicit and prevents the service from deciding how its storage dependency must be created. Tests can provide a fresh in-memory repository, while a later application can provide a different repository implementation.

Constructor injection also makes test isolation easier because each test controls the repository instance used by the service.

## Multi-Record Rules

A ticket cannot decide whether its ID already belongs to another ticket because a model instance does not know the complete collection.

The service queries the repository before saving:

```python
existing_ticket = self._repository.find_by_id(ticket_id)

if existing_ticket is not None:
    raise ValueError(f"Ticket with ID {ticket_id} already exists.")
```

The check must happen before `save()`. Invalid input should fail before it changes stored state.

`find_by_id()` returns `None` when a ticket is absent because absence is an expected query result. The service decides whether that absence is acceptable for the current use case.

## Isolated In-Memory Tests

Repository and service tests create a new in-memory repository for each test. They do not read or modify the Week 02 JSON file.

This keeps tests fast, deterministic, independent of execution order, and safe for real project data.

## Invariants and Controlled State Changes

An invariant is a rule that must remain true throughout an object's lifetime. A `Ticket` must always contain a `TicketStatus` instance in its status field.

`__post_init__` protects this rule when the dataclass is first created. Later state changes need their own validation because `__post_init__` does not run again.

```python
def change_status(self, new_status: TicketStatus) -> None:
    if not isinstance(new_status, TicketStatus):
        raise TypeError("new_status must be an instance of TicketStatus")

    self.status = new_status
```

The method validates before assignment so a failed operation leaves the existing state unchanged. The public method provides a controlled path for changing status. Python conventions still allow direct access to public attributes, so callers must use the model's intended API.

## Basic Inheritance

Inheritance represents an **is-a** relationship. A `SupportAgent` is a specialized `Employee`.

```python
class SupportAgent(Employee):
    def __init__(self, name: str, queue_name: str) -> None:
        super().__init__(name)
        self.queue_name = queue_name
```

`super().__init__(name)` reuses the parent initialization instead of duplicating it. A child class can override an inherited method when the specialized type needs different behavior.

Inheritance should not be introduced only to reuse code. The relationship must also make sense in the domain. Separate ticket classes for each priority would add unnecessary hierarchy because priority is already modeled as data with `TicketPriority`.

## Composition

Composition represents a **has-a** relationship. One object receives or contains another object that provides a needed capability.

```python
class TicketNotificationService:
    def __init__(self, formatter: MessageFormatter) -> None:
        self._formatter = formatter
```

The notification service has a formatter; it is not a type of formatter. The same relationship exists between `TicketService` and `TicketRepository`.

Composition is often more flexible for backend dependencies because collaborators can be supplied from outside. Storage, formatting, logging, or notification implementations can change without turning the service into a subclass of those components.

Prefer inheritance for a genuine **is-a** relationship and composition for a **has-a** or **uses-a** relationship.

## Keep I/O at the Boundary

Reusable model and service methods should usually return values instead of printing them.

```python
def create_notification(self, ticket_title: str) -> str:
    return self._formatter.format(ticket_title)
```

The application boundary, such as `main()` or a future FastAPI route, decides how to present the returned value. This separation improves reuse and makes behavior tests simpler.

Ruff can find many static lint problems, but it does not know the application's business requirements or architectural boundaries. Code review and behavior tests are still needed to detect hardcoded business data, misplaced I/O, and incorrect responsibility boundaries.

## Clean-Code Review

Clean code is not only code that passes tests. A review should also examine names, responsibility boundaries, dependency direction, duplication, failure behavior, and whether tests can detect realistic mistakes.

A repository lookup test is stronger when it stores multiple records and verifies that the requested record is selected. With only one record, an incorrect implementation that always returns the first item could still pass.

Service operations should validate and construct a model before saving it:

```text
check application rule
-> construct and validate model
-> save valid model
```

This fail-fast order prevents invalid operations from changing stored state.

A small delegation method can still protect a useful boundary:

```python
def list_tickets(self) -> list[Ticket]:
    return self._repository.list_all()
```

The CLI can now depend on the service rather than knowing both service and repository details. Future authorization, filtering, or ordering rules can be added at the application layer without changing the CLI's storage interaction.

## Linting, Formatting, and Tests

These quality checks answer different questions:

- `ruff check .`: Does the code violate configured static lint rules?
- `ruff format --check .`: Does the code match the configured formatter style?
- `python -m pytest -q`: Does the executed behavior satisfy the test expectations?

No single command replaces the others. Ruff lint does not prove business behavior, formatting does not prove correctness, and passing tests do not guarantee consistent style or catch every static issue.

`ruff format --check` reports formatting differences without modifying files. `ruff format` applies the formatting. Tests should run again after automated changes as a regression check, even when the tool is designed to preserve behavior.

## Avoid Premature Test Abstractions

Repeated test setup should not automatically become a helper or fixture. Explicit setup can make a small test easier to read in isolation.

Extract shared setup when repetition becomes substantial, obscures the behavior under test, or creates a real maintenance problem. An abstraction should reduce cognitive load rather than merely reduce line count.

Test code belongs in test modules. Production modules should not import Pytest or contain test functions. This keeps development-only dependencies out of the application dependency direction and allows Pytest's test discovery rules to work predictably.
