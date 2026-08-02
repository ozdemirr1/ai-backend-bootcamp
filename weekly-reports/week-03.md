# Week 03 Report

## Date

27 July - 2 August

## Main Focus

- Python engineering fundamentals
- List comprehensions and type hints
- Exception handling
- Modules and imports
- Pytest
- Ruff
- Dependency management
- Git branch and pull request workflow
- Terminal and HTTP gap review

## What I Completed

- [x] Practiced Git branches and switching between branches
- [x] Reviewed `grep`, `find`, `chmod`, and `curl`
- [x] Reviewed HTTP headers, path parameters, and query parameters
- [x] Reviewed `409 Conflict` and `500 Internal Server Error`
- [x] Practiced readable list comprehensions
- [x] Added parameter and return type hints
- [x] Compared returning `None` with raising an exception
- [x] Practiced `try`, `except`, `else`, and `finally`
- [x] Split reusable ticket rules into a Python module
- [x] Added an import-safe main guard
- [x] Converted ticket checks into Pytest tests
- [x] Isolated persistence tests with `tmp_path`
- [x] Added Ruff configuration for Python 3.9
- [x] Recorded development dependencies
- [x] Documented test and lint commands
- [x] Opened, reviewed, and merged the first pull request

## What I Learned

- List comprehensions are useful for simple transformations and filters, but complex logic is clearer in a normal loop.
- Type hints communicate expected types but do not enforce values at runtime.
- `Optional[int]` represents a value that can be an integer or `None` in the Python 3.9 codebase.
- Returning `None` can represent an expected absence, while raising `ValueError` reports invalid input that the caller should handle.
- Catching specific exceptions prevents unrelated programming errors from being hidden.
- The `else` block runs after a successful `try`, while `finally` runs whether the operation succeeds or fails.
- A module separates reusable definitions from application execution.
- A main guard prevents application code from running during import.
- Pytest discovers tests through naming conventions.
- A collection error happens before tests run, while a test failure means a collected test did not meet its expectation.
- `tmp_path` keeps test data separate from real application data.
- Pytest checks behavior, while Ruff performs static code-quality checks.
- Runtime and development dependencies serve different purposes.
- Ruff must target the project's Python version to avoid incompatible suggestions.
- A branch is a movable pointer to a commit, not a separate copy of the repository.
- A pull request should be reviewed even when Git reports no merge conflicts.
- Local checks provide evidence, while automated GitHub checks require a CI workflow.
- HTTP headers carry request and response metadata.
- Path parameters identify resources, while query parameters shape or filter a request.

## Code and Documentation I Added

### Python Engineering Practice

- Priority normalization with list comprehensions
- Urgent-priority filtering
- Type-annotated functions
- Optional return values
- Priority validation with `ValueError`
- Specific exception handling
- Import-safe application execution

### Reusable Ticket Rules Module

- Priority constants
- Priority normalization
- Priority validation
- SLA lookup
- Reusable functions imported by practice and test files

### Pytest Checks

- Priority normalization test
- Valid-priority normalization test
- Invalid-priority exception test
- CLI priority validation test
- JSON persistence round-trip test
- Invalid JSON handling test

### Engineering Tooling

- `pyproject.toml` with Ruff configuration
- `requirements-dev.txt` with direct development dependencies
- Python 3.9 lint target
- Pytest and Ruff cache exclusions
- Documented setup, test, lint, and dependency commands

### Git, Terminal, and HTTP Notes

- Branch and pull request workflow
- Branch comparison and review commands
- `grep`, `find`, and permission practice
- HTTP request parts
- Headers, path parameters, and query parameters
- `409 Conflict` and `500 Internal Server Error`

## Problems I Faced

- I initially raised `ValueError` with an unclear validation message.
- I accidentally printed a function object instead of a returned value.
- My first Pytest test caused a collection error because I compared the function itself instead of calling it inside the test.
- Ruff found an unused import and an unformatted import block.
- Ruff initially suggested newer union syntax that is not compatible with the project's Python 3.9 target.
- Several Python files needed final newline and blank-line cleanup before the pull request.
- I needed to distinguish local quality checks from automated GitHub checks.

## How I Solved Them

- I changed validation errors to describe the unsupported input clearly.
- I separated function references from function calls and inspected the returned values.
- I moved assertions inside properly named Pytest functions.
- I used specific exception checks with `pytest.raises`.
- I reviewed Ruff output before applying fixes.
- I configured Ruff with `target-version = "py39"`.
- I ran `git diff --check`, Ruff, and Pytest before opening and merging the pull request.
- I reviewed the complete branch diff and the GitHub `Files changed` section.
- I documented local test results in the pull request description.

## GitHub Outputs

- Commits created during 27 July - 2 August: 14, including the merge and status commits
- Feature branch commits merged through pull request: 12
- Pull requests opened and merged: 1
- Files changed in the first pull request: 15
- Pytest tests: 6 passing
- Ruff result: all checks passed
- Dependency check: no broken requirements
- Main Week 03 project: `projects/week-03-python-engineering/`
- Pull request: `week-03: add Python engineering fundamentals and tooling`

## Interview Questions I Can Answer

- When should a list comprehension be used?
- Do type hints enforce values at runtime?
- What does `Optional[int]` mean?
- What is the difference between returning `None` and raising `ValueError`?
- Why should specific exceptions be caught?
- What is the difference between `else` and `finally` in exception handling?
- What is a Python module?
- Why is a main guard useful?
- How does Pytest discover tests?
- What is the difference between a collection error and a test failure?
- Why should tests use temporary data?
- What is the difference between Pytest and Ruff?
- What is the difference between a branch and a commit?
- Why should a pull request diff be reviewed?
- What does an HTTP header represent?
- What is the difference between a path parameter and a query parameter?
- When are `409 Conflict` and `500 Internal Server Error` appropriate?

## Next Week Goals

- Learn the purpose of classes and objects
- Practice constructors, `self`, instance attributes, and instance methods
- Learn basic encapsulation and inheritance without overusing them
- Use `dataclass` for simple data-focused models
- Use `Enum` for controlled ticket status and priority values
- Understand how objects receive and use dependencies
- Practice modular project structure and clean-code principles
- Refactor the ticket CLI with `Ticket`, `TicketService`, and `TicketRepository` responsibilities
- Add tests for model, service, and repository behavior
- Keep abstractions small and avoid unnecessary inheritance
- Prepare for FastAPI without starting it early
