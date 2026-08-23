# Week 07 Plan

## Date

24 August - 30 August 2026

## Main Focus

- SQLAlchemy 2 fundamentals
- Psycopg PostgreSQL connectivity
- Environment-based database configuration
- Engine, connection, session, and transaction responsibilities
- Declarative persistence models
- Explicit ORM-to-domain mapping
- Alembic migration fundamentals
- PostgreSQL repository implementation
- FastAPI request-scoped database sessions
- Isolated PostgreSQL integration tests

## Main Goal

Replace the temporary in-memory storage boundary of the Week 05 Ticket API with
a PostgreSQL-backed repository while preserving the existing domain, service,
and HTTP responsibilities.

Week 07 is an integration week. The goal is not to redesign the API or add new
product features. It is to connect the application architecture already built
in Week 05 to the relational model understood in Week 06.

## Why This Week Matters

Writing SQL directly established the behavior that an ORM will later express.
SQLAlchemy should make persistence code composable and testable without hiding
transactions, constraints, joins, or generated SQL. Alembic should preserve an
explicit, reviewable history of schema changes instead of relying on implicit
table creation at application startup.

## Planned Architecture

```text
HTTP client
    |
    v
FastAPI route --------> request and response contracts
    |
    v
TicketService --------> application workflows
    |
    v
Repository boundary --> storage operations expected by the service
    |
    v
SQLAlchemy repository -> ORM/domain mapping and queries
    |
    v
Session --------------> unit of work and transaction boundary
    |
    v
Psycopg --------------> PostgreSQL driver
    |
    v
PostgreSQL -----------> durable data and constraints

Alembic --------------> independent, versioned schema history
```

## Architecture Rules

- Routes must not write SQL or construct persistence models directly.
- The service must not depend on FastAPI or HTTP exceptions.
- SQLAlchemy sessions must not leak into domain objects or response schemas.
- Persistence models must remain separate from the existing domain model when
  their responsibilities differ.
- Driver and SQLAlchemy exceptions must not become public API responses.
- Transaction ownership must be explicit and testable.
- Alembic migrations, not application startup, must own schema evolution.
- Existing domain invariants and API validation must not be weakened.

## Technical Direction

### Synchronous First

Use SQLAlchemy's synchronous workflow first. The current FastAPI routes and
service are synchronous, so adding asynchronous database access now would mix
two learning problems and obscure session and transaction fundamentals.

### Configuration

- Read the database URL from an environment variable.
- Never commit a real password, `.env` file, or complete local connection URL.
- Fail clearly when required configuration is missing.
- Keep development and test database URLs separate.
- Use a dedicated `opsdesk_test` database for integration tests.
- Never run destructive test isolation against `opsdesk_dev`.

### Dependency Workflow

- Verify the latest stable, mutually compatible dependency versions before
  installation.
- Add only the dependencies required for SQLAlchemy, Psycopg, Alembic, and
  configuration.
- Record dependency intent in `pyproject.toml` and exact resolution in
  `uv.lock`.
- Re-run lock, synchronization, package compatibility, lint, formatting, and
  test checks after dependency changes.

## Daily Plan

### Monday - Persistence Tools and Configuration

- Create `feature/week-07-sqlalchemy-alembic` from updated `main`.
- Explain ORM, driver, migration, engine, connection, session, and transaction
  responsibilities before writing code.
- Verify compatible package versions from primary documentation.
- Add the selected runtime and development dependencies with `uv`.
- Add environment-based database configuration without tracked secrets.
- Create a minimal connection check through the non-superuser application role.
- Document why the first implementation remains synchronous.

### Tuesday - SQLAlchemy Models and Mapping

- Learn SQLAlchemy 2 declarative mapping and typed mapped columns.
- Map Ticket persistence fields without replacing the domain model.
- Preserve identity, defaults, nullability, constraints, and timestamps.
- Decide how priority and status cross the persistence boundary.
- Write explicit conversion between persistence records and domain objects.
- Compare database constraints with ORM declarations and domain validation.
- Add focused mapping tests.

### Wednesday - Alembic Fundamentals

- Initialize Alembic in the FastAPI project.
- Connect Alembic configuration to the environment-based database URL.
- Create and review an initial migration.
- Inspect generated SQL instead of trusting autogeneration blindly.
- Upgrade an empty development database to the latest revision.
- Downgrade and upgrade again to demonstrate reversible schema history.
- Confirm that `Base.metadata.create_all()` is not used as a migration system.

### Thursday - PostgreSQL Repository

- Implement Ticket add, lookup, list, update, and delete persistence operations.
- Use SQLAlchemy 2 `select()` statements and explicit result handling.
- Clarify `flush`, `commit`, `rollback`, `refresh`, and identity generation.
- Preserve the service-facing repository behavior where appropriate.
- Translate expected persistence conflicts into application-level errors.
- Add repository integration tests against `opsdesk_test`.

### Friday - FastAPI Database Integration

- Provide a request-scoped SQLAlchemy session through FastAPI dependency
  injection.
- Compose the PostgreSQL repository and Ticket service without leaking the
  session into route code.
- Connect create, list, detail, update, and delete routes to durable storage.
- Define commit and rollback behavior for successful and failed requests.
- Verify that data remains available after application restart.
- Preserve intentional `201`, `204`, `404`, `409`, and `422` behavior.

