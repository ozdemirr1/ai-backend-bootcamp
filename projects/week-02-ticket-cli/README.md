# Week 02 OpsDesk Ticket CLI

A small command-line ticket management project built to practice the Python fundamentals covered in Week 02.

This is a learning project and an early CLI-based precursor to the full OpsDesk application.

## Features

- List existing tickets
- Add a new ticket
- Validate ticket titles
- Validate and normalize priorities
- Save tickets to JSON
- Load tickets from JSON
- Handle missing and invalid JSON files
- Exit through an interactive menu

## Ticket Model

Each ticket contains:

```json
{
  "id": 1,
  "title": "Password reset email is not received",
  "priority": "high",
  "status": "open"
}
```

Supported priorities:

```text
low, medium, high, critical
```

New tickets use the `open` status.

## Project Structure

```text
week-02-ticket-cli/
├── app.py
├── test_app.py
├── README.md
└── data/
    └── tickets.json
```

## Application Flow

```text
CLI input
    ↓
Validation
    ↓
Ticket list operations
    ↓
JSON persistence
    ↓
Terminal output
```

## Run

From the repository root, activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the application:

```bash
python projects/week-02-ticket-cli/app.py
```

## Tests

Run the basic checks:

```bash
python projects/week-02-ticket-cli/test_app.py
```

Expected output:

```text
All CLI checks passed.
```

The tests use Python's standard library and a temporary directory, so the real ticket data is not modified.

## Validation Rules

- Ticket title cannot be empty.
- Priority must be one of the supported values.
- Priority input is normalized to lowercase.
- Invalid JSON prevents the application from continuing with unsafe empty data.

## Current Limitations

- IDs use `len(tickets) + 1` and assume tickets are not deleted.
- Data is stored in a local JSON file instead of a database.
- Concurrent writes are not supported.
- Ticket fields do not yet have schema validation.
- The checks use plain `assert` instead of a test framework.

These limitations will be addressed later with FastAPI, Pydantic validation, PostgreSQL, and proper automated tests.

## Dependencies

This project uses only the Python standard library.