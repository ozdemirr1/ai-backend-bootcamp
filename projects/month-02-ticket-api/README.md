# Month 02 Ticket API

## Goal

Build a small, tested FastAPI application while learning the request lifecycle,
ASGI, Uvicorn, route handling, validation, and API documentation.

## Current Scope

- Minimal FastAPI application
- Health endpoint
- Ticket collection and detail route examples
- Typed path and query parameters
- Pydantic request body schema
- Strict partial-update request schema
- Explicit ticket response schema
- Request normalization and automatic validation
- Ticket domain model and invariants
- Domain-safe title, priority, and status changes
- Typed SQLAlchemy Ticket persistence record
- Explicit persistence-to-domain mapping
- Database identity, default, timestamp, and constraint metadata tests
- Reviewed and reversible Alembic schema history
- Composite index for status-filtered Ticket listing
- Storage-independent Ticket repository protocol
- In-memory ticket repository
- PostgreSQL-backed SQLAlchemy Ticket repository
- Explicit repository flush and caller-owned transaction boundaries
- Ticket application service with complete CRUD workflows
- Dependency-injected FastAPI routes
- Application factory and startup/shutdown database lifespan
- Request-scoped Sessions with explicit commit, rollback, and cleanup
- Explicit HTTP status and application-error mapping
- Isolated endpoint, schema, domain, repository, and service tests
- Dedicated-database PostgreSQL repository integration tests
- Eight PostgreSQL HTTP transaction and lifecycle integration tests
- User domain, persistence, mapping, and repository boundaries
- Nullable Ticket ownership foreign key and reviewed Alembic expand migration
- Strict registration request and public User response contracts
- Injected registration service with Argon2id password hashing
- `POST /auth/register` with duplicate-conflict and transaction rollback tests
- Strict login and bearer-token response contracts
- Deterministic UTC clock boundary and fixed-algorithm JWT manager
- Generic, storage-independent authentication service with a cached real
  Argon2id dummy-verification path
- JSON `POST /auth/login` with one public invalid-credential contract
- Bearer-token current-User resolution backed by current database state
- Protected `GET /users/me`
- Authenticated Ticket creation with server-derived ownership
- Authenticated, owner-scoped Ticket collection queries
- Automatic OpenAPI schema and Swagger UI
- Endpoint testing without a manually running server

## Verified Environment

The following stable versions were verified on 10 August 2026:

- Python 3.14.7
- uv 0.12.3
- FastAPI 0.141.1
- Uvicorn 0.52.1
- Pydantic 2.13.4
- HTTPX2 2.10.0
- Pytest 9.1.1
- Ruff 0.16.2

The Week 07 persistence foundation adds the following verified versions:

- SQLAlchemy 2.0.52
- Psycopg 3.3.4
- Alembic 1.19.1
- Pydantic Settings 2.15.0

The Week 08 authentication foundation adds the following verified versions:

- pwdlib 0.3.1
- Argon2 CFFI 25.1.0
- PyJWT 2.13.0
- email-validator 2.3.0

## Database Configuration Foundation

The application reads its PostgreSQL connection URL from the required
`DATABASE_URL` environment variable. Copy the tracked example locally and
replace every placeholder without committing the resulting file:

```bash
cp .env.example .env
```

The URL uses SQLAlchemy's explicit Psycopg driver name:

```text
postgresql+psycopg://APP_USER:URL_ENCODED_PASSWORD@DB_HOST:5432/APP_DATABASE
```

The real `.env` file is ignored by Git. Passwords containing URL-reserved
characters must be URL-encoded. Do not paste the real URL into source code,
tests, documentation, terminal screenshots, or Git history.

`ticket_api.config` loads and validates settings. `ticket_api.database`
contains testable Engine and Session factory functions. Engine creation is
lazy: a real connection is opened only when a Connection or Session first
executes database work.

## Password and Token Configuration Foundation

