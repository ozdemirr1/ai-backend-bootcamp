# Week 03 Plan

## Date

27 July - 2 August

## Main Focus

- Python engineering fundamentals
- Type hints
- List comprehensions
- Exception handling
- Modules and imports
- Pytest basics
- Ruff basics
- Dependency management
- Git branch and pull request workflow
- Remaining terminal and HTTP fundamentals

## Why This Week Exists

Week 01 and Week 02 progressed faster than the original schedule.

Before starting FastAPI, this week will close the remaining Git, terminal, HTTP, testing, and Python engineering gaps.

FastAPI and OOP will not be started early.

## Learning Goals

- Write readable list comprehensions.
- Add meaningful type hints to functions.
- Understand that type hints are not runtime validation.
- Raise and handle specific exceptions.
- Understand `try`, `except`, `else`, and `finally`.
- Organize code with modules and imports.
- Convert basic checks into pytest tests.
- Run lint checks with Ruff.
- Understand basic Python dependency management.
- Practice Git branches and pull requests.
- Send HTTP requests with `curl`.
- Review headers, query parameters, path parameters, `409`, and `500`.

## Daily Plan

### Monday

Git branch workflow, remaining terminal commands, and HTTP review.

Practice:

- Create and switch to a feature branch.
- Review `git branch`, `git switch`, and merge concepts.
- Practice `grep`, `find`, `chmod`, and `curl`.
- Review headers, query parameters, and path parameters.
- Review `409 Conflict` and `500 Internal Server Error`.

### Tuesday

List comprehensions and type hints.

Practice:

- Convert simple loops into readable comprehensions.
- Add parameter and return type hints.
- Practice `list`, `dict`, `str`, `int`, `bool`, and `None` annotations.
- Explain why type hints do not validate data at runtime.

### Wednesday

Exceptions, modules, and imports.

Practice:

- Raise `ValueError` for invalid input.
- Use specific exception handlers.
- Review `try`, `except`, `else`, and `finally`.
- Create a small multi-file Python example.
- Review local imports and main guards.

### Thursday

Pytest basics.

Practice:

- Install pytest in the virtual environment.
- Learn test discovery.
- Convert plain CLI checks into pytest tests.
- Test priority validation.
- Test missing-file behavior.
- Test JSON persistence round trips.
- Keep tests isolated from real data.

### Friday

Ruff and dependency-management basics.

Practice:

- Install and run Ruff.
- Review lint output.
- Fix style problems intentionally.
- Record project dependencies.
- Understand direct and development dependencies.
- Add test and lint commands to documentation.

### Saturday

Integration, cleanup, and pull request practice.

Practice:

- Run all tests.
- Run Ruff.
- Review the full diff.
- Update README files.
- Push the feature branch.
- Open the first pull request.
- Review the pull request diff before merging.

### Sunday

Week 03 report and Week 04 preparation.

Practice:

- Complete `weekly-reports/week-03.md`.
- Update `WEEKLY_STATUS.md`.
- Review GitHub repository health.
- Prepare the Week 04 OOP and clean-code plan.
- Answer interview questions.

## Code To Implement

- List comprehension exercises
- Type hint exercises
- Exception handling examples
- Small module/import example
- Pytest tests for the ticket CLI
- Ruff configuration
- Dependency configuration

## Notes To Write

- `notes/python/python-engineering.md`
- `notes/git-github/branch-and-pr-workflow.md`
- `notes/http-rest/http-request-parts.md`

## Test Goals

- Pytest discovers and runs the CLI tests.
- Missing files return an empty collection.
- JSON persistence round trips preserve ticket data.
- Valid and invalid priorities are tested.
- Real CLI data is not modified by tests.
- Ruff completes without unresolved violations.

## Git Workflow Goal

Use a feature branch for Week 03 work.

Planned branch:

```text
feature/week-03-python-engineering
```

Open and review the first pull request before merging into `main`.

## Expected Commits

- `week-03: document Git and HTTP gap review`
- `week-03: add Python engineering exercises`
- `week-03: add pytest checks for ticket CLI`
- `week-03: add Ruff and dependency tooling`
- `week-03: document branch and pull request workflow`
- `week-03: add weekly report`

## Interview Questions

- What is a list comprehension?
- When does a comprehension reduce readability?
- What is a type hint?
- Do type hints enforce values at runtime?
- What is the difference between returning `None` and raising an exception?
- Why should specific exceptions be caught?
- What is a Python module?
- Why is a main guard useful?
- How does pytest discover tests?
- Why should tests not use production data?
- What does a linter check?
- What is the difference between a Git branch and a commit?
- Why should a pull request diff be reviewed?
- What is an HTTP header?
- What is the difference between a query parameter and a path parameter?
- When can `409 Conflict` be appropriate?
- What does `500 Internal Server Error` represent?

## Definition of Done

Week 03 is complete when:

- Python engineering notes are written.
- Type hint and exception exercises work.
- Ticket CLI checks run through pytest.
- Ruff passes.
- Dependency usage is documented.
- Remaining HTTP topics are reviewed.
- Terminal gap commands are practiced.
- A feature branch is pushed.
- The first pull request is reviewed and merged.
- The Week 03 report is complete.

## Guardrails

- Do not start FastAPI this week.
- Do not start OOP before Week 04.
- Do not add unrelated technologies.
- Do not rewrite the entire CLI.
- Prefer small, reviewable changes.
- Keep tests and documentation updated.
