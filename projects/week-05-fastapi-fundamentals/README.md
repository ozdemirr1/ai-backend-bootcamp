# Week 05 FastAPI Fundamentals

## Goal

Build a small, tested FastAPI application while learning the request lifecycle,
ASGI, Uvicorn, route handling, validation, and API documentation.

## Current Scope

- Minimal FastAPI application
- Health endpoint
- Ticket collection and detail route examples
- Typed path and query parameters
- Pydantic request body schema
- Request normalization and automatic validation
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
| `POST` | `/tickets/preview`     | `200 OK`       | `{"title":"VPN fails","priority":"high"}` |
| `GET`  | `/tickets/{ticket_id}` | `200 OK`       | `{"ticket_id":42}`                     |

`GET /tickets` accepts two optional query parameters:

- `status`: an optional string filter with a default value of `null`
- `limit`: an integer with a default value of `10`

FastAPI returns `422 Unprocessable Content` before calling the route function
when path, query, or body input does not satisfy its declared contract. For
example, `/tickets/not-a-number` fails path validation,
`/tickets?limit=not-a-number` fails query validation, and an invalid preview
payload fails body validation.

`POST /tickets/preview` validates a JSON body containing `title` and `priority`.
It trims surrounding title whitespace, enforces title length, restricts priority
values, and rejects extra fields. It returns `200 OK` because it previews
validated input without creating or storing a ticket.

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
