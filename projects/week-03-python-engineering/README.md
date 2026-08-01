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
- Pytest basics and test isolation
- Ruff linting and import organization
- Development dependency management

## Project Files

- `ticket_rules.py`: Priority constants, validation, normalization, and SLA rules
- `python_engineering_practice.py`: Example application flow and exception handling
- `test_ticket_rules.py`: Pytest checks for normalization and validation rules

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

## Tests

Run the project tests:

```bash
python -m pytest projects/week-03-python-engineering/test_ticket_rules.py -v
```

Run all tests from the repository root:

```bash
python -m pytest -v
```

Pytest discovers files matching `test_*.py` or `*_test.py` and functions whose names begin with `test`.

## Dependencies

The application code uses only the Python standard library.

Install the repository development dependencies from the repository root:

```bash
python -m pip install -r requirements-dev.txt
```

The development dependencies are:

- Pytest for automated tests
- Ruff for linting and import checks

## Lint

Run Ruff from the repository root:

```bash
ruff check .
```

Ruff uses the settings in `pyproject.toml`, including the Python 3.9 target and first-party module names.
