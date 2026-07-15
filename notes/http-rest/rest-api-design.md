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

## Request Body Validation

Request body validation means checking the data sent by the client before processing it.

For example, when creating a ticket, the backend should check:
- Is the title provided ? 
- Is the title empty ?
- Is the description provided ?
- Is the priority value valid ? 
- Are the data types correct ?
 
The backend should not trust client input blindly. Invalid request data should return a proper error response, such as 400 Bad Request or 422 Validation Error.
