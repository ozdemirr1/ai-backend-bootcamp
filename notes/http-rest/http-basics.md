# HTTP Basics

## What is HTTP?

HTTP is the communication protocol between client and server.

## Request

A request is sent by the client to the server.

Common parts:
- Method
- URL
- Headers
- Body

## Response

A response is sent by the server to the client.

Common parts:
- Status code
- Headers
- Body

### Common HTTP Methods

### GET
Used to retrieve data.

### POST
Used to create new data.

### PUT
Used to replace existing data.

### PATCH
Used to partially update existing data.

### DELETE
Used to delete data.

## Common Status Codes

- 200 OK
- 201 Created
- 204 No Content
- 400 Bad Request
- 401 Unauthorized
- 403 Forbiden
- 404 Not found
- 409 Conflict 
- 422 Validation Error
- 500 Internal Server Error

## Interview Questions

### What is the difference between 401 and 403 ? 

401 means the user is not authenticated.
403 means the user is authenticated but does not have permission.

### What is the difference between PUT and PATCH ?

PUT replaces the entire resource.
PATCH updates part of the resource. 

## My Summary 
HTTP is the basic communication system between a client and a server. The client sends a request, and the server returns a response.