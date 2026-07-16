# OpsDesk Ticket API Design

## Goal

This note describes the first REST API design draft for the OpsDesk ticket system.

## Resource

Main resource:

- tickets

Related resources:

- users
- organizations
- comments
- status

## Ticket Fields

- id
- title
- description
- status
- priority
- category
- organization_id
- created_by_user_id
- assigned_to_user_id
- created_at
- updated_at

## Ticket Endpoints

### List Tickets

GET /tickets

Expected status codes:
- 200 OK
- 401 Unauthorized

### Get Ticket Detail

GET /tickets/{ticket_id}

Expected status codes:
- 200 OK
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found

### Create Ticket

POST /tickets

Expected status codes:
- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 422 Validation Error

### Update Ticket

PATCH /tickets/{ticket_id}

Expected status codes:
- 200 OK
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 422 Validation Error

### Delete Ticket

DELETE /tickets/{ticket_id}

Expected status codes:
- 204 No Content
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found

### Add Comment To Ticket

POST /tickets/{ticket_id}/comments

Expected status codes:
- 201 Created
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 422 Validation Error

### Update Ticket Status

PATCH /tickets/{ticket_id}/status

Expected status codes:
- 200 OK
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 422 Validation Error

## My Notes

In REST API design, endpoints should represent resources. HTTP methods describe the action. Ticket access should be protected because tickets may contain private organization data.