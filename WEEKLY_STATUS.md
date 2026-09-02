# Weekly Status

## Current Week

Week 08

## Date

31 August - 6 September 2026

## Current Focus

- User registration and login
- Secure password hashing and verification
- JWT access-token creation and validation
- Current-user dependency
- Protected Ticket endpoints
- Ticket ownership and object-level authorization
- Bounded role/function-level authorization
- Authentication and authorization testing

## Completed

- [x] Week 06 PostgreSQL 18.6 learning environment
- [x] Dedicated non-superuser application role and development database
- [x] SCRAM-authenticated local application connection
- [x] Constrained four-table Ticket relational schema
- [x] One-to-many and many-to-many relationships
- [x] Deterministic development seed data
- [x] CRUD, join, aggregation, transaction, and index exercises
- [x] Mermaid Ticket ERD and PostgreSQL notes
- [x] Clean-database reconstruction and verification
- [x] Ruff checks and 107 repository tests
- [x] Week 06 pull request merged and feature branches cleaned
- [x] Week 06 interview review
- [x] Week 06 report
- [x] Week 07 plan
- [x] Week 07 feature branch
- [x] SQLAlchemy, Psycopg, Alembic, and Pydantic Settings dependencies
- [x] Environment-based database configuration
- [x] SQLAlchemy Engine and Session factory foundation
- [x] Manual synchronous connection through `opsdesk_app`
- [x] Five focused configuration and database-factory unit tests
- [x] Complete dependency and quality checks with 112 passing tests
- [x] Stable Month 02 Ticket API project naming
- [x] Typed SQLAlchemy Ticket persistence record
- [x] Explicit persistence-to-domain mapping
- [x] Five persistence metadata tests and five mapper tests
- [x] Complete quality checks with 121 passing tests
- [x] Alembic migration workflow
- [x] PostgreSQL repository implementation
- [x] FastAPI lifespan, application factory, and request-scoped Session wiring
- [x] PostgreSQL API creation and subsequent lookup integration test
- [x] Complete PostgreSQL HTTP failure-path and restart verification
- [x] Isolated database integration tests
- [x] Week 07 technical interview review
- [x] Week 07 pull request merged and feature branches cleaned
- [x] Week 07 report
- [x] Week 08 plan
- [x] Week 08 feature branch
- [x] Authentication and authorization threat model
- [x] Argon2id password hashing boundary and behavior tests
- [x] Secret-aware JWT configuration foundation
- [x] Monday dependency, lint, formatting, unit, and integration quality gates

## Problems

- No current blockers.

## Week 06 Handoff

- PostgreSQL 18.6 is running locally.
- `opsdesk_app` is a non-superuser role that owns `opsdesk_dev`.
- The local application connection requires SCRAM password authentication.
- The relational model contains `tickets`, `comments`, `tags`, and
  `ticket_tags`.
- The schema contains 16 columns and 14 named primary-key, foreign-key, unique,
  and check constraints.
- The deterministic development state contains six Tickets, six Comments, five
  Tags, and six Ticket-Tag assignments.
- The composite index `tickets_status_ticket_id_idx` supports status-filtered
  Ticket listing in identifier order.
- Eight ordered SQL scripts can rebuild data and reproduce the Week 06
  exercises.
- Pull request #4 was merged into `main` as commit `6c60128`.
- Local and remote Week 06 feature branches were deleted after merge.
- `main` is synchronized with `origin/main`.

## Week 07 Monday Outcome

- Created `feature/week-07-sqlalchemy-alembic` from synchronized `main`.
- Added SQLAlchemy 2.0.52, Psycopg 3.3.4, Alembic 1.19.1, and Pydantic Settings
  2.15.0 through `uv`.
- Verified the lockfile, environment synchronization, and installed-package
  compatibility.
- Added a required, immutable, secret-aware database settings model.
- Confirmed that the real `.env` file is ignored while `.env.example` is
  trackable.
- Added testable Engine and Session factory functions without import-time
  connectivity.
- Verified a real SQLAlchemy connection to PostgreSQL 18.6 through
  `opsdesk_app` and `opsdesk_dev`.
- Observed lazy Session transaction behavior before and after its first query.
- Passed five focused configuration and database-factory unit tests.
- Passed the complete 112-test repository suite with Ruff lint and formatting
  checks.
- Renamed the living Weeks 05-08 application to
  `projects/month-02-ticket-api/` while preserving the bounded Week 06 SQL lab.

## Week 07 Tuesday Outcome

- Added a typed declarative `TicketRecord` without replacing the domain
  `Ticket` model.
- Matched the Week 06 PostgreSQL identity, defaults, timestamps, nullability,
  and named constraints in SQLAlchemy metadata.
- Compiled and reviewed the generated PostgreSQL `CREATE TABLE` statement.
- Added explicit conversion from persistence strings to domain enums.
- Added safe business-field mapping back onto an existing persistence record.
- Rejected mismatched identifiers before record mutation.
- Preserved database-owned identifiers and timestamps across mapper updates.
- Passed 25 focused tests and the complete 121-test repository suite.
- Passed Ruff lint, Ruff formatting, and Git diff checks.

## Week 07 Wednesday Outcome

- Initialized Alembic inside the stable Month 02 Ticket API project.
- Connected Alembic to secret-aware settings and `Base.metadata` without
  tracking credentials.
- Added and tested the `(status, ticket_id)` composite index in SQLAlchemy
  metadata.
- Created the isolated `opsdesk_migration_dev` migration database under the
  non-superuser application role.
- Generated and reviewed revision `e07f08d4399d` before applying it.
- Verified the migrated Ticket columns, identity, defaults, constraints,
  primary key, and composite index through the PostgreSQL catalogs.
- Completed upgrade, downgrade, and re-upgrade successfully.
- Confirmed the database is at `head` and `alembic check` reports no metadata
  drift.
- Inspected the complete offline transactional SQL without applying it.
- Passed lockfile, environment, package compatibility, Ruff lint, Ruff
  formatting, Git diff, and all 122 repository tests.

## Week 07 Thursday Outcome

- Added `NewTicket` to separate validated creation input from a persisted
  Ticket with a database-generated identifier.
- Introduced the `TicketRepository` protocol and kept `TicketService`
  independent of concrete storage technology.
- Adapted the in-memory repository and service while preserving existing unit
  and HTTP behavior.
- Implemented SQLAlchemy Ticket create, lookup, ordered listing, update, and
  delete operations.
- Kept repository `flush()` and `refresh()` behavior separate from
  caller-owned `commit()` and `rollback()` decisions.
- Translated expected persistence conflicts without leaking SQLAlchemy
  exceptions into the application contract.
- Added ORM-driven `updated_at` behavior and verified timestamp advancement in
  separate PostgreSQL transactions.
- Created and migrated the dedicated `opsdesk_test` database under
  `opsdesk_app`.
- Added guarded, opt-in integration fixtures and 11 real PostgreSQL repository
  tests.
- Verified commit visibility, rollback invisibility, no implicit repository
  commit, generated identity, CRUD behavior, ordering, missing records, and
  final test cleanup.
- Passed lockfile, environment, package compatibility, Ruff lint, Ruff
  formatting, and Git diff checks.
- Passed 132 tests with 11 integration skips in the default run and all 143
  tests with database integration enabled.
- Confirmed the final `opsdesk_test` Ticket count was zero.

## Week 07 Friday Outcome - 28 August

- Added an application lifespan that constructs the Engine and Session factory
  at startup and disposes the Engine on shutdown or setup failure.
- Added a request-scoped Session dependency with commit on success, rollback
  on an exception or commit failure, and unconditional Session cleanup.
- Selected function-scoped dependency finalization so transaction completion
  occurs before FastAPI sends the response.
- Composed `SqlAlchemyTicketRepository` and `TicketService` through dependency
  injection and removed the default process-global in-memory service.
- Added `create_app()` and preserved fast API tests with a fresh application,
  disabled database lifespan, and an explicit in-memory service override.
- Passed 39 focused tests: 31 existing API tests and eight database-factory,
  Session-finalization, and lifespan tests.
- Passed the first real PostgreSQL API integration test: POST returned `201`,
  a separate database connection saw the committed row, and a subsequent GET
  returned the same Ticket. The production Session/service dependencies were
  used with a guarded test-database Session factory.
