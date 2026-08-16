# Week 05 Report

## Date

10 August - 16 August 2026

## Main Focus

- Python and dependency workflow modernization with `uv`
- FastAPI, ASGI, and Uvicorn responsibilities
- Route decorators and HTTP methods
- Path, query, and request-body parameters
- Pydantic request, update, and response schemas
- Input validation and normalization
- Domain, repository, service, and presentation boundaries
- In-memory Ticket CRUD API
- Dependency injection and endpoint test isolation
- HTTP status and application-error mapping
- OpenAPI, Swagger UI, curl, and automated endpoint verification
- Feature branch and pull request workflow

## What I Completed

- [x] Migrated the project from a manual virtual-environment workflow to `uv`
- [x] Pinned Python 3.14.7 in `.python-version`
- [x] Recorded direct dependencies in `pyproject.toml`
- [x] Added a reproducible `uv.lock`
- [x] Separated runtime and development dependency groups
- [x] Created the Week 05 FastAPI application
- [x] Added and manually verified `GET /health`
- [x] Practiced typed path and query parameters
- [x] Added strict create, partial-update, and response schemas
- [x] Added title normalization and length validation
- [x] Rejected missing, invalid, and extra request fields
- [x] Added a validated Ticket domain model with controlled state changes
- [x] Added an in-memory ticket repository
- [x] Added a ticket application service
- [x] Connected FastAPI routes to the service through dependency injection
- [x] Implemented create, list, detail, partial-update, and delete endpoints
- [x] Added status filtering and constrained list limits
- [x] Returned intentional `201`, `200`, `204`, `404`, `409`, and `422` results
- [x] Added an explicit domain-to-response mapping function
- [x] Isolated endpoint state with a fresh repository and service per test
- [x] Verified CRUD behavior through TestClient, curl, Swagger UI, and OpenAPI
- [x] Passed the complete 107-test repository suite
- [x] Reviewed and merged pull request #3
- [x] Cleaned local and remote feature branches after the merge

## What I Learned

- FastAPI is responsible for route registration, HTTP input parsing, validation,
  response serialization, and OpenAPI generation.
- Uvicorn is the ASGI server that accepts network connections and passes request
  events to the Python application.
- ASGI is the interface contract between an asynchronous Python web application
  and its server; it is not a framework or a server by itself.
- A route decorator connects an HTTP method and path to a Python handler.
- A parameter name present in a route path is treated as a path parameter.
- A simple typed parameter that is not part of the path is normally interpreted
  as a query parameter.
- A route parameter typed as a Pydantic model is interpreted as a request body.
- A type that includes `None` describes an allowed value, while a default value
  controls whether the client may omit the parameter.
- FastAPI rejects input that cannot satisfy the declared HTTP contract before
  the route handler and service are called.
- A valid path identifier can still refer to a missing resource, which requires
  an application lookup and a deliberate `404` response.
- Validation rejects data that violates a contract, while normalization converts
  accepted data into a consistent representation.
- Request schemas, domain models, and response schemas protect different
  boundaries and should not replace one another.
- `TicketCreateRequest` accepts only client-owned creation fields.
- The domain `Ticket` model protects valid state regardless of whether the object
  is created through an API, a test, or a future persistence adapter.
- `TicketResponse` defines and validates the public response representation.
- A partial-update schema needs optional fields but must still reject an update
  that contains no actual change.
- A partial update must preserve every field that the client did not supply.
- API literals represent JSON strings, while domain enums protect internal state.
- Conversion from API strings to domain enums belongs at the presentation
  boundary.
- A route should call the service instead of bypassing application rules through
  direct repository access.
- The service coordinates application workflows, the repository manages
  storage, and the domain model owns object invariants.
- Application exceptions should remain independent of FastAPI until a route
  translates them into HTTP responses.
- `201 Created` communicates successful resource creation.
- `204 No Content` is an explicit successful response contract with no body.
- `404 Not Found` represents a structurally valid request for a missing resource.
- `409 Conflict` represents an operation that conflicts with current state.
- `422` represents input that cannot satisfy the declared request contract.
- FastAPI dependency injection separates route behavior from dependency
  construction and allows dependencies to be replaced during tests.
- Constructing a new in-memory repository inside every request would reset state
  and make created tickets disappear from later requests.
- TestClient communicates with the application through ASGI and does not require
  a manually running Uvicorn process or TCP port.
- A fresh repository and service per endpoint test prevent test-order coupling
  and unexpected identifier changes.
- OpenAPI is a machine-readable API contract, while Swagger UI renders that
  contract as an interactive interface.
- `pyproject.toml` records direct dependency intent and compatible ranges.
- `uv.lock` records the exact resolved direct and transitive dependency set.
- `uv lock --check`, `uv sync --check`, and `uv pip check` answer different
  dependency-health questions.
