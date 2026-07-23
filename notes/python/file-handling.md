# Python File Handling

## Goal

This note covers reading and writing files with Python.

## Topics

- Reading text files
- Writing text files
- Working with JSON files
- Basic error handling

## File Paths

`pathlib.Path` provides a readable and cross-platform way to work with file paths.

```python
from pathlib import Path

current_directory = Path(__file__).parent
data_directory = current_directory / "data"
data_directory.mkdir(exist_ok=True)
```

`Path(__file__).parent` represents the directory containing the current Python file.

`exist_ok=True` prevents an error when the directory already exists.

## Opening Files Safely

The `with` statement automatically closes a file after the operation finishes.

```python
with file_path.open("r", encoding="utf-8") as file:
    content = file.read()
```

Using UTF-8 supports Turkish and other Unicode characters.

## File Modes

| Mode | Purpose | Important behavior |
|---|---|---|
| `"r"` | Read | Fails if the file does not exist |
| `"w"` | Write | Creates or overwrites the file |
| `"a"` | Append | Adds content to the end |

The `"w"` mode can delete existing content, so the target path must be checked carefully.

## Writing and Reading Text

```python
with summary_file_path.open("w", encoding="utf-8") as summary_file:
    summary_file.write("Ticket ID: 1001\n")

with summary_file_path.open("r", encoding="utf-8") as summary_file:
    ticket_summary = summary_file.read().strip()
```

`\n` creates a new line. `.strip()` removes unnecessary whitespace from the beginning and end of a string.

## Working with JSON

Serialization converts Python data into JSON.

Deserialization converts JSON back into Python data.

```python
import json

with ticket_file_path.open("w", encoding="utf-8") as ticket_file:
    json.dump(ticket, ticket_file, indent=2, ensure_ascii=False)

with ticket_file_path.open("r", encoding="utf-8") as ticket_file:
    loaded_ticket = json.load(ticket_file)
```

- `json.dump()` writes Python data to a JSON file.
- `json.load()` reads JSON data into Python.
- `indent=2` makes the file readable.
- `ensure_ascii=False` preserves readable Unicode characters.

## Python and JSON Types

| Python | JSON |
|---|---|
| `dict` | object |
| `list` | array |
| `str` | string |
| `int` or `float` | number |
| `True` or `False` | `true` or `false` |
| `None` | `null` |

A Python set cannot be serialized directly because JSON does not have a set type.

## Basic Error Handling

A missing file raises `FileNotFoundError`.

```python
try:
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"File not found: {file_path.name}")
```

Invalid JSON raises `json.JSONDecodeError`.

Specific exceptions should be caught instead of using a bare `except`.

## Basic Checks

```python
assert file_path.exists()
assert loaded_ticket == ticket
assert loaded_ticket["assigned_user"] is None
```

These checks verify that the file exists and the serialized data can be read back correctly.