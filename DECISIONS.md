# Technical Decisions

## Decision 001 - Main Career Direction

I will focus on becoming an AI-assisted Backend / Full-Stack Developer.

## Reason

Instead of learning many technologies at a shallow level, I will build a strong foundation in backend development, database design, API development, AI integration, cloud deployment, and basic frontend skills.

## Main Stack

Python, FastAPI, PostgreSQL, Redis, Docker, React, TypeScript, OpenAI API, RAG, pgvector, GitHub Actions.

## What I Will Avoid

- Random technology switching
- Deep Flutter specialization during this bootcamp
- WordPress/PHP focus
- Game development
- Desktop applications
- Watching courses without building projects

## Decision 002 - Python and Dependency Workflow

The repository uses Python 3.14 and `uv` for Python version, environment, dependency, and lockfile management.

Direct runtime dependencies are declared in `[project.dependencies]`. Development-only tools are declared in `[dependency-groups].dev`. Exact direct and transitive versions are recorded in `uv.lock`.

## Reason

Python 3.9 reached end of life and no longer provides an appropriate baseline for the FastAPI phase of the bootcamp. Python 3.14 is an actively supported stable release.

Using one dependency workflow prevents `requirements-dev.txt`, manually installed packages, and the actual environment from becoming inconsistent. The lockfile makes the verified environment reproducible while `pyproject.toml` keeps direct dependency intent explicit.

## Decision 003 - Local PostgreSQL Workflow

Week 06 uses the current stable PostgreSQL 18 release installed and managed
through Homebrew. SQL is written in version-controlled files, executed through
`psql`, and may be inspected later with pgAdmin as a secondary visual tool.

The local learning environment uses a dedicated `opsdesk_app` login role and an
`opsdesk_dev` database. The application role is not a superuser and its
connection requires SCRAM password authentication. Credentials and connection
URLs remain outside the repository.

## Reason

Using PostgreSQL and `psql` directly makes server, client, role, database,
schema, SQL, and authentication behavior visible before SQLAlchemy and Alembic
introduce another abstraction layer. Homebrew matches the existing macOS tool
workflow and avoids adding Docker before its planned month.

Separating the application role from the cluster administrator applies least
privilege and prevents application code from depending on administrative
access. Repeatable SQL files preserve the database design in Git without
storing machine-specific state or secrets.

## Decision 004 - Synchronous SQLAlchemy Persistence Foundation

The first PostgreSQL integration uses synchronous SQLAlchemy 2 with Psycopg.
Database configuration is loaded from the required `DATABASE_URL` environment
variable through Pydantic Settings. The real `.env` file remains local, while
`.env.example` documents only the connection-string shape and placeholders.

Engine and session construction remain in testable factory functions. Creating
an engine or a session does not itself prove connectivity; an explicit query is
used when a real database connection must be verified. Sessions will later be
created per FastAPI request instead of being shared across requests.

## Reason

The existing FastAPI routes and service workflows are synchronous. Starting
with synchronous persistence keeps the session and transaction lifecycle
visible without introducing async-specific connection and testing concerns at
the same time.

Environment-based configuration prevents credentials from being hardcoded or
tracked. Factory functions avoid reading local configuration during module
import and let unit tests supply safe, synthetic settings without contacting
PostgreSQL. Request-scoped sessions will provide an explicit unit-of-work
boundary and prevent unrelated requests from sharing mutable persistence state.