`ticket_api.passwords.PasswordHasher` is the application boundary around
pwdlib's recommended Argon2 configuration. `RegistrationService` receives the
smaller `PasswordHashing` protocol, while dependency composition supplies the
real implementation. The plaintext password is never recoverable from
the stored value; verification repeats the password-hashing calculation using
the algorithm parameters and salt encoded in the stored hash.

The application also requires `JWT_SECRET`. Pydantic represents it as a
`SecretStr` so ordinary settings representations mask the value. Masking is
not encryption: application code can still retrieve the value when signing or
validating a token, so it must not be printed, returned, or committed. A
minimum length rejects obvious placeholder-sized secrets but does not make a
predictable value secure; local secrets must be generated randomly.

`ACCESS_TOKEN_EXPIRE_MINUTES` defaults to `30` and accepts values from `1`
through `1440`. `JwtAccessTokenManager` signs with server-configured HS256 and
decodes with the same fixed accepted algorithm. It issues only `sub`, `iat`,
and `exp`, requires those claims during validation, and converts `sub` back to
a positive User identifier. JWT payloads are signed rather than encrypted and
must not contain passwords, password hashes, secrets, or other sensitive User
records.

The time source is injected through a small `Clock` protocol. `SystemClock`
provides timezone-aware UTC in production, while frozen test clocks make
expiration behavior deterministic. Token tests reject modified signatures,
wrong secrets, unsupported algorithms, expired tokens, missing claims, invalid
subjects, and timezone-naive issuance times.

`AuthenticationService` orchestrates normalized User lookup, password
verification, active-state enforcement, and token issuance behind narrow
protocols. Missing Users, incorrect passwords, and inactive Users share one
generic failure and never issue a token. A dummy-hash path prevents an
immediate missing-User exit. Production composition generates and caches a
valid Argon2id dummy hash once per process. The JSON login route returns a
bearer token, while protected dependencies decode it and reload the current
active User from PostgreSQL instead of trusting stale account state in a JWT.

## User Identity Foundation

`ticket_api.user_models` defines a stable database-generated User identity,
normalized email login field, internal password-hash value, active state, and
the bounded `member`/`admin` role set. Ordinary `NewUser` registration data has
no role field; elevated access is never accepted from untrusted client input.

Email syntax is validated through the maintained `email-validator` library
without DNS checks. The application stores and looks up one normalized,
case-folded account identity. Email remains mutable login data; relationships
and future JWT subject claims use immutable `user_id` instead.

`UserRecord` is the separate SQLAlchemy persistence representation. PostgreSQL
owns the generated identity and safe member/active defaults, and named
constraints protect email uniqueness, normalized storage, allowed roles, and
timestamp ordering. Explicit mapper functions cross between registration,
persistence, and domain representations without allowing registration input
to assign privileged fields.

The User repository has in-memory and SQLAlchemy implementations behind one
service-facing protocol. Alembic revision `e98825c4d6b6` creates `users` and
adds nullable Ticket `owner_id` as the safe expand phase for historical rows.
The foreign key uses `ON DELETE RESTRICT`; backfill and a later non-null
contract remain future explicit changes.

## Registration Workflow

`POST /auth/register` accepts only a validated email and a 12-to-128-character
password. Registration validates identity before performing the deliberately
expensive hash, stores only an Argon2id encoding, and lets PostgreSQL assign the
User identity, `member` role, and active state. Duplicate normalized identities
return `409 Conflict` and cause the request transaction to roll back.

The public response exposes only User identity, normalized email, role, and
active state. Plaintext passwords and password hashes are never returned.
Fast tests replace repositories and hashing through dependency injection;
guarded PostgreSQL tests retain the real request-scoped Session, repository,
Argon2id hashing, commit, conflict rollback, and cleanup chain.

## Persistence Mapping Foundation