### Saturday - Isolation and Complete Verification

- Recreate or migrate the dedicated test database safely.
- Make database tests independent of execution order.
- Ensure each test leaves a predictable database state.
- Test persistence, rollback, uniqueness, missing resources, and invalid input.
- Run the complete repository quality suite.
- Review diffs for credentials, local paths, and destructive database targets.
- Update README, notes, decisions, and weekly status.
- Open and review the Week 07 pull request when the work is complete.

### Sunday - Review and Transition

- Answer SQLAlchemy, session, transaction, and migration interview questions.
- Write the Week 07 report.
- Merge the reviewed pull request and clean feature branches.
- Prepare Week 08 without starting authentication early.

## Likely Project Changes

The exact structure will be chosen after Monday's architecture review. Likely
additions include:

- `alembic.ini`
- an `alembic/` migration directory
- `ticket_api/database.py`
- persistence model and mapping modules
- a SQLAlchemy Ticket repository
- database integration tests
- environment and migration instructions in the project README

Files should be added only after their boundaries can be explained. A new file
is not automatically a better abstraction.

## Test Plan

- Missing database configuration fails clearly.
- A session can connect using the expected non-superuser role and database.
- A persistence row maps to a valid domain Ticket.
- A domain Ticket maps to valid persistence values.
- Creating a Ticket returns its database-generated identifier.
- Created data is visible in a new session after commit.
- Rolled-back data is not visible in a new session.
- Listing and lookup return the intended records.
- Updating changes only requested fields and advances `updated_at`.
- Deleting removes the intended Ticket and respects cascade behavior.
- Duplicate or invalid persistence writes do not leave partial state.
- A missing Ticket still produces the expected application and HTTP behavior.
- API tests remain isolated and independent of execution order.
- The existing non-database test suite continues to pass.

## Verification Goals

- The database URL is supplied only through environment configuration.
- The application connects through `opsdesk_app`, not a superuser.
- Alembic can build the schema from an empty database.
- Migration upgrade, downgrade, and re-upgrade behavior is understood.
- ORM mappings preserve the Week 06 relational constraints.
- SQLAlchemy-generated queries can be related back to equivalent SQL.
- Session and transaction ownership can be explained.
- The PostgreSQL repository satisfies the application workflow.
- The FastAPI API persists data across process restarts.
- Integration tests use only the dedicated test database.
- Ruff, formatting, dependency, and full test checks pass.
- No credentials or machine-specific connection values are tracked.

## Git Workflow Goal

Planned branch:

```text
feature/week-07-sqlalchemy-alembic
```

Likely commit themes:

- `week-07: add database configuration and session setup`
- `week-07: map ticket persistence models`
- `week-07: add initial Alembic migration`
- `week-07: implement PostgreSQL ticket repository`
- `week-07: connect FastAPI routes to PostgreSQL`
- `week-07: add database integration tests`
- `week-07: complete SQLAlchemy persistence workflow`

Commit messages will reflect the actual completed changes rather than being
used as a fixed checklist.

## Interview Questions

- What problems do Psycopg, SQLAlchemy, and Alembic solve separately?
- What is the difference between an engine, connection, and session?
- Is a SQLAlchemy session the same as a database connection?
- What is a unit of work?
- What are `flush`, `commit`, `rollback`, and `refresh`?
- When does SQLAlchemy obtain a database connection from the pool?
- Why should a session normally be request-scoped in FastAPI?
- Why should ORM models not automatically replace domain models?
- What is the identity map?
- What is the difference between eager and lazy loading?
- What problem does an N+1 query create?
- Why are migrations preferable to `create_all()` for schema evolution?
- What can Alembic autogeneration detect, and what must still be reviewed?
- Why should migrations be tested in both upgrade and downgrade directions?
- How should database constraint errors cross the repository boundary?
- Why must integration tests use a separate database?
- How can tests isolate committed database state?
- Why are secrets and complete database URLs excluded from Git?

## Definition of Done

Week 07 is complete when:

- SQLAlchemy, Psycopg, and Alembic responsibilities can be explained.
- Database configuration is environment-based and contains no tracked secrets.
- The Ticket persistence mapping preserves the relational model.
- Alembic owns a reviewed and repeatable schema history.
- A PostgreSQL repository supports the Ticket service workflows.
- FastAPI uses request-scoped database sessions through dependency injection.
- API data survives application restart.
- Database integration tests are isolated in `opsdesk_test`.
- Existing application behavior and domain invariants remain protected.
- Complete quality, dependency, and test checks pass.
- The Week 07 feature branch is reviewed and merged through a pull request.

## Guardrails

- Do not commit passwords, `.env` files, or complete connection URLs.
- Do not run integration tests against `opsdesk_dev` or another valuable
  database.
- Do not give the runtime application role superuser privileges.
- Do not leak sessions or ORM records into HTTP response contracts.
- Do not weaken domain rules merely to simplify persistence.
- Do not accept generated migrations without reading their operations.
- Do not use `create_all()` as a substitute for Alembic migrations.
- Do not introduce asynchronous SQLAlchemy before the synchronous lifecycle is
  understood.
- Do not add authentication, Docker, Redis, background jobs, or AI features
  before their planned roadmap stages.
- Keep every persistence change connected to tests and documentation.
