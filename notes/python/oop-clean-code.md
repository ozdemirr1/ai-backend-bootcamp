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

The current `Ticket` class accepts status values as unrestricted strings. Controlled values and validation will be introduced with enums and dataclasses.