- Runtime dependencies are required to run the application, while development
  dependencies support testing and code quality.

## Architecture I Built

```text
HTTP client
    |
    v
Uvicorn and ASGI
    |
    v
FastAPI route --------> request parsing, schema conversion, HTTP mapping
    |
    v
TicketService --------> application workflows and application errors
    |
    v
TicketRepository -----> temporary in-memory storage
    |
    v
Ticket model ---------> valid domain state and controlled behavior
```

FastAPI is the presentation boundary. It does not replace the domain,
repository, or service layers built during Week 04. The application composes a
repository and service once, exposes the service through a replaceable FastAPI
dependency, and keeps route handlers focused on HTTP concerns.

## API I Built

| Method | Path | Success result | Responsibility |
| --- | --- | --- | --- |
| `GET` | `/health` | `200 OK` | Report application health |
| `POST` | `/tickets` | `201 Created` | Validate and create a ticket |
| `GET` | `/tickets` | `200 OK` | List, filter, and limit tickets |
| `GET` | `/tickets/{ticket_id}` | `200 OK` | Return one ticket |
| `PATCH` | `/tickets/{ticket_id}` | `200 OK` | Partially update one ticket |
| `DELETE` | `/tickets/{ticket_id}` | `204 No Content` | Delete one ticket without a body |
| `POST` | `/tickets/preview` | `200 OK` | Validate input without persistence |

The list endpoint accepts an optional controlled status value and a limit from
1 through 100. Create and update requests reject extra fields. Missing tickets
produce `404`, duplicate identifiers produce `409`, and framework input
validation produces `422`.

## Code and Documentation I Added

### Environment and Dependencies

- `.python-version` with Python 3.14.7
- `pyproject.toml` project metadata and dependency groups
- `uv.lock` with the resolved dependency graph
- Updated root setup and quality-check instructions
- A documented dependency-workflow decision

### FastAPI Presentation Layer

- Application composition root
- Health endpoint
- CRUD route declarations
- Typed path and query parameters
- Constrained query limits
- Status filtering
- Request and response models
- Domain-to-response mapping
- Service dependency provider and annotated alias
- Application-exception to HTTP-exception conversion
- Empty `204 No Content` response handling

### API Schemas

- `TicketCreateRequest`
- `TicketUpdateRequest`
- `TicketResponse`
- Controlled external priority and status literals
- Shared normalized title contract
- Strict extra-field rejection
- Model-level partial-update validation

### Domain, Repository, and Service

- Ticket priority and status enums
- Positive ticket identifier protection
- Reusable title normalization and validation
- Controlled title, priority, and status changes
- In-memory add, lookup, list, and delete operations
- Sequential identifier assignment
- Create, list, detail, update, and delete application workflows
- Missing-ticket and duplicate-ticket application errors

### Tests

- 31 endpoint tests
- 14 domain-model tests
- 8 repository tests
- 9 API-schema tests
- 17 service tests
- Existing 28 Month 1 regression tests
- 107 passing tests in the complete repository suite

### Documentation

- FastAPI, ASGI, Uvicorn, and request-lifecycle notes
- Path, query, header, and body parameter explanations
- Validation-error structure and stable test assertions
- Request, update, domain, and response model boundaries
- Validation versus normalization
- HTTP status and application-error mapping
- Dependency injection and endpoint-state isolation
- Project setup, endpoint, test, and manual-verification instructions

## Problems I Faced

- The Month 1 environment used an unsupported Python baseline for the new
  FastAPI phase and needed a deliberate migration.
- Ruff formatting found older files that were lint-clean but not format-clean.
- The first endpoint test stack produced a deprecation warning because the
  installed FastAPI/Starlette version had moved to HTTPX2 compatibility.
- The generic package name `app` collided with an older learning module during
  full-suite test collection.
- Ruff repeatedly exposed import-order mistakes while new modules were added.
- A malformed function signature made `limit` appear undefined during the first
  query-parameter exercise.
- Early tests contained misspelled JSON keys and incorrect expected status codes.
- A title with only spaces initially passed length validation before whitespace
  normalization was added.
- A model test expected punctuation that the domain model was never designed to
  add.
- A repository exception test called the `pytest` module instead of
  `pytest.raises()`.
- The initial response mapper referenced class attributes instead of the actual
  Ticket instance.
- Endpoint tests initially shared one global client and application state.
- Some tests received the fixture function definition instead of a TestClient
  because they did not request the `client` fixture parameter.
- The first route examples only echoed parameters and returned `200` for valid
  but missing identifiers.
- Empty partial-update bodies needed cross-field validation rather than a
  single-field constraint.

## How I Solved Them

- I verified stable compatible versions before changing the interpreter and
  dependency workflow.
