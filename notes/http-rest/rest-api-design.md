# REST API Design

## Resource

A resource is an entity exposed through the API.

Examples:
- users
- tickets
- comments
- documents
- tasks

## Good Endpoint Examples

GET /tickets
GET /tickets/{ticket_id}
POST /tickets
PATCH /tickets/{ticket_id}
DELETE /tickets/{ticket_id}

## Bad Endpoint Examples

GET /getTickets
POST /createTicket
POST /deleteTicket

## Rules

- Use nouns, not verbs.
- Use plural resource names.
- Use proper HTTP methods.
- Return meaningful status codes.
- Validate request body.
- Protect private resources with authentication.

## Example Ticket API

GET /tickets
POST /tickets
GET /tickets/{ticket_id}
PATCH /tickets/{ticket_id}
POST /tickets/{ticket_id}/comments
PATCH /tickets/{ticket_id}/status

## Task API Design

## Endpoints

GET /tasks
GET /tasks/{task_id}
POST /tasks
PATCH /tasks/{task_id}
DELETE /tasks/{task_id}


## Task Fields

- id
- title
- description
- status
- created_at
- updated_at

## My REST Summary

In REST API design, endpoints should represent resources, not actions. HTTP methods describe the action. For example, GET /tickets is better than GET /getTickets because GET already means retrieve data.

## Request Body Validation

Request body validation means checking the data sent by the client before processing it.

For example, when creating a ticket, the backend should check:
- Is the title provided?
- Is the title empty?
- Is the description provided?
- Is the priority value valid?
- Are the data types correct?
 
The backend should not trust client input blindly. Invalid request data should return a proper error response, such as 400 Bad Request or 422 Validation Error.


## Status Code Selection

Status codes describe the result of an HTTP response.

### 200 OK
Used when a request succeeds and returns data.

Example:
GET /tickets

### 201 Created
Used when a new resource is created successfully.

Example:
POST /tickets

### 204 No Content
Used when a request succeeds but does not return a response body.

Example:
DELETE /tickets/{ticket_id}

### 400 Bad Request
Used when the request is invalid or malformed.

Example:
The request body is not valid JSON.

### 401 Unauthorized
Used when the user is not authenticated.

Example:
The request does not include a valid token.

### 403 Forbidden
Used when the user is authenticated but does not have permission.

Example:
A normal user tries to access an admin-only endpoint.

### 404 Not Found
Used when the requested resource does not exist.

Example:
GET /tickets/999 when ticket 999 does not exist.

### 409 Conflict
Used when the request conflicts with the current state of the resource.

Example:
Trying to register with an email address that already exists.

### 422 Validation Error
Used when the request body is syntactically valid but fails validation rules.

Example:
The title field is empty or priority has an invalid value.

### 500 Internal Server Error
Used when an unexpected server-side error occurs.

Example:
Unhandled exception or database failure.
