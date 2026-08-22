# Week 06 PostgreSQL and SQL Fundamentals

## Goal

Design and verify a small relational ticket database by working directly with
PostgreSQL and SQL before introducing an ORM.

## Current Scope

- PostgreSQL 18.6 local development environment
- Dedicated `opsdesk_app` login role
- Dedicated `opsdesk_dev` database
- SCRAM password authentication for the application connection
- `psql` inspection and repeatable SQL scripts
- Relational ticket schema, constraints, CRUD, relationships, joins, indexes,
  transactions, and an ERD

The FastAPI application is not connected to PostgreSQL during Week 06.
SQLAlchemy and Alembic remain Week 07 topics, and authentication remains a Week
08 topic.

## Verified Environment

The following environment was verified on 17 August 2026:

- PostgreSQL server 18.6
- `psql` client 18.6
- Homebrew service `postgresql@18`
- Server address `localhost`
- Server port `5432`
- Database `opsdesk_dev`
- Database owner and application role `opsdesk_app`
- Application authentication method `scram-sha-256`

No password, connection URL, or `.env` file belongs in this repository.

## Service and Connection Commands

Inspect or control the local server:

```bash
brew services list
brew services start postgresql@18
brew services stop postgresql@18
pg_isready -h localhost -p 5432
```

Connect through TCP as the application role:

```bash
psql -h localhost -U opsdesk_app -d opsdesk_dev -W
```

Inspect the active identity after connecting:

```sql
SELECT current_user, current_database();
```

Useful `psql` inspection commands:

```text
\conninfo
\dn+
\dt
\q
```

## Current Structure

The SQL scripts are numbered in dependency order:

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
    ├── 007_transactions.sql
    └── 008_indexes.sql
```

Each SQL file will have one clear responsibility and will contain no secrets.

## Core Ticket Schema

`sql/001_schema.sql` creates the first `tickets` table with:

- a database-generated `BIGINT` identity primary key;
- required title, priority, status, and timestamp fields;
- an `open` default status;
- database-generated creation and update timestamps;
- normalized title requirements;
- allowed priority and status values; and
- chronological timestamp protection.

Execute the schema as the dedicated application role:

```bash
psql -X \
  -h localhost \
  -U opsdesk_app \
  -d opsdesk_dev \
  -W \
  -v ON_ERROR_STOP=1 \
  -f projects/week-06-postgresql-sql/sql/001_schema.sql
```

Inspect the result from an interactive `psql` session:

```text
\d+ tickets
```

The schema was verified with successful inserts around intentional violations
of every named check constraint, a required-field rule, and the generated
identity boundary. Failed rows were not stored. Their generated identity
values were still consumed, demonstrating that a sequence supplies values
rather than gapless row numbering. The primary key separately enforces
uniqueness.

## Relationships

`sql/002_relationship_schema.sql` adds:

- a one-to-many relationship from `tickets` to `comments`;
- reusable, normalized, unique rows in `tags`; and
- a many-to-many relationship through the `ticket_tags` junction table.

The junction table uses `(ticket_id, tag_id)` as a composite primary key, so a
Tag cannot be assigned to the same Ticket twice. Foreign keys use deliberate
`ON DELETE CASCADE` behavior for dependent comments and relationship rows.
Deleting a Ticket does not delete reusable Tag rows.

## Seed and CRUD Practice

`sql/003_ticket_seed.sql` resets all four local tables and creates six
deterministic Ticket rows. `sql/004_relationship_seed.sql` then inserts five
Tags, six comments, and six Ticket-Tag assignments. These scripts are
intentionally destructive and must target only the dedicated `opsdesk_dev`
learning database.

Run it atomically so an unexpected insert error also rolls back the truncate:

```bash
psql -X \
  -h localhost \
  -U opsdesk_app \
  -d opsdesk_dev \
  -W \
  -v ON_ERROR_STOP=1 \
  --single-transaction \
  -f projects/week-06-postgresql-sql/sql/003_ticket_seed.sql \
  -f projects/week-06-postgresql-sql/sql/004_relationship_seed.sql
```

`sql/006_crud_queries.sql` contains explicit-column selects, filtering,
predicate grouping, ordering, limiting, a scoped update, and a guarded delete.
Run the seed first whenever the CRUD exercise needs its known starting state:

```bash
psql -X \
  -h localhost \
  -U opsdesk_app \
  -d opsdesk_dev \
  -W \
  -v ON_ERROR_STOP=1 \
  --single-transaction \
  -f projects/week-06-postgresql-sql/sql/006_crud_queries.sql
