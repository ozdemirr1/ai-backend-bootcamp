# Python Functions

## Goal

This note covers how to write reusable Python functions.

## Topics

- Function definition
- Parameters
- Return values
- Function naming
- Small backend-style examples

## Function Definition

A function is a reusable block of code that performs a specific task.

Functions are defined with the `def` keyword.

```python
def show_system_status():
    print("System is ready.")
```

Defining a function does not run it. The function must be called:

```python
show_system_status()
```

## Parameters and Arguments

Parameters are the input names defined by a function.

Arguments are the actual values passed when the function is called.

```python
def show_ticket_title(ticket_title):
    print(f"Ticket title: {ticket_title}")


show_ticket_title("Password reset problem")
```

In this example:

- `ticket_title` is a parameter.
- `"Password reset problem"` is an argument.

## Return Values

The `return` statement sends a value back to the code that called the function.

```python
def calculate_sla_hours(ticket_priority):
    if ticket_priority == "high":
        return 4
    else:
        return None


sla_hours = calculate_sla_hours("high")
```

The returned value can be stored, tested, or used in another operation.

## `print()` vs `return`

`print()` displays a value in the terminal.

`return` gives a value back to the calling code.

```python
def show_priority(ticket_priority):
    print(ticket_priority)


def get_priority():
    return "high"
```

A function without an explicit `return` returns `None`.

Backend service functions usually return values so other parts of the application can use them.

## Function Naming

Function names should:

- Use `snake_case`.
- Describe the function's responsibility.
- Prefer action-oriented names.

Examples:

```python
calculate_sla_hours()
show_ticket_details()
assign_ticket()
```

## Basic Function Checks

`assert` can verify that a function returns the expected result.

```python
assert calculate_sla_hours("high") == 4
assert calculate_sla_hours("unknown") is None
```

If an assertion is false, Python raises an `AssertionError`.
