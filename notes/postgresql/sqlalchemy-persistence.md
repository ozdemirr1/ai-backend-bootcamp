# SQLAlchemy Persistence Fundamentals

## Responsibility Boundaries

The Week 07 persistence stack has separate layers:

- PostgreSQL stores durable relational data and enforces constraints.
- Psycopg implements the PostgreSQL driver protocol used by Python.
- SQLAlchemy provides engine, connection, transaction, SQL expression, and ORM
  abstractions on top of the driver.
- Alembic owns explicit, versioned schema migration history.
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

FastAPI now obtains a Session through a request dependency. The shared object
is the Session factory, not a mutable Session. Sessions must not be shared
globally between concurrent requests.

## Transaction Lifecycle

The manual Session check demonstrated SQLAlchemy's lazy `autobegin` behavior:

```text
before the first query: no active transaction
after the first query: active transaction
```

Even a `SELECT` begins a database transaction when the Session first performs
work. Closing the Session releases its connection and ends an uncommitted
transaction. The request dependency now chooses `commit` or `rollback`
explicitly; successful repository persistence and rollback behavior have also
been exercised with isolated PostgreSQL tests.

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
Alembic uses this metadata to create reviewable migrations, while
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

A new record is not created by copying a domain Ticket identifier. `NewTicket`
represents validated creation input without a durable identifier. The
SQLAlchemy repository converts it into a new `TicketRecord`, flushes the row,
loads the PostgreSQL-generated identity, and returns a complete domain
`Ticket`.

## Alembic Migration Lifecycle

SQLAlchemy metadata describes the desired application schema, while Alembic
stores the ordered operations required to move a real database between schema
versions. Calling `Base.metadata.create_all()` is intentionally not part of the
application lifecycle because it does not provide a reviewable, reversible
history of schema changes.

The Alembic environment loads the same secret-aware `DATABASE_URL` setting as
the application, but `alembic.ini` contains no connection credentials. During
the Week 07 migration exercise, `ALEMBIC_DATABASE_NAME` replaced only the
database component of that URL so all destructive migration checks targeted
the isolated `opsdesk_migration_dev` database rather than `opsdesk_dev`.

`target_metadata = Base.metadata` allows autogeneration to compare the
declarative schema with PostgreSQL. Type and server-default comparison are
enabled in both offline and online configuration. Autogeneration remains a
proposal rather than an approval step: the generated Python operations and
offline SQL must be reviewed before an upgrade is applied.

The initial revision creates:

- the six-column `tickets` table;
- a database-generated `BIGINT` identity primary key;
- database-owned status and timestamp defaults;
- four named check constraints; and
- the `(status, ticket_id)` composite listing index.

Alembic records the applied revision in its own `alembic_version` table. The
initial workflow was verified by upgrading an empty database, inspecting the
resulting PostgreSQL catalog, downgrading to `base`, and upgrading to `head`
again. `alembic check` then reported no difference between `Base.metadata` and
the migrated database.

Offline mode generated the complete transactional SQL without applying it. It
included `BEGIN`, the Alembic version table, the Ticket table and index, the
revision insert, and `COMMIT`. Online mode instead used a live SQLAlchemy
Connection that remained open for the complete migration transaction.

## Repository Boundary

`TicketRepository` is a structural `Protocol` describing the storage behavior
required by `TicketService`: create, lookup, ordered listing, update, and
delete. The service depends on that contract and does not import SQLAlchemy,
Session, persistence records, or PostgreSQL exceptions.

The in-memory and SQLAlchemy repositories implement the same protocol. The
in-memory implementation remains useful for deterministic unit and HTTP tests.
`SqlAlchemyTicketRepository` maps the same workflows onto a real Session and
PostgreSQL. This keeps storage replacement at the composition boundary instead
of spreading database knowledge through the service and route layers.

