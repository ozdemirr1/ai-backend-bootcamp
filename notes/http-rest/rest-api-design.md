# REST API Design

## Resource

A resource is an entity exposed through the API.

Examples : 
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

# Task API Desing

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

In REST API design, endpoints should represent resources, not actions. HTTP methods describe the action. For example, GET /getTickets because GET already means retrieve data.
