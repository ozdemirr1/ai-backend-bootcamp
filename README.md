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

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

The current application exercises use only the Python standard library. Pytest and Ruff are development tools used for tests and code-quality checks.

## Quality Checks

Run all tests:

```bash
python -m pytest -q
```

Run the linter:

```bash
ruff check .
```

Ruff is configured in `pyproject.toml` for Python 3.9 compatibility.
