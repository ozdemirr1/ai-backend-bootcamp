# Week 05 Plan

## Date

10 August - 16 August

## Main Focus

- FastAPI fundamentals
- ASGI and Uvicorn
- Route decorators and HTTP methods
- Path and query parameters
- Pydantic request and response models
- API validation and error responses
- FastAPI endpoint tests
- Current stable dependency versions
- `uv` environment and dependency workflow
- In-memory ticket CRUD API
- Modular API structure

## Why This Week Exists

Month 1 established Python, HTTP, testing, Git, dependency, OOP, and clean-code foundations. Week 05 begins Month 2 by applying those foundations through an HTTP API.

The goal is not to build the complete OpsDesk backend immediately. The goal is to understand FastAPI's request lifecycle, create a small tested API, and preserve the responsibility boundaries learned in Week 04.

The roadmap describes an in-memory Task API. This repository will implement the same Week 05 learning scope with tickets so the exercise remains connected to OpsDesk. The resource name changes, but the required create, list, detail, partial update, and delete behaviors remain the same.

## Version Policy

Use the latest **stable** releases that are mutually compatible when the environment is prepared.

- Verify versions through official project documentation or official package indexes on installation day.
- Do not use alpha, beta, release-candidate, nightly, or preview releases.
- Do not copy outdated versions from tutorials without checking current releases.
- Confirm the supported Python version before upgrading the project interpreter.
- Prefer a current supported Python release instead of remaining on Python 3.9.6 without review.
- Record direct dependencies and their installed versions.
- Use the latest stable compatible `uv` release for the new Month 2 project after verifying its official installation guidance.
- Do not manually list transitive dependencies as project requirements.
- Run the complete test, lint, format, and dependency checks after an environment change.
- If the newest stable packages are incompatible, choose the newest compatible stable combination and document the reason.

This policy means **current and compatible**, not blindly installing every newest package.

## Learning Goals

- Explain what FastAPI provides.
- Explain the roles of ASGI and an ASGI server.
- Create and run a minimal FastAPI application.
- Map HTTP methods and paths to route functions.
- Use path parameters and query parameters.
- Define request bodies with Pydantic models.
- Define explicit response models.
- Understand automatic request validation.
- Distinguish framework validation from domain and application rules.
- Return appropriate HTTP status codes.
- Test endpoints without depending only on manual browser checks.
- Use FastAPI's testing utilities with the compatible HTTPX2 stack.
- Keep API presentation code separate from service and domain responsibilities.

## Daily Plan

### Monday

Environment audit, FastAPI overview, and the first application.

Practice:

- Create the Week 05 feature branch.
- Check the current Python and package-tool versions.
- Verify the latest stable compatible Python and FastAPI stack through official sources.
- Verify and install the latest stable compatible `uv` release.
- Prepare a clean virtual environment if an interpreter upgrade is approved.
- Install only the direct packages needed for this week.
- Record installed versions.
- Explain FastAPI, ASGI, Uvicorn, and the request lifecycle.
- Create a minimal health endpoint.
- Run the application locally and inspect the generated OpenAPI documentation.
- Use the official FastAPI tutorial as the primary framework reference.

### Tuesday

Routes, HTTP methods, path parameters, and query parameters.

Practice:

- Add `GET` endpoints for ticket collection and ticket detail examples.
- Add a typed ticket ID path parameter.
- Add optional query parameters for filtering.
- Compare path, query, header, and body data.
- Inspect successful and invalid requests.
- Add focused endpoint tests.

### Wednesday

Pydantic request models and automatic validation.

Practice:

- Create a ticket request model.
- Add field types and validation constraints.
- Send valid and invalid JSON request bodies.
- Observe FastAPI validation error responses.
- Compare Pydantic input validation with Ticket domain validation.
- Test missing fields, wrong types, and invalid values.

### Thursday

Response models, status codes, and error handling.

Practice:

- Create an explicit ticket response model.
- Add a small ticket creation endpoint.
- Add a partial ticket update endpoint.
- Add a ticket deletion endpoint.
- Return `201 Created` for successful creation.
- Return `204 No Content` for successful deletion.
- Return `404 Not Found` for a missing ticket.
- Return `409 Conflict` for a duplicate ticket ID.
- Use `HTTPException` only at the API boundary.
- Test response bodies, status codes, and content types.

### Friday

Modular API structure and dependency boundaries.

Practice:

- Separate API schemas from domain models where responsibilities differ.
- Keep route functions small.
- Delegate application rules to a service.
- Complete the in-memory create, read, update, and delete flow.
- Review dependency injection concepts in FastAPI without adding premature abstractions.
- Avoid placing repository logic directly in route functions.
- Update notes and project documentation.

### Saturday

Integration, quality review, and pull request.

Practice:

- Run the complete endpoint and repository test suite.
- Run Ruff lint and formatting checks.
- Run the dependency health check.
- Review the full feature branch diff.
- Confirm no secrets or environment-specific paths are committed.
- Open and review the Week 05 pull request.
- Merge only after the API behavior and documentation are verified.

### Sunday

Week 05 report and Week 06 preparation.

Practice:

- Complete `weekly-reports/week-05.md`.
- Review Week 05 interview questions.
- Update repository status and documentation.
- Review FastAPI fundamentals before adding PostgreSQL.
- Prepare the Week 06 database plan without starting it early.

## Architecture Target

```text
HTTP request
     |
     v
FastAPI route --------> HTTP parsing and response mapping
     |
     v
TicketService --------> application rules
     |
     v
TicketRepository -----> temporary in-memory storage
     |
     v
Ticket model ---------> domain data and valid state
```

FastAPI replaces the terminal presentation boundary; it does not replace the service, repository, or domain responsibilities.

## Code To Implement

- Minimal FastAPI application
- Health endpoint
- Ticket list endpoint
- Ticket detail endpoint
- Ticket creation endpoint
- Ticket update endpoint
- Ticket deletion endpoint
- Path and query parameter examples
- Pydantic request schema
- Pydantic partial-update schema
- Pydantic response schema
- API error mapping
- Endpoint tests

## Planned Project Structure

```text
projects/week-05-fastapi-fundamentals/
├── README.md
├── ticket_api/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── repositories.py
│   ├── schemas.py
│   └── services.py
└── tests/
    ├── __init__.py
    ├── test_api.py
    ├── test_models.py
    ├── test_repositories.py
    └── test_services.py
```

This is a target structure. Files should be added only when they have a clear responsibility.

## Notes To Write

- `notes/fastapi/fastapi-fundamentals.md`
- `notes/fastapi/request-response-validation.md`

## Test Goals

- Health endpoint returns a successful JSON response.
- Path parameters are parsed and validated.
- Query parameters are optional and typed.
- Valid request bodies create the expected response.
- Missing and invalid request fields are rejected.
- Missing tickets return `404`.
- Duplicate ticket IDs return `409`.
- Successful creation returns `201`.
- Partial updates change only the supplied fields.
- Successful deletion returns `204` with no response body.
- Tests do not require a manually running server.
- Tests do not depend on execution order or real project data.

## Dependency Goals

Direct runtime dependencies should be limited to the FastAPI application and its server requirements.

Direct development dependencies should include only the tools required for testing and code quality, including the compatible HTTPX2-based endpoint testing stack.

Use `uv` for the new Month 2 environment and dependency workflow after its current stable release and installation instructions are verified. Learn only the commands needed to create the environment, add dependencies, lock versions, sync the environment, and run project commands.

Before recording any version:

1. Check the official release source.
2. Confirm Python compatibility.
3. Install into the active isolated environment.
4. Run `uv pip check`.
5. Run tests, lint, and formatting checks.
6. Record the verified direct versions.

## Git Workflow Goal

Use a dedicated Week 05 feature branch.

Planned branch:

```text
feature/week-05-fastapi-fundamentals
```

Keep environment changes, application code, tests, documentation, and dashboard updates in meaningful commits.

## Expected Commits

- `week-05: prepare FastAPI development environment`
- `week-05: add FastAPI application basics`
- `week-05: add ticket route parameters`
- `week-05: add request and response schemas`
- `week-05: add ticket update and delete endpoints`
- `week-05: add API error handling and tests`
- `week-05: document FastAPI fundamentals`
- `week-05: complete FastAPI fundamentals pull request`
- `week-05: add weekly report`

## Interview Questions

- What problem does FastAPI solve?
- What is ASGI?
- What is the responsibility of Uvicorn?
- What is a route decorator?
- What is the difference between path and query parameters?
- How does FastAPI decide where a function parameter comes from?
- What is a Pydantic model?
- What is the difference between a request model and a domain model?
- What is a response model and why is it useful?
- What happens when request validation fails?
- When are `201`, `404`, `409`, and `422` appropriate?
- When is `204 No Content` appropriate?
- Why should route functions remain small?
- Why should a route call a service instead of a repository directly?
- How can a FastAPI endpoint be tested without running a live server?
- What does OpenAPI provide?
- Why should dependency versions be verified instead of copied from a tutorial?
- What problem does a lockfile solve?

## Definition of Done

Week 05 is complete when:

- The current stable compatible toolchain is verified and documented.
- The FastAPI application runs locally.
- OpenAPI documentation is available.
- Path and query parameters work.
- Request and response schemas are defined.
- Automatic validation behavior can be explained.
- Ticket endpoints return intentional status codes.
- The in-memory API supports create, list, detail, partial update, and delete operations.
- Route functions preserve service and repository boundaries.
- Endpoint tests pass without a manually running server.
- Ruff, formatting, Pytest, and dependency checks pass.
- The feature branch is reviewed and merged through a pull request.
- The Week 05 report is complete.

## Guardrails

- Use latest stable compatible releases, not preview releases.
- Verify current versions through official sources before installation.
- Use `uv` deliberately; do not introduce Poetry or a second dependency manager in parallel.
- Do not add PostgreSQL, SQLAlchemy, Alembic, or authentication during Week 05.
- Do not put all application logic into route functions.
- Do not treat Pydantic schemas as automatic replacements for domain models.
- Do not test only through Swagger UI or a manually running server.
- Do not commit secrets, local environment files, or machine-specific paths.
- Do not create abstractions before a real dependency or rule requires them.
- Keep changes small, tested, documented, and reviewable.
