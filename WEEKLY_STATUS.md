# Weekly Status

## Current Week

Week 09

## Date

7 September - 13 September 2026

## Current Focus

- Separate OpsDesk product repository
- Product requirements and explicit non-goals
- User, Organization, OrganizationMembership, Ticket, Comment, and Attachment
- Organization-scoped owner, admin, agent, and customer roles
- Ticket participant and lifecycle terminology
- Relational ERD
- Authorization and status-transition matrices
- Initial API endpoint inventory
- Prioritized GitHub issue list

## Completed

- [x] Week 06 PostgreSQL 18.6 learning environment
- [x] Dedicated non-superuser application role and development database
- [x] SCRAM-authenticated local application connection
- [x] Constrained four-table Ticket relational schema
- [x] One-to-many and many-to-many relationships
- [x] Deterministic development seed data
- [x] CRUD, join, aggregation, transaction, and index exercises
- [x] Mermaid Ticket ERD and PostgreSQL notes
- [x] Clean-database reconstruction and verification
- [x] Ruff checks and 107 repository tests
- [x] Week 06 pull request merged and feature branches cleaned
- [x] Week 06 interview review
- [x] Week 06 report
- [x] Week 07 plan
- [x] Week 07 feature branch
- [x] SQLAlchemy, Psycopg, Alembic, and Pydantic Settings dependencies
- [x] Environment-based database configuration
- [x] SQLAlchemy Engine and Session factory foundation
- [x] Manual synchronous connection through `opsdesk_app`
- [x] Five focused configuration and database-factory unit tests
- [x] Complete dependency and quality checks with 112 passing tests
- [x] Stable Month 02 Ticket API project naming
- [x] Typed SQLAlchemy Ticket persistence record
- [x] Explicit persistence-to-domain mapping
- [x] Five persistence metadata tests and five mapper tests
- [x] Complete quality checks with 121 passing tests
- [x] Alembic migration workflow
- [x] PostgreSQL repository implementation
- [x] FastAPI lifespan, application factory, and request-scoped Session wiring
- [x] PostgreSQL API creation and subsequent lookup integration test
- [x] Complete PostgreSQL HTTP failure-path and restart verification
- [x] Isolated database integration tests
- [x] Week 07 technical interview review
- [x] Week 07 pull request merged and feature branches cleaned
- [x] Week 07 report
- [x] Week 08 plan
- [x] Week 08 feature branch
- [x] Authentication and authorization threat model
- [x] Argon2id password hashing boundary and behavior tests
- [x] Secret-aware JWT configuration foundation
- [x] Monday dependency, lint, formatting, unit, and integration quality gates
- [x] Strict login and access-token response schemas
- [x] Deterministic UTC clock boundary for token tests
- [x] Fixed-algorithm JWT creation and validation
- [x] Generic authentication service failure contract
- [x] User registration, login, and persisted current-User resolution
- [x] Server-derived Ticket ownership
- [x] Owner-scoped Ticket collection
- [x] Object-level Ticket detail, update, and delete authorization
- [x] Bounded admin-only cross-owner Ticket collection
- [x] Fast and guarded PostgreSQL authorization tests
- [x] Explicit deferral of unsafe legacy ownership backfill
- [x] Week 08 authentication and authorization interview review
- [x] Week 08 pull request merged and feature branches cleaned
- [x] Week 08 report
- [x] Month 02 report
- [x] Week 09 plan

## Problems

- No current blockers.

## Week 06 Handoff

- PostgreSQL 18.6 is running locally.
- `opsdesk_app` is a non-superuser role that owns `opsdesk_dev`.
- The local application connection requires SCRAM password authentication.
- The relational model contains `tickets`, `comments`, `tags`, and
  `ticket_tags`.
- The schema contains 16 columns and 14 named primary-key, foreign-key, unique,
  and check constraints.
- The deterministic development state contains six Tickets, six Comments, five
  Tags, and six Ticket-Tag assignments.
- The composite index `tickets_status_ticket_id_idx` supports status-filtered
  Ticket listing in identifier order.
- Eight ordered SQL scripts can rebuild data and reproduce the Week 06
  exercises.
- Pull request #4 was merged into `main` as commit `6c60128`.
- Local and remote Week 06 feature branches were deleted after merge.
- `main` is synchronized with `origin/main`.

## Week 07 Monday Outcome

- Created `feature/week-07-sqlalchemy-alembic` from synchronized `main`.
- Added SQLAlchemy 2.0.52, Psycopg 3.3.4, Alembic 1.19.1, and Pydantic Settings
  2.15.0 through `uv`.
- Verified the lockfile, environment synchronization, and installed-package
  compatibility.
- Added a required, immutable, secret-aware database settings model.
- Confirmed that the real `.env` file is ignored while `.env.example` is
  trackable.
- Added testable Engine and Session factory functions without import-time
  connectivity.
- Verified a real SQLAlchemy connection to PostgreSQL 18.6 through
  `opsdesk_app` and `opsdesk_dev`.
- Observed lazy Session transaction behavior before and after its first query.
- Passed five focused configuration and database-factory unit tests.
- Passed the complete 112-test repository suite with Ruff lint and formatting
  checks.
- Renamed the living Weeks 05-08 application to
  `projects/month-02-ticket-api/` while preserving the bounded Week 06 SQL lab.

## Week 07 Tuesday Outcome

- Added a typed declarative `TicketRecord` without replacing the domain
  `Ticket` model.
- Matched the Week 06 PostgreSQL identity, defaults, timestamps, nullability,
  and named constraints in SQLAlchemy metadata.
- Compiled and reviewed the generated PostgreSQL `CREATE TABLE` statement.
- Added explicit conversion from persistence strings to domain enums.
- Added safe business-field mapping back onto an existing persistence record.
- Rejected mismatched identifiers before record mutation.
- Preserved database-owned identifiers and timestamps across mapper updates.
- Passed 25 focused tests and the complete 121-test repository suite.
- Passed Ruff lint, Ruff formatting, and Git diff checks.

## Week 07 Wednesday Outcome

- Initialized Alembic inside the stable Month 02 Ticket API project.
- Connected Alembic to secret-aware settings and `Base.metadata` without
  tracking credentials.
- Added and tested the `(status, ticket_id)` composite index in SQLAlchemy
  metadata.
- Created the isolated `opsdesk_migration_dev` migration database under the
  non-superuser application role.
- Generated and reviewed revision `e07f08d4399d` before applying it.
- Verified the migrated Ticket columns, identity, defaults, constraints,
  primary key, and composite index through the PostgreSQL catalogs.
- Completed upgrade, downgrade, and re-upgrade successfully.
- Confirmed the database is at `head` and `alembic check` reports no metadata
  drift.
- Inspected the complete offline transactional SQL without applying it.
- Passed lockfile, environment, package compatibility, Ruff lint, Ruff
  formatting, Git diff, and all 122 repository tests.

## Week 07 Thursday Outcome

- Added `NewTicket` to separate validated creation input from a persisted
  Ticket with a database-generated identifier.
- Introduced the `TicketRepository` protocol and kept `TicketService`
  independent of concrete storage technology.
- Adapted the in-memory repository and service while preserving existing unit
  and HTTP behavior.
- Implemented SQLAlchemy Ticket create, lookup, ordered listing, update, and
  delete operations.
- Kept repository `flush()` and `refresh()` behavior separate from
  caller-owned `commit()` and `rollback()` decisions.
- Translated expected persistence conflicts without leaking SQLAlchemy
  exceptions into the application contract.
- Added ORM-driven `updated_at` behavior and verified timestamp advancement in
  separate PostgreSQL transactions.
- Created and migrated the dedicated `opsdesk_test` database under
  `opsdesk_app`.
- Added guarded, opt-in integration fixtures and 11 real PostgreSQL repository
  tests.
- Verified commit visibility, rollback invisibility, no implicit repository
  commit, generated identity, CRUD behavior, ordering, missing records, and
  final test cleanup.
- Passed lockfile, environment, package compatibility, Ruff lint, Ruff
  formatting, and Git diff checks.
- Passed 132 tests with 11 integration skips in the default run and all 143
  tests with database integration enabled.
- Confirmed the final `opsdesk_test` Ticket count was zero.

## Week 07 Friday Outcome - 28 August

- Added an application lifespan that constructs the Engine and Session factory
  at startup and disposes the Engine on shutdown or setup failure.
- Added a request-scoped Session dependency with commit on success, rollback
  on an exception or commit failure, and unconditional Session cleanup.
- Selected function-scoped dependency finalization so transaction completion
  occurs before FastAPI sends the response.
- Composed `SqlAlchemyTicketRepository` and `TicketService` through dependency
  injection and removed the default process-global in-memory service.
- Added `create_app()` and preserved fast API tests with a fresh application,
  disabled database lifespan, and an explicit in-memory service override.
- Passed 39 focused tests: 31 existing API tests and eight database-factory,
  Session-finalization, and lifespan tests.
- Passed the first real PostgreSQL API integration test: POST returned `201`,
  a separate database connection saw the committed row, and a subsequent GET
  returned the same Ticket. The production Session/service dependencies were
  used with a guarded test-database Session factory.
- Confirmed `opsdesk_test` contained zero Tickets after targeted cleanup.
- Passed the final whole-repository Ruff lint and formatting checks (90 files
  already formatted), plus `git diff --check`.
- Passed 138 tests with 12 integration skips under `RUN_DATABASE_TESTS=0`
  and all 150 tests under `RUN_DATABASE_TESTS=1`.
- Confirmed zero Tickets in `opsdesk_test` after the complete integration run.
  Staged review, commit, and push remain the Git closing steps.
- Stopped feature work by choice and moved the unfinished Friday verification
  to Saturday. Week 07 is not yet complete.

## Week 07 Saturday Outcome - 29 August

- Confirmed that `opsdesk_test` was empty, migrated to revision `e07f08d4399d`
  at `head`, and free of pending Alembic upgrade operations before testing.
- Expanded the PostgreSQL HTTP suite to eight integration tests using the real
  request Session, SQLAlchemy repository, service, routes, and PostgreSQL
  transaction boundary.
- Verified committed create/read behavior, status filtering and limiting,
  committed update/delete behavior, missing-resource `404` responses, and
  validation `422` responses.
- Verified that an exception after `flush()` rolls back the write, an injected
  commit failure returns no false `201` and leaves no row, and two requests use
  distinct Session instances.
- Kept the existing `409` application contract covered by fast tests without
  inventing a duplicate-title constraint that the relational model does not
  require.
- Started the application against `opsdesk_test` using a process-local database
  override without changing `.env` or exposing credentials.
- Created Ticket `97`, stopped and restarted Uvicorn, retrieved the same Ticket
  after restart, then deleted only that demonstration record. The final Ticket
  count was zero and port `8000` was closed cleanly.
- Passed dependency consistency checks, Ruff lint, Ruff formatting for 90
  files, and `git diff --check`.
- Passed `138` tests with `19` integration skips when database tests were
  disabled and all `157` tests when they were enabled.
- Reconfirmed zero Tickets in `opsdesk_test` and Alembic revision
  `e07f08d4399d` after the complete run.

## Week 07 Sunday Outcome - 30 August

- Completed an eight-question technical interview review covering Psycopg,
  SQLAlchemy, Alembic, Engine, Connection, Session, transaction methods,
  migration safety, mapping, repositories, integration tests, and the complete
  HTTP persistence lifecycle.
- Re-ran the complete dependency, Ruff, formatting, and test gates before
  merge: `138 passed, 19 skipped` without database tests and all `157` tests
  with database tests enabled.
- Reviewed the complete pull-request diff for credentials, local paths,
  destructive development-database targets, test-only behavior, and production
  boundary leaks; no merge blockers remained.
- Merged pull request #5 into `main` through merge commit `7ebc076`.
- Fast-forwarded local `main` to `origin/main` and removed both local and remote
  `feature/week-07-sqlalchemy-alembic` branches.
- Added the Week 07 report and prepared the Week 08 authentication and
  authorization plan.

## Week 08 Monday Outcome - 31 August

- Created `feature/week-08-auth-authorization` from synchronized `main`.
- Separated authentication from authorization and threat-modeled database
  compromise, credential enumeration, bearer-token theft, token tampering,
  IDOR/BOLA, and role escalation before implementation.
- Verified `pwdlib`, Argon2id, PyJWT, FastAPI, and OWASP password-storage
  guidance from primary documentation.
- Added `pwdlib` 0.3.1 with Argon2 support and PyJWT 2.13.0 through `uv`.
- Added a focused `PasswordHasher` boundary around the maintained library
  instead of distributing password-library calls through routes and services.
- Verified that hashes differ from plaintext, correct credentials verify,
  incorrect credentials fail, per-hash salts produce distinct values, and the
  selected encoding identifies Argon2id.
- Added a required secret-aware JWT setting with a minimum length guard and a
  bounded access-token lifetime of 1 through 1,440 minutes, defaulting to 30.