`NewTicket` represents a valid Ticket request before persistence assigns an
identity. `Ticket` represents a domain entity with a positive durable
identifier. This distinction prevents the service from inventing database
identifiers and keeps `GENERATED ALWAYS AS IDENTITY` authoritative.

The repository's create operation translates SQLAlchemy integrity failures into
`TicketRepositoryConflictError`. The service then translates that persistence-
neutral error into its existing application-level conflict error. This keeps
expected creation conflicts independent of the driver. It is not blanket
translation of every database failure: update, delete, and commit failures
must also be considered in the HTTP error-path review.

## Flush, Refresh, Commit, and Rollback

`flush()` sends pending SQL inside the current transaction. It allows the
repository to receive generated identities and detect database constraint
failures without deciding whether the complete use case should be committed.
`refresh()` reloads database-owned values such as server defaults into a
persistence record.

`commit()` makes the complete transaction durable and visible to other
connections. `rollback()` discards its uncommitted effects. The repository
does neither: transaction ownership belongs to the caller. This permits the
request boundary to compose several repository operations into one
atomic unit of work and roll all of them back when any step fails.

After an `IntegrityError` during flush, the Session transaction is failed and
cannot continue normally until its owner rolls it back. Translating the
exception does not repair or end the transaction; it only preserves the
application boundary.

## Timestamp Update Behavior

The `updated_at` mapping uses a server default for insertion and SQLAlchemy's
`onupdate=func.current_timestamp()` behavior for ORM-generated updates. The
repository therefore includes `CURRENT_TIMESTAMP` when it flushes a changed
Ticket record.

PostgreSQL `CURRENT_TIMESTAMP` is the start time of the current transaction.
The integration test creates and updates its Ticket in separate transactions
so it can prove that `updated_at` advances beyond `created_at`. This mapping
does not create a PostgreSQL update trigger: direct SQL writers must still set
`updated_at` explicitly if they bypass the ORM repository.

## Dedicated-Database Integration Testing

PostgreSQL repository tests are disabled unless `RUN_DATABASE_TESTS=1` is set.
They derive the connection from the normal secret-aware configuration but
replace only the database component with `opsdesk_test`. Before running, the
session-scoped guard verifies the exact database name, rejects a superuser
role, and requires the Alembic-managed `tickets` table.

The per-test fixture refuses to delete pre-existing data. It stops when the
Ticket table is not empty, then wraps ordinary test work in an external
transaction that is rolled back during teardown. Commit and visibility tests
use separate Sessions and clean only the identifiers they created. This makes
destructive intent explicit and prevents accidental isolation against
`opsdesk_dev`.

The integration suite verifies database-generated identity, defaults, CRUD,
ordered listing, missing rows, flush without commit, cross-Session commit
visibility, rollback invisibility, and timestamp advancement. Rolled-back
identity values are not reused, so gaps in generated identifiers remain
expected behavior.

## Verified Tests

Five focused unit tests currently verify that:

- `DATABASE_URL` can be read from the environment;
- missing required configuration fails clearly;
- the secret URL is hidden from the settings representation;
- the Engine uses PostgreSQL with the Psycopg driver and expected URL parts;
- the Session factory uses the intended Engine and lifecycle options.

Five persistence-model tests additionally verify table and column metadata,
database-generated identity configuration, defaults, timezone-aware
timestamps, nullability, the four named check constraints, and the composite
status-listing index.

Five mapper tests verify valid record-to-domain conversion, rejection of
invalid persistence enum values, business-field updates, preservation of
identity and timestamps, and non-mutating rejection of mismatched identifiers.

Eleven opt-in PostgreSQL integration tests verify the SQLAlchemy repository and
transaction lifecycle against the dedicated `opsdesk_test` database. They must
never run destructive isolation against `opsdesk_dev`.

The complete 27 August quality run collected 143 tests. Without database tests,
132 passed and 11 integration tests were skipped. With
`RUN_DATABASE_TESTS=1`, all 143 passed. Dependency consistency, Ruff lint, Ruff
formatting, and Git diff checks also passed, and the final `opsdesk_test`
Ticket count was zero.

