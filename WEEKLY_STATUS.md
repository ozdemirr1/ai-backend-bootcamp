# Weekly Status

## Current Week

Week 06

## Date

17 August - 23 August

## Current Focus

- PostgreSQL fundamentals
- Relational tables, rows, columns, and schemas
- SQL data types and constraints
- Primary and foreign keys
- One-to-many and many-to-many relationships
- `SELECT`, `INSERT`, `UPDATE`, and `DELETE`
- Filtering, ordering, grouping, and joins
- Index purpose and tradeoffs
- Transactions, commit, and rollback
- Ticket database schema, SQL scripts, and ERD

## Completed

- [x] Week 05 report completed
- [x] Week 05 pull request merged and branches cleaned
- [x] Week 06 plan created
- [x] Week 05-to-Week 06 transition quality checks
- [x] Second LinkedIn progress update published
- [x] PostgreSQL environment and version audit
- [x] PostgreSQL 18.6 installed and verified
- [x] Dedicated local role and database
- [x] SCRAM authentication verified for the application connection
- [x] Ticket table and database constraints
- [x] CRUD and query exercises
- [x] One-to-many and many-to-many relationships
- [x] Join and aggregation exercises
- [x] Index and query-plan exercise
- [x] Transaction, commit, and rollback exercises
- [x] Ticket ERD and SQL project documentation
- [x] SQL verification and Python regression checks
- [ ] Feature branch and pull request practice
- [ ] Week 06 report

## Problems

- No current blockers.

## Monday Outcome

- Audited the existing Homebrew, PostgreSQL, service, client, and server state.
- Removed the confirmed disposable `visabot` database before changing servers.
- Verified PostgreSQL 18.6 as the current stable release from official sources.
- Installed PostgreSQL 18.6 and initialized its checksum-enabled local cluster.
- Stopped PostgreSQL 14 and started PostgreSQL 18 on `localhost:5432`.
- Configured the shell to use the PostgreSQL 18 client tools by default.
- Created the non-superuser `opsdesk_app` login role and its `opsdesk_dev`
  database.
- Added specific `pg_hba.conf` rules requiring SCRAM authentication for the
  OpsDesk application connection.
- Verified the role, database owner, schema, server version, connection details,
  and password-authenticated TCP connection through `psql`.
- Kept the Week 05 FastAPI application in-memory and did not start ORM work.

## Tuesday Outcome

- Compared core PostgreSQL data types and assigned ownership for each Ticket
  field.
- Designed the `tickets` table before writing SQL.
- Created and executed the repeatable `sql/001_schema.sql` script through the
  non-superuser application connection.
- Added an identity primary key, required fields, defaults, and four named
  check constraints.
- Inspected the stored table and constraint definitions through `psql` and the
  PostgreSQL system catalog.
- Verified valid inserts, database-generated values, and persistent data.
- Intentionally triggered title, priority, status, required-field, timestamp,
  and identity errors.
- Confirmed that failed inserts do not persist rows but can consume identity
  sequence values.
- Kept SQLAlchemy, Alembic, and FastAPI database integration out of Week 06.

## Wednesday Outcome

- Created a deterministic six-row Ticket seed dataset with varied priorities
  and statuses.
- Used multi-row `INSERT` and `RETURNING` to inspect generated values.
- Executed the destructive seed reset atomically with `ON_ERROR_STOP` and a
  single transaction.
- Practiced explicit-column selects, filtering, `IN`, `AND`, `OR`, predicate
  grouping, ordering, and limiting.
- Compared ungrouped and parenthesized boolean predicates through their actual
  result sets.
- Previewed mutation targets with the same predicates used by the changes.
- Updated one Ticket, changed its status, and advanced `updated_at` explicitly.
- Deleted one expected closed Ticket with both identifier and state guards.
- Verified the final five-row table and confirmed that unrelated rows remained
  unchanged.

## Thursday Outcome

- Modeled a one-to-many relationship from Tickets to comments.
- Modeled a many-to-many relationship from Tickets to reusable Tags through a
  `ticket_tags` junction table.
- Added three foreign keys with deliberate `ON DELETE CASCADE` behavior.
- Used a composite `(ticket_id, tag_id)` primary key to prevent duplicate Tag
  assignments.
