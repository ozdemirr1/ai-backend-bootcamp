# Weekly Status

## Current Week

Week 07

## Date

24 August - 30 August 2026

## Current Focus

- SQLAlchemy 2 fundamentals
- Psycopg PostgreSQL connectivity
- Environment-based database configuration
- Engine, connection, session, and transaction responsibilities
- Declarative persistence mappings
- Alembic migration fundamentals
- PostgreSQL Ticket repository
- FastAPI request-scoped database sessions
- Isolated PostgreSQL integration tests

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
- [ ] Complete PostgreSQL HTTP failure-path and restart verification
- [x] Isolated database integration tests

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

## Next Tasks - Saturday, 29 August

1. Resume PostgreSQL HTTP integration tests for listing, filtering, updating,
   deleting, missing resources, invalid input, and expected conflict handling.
2. Verify rollback after a write followed by a request failure, commit failure
   without a false successful response, and separate Sessions per request.
   Mock lifecycle tests and the successful POST test do not replace these
   end-to-end failure checks.
3. Check the manual runtime's database target and migration state without
   exposing credentials. `ALEMBIC_DATABASE_NAME` does not change the API's
   `DATABASE_URL`; preserve the Week 06 SQL laboratory.
4. Demonstrate persistence across a real application restart, using only
   explicitly identified demonstration records for cleanup.
5. Complete Saturday's isolation review and full quality checks, update the
   evidence, and prepare the Week 07 PR only after the remaining checks pass.

## Week 07 Guardrails

- Use a dedicated `opsdesk_test` database for integration tests.
- Never run destructive tests against `opsdesk_dev`.
- Do not commit passwords, `.env` files, or complete database URLs.
- Do not use a superuser as the application runtime role.
- Keep domain, service, persistence, and HTTP responsibilities separate.
- Do not use `create_all()` as a replacement for migrations.
- Begin with synchronous SQLAlchemy to match the current application flow.
- Do not add authentication, Docker, Redis, or AI features early.
