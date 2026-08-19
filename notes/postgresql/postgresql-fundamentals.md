# PostgreSQL Fundamentals

## Goal

This note records the PostgreSQL concepts and local development workflow used
during Week 06. The objective is to understand the database directly before an
ORM hides SQL statements, connections, and database behavior.

## Core Components

PostgreSQL development involves several separate components:

| Component | Responsibility |
| --- | --- |
| `postgres` | Runs the database server and manages one database cluster. |
| Database cluster | Stores a collection of databases in one data directory. |
| Database | Provides an isolated namespace and ownership boundary inside a cluster. |
| Schema | Groups tables and other database objects inside one database. |
| Table | Stores related rows using a declared column structure. |
| Row | Represents one stored record. |
| Column | Defines one named and typed attribute of every row. |
| `psql` | Connects to a running PostgreSQL server as a client. |

The Week 06 environment currently has this shape:

```text
PostgreSQL 18.6 server
└── opsdesk_dev database
    └── public schema
        └── tickets table
```

The server and client are not the same program. `psql --version` reports the
client version, while `SELECT version();` reports the version of the connected
server.

## Verified Local Environment

The environment was audited and verified on 17 August 2026:

- Apple Silicon (`arm64`) macOS
- Homebrew 6.0.18
- PostgreSQL 18.6
- PostgreSQL 18 data directory: `/opt/homebrew/var/postgresql@18`
- Server address: `localhost`
- Server port: `5432`
- Default locale: `en_US.UTF-8`
- Server time zone: `Europe/Istanbul`
- Data page checksums enabled
- Default password encryption: `scram-sha-256`

PostgreSQL 18.6 was selected because it was the latest stable release verified
through the official PostgreSQL release announcement and Homebrew formula. The
PostgreSQL 19 beta release was intentionally excluded.

Homebrew was retained as the single local installation and service workflow.
Docker was not introduced early merely to start PostgreSQL.

## Local Service Commands

Inspect the Homebrew services:

```bash
brew services list
```

Start PostgreSQL 18 and configure it to restart at login:

```bash
brew services start postgresql@18
```

Stop the service deliberately:

```bash
brew services stop postgresql@18
```

Check whether the server accepts connections:

```bash
pg_isready -h localhost -p 5432
```

PostgreSQL 18 is a versioned, keg-only Homebrew formula. Its binary directory is
placed before older PostgreSQL commands through this shell configuration:

```bash
export PATH="/opt/homebrew/opt/postgresql@18/bin:$PATH"
```

## Roles and Least Privilege

A PostgreSQL role represents an identity and a set of privileges. A role needs
the `LOGIN` attribute to act as a database login.

The local cluster contains two roles with intentionally different purposes:

| Role | Purpose |
| --- | --- |
| `furkan` | Local cluster administrator created during cluster initialization. |
| `opsdesk_app` | Non-superuser application login for the learning database. |

The application role cannot create databases, create roles, use replication,
or bypass the cluster administrator. The application should not connect using
the administrator role.

The dedicated development database is:

```text
database: opsdesk_dev
owner:    opsdesk_app
```

Passwords must not be placed in SQL scripts, shell history, README files, Git,
or screenshots. `psql`'s `\password` command allows a role password to be set
without embedding it in a SQL statement. Environment variables and ignored
local configuration will be introduced when an application connection is
needed.

## Client Authentication

PostgreSQL reads client authentication rules from `pg_hba.conf`. HBA means
host-based authentication. A rule considers the connection type, requested
database, role, client address, and authentication method.

Rules are evaluated from top to bottom. PostgreSQL uses the first matching rule
and does not fall through to a later rule after an authentication failure.

The Homebrew cluster initially used `trust` for all local connections. `trust`
accepts a matching connection without verifying a password. The Week 06 setup
added narrower rules before the general development rules:

```text
# Require SCRAM authentication for the OpsDesk application role.
local   opsdesk_dev   opsdesk_app                           scram-sha-256
host    opsdesk_dev   opsdesk_app   127.0.0.1/32            scram-sha-256
host    opsdesk_dev   opsdesk_app   ::1/128                 scram-sha-256
```

