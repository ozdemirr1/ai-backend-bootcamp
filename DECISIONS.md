# Technical Decisions

## Decision 001 - Main Career Direction

I will focus on becoming an AI-assisted Backend / Full-Stack Developer.

## Reason

Instead of learning many technologies at a shallow level, I will build a strong foundation in backend development, database design, API development, AI integration, cloud deployment, and basic frontend skills.

## Main Stack

Python, FastAPI, PostgreSQL, Redis, Docker, React, TypeScript, OpenAI API, RAG, pgvector, GitHub Actions.

## What I Will Avoid

- Random technology switching
- Deep Flutter specialization during this bootcamp
- WordPress/PHP focus
- Game development
- Desktop applications
- Watching courses without building projects

## Decision 002 - Python and Dependency Workflow

The repository uses Python 3.14 and `uv` for Python version, environment, dependency, and lockfile management.

Direct runtime dependencies are declared in `[project.dependencies]`. Development-only tools are declared in `[dependency-groups].dev`. Exact direct and transitive versions are recorded in `uv.lock`.

## Reason

Python 3.9 reached end of life and no longer provides an appropriate baseline for the FastAPI phase of the bootcamp. Python 3.14 is an actively supported stable release.

Using one dependency workflow prevents `requirements-dev.txt`, manually installed packages, and the actual environment from becoming inconsistent. The lockfile makes the verified environment reproducible while `pyproject.toml` keeps direct dependency intent explicit.

## Decision 003 - Local PostgreSQL Workflow

Week 06 uses the current stable PostgreSQL 18 release installed and managed
through Homebrew. SQL is written in version-controlled files, executed through
`psql`, and may be inspected later with pgAdmin as a secondary visual tool.

The local learning environment uses a dedicated `opsdesk_app` login role and an
`opsdesk_dev` database. The application role is not a superuser and its
connection requires SCRAM password authentication. Credentials and connection
URLs remain outside the repository.

## Reason

Using PostgreSQL and `psql` directly makes server, client, role, database,
schema, SQL, and authentication behavior visible before SQLAlchemy and Alembic
introduce another abstraction layer. Homebrew matches the existing macOS tool
workflow and avoids adding Docker before its planned month.

Separating the application role from the cluster administrator applies least
privilege and prevents application code from depending on administrative
access. Repeatable SQL files preserve the database design in Git without
storing machine-specific state or secrets.

## Decision 004 - Synchronous SQLAlchemy Persistence Foundation

The first PostgreSQL integration uses synchronous SQLAlchemy 2 with Psycopg.
Database configuration is loaded from the required `DATABASE_URL` environment
variable through Pydantic Settings. The real `.env` file remains local, while
`.env.example` documents only the connection-string shape and placeholders.

Engine and session construction remain in testable factory functions. Creating
an engine or a session does not itself prove connectivity; an explicit query is
used when a real database connection must be verified. Sessions are now
created through a FastAPI request dependency instead of shared across requests.

## Reason

The existing FastAPI routes and service workflows are synchronous. Starting
with synchronous persistence keeps the session and transaction lifecycle
visible without introducing async-specific connection and testing concerns at
the same time.

Environment-based configuration prevents credentials from being hardcoded or
tracked. Factory functions avoid reading local configuration during module
import and let unit tests supply safe, synthetic settings without contacting
PostgreSQL. Request-scoped sessions provide an explicit unit-of-work
boundary and prevent unrelated requests from sharing mutable persistence state.

## Decision 005 - Stable Learning Module and Product Repository Names

The living Ticket API that began in Week 05 uses the stable directory
`projects/month-02-ticket-api/` while it progresses through FastAPI,
PostgreSQL persistence, migrations, and authentication during Weeks 05-08.
Weekly reports, feature branches, and commit messages remain week-based.

The completed `projects/week-06-postgresql-sql/` directory remains unchanged
because it is a bounded SQL laboratory and historical learning artifact.

OpsDesk, DocuMind, and HireMatch AI will each receive a separate public product
repository when real implementation of that product begins. Each product will
start as one repository rather than separate backend and frontend repositories.

## Reason

A living application should have a stable identity instead of being renamed at
every weekly transition. Time-based names remain useful for reports and Git
history, while a stable module name keeps commands, documentation, and paths
predictable.

Separate product repositories will make the three portfolio applications easy
to understand and pin on GitHub without mixing their production code with the
bootcamp's notes and laboratories. Creating them only when implementation
begins avoids empty showcase repositories and premature structure.

## Decision 006 - Repository and Transaction Ownership