- I separated the mechanical Ruff formatting cleanup into its own commit and
  reran the complete regression suite.
- I replaced the deprecated endpoint-test dependency with the compatible HTTPX2
  stack and regenerated the lockfile.
- I renamed the FastAPI package to `ticket_api` to prevent import collisions.
- I used Ruff's exact import-order guidance and rechecked the complete project.
- I corrected route signatures by separating parameters with commas and
  formatting them before testing.
- I compared failing test inputs and expected results with the declared API
  contract instead of changing production behavior to match test typos.
- I normalized title whitespace before enforcing length limits.
- I corrected test expectations to protect intended behavior rather than an
  accidental string difference.
- I used `pytest.raises()` to assert expected exceptions.
- I mapped values from the Ticket instance and converted domain enums through
  their `.value` properties.
- I added a yielding TestClient fixture with a fresh repository and service for
  every test.
- I requested the `client` fixture explicitly in each endpoint test.
- I connected the routes to the service and translated application errors at the
  HTTP boundary.
- I added a Pydantic model-level validator requiring at least one actual update
  value.

## Quality Results

- Python: 3.14.7
- uv: 0.12.3
- FastAPI: 0.141.1
- Uvicorn: 0.52.1
- Pydantic: 2.13.4
- HTTPX2: 2.10.0
- Pytest: 9.1.1
- Ruff: 0.16.2
- Complete Pytest suite: 107 passed
- Week 05 endpoint suite: 31 passed
- Ruff lint: all checks passed
- Ruff format: 67 files already formatted
- Lockfile check: passed
- Environment synchronization check: passed
- Installed-package compatibility check: passed
- Git whitespace check: passed
- Manual CRUD lifecycle: passed through Uvicorn and curl
- Swagger UI and OpenAPI schema: verified

## GitHub Outputs

- Feature branch: `feature/week-05-fastapi-fundamentals`
- Feature commits merged through the pull request: 8
- Pull requests opened and merged: 1
- Pull request number: #3
- Pull request title: `week-05: complete FastAPI fundamentals and ticket CRUD API`
- Files changed in the pull request: 31
- Pull request merge commit: `b02c983`
- Final feature commit: `bf9ad69`
- Local and remote feature branches: deleted after merge
- Final branch state: clean `main` synchronized with `origin/main`

## Interview Questions I Can Answer

- What problem does FastAPI solve?
- What are the separate responsibilities of Uvicorn, ASGI, and FastAPI?
- What is a route decorator?
- How does FastAPI identify path, query, and request-body parameters?
- Why does invalid typed input return `422` before the route runs?
- What is the difference between `422` and `404`?
- What is the difference between validation and normalization?
- Why are request, domain, update, and response models separate?
- Why does a partial update change only supplied fields?
- Why must a domain model protect invariants independently of Pydantic?
- Why should a route call a service instead of a repository directly?
- Which responsibilities belong to routes, services, repositories, and domain
  models?
- When are `201`, `204`, `404`, `409`, and `422` appropriate?
- Why must a successful `204` response have an empty body?
- What does FastAPI dependency injection provide?
- Why should dependencies be replaceable during endpoint tests?
- How does TestClient test an endpoint without Uvicorn?
- Why does every endpoint test need isolated in-memory state?
- What does a response model protect?
- What is the difference between OpenAPI and Swagger UI?
- What is the difference between `pyproject.toml` and `uv.lock`?
- What do `uv lock --check`, `uv sync --check`, and `uv pip check` verify?
- What is the difference between runtime and development dependencies?
- Why should dependency versions be stable and mutually compatible?

## Known Limitations

- Ticket data exists only in one application process and disappears on restart.
- Multiple application workers would not share the same in-memory state.
- The API does not use PostgreSQL yet.
- SQLAlchemy and Alembic are intentionally deferred to Week 07.
- Authentication and authorization are intentionally deferred to Week 08.
- Error bodies still use framework-default structures rather than one custom
  application-wide error schema.
- Error response schemas are not yet declared as additional OpenAPI metadata.
- GitHub Actions has not been added, so pull requests do not yet show automated
  checks on GitHub.
- Coverage percentage and static type checking are not yet part of the required
  quality gate.

## Next Week

Week 06 will focus on PostgreSQL and SQL fundamentals without introducing an ORM
early. The Ticket API domain will be used to practice:

- relational tables, rows, columns, and constraints
- primary and foreign keys
- one-to-many and many-to-many relationships
- `SELECT`, `INSERT`, `UPDATE`, and `DELETE`
- filtering, ordering, grouping, and joins
- indexes and their tradeoffs
- transactions, commit, and rollback
- a Ticket database schema, SQL script, and ERD

The goal is to understand the database directly before SQLAlchemy and Alembic
are introduced in Week 07.
