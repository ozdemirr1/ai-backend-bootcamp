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

## Next Tasks - Monday, 31 August

1. Create the Week 08 feature branch from synchronized `main`.
2. Explain authentication, authorization, password hashing, bearer tokens,
   JWT, and IDOR/BOLA before implementation.
3. Review the existing dependency and persistence boundaries for reuse.
4. Verify current compatible security dependencies from primary documentation.
5. Add environment-based token configuration without tracked secrets.
6. Implement only the password hashing and verification foundation with focused
   tests after the architecture review.

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