`TicketService` depends on a storage-independent `TicketRepository` protocol.
The in-memory and SQLAlchemy implementations satisfy the same application
contract. The SQLAlchemy repository owns persistence queries, ORM/domain
mapping, `flush()`, and `refresh()`, but it does not call `commit()` or
`rollback()`.

Transaction ownership belongs to the application use-case boundary. The
request-scoped FastAPI Session dependency commits on successful completion and
rolls back when an exception occurs, including during commit. It closes the
Session in `finally` and uses function-scoped finalization before response
transmission. Destructive repository and HTTP integration tests run only
against the dedicated `opsdesk_test` database through the non-superuser
application role.

## Reason

A use case may require multiple repository operations to succeed or fail as
one unit. If a repository commits internally, it closes the transaction before
the caller knows whether the complete workflow succeeded. Caller-owned
transactions preserve atomicity, keep persistence behavior composable, and
make commit and rollback outcomes directly testable.

The repository protocol keeps services independent of SQLAlchemy and permits
fast in-memory tests alongside real PostgreSQL integration tests. A dedicated,
guarded test database makes destructive isolation explicit and prevents test
cleanup from touching development data.

## Decision 007 - Application Lifecycle and Test Composition

The Ticket API uses `create_app()` with an application lifespan that creates
the Engine and Session factory at startup and disposes the Engine on exit.
The factory lives in `app.state`; mutable Sessions do not. Route definitions
remain in an `APIRouter`, and the default service dependency now composes the
PostgreSQL repository.

Fast HTTP tests create an application without database startup and explicitly
override the service with an in-memory implementation. PostgreSQL HTTP tests
provide a guarded `opsdesk_test` factory but retain the real Session and
service dependency chain. No application startup hook creates or migrates
tables.

## Reason

Separating application construction from resource startup avoids import-time
configuration and makes test composition explicit. It preserves inexpensive
HTTP contract tests while enabling focused tests of real commits and database
visibility. Lifespan and Session mocks verify cleanup paths, but do not replace
real HTTP failure tests or a persistence-after-restart check. The PostgreSQL
HTTP suite therefore also exercises rollback after a flushed write, commit
failure without a false success response, and separate Sessions per request.
Test-only failure injection stays inside fixture-created applications. A manual
Uvicorn stop/start check against `opsdesk_test` proves that committed data
survives the application process and is cleaned up by its exact identifier
afterward.

## Decision 008 - Password Hashing and Token Configuration Boundary

The authentication foundation uses pwdlib's maintained recommended Argon2
configuration through the local `PasswordHasher` boundary. Routes, services,
and repositories will not call the third-party password library directly.

JWT signing configuration comes from environment-backed Pydantic Settings.
`JWT_SECRET` is required, represented as `SecretStr`, and guarded against
obviously short values. Access-token lifetime is bounded and defaults to 30
minutes. No default signing secret, real secret, complete token, or plaintext
password is stored in Git. Tracked tests use explicit synthetic secrets.

## Reason

Password hashing is a specialized, deliberately expensive one-way operation;
it must not be replaced with reversible encryption or a fast general-purpose
digest. Centralizing the maintained library keeps cryptographic details out of
HTTP, application, and persistence responsibilities while preserving a clear
place for later algorithm upgrades.

A signing secret is runtime configuration rather than source code. Requiring
it makes unsafe omission fail at startup, while `SecretStr` reduces accidental
display in ordinary representations. The length guard catches obvious
placeholders but does not replace cryptographically random generation. Test
secrets remain deterministic and non-sensitive so the suite does not depend
on a developer's local secret.

## Decision 009 - Stable User Identity and Trusted Registration Defaults

Users use a database-generated `user_id` as their durable identity. Email is a
normalized, case-insensitive account login field with a named database unique
constraint, but it is not used as a Ticket relationship key. The current role
set is limited to `member` and `admin`.

Ordinary registration data contains email and password hash only. It cannot
select a role, active state, identity, or Ticket owner. PostgreSQL supplies the
safe `member` and active defaults. Domain and persistence models remain
separate and cross through explicit mapper functions.

Ticket ownership will reference `users.user_id`. The first migration adds
`owner_id` as nullable because existing Ticket rows have no trustworthy owner;
backfill and a later non-null contract remain explicit follow-up steps.

## Reason

Email is mutable business data, while primary-key relationships and token
subjects require a stable identifier. A client-controlled role would permit
privilege escalation, so authorization attributes must come from trusted
server state.

Adding a non-null foreign key immediately would make PostgreSQL invent or
require an owner for historical Tickets. The expand-backfill-contract sequence
preserves existing data and makes the ownership decision visible instead of
hiding it inside a destructive or misleading migration.
