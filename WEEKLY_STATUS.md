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
- [ ] SQLAlchemy persistence mapping
- [ ] Alembic migration workflow
- [ ] PostgreSQL repository implementation
- [ ] FastAPI database integration
- [ ] Isolated database integration tests

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

## Next Tasks

1. Verify the structural rename through the focused and complete quality suite.
2. Review and commit the stable project naming change.
3. Begin Tuesday with SQLAlchemy 2 declarative Ticket mapping.
4. Keep persistence records separate from the existing domain Ticket model.

## Week 07 Guardrails

- Use a dedicated `opsdesk_test` database for integration tests.
- Never run destructive tests against `opsdesk_dev`.
- Do not commit passwords, `.env` files, or complete database URLs.
- Do not use a superuser as the application runtime role.
- Keep domain, service, persistence, and HTTP responsibilities separate.
- Do not use `create_all()` as a replacement for migrations.
- Begin with synchronous SQLAlchemy to match the current application flow.
- Do not add authentication, Docker, Redis, or AI features early.
