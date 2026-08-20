# Week 06 Plan

## Date

17 August - 23 August 2026

## Main Focus

- PostgreSQL fundamentals
- Relational database concepts
- SQL data-definition and data-manipulation statements
- Primary keys, foreign keys, and constraints
- One-to-many and many-to-many relationships
- Filtering, ordering, aggregation, and joins
- Index purpose and tradeoffs
- Transactions, commit, and rollback
- Ticket database schema and ERD
- Repeatable SQL scripts and verification

## Why This Week Exists

Week 05 created a complete in-memory Ticket API. Its repository stores tickets
inside one Python process, so data disappears when the application stops and
cannot be shared safely across multiple application processes.

Week 06 introduces the relational database concepts needed to replace that
temporary storage later. The goal is to understand PostgreSQL and SQL directly
before an ORM hides the queries and database behavior.

The FastAPI application will not be connected to PostgreSQL this week.
SQLAlchemy and Alembic remain Week 07 topics. Authentication remains a Week 08
topic.

## Learning Goals

- Explain what a relational database, table, row, column, and schema represent.
- Connect to a local PostgreSQL server through `psql`.
- Create a dedicated development database without exposing credentials.
- Define tables with appropriate PostgreSQL data types.
- Explain and use primary-key, foreign-key, unique, not-null, default, and check
  constraints.
- Model one-to-many and many-to-many relationships.
- Insert, select, update, and delete records with SQL.
- Filter, order, limit, group, and aggregate query results.
- Join related tables and explain the difference between inner and outer joins.
- Explain why indexes improve some reads but add storage and write costs.
- Use a transaction to group operations atomically.
- Demonstrate commit and rollback behavior.
- Produce a readable Ticket schema, seed script, query exercises, and ERD.
- Verify scripts against a dedicated local learning database.

## Environment Policy

- Verify the current stable PostgreSQL release and supported macOS installation
  guidance from official sources before installation.
- Do not use preview, beta, release-candidate, or development releases.
- Audit existing PostgreSQL installations and commands before adding another
  installation.
- Choose one local PostgreSQL workflow and document the reason.
- Keep database credentials, passwords, connection URLs, and `.env` files out of
  Git.
- Use a dedicated bootcamp database and role rather than a personal or production
  database.
- Do not add SQLAlchemy, Alembic, an async database driver, or authentication.
- Do not add Docker only to run PostgreSQL; Docker remains part of its planned
  month.
- Keep the Week 05 in-memory API unchanged during the SQL fundamentals week.

## Daily Plan

### Monday

PostgreSQL concepts, environment audit, and first connection.

Status: completed on 17 August 2026.

Practice:

- Review the difference between an application, database server, database, and
  client.
- Explain relational tables, rows, columns, and schemas.
- Inspect existing PostgreSQL and `psql` installations.
- Verify the current stable PostgreSQL release through official sources.
- Choose and document one supported local installation method.
- Start the local PostgreSQL server deliberately.
- Inspect the current PostgreSQL version and connection information.
- Create a dedicated local bootcamp role and database.
- Connect through `psql` and inspect databases, schemas, and tables.
- Record safe start, stop, connect, and inspection commands.

Outcome:

- Verified PostgreSQL 18.6 as the current stable release and Homebrew as the
  supported local workflow.
- Installed and started PostgreSQL 18.6 on `localhost:5432`.
- Created the non-superuser `opsdesk_app` role and the owned `opsdesk_dev`
  database.
- Required SCRAM authentication for the OpsDesk application connection while
  keeping credentials outside the repository.
- Verified the client version, server version, service state, role attributes,
  database ownership, schema information, and password-authenticated TCP
  connection.
- Documented the `psql`-first workflow and reserved pgAdmin for secondary visual
  inspection.

### Tuesday

Data types, table definition, and constraints.

Practice:

- Compare integer, text, timestamp, boolean, and identity types.
- Design the core `tickets` table before writing SQL.
- Choose server-owned and client-owned fields.
- Add a generated primary key.
- Add not-null, default, and check constraints.
- Protect allowed priority and status values at the database boundary.
- Protect normalized title length with an intentional constraint.
- Execute the schema script against the dedicated learning database.
- Inspect the created table definition through `psql`.
- Intentionally attempt invalid inserts and explain each database error.

Outcome:

- Compared the relevant PostgreSQL types and classified client-owned and
  server-owned Ticket fields.
- Designed and created the core `tickets` table through a repeatable SQL
  script.
- Added a generated identity primary key, required fields, defaults, and named
  constraints for title, priority, status, and timestamp order.
- Executed the schema as the non-superuser `opsdesk_app` role and verified that
  it owns the table.
