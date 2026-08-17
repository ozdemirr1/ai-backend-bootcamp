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
        └── tables will be introduced after their design is understood
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
| `\connect database role` | Change the database and role. |
| `\r` | Clear an unfinished query buffer. |
| `\q` | Exit `psql`. |

Backslash meta-commands do not use a semicolon. SQL statements do:

```sql
SELECT current_user, current_database();
```

An interactive prompt ending in `-#` or `->` indicates that `psql` is still
waiting for the current statement to finish. `\r` clears the unfinished query.

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
