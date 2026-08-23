# Week 06 Report

## Date

17 August - 23 August 2026

## Main Focus

- PostgreSQL server and `psql` client fundamentals
- Dedicated database roles and password authentication
- Relational schema design and data ownership
- SQL data types, defaults, and constraints
- Primary keys, foreign keys, and identity columns
- One-to-many and many-to-many relationships
- Deterministic development seed data
- CRUD, filtering, ordering, joins, grouping, and aggregation
- Transactions, commit, rollback, and atomic script execution
- B-tree indexes and query-plan inspection
- Repeatable database reconstruction and verification

## What I Completed

- [x] Installed and verified PostgreSQL 18.6
- [x] Distinguished the PostgreSQL server from the `psql` client
- [x] Created the non-superuser `opsdesk_app` application role
- [x] Created the role-owned `opsdesk_dev` development database
- [x] Required SCRAM password authentication for the local application connection
- [x] Designed a relational Ticket data model before implementing it
- [x] Added database-generated identity primary keys
- [x] Added defaults, required fields, and named check constraints
- [x] Added `tickets`, `comments`, `tags`, and `ticket_tags` tables
- [x] Modelled one-to-many Ticket comments
- [x] Modelled many-to-many Ticket tags with a junction table
- [x] Added deliberate `ON DELETE CASCADE` behavior
- [x] Added deterministic Ticket, Comment, Tag, and Ticket-Tag seed data
- [x] Practiced CRUD, filtering, ordering, limiting, and boolean predicates
- [x] Practiced inner joins, left joins, grouping, and aggregation
- [x] Compared `COUNT(*)` with counting a nullable joined column
- [x] Demonstrated commit, rollback, and atomic related writes
- [x] Added a justified composite index and inspected its query plans
- [x] Recreated the development database from an empty state
- [x] Re-ran the schema and seed scripts in dependency order
- [x] Verified expected constraint, foreign-key, and uniqueness failures
- [x] Documented the schema with a Mermaid ERD
- [x] Passed Ruff checks and the complete 107-test Python suite
- [x] Merged pull request #4 and cleaned the feature branches

## What I Learned

### PostgreSQL Components and Roles

- The `postgres` server owns storage, query execution, concurrency, and client
  connections.
- `psql` is a client that sends SQL and meta-commands to a PostgreSQL server.
- `psql --version` verifies the installed client, while `SELECT version()`
  verifies the server handling the active connection.
- A PostgreSQL server can contain multiple logically isolated databases.
- Roles exist at the PostgreSQL cluster level and receive access through
  ownership and grants.
- An application role should follow the principle of least privilege instead
  of running as a superuser.

### Constraints and Data Integrity

- `NOT NULL` prevents a missing value but does not reject an empty or
  whitespace-only string.
- `DEFAULT` supplies a value only when an insert omits that column.
- A named `CHECK` constraint protects a specific invariant and makes failures
  easier to diagnose.
- PostgreSQL constraints remain necessary even when FastAPI and Pydantic
  validate requests, because not every future write must pass through that API.
- The database rejects surrounding title whitespace, while the API currently
  normalizes accepted titles before they reach the domain layer.

### Identity and Relationships

- `GENERATED ALWAYS AS IDENTITY` makes PostgreSQL responsible for identifiers
  and rejects ordinary client-supplied values.
- Identity sequences are not gapless: failed or rolled-back inserts may consume
  values without persisting rows.
- A foreign key belongs on the many side of a one-to-many relationship.
- A junction row represents one association in a many-to-many relationship and
  may also store information about that association.
- The composite primary key `(ticket_id, tag_id)` prevents the same tag from
  being assigned to the same ticket more than once.
- Cascade deletion is useful for dependent rows but must be treated as a
  destructive data-lifecycle decision.

### Queries and Aggregation

- `INNER JOIN` returns matching rows from both sides.
- `LEFT JOIN` preserves every row from the left side and fills missing child
  columns with `NULL`.
- After a left join, `COUNT(*)` counts the preserved parent row, while
  `COUNT(child_id)` counts only real non-null child identifiers.
- `AND` has higher precedence than `OR`; parentheses make business intent
  explicit and prevent accidental broad matches.
- A target should be previewed with `SELECT` before running a destructive
  `UPDATE` or `DELETE`.

### Transactions and Time

- A transaction protects atomicity: related operations either all commit or all
  roll back.
- `ON_ERROR_STOP=1` stops a `psql` script at the first error.
- Combined with `--single-transaction`, it prevents a script from leaving a
  partially applied state.
- `CURRENT_TIMESTAMP` is fixed at the start of the transaction,
  `statement_timestamp()` at the start of the statement, and
  `clock_timestamp()` follows the wall clock.
- `DEFAULT CURRENT_TIMESTAMP` applies during insert; `updated_at` must be
  changed explicitly or through a trigger during update.

### Indexes and Query Plans

- The composite index `(status, ticket_id)` supports status filtering followed
  by identifier ordering.
- Column order matters because the leading column determines which predicates
  can efficiently narrow the B-tree range.
- A primary-key index on `ticket_id` does not directly group rows by status.
- PostgreSQL correctly preferred a sequential scan for the six-row seed table;
  an index is not guaranteed to be faster for every dataset.
- `EXPLAIN (ANALYZE, BUFFERS)` shows the selected plan, actual work, timing, and
  buffer activity.
- Indexes consume storage and add maintenance work to inserts, updates, and
  deletes, so they should support observed query patterns.

### Repeatability

- `TRUNCATE ... RESTART IDENTITY` provides a deterministic development reset but
  is unsafe for production data.
- Seed scripts need a known starting state so identifiers and expected results
  remain stable.
- A state-changing SQL script may return different results on its second run;
  reseeding restores the expected preconditions.
- Recreating the database from nothing is stronger evidence of repeatability
  than testing only an already-prepared local database.

## Relational Model I Built

```text
tickets 1 -------- many comments
   |
   | many
   v
ticket_tags
   ^
   | many
   |
 tags
```

The implemented model contains four tables, 16 columns, and 14 named primary
key, foreign-key, unique, and check constraints. The final deterministic seed
state contains six tickets, six comments, five reusable tags, and six tag
assignments.

## SQL Files I Added

| File | Responsibility |
| --- | --- |
| `001_schema.sql` | Create the constrained Ticket table |
| `002_relationship_schema.sql` | Create comments, tags, and the junction table |
| `003_ticket_seed.sql` | Reset development data and seed Tickets |
| `004_relationship_seed.sql` | Seed Tags, Comments, and Ticket-Tag rows |
| `005_join_queries.sql` | Practice joins, grouping, and aggregation |
| `006_crud_queries.sql` | Practice filtering and state-changing CRUD |
| `007_transactions.sql` | Demonstrate rollback, commit, atomic writes, and cleanup |
| `008_indexes.sql` | Create the composite index and inspect query plans |

## Verification Results

- PostgreSQL server: 18.6
- Application role: `opsdesk_app`, non-superuser
- Development database: `opsdesk_dev`
- Application authentication: SCRAM password authentication verified
- Public tables: 4, all owned by `opsdesk_app`
- Columns: 16
- Named constraints: 14
- Deterministic rows: 6 Tickets, 6 Comments, 5 Tags, 6 assignments
- Secondary index: `tickets_status_ticket_id_idx`
- Ruff lint: passed
- Ruff formatting check: passed
- Repository tests: 107 passed
- Credentials or machine-specific paths tracked: none found

## GitHub Output

- Branch: `feature/week-06-postgresql-sql`
- Pull request: #4, `week-06: complete PostgreSQL and SQL fundamentals`
- Feature commits: 6
- Changed files in the pull request: 16
- Final feature commit: `e63f13b`
- Merge commit: `6c60128`
- Local and remote feature branches removed after merge
- Final `main` branch synchronized with `origin/main`

## Known Limitations

- The Week 05 FastAPI API still uses its in-memory repository.
- SQLAlchemy, Psycopg, and Alembic are intentionally deferred to Week 07.
- Database checks are currently manual SQL verification rather than automated
  integration tests.
- The learning role owns the development database; a production system may
  separate migration ownership from the restricted runtime role.
- Physical deletion and cascade behavior do not yet provide soft delete or an
  audit history.
- `updated_at` is updated explicitly rather than by a trigger.
- The tiny seed dataset demonstrates plan reasoning but is not a meaningful
  performance benchmark.
- Authentication and authorization remain scheduled for a later week.

## Next Week

Week 07 will connect the existing FastAPI architecture to PostgreSQL with
SQLAlchemy 2, Psycopg, and Alembic. The focus will be configuration through
environment variables, explicit ORM-to-domain mapping, migration-managed schema
history, a PostgreSQL repository implementation, request-scoped sessions, and
isolated database integration tests.
