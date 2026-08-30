# Week 07 Report

## Date

24 August - 30 August 2026

## Main Focus

- Synchronous SQLAlchemy 2 and Psycopg connectivity
- Environment-based, secret-aware database configuration
- Engine, Connection, Session, and transaction responsibilities
- Separate domain and persistence models
- Explicit ORM-to-domain mapping
- Alembic migration history
- PostgreSQL repository implementation
- FastAPI request-scoped database Sessions
- Guarded PostgreSQL integration tests
- Durable HTTP behavior across application restarts

## What I Completed

- [x] Added and locked SQLAlchemy, Psycopg, Alembic, and Pydantic Settings
- [x] Added required `DATABASE_URL` configuration without tracking secrets
- [x] Added testable Engine and Session factory functions
- [x] Kept the first persistence implementation synchronous
- [x] Renamed the living API to the stable `month-02-ticket-api` directory
- [x] Added a typed SQLAlchemy `TicketRecord`
- [x] Preserved identity, defaults, timestamps, constraints, and the listing index
- [x] Kept the persistence record separate from the domain `Ticket`
- [x] Added explicit record/domain mapper functions
- [x] Initialized Alembic and connected it to application metadata
- [x] Generated and reviewed revision `e07f08d4399d`
- [x] Verified upgrade, downgrade, re-upgrade, offline SQL, and schema drift
- [x] Added a storage-independent `TicketRepository` protocol
- [x] Added a PostgreSQL-backed SQLAlchemy repository
- [x] Kept repository `flush()` separate from transaction `commit()`
- [x] Added application lifespan and request-scoped Session dependencies
- [x] Connected the real PostgreSQL repository to the FastAPI application
- [x] Preserved fast in-memory HTTP tests through dependency overrides
- [x] Added guarded, opt-in PostgreSQL repository and HTTP integration tests
- [x] Verified rollback after request and commit failures
- [x] Verified a distinct Session for each request
- [x] Verified committed data across a real Uvicorn restart
- [x] Completed the Week 07 technical interview review
- [x] Merged pull request #5 and removed the feature branches

## What I Learned

### Psycopg, SQLAlchemy, and Alembic

- Psycopg is the PostgreSQL driver that performs the real database communication.
- SQLAlchemy provides SQL composition, ORM mapping, identity tracking, and
  unit-of-work behavior above the driver.
- Alembic owns ordered, reviewable, and reversible schema evolution.
- SQLAlchemy `create_all()` can create missing tables but does not replace a
  versioned migration history.
- Alembic autogeneration is a draft that must be reviewed for renames,
  destructive operations, constraints, indexes, and data changes.

### Engine, Connection, and Session

- The Engine owns database dialect and connection-pool configuration.
- Creating an Engine does not immediately open a PostgreSQL connection.
- A SQLAlchemy Connection manages a checked-out DBAPI/Psycopg connection.
- A Session is an ORM unit of work, identity map, and transaction coordinator;
  it is not merely a connection.
- A Session normally obtains a connection lazily when it first performs real
  database work.
- Mutable Sessions must not be shared globally or across concurrent requests.

### Flush, Refresh, Commit, and Rollback

- `flush()` sends pending SQL inside the current transaction without making it
  durable.
- PostgreSQL can return database-generated identity values during flush.
- `refresh()` deliberately reloads the current database representation into an
  ORM record.
- `commit()` makes the complete successful transaction durable.
- `rollback()` cancels uncommitted database work and resets Session state
  according to SQLAlchemy's lifecycle rules.
- Repository methods may flush for generated values and constraint detection,
  while the caller retains commit and rollback ownership.

### Domain and Persistence Boundaries

- `Ticket` protects business invariants and behavior.
- `TicketRecord` describes the relational storage representation.
- Mapper functions make string-to-enum conversion and record mutation explicit.
- Invalid persisted priority or status values must fail rather than silently
  entering the domain.
- Separate models add mapping code but prevent ORM and schema details from
  becoming the public API or business model.

### Repository and Transaction Design

- `TicketService` depends on the repository protocol rather than SQLAlchemy.
- The in-memory implementation keeps domain, service, and HTTP tests fast.
- The SQLAlchemy implementation owns queries, persistence mapping, `flush()`,
  and `refresh()`.
- Expected integrity failures are translated into repository-level errors.
- Driver and ORM exceptions are not exposed as public HTTP contracts.
- Request-level transaction ownership permits multiple operations to succeed
  or fail atomically.

### FastAPI Request Lifecycle

