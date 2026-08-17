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
- [ ] Ticket table and database constraints
- [ ] CRUD and query exercises
- [ ] One-to-many and many-to-many relationships
- [ ] Join and aggregation exercises
- [ ] Index and query-plan exercise
- [ ] Transaction, commit, and rollback exercises
- [ ] Ticket ERD and SQL project documentation
- [ ] SQL verification and Python regression checks
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

- Review PostgreSQL data types and database-owned identifiers.
- Design the core `tickets` table before writing its schema.
- Add primary-key, required-field, default, and check constraints.
- Execute and inspect the first schema script against `opsdesk_dev`.
- Intentionally test invalid inserts and explain each database error.
