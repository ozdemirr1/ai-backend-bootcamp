# HTTP Request Parts

## Goal

This note explains the main parts of an HTTP request and reviews `409 Conflict` and `500 Internal Server Error` through backend-style examples.

## Request Method

The HTTP method describes the intended operation.

```http
GET /tickets/1001
```

In this example, `GET` requests ticket data without changing the resource.

Common methods include:

- `GET`: Read a resource.
- `POST`: Create a resource.
- `PATCH`: Partially update a resource.
- `DELETE`: Delete a resource.

## Request Path

The path identifies the requested resource:

```text
/tickets/1001
```

If the backend route is defined as `/tickets/{ticket_id}`, the value `1001` is the `ticket_id` path parameter.

Path parameters usually identify a specific resource:

```http
GET /tickets/1001
```

## Query Parameters

Query parameters add optional instructions such as filtering, sorting, pagination, or including related data.

```http
GET /tickets?priority=high
```

Multiple query parameters are separated with `&`:

```http
GET /tickets?priority=high&status=open
```

Values received from a URL must still be parsed and validated by the backend.

## Request Headers

Headers carry metadata about the request.

```http
Accept: application/json
X-Client-Name: OpsDesk-CLI
```

- `Accept` tells the server which response format the client can process.
- `X-Client-Name` is an example of a custom header.

Authentication tokens and other sensitive header values must not be committed, logged carelessly, or included in public screenshots.

## Sending Requests With `curl`

Send a basic `GET` request:

```bash
curl https://httpbin.org/get
```

Include response headers and the status line:

```bash
curl -i https://httpbin.org/get
```

Send query parameters and custom request headers:

```bash
curl -i \
  -H "Accept: application/json" \
  -H "X-Client-Name: OpsDesk-CLI" \
  "https://httpbin.org/anything/tickets/1001?include_comments=true"
```

- `-i` includes the response status line and headers.
- `-H` adds a request header.
- `\` continues a shell command on the next line.

Public terminal screenshots should not expose tokens, credentials, personal data, or unnecessary network information such as a public IP address.

## `409 Conflict`

`409 Conflict` means that a valid request conflicts with the current state of a resource.

OpsDesk-style examples:

- Registering with an email address that already exists
- Repeating an invalid ticket status transition
- Updating a resource with an outdated version

Example response:

```http
HTTP/2 409
```

A `409` response represents an expected and explainable business conflict.

## `500 Internal Server Error`

`500 Internal Server Error` means that the server encountered an unexpected condition while processing the request.

Examples include:

- An unexpected database failure
- An unhandled programming error
- A failure in an internal dependency

Example response:

```http
HTTP/2 500
```

A `500` response must not expose stack traces, credentials, database details, or internal file paths. Technical details should be recorded in secure application logs, while the client receives a safe and general error message.

## Path Parameters vs Query Parameters

| Part | Main purpose | Example |
|---|---|---|
| Path parameter | Identify a resource | `/tickets/1001` |
| Query parameter | Filter or modify an optional behavior | `/tickets?status=open` |

The backend route definition determines whether a path segment is treated as a named path parameter.