- Confirmed `opsdesk_test` contained zero Tickets after targeted cleanup.
- Passed the final whole-repository Ruff lint and formatting checks (90 files
  already formatted), plus `git diff --check`.
- Passed 138 tests with 12 integration skips under `RUN_DATABASE_TESTS=0`
  and all 150 tests under `RUN_DATABASE_TESTS=1`.
- Confirmed zero Tickets in `opsdesk_test` after the complete integration run.
  Staged review, commit, and push remain the Git closing steps.
- Stopped feature work by choice and moved the unfinished Friday verification
  to Saturday. Week 07 is not yet complete.

## Week 07 Saturday Outcome - 29 August

- Confirmed that `opsdesk_test` was empty, migrated to revision `e07f08d4399d`
  at `head`, and free of pending Alembic upgrade operations before testing.
- Expanded the PostgreSQL HTTP suite to eight integration tests using the real
  request Session, SQLAlchemy repository, service, routes, and PostgreSQL
  transaction boundary.
- Verified committed create/read behavior, status filtering and limiting,
  committed update/delete behavior, missing-resource `404` responses, and
  validation `422` responses.
- Verified that an exception after `flush()` rolls back the write, an injected
  commit failure returns no false `201` and leaves no row, and two requests use
  distinct Session instances.
- Kept the existing `409` application contract covered by fast tests without
  inventing a duplicate-title constraint that the relational model does not
  require.
- Started the application against `opsdesk_test` using a process-local database
  override without changing `.env` or exposing credentials.
- Created Ticket `97`, stopped and restarted Uvicorn, retrieved the same Ticket
  after restart, then deleted only that demonstration record. The final Ticket
  count was zero and port `8000` was closed cleanly.
- Passed dependency consistency checks, Ruff lint, Ruff formatting for 90
  files, and `git diff --check`.
- Passed `138` tests with `19` integration skips when database tests were
  disabled and all `157` tests when they were enabled.
- Reconfirmed zero Tickets in `opsdesk_test` and Alembic revision
  `e07f08d4399d` after the complete run.

## Week 07 Sunday Outcome - 30 August

- Completed an eight-question technical interview review covering Psycopg,
  SQLAlchemy, Alembic, Engine, Connection, Session, transaction methods,
  migration safety, mapping, repositories, integration tests, and the complete
  HTTP persistence lifecycle.
- Re-ran the complete dependency, Ruff, formatting, and test gates before
  merge: `138 passed, 19 skipped` without database tests and all `157` tests
  with database tests enabled.
- Reviewed the complete pull-request diff for credentials, local paths,
  destructive development-database targets, test-only behavior, and production
  boundary leaks; no merge blockers remained.
- Merged pull request #5 into `main` through merge commit `7ebc076`.
- Fast-forwarded local `main` to `origin/main` and removed both local and remote
  `feature/week-07-sqlalchemy-alembic` branches.
- Added the Week 07 report and prepared the Week 08 authentication and
  authorization plan.

## Week 08 Monday Outcome - 31 August

- Created `feature/week-08-auth-authorization` from synchronized `main`.
- Separated authentication from authorization and threat-modeled database
  compromise, credential enumeration, bearer-token theft, token tampering,
  IDOR/BOLA, and role escalation before implementation.
- Verified `pwdlib`, Argon2id, PyJWT, FastAPI, and OWASP password-storage
  guidance from primary documentation.
- Added `pwdlib` 0.3.1 with Argon2 support and PyJWT 2.13.0 through `uv`.
- Added a focused `PasswordHasher` boundary around the maintained library
  instead of distributing password-library calls through routes and services.
- Verified that hashes differ from plaintext, correct credentials verify,
  incorrect credentials fail, per-hash salts produce distinct values, and the
  selected encoding identifies Argon2id.
- Added a required secret-aware JWT setting with a minimum length guard and a
  bounded access-token lifetime of 1 through 1,440 minutes, defaulting to 30.
- Kept the real JWT secret out of source, examples, logs, and tests;
  `.env.example` contains only a deliberately invalid placeholder.
- Isolated configuration and PostgreSQL tests from machine-specific JWT
  secrets by providing explicit synthetic test values.
- Passed dependency consistency, Ruff lint, formatting for 94 files, and Git
  diff checks.
- Passed `150` tests with `19` integration skips when database tests were
  disabled and all `169` tests against the guarded `opsdesk_test` database.

## Week 08 Tuesday Outcome - 1 September

- Selected a stable database-generated `user_id` for identity, Ticket
  ownership, and the future JWT subject instead of using mutable email data as
  a relationship key.
- Defined an explicit case-insensitive account-email policy and added
  `email-validator` 2.3.0 for maintained syntax validation and normalization
  without runtime DNS checks.
- Added `NewUser`, `User`, and the bounded `member`/`admin` `UserRole` enum.
  Ordinary registration data contains no client-selected role.
- Added nine User-domain tests covering normalization, invalid input, strict
  identifiers, role types, active state, and password-hash preservation.
- Added a typed SQLAlchemy `UserRecord` with database identity, named unique
  and check constraints, safe `member`/active server defaults, and
  timezone-aware timestamps.
- Added five persistence-model tests for the User table alongside the existing
  Ticket metadata tests.
- Added explicit mapping from trusted registration data to `UserRecord` and
  from persisted records to the `User` domain type. Database defaults remain
  database-owned until `flush()`/`refresh()`.
- Passed Ruff, `git diff --check`, and 29 focused domain, persistence-model,
  and mapper tests.
- Deliberately deferred repository, Ticket ownership, and migration work to a
  longer Wednesday session rather than rushing database-sensitive changes.

## Week 08 Wednesday Outcome - 2 September

- Added a storage-independent User repository protocol plus in-memory and
  SQLAlchemy implementations with normalized-email lookup, database-generated
  defaults, and duplicate-identity exception translation.
- Added guarded PostgreSQL User repository tests without moving `commit()` or
  `rollback()` into the repository boundary.
- Added nullable Ticket `owner_id` metadata, a restrictive foreign key to
  `users.user_id`, an ownership/status/listing index, and mapper protection
  against accidental ownership transfer.
- Added and manually reviewed Alembic revision `e98825c4d6b6` for the User
  table and Ticket ownership expand phase.
- Proved upgrade, downgrade, and re-upgrade behavior against
  `opsdesk_migration_dev`, including preservation of a legacy Ticket while the
  nullable ownership column was added and removed. `alembic check` reports no
  metadata drift.
- Applied the revision to guarded `opsdesk_test` and verified its tables,
  column, unique constraint, foreign key, empty state, and head revision.
- Added strict registration request and public User response contracts. Client
  input cannot select role, identity, active state, or ownership, and responses
  cannot expose plaintext or hashed passwords.
- Added an injected `PasswordHashing` protocol and `RegistrationService` that
  validates identity before the expensive hash, stores only an Argon2id hash,
  and translates repository conflicts without depending on SQLAlchemy.
- Added `POST /auth/register`, dependency composition, fast HTTP tests, and
  guarded PostgreSQL tests for durable registration, password hashing,
  duplicate conflict rollback, and exact cleanup.
- Passed dependency consistency, Ruff, formatting for 101 files, and Git diff
  checks. Passed `205` tests with `27` integration skips and all `232` tests
  with guarded database tests enabled.

## Next Tasks - Thursday, 3 September

1. Define strict login and token response contracts.
2. Add a login service with one generic public invalid-credential failure for
   missing users, incorrect passwords, and inactive users.
3. Add deterministic clock-backed JWT creation and validation with fixed
   algorithm selection, minimal claims, and bounded expiration.
4. Reject malformed, tampered, expired, and unsupported tokens with `401`.
5. Load the persisted active User through a current-user dependency.
6. Add and test `POST /auth/login` and `GET /users/me` without logging or
   returning complete tokens outside the intended login response.

## Week 08 Guardrails

- Never store, log, return, or commit plaintext passwords, token secrets, or
  complete access tokens.
- Do not implement password hashing or JWT cryptography manually.
- Treat authentication and authorization as separate decisions.
- Derive Ticket ownership from the authenticated User, not client input.
- Add explicit object-level and function/role-level authorization checks.
- Keep routes independent of SQLAlchemy and preserve transaction ownership.
- Use Alembic for User and Ticket-ownership schema changes.
- Continue destructive integration testing only against `opsdesk_test`.
- Do not add OAuth providers, refresh-token rotation, Docker, Redis, React, or
  AI features before the core Week 08 scope is complete.
