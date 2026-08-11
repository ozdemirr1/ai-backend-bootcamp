# Week 05 FastAPI Fundamentals

## Goal

Build a small, tested FastAPI application while learning the request lifecycle,
ASGI, Uvicorn, route handling, validation, and API documentation.

## Current Scope

- Minimal FastAPI application
- Health endpoint
- Ticket collection and detail route examples
- Typed path and query parameters
- Automatic request validation
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

| Method | Path                   | Success status | Response body example                  |
| ------ | ---------------------- | -------------- | -------------------------------------- |
| `GET`  | `/health`              | `200 OK`       | `{"status":"ok"}`                      |
| `GET`  | `/tickets`             | `200 OK`       | `{"status_filter":null,"limit":10}`    |
| `GET`  | `/tickets/{ticket_id}` | `200 OK`       | `{"ticket_id":42}`                     |

`GET /tickets` accepts two optional query parameters:

- `status`: an optional string filter with a default value of `null`
- `limit`: an integer with a default value of `10`

FastAPI returns `422 Unprocessable Content` before calling the route function
when a path or query value cannot be converted to its declared type. For
example, `/tickets/not-a-number` fails path validation and
`/tickets?limit=not-a-number` fails query validation.

The ticket routes currently demonstrate parameter parsing and validation. They
do not access a repository or determine whether a ticket exists yet.

## Run the Tests

Run the Week 05 endpoint tests from the repository root:

```bash
uv run pytest projects/week-05-fastapi-fundamentals/tests -v
```

Run the complete repository test suite:

```bash
uv run pytest
```
