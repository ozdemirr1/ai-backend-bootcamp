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
- [x] FastAPI dependency injection and isolated endpoint state
- [x] Repository-backed ticket CRUD routes
- [x] API error mapping tests
- [x] Manual Uvicorn, curl, Swagger UI, and OpenAPI verification
- [x] Full repository quality and public-diff review
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

## Saturday Progress - 15 August

- Added a replaceable `TicketService` dependency for FastAPI routes.
- Added explicit domain-to-response mapping through `TicketResponse`.
- Connected create, list, detail, partial-update, and delete routes to the
  service layer without bypassing repository or domain boundaries.
- Added status filtering and constrained the list limit to values from 1 to
  100.
- Returned `201 Created` for creation and an empty `204 No Content` response
  for deletion.
- Mapped missing tickets to `404 Not Found` and duplicate identifiers to
  `409 Conflict` at the presentation boundary.
- Isolated endpoint state with a fresh repository and service dependency in
  every API test.
- Expanded the endpoint suite to 31 tests covering CRUD behavior, validation,
  filtering, limits, state changes, and error mapping.
- Passed the complete 107-test repository suite together with Ruff formatting,
  lint, lockfile, environment, and package compatibility checks.
- Verified the complete CRUD lifecycle manually through Uvicorn, curl, Swagger
  UI, and the generated OpenAPI schema.

## Next Tasks

- Commit and push the completed CRUD API and documentation.
- Open and review the Week 05 pull request.
