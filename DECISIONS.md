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
