# Python Basics

## Goal

This note covers Python syntax basics for backend development, using examples from the OpsDesk ticket system.

## Topics

- Variables
- Data types
- Conditionals
- Loops
- Basic output

## Variables

Variables store values so we can use them later. We use `=` to assign a value.

```python
ticket_id = 1001
ticket_title = "Password reset problem"
assigned_user = "Furkan"
estimated_hours = 1.5
```

## Basic Data Types

### String (`str`)

Regular text values.

```python
ticket_title = "Password reset email is not received"
```

### Integer (`int`)

Whole numbers.

```python
open_ticket_count = 5
```

### Float (`float`)

Numbers with decimal points.

```python
estimated_hours = 1.5
```

### Boolean (`bool`)

Either `True` or `False`. Booleans are useful for yes/no state flags in backend applications.

```python
is_resolved = False  # Ticket has not been resolved yet.
```

### None

`None` means that a value is absent. It is different from `0` or an empty string.

If an OpsDesk ticket has not been assigned to an agent, we can set:

```python
assigned_user = None
```

## Checking Types

The `type()` function shows what kind of data a value contains.

```python
ticket_id = 1001
print(type(ticket_id))
```

Output:

```text
<class 'int'>
```

## Conditionals

Conditionals run different code depending on whether a condition is `True` or `False`.

```python
if is_resolved:
    print("The ticket has been resolved.")
elif assigned_user is None:
    print("The ticket is waiting to be assigned.")
else:
    print(f"The ticket is in progress and assigned to {assigned_user}.")
```

Python uses `if`, `elif`, and `else` to represent different decision branches. The order of these checks matters.

## Loops

Loops repeat an operation without duplicating code.

### For Loop

A `for` loop processes each item in a collection.

```python
ticket_priorities = ["critical", "high", "medium", "low"]

for priority in ticket_priorities:
    print(f"Ticket priority: {priority}")
```

### While Loop

A `while` loop continues as long as its condition is `True`.

```python
remaining_tickets = 3

while remaining_tickets > 0:
    print(f"Remaining tickets: {remaining_tickets}")
    remaining_tickets -= 1
```

The value used in the condition must change so that the loop can finish.

## Basic Output

The `print()` function displays values in the terminal.

```python
ticket_id = 1001
print(f"Ticket ID: {ticket_id}")
```
