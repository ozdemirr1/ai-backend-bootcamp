# Python Data Structures

## Goal

This note covers Python data structures used in backend development.

## Topics

- Lists
- Dictionaries
- Tuples
- Sets
- Basic data modeling examples

## Choosing a Data Structure

| Structure | Ordered | Mutable | Allows duplicates | Common use |
|---|---:|---:|---:|---|
| List | Yes | Yes | Yes | Collections of records |
| Dictionary | Yes | Yes | Keys: No | Structured records |
| Tuple | Yes | No | Yes | Fixed sequences |
| Set | No | Yes | No | Unique values |

## Lists

A list stores an ordered and changeable collection of values.

```python
ticket_statuses = ["open", "in_progress", "resolved"]

ticket_statuses.append("waiting_for_customer")
print(ticket_statuses[0])
```

Lists use zero-based indexes. The first element is `[0]`, and the last element can be accessed with `[-1]`.

## Dictionaries

A dictionary stores values as key-value pairs.

```python
ticket = {
    "id": 1001,
    "title": "Password reset problem",
    "priority": "high",
}
```

Values are accessed through their keys:

```python
print(ticket["title"])
ticket["assigned_user"] = "Furkan"
```

Dictionaries are useful for modeling backend records and are similar to JSON objects.

## Tuples

A tuple is an ordered collection that cannot be changed after creation.

```python
supported_priorities = ("critical", "high", "medium", "low")
```

Tuples can represent fixed sequences of values.

## Sets

A set stores unique values and does not guarantee element order.

```python
raw_tags = ["email", "urgent", "email"]
unique_tags = set(raw_tags)
```

The repeated `"email"` value is stored only once.

An empty set must be created with `set()` because `{}` creates an empty dictionary.

## Nested Data Structures

Backend applications often use lists of dictionaries.

```python
tickets = [
    {
        "id": 1001,
        "title": "Password reset problem",
    },
    {
        "id": 1002,
        "title": "VPN connection fails",
    },
]
```

Each dictionary represents one ticket, while the list represents the ticket collection.

## Membership Checks

The `in` operator checks whether a value exists in a collection.

```python
assert "high" in supported_priorities
assert "urgent" in unique_tags
```

Membership checks return either `True` or `False`.