# Week 04 Report

## Date

3 August - 9 August

## Main Focus

- Python classes and objects
- Constructors, `self`, attributes, and methods
- Dataclasses and enums
- Runtime validation and object invariants
- Repository and service responsibilities
- Dependency injection
- Inheritance and composition
- Modular project structure
- Clean-code review
- OOP behavior and CLI tests
- Feature branch and pull request workflow

## What I Completed

- [x] Practiced classes, objects, constructors, and instance behavior
- [x] Compared independent object state through multiple ticket instances
- [x] Added a validated `Ticket` dataclass
- [x] Added controlled priority and status enums
- [x] Protected model invariants during construction and status changes
- [x] Added an in-memory `TicketRepository`
- [x] Added a `TicketService` for application rules
- [x] Injected the repository into the service constructor
- [x] Rejected duplicate ticket IDs before stored state changed
- [x] Compared inheritance with composition
- [x] Kept terminal input and output outside domain modules
- [x] Built an interactive OOP ticket CLI
- [x] Tested model, repository, service, and CLI behavior
- [x] Reviewed linting, formatting, tests, and clean-code boundaries
- [x] Opened, reviewed, and merged the Week 04 pull request
- [x] Cleaned local and remote feature branches after the merge

## What I Learned

- A class defines structure and behavior, while an object is an independent instance with its own state.
- `self` refers to the instance currently using an instance method.
- `__init__` initializes an object after it is created.
- Instance attributes belong to individual objects, while class attributes are defined at class level and are normally shared.
- A dataclass removes repetitive initialization, representation, and equality code from data-focused models.
- Enums provide controlled domain values, clearer intent, IDE support, and protection from uncontrolled strings.
- Type hints communicate expected types but do not enforce them at runtime.
- `__post_init__` can validate a dataclass after generated initialization finishes.
- Object invariants must be protected both during construction and during later state changes.
- `TypeError` is appropriate for an unexpected type, while `ValueError` is appropriate when the type is valid but the value violates a rule.
- A model protects its own valid state, a repository handles storage operations, a service coordinates application rules, and a CLI handles presentation.
- Returning a copy from a repository protects its internal collection from external mutation.
- Constructor dependency injection reduces coupling and makes service tests independent of real storage.
- Inheritance represents an **is-a** relationship, while composition represents a **has-a** or **uses-a** relationship.
- Composition is usually more flexible for backend dependencies such as repositories, formatters, and notification providers.
- A CLI should call the service instead of bypassing application rules through direct repository access.
- Expected validation failures should be converted into useful messages at the application boundary.
- Pytest, Ruff lint, and Ruff formatting answer different quality questions and cannot replace one another.
- Test and application module names must be unique when several non-package learning projects are collected together.

## Architecture I Built

```text
terminal input/output
        |
        v
OOP Ticket CLI
        |
        v
TicketService --------> application rules
        |
        v
TicketRepository -----> in-memory storage
        |
        v
Ticket model ---------> data, validation, and valid state
```

The CLI creates the dependency graph at the application entry point. It passes a repository into the service and communicates with ticket operations through the service layer.

## Code and Documentation I Added

### OOP Foundations

- Class and object practice
- Constructor and `self` examples
- Independent instance state
- Instance methods and controlled state changes
- Import-safe main guards

### Domain Model

- `TicketPriority` enum
- `TicketStatus` enum
- Validated `Ticket` dataclass
- Positive ticket ID validation
- Non-empty title validation and normalization
- Runtime enum type validation
- Controlled `change_status()` behavior
- Human-readable ticket summaries

### Repository and Service Layers

- In-memory ticket storage
- Safe ticket listing through a copied collection
- Ticket lookup by ID
- Expected missing-ticket behavior through `None`
- Ticket creation workflow
- Duplicate ticket ID protection
- Service-level ticket listing
- Constructor dependency injection

### OOP Design Practice

- `Employee` and `SupportAgent` inheritance example
- Parent initialization through `super()`
- Method overriding
- Formatter and notification-service composition example
- Comparison of **is-a** and **has-a** relationships

### OOP Ticket CLI

- List tickets
- Add a ticket
- Exit cleanly
- Convert raw priority input into an enum
- Handle invalid priority input
- Handle model validation errors
- Preserve repository state after failed operations
- Keep presentation logic outside model and repository modules

### Tests

- Default ticket status
- Empty title rejection
- Raw string priority and status rejection
- Non-positive ticket ID rejection
- Ticket summary output
- Valid and invalid status changes
- Repository save, list, copy, and lookup behavior
- Missing-ticket lookup
- Service creation and duplicate-ID behavior
- Failed creation without repository mutation
- Service ticket listing
- Empty and populated CLI output
- Valid CLI ticket creation
- Invalid priority and title input
- Invalid menu option and clean exit behavior

### Documentation

- OOP and clean-code notes
- Project architecture and responsibility boundaries
- Run, test, lint, and format commands
- Dataclass, enum, invariant, dependency, inheritance, and composition explanations
- CLI boundary and terminal testing notes

## Problems I Faced

- My first status-change test failed because the model did not yet have `change_status()`.
- Ruff passed when a method was accidentally outside its class because the standalone function was syntactically valid.
- Repository tests initially used a model field that did not exist.
- A duplicate-ID test failed before the service rule was implemented.
- Ruff detected unsorted imports in production and test modules.
- A production module temporarily imported Pytest, creating the wrong dependency direction.
- The formatter changed several existing Week 04 files and required regression testing.
- The CLI initially imported domain types from the wrong module.
- Invalid Enum and model inputs initially escaped the CLI as uncaught exceptions.
- The full Pytest suite found import collisions because Week 02 and Week 04 reused the generic names `test_app.py` and `app.py`.

## How I Solved Them

- I used a Red-Green TDD cycle to add missing behavior only after observing focused test failures.
- I used behavior tests to catch architectural mistakes that Ruff could not understand.
- I aligned tests with the actual domain model instead of inventing unsupported fields.
- I placed duplicate-ID validation in the service before model storage.
- I reviewed and corrected import grouping rather than relying only on formatting.
- I removed development-tool imports from production modules.
- I reran all tests after automated formatting changes.
- I imported `Ticket` and its enums from the model module that owns them.
- I caught expected conversion and validation errors at the CLI boundary.
- I renamed Week 04 modules to `oop_ticket_cli.py` and `test_cli_app.py` to prevent Pytest import-cache collisions.

## Quality Results

- Pytest: 28 tests passed
- Ruff lint: all checks passed
- Ruff format: 13 Week 04 Python files formatted
- Dependency check: no broken requirements
- Git whitespace check: no errors
- Tests use in-memory storage and do not modify real ticket JSON data

## GitHub Outputs

- Commits created during 3 August - 9 August: 14, including merge and status commits
- Feature branch commits merged through pull request: 12
- Pull requests opened and merged: 1
- Pull request number: #2
- Files changed in the pull request: 15
- Main Week 04 project: `projects/week-04-oop-ticket-cli/`
- Pull request: `week-04: add OOP ticket CLI and clean-code architecture`
- Merge commit: `852e0fc`
- Final Week 04 status commit before this report: `dd84581`

## Interview Questions I Can Answer

- What is the difference between a class and an object?
- What does `self` represent?
- What is the responsibility of `__init__`?
- What is the difference between instance and class attributes?
- When is a dataclass useful?
- Why use an enum instead of uncontrolled strings?
- Why do type hints not replace runtime validation?
- What is an object invariant?
- What should belong to a model, repository, service, and CLI?
- Why should a repository protect its internal collection?
- What is dependency injection?
- Why does a service receive its repository from outside?
- Where should duplicate-ID validation live?
- What is the difference between inheritance and composition?
- Why should a CLI avoid direct repository access?
- How can failed operations be tested for unwanted state changes?
- Why can Ruff pass while a behavior test fails?
- What is the difference between linting, formatting, and behavior testing?

## Month 1 Review

During the first four weeks, I moved from repository and protocol fundamentals to a small layered Python application.

### Engineering Workflow

- Created and maintained a focused bootcamp repository
- Practiced terminal navigation, file operations, and permissions
- Used meaningful commits and weekly status updates
- Worked on feature branches
- Reviewed complete branch diffs
- Opened and merged two pull requests
- Kept local and remote branches clean after merges

### Backend Foundations

- Reviewed HTTP methods, status codes, request parts, headers, path parameters, and query parameters
- Designed validation and REST API notes around the OpsDesk domain
- Practiced Python values, conditions, loops, functions, collections, and file handling
- Built a JSON-backed procedural ticket CLI
- Added exceptions, modules, type hints, and reusable rules
- Added Pytest, Ruff, formatting, and dependency checks
- Built a layered OOP ticket CLI with domain, repository, service, and presentation responsibilities

### Evidence of Progress

- Four completed weekly plans
- Three completed weekly reports before this report
- Two working ticket CLI iterations
- Two reviewed and merged pull requests
- 28 passing tests at the end of Month 1
- A clean `main` branch synchronized with GitHub
- Notes that explain both syntax and engineering decisions

### Current Strengths

- Consistent daily practice and Git discipline
- Strong understanding of validation and failure behavior
- Ability to explain why a design choice was made
- Growing test-first debugging habits
- Clearer separation of responsibilities and dependency direction
- Willingness to inspect errors instead of hiding them

### Areas To Keep Improving

- Write more code independently before comparing with a reference
- Keep test names and module names unique across the repository
- Distinguish framework behavior from application business rules
- Avoid absolute claims when infrastructure and application layers can share data-integrity responsibilities
- Continue practicing concise technical explanations in English
- Preserve depth and resist adding abstractions before they solve a real problem

## Month 1 Success Criteria

- [x] Git and terminal workflow is repeatable
- [x] HTTP and REST fundamentals can be explained
- [x] Python fundamentals have been refreshed through working exercises
- [x] File handling and JSON persistence have been practiced
- [x] Tests and linting are part of the normal workflow
- [x] Feature branches and pull requests have been practiced
- [x] Basic OOP and clean-code responsibilities can be explained
- [x] A small project can be structured into model, repository, service, and presentation layers
- [x] Documentation and weekly progress are maintained consistently
- [x] The repository is ready to begin FastAPI without skipping the Month 1 foundation

## Next Week Goals

- Understand what FastAPI provides and how an ASGI application runs
- Create the first small FastAPI application
- Learn route decorators and HTTP method mapping
- Use path and query parameters in real API endpoints
- Define request and response models
- Connect HTTP validation behavior to existing Python validation knowledge
- Test endpoints without relying only on manual browser checks
- Keep API, service, and domain responsibilities separate
- Add only the dependencies required for the first FastAPI exercises
- Prepare the foundation for the first deployed API milestone in Month 2

## Final Assessment

Week 04 and Month 1 are complete. The repository now demonstrates more than Python syntax: it shows validation, testing, dependency management, modular responsibilities, pull request review, and repeatable quality checks.

The next step is to apply these foundations through FastAPI. The goal is not to replace the existing architecture with framework code, but to use FastAPI as a new presentation boundary over clear application and domain responsibilities.