- Application lifespan creates the Engine and Session factory at startup and
  disposes the Engine during shutdown.
- Each database-backed request receives a new Session.
- The service dependency composes the request Session with the SQLAlchemy
  repository.
- Function-scoped dependency finalization commits before the response is sent.
- Request or commit errors trigger rollback, are re-raised, and prevent false
  success responses.
- Session cleanup always runs in `finally` and returns its connection resources.

### Integration-Test Isolation

- Destructive database tests run only against the dedicated `opsdesk_test`
  database.
- Guards reject the wrong database, a superuser, missing migrations, and dirty
  starting data.
- Transactional repository tests roll back ordinary work automatically.
- Tests that intentionally commit remove only their own unique records or
  captured identifiers.
- Mock lifecycle tests prove control flow; PostgreSQL tests prove real SQL,
  transaction, constraint, and visibility behavior.
- A zero final Ticket count is evidence that tests remain isolated and
  repeatable.

## Architecture Built

```text
HTTP request
    |
    v
FastAPI + Pydantic contracts
    |
    v
request-scoped Session dependency ----> commit / rollback / close
    |
    v
TicketService
    |
    v
TicketRepository protocol
    |
    +----> InMemoryTicketRepository     (fast tests)
    |
    +----> SqlAlchemyTicketRepository   (PostgreSQL runtime)
               |
               v
        TicketRecord <----> Ticket mapper
               |
               v
          SQLAlchemy Engine
               |
               v
             Psycopg
               |
               v
           PostgreSQL

Alembic -----------------------------> versioned schema history
```

## Migration Evidence

- Migration database: `opsdesk_migration_dev`
- Initial revision: `e07f08d4399d`
- Upgrade to head: passed
- Downgrade to base: passed
- Second upgrade to head: passed
- Offline transactional SQL review: passed
- `alembic current`: head verified
- `alembic check`: no new upgrade operations detected
- Application startup does not call `create_all()` or apply migrations

## Test Evidence

- Configuration and factory tests: 5
- Persistence metadata tests: 5
- Mapper tests: 5
- PostgreSQL repository integration tests: 11
- PostgreSQL HTTP integration tests: 8
- Final run with database tests disabled: 138 passed, 19 skipped
- Final run with database tests enabled: 157 passed
- Ruff lint: passed
- Ruff formatting: 90 files formatted
- Dependency lock, synchronization, and compatibility checks: passed
- Git diff checks: passed
- Final `opsdesk_test` Ticket count: 0

The HTTP integration suite verifies committed CRUD, filtering and limiting,
`404`, `422`, rollback after a flushed write, commit failure without a false
`201`, and a distinct Session per request. A manual Uvicorn stop/start cycle
proved that a committed Ticket survived the application process and could be
deleted precisely afterward.

## Interview Review

I explained:

- the separate responsibilities of Psycopg, SQLAlchemy, and Alembic
- Engine, Connection, Session, lazy checkout, and request scope
- `flush`, `refresh`, `commit`, and `rollback`
- why Alembic migrations replace `create_all()` for schema evolution
- domain-model and persistence-model separation
- repository protocols and caller-owned transactions
- dedicated-database integration-test isolation
- the complete POST request path from validation through commit and cleanup

The review confirmed that I can explain the architecture and transaction
behavior instead of only reproducing the implementation.

## GitHub Output

- Branch: `feature/week-07-sqlalchemy-alembic`
- Pull request: #5, `Week 07: integrate SQLAlchemy, Alembic, and PostgreSQL persistence`
- Feature commits: 7
- Changed files in the pull request: 42
- Final feature commit: `fbd1a9e`
- Merge commit: `7ebc076`
- Local and remote feature branches removed after merge
- Final `main` branch synchronized with `origin/main`

## Known Limitations

- The Ticket API has no user identity, login, or authorization yet.
- Tickets do not yet belong to authenticated users.
- The first persistence workflow is intentionally synchronous.
- Only the Ticket aggregate is mapped; the Week 06 comments and tags remain a
  bounded relational-learning artifact.
- The repository has no production CI workflow or deployed environment yet.
- The application currently uses one learning role for migration and runtime;
  production systems may separate those privileges.
- Refresh tokens, token revocation, organization access, and advanced account
  recovery are outside the completed Week 07 scope.

## Next Week

Week 08 will add the authentication and authorization foundation without
starting Docker, Redis, or AI work early. The focus is password hashing,
registration, login, JWT access tokens, current-user resolution, protected
routes, Ticket ownership, object-level access checks, and bounded role-level
authorization.