```

The mutation workflow previews targets with `SELECT`, scopes every change with
`WHERE`, updates `updated_at` explicitly, and inspects affected rows through
`RETURNING`.

## Join and Aggregation Practice

`sql/005_join_queries.sql` demonstrates:

- an inner join that returns only Tickets with comments;
- a left join that preserves Tickets without comments;
- traversal of the Ticket-Tag many-to-many relationship;
- comment and Tag counts grouped by Ticket; and
- ordered Tag summaries with `STRING_AGG` and `COALESCE`.

The verified dataset returns six inner-joined comment rows and eight
left-joined rows. Ticket 3 and Ticket 6 have zero comments, while Ticket 6 has
zero Tags and receives the summary value `no tags`.

## ERD

`docs/ticket-erd.md` records the implemented entities, columns, primary keys,
foreign keys, cardinalities, and delete behavior. It represents the same schema
declared by `001_schema.sql` and `002_relationship_schema.sql`.

## Index and Query-Plan Practice

`sql/008_indexes.sql` creates one secondary index for the future Ticket-listing
query pattern:

```sql
CREATE INDEX tickets_status_ticket_id_idx
    ON tickets (status, ticket_id);
```

The query filters by status, orders by Ticket identifier, and applies a limit.
`EXPLAIN (ANALYZE, BUFFERS)` showed that PostgreSQL naturally prefers a
sequential scan for the six-row seed table. A controlled diagnostic verified
that the composite index can provide both filtering and ordering without a
separate sort. Sequential scans are not disabled in normal operation.

Execute the index exercise atomically:

```bash
psql -X \
  -h localhost \
  -U opsdesk_app \
  -d opsdesk_dev \
  -W \
  -v ON_ERROR_STOP=1 \
  --single-transaction \
  -f projects/week-06-postgresql-sql/sql/008_indexes.sql
```

## Transaction Practice

`sql/007_transactions.sql` manages explicit transaction boundaries and must be
executed without `--single-transaction`:

```bash
psql -X \
  -h localhost \
  -U opsdesk_app \
  -d opsdesk_dev \
  -W \
  -v ON_ERROR_STOP=1 \
  -f projects/week-06-postgresql-sql/sql/007_transactions.sql
```

The script verifies that rollback restores a Ticket and its cascaded dependent
rows. It also commits a related Ticket and Comment write, verifies both rows,
and commits a cleanup that cascades to the demonstration Comment.

## Clean-Database Verification Order

The SQL files have separate responsibilities, but the mutating exercises do not
all share the same preconditions. Use this order when verifying the complete
project from an empty `opsdesk_dev` database:

1. Run `001_schema.sql` through `004_relationship_seed.sql` together in one
   transaction.
2. Run the read-only `005_join_queries.sql` file.
3. Run `006_crud_queries.sql` from the deterministic seed state.
4. Re-run `003_ticket_seed.sql` and `004_relationship_seed.sql` because the CRUD
   exercise resolves Ticket 2 and deletes Ticket 5.
5. Run `007_transactions.sql` without an outer single transaction because it
   controls its own commit and rollback boundaries.
6. Run `008_indexes.sql` once on the clean schema.
7. Re-run the two seed files to leave deterministic identifiers and rows for
   later inspection. The secondary index remains present after the seed reset.

The final verified state contains six Tickets, six comments, five Tags, six
Ticket-Tag assignments, and the `tickets_status_ticket_id_idx` secondary index.

Mutation verification must begin from a known seed state. Running the CRUD file
again after it has already deleted Ticket 5 correctly produces `DELETE 0`, but
that does not independently verify the intended deletion path.

`CURRENT_TIMESTAMP` is fixed at transaction start. When seed inserts and the
Ticket update run inside the same outer transaction, `created_at` and
`updated_at` can be equal even after `UPDATE 1`. This is normal PostgreSQL
transaction-time behavior.

The clean-database audit also verified expected title, priority, foreign-key,
composite-key, and unique-name failures. `ON_ERROR_STOP=1` combined with a
single transaction prevented an earlier valid insert from remaining after a
later constraint failure.

## Safety Rules

- Review the target database and active role before executing a script.
- Keep credentials and connection strings outside Git.
- Use the dedicated learning database rather than an unrelated database.
- Inspect affected rows before running an `UPDATE` or `DELETE`.
- Use transactions when experimenting with multi-step data changes.
- Keep the Week 05 in-memory API unchanged during this week.