The `scram-sha-256` method performs password authentication without storing the
plain password in PostgreSQL. A TCP connection through `localhost` verified:

```text
Database      opsdesk_dev
Client User   opsdesk_app
Password Used true
Superuser     off
```

The server currently listens only on `localhost`. This is a local learning
environment, not a production security configuration. Broader authentication,
TLS, secret delivery, and deployment rules require a separate production
review.

## Useful `psql` Commands

Connect to the administrative database using the current operating-system
user:

```bash
psql -d postgres
```

Connect to the learning database through TCP as the application role:

```bash
psql -h localhost -U opsdesk_app -d opsdesk_dev -W
```

Useful meta-commands inside `psql`:

| Command | Purpose |
| --- | --- |
| `\conninfo` | Show current connection details. |
| `\du` | List roles and role attributes. |
| `\l` | List databases and owners. |
| `\dn+` | List schemas with ownership and privileges. |
| `\dt` | List visible tables. |
| `\d+ table_name` | Inspect a table, including defaults and constraints. |
| `\connect database role` | Change the database and role. |
| `\p` | Print the current query buffer. |
| `\r` | Clear an unfinished query buffer. |
| `\pset pager off` | Disable paged output for the current session. |
| `\q` | Exit `psql`. |

Backslash meta-commands do not use a semicolon. SQL statements do:

```sql
SELECT current_user, current_database();
```

An interactive prompt ending in `->` indicates that `psql` is still waiting
for the current statement to finish. A prompt ending in `(>` specifically
indicates an unmatched opening parenthesis. `\r` or `Ctrl+C` clears the
unfinished query. When `(END)` is visible, output is open in a pager; `q`
returns to `psql`, while `\q` exits `psql` itself.

## Ticket Table Design

The first repeatable schema script is:

```text
projects/week-06-postgresql-sql/sql/001_schema.sql
```

The core `tickets` table separates client-owned input from server-owned
state:

| Column | Type | Ownership and rule |
| --- | --- | --- |
| `ticket_id` | `BIGINT` identity | Generated by PostgreSQL and used as the primary key. |
| `title` | `TEXT` | Required client input stored without surrounding whitespace. |
| `priority` | `TEXT` | Required client input restricted to supported priority values. |
| `status` | `TEXT` | Server-owned at creation with an `open` default. |
| `created_at` | `TIMESTAMPTZ` | Generated by PostgreSQL when the row is inserted. |
| `updated_at` | `TIMESTAMPTZ` | Initially generated by PostgreSQL and updated explicitly later. |

`GENERATED ALWAYS AS IDENTITY` prevents normal clients from choosing a ticket
identifier. The identity generator supplies server-generated values, while the
primary key enforces uniqueness. The generated sequence is not a gapless row
count. Rejected inserts consumed values `2` through `7`, so the next successful
row received identifier `8` even though the table contained only two rows.

The database protects four named check constraints:

- `tickets_title_format` requires a stored title to equal `btrim(title)` and
  have a length between 3 and 100 characters.
- `tickets_priority_allowed` restricts priority to `low`, `medium`, `high`, or
  `critical`.
- `tickets_status_allowed` restricts status to `open`, `in_progress`,
  `resolved`, or `closed`.
- `tickets_timestamp_order` prevents `updated_at` from preceding `created_at`.

`NOT NULL` does not reject an empty string or whitespace-only text. A check
constraint is therefore needed in addition to `NOT NULL`. A check constraint
validates stored input; it does not normalize or rewrite it.

## Constraint Verification

The schema was executed through the password-authenticated, non-superuser
`opsdesk_app` connection. `\d+ tickets` confirmed the columns, defaults,
primary-key index, not-null rules, and named checks. PostgreSQL's system
catalog exposed the stored definitions directly:

```sql
SELECT
    conname,
    pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'tickets'::regclass
ORDER BY conname;
```

PostgreSQL may display an `IN` check internally as `= ANY (ARRAY[...])` and a
`BETWEEN` check as equivalent lower and upper comparisons. These are normalized
representations of the declared rules, not changes in their behavior.

Intentional invalid inserts verified that the database rejects:

- whitespace-only and non-normalized titles;
- unsupported priority and status values;
- missing required values;
- timestamps in an invalid order; and
- explicit values for the generated identity column.

Only successful inserts remained stored. Defaults and identity values are
evaluated before later constraint checks, while sequence advancement is not
rolled back when an insert fails.

## Seed Data Workflow

`sql/002_seed.sql` provides a deterministic local development dataset. It
clears the existing Ticket rows, resets the identity generator, inserts six
known rows with varied priorities and statuses, and returns the generated
values.

```sql
TRUNCATE TABLE tickets RESTART IDENTITY;
```

`TRUNCATE` is deliberately destructive and belongs only in the dedicated
learning database. The script is executed with both `ON_ERROR_STOP` and
`--single-transaction`. If an insert fails, the transaction prevents the
preceding truncate from leaving the table empty.

A multi-row insert uses one column list followed by comma-separated value
groups. String literals use single quotes. Double quotes identify SQL objects
such as case-sensitive column or table names and do not represent strings.

`RETURNING` exposes database-generated identifiers, defaults, and timestamps
without requiring a separate select. The six seed rows receive identifiers
`1` through `6` after `RESTART IDENTITY`.

## Query and CRUD Fundamentals

`sql/003_crud_queries.sql` records direct SQL exercises. The main query clauses
appear in this written order:

```text
SELECT -> FROM -> WHERE -> ORDER BY -> LIMIT
```

Explicit column lists are preferred to `SELECT *` for application and report
queries. They document the result contract, avoid retrieving unneeded data,
and prevent newly added columns from silently changing the output shape.

`WHERE` filters rows before ordering and limiting the result. `IN` expresses a
set of accepted values. Multiple predicates can be combined with `AND` and
`OR`, but `AND` has higher precedence. Parentheses make the intended business
rule explicit:

```sql
WHERE priority = 'low'
    AND (status = 'resolved' OR status = 'open')
```

Without `ORDER BY`, PostgreSQL does not guarantee row order. A deterministic
query therefore declares its ordering, including a tie-breaker when needed.
`LIMIT` is applied after ordering and should be used with a deliberate order
when the selected subset must be predictable.

Data-changing statements follow a preview-first rule:

1. Run a `SELECT` with the intended predicate.
2. Confirm that only the expected rows are returned.
3. Reuse that scope in `UPDATE` or `DELETE`.
4. Use `RETURNING` to inspect the affected rows.

An `UPDATE` without `WHERE` changes every row, and a `DELETE` without `WHERE`
removes every row. Primary-key predicates provide exact row targeting, while
an additional expected-state predicate can add protection for deletion.

`DEFAULT CURRENT_TIMESTAMP` applies only when a row is inserted. A later
update must set the modification timestamp explicitly:

```sql
SET
    status = 'resolved',
    updated_at = CURRENT_TIMESTAMP
```

The verified update affected one Ticket and advanced only its `updated_at`
value. The verified delete used both identifier and status predicates and
removed one closed Ticket. The final table retained five rows.

## SQL Editing Workflow

Week 06 uses three tools with separate responsibilities:

1. Write repeatable `.sql` files in VS Code.
2. Execute and inspect them through `psql`.
3. Use pgAdmin later as an optional visual inspection and administration tool.

The committed `.sql` files remain the source of truth. Clicking through a GUI
must not replace understanding or recording the SQL operation.

## Current Scope Boundary

Week 06 studies PostgreSQL and SQL directly. The Week 05 FastAPI application
remains in-memory. SQLAlchemy, Alembic, database drivers, API integration, and
authentication features are intentionally deferred to their planned weeks.

## Official References

- [PostgreSQL 18.6 release announcement](https://www.postgresql.org/about/news/postgresql-186-1711-1615-1519-1424-and-19-beta-3-released-3365/)
- [PostgreSQL macOS packages](https://www.postgresql.org/download/macosx/)
- [PostgreSQL 18 `psql` documentation](https://www.postgresql.org/docs/18/app-psql.html)
- [PostgreSQL 18 `pg_hba.conf` documentation](https://www.postgresql.org/docs/18/auth-pg-hba-conf.html)
