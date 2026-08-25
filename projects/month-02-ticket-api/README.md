# Month 02 Ticket API

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
- Typed SQLAlchemy Ticket persistence record
- Explicit persistence-to-domain mapping
- Database identity, default, timestamp, and constraint metadata tests
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

The Week 07 persistence foundation adds the following verified versions:

- SQLAlchemy 2.0.52
- Psycopg 3.3.4
- Alembic 1.19.1
- Pydantic Settings 2.15.0

## Database Configuration Foundation

The application reads its PostgreSQL connection URL from the required
`DATABASE_URL` environment variable. Copy the tracked example locally and
replace every placeholder without committing the resulting file:

```bash
cp .env.example .env
```

The URL uses SQLAlchemy's explicit Psycopg driver name:

```text
postgresql+psycopg://APP_USER:URL_ENCODED_PASSWORD@DB_HOST:5432/APP_DATABASE
```

The real `.env` file is ignored by Git. Passwords containing URL-reserved
characters must be URL-encoded. Do not paste the real URL into source code,
tests, documentation, terminal screenshots, or Git history.

`ticket_api.config` loads and validates settings. `ticket_api.database`
contains testable Engine and Session factory functions. Engine creation is
lazy: a real connection is opened only when a Connection or Session first
executes database work.

## Persistence Mapping Foundation

`ticket_api.persistence_models` defines a typed SQLAlchemy `TicketRecord` that
mirrors the constrained PostgreSQL `tickets` table. The record preserves the
database-generated identity, server defaults, timezone-aware timestamps,
nullability, and named check constraints established during Week 06.

The persistence record remains separate from the domain `Ticket`. Database
priority and status strings cross the boundary through explicit mapper
functions, which convert them to domain enums and apply domain business fields
back to an existing record without overwriting identity or timestamps.

The current application routes still use the in-memory repository. The next
Week 07 steps add Alembic migrations, a PostgreSQL repository, and
request-scoped FastAPI sessions without weakening the existing domain or HTTP
boundaries.

## Run the Application

From the repository root, run:

```bash
uv run uvicorn ticket_api.main:app \
  --app-dir projects/month-02-ticket-api \
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

Run all Month 02 Ticket API tests from the repository root:

```bash
uv run pytest projects/month-02-ticket-api/tests -v
```

Run the complete repository test suite:

```bash
uv run pytest
```