`ticket_api.persistence_models` defines a typed SQLAlchemy `TicketRecord` that
mirrors the constrained PostgreSQL `tickets` table. The record preserves the
database-generated identity, server defaults, timezone-aware timestamps,
nullability, named check constraints, and justified status-listing index
established during Week 06.

The persistence record remains separate from the domain `Ticket`. Database
priority and status strings cross the boundary through explicit mapper
functions, which convert them to domain enums and apply domain business fields
back to an existing record without overwriting identity or timestamps.

`TicketService` now depends on the storage-independent `TicketRepository`
protocol rather than a concrete implementation. The in-memory repository
continues to support fast unit and API tests, while
`SqlAlchemyTicketRepository` implements the same service-facing operations
against PostgreSQL.

The SQLAlchemy repository owns queries, persistence mapping, `flush()`, and
`refresh()` where server-generated values must be loaded. It deliberately does
not call `commit()` or `rollback()`. Transaction ownership remains outside the
repository so a caller can compose multiple operations into one atomic unit of
work. The default application now composes the SQLAlchemy repository and
service through a request-scoped Session dependency.

## Application and Request Lifecycle

`create_app()` builds a fresh application using the shared route definitions.
The default `database_lifespan` loads settings and creates an Engine and
Session factory at startup. The factory is stored in `app.state`; the Engine
is disposed on exit, including when factory creation fails. The lifespan's
async context-manager interface does not change the synchronous database API.

`get_session` creates a Session for database-backed requests, yields it to the
service dependency, commits on success, rolls back on an exception (including
a commit failure), and closes the Session in `finally`. Its function scope
places finalization before the response is sent. The repository continues to
flush without deciding whether the request should commit.

Fast API tests create an application without the database lifespan and override
the service with a fresh in-memory implementation. The PostgreSQL API test
suite instead injects a guarded `opsdesk_test` Session factory while keeping
the real Session and service dependencies.

## Alembic Migration Workflow

Alembic owns schema evolution; the application does not call
`Base.metadata.create_all()`. Its configuration imports `Base.metadata` for
autogeneration and reads the database URL through the same secret-aware
settings used by the application. No complete connection URL is stored in
`alembic.ini`.

Run Alembic from the repository root and always select the intended disposable
migration database explicitly during local schema exercises:

```bash
ALEMBIC_DATABASE_NAME=opsdesk_migration_dev \
uv run alembic \
  -c projects/month-02-ticket-api/alembic.ini \
  current
```

Apply the reviewed migration history:

```bash
ALEMBIC_DATABASE_NAME=opsdesk_migration_dev \
uv run alembic \
  -c projects/month-02-ticket-api/alembic.ini \
  upgrade head
```

Check for differences between the migrated database and current ORM metadata:

```bash
ALEMBIC_DATABASE_NAME=opsdesk_migration_dev \
uv run alembic \
  -c projects/month-02-ticket-api/alembic.ini \
  check
```

Generate offline SQL for review without applying it:

```bash
ALEMBIC_DATABASE_NAME=opsdesk_migration_dev \
uv run alembic \
  -c projects/month-02-ticket-api/alembic.ini \
  upgrade head --sql
```

Never run destructive migration practice against `opsdesk_dev`. Autogenerated
revisions must be inspected for unexpected tables, constraints, indexes, data
operations, and destructive statements before they are applied.

## Run the Application

The default application now requires valid database settings and an existing
compatible schema. Startup does not apply migrations or seed data. Verify the
intended database and migration state before manual writes. Setting
`ALEMBIC_DATABASE_NAME` affects Alembic only, not the API's `DATABASE_URL`.
Preserve the Week 06 `opsdesk_dev` laboratory; do not run blind migrations or
destructive cleanup against it.

From the repository root, run:

```bash
uv run uvicorn ticket_api.main:app \
  --app-dir projects/month-02-ticket-api \
  --reload
```