- Kept the real JWT secret out of source, examples, logs, and tests;
  `.env.example` contains only a deliberately invalid placeholder.
- Isolated configuration and PostgreSQL tests from machine-specific JWT
  secrets by providing explicit synthetic test values.
- Passed dependency consistency, Ruff lint, formatting for 94 files, and Git
  diff checks.
- Passed `150` tests with `19` integration skips when database tests were
  disabled and all `169` tests against the guarded `opsdesk_test` database.

## Week 08 Tuesday Outcome - 1 September

- Selected a stable database-generated `user_id` for identity, Ticket
  ownership, and the future JWT subject instead of using mutable email data as
  a relationship key.
- Defined an explicit case-insensitive account-email policy and added
  `email-validator` 2.3.0 for maintained syntax validation and normalization
  without runtime DNS checks.
- Added `NewUser`, `User`, and the bounded `member`/`admin` `UserRole` enum.
  Ordinary registration data contains no client-selected role.
- Added nine User-domain tests covering normalization, invalid input, strict
  identifiers, role types, active state, and password-hash preservation.
- Added a typed SQLAlchemy `UserRecord` with database identity, named unique
  and check constraints, safe `member`/active server defaults, and
  timezone-aware timestamps.
- Added five persistence-model tests for the User table alongside the existing
  Ticket metadata tests.
- Added explicit mapping from trusted registration data to `UserRecord` and
  from persisted records to the `User` domain type. Database defaults remain
  database-owned until `flush()`/`refresh()`.
- Passed Ruff, `git diff --check`, and 29 focused domain, persistence-model,
  and mapper tests.
- Deliberately deferred repository, Ticket ownership, and migration work to a
  longer Wednesday session rather than rushing database-sensitive changes.

## Week 08 Wednesday Outcome - 2 September

- Added a storage-independent User repository protocol plus in-memory and
  SQLAlchemy implementations with normalized-email lookup, database-generated
  defaults, and duplicate-identity exception translation.
- Added guarded PostgreSQL User repository tests without moving `commit()` or
  `rollback()` into the repository boundary.
- Added nullable Ticket `owner_id` metadata, a restrictive foreign key to
  `users.user_id`, an ownership/status/listing index, and mapper protection
  against accidental ownership transfer.
- Added and manually reviewed Alembic revision `e98825c4d6b6` for the User
  table and Ticket ownership expand phase.
- Proved upgrade, downgrade, and re-upgrade behavior against
  `opsdesk_migration_dev`, including preservation of a legacy Ticket while the
  nullable ownership column was added and removed. `alembic check` reports no
  metadata drift.
- Applied the revision to guarded `opsdesk_test` and verified its tables,
  column, unique constraint, foreign key, empty state, and head revision.
- Added strict registration request and public User response contracts. Client
  input cannot select role, identity, active state, or ownership, and responses
  cannot expose plaintext or hashed passwords.
- Added an injected `PasswordHashing` protocol and `RegistrationService` that
  validates identity before the expensive hash, stores only an Argon2id hash,
  and translates repository conflicts without depending on SQLAlchemy.
- Added `POST /auth/register`, dependency composition, fast HTTP tests, and
  guarded PostgreSQL tests for durable registration, password hashing,
  duplicate conflict rollback, and exact cleanup.
- Passed dependency consistency, Ruff, formatting for 101 files, and Git diff
  checks. Passed `205` tests with `27` integration skips and all `232` tests
  with guarded database tests enabled.

## Week 08 Thursday Outcome - 3 September

- Added strict login and access-token response schemas.
- Added a small `Clock` protocol and timezone-aware `SystemClock`, allowing
  deterministic token issuance tests without changing production time code.
- Added an HS256 JWT manager that issues only `sub`, `iat`, and `exp`, requires
  those claims during decoding, fixes the accepted algorithm in server code,
  and returns a validated positive `user_id`.
- Covered modified signatures, wrong secrets, unsupported algorithms, expired
  tokens, missing claims, invalid subjects, naive clocks, and invalid creation
  identities with 17 focused token tests.
- Added `AuthenticationService` behind repository, password-verification, and
  token-issuing protocols. Correct credentials issue a token for immutable
  `user_id`; wrong passwords, missing users, and inactive users produce the
  same public error and never invoke token issuance.
- Included a dummy password-hash input in the application contract so missing-
  user authentication does not take an immediate fast-exit path. Real cached
  Argon2id dummy-hash composition remains the first Friday task.
