# Request and Response Validation

## Goal

This note explains how FastAPI converts path, query, and body inputs, rejects
invalid values, represents validation errors, and uses explicit schemas to
describe external response contracts.

## Type Conversion

Values received through an HTTP path or query string begin as textual input.
FastAPI uses the route function's type annotations to parse them into Python
values.

```python
@app.get("/tickets/{ticket_id}")
def read_ticket(ticket_id: int) -> dict[str, int]:
    return {"ticket_id": ticket_id}
```

For `GET /tickets/42`, FastAPI converts the path text `"42"` into the integer
`42` before calling `read_ticket`.

The same conversion applies to query parameters:

```python
@app.get("/tickets")
def list_tickets(limit: int = 10) -> dict[str, int]:
    return {"limit": limit}
```

`GET /tickets?limit=5` calls the function with `limit=5`, while omitting the
query parameter uses the default integer value `10`.

## Type Hints and Runtime Validation

Normal Python type hints are not enforced automatically when a function is
called directly. FastAPI reads the annotations at the HTTP boundary and uses
them for runtime parsing and validation.

This distinction means the annotation has two roles in a FastAPI route:

- It documents the Python value expected by the function.
- It contributes to request validation and generated OpenAPI documentation.

## Automatic Validation

When a value cannot be converted to its declared type, FastAPI rejects the
request before calling the route function.

```text
GET /tickets/not-a-number
-> ticket_id cannot be parsed as int
-> route function is not called
-> 422 Unprocessable Content
```

The same behavior applies to an invalid typed query parameter:

```text
GET /tickets?limit=not-a-number
-> limit cannot be parsed as int
-> route function is not called
-> 422 Unprocessable Content
```

This protects application code from receiving a value that failed the declared
HTTP input contract.

## Validation Error Structure

FastAPI returns structured JSON describing one or more validation errors:

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["query", "limit"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "not-a-number"
    }
  ]
}
```

The fields communicate different information:

- `type` identifies the validation failure category.
- `loc` identifies the request part and field containing the error.
- `msg` provides a human-readable explanation.
- `input` contains the rejected value.

`detail` is a list because one request can contain multiple validation errors.

The location distinguishes path and query failures:

```json
["path", "ticket_id"]
["query", "limit"]
```

## Testing Validation Errors

Endpoint tests should verify stable parts of the error contract without relying
on every word of a framework-generated message.

```python
def test_list_tickets_rejects_non_integer_limit() -> None:
    response = client.get("/tickets?limit=not-a-number")

    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["query", "limit"]
    assert error["type"] == "int_parsing"
```

The exact English `msg` text may change between compatible framework versions.
The error location and category express the behavior the API test needs to
protect.

## Pydantic Request Body Models

A route parameter typed as a Pydantic model is interpreted as a JSON request
body:

```python
class TicketCreateRequest(BaseModel):
    title: TicketTitle
    priority: Literal["low", "medium", "high", "critical"]


@app.post("/tickets/preview")
def preview_ticket(ticket: TicketCreateRequest) -> dict[str, str]:
    return {"title": ticket.title, "priority": ticket.priority}
```

Both model fields are required because neither has a default value. FastAPI
parses the JSON body, validates it through Pydantic, and passes a
`TicketCreateRequest` instance to the route.

The create request intentionally excludes `ticket_id` and `status`. A future
creation workflow will assign the identifier and initial status on the server.

## Validation and Normalization

Validation checks whether input satisfies a contract and rejects input that
does not. Normalization converts accepted input into a consistent form.

```python
TicketTitle = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=3,
        max_length=100,
    ),
]
```

- `strip_whitespace=True` normalizes leading and trailing whitespace.
- `min_length=3` and `max_length=100` validate the normalized length.

As a result, `"  VPN connection fails  "` becomes `"VPN connection fails"`,
while a whitespace-only title becomes empty after normalization and fails the
minimum-length constraint.

## Extra Fields

Pydantic ignores fields that are not declared on a model by default. A strict
API input contract can reject them instead:

```python
class TicketCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
```

This prevents clients from silently sending misspelled fields or server-owned
fields such as `status`. The validation error uses the `extra_forbidden` type.

## 422 Versus 404

`422 Unprocessable Content` and `404 Not Found` represent different failures.

- `422` means the request input does not satisfy the declared input contract.
- `404` means the request is structurally valid, but the requested resource does
  not exist.

For example, `/tickets/not-a-number` cannot provide a valid integer ticket ID,
so FastAPI returns `422` before any resource lookup.

By contrast, `/tickets/999` contains a valid integer. Determining whether ticket
`999` exists requires a repository lookup. The current example does not perform
that lookup, so it returns `200 OK` with `{"ticket_id": 999}`.

The future responsibility flow will be:

```text
FastAPI route ------ parse input and map HTTP responses
      |
      v
TicketService ------ decide how a missing ticket affects the operation
      |
      v
TicketRepository --- look up the ticket in storage
```

The repository should not create HTTP responses. HTTP-specific `404` mapping
belongs at the API presentation boundary.

## Framework and Domain Validation

Framework validation answers questions such as:

- Can `ticket_id` be parsed as an integer?
- Can `limit` be parsed as an integer?
- Is a required HTTP field present?
- Does a title satisfy the API length constraints?
- Is a priority one of the accepted external values?

Domain or application validation answers questions such as:

- Is the requested status transition allowed?
- Is the priority supported by the ticket workflow?
- Does the referenced ticket exist?

Keeping these responsibilities separate prevents FastAPI route functions from
becoming the location for every business rule.

## Explicit Response Models

Request and response schemas protect different directions at the HTTP boundary.
A request schema describes data accepted from a client. A response schema
describes data the API promises to return.

```python
class TicketResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_id: int = Field(gt=0)
    title: TicketTitle
    priority: TicketPriority
    status: TicketStatus
```

This schema makes the intended public ticket representation explicit. It also
keeps the API contract separate from the mutable domain `Ticket` object. The
domain model owns internal validity and behavior, while the response model owns
serialization constraints at the presentation boundary.

Defining the schema alone does not apply it to an endpoint. A route must declare
it as its response model when the repository-backed API operations are wired to
the service.

## Current Limitations

The current routes return dictionaries with broad dictionary return annotations.
The explicit ticket response schema and internal domain, repository, and service
layers now exist, but the routes do not yet provide:

- response-model enforcement on ticket endpoints
- repository-backed existence checks
- application error-to-HTTP response mapping
- partial-update request handling

These concerns will be added when the presentation layer is connected to the
tested service workflow.
