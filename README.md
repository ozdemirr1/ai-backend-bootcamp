# AI Backend / Full-Stack Bootcamp

This repository tracks my 12-month learning journey to become an AI-assisted Backend / Full-Stack Developer.

## Goal

My goal is to become a job-ready AI-assisted Backend / Full-Stack Developer by building real-world projects with backend, database, cloud, AI integration, and frontend skills.

## Main Stack

- Python
- FastAPI
- PostgreSQL
- Redis
- Docker
- React
- TypeScript
- OpenAI API
- RAG
- pgvector
- GitHub Actions

## Main Projects

1. OpsDesk - AI-powered support ticket management system
2. DocuMind - RAG-based document intelligence platform
3. HireMatch AI - CV and job matching assistant

The product repositories will be created when their implementation phases
begin. This repository remains the learning log and evidence base.

## Current Learning Modules

- [Month 02 Ticket API](projects/month-02-ticket-api/README.md) - the completed
  Weeks 05-08 learning application covering FastAPI, PostgreSQL, SQLAlchemy,
  Alembic, authentication, and authorization
- [Week 06 PostgreSQL and SQL](projects/week-06-postgresql-sql/README.md) - a
  bounded SQL laboratory with schema, relationship, query, transaction, and
  index exercises

## Current Weekly Evidence

- [Week 08 Report](weekly-reports/week-08.md) - Argon2id, JWT, persisted User
  identity, Ticket ownership, and authorization
- [Month 02 Report](monthly-reports/month-02.md) - the complete progression
  from FastAPI fundamentals to a PostgreSQL-backed secured API
- [Week 09 Plan](weekly-reports/week-09-plan.md) - OpsDesk requirements,
  organization-scoped domain design, ERD, access rules, and issue planning

The real OpsDesk product begins in Week 09 in a separate public repository.
This repository continues to hold the learning evidence and roadmap history.

## Learning Rule

I will not jump between random technologies.  
I will focus on backend, full-stack fundamentals, AI integration, and production-ready project development.

## Development Setup

Install `uv` by following the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

The repository pins its development Python version in `.python-version` and stores the exact dependency resolution in `uv.lock`.

Create or synchronize the project environment:

```bash
uv sync
```

Project commands can be run through `uv run` without manually activating the virtual environment.

Runtime dependencies are declared in `[project.dependencies]`. Test and code-quality tools are declared in `[dependency-groups].dev`.

## Quality Checks

Verify that the lockfile and environment are synchronized:

```bash
uv sync --check
uv lock --check
```

Run all tests:

```bash
uv run pytest -q
```

Run lint and formatting checks:

```bash
uv run ruff check .
uv run ruff format --check .
```

Check the installed dependency set:

```bash
uv pip check
```