- Passed dependency consistency, Ruff lint, formatting for 105 files, and Git
  diff checks.
- Passed `235` tests with `27` integration skips and all `262` guarded database
  tests. Reconfirmed zero Users, zero Tickets, and Alembic revision
  `e98825c4d6b6` in `opsdesk_test`.

## Week 08 Friday Outcome - 4 September

- Added one process-cached, valid Argon2id dummy hash and composed the real
  authentication service from settings, SQLAlchemy, pwdlib, the UTC clock,
  and the fixed-algorithm JWT manager.
- Added JSON `POST /auth/login` and a single generic `401` contract for missing
  accounts, incorrect passwords, inactive accounts, and invalid credentials.
- Added optional HTTP Bearer extraction, strict scheme/token validation, and a
  current-User service that reloads the persisted User on every request.
- Added `GET /users/me`; malformed and expired tokens, deleted Users, and
  inactive Users fail closed even when the token signature remains valid.
- Protected `POST /tickets` and derived `owner_id` exclusively from the
  authenticated User. Client-supplied ownership is rejected by the strict
  request schema, and the service/repository path preserves the owner.
- Added focused unit, HTTP, and guarded PostgreSQL coverage for login, current
  identity, stale-token rejection, protected creation, persisted ownership,
  commit failure, rollback, and exact database cleanup.
- Passed dependency consistency, Ruff lint, formatting for 106 files, and Git
  diff checks. Passed `255` tests with `33` integration skips and all `288`
  tests with guarded database tests enabled.

## Week 08 Saturday Outcome - 5 September

- Replaced the broad Ticket collection repository operation with the explicit
  `list_by_owner(owner_id)` contract in both in-memory and SQLAlchemy adapters.
- Applied the ownership predicate inside the PostgreSQL query so another
  User's Ticket does not cross the persistence boundary.
- Required authentication for `GET /tickets` and passed the current persisted
  User's immutable identifier through the route and service layers.
- Added in-memory repository, service, HTTP, missing-Bearer, SQLAlchemy, and
  two-User PostgreSQL tests for owner-scoped listing and stable ID ordering.
- Confirmed two real Users can create separate Tickets while each collection
  response returns only the caller's Ticket; cleanup left zero Users and zero
  Tickets.
- Updated the request-scoped Session isolation test for the newly protected
  route without weakening its original two-request/two-Session assertion.
- Passed dependency consistency, Ruff lint, formatting for 106 files, and Git
  diff checks. Passed `257` tests with `34` integration skips and all `291`
  tests with guarded database tests enabled.
- Stopped intentionally after the complete collection-authorization slice;
  identified-resource and role authorization move to Sunday.

## Week 08 Sunday Outcome - 6 September

- Protected Ticket preview, detail, update, and delete with the current active
  User dependency.
- Added owner-aware service checks and consistent non-disclosing `404`
  responses for missing and foreign-owned Ticket identifiers.
- Proved through fast and real PostgreSQL tests that another User cannot read,
  update, or delete a Ticket and that failed attacks preserve the stored row.
- Added a dedicated admin dependency and the separate `GET /admin/tickets`
  function. Members receive `403`; admins can list across owners while normal
  `/tickets` remains owner-scoped.
- Verified that JWTs keep only the User subject and that role changes in
  PostgreSQL affect the next request made with an already-issued token.
- Deferred the nullable ownership contract rather than inventing a false owner
  for historical rows; new API writes continue to require authenticated,
  server-derived ownership.
- Passed dependency consistency, Ruff lint, formatting for 107 files, Git
  diff, Alembic-head, and zero-drift checks. Passed `274` tests with `37`
  integration skips and all `311` guarded database tests.
- Confirmed `opsdesk_test` ended with zero Users and Tickets at Alembic revision
  `e98825c4d6b6`.

## Week 08 Closure and Month 02 Handoff

- Reviewed the complete 43-file pull-request diff for credentials, complete
  tokens, local paths, test-only production behavior, and authorization
  bypasses; no merge blocker remained.
