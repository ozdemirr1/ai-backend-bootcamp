# Week 03 Python Engineering Practice

## Goal

This project practices Python features that improve readability and maintainability in backend-oriented code.

## Current Topics

- List comprehensions
- Filtering values with comprehensions
- Function parameter and return type hints
- `list` and `dict` type annotations
- Optional values with `Optional`
- The difference between type hints and runtime validation
- Constant naming conventions
- Raising and handling specific exceptions
- `try`, `except`, `else`, and `finally`
- Modules and local imports
- Main guards and import safety

## Project Files

- `ticket_rules.py`: Priority constants, validation, normalization, and SLA rules
- `python_engineering_practice.py`: Example application flow and exception handling

## Run

From the repository root, activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the practice file:

```bash
python projects/week-03-python-engineering/python_engineering_practice.py
```

Import the practice module without running its application flow:

```bash
cd projects/week-03-python-engineering
python -c "import python_engineering_practice"
```

The import check should complete without printing application output.

## Dependencies

The current exercises use only the Python standard library and do not require external packages.
