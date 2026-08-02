# Week 04 Plan

## Date

3 August - 9 August

## Main Focus

- Python classes and objects
- Constructors and `self`
- Instance attributes and methods
- Encapsulation and basic inheritance
- Dataclasses and enums
- Object dependencies
- Modular project structure
- Clean-code principles
- OOP behavior tests

## Why This Week Exists

Week 02 produced a working ticket CLI, and Week 03 added reusable functions, exceptions, Pytest, Ruff, and a pull request workflow.

Before starting FastAPI, the CLI will be modeled with small objects and clear responsibilities. The goal is not to turn every function into a class. The goal is to understand when an object improves domain modeling, state management, testability, and maintainability.

## Learning Goals

- Explain the difference between a class and an object.
- Create objects with `__init__` and understand `self`.
- Separate instance data from instance behavior.
- Use a dataclass for a data-focused ticket model.
- Use enums for controlled status and priority values.
- Understand basic encapsulation.
- Recognize inheritance and avoid unnecessary inheritance hierarchies.
- Pass a repository dependency into a service.
- Separate model, repository, service, and CLI responsibilities.
- Test object behavior without using real application data.
- Apply clear naming and the single-responsibility principle.

## Daily Plan

### Monday

Classes, objects, constructors, and instance behavior.

Practice:

- Review the problem that classes solve.
- Compare a dictionary record with a small class instance.
- Create a simple example before modeling a ticket.
- Practice `class`, `__init__`, `self`, attributes, and methods.
- Explain the difference between a class and an object.

### Tuesday

Dataclasses, enums, and ticket domain modeling.

Practice:

- Compare a regular class with a dataclass.
- Create controlled ticket priority and status enums.
- Model a `Ticket` with explicit fields and type hints.
- Decide which validation belongs to the model.
- Add focused model tests.

### Wednesday

Repositories, services, and dependency logic.

Practice:

- Explain model, repository, and service responsibilities before coding.
- Create an in-memory `TicketRepository`.
- Create a `TicketService` for application rules.
- Pass the repository into the service constructor.
- Keep storage details outside the ticket model.

### Thursday

Modular project structure, encapsulation, and inheritance basics.

Practice:

- Split code into small modules.
- Protect object invariants through methods and validation.
- Learn basic inheritance with a small example.
- Compare inheritance with composition.
- Avoid forcing inheritance into the ticket CLI when it adds no value.

### Friday

Clean code, refactoring, and testing.

Practice:

- Review naming and single-responsibility principles.
- Remove duplication without creating unnecessary abstractions.
- Test model, repository, and service behavior.
- Run Pytest and Ruff.
- Document project setup and design decisions.

### Saturday

OOP ticket CLI integration and pull request review.

Practice:

- Connect the CLI to the service layer.
- Keep terminal input/output outside domain and repository code.
- Test valid and invalid ticket creation flows.
- Review the full branch diff.
- Open and review the Week 04 pull request.

### Sunday

Month 1 review and Week 05 preparation.

Practice:

- Complete `weekly-reports/week-04.md`.
- Review Week 04 interview questions.
- Update repository status and documentation.
- Evaluate the Month 1 success criteria.
- Prepare the Week 05 FastAPI plan without starting it early.

## Architecture Target

```text
CLI input/output
      |
      v
TicketService  ---> application rules
      |
      v
TicketRepository ---> ticket storage
      |
      v
Ticket model ---> ticket data and valid state
```

The dependency direction should remain clear: the CLI uses the service, and the service receives a repository. The ticket model should not read terminal input or open storage files.

## Code To Implement

- `TicketPriority` enum
- `TicketStatus` enum
- `Ticket` dataclass
- In-memory `TicketRepository`
- `TicketService`
- Small OOP-based ticket CLI
- Pytest tests for model, repository, and service behavior

## Planned Project Structure

```text
projects/week-04-oop-ticket-cli/
├── README.md
├── app.py
├── models.py
├── repositories.py
├── services.py
├── test_models.py
├── test_repositories.py
└── test_services.py
```

The structure is a target, not a reason to create empty or unnecessary modules. Each file should have a clear responsibility before it is added.

## Notes To Write

- `notes/python/oop-clean-code.md`

## Test Goals

- Ticket creation stores valid data.
- Invalid status and priority values are rejected safely.
- Repository operations do not use real Week 02 JSON data.
- Service rules are tested separately from terminal input.
- Tests do not depend on execution order.
- Pytest and Ruff pass before the pull request is merged.

## Git Workflow Goal

Use a feature branch for Week 04 work.

Planned branch:

```text
feature/week-04-oop-clean-code
```

Keep commits small and review the pull request before merging into `main`.

## Expected Commits

- `week-04: add OOP and clean code notes`
- `week-04: add ticket domain models`
- `week-04: add repository and service exercises`
- `week-04: add OOP ticket CLI tests`
- `week-04: complete OOP ticket CLI`
- `week-04: add weekly report`

## Interview Questions

- What is the difference between a class and an object?
- What does `self` represent?
- What is the purpose of `__init__`?
- What is the difference between a class attribute and an instance attribute?
- When is a dataclass useful?
- Why use an enum instead of uncontrolled strings?
- What is encapsulation?
- What is inheritance?
- When is composition safer than inheritance?
- What is a dependency?
- Why should a service receive its repository from outside?
- What is the single-responsibility principle?
- What should belong to a model, repository, service, and CLI?
- Why should domain tests avoid terminal input and real data files?

## Definition of Done

Week 04 is complete when:

- OOP and clean-code notes are written.
- Classes, objects, `self`, and constructors can be explained.
- Dataclass and enum exercises work.
- Basic inheritance and composition can be compared.
- Ticket model, repository, and service responsibilities are separated.
- The OOP ticket CLI works through the service layer.
- Model, repository, and service tests pass.
- Ruff passes without unresolved violations.
- The feature branch is reviewed and merged through a pull request.
- The Week 04 report is complete.

## Guardrails

- Do not convert every function into a class.
- Do not create inheritance only to demonstrate syntax.
- Do not introduce abstract base classes or design patterns before they solve a real problem.
- Do not mix terminal input/output with domain rules.
- Do not modify real Week 02 ticket data in tests.
- Do not start FastAPI before Week 05.
- Prefer small, testable changes over a full rewrite.
