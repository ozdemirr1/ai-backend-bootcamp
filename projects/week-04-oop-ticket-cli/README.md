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

## Current Files

- `oop_basics.py`: introductory class, object, and instance-method practice

## Run

From the repository root, activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the OOP basics practice:

```bash
python projects/week-04-oop-ticket-cli/oop_basics.py
```

## Current Behavior

The practice creates two independent ticket objects, displays their summaries, and changes the status of one ticket through an instance method.

## Planned Evolution

- Dataclass-based ticket model
- Priority and status enums
- Repository responsibility
- Service responsibility
- Isolated Pytest tests
- CLI integration

The project will avoid unnecessary inheritance and abstractions. New modules will be added only when their responsibilities are clear.