- Protected normalized, unique Tag names and validated comment body format.
- Inspected the implemented tables, indexes, checks, and foreign keys through
  `psql` and `pg_constraint`.
- Reordered the SQL scripts so schemas, seeds, joins, and mutating CRUD practice
  can be executed in dependency order.
- Seeded six Tickets, six comments, five Tags, and six Ticket-Tag assignments in
  one atomic workflow.
- Compared inner and left joins through their actual result sets.
- Traversed the many-to-many relationship through the junction table.
- Grouped related rows and counted nullable child identifiers deliberately.
- Demonstrated why `COUNT(*)` and `COUNT(child_id)` differ after a left join.
- Combined ordered Tag names with `STRING_AGG` and represented a missing Tag set
  with `COALESCE`.

## Friday Outcome

- Verified actual cascade behavior inside a transaction without changing the
  deterministic seed state.
- Confirmed that deleting a Ticket removes its Comment and Ticket-Tag assignment
  while preserving the reusable Tag row.
- Demonstrated that `ROLLBACK` restores both direct and cascaded changes.
- Created a Mermaid ERD matching all implemented tables, keys, cardinalities,
  and delete behavior.
- Connected the future status-filtered Ticket API query to one justified
  `(status, ticket_id)` secondary index.
- Compared execution plans before and after index creation with
  `EXPLAIN (ANALYZE, BUFFERS)`.
- Confirmed that PostgreSQL correctly prefers a sequential scan for the tiny
  seed dataset.
- Verified that the composite index can satisfy both filtering and ordering
  without a separate sort.
- Used `ANALYZE` to refresh planner statistics and separated cost estimates from
  elapsed time.
- Committed a Ticket and related Comment atomically through two SQL statements.
- Verified committed persistence, then committed a cascade cleanup of the demo
  relationship.
- Kept SQLAlchemy, Alembic, database drivers, and FastAPI database integration
  out of the SQL fundamentals week.

## Saturday Outcome

- Recreated `opsdesk_dev` from an empty database owned by the non-superuser
  `opsdesk_app` role.
- Applied all schema and seed files atomically in dependency order and verified
  four table owners, sixteen columns, fourteen named constraints, and expected
  row counts.
- Re-ran join and aggregation queries against the clean deterministic dataset.
- Verified guarded CRUD mutations from a known seed state, including one
  expected update and one expected cascade delete.
- Restored the seed before transaction tests and reproduced rollback, commit,
  atomic related writes, and cascade cleanup behavior.
- Created and inspected the justified composite index on the clean database.
- Confirmed that PostgreSQL naturally prefers a sequential scan for six rows
  while the index remains eligible for the real filter-and-order query shape.
- Demonstrated that `CURRENT_TIMESTAMP` remains fixed throughout one
  transaction, so an insert and update in that transaction can share a value.
- Verified title, priority, foreign-key, composite-key, and unique-name
  rejection without persisting invalid rows.
- Demonstrated that `ON_ERROR_STOP=1` and a single transaction prevent a
  partially applied multi-statement workflow.
- Restored deterministic IDs and seed counts after destructive and invalid
  exercises.
- Reviewed all destructive SQL targets and confirmed that no credential,
  connection URI, or machine-specific path is tracked.
- Passed Ruff lint, Ruff formatting, and all 107 repository tests.

## Week 05 Handoff

- Completed the in-memory Ticket CRUD API with explicit presentation, service,
  repository, and domain boundaries.
- Passed 31 endpoint tests and 107 tests in the complete repository suite.
- Verified the CRUD lifecycle through TestClient, Uvicorn, curl, Swagger UI,
  and OpenAPI.
- Merged pull request #3 through merge commit `b02c983`.
- Synchronized `main` with `origin/main` and removed the merged feature branch.
- Recorded the complete result in `weekly-reports/week-05.md`.
- PostgreSQL, SQLAlchemy, Alembic, and authentication were not started early.

## Next Tasks

- Review and commit the Saturday verification documentation.
- Open and review the Week 06 pull request.
- Complete the Week 06 report and prepare Week 07.
