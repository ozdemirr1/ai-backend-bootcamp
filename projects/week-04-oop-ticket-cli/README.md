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

## Current Files

- `oop_basics.py`: introductory class, object, and instance-method practice
- `models.py`: ticket enums and validated dataclass model
- `model_practice.py`: enum and dataclass behavior demonstration
- `test_models.py`: focused Ticket model tests

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

Run the model tests:

```bash
python -m pytest projects/week-04-oop-ticket-cli/test_models.py -v
```

## Current Behavior

The introductory practice creates two independent ticket objects, displays their summaries, and changes the status of one ticket through an instance method.

The domain model uses enums for controlled priority and status values. The Ticket dataclass rejects empty titles, non-positive IDs, raw string priorities, and raw string statuses.

## Planned Evolution

- Repository responsibility
- Service responsibility
- CLI integration

The project will avoid unnecessary inheritance and abstractions. New modules will be added only when their responsibilities are clear.
