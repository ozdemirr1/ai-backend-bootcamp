# Weekly Status

## Current Week

Week 05

## Date

10 August - 16 August

## Current Focus

- FastAPI fundamentals
- ASGI and Uvicorn
- Route decorators and HTTP methods
- Path and query parameters
- Pydantic request and response models
- API validation and error responses
- FastAPI endpoint tests
- Current stable dependency versions
- `uv` dependency workflow
- In-memory ticket CRUD API

## Completed

- [x] Week 05 plan created
- [x] FastAPI environment and version audit
- [x] Minimal FastAPI application and health endpoint
- [x] Route, path, and query parameter exercises
- [x] Path and query parameter tests
- [x] Pydantic request schema and body validation exercises
- [x] Explicit response schema exercises
- [x] API input validation tests
- [x] Ticket domain model and invariant tests
- [x] In-memory repository and repository tests
- [x] Ticket service and application-rule tests
- [x] Partial-update request schema and schema tests
- [x] Domain-safe title and priority changes
- [x] Partial-update service workflow and tests
- [ ] API error mapping tests
- [ ] Feature branch and pull request practice
- [ ] Week 05 report

## Problems

- No current blockers.

## Friday Progress - 14 August

- Added `TicketUpdateRequest` with optional title, priority, and status fields.
- Rejected empty updates, all-`None` updates, invalid literals, and extra fields.
- Kept API string literals separate from domain enum values.
- Centralized title normalization and validation in the domain model.
- Added domain methods for safe title and priority changes.
- Added `TicketService.update_ticket()` for partial application updates.
- Verified 9 schema tests, 14 domain model tests, and 17 service tests.

The remaining presentation-layer integration was intentionally moved to
Saturday so it can be completed as one uninterrupted CRUD and endpoint-testing
session.

## Next Tasks

- Review basic FastAPI dependency injection
- Connect the ticket service to the FastAPI routes
- Complete repository-backed create, list, detail, partial-update, and delete routes
- Return intentional HTTP status codes
- Map missing and duplicate tickets to API errors
- Isolate endpoint state between tests
- Complete endpoint tests and documentation
- Run the full quality review and prepare the pull request
