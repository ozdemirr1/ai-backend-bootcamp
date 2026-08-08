# Week 04 OOP Ticket CLI

## Goal

This project practices Python object-oriented programming and clean-code principles through a small OpsDesk ticket domain.

The project begins with a regular `Ticket` class and will grow incrementally as each responsibility is understood.

## Current Topics

- Classes and objects
- `__init__` and `self`
- Instance attributes
- Instance methods
- Object state changes
- Returning values from methods
- Small method responsibilities
- Dataclasses
- Priority and status enums
- `__post_init__` validation
- `TypeError` and `ValueError`
- TDD Red and Green phases
- Focused model tests
- In-memory repository operations
- Service-layer application rules
- Constructor dependency injection
- Duplicate ticket ID protection
- Isolated repository and service tests
- Controlled status changes and model invariants
- Basic inheritance and method overriding
- Composition and constructor dependencies
- Separation of returned values from terminal output
- Stronger lookup and failed-operation tests
- Service-level ticket listing
- Ruff lint and format checks

## Current Files

- `oop_basics.py`: introductory class, object, and instance-method practice
- `models.py`: ticket enums and validated dataclass model
- `model_practice.py`: enum and dataclass behavior demonstration
- `test_models.py`: focused Ticket model tests
- `repositories.py`: in-memory ticket storage and lookup operations
- `services.py`: ticket creation workflow and duplicate ID rule
- `test_repositories.py`: repository behavior and encapsulation tests
- `test_services.py`: service workflow and dependency tests
- `inheritance_practice.py`: small `Employee` and `SupportAgent` inheritance example
- `composition_practice.py`: formatter dependency and notification service example
- `oop_ticket_cli.py`: terminal presentation layer and application composition root
- `test_cli_app.py`: isolated CLI output and user-input behavior tests

## Run

From the repository root, activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the OOP basics practice:

```bash
python projects/week-04-oop-ticket-cli/oop_basics.py
```

Run the dataclass and enum practice:

```bash
python projects/week-04-oop-ticket-cli/model_practice.py
```

Run the inheritance and composition examples:

```bash
python projects/week-04-oop-ticket-cli/inheritance_practice.py
python projects/week-04-oop-ticket-cli/composition_practice.py
```

Run the OOP ticket CLI:

```bash
python projects/week-04-oop-ticket-cli/oop_ticket_cli.py
```

Run the model tests:

```bash
python -m pytest projects/week-04-oop-ticket-cli/test_models.py -v
```

Run the repository and service tests:

```bash
python -m pytest projects/week-04-oop-ticket-cli/test_repositories.py -v
python -m pytest projects/week-04-oop-ticket-cli/test_services.py -v
```

Run the CLI tests:

```bash
python -m pytest projects/week-04-oop-ticket-cli/test_cli_app.py -v
```

Run all project tests:

```bash
python -m pytest projects/week-04-oop-ticket-cli -v
```

Run the project quality checks:

```bash
ruff format --check projects/week-04-oop-ticket-cli
ruff check projects/week-04-oop-ticket-cli
python -m pytest projects/week-04-oop-ticket-cli -q
```

## Current Behavior

The introductory practice creates two independent ticket objects, displays their summaries, and changes the status of one ticket through an instance method.

The domain model uses enums for controlled priority and status values. The Ticket dataclass rejects empty titles, non-positive IDs, raw string priorities, and raw string statuses.

The in-memory repository saves, lists, and finds tickets without reading or changing the Week 02 JSON data. `list_all()` returns a copy of its internal list to protect the collection from external mutation.

The service receives its repository through constructor injection. It creates valid tickets, stores them through the repository, and rejects duplicate ticket IDs before stored state changes.

The service also exposes ticket listing so the CLI does not need to access repository storage operations directly. Invalid model input is rejected before `save()`, leaving repository state unchanged.

The Ticket model validates status changes through a public behavior method. The standalone inheritance and composition examples demonstrate the difference between **is-a** and **has-a** relationships without adding an unnecessary class hierarchy to the ticket domain.

The CLI constructs the repository and service at the application boundary. It communicates only with the service during ticket operations, converts terminal input into domain values, and turns expected validation failures into clear user-facing messages. The in-memory repository keeps tickets available during one CLI session without writing to the Week 02 JSON data.

CLI tests replace interactive input with controlled values and capture terminal output. They cover empty and populated ticket lists, successful creation, invalid priorities, invalid titles, invalid menu choices, and clean exit behavior.

## Planned Evolution

- Persistent repository implementation
- Additional ticket operations such as status updates

The project will avoid unnecessary inheritance and abstractions. New modules will be added only when their responsibilities are clear.
