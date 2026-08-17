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

## Planned Structure

Files will be added only after their related concepts are understood:

```text
projects/week-06-postgresql-sql/
├── README.md
├── docs/
│   └── ticket-erd.md
└── sql/
    ├── 001_schema.sql
    ├── 002_seed.sql
    ├── 003_crud_queries.sql
    ├── 004_relationship_queries.sql
    └── 005_transactions.sql
```

Each SQL file will have one clear responsibility and will contain no secrets.

## Safety Rules

- Review the target database and active role before executing a script.
- Keep credentials and connection strings outside Git.
- Use the dedicated learning database rather than an unrelated database.
- Inspect affected rows before running an `UPDATE` or `DELETE`.
- Use transactions when experimenting with multi-step data changes.
- Keep the Week 05 in-memory API unchanged during this week.
