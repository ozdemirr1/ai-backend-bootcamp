# SQLAlchemy Persistence Fundamentals

## Responsibility Boundaries

The Week 07 persistence stack has separate layers:

- PostgreSQL stores durable relational data and enforces constraints.
- Psycopg implements the PostgreSQL driver protocol used by Python.
- SQLAlchemy provides engine, connection, transaction, SQL expression, and ORM
  abstractions on top of the driver.
- Alembic will own explicit, versioned schema migration history.
- Pydantic Settings loads and validates application configuration.

An ORM does not replace PostgreSQL knowledge. SQLAlchemy-generated operations
must still be understood in terms of SQL, transactions, constraints, indexes,
and connection behavior.

## Synchronous First

The current FastAPI Ticket API uses synchronous routes and services. The first
database implementation therefore uses SQLAlchemy's synchronous API. This
keeps the initial learning scope focused on persistence mapping, sessions, and
transactions. Async database access can be evaluated later when the synchronous
lifecycle is understood and a measured need exists.

## Environment Configuration

The application requires `DATABASE_URL`. Pydantic Settings reads the value from
the process environment or a local `.env` file. `SecretStr` prevents the value
from appearing in ordinary settings representations.

The repository tracks `.env.example`, which documents the expected URL shape:

```text
postgresql+psycopg://APP_USER:URL_ENCODED_PASSWORD@DB_HOST:5432/APP_DATABASE
```

The real `.env` file and password are excluded from Git. A password containing
reserved URL characters must be URL-encoded before being placed in the URL.

Unit tests disable `.env` loading with `_env_file=None`. They provide synthetic
configuration directly, so results do not depend on a developer's machine and
do not contact a real database.

## Engine

An SQLAlchemy `Engine` holds the database dialect, driver configuration, and
connection pool. It is intended to be a long-lived application object.

Creating an engine is lazy. `create_engine()` validates and stores connection
configuration but normally does not open a PostgreSQL connection immediately.
The first operation that needs database access checks a connection out of the
pool.

`pool_pre_ping=True` checks a pooled connection before reuse. This helps replace
connections that PostgreSQL or the network has already closed.

## Connection

An SQLAlchemy `Connection` represents a checked-out database connection at the
Core layer. Calling `engine.connect()` crosses the lazy boundary and attempts a
real driver connection.

The Week 07 manual check executed a SQL statement through a Connection and
confirmed:

- the `postgresql+psycopg` dialect and driver combination;
- the `opsdesk_dev` database;
- the non-superuser `opsdesk_app` role;
- the PostgreSQL 18.6 server.

## Session and Session Factory

An ORM `Session` is not the same as a permanent database connection. It is a
unit-of-work and persistence context. It tracks ORM objects, coordinates SQL,
and obtains a pooled connection only when work requires one.

`sessionmaker` is a factory that creates independent Session instances. The
current factory uses:

- `bind=engine` to select the database engine;
- `autoflush=False` to keep flushing explicit while learning the lifecycle;
- `expire_on_commit=False` so committed attributes remain readable while an
  HTTP response is produced.

These options do not automatically commit application work. Transaction
ownership must still be defined explicitly.

FastAPI will eventually create one Session per request. A Session must not be
shared globally between concurrent requests.

## Transaction Lifecycle

The manual Session check demonstrated SQLAlchemy's lazy `autobegin` behavior:

```text
before the first query: no active transaction
after the first query: active transaction
```

Even a `SELECT` begins a database transaction when the Session first performs
work. Closing the Session releases its connection and ends an uncommitted
transaction. Future write workflows must choose `commit` or `rollback`
deliberately and verify both behaviors with isolated tests.

## Declarative Persistence Mapping

SQLAlchemy's declarative mapping connects a Python persistence class to table
metadata. `DeclarativeBase` owns the shared metadata registry, `Mapped[T]`
describes the Python-facing attribute type, and `mapped_column()` declares the
database-facing column behavior.

`TicketRecord` mirrors the durable `tickets` row rather than replacing the
domain `Ticket` model. The persistence record includes database concerns such
as:

- a `BIGINT GENERATED ALWAYS AS IDENTITY` primary key;
- `TEXT NOT NULL` business columns;
- a server-owned `open` status default;
- timezone-aware server timestamp defaults;
- named title, priority, status, and timestamp check constraints.

The compiled PostgreSQL DDL was inspected directly. This caught an important
default-expression distinction: `server_default=text("'open'")` produces
`DEFAULT 'open'`, while passing a string that already contains quotes would
produce a value with additional literal quote characters.

The ORM metadata intentionally repeats the Week 06 database constraints.
Alembic will use this metadata to create reviewable migrations, while
PostgreSQL remains the final authority that enforces the resulting schema.

## Persistence and Domain Mapping

Persistence records keep database strings for priority and status because the
current PostgreSQL schema uses `TEXT` plus named check constraints. The domain
model keeps `TicketPriority` and `TicketStatus` enums and owns behavior such as
title normalization and state changes.

The mapper boundary performs explicit conversion:

```text
TicketRecord string values -> Ticket domain enums
Ticket domain enums        -> existing TicketRecord string values
```

Mapping an existing domain Ticket back onto a record updates only title,
priority, and status. It rejects mismatched identifiers before mutation and
does not change the database-owned identity or timestamp fields.

A new record is not created by copying a domain Ticket identifier. New Ticket
identity generation must remain owned by PostgreSQL's `GENERATED ALWAYS`
column. The repository creation workflow will handle that lifecycle later.

## Verified Tests

Five focused unit tests currently verify that:

- `DATABASE_URL` can be read from the environment;
- missing required configuration fails clearly;
- the secret URL is hidden from the settings representation;
- the Engine uses PostgreSQL with the Psycopg driver and expected URL parts;
- the Session factory uses the intended Engine and lifecycle options.

Four persistence-model tests additionally verify table and column metadata,
database-generated identity configuration, defaults, timezone-aware
timestamps, nullability, and the four named check constraints.

Five mapper tests verify valid record-to-domain conversion, rejection of
invalid persistence enum values, business-field updates, preservation of
identity and timestamps, and non-mutating rejection of mismatched identifiers.

These are unit tests, not PostgreSQL integration tests. Dedicated integration
tests will later use `opsdesk_test`; they must never destructively isolate data
inside `opsdesk_dev`.

After adding the declarative model and mapper tests, the complete repository
suite contained 121 tests. All 121 passed together with Ruff lint, Ruff
formatting, and diff checks.
