# Request and Response Validation

## Goal

This note explains how FastAPI converts path and query inputs, rejects invalid
values, and represents validation errors. Request body models and explicit
response models will extend this foundation in later exercises.

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

Domain or application validation answers questions such as:

- Is the requested status transition allowed?
- Is the priority supported by the ticket workflow?
- Does the referenced ticket exist?

Keeping these responsibilities separate prevents FastAPI route functions from
becoming the location for every business rule.

## Current Limitations

The current routes return dictionaries with broad dictionary return annotations.
They demonstrate parameter validation, but they do not yet provide:

- Pydantic request body models
- field constraints for ticket data
- explicit response schemas
- repository-backed existence checks
- application error-to-HTTP response mapping

These concerns will be added incrementally after the path and query foundations
are understood and tested.