- Inspected the table and all stored constraint definitions through `psql` and
  `pg_constraint`.
- Verified database-generated identity, status, and timestamp values through
  successful inserts.
- Triggered each intended database error and confirmed that rejected rows did
  not persist.
- Demonstrated that failed inserts may consume identity values and that an
  identity is not a gapless row count.

### Wednesday

CRUD statements and result queries.

Practice:

- Insert individual and multiple ticket rows.
- Use `RETURNING` to inspect server-generated values.
- Select all columns and selected columns.
- Filter with `WHERE`.
- Combine predicates with `AND`, `OR`, and `IN`.
- Sort with `ORDER BY`.
- Limit results deliberately.
- Update specific rows without accidentally updating the whole table.
- Delete specific rows without accidentally deleting the whole table.
- Compare application validation with database constraints.
- Create a repeatable seed script and a separate query-practice script.

Outcome:

- Created a repeatable six-row Ticket seed script with multi-row `INSERT` and
  `RETURNING`.
- Used `TRUNCATE ... RESTART IDENTITY` only against the dedicated learning
  database and executed the script atomically.
- Practiced explicit-column selects, filtering, `IN`, `AND`, `OR`, predicate
  grouping, deterministic ordering, and limiting.
- Demonstrated the result difference between default boolean precedence and an
  explicitly parenthesized business rule.
- Previewed the exact target before each data-changing statement.
- Updated one Ticket with a scoped predicate and set `updated_at` explicitly.
- Deleted one closed Ticket using both identifier and expected-state guards.
- Verified affected rows with `RETURNING` and confirmed the final persistent
  dataset.

### Thursday

Relationships and joins.

Status: completed on 20 August 2026.

Practice:

- Add a `comments` table for a one-to-many Ticket relationship.
- Add `tags` and `ticket_tags` for a many-to-many relationship.
- Define foreign keys and deliberate delete behavior.
- Explain parent and child rows.
- Insert related records in a valid order.
- Query tickets with comments through an inner join.
- Use a left join to retain tickets that have no comments.
- Query tickets with tags through the junction table.
- Use grouping and aggregate functions to count related rows.
- Update the ERD to show keys and cardinality.

Outcome:

- Created `comments`, `tags`, and `ticket_tags` through a repeatable relationship
  schema script.
- Verified one-to-many and many-to-many foreign keys and deliberate cascade
  behavior through `psql` metadata.
- Added a composite junction-table primary key and normalized unique Tag names.
- Reordered scripts into schema, seed, join, and mutating CRUD dependency order.
- Seeded Tickets, comments, Tags, and assignments atomically with deterministic
  identifiers.
- Compared inner joins with left joins, including Tickets without related rows.
- Traversed the Ticket-Tag relationship through two explicit joins.
- Grouped child rows, counted nullable identifiers, and demonstrated the
  difference between `COUNT(*)` and `COUNT(child_id)`.
- Produced ordered per-Ticket Tag summaries with `STRING_AGG` and `COALESCE`.
- Deferred the ERD and destructive cascade verification to Friday alongside
  index and transaction practice.

### Friday

Indexes, query plans, and transactions.

Practice:

- Explain how PostgreSQL can find rows with and without an index.
- Identify columns that may support real Ticket API query patterns.
- Avoid indexing every column without evidence.
- Create one justified secondary index.
- Inspect a query with `EXPLAIN` and discuss the limitations of a tiny dataset.
- Compare primary-key indexes with manually created indexes.
- Begin, commit, and roll back transactions.
- Demonstrate that a rolled-back change is not persisted.
- Demonstrate why related writes may need one atomic transaction.

### Saturday

Ticket SQL project completion and verification.

Practice:

- Review every schema constraint and relationship.
- Run the schema and seed scripts against a clean dedicated database.
- Run CRUD, join, aggregation, index, and transaction exercises.
- Verify expected valid and invalid operations.
- Confirm scripts stop when an unexpected SQL error occurs.
- Review destructive statements before execution.
- Complete the project README and ERD.
- Run the existing Python regression suite to confirm Week 05 remains stable.
- Review the complete feature-branch diff.
- Confirm no credentials, connection secrets, or machine-specific paths are
  included.
- Open and review the Week 06 pull request.

### Sunday

Week 06 report and Week 07 preparation.

Practice:

- Complete `weekly-reports/week-06.md`.
- Review PostgreSQL and SQL interview questions.
- Update repository status and documentation.
- Explain the SQL schema and important queries without reading them.
- Prepare the Week 07 SQLAlchemy and Alembic plan without starting it early.

## Architecture Context

Week 05 currently uses:

```text
FastAPI route
    |
    v
TicketService
    |
    v
InMemoryTicketRepository
    |
    v
Python dictionary
```

Week 06 studies the future persistence target separately:

```text
psql and SQL scripts
    |
    v
PostgreSQL server
    |
    v
Ticket relational schema
```

Week 07 will later connect these paths through a SQLAlchemy repository and
Alembic migrations. Week 06 must first make the SQL and database behavior
understandable without ORM abstraction.

## Planned Data Model

The final columns and constraints must be decided before implementation, but the
learning model will include these relationships:

```text
tickets 1 -------- * comments

tickets * -------- * tags
          through
        ticket_tags
```

This model is intentionally smaller than the final OpsDesk schema. Users,
organizations, roles, authentication, attachments, and authorization are not
part of Week 06.

## Planned Project Structure

```text
projects/week-06-postgresql-sql/
├── README.md
├── docs/
│   └── ticket-erd.md
└── sql/
    ├── 001_schema.sql
    ├── 002_relationship_schema.sql
    ├── 003_ticket_seed.sql
    ├── 004_relationship_seed.sql
    ├── 005_join_queries.sql
    ├── 006_crud_queries.sql
    └── 007_transactions.sql
```

Files should be created only when the related concept is understood. SQL
scripts should have one clear responsibility and should not contain credentials.

## Notes To Write

- `notes/postgresql/postgresql-fundamentals.md`
- `notes/postgresql/sql-queries-and-transactions.md`

## Verification Goals

- PostgreSQL and `psql` versions are documented.
- The dedicated learning database can be recreated safely.
- The schema script creates all planned tables and constraints.
- The seed script inserts valid deterministic sample data.
- Invalid priority, status, foreign-key, and required-field operations fail.
- CRUD queries affect only their intended rows.
- One-to-many and many-to-many joins return expected results.
- Aggregation queries return explainable counts.
- The selected index has a documented query purpose.
- A committed transaction persists changes.
- A rolled-back transaction does not persist changes.
- Existing Python tests continue to pass.
- No test or script targets an unrelated database.

## Git Workflow Goal

Use a dedicated Week 06 feature branch.

Planned branch:

```text
feature/week-06-postgresql-sql
```

Review every SQL diff carefully because an incorrect `UPDATE`, `DELETE`, or
schema statement can modify more data than intended.

## Expected Commits

- `week-06: document PostgreSQL environment`
- `week-06: add ticket database schema`
- `week-06: add ticket CRUD queries`
- `week-06: add ticket relationships and joins`
- `week-06: add index and transaction exercises`
- `week-06: document PostgreSQL fundamentals`
- `week-06: complete PostgreSQL fundamentals pull request`
- `week-06: add weekly report`

## Interview Questions

- What is the difference between a database server, database, schema, and table?
- What is a relational database?
- What is a primary key?
- What does a foreign key guarantee?
- What is the difference between one-to-many and many-to-many relationships?
- Why does a many-to-many relationship need a junction table?
- What is the difference between `WHERE` and `HAVING`?
- What is the difference between an inner join and a left join?
- What do `INSERT`, `SELECT`, `UPDATE`, and `DELETE` do?
- Why should `UPDATE` and `DELETE` statements usually include a `WHERE` clause?
- What does a database constraint protect?
- Why should application validation not replace database constraints?
- What is an index?
- Why should every column not automatically receive an index?
- What write and storage costs can an index add?
- What is a transaction?
- What do commit and rollback mean?
- What does atomicity protect?
- What problem does `EXPLAIN` help investigate?
- Why should SQL be understood before using an ORM?

## Definition of Done

Week 06 is complete when:

- A supported stable PostgreSQL environment is installed and documented.
- A dedicated local learning database and role are used safely.
- The Ticket relational schema is implemented through repeatable SQL scripts.
- Primary keys, foreign keys, constraints, and relationships can be explained.
- CRUD, filter, ordering, join, grouping, and aggregation queries work.
- One justified secondary index and its tradeoffs are documented.
- Commit and rollback behavior are demonstrated.
- The ERD matches the implemented schema.
- SQL verification and the existing Python regression suite pass.
- The feature branch is reviewed and merged through a pull request.
- The Week 06 report is complete.

## Guardrails

- Use a dedicated bootcamp database only.
- Inspect the active database and target rows before destructive statements.
- Do not place passwords or complete connection URLs in tracked files.
- Do not use the default superuser for application-style exercises after setup.
- Do not connect the FastAPI project to PostgreSQL during the fundamentals week.
- Do not add SQLAlchemy or Alembic before Week 07.
- Do not add authentication before Week 08.
- Do not use Docker before its planned month merely to start PostgreSQL.
- Do not copy SQL that cannot be explained statement by statement.
- Keep SQL scripts small, ordered, repeatable, and reviewable.
