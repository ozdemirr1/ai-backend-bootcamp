# Month 02 Report

## Date

10 August - 6 September 2026

## Monthly Goal

Build a complete backend-learning progression from an in-memory FastAPI API to
a PostgreSQL-backed, migration-managed, authenticated, and authorized service.

## Executive Result

Month 02 produced a tested Ticket API learning application that demonstrates
the complete path from HTTP contracts to durable PostgreSQL transactions and
security boundaries.

```text
FastAPI and Pydantic
        |
        v
domain and service boundaries
        |
        v
repository protocols
        |
        +----> in-memory adapters for fast tests
        |
        +----> SQLAlchemy adapters
                    |
                    v
                 Psycopg
                    |
                    v
               PostgreSQL

Alembic --> versioned schema evolution
Argon2id + JWT --> authentication
owner and role checks --> authorization
```

The Month 02 learning curriculum is complete. The public CI and deployment
milestones from the original roadmap were not completed and are explicitly
carried into the real OpsDesk product phase rather than being recorded as
finished.

## Week-by-Week Progression

### Week 05 - FastAPI Fundamentals

- Learned the separate responsibilities of Uvicorn, ASGI, FastAPI, and
  Pydantic.
- Built strict create, update, and response contracts.
- Added a validated Ticket domain model, in-memory repository, and service.
- Implemented Ticket CRUD, filtering, error mapping, OpenAPI, and HTTP tests.
- Merged pull request #3 through merge commit `b02c983`.
- Final evidence: 107 passing tests.

### Week 06 - PostgreSQL and SQL

- Installed PostgreSQL and created a non-superuser application role.
- Designed the Ticket relational model directly in SQL before using an ORM.
- Practiced constraints, relationships, joins, aggregation, transactions, and
  query-plan reasoning.
- Added repeatable schema, seed, exercise, and verification scripts.
- Merged pull request #4 through merge commit `6c60128`.
- Final evidence: SQL reconstruction passed and the 107-test Python suite
  remained green.

### Week 07 - SQLAlchemy and Alembic

- Connected FastAPI to PostgreSQL with synchronous SQLAlchemy and Psycopg.
- Separated domain models from persistence records with explicit mappers.
- Added repository protocols and a PostgreSQL repository adapter.
- Introduced Alembic migration history instead of application `create_all()`.
- Added application lifespan and one Session/transaction boundary per request.
- Verified commit, rollback, failure behavior, Session isolation, and durable
  data across an application restart.
- Merged pull request #5 through merge commit `7ebc076`.
- Final evidence: 138 passed and 19 skipped without integration tests; all 157
  passed with the guarded PostgreSQL suite enabled.

### Week 08 - Authentication and Authorization

- Added User identity, normalized email registration, and database uniqueness.
- Added Argon2id password hashing and generic login failures.
- Added short-lived, fixed-algorithm JWT access tokens.
- Reloaded the current active User from persistence on protected requests.
- Derived Ticket ownership from server-trusted identity.
- Added SQL owner filtering, object-level BOLA protection, and a bounded
  admin-only function.
- Verified migration safety, stale-token behavior, transaction rollback,
  cross-User denial, current persisted roles, and exact test cleanup.
- Merged pull request #6 through merge commit `9876703`.
- Final evidence: 274 passed and 37 skipped without database tests; all 311
  passed with the guarded PostgreSQL suite enabled.

## Engineering Capabilities Demonstrated

### HTTP and Validation

- Resource-oriented endpoints and deliberate status codes
- Strict request and response schemas
- Partial updates and field normalization
- Dependency injection and OpenAPI generation
- Safe public error contracts for authentication and authorization

### Architecture

- Domain, presentation, service, repository, and persistence separation
- Dependency inversion through narrow protocols
- In-memory and PostgreSQL adapters behind the same application contracts
- Explicit mapper functions instead of leaking ORM records through the API
- Testable time, password, and token boundaries

### PostgreSQL and Persistence

- Relational modelling, constraints, indexes, joins, and transactions
- SQLAlchemy Engine, Connection, Session, identity map, and unit of work
- Request-scoped Session lifecycle and caller-owned transaction completion
- Alembic revision review, upgrade, downgrade, and schema-drift detection
- Dedicated guarded integration-test database and deterministic cleanup

### Security

- Secret-aware configuration and ignored environment files
- Argon2id hashing with salt and work-factor reasoning
- Minimal JWT claims and fixed server-selected validation algorithm
- Generic invalid-credential responses and dummy-hash work
- Server-derived ownership and denial of client-selected privilege
- SQL-level collection scoping, object-level checks, and role/function checks

### Verification and Delivery

- Focused unit tests, HTTP tests, lifecycle tests, and PostgreSQL integration
  tests
- Ruff lint and formatting gates
- Reproducible `uv` dependency locking and compatibility checks
- Feature branches, staged diff review, pull requests, and branch cleanup
- Weekly plans, technical notes, architecture decisions, and reports

## Month-End Evidence

- Python: 3.14.7
- PostgreSQL: 18.6
- Final migration revision: `e98825c4d6b6`
- Final test suite without database tests: 274 passed, 37 skipped
- Final test suite with database tests: 311 passed
- Ruff formatting: 107 files verified
- Month 02 pull requests: #3, #4, #5, and #6
- Month 02 feature commits merged through those pull requests: 29
- Final Month 02 merge commit: `9876703`
- Final guarded test state: 0 Users and 0 Tickets
- Real secrets, `.env`, complete database URLs, and complete JWTs: excluded

## Important Decisions

- Learn SQL directly before introducing SQLAlchemy.
- Keep the first database lifecycle synchronous and explicit.
- Use Alembic rather than `create_all()` for schema evolution.
- Keep domain and persistence representations separate where responsibilities
  differ.
- Keep commit and rollback at the request transaction boundary.
- Use a dedicated guarded database for destructive integration tests.
- Treat authentication and authorization as separate decisions.
- Derive ownership from current server-trusted identity.
- Do not fabricate historical Ticket ownership merely to add `NOT NULL`.
- Keep this application as a bounded Month 02 learning artifact and begin the
  real OpsDesk product in its own repository.

## Roadmap Variance and Carry-Over

The original Month 02 roadmap also named basic CI and a first backend
deployment. Those outcomes were not completed.

This is an explicit schedule adjustment, not hidden completion:

- Add a minimal GitHub Actions workflow to OpsDesk after an executable Python
  package and meaningful tests exist.
- Produce the early deployed OpsDesk backend preview during Month 03.
- Add Docker build checks only after the Month 05 Docker phase creates a real
  Dockerfile.

The adjustment keeps deployment and CI attached to the portfolio product that
will continue evolving instead of polishing a learning-only application that
is now intentionally frozen.

## Known Limitations

- The Month 02 Ticket API is not the production OpsDesk application.
- Organization, membership, comments, attachments, audit history, standardized
  error responses, logging, correlation IDs, and pagination are not included.
- Historical `owner_id` values remain nullable without a trustworthy backfill.
- Advanced account security and refresh-token lifecycle are not implemented.
- No CI workflow or public deployment currently exists.

## Month 03 Transition

Month 03 begins with a separate public `opsdesk` repository and a design-first
Week 09. The first deliverables are product requirements, domain language,
organization-scoped roles, an ERD, an access-control matrix, an endpoint list,
and a prioritized GitHub issue backlog. Weeks 10-12 then turn those decisions
into a tested backend with consistent errors, validation, logging, correlation
IDs, pagination, CI, and an early deployed preview.