## FastAPI Lifespan and Request Transactions - 28 August

The application factory creates the FastAPI instance and includes the router.
The default lifespan loads settings at startup, constructs the Engine and
Session factory, and stores the factory in `app.state`. Engine disposal is in
`finally`, including the path where Session factory creation fails. Importing
the application does not read the local settings or open a database connection.

The lifespan is an async context manager because of the ASGI application
lifecycle. Database Sessions, repository operations, and routes remain
synchronous; no async SQLAlchemy or new driver was introduced.

The dependency chain is:

```text
app.state.session_factory -> get_session -> SQLAlchemy repository -> TicketService
```

`get_session` yields one Session and owns its transaction boundary:

- Normal completion: commit, then close.
- An exception during the request: rollback, re-raise, then close.
- An exception during commit: rollback, re-raise, then close.

The commit is inside the same `try` as `yield`, not outside the exception
handler. `Depends(get_session, scope="function")` requests cleanup before the
HTTP response is sent. This is important because a successful route return is
not itself proof that the database transaction committed.

Eight database tests now cover the original two factories plus six Session
and lifespan scenarios. These lifecycle tests use mocks, so their success
proves control flow without proving every real HTTP/database failure outcome.

## Fast Tests Versus PostgreSQL HTTP Tests

The existing API fixture creates a fresh application with
`lifespan_handler=None` and overrides `get_ticket_service` with an in-memory
service. Disabling the lifespan alone does not select in-memory storage; the
explicit override does that. All 31 existing API tests passed alongside the
eight database tests (`39 passed`).

The first PostgreSQL API test disables only production startup and supplies
the guarded test Engine's Session factory. It leaves `get_session` and
`get_ticket_service` unchanged, so the POST uses the real transaction and
repository chain. The test checks `201`, a generated identifier, server-owned
status, committed visibility through a separate connection, and a subsequent
HTTP GET. Cleanup removes only its unique probe title in `finally`.

That focused test passed and the final `opsdesk_test` Ticket count was zero.
Although its name is `test_create_ticket_commits_before_response`, the current
assertions observe state after `TestClient` returns. They prove successful
commit visibility, not by themselves the ordering of response transmission or
the absence of a false success when commit fails.

On 29 August, the PostgreSQL HTTP suite grew to eight scenarios. It verifies
committed create/read behavior, filtered and limited listing, committed update
and delete operations, `404` and `422` responses without state changes,
rollback after a deliberately flushed write, commit failure without a false
`201`, and a distinct Session for each request.

The rollback probe is a hidden route added only to a fixture-created test
application. The commit failure uses a test-only `Session` subclass. Neither is
part of the production application. This bounded fault injection exercises the
real dependency finalizer and PostgreSQL transaction while keeping the failure
mechanism explicit. A natural database-backed `409` was not manufactured:
Ticket titles are not unique, and adding a uniqueness rule solely for a test
would change the domain. The existing fast HTTP contract test continues to
cover application-error-to-`409` translation.

The manual restart check safely changed only the process-local database target
to `opsdesk_test`, created one identified Ticket, stopped Uvicorn, restarted it,
and retrieved the same row. Deleting it through the API produced `204`; a later
lookup produced `404`, and PostgreSQL confirmed zero remaining Tickets. This
proves persistence beyond both a request and an application process lifetime.

The final 29 August runs passed 138 tests with 19 integration skips under
`RUN_DATABASE_TESTS=0` and all 157 tests under `RUN_DATABASE_TESTS=1`. Ruff,
formatting for 90 files, dependency checks, Git diff checks, Alembic head state,
and the final zero-row test-database check also passed.

For the manual runtime check, inspect the configured database without printing
the password or complete URL. `ALEMBIC_DATABASE_NAME` selects a migration
target only; the API still uses `DATABASE_URL`. Do not assume a migration
performed on one database prepared a different database for the API.
