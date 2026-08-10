# Week 05 FastAPI Fundamentals

## Goal

Build a small, tested FastAPI application while learning the request lifecycle,
ASGI, Uvicorn, route handling, validation, and API documentation.

## Current Scope

- Minimal FastAPI application
- Health endpoint
- Automatic OpenAPI schema and Swagger UI
- Endpoint testing without a manually running server

## Verified Environment

The following stable versions were verified on 10 August 2026:

- Python 3.14.7
- uv 0.12.3
- FastAPI 0.141.1
- Uvicorn 0.52.1
- Pydantic 2.13.4
- HTTPX2 2.10.0
- Pytest 9.1.1
- Ruff 0.16.2

## Run the Application

From the repository root, run:

```bash
uv run uvicorn ticket_api.main:app \
  --app-dir projects/week-05-fastapi-fundamentals \
  --reload
```

The application is available at `http://127.0.0.1:8000`. Swagger UI is
available at `http://127.0.0.1:8000/docs`.

## Available Endpoints

| Method | Path      | Success status | Response body     |
| ------ | --------- | -------------- | ----------------- |
| `GET`  | `/health` | `200 OK`       | `{"status":"ok"}` |

## Run the Tests

Run the Week 05 endpoint tests from the repository root:

```bash
uv run pytest projects/week-05-fastapi-fundamentals/tests -v
```

Run the complete repository test suite:

```bash
uv run pytest
```
