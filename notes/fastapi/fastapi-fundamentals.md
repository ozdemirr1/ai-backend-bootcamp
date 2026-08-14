# FastAPI Fundamentals

## Goal

This note explains the roles of FastAPI, ASGI, and Uvicorn, how an HTTP request
reaches a route function, and how FastAPI identifies path and query parameters.

## FastAPI, ASGI, and Uvicorn

FastAPI is the web framework used to define API routes, parse request data,
validate inputs, generate responses, and produce OpenAPI documentation.

ASGI is the interface contract between an asynchronous Python web application
and an application server. It defines how the server and application exchange
request and response events. ASGI is not a server or a framework by itself.

Uvicorn is an ASGI server. It listens on a network address and port, accepts HTTP
connections, translates them into ASGI events, and passes those events to the
FastAPI application.

Their responsibilities can be summarized as:

```text
HTTP client
    |
    v
Uvicorn -------- network and server responsibilities
    |
    v
ASGI ----------- server-application communication contract
    |
    v
FastAPI -------- routing, parsing, validation, and response mapping
    |
    v
Route function - application entry point for one API operation
```

## Request Lifecycle

For a request such as `GET /tickets/42`, the basic lifecycle is:

1. The client sends an HTTP request.
2. Uvicorn accepts the network connection.
3. Uvicorn passes the request to the FastAPI application through ASGI.
4. FastAPI matches the HTTP method and path to a registered route.
5. FastAPI extracts and validates the route parameters.
6. FastAPI calls the route function when validation succeeds.
7. The returned Python value is serialized into an HTTP response.
8. Uvicorn sends the response to the client.

If parameter validation fails, FastAPI returns a validation response before the
route function is called.

## Routes and HTTP Methods

A route is defined by an HTTP method and a path. The path alone does not identify
an API operation.

```text
GET /tickets
GET /tickets/42
POST /tickets
```

These are three different operations. In FastAPI, a decorator registers the
method and path with the application:

```python
@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok"}
```

The decorator registers `read_health` as the handler for `GET /health`. The
function name describes the Python operation, while the decorator defines its
HTTP boundary.

## Path and Query Parameters

A path parameter identifies a specific resource or path segment. It is declared
inside braces in the route path and is required by that route.

```python
@app.get("/tickets/{ticket_id}")
def read_ticket(ticket_id: int) -> dict[str, int]:
    return {"ticket_id": ticket_id}
```

In `GET /tickets/42`, FastAPI extracts `42`, converts it to an integer, and calls
`read_ticket(ticket_id=42)`.

A query parameter modifies a request without changing the resource path. Common
uses include filtering, pagination, sorting, and search.

```python
@app.get("/tickets")
def list_tickets(
    status: str | None = None,
    limit: int = 10,
) -> dict[str, str | int | None]:
    return {"status_filter": status, "limit": limit}
```

The function signature produces these behaviors:

```text
GET /tickets
-> status=None, limit=10

GET /tickets?status=open&limit=5
-> status="open", limit=5
```

Both query parameters may be omitted from the HTTP request, but their Python
contracts differ:

- `status: str | None = None` may contain a string or `None`.
- `limit: int = 10` always receives an integer after validation and uses `10`
  when the client omits it.

`Optional` or `| None` describes a possible value. A default value determines
whether a function argument may be omitted.

## Header and Body Data

Path and query parameters are only two parts of an HTTP request:

| Request part | Typical responsibility | Ticket API example |
| --- | --- | --- |
| Path | Identify a resource | `/tickets/42` |
| Query | Filter or modify retrieval | `?status=open&limit=5` |
| Header | Carry request metadata | `Authorization`, `Accept` |
| Body | Carry a resource representation | JSON used to preview a ticket |

A Pydantic model used as a route parameter is interpreted as a request body:

```python
@app.post("/tickets/preview")
def preview_ticket(ticket: TicketCreateRequest) -> dict[str, str]:
    return {"title": ticket.title, "priority": ticket.priority}
```

FastAPI reads the JSON body, validates it against `TicketCreateRequest`, and
calls the route with a validated model instance. A body validation failure
returns `422 Unprocessable Content` before the route function runs.

## Automatic API Documentation

FastAPI generates an OpenAPI schema from the application routes and type
annotations. Swagger UI is available at `/docs`, and the raw schema is available
at `/openapi.json`.

The documentation identifies whether a parameter belongs to the path or query,
whether it is required, its declared type, and possible validation responses.

## Testing Without Uvicorn

FastAPI's `TestClient` calls the ASGI application inside the test process. It
does not need a manually running Uvicorn server, a TCP port, or an external HTTP
connection.

```python
def test_read_ticket_accepts_integer_id() -> None:
    response = client.get("/tickets/42")

    assert response.status_code == 200
    assert response.json() == {"ticket_id": 42}
```

Uvicorn remains useful for manual browser and `curl` checks. `TestClient` is used
for fast, repeatable automated endpoint tests.

## Project Boundaries

The ticket project separates four responsibilities:

```text
FastAPI route ------ HTTP parsing, schemas, status codes, and error mapping
      |
      v
TicketService ------ application workflows and application-level errors
      |
      v
Repository --------- temporary in-memory persistence operations
      |
      v
Ticket model ------- valid domain state and behavior
```

The domain `Ticket` model rejects invalid identifiers, titles, priorities, and
statuses regardless of whether it is created by an API route, a test, or a
future persistence adapter. `InMemoryTicketRepository` stores valid tickets
without knowing about HTTP. `TicketService` coordinates identifier assignment,
creation, listing, lookup, and deletion while raising application-specific
errors for missing and duplicate tickets. Its partial-update workflow delegates
title, priority, and status changes back to domain methods instead of assigning
fields directly.

The domain model uses one title-normalization function during both initial
construction and later title changes. This prevents creation and update paths
from applying different validity rules. A failed change raises before assignment,
so the ticket keeps its previous valid state.

These layers have focused unit tests but are not connected to the FastAPI routes
yet. For example, `GET /tickets/999` still returns `{"ticket_id": 999}` because
the current route only echoes the validated identifier. The next presentation
layer exercise will call the service and translate its errors into intentional
HTTP responses.