- Committed the final authorization boundary as `a1cf847`.
- Merged pull request #6, `Week 08: add authentication, Ticket ownership, and
  authorization`, through merge commit `9876703`.
- Fast-forwarded local `main` to `origin/main` and deleted both local and
  remote `feature/week-08-auth-authorization` branches.
- Recorded the completed Week 08 evidence and Month 02 result without marking
  the missing CI or deployment milestones as complete.
- Froze `projects/month-02-ticket-api/` as a bounded learning application.
- Prepared Week 09 for the separate real OpsDesk product repository.

## Week 09 Monday Outcome - 7 September

- Started the primary Month 03 mentoring conversation and reviewed the Month 02
  handoff, Week 09 plan, working rules, status, and historical decisions.
- Confirmed the bootcamp repository was clean and synchronized on `main` before
  the day's documentation changes.
- Furkan drafted the product scope, two additional acceptance scenarios, and
  the README; mentoring review refined wording and security boundaries.
- Created the separate [OpsDesk repository](https://github.com/ozdemirr1/opsdesk)
  with README, `.gitignore`, and `docs/requirements.md`. The Month 02 application
  was not copied.
- Recorded initial functional requirements, organization-isolation expectations,
  explicit Month 03 non-goals, three acceptance scenarios, and open decisions.
- Kept the customer-resolution restriction explicitly proposed until the access
  and status-transition matrices are reviewed. Attachment scope remains metadata
  design rather than file-content upload or storage.
- Furkan reviewed the staged diff, created commit `eb0e20e` with message
  `week-09: define OpsDesk scope and repository foundation`, configured `origin`,
  and pushed `main` with upstream tracking.
- Verified public visibility through the signed-out GitHub repository page.
  The supplied terminal evidence shows a successful push and a clean, synchronized
  `main`; the local status was independently checked afterward.
- Passed Git whitespace checks and verified `.env` and local environment/cache
  ignore rules. No executable code exists in OpsDesk, so no automated tests ran.
  Acceptance scenarios are design evidence, not passing test results.
- Completed the seven-question Monday learning review. Core reasoning was sound;
  the precision corrections below were recorded for future implementation.
- Furkan committed the Monday bootcamp evidence as `439e24c`, pushed `main`,
  and supplied terminal evidence of a clean, synchronized working tree.

### Monday Learning Review Corrections

- A membership role models organization-specific authority; the schema alone
  does not enforce authorization. Backend queries and permission checks must
  enforce the boundary on every relevant operation.
- Role checks and identified-Ticket access checks are separate. Two customers
  with the same organization role can have different access to a specific Ticket.
- For the ordinary customer creation workflow, derive the requester from the
  current authenticated User. A validated JWT subject identifies the User to load;
  check current account state and target membership rather than trusting the token
  alone. Do not treat a bearer credential as proof of the human operating it.
- Denied mutations must leave business data unchanged. Prefer authorization before
  writes; rollback handles failures within a transaction and is not a substitute
  for authorization. Verify durable state through an independent database read.
- A lifecycle includes allowed transitions, actors, and preconditions, not just
  status labels. The exact OpsDesk transition policy remains unresolved.
- Attachment metadata describes a file and its relationships; it is distinct from
  a stable attachment identifier and from the file bytes. A local filesystem is
  a storage option, but is not itself an object-storage service such as S3.
- Commit records staged changes locally; remote configuration names a repository
  URL; push sends required objects and updates remote refs. The `-u` option sets
  upstream tracking. Public visibility is a GitHub setting, not a push effect.

## Week 09 Tuesday Outcome - 8 September

- Furkan drafted User, Organization, OrganizationMembership, Ticket, Comment,
  and Attachment, then explained and refined the associated domain policies.
- Consolidated the reviewed vocabulary, purposes, identities, relationships,
  lifecycles, invariants, preconditions, and unresolved decisions in OpsDesk's
  `docs/domain-model.md` on `feature/week-09-domain-design`.
- Updated the OpsDesk README link and requirements to distinguish reviewed
  policies from unresolved relational and authorization choices.
- Selected exactly one active owner per active Organization, backed by an active
  User; ownership transfer is atomic and leaves the former owner as admin.
- Selected one membership record per User-Organization pair across all states,
  reactivation with an explicitly authorized current role, and ownership checks
  before global account deactivation.
- Separated fixed Ticket requester/creator attribution from mutable current
  assignment. New Tickets are open and may be unassigned.
- Required handover before changes revoke eligibility for assigned open or
  in-progress Tickets. Membership and role changes check the target Organization;
  global account deactivation checks all Organizations. Reopening requires renewed
  eligibility evaluation, with the exact transition behavior still pending.
- Selected append-only Comments for all user roles and Ticket-derived reading
  visibility. Staff-only internal notes are outside Month 03.
- Selected Attachment metadata linked exclusively to one fixed Ticket; metadata
  does not establish upload success, physical availability, or verified file type.
- Passed documentation whitespace, code-fence, and local-link checks. No executable
  code, migrations, or automated application tests were added or run. The domain
  document lists future test expectations without claiming passing tests.
- Completed the seven-question Tuesday review. Answers correctly distinguished
  atomicity from simultaneous SQL execution, membership identity from audit history,
  fixed attribution from assignment, scoped from global checks, reactivation from
  historical eligibility, reading from posting, and metadata from file evidence.
- Clarified one terminology detail: resolved means the issue is resolved; it is
  not the separate closed status. Reopening rules remain an explicit open decision.
- Furkan reviewed and committed the three OpsDesk documentation files as `0dab9c4`.
  The initial push needed upstream configuration; the retry succeeded and the
  working tree is clean. Furkan renamed the branch to
  `feature/week-09-domain-design`, published it with upstream tracking, and removed
  the old remote branch name. Commit `0dab9c4` was preserved.
- Furkan committed the Tuesday bootcamp evidence as `5f0dad5` and pushed main.
  Wednesday's local inspection confirmed a clean, synchronized working tree.
- Recorded Furkan's branch-naming preference: use `feature/week-XX-topic` and
  product-focused wording without assistant branding in new GitHub work.

## Week 09 Wednesday Outcome - 9 September

- Furkan translated all six domain entities into relational tables, then drafted
  the constraints, composite participant references, child tables, and Mermaid ERD.
- Recorded the reviewed baseline in OpsDesk's `docs/relational-model.md` and
  `docs/erd.md`; updated README, requirements, and domain-model references.
- Selected bigint identity primary keys, database role/status/priority checks,
  one membership per User-Organization pair across states, and structural UNIQUE
  groups for organization-scoped composite foreign keys.
- Selected an optional assignee with MATCH SIMPLE, ten ON DELETE RESTRICT foreign
  keys, fixed historical participant references, append-only Comment operations,
  and Ticket-bound Attachment metadata without physical upload/storage behavior.
- Distinguished the owner partial unique index's at-most-one guarantee from the
  application's exactly-one active owner and active global User requirements.
  The cooperating concurrency protocol and lock order remain design prerequisites.
- Reviewed timestamp defaults, explicit updated_at refresh, nonblank text checks,
  deletion direction, and the separation between tenant consistency and access.
- Rendered the corrected Mermaid diagram with six entities and ten relationships.
  Passed Markdown fence, local-link, whitespace, and Git diff checks. No OpsDesk
  migrations or application tests were executed; this is documentation evidence.
- Completed the seven-question Wednesday learning review. Core reasoning was
  correct; the precision corrections below are part of the review record.
- Furkan reviewed and committed the five OpsDesk documentation files as `e021f17`
  with message `week-09: document relational design and ERD`, then pushed
  `feature/week-09-domain-design`. Supplied terminal evidence confirms a clean
  working tree and synchronization with the remote branch.
- Furkan committed the Wednesday bootcamp evidence as `dc44bef` and pushed main;
  supplied terminal evidence confirmed a clean, synchronized working tree.

### Wednesday Learning Review Corrections

- RESTRICT protects a referenced parent while child references exist. The precise
  phrase is an unreferenced record, not a record without a parent. The current FK
  does not stop deleting the Comment itself. The selected application policy
  enforces append-only behavior; additional database permissions or triggers could
  provide stronger enforcement if explicitly designed later.
- DEFAULT does not automatically run on every UPDATE. It can nevertheless be
  requested explicitly with SET column = DEFAULT. now() is transaction-start
  time; wall-clock time means actual clock time, not specifically commit time.
- The POSIX [:space:] class is not a universal guarantee for every Unicode
  whitespace or invisible character. Non-ASCII classification depends on
  locale/collation; application normalization and database validation need shared
  examples. Keep NOT NULL alongside the proposed nonblank CHECK.
- MATCH SIMPLE skips this composite FK match when an assignee is absent; it does
  not disable the Ticket's separate Organization FK or other constraints.

## Week 09 Thursday Outcome - 10 September

- Confirmed both repositories were clean before the day's design work. OpsDesk
  remains on `feature/week-09-domain-design`; Git mutations remain Furkan's task.
- Furkan drafted and reviewed Ticket visibility, creation, priority, commenting,
  assignment, membership management, ownership transfer, and lifecycle matrices.
- Customers see their requested Tickets; staff see all Tickets in the Organization.
  Assignment permissions are separate: agents can distribute unassigned work but
  can only reassign/remove their own existing assignments under status rules.
- All roles may create for self; creation is always open and unassigned, with
  medium priority when omitted. Explicit invalid/null priority is not defaulted.
- Agent/admin/owner are eligible assignee roles. Admin-to-agent preserves active
  assignments; changes that revoke eligibility require the reviewed handover checks.
- Admins may manage non-owner peers. Ordinary self-role changes are denied;
  non-owners may leave subject to handover. Only the current owner can transfer
  ownership to a different active User with an active same-Organization admin membership.
- Reviewed peer-management risk and clarified that owner protection is not complete
  account-abuse prevention. Admin promotion before transfer is a prerequisite, not
  independent proof of intent or approval by a second person.
- Defined six allowed state transitions. In_progress requires an eligible assignee;
  closed is terminal but remains readable. Comments are allowed under resource/role
  rules until closed; priority and ordinary assignment changes stop at resolved.
- Returning to open preserves an eligible assignee and clears an ineligible one
  atomically with the status change. This cleanup grants no general assignment
  authority to the customer and does not preserve a complete assignment history.
- Furkan authored four acceptance scenarios covering customer reopening with an
  inactive assignee, denied reassignment by a different agent, admin-to-agent role
  change with active work, and rejected commenting on a closed Ticket.
- Prepared OpsDesk's `docs/access-control.md` and `docs/ticket-lifecycle.md` and
  aligned the README, requirements, domain, and relational documents. The scenarios
  are design evidence, not executed tests. No CRUD, migration, or application tests
  have been added or run. Documentation links, anchors, table widths, code fences,
  whitespace, and Git diff checks passed.
- Completed the seven-question Thursday review. Furkan explained separate visibility
  and mutation permissions, eligibility-preserving role changes, conditional cleanup,
  atomicity versus concurrency, separate-request outcomes, ownership-transfer limits,
  and durable unchanged state after rejected commenting.
- Furkan reviewed and committed the six OpsDesk documentation files as `196c1b2`
  with message `week-09: define access control and ticket lifecycle`, then pushed
  `feature/week-09-domain-design`. Supplied terminal evidence confirms a clean
  working tree and synchronization with the remote branch. Only the bootcamp
  documentation closing commit and push remain pending.

### Thursday Learning Review Corrections

- A customer can reopen their resolved Ticket, not a closed Ticket. Closed is a
  terminal state for all roles; use exact state names rather than colloquial closed.
- Active-work handover means transferring responsibility before eligibility is
  revoked. The rule blocks eligibility revocation while assignments remain, not
  the handover itself. Admin-to-agent preserves eligibility under this product policy.
- Transaction atomicity does not by itself coordinate concurrent eligibility and
  assignment changes. Reads and writes may be separate statements within a correctly
  coordinated transaction. The concrete concurrency mechanism and lock order have
  not yet been selected; do not mistake the design requirement for an implementation.
- An open-and-assigned result after failed ordinary unassignment is valid. This
  example assumes no additional successful intervening operation; each request must
  evaluate current state rather than assuming the previous request's snapshot.

## Week 09 Immediate Actions

1. Review, commit, and push Thursday's bootcamp evidence manually. OpsDesk's
   documentation commit and push are complete as `196c1b2`; the learning review is complete.
2. On Friday, define endpoint scope, request/response boundaries, public errors,
   pagination, and remaining operation permissions without assuming admin bypasses.
3. Resolve remaining validation/concurrency decisions and complete the issue
   backlog before beginning Week 10 CRUD implementation.

## Week 09 Guardrails

- Do not copy the Month 02 learning API wholesale into OpsDesk.
- Do not put organization roles directly on the global User.
- Do not use an ambiguous owner field for organization ownership, Ticket
  requester, and Ticket assignment.
- Do not begin CRUD before domain and authorization rules are reviewable.
- Keep persistence synchronous unless a demonstrated requirement changes it.
- Add minimal CI only after executable code and meaningful tests exist.
- Do not add a Docker build before the scheduled Docker phase creates a real
  Dockerfile.
- Do not start Redis, React, or AI integration early.
- Keep credentials, `.env`, complete URLs, and complete tokens outside Git.