The application is available at `http://127.0.0.1:8000`. Swagger UI is
available at `http://127.0.0.1:8000/docs`.

## Available Endpoints

| Method   | Path                   | Success status   | Purpose |
| -------- | ---------------------- | ---------------- | ------- |
| `GET`    | `/health`              | `200 OK`         | Return application health. |
| `POST`   | `/auth/register`       | `201 Created`    | Register a member with a hashed password. |
| `POST`   | `/auth/login`          | `200 OK`         | Exchange valid credentials for a bearer access token. |
| `GET`    | `/users/me`            | `200 OK`         | Return the current active public User. |
| `GET`    | `/tickets`             | `200 OK`         | List, filter, and limit the authenticated User's Tickets. |
| `POST`   | `/tickets`             | `201 Created`    | Create a Ticket owned by the authenticated User. |
| `POST`   | `/tickets/preview`     | `200 OK`         | Validate input without storing it. |
| `GET`    | `/tickets/{ticket_id}` | `200 OK`         | Return one stored ticket. |
| `PATCH`  | `/tickets/{ticket_id}` | `200 OK`         | Partially update a stored ticket. |
| `DELETE` | `/tickets/{ticket_id}` | `204 No Content` | Delete a stored ticket without a body. |

`GET /tickets` requires a Bearer credential and returns only Tickets owned by
the current active User. The ownership predicate is applied in the repository
query before status filtering and limiting. It accepts two optional query
parameters:

- `status`: an optional filter restricted to `open`, `in_progress`, `resolved`,
  or `closed`
- `limit`: an integer from `1` through `100` with a default value of `10`

FastAPI returns `422 Unprocessable Content` before calling the route function
when path, query, or body input does not satisfy its declared contract. For
example, `/tickets/not-a-number` fails path validation,
`/tickets?limit=not-a-number` fails query validation, and an invalid preview
payload fails body validation.

`POST /tickets/preview` validates a JSON body containing `title` and `priority`.
It trims surrounding title whitespace, enforces title length, restricts priority
values, and rejects extra fields. It returns `200 OK` because it previews
validated input without creating or storing a ticket.

`POST /tickets` accepts the same create contract and requires an HTTP Bearer
credential. It derives ownership from the current persisted User, delegates
ticket creation to the service, and returns the stored representation through
`TicketResponse`. An `owner_id` supplied by the client is rejected rather than
trusted.
`PATCH /tickets/{ticket_id}` accepts one or more updatable fields. An empty
update is rejected with `422`, while a missing ticket produces `404` after a
valid identifier has reached the service.

The project has separate presentation, API schema, domain model, repository,
and service responsibilities. Routes receive a replaceable `TicketService`
dependency and do not access the repository directly. They convert validated
API strings into domain enums, translate application errors into `404` or `409`
HTTP responses, and map domain tickets into the explicit response schema.

The default application uses PostgreSQL storage. In-memory storage is retained
for isolated unit/API tests, not as the default runtime. Committed CRUD,
failure rollback, request isolation, and persistence across a real application
restart have been verified against the dedicated test database.

Registration, login, current-User resolution, stale-token rejection,
authenticated Ticket ownership, and owner-scoped collection listing have also
been verified through the real HTTP/Session/Argon2/PostgreSQL stack. Identified-
resource authorization is still pending; a valid login must not be interpreted
as permission to access every Ticket.

The earlier in-memory CRUD lifecycle was verified manually on 15 August 2026 with
Uvicorn, curl, Swagger UI, and the generated OpenAPI schema. The checks covered
creation, listing, filtering, limiting, detail lookup, partial update, deletion,
input validation, and missing-resource behavior.

## Run the Tests

Run all Month 02 Ticket API tests from the repository root:

```bash
uv run pytest projects/month-02-ticket-api/tests -v
```

Run the complete repository test suite:

```bash
uv run pytest
```

PostgreSQL integration tests are opt-in and use only the dedicated
`opsdesk_test` database:

