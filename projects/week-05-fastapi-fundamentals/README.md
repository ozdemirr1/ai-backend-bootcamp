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
- Strict partial-update request schema
- Explicit ticket response schema
- Request normalization and automatic validation
- Ticket domain model and invariants
- Domain-safe title, priority, and status changes
- In-memory ticket repository
- Ticket application service with complete CRUD workflows
- Dependency-injected FastAPI routes
- Explicit HTTP status and application-error mapping
- Isolated endpoint, schema, domain, repository, and service tests
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

| Method   | Path                   | Success status   | Purpose |
| -------- | ---------------------- | ---------------- | ------- |
| `GET`    | `/health`              | `200 OK`         | Return application health. |
| `GET`    | `/tickets`             | `200 OK`         | List, filter, and limit stored tickets. |
| `POST`   | `/tickets`             | `201 Created`    | Validate and create a ticket. |
| `POST`   | `/tickets/preview`     | `200 OK`         | Validate input without storing it. |
| `GET`    | `/tickets/{ticket_id}` | `200 OK`         | Return one stored ticket. |
| `PATCH`  | `/tickets/{ticket_id}` | `200 OK`         | Partially update a stored ticket. |
| `DELETE` | `/tickets/{ticket_id}` | `204 No Content` | Delete a stored ticket without a body. |

`GET /tickets` accepts two optional query parameters:

- `status`: an optional filter restricted to `open`, `in_progress`, `resolved`,
  or `closed`
- `limit`: an integer from `1` through `100` with a default value of `10`

FastAPI returns `422 Unprocessable Content` before calling the route function
when path, query, or body input does not satisfy its declared contract. For
example, `/tickets/not-a-number` fails path validation,
`/tickets?limit=not-a-number` fails query validation, and an invalid preview
payload fails body validation.

`POST /tickets/preview` validates a JSON body containing `title` and `priority`.
It trims surrounding title whitespace, enforces title length, restricts priority
values, and rejects extra fields. It returns `200 OK` because it previews
validated input without creating or storing a ticket.

`POST /tickets` accepts the same create contract, delegates ticket creation to
the service, and returns the stored representation through `TicketResponse`.
`PATCH /tickets/{ticket_id}` accepts one or more updatable fields. An empty
update is rejected with `422`, while a missing ticket produces `404` after a
valid identifier has reached the service.

The project has separate presentation, API schema, domain model, repository,
and service responsibilities. Routes receive a replaceable `TicketService`
dependency and do not access the repository directly. They convert validated
API strings into domain enums, translate application errors into `404` or `409`
HTTP responses, and map domain tickets into the explicit response schema.

The default application service uses process-local in-memory storage. Data is
lost when the server restarts. Endpoint tests replace that dependency with a
fresh repository and service for every test, so results do not depend on test
order or data left by another test.

The complete CRUD lifecycle was also verified manually on 15 August 2026 with
Uvicorn, curl, Swagger UI, and the generated OpenAPI schema. The checks covered
creation, listing, filtering, limiting, detail lookup, partial update, deletion,
input validation, and missing-resource behavior.

## Run the Tests

Run all Week 05 tests from the repository root:

```bash
uv run pytest projects/week-05-fastapi-fundamentals/tests -v
```

Run the complete repository test suite:

```bash
uv run pytest
```
