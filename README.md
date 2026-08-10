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