```bash
RUN_DATABASE_TESTS=1 \
uv run pytest \
  projects/month-02-ticket-api/tests/test_sqlalchemy_repositories.py \
  projects/month-02-ticket-api/tests/test_database_api.py \
  -v
```

The integration-test guard derives a test URL without tracking another secret,
verifies the exact database name, rejects a superuser connection, requires the
migrated `tickets` table, and refuses to start when existing Ticket data is
present. Per-test transactions roll back ordinary repository work. HTTP tests
that verify real commits remove only records they created, using unique probe
titles or captured identifiers. Never point these tests at `opsdesk_dev`.

The complete quality run on 27 August 2026 produced `132 passed, 11 skipped`
without database tests and `143 passed` with `RUN_DATABASE_TESTS=1`. The final
Ticket count in `opsdesk_test` was zero.

On 28 August, the focused API and database/lifecycle run passed 39 tests; the
first PostgreSQL API test passed separately and left zero Tickets behind. It
verified a successful POST, visibility through an independent connection, and
a subsequent GET. It does not alone prove HTTP behavior when commit fails.
Full PostgreSQL HTTP CRUD/error coverage, request isolation checks, and the
manual restart demonstration are carried to 29 August.

The final 28 August regression run produced `138 passed, 12 skipped` with
`RUN_DATABASE_TESTS=0` and `150 passed` with `RUN_DATABASE_TESTS=1`. Ruff lint,
formatting (90 files), and `git diff --check` passed. The final `opsdesk_test`
Ticket count was zero. These results cover the implemented suite, not the
additional scenarios scheduled for 29 August.

On 29 August, eight PostgreSQL HTTP tests verified committed creation and later
lookup, filtering and limiting, committed update/delete behavior, `404` and
`422` paths, rollback after a flushed write, commit failure without a false
`201`, and a distinct Session per request. Test-only routes and fault-injecting
Session classes exist only in fixture-created applications.

A manual Uvicorn stop/start check used a process-local override targeting
`opsdesk_test`; it did not modify `.env`. A precisely identified Ticket was
created, observed directly in PostgreSQL, retrieved after process restart, and
then deleted through the API. PostgreSQL ended with zero Tickets.

The final 29 August quality run produced `138 passed, 19 skipped` with database
tests disabled and `157 passed` with `RUN_DATABASE_TESTS=1`. Dependency checks,
Ruff lint, formatting for 90 files, `git diff --check`, the zero-row isolation
check, and Alembic revision `e07f08d4399d` all passed.

On 31 August, the password and token-configuration foundation increased the
complete suite to `150 passed, 19 skipped` with database tests disabled and
`169 passed` with `RUN_DATABASE_TESTS=1`. PostgreSQL fixtures use a synthetic
test-only JWT secret, while the real ignored `.env` remains outside tests and
Git. Dependency consistency, Ruff lint, formatting for 94 files, and
`git diff --check` passed.

On 4 September, the completed login/current-User boundary and protected Ticket
creation increased the complete suite to `255 passed, 33 skipped` with database
tests disabled and `288 passed` with `RUN_DATABASE_TESTS=1`. The guarded tests
proved real Argon2 registration-to-login, generic authentication failures,
expired and stale token rejection, server-derived persisted ownership, rollback
behavior, and exact cleanup. Dependency consistency, Ruff lint, formatting for
106 files, and `git diff --check` passed.

On 5 September, authenticated owner-scoped collection listing increased the
complete suite to `257 passed, 34 skipped` with database tests disabled and
`291 passed` with `RUN_DATABASE_TESTS=1`. In-memory and PostgreSQL adapters share
an explicit `list_by_owner` contract, and a guarded two-User HTTP test proved
that a caller cannot list another User's Ticket. Dependency consistency, Ruff
lint, formatting for 106 files, exact database cleanup, and `git diff --check`
passed.
