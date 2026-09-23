# Weekly Status

## Current Week

Week 11 — identity implementation; Week 10 evidence ready for Git closure

## Date

21 September - 27 September 2026

## Current Focus

- Publish the [Week 10 report](weekly-reports/week-10.md) and closing evidence
- Follow the [23–27 September Week 11 plan](weekly-reports/week-11-plan.md)
- Implement reviewed registration #11, login #12 and current-user resolution #13
- Complete all remaining D03 decisions alongside #11/#12/#13 by 27 September
- #4 design is merged; business locking remains dependent feature work

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
  working tree and synchronization with the remote branch.
- Furkan committed the Thursday bootcamp evidence as `23296e7` and pushed main;
  supplied terminal evidence confirmed a clean, synchronized working tree.

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

## Week 09 Friday Progress - 11 September

- Confirmed clean working trees before Friday consolidation: OpsDesk at `196c1b2`
  on `feature/week-09-domain-design`, bootcamp at `23296e7` on main. Local tracking
  references agree; the supplied Thursday terminal output establishes push evidence.
- Furkan drafted 22 endpoints covering identity, Organizations, Tickets, Comments,
  memberships, and ownership transfer, then public errors and pagination.
- Recorded the reviewed baseline in OpsDesk's `docs/api-contract.md` and aligned
  README, requirements, domain, relational, access-control, and lifecycle documents.
- Organization creation establishes the actor's owner membership atomically. Basic
  suspended-Organization information remains visible to active members, while child
  resources and scoped mutations remain blocked.
- Reviewed safe response projections, actor-derived creation fields, logical
  membership deactivation, separate admin promotion, and current target eligibility.
- Corrected same-status no-op ordering: Ticket visibility alone is insufficient;
  explicit operation permission is required. Authorized no-ops do not refresh
  updated_at or execute transition effects. Idempotency does not require equal responses.
- Exact-email addition uses an existing active User and creates membership directly.
  Missing/inactive targets share a safe failure, but successful addition can still
  disclose account existence. No invitation or independent approval is implied.
- Selected limit/offset, default 20, maximum 100, scoped counts, and Ticket ordering
  by created_at DESC then ticket_id DESC. Empty collections retain the response
  envelope. Offset ordering does not guarantee a snapshot under concurrent changes.
- Deferred Ticket text editing/deletion, Organization renaming/suspension endpoints,
  global User deactivation, and all Attachment metadata endpoints beyond Month 03.
  Their relevant domain rules remain; closing a Ticket is not data erasure.
- Furkan supplied a TicketResponse and a validation-error JSON example. Both match
  the selected fields; the error does not echo raw rejected input. Added an empty
  pagination example for the common envelope.
- Documentation checks passed for JSON syntax, 22 unique endpoints, local links and
  anchors, Markdown fences/table widths, and whitespace. No API, migration, or
  executable application tests were added or run.
- Precise validation, remaining error/response cases, proposed queue/directory
  filters, other collection orderings, count/items consistency, and transaction
  coordination are explicitly unfinished. The issue backlog still precedes CRUD.
- Completed Friday's seven-question learning review. Furkan correctly explained
  response/request separation, explicit no-op permission, the suspended-Organization
  visibility exception, logical membership deletion, account-enumeration limits,
  scoped pagination counts, and safe errors with unchanged durable business state.
- Furkan reviewed and committed the seven OpsDesk documentation files as `35ba9b5`
  with message `week-09: define API contracts and release boundaries`, then pushed
  `feature/week-09-domain-design`. Supplied terminal evidence confirms a clean
  working tree and synchronization with the remote branch.
- Furkan committed the Friday bootcamp evidence as `5edc020` and pushed main.
  Supplied terminal evidence confirmed a clean, synchronized working tree;
  Saturday's opening local inspection also confirmed both repositories were clean.

### Friday Learning Review Notes

- No substantive answer correction was required. The suspended-Organization
  visibility exception still requires an active authenticated global User as well
  as an active membership; it does not weaken authentication.
- For offset pagination, updates matter when they change ordering or whether a
  record matches the query's filters or visibility scope. An unrelated field
  update does not necessarily shift the result set.
- Rejected-mutation tests should reload persisted state and compare relevant fields
  and child records: status, assignment, updated_at, and newly created Comments as
  applicable. An unchanged in-memory object or error response alone is insufficient.
  This assertion concerns business state; it need not prohibit an intended rejection
  log or security event.

## Week 09 Saturday Progress - 12 September

- Furkan drafted and revised four bounded issues: Ticket creation validation,
  authenticated-member Ticket creation, backend application foundation, and guarded
  PostgreSQL integration-test infrastructure. The first three drafts are reviewed;
  the guarded-test draft still needs its concrete isolation method and verification
  of application commits, exception cleanup, and resource release.
- Preserved the drafts and preliminary dependency map in OpsDesk's
  `docs/issue-plan.md`, linked from README. These are local planning documents,
  not published GitHub issues or completed implementation.
- Distinguished defining validation policy from implementing it. Creation rejects
  server-controlled fields rather than ignoring them, derives tenant membership
  references, and tests durable state as well as status codes.
- Reviewed foundation acceptance criteria: reproducible installation, documented
  configuration, actual startup/shutdown, isolated tests, and safe errors. Minimal
  CI waits for executable code and meaningful tests; no health endpoint is added
  solely to satisfy a superficial test.
- Reviewed dependencies: independent design work, required schema and authentication
  inputs, and guarded test infrastructure before business-schema verification.
  Identity validation/authentication contracts need their own bounded design work.
- Restricted integration-test targeting to exact opsdesk_test plus an explicitly
  allowed server. A _test suffix is insufficient. Guard tests must verify that
  rejected targets never reach destructive setup/cleanup.
- Isolation verification uses successive scopes with a probe table, not two tests
  that depend on execution order or an assertion that the whole database is empty.
  App/test configuration remains separate; engine/session setup is assigned to the
  guarded-test issue rather than silently assumed to exist in foundation.
- Furkan explicitly chose to stop new drafting and begin daily closure. Moved
  remaining issues, isolation follow-up, priorities/labels, Week 10 sequencing,
  GitHub publication, and the full weekly review/report to Sunday, 13 September.
- No application, schema, executable tests, CI, or GitHub issues were created
  during this session. Documentation checks passed.
- Completed Saturday's four-question learning review. Furkan correctly explained
  a ready issue versus completed decisions, exact database/server targeting,
  rollback limitations after a real commit, and independence from test order.
- Furkan reviewed and committed README and the issue-plan document as `8d546bd`
  with message `week-09: draft implementation issues and dependencies`, then pushed
  `feature/week-09-domain-design`. Supplied terminal evidence confirms a clean,
  synchronized working tree.
- Furkan committed the Saturday bootcamp evidence as `40df4cc` and pushed main.
  Supplied terminal evidence confirmed a clean, synchronized working tree;
  Sunday's opening local inspection also confirmed both repositories were clean.

### Saturday Learning Review Notes

- A real committed database transaction cannot be undone by rolling back a later
  transaction. A Session commit in a deliberately configured test harness can have
  different boundaries when joined to an externally owned transaction; the concrete
  method remains Sunday's design work, not an implemented isolation guarantee.
- Test independence is the requirement; pytest need not be described as inherently
  random. Tests must work when selected alone or reordered. The chosen isolation
  verification exercises successive scopes in one controlled test; this is a useful
  technique, not the only possible way to verify isolation. Concurrent test execution
  additionally requires its own resource-isolation policy and is not promised here.

## Week 09 Sunday Progress - 13 September

- Opening checks confirmed OpsDesk at `8d546bd` and bootcamp at `40df4cc`, both
  initially clean. Recorded Saturday's completed bootcamp push evidence.
- Reviewed explicit test isolation: real application commits, independent-session
  verification, validated allowlisted DELETE cleanup before/after scopes, preserved
  migration history, and one suite per test database. Controlled multi-session
  concurrency belongs inside one test and must finish before cleanup.
- Furkan drafted identity/authentication contract, initial schema, Ticket schema,
  and registration issues; mentoring corrections clarified token-validation tests
  target protected requests, migration predecessor boundaries, password verification,
  known-constraint conflict mapping, and real concurrent registration checks.
- At Furkan's request, prepared login and current-user issue drafts, then continued
  Organization creation/read, staff directory, and member addition/reactivation.
  Four Saturday drafts plus ten additions made 14, correcting the earlier estimate
  of 12 drafts. No GitHub issues had been created.
- Following Furkan's request to continue with grouped drafting, prepared twelve
  further proposals covering remaining membership/Ticket/Comment workflows, contract
  and concurrency design, shared errors/logging, CI, and the Month 03 preview.
- Consolidated 26 English issue bodies in OpsDesk's `docs/issues/`; `docs/issue-plan.md`
  now contains local IDs, suggested priorities/labels, an acyclic dependency graph,
  exact coverage of all 22 API endpoints, and a proposed Week 10 sequence. The four
  original drafts remain in individual files rather than being discarded.
- Updated the API baseline with the reviewed common login 401 outcome. Exact identity
  policies and remaining API/concurrency choices are still design work, not resolved
  merely by creating an issue about them.
- Furkan reviewed and committed the consolidated 26-issue backlog as `3ad42fe`
  (`week-09: consolidate issue drafts and implementation plan`) and pushed the
  OpsDesk feature branch. Supplied terminal evidence confirmed a clean working tree.
- Furkan installed GitHub CLI, authenticated, verified an empty issue list, created
  D01 as #1, then ran the prepared batch publication. All 26 issues and eight labels
  now exist. Read-only GitHub verification confirmed exact titles, local IDs, labels,
  and dependency links. See the [published backlog](https://github.com/ozdemirr1/opsdesk/issues).
- Linked real issue numbers in the product issue index and marked local issue bodies
  as initial-publication snapshots. GitHub owns live task status; product contracts
  must still be updated when accepted behavior changes. Dependency links are Markdown
  references, not native GitHub blocking relationships.
- Completed Sunday's seven-question architecture review. Furkan correctly explained
  tenant consistency versus authorization, owner-index limits, real commit boundaries,
  persisted identity, design prerequisites, and durable-state checks. Precision notes
  are recorded below and in the [Week 09 report](weekly-reports/week-09.md).
- Prepared the [Week 10 handoff](weekly-reports/week-10-plan.md) for 15-20 active hours.
  Foundation, guarded tests, and initial schema take priority; authentication is
  capacity-dependent. D01-D04 still require decisions before dependent implementation.
- No completed career action was evidenced; explicitly carried a bounded internship
  preparation task into Week 10. The subsequent bootcamp push and PR merge are
  verified below.
- Furkan committed the 28 OpsDesk publication/review documents as `08717e6`
  (`week-09: link published backlog and record review completion`) and pushed
  `feature/week-09-domain-design`. Supplied terminal evidence confirms a clean
  working tree synchronized with the remote feature branch.
- Documentation checks passed for local links/anchors, Markdown structure/whitespace,
  existing JSON examples, required issue sections, dependency cycles, and endpoint
  coverage. No OpsDesk runtime code, migrations, application tests, CI, or deployment
  were created. The temporary publication helper was checked with an offline
  simulation for existing-issue reuse, repeat execution, and dependency-link mapping;
  that is tooling verification, not evidence of a tested product API.

- Furkan committed and pushed the five bootcamp closing documents as `ae8133a`;
  supplied terminal evidence confirmed clean, synchronized main.
- Furkan created and merged [OpsDesk PR #27](https://github.com/ozdemirr1/opsdesk/pull/27)
  as `c3a45ed`. The PR state is MERGED. He switched to main and pulled with
  `--ff-only`; supplied evidence confirms clean main synchronized with origin/main.
  Feature-branch cleanup remains the final repository housekeeping step.

### Sunday Learning Review Corrections

- Atomic ownership transfer does not execute every SQL statement simultaneously.
  Coordinate constraint timing and concurrent workflows; locks do not replace actor
  authorization or target eligibility checks.
- Cleanup requires exact `opsdesk_test` and allowed-server validation before writes,
  a fixed table allowlist, FK-safe deletion, preserved migration history, and closed
  sessions. Surface cleanup failures and stop subsequent scopes; ordinary teardown
  cannot be guaranteed after hard process termination.
- Issue closure is bookkeeping, not proof. Design tasks require reviewed decisions
  and contract examples; implementation tasks require relevant code/test evidence.
  Ticket creation #18 depends on #1, #3, #4, #8, #13, and #10, not only validation #1.
- Independent-session checks should compare all relevant durable business fields;
  permitted rejection logs are not forbidden by the unchanged-business-state rule.
- Current accepted behavior belongs in product documents. Closed design issues are
  historical rationale and may be superseded; local drafts are publication snapshots.

## Week 09 Immediate Actions

1. Remove the merged OpsDesk feature branch locally and remotely, then verify main.
2. Have Furkan commit/push this final merge-evidence update in the bootcamp repository.
3. Begin Week 10 from OpsDesk main at `c3a45ed` (or its verified successor), create
   the agreed Week 10 feature branch, and resolve design prerequisites before their
   dependent implementation. The reviewed plan is in `weekly-reports/week-10-plan.md`.
4. Complete the explicitly carried-over bounded career task during Week 10.

Sunday estimate: 3-4 hours of active work including carried-over planning and weekly
review; keep any unfinished work explicit if the available session is shorter.

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

## Week 10 Tuesday Opening — 15 September

- Furkan could not access the system on Monday, 14 September. At his request,
  Monday and Tuesday work is combined today; no Monday completion is claimed.
- Opening local checks: OpsDesk main at `c3a45ed`, bootcamp main at `f136471`,
  both clean and matching their local origin/main tracking references. The previously
  supplied terminal output confirms the Week 09 pushes and feature-branch deletion.
- Week 09 housekeeping is complete: PR #27 merged, feature branch deleted locally
  and remotely, and final bootcamp handoff evidence pushed as `f136471`.
- Revised today's plan to approximately 5-6 active hours: #1, #2, #5, #9, then
  grouped learning review and Git closure. No Week 10 issue is completed yet.
- Git and GitHub mutations remain Furkan's task; no implementation was generated
  during the opening repository and schedule checks.

### Tuesday — Ticket Creation Validation Review

- Furkan created `feature/week-10-backend-foundation`; supplied terminal evidence
  confirmed a clean branch before design changes.
- Reviewed title length 1..255 and description length 1..10000 after Python str.strip(),
  measured in Unicode code points with no additional Unicode normalization.
- Reject title tab/CR/LF and both fields' NUL before trimming; preserve internal
  description formatting and store trimmed text. Corrected the sample description
  to retain four- and two-space internal indentation.
- Priority is an exact enum with no trimming/case conversion; only omission defaults
  to medium. Required field types are strict and every unlisted field is rejected,
  including server-controlled values matching creation defaults.
- Furkan correctly classified the supplied boundary and invalid-input cases. Recorded
  the reviewed contract in OpsDesk's `docs/ticket-creation-validation.md` and aligned
  API, relational, requirements, and issue-index references.
- Clarified validation acceptance versus successful authorized commit; the field
  policy does not resolve shared authentication/authorization error precedence (#3).
- Documentation links, JSON examples, and whitespace checked. No endpoint, migration,
  or application tests implemented. Furkan committed/pushed the five contract documents
  as `fc81057` on `feature/week-10-backend-foundation`; supplied terminal evidence
  confirms a clean working tree and upstream tracking. GitHub issue closure remains
  separate from this commit. #2, #5, and #9 remain in today's combined session.

### Tuesday — Identity and Authentication Contract Review

- Furkan selected lowercase canonical ASCII email, edge trimming, preserved dots/tags,
  exact shared identity lookup, and 409 email_already_exists for duplicate registration.
  Reviewed format examples, 254-character limit, bare addresses, and no DNS checks.
- Furkan defined NFC-normalized Unicode passwords of 15..128 code points, preserved
  whitespace/case, no truncation, and consistent registration/login preprocessing.
  Clarified valid UTF-8 input and hashing at registration versus verification at login.
- Furkan defined HS256-only access tokens with 30-minute lifetime, zero leeway,
  mandatory sub/iat/exp/iss/aud, environment secret, and current persisted active User.
  Corrected algorithm-header wording: reject unsupported alg rather than ignore it;
  claim types require strict validation beyond presence checks.
- Consolidated the reviewed outcomes in OpsDesk's
  `docs/identity-authentication-contract.md`, including examples, canonical email
  storage obligations, generic login failures, and separate authorization checks.
  Updated API/relational/requirements/index references and checked documentation.
- Furkan committed and pushed the reviewed identity contract and aligned documents
  as `8959911`. No login, JWT, password hashing, or database implementation is claimed.

### Tuesday — Executable Foundation and CI Evidence

- Furkan initialized the independent OpsDesk package with uv and Python 3.14.7,
  wrote the application factory and Pydantic Settings, and implemented seven tests.
  Reviewed settings defaults, environment parsing, invalid configuration rejection,
  hidden input in exception text, documentation visibility, and explicit settings
  overriding invalid ambient configuration. TestClient context managers exercise
  application startup/shutdown; no artificial lifecycle resource was introduced.
- Review corrections covered the main.py module location, case-sensitive keyword
  arguments, an unused TestClient instance, explicit test settings, and separation
  of application tests from configuration tests. Furkan requested direct file review
  rather than repeatedly pasting code into the conversation.
- Recorded settings and local commands in README. No automatic .env loading or
  required database/JWT setting is introduced. Production environment selection does
  not implicitly disable documentation or establish production readiness.
- Furkan committed and pushed foundation code, tests, dependency lockfile, and README
  as `a5461a4`. Added explicit Ruff and pytest configuration before CI publication.
- Furkan authored the GitHub Actions workflow with read-only contents permission,
  checkout credentials disabled, pinned uv version, locked installation, and explicit
  selection of the two foundation test files. Database integration tests are excluded.
  He committed and pushed the workflow, tool configuration, and CI README as `0bc43d5`.
- Local checks passed: seven tests, Ruff lint, five Python files formatted, and
  git diff --check. The Starlette/AnyIO deprecation warning remains visible.
  Updated the test-client dependency to httpx2 following the installed Starlette
  compatibility warning; no warning-suppression rule was added.
- Hosted [Backend CI run 35004969487](https://github.com/ozdemirr1/opsdesk/actions/runs/35004969487)
  completed successfully for `0bc43d570b80e1cdd631bed7781f947a2ba5a938`.
  Read-only API verification and Furkan's terminal output both confirm success.
  gh run list with a workflow filename initially returned 404 because the workflow
  was absent from default main; listing the feature branch without that filter worked.
- Controlled failure checks in temporary copies confirmed exit code 1 for an unused
  import, formatting violation, and intentionally incorrect test expectation. These
  are local negative checks, not failed hosted runs. The product checkout stayed clean.
- Combined Monday/Tuesday technical scope (#1, #2, #5, #9) has reviewed evidence on
  feature/week-10-backend-foundation. GitHub issue closure and PR merge have not been
  performed or claimed. The grouped learning review is complete; the bootcamp closing
  commit/push was subsequently completed as `5275f70`, confirmed at Wednesday opening.
  No actual total session duration was measured.

### Tuesday — Grouped Learning Review

- Furkan explained factory-based configuration, monkeypatch restoration, integration
  of settings validation with application creation, exception-text redaction limits,
  dependency/configuration files, non-mutating format checks, and CI evidence scope.
- A new app instance supports isolation but does not automatically isolate shared
  globals, caches, databases, or external services. These require explicit ownership
  and cleanup. Module-level Settings captures configuration at initialization.
- In the current code, invalid settings fail inside create_app before a FastAPI
  instance is returned; this is before ASGI lifespan startup, not an exception raised
  by a lifespan startup handler. TestClient contexts separately exercise lifespan.
- uv.lock records resolved dependencies, hashes, and platform conditions for
  reproducible resolution; it cannot guarantee identical behavior across operating
  systems, architectures, environment values, or external services. .python-version
  is honored by supporting tools in the chosen workflow, not by every CI/tool
  automatically; pyproject.toml separately declares the supported Python range.
- monkeypatch restores changes made through that fixture, not arbitrary test side
  effects. Current secret-redaction evidence concerns str(ValidationError), not all
  structured error representations or logs.
- CI may support other automation, but this quality-check job must report formatting
  violations rather than silently modify its checkout. A green run proves only the
  selected checks; authentication and tenant data isolation remain unimplemented.

### Week 10 Next Actions

1. Commit/push the bootcamp evidence after the PostgreSQL infrastructure handoff;
   OpsDesk commit/push is verified as a91e2fd and grouped learning review is complete.
2. Remove the merged feature/week-10-postgresql-tests branch locally/remotely.
   PR #29 is merged and #6 is closed; main is synchronized at 3f85571.
3. Extend fast CI test selection in a bounded follow-up; the current job still
   runs only seven foundation tests. PostgreSQL CI remains #25.
4. Begin #7 only after the guarded-test handoff; preserve the Week 10 capacity plan.

## Week 10 Wednesday Opening — 16 September

- Confirmed clean working trees: bootcamp main at `5275f70` and OpsDesk
  feature/week-10-backend-foundation at `0bc43d5`, matching local tracking refs.
  Furkan's supplied Tuesday terminal evidence confirms the bootcamp closing push.
- Read-only GitHub checks confirm no PR for the foundation branch, open issues
  #1/#2/#5/#9, and successful hosted CI run 35004969487 for the current branch commit.
- First complete the agreed foundation PR review/merge and verify issue closure.
  Prepared an English PR description with acceptance evidence and closing keywords;
  Furkan will create and merge it. No PR creation or merge is claimed yet.
- Then begin #6 with database lifecycle reasoning, exact target guards, synchronous
  engine/session setup, and probe-table isolation that survives real commits.
  Allow 3-3.5 hours including the carried-over PR work and grouped daily closure.
  Database provisioning and destructive test operations have not started.

### Wednesday — Foundation PR Merged

- Furkan created PR #28, targeting main from feature/week-10-backend-foundation.
  Review confirmed the expected 16-file scope, closing links to #1/#2/#5/#9,
  no conflicts, and successful PR checks for head `0bc43d5`.
- Furkan merged PR #28 with a head-commit match and preserved commit history.
  Merge commit: `64b14eb515fcb49091c2b02e77bd85b1cdff40a8`. He switched to main
  and pulled with --ff-only; terminal evidence confirms clean synchronized main.
- Read-only GitHub verification confirms issues #1, #2, #5, and #9 are CLOSED.
  [Main CI run 35118215125](https://github.com/ozdemirr1/opsdesk/actions/runs/35118215125)
  passed for the merge commit. This is merged foundation evidence, not deployment.
- Feature-branch cleanup and the new #6 working branch remain Furkan's next Git steps.

### Wednesday — Test Target Guard and Dependency Warning

- Furkan deleted the merged foundation branch locally/remotely and created
  feature/week-10-postgresql-tests from clean main. He wrote validate_test_target
  and six unit tests covering the exact localhost IPv4/port/database target and
  rejected alternatives. Corrected a function-name typo and formatting; 13 tests pass.
  These unit tests do not yet prove integration with connection or cleanup code.
- Local PostgreSQL 18 is running and 127.0.0.1:5432 accepts connections. No database
  creation, schema changes, or destructive test operations have been performed.
- At Furkan's request, investigated the Starlette/AnyIO warning before proceeding.
  Installed Starlette 1.6.0 references anyio.abc.BlockingPortal; upstream main has
  changed to anyio.from_thread.BlockingPortal, but the published release checked
  on 16 September remains 1.6.0.
- Added a temporary pytest warning filter restricted to the exact message,
  DeprecationWarning category, and starlette.testclient module, with rationale and
  removal condition in README. No dependency downgrade, site-packages patch, or
  dependency version change. This filters known test output; it is not an upstream fix.
- Verification: 13 tests pass without warnings; Ruff lint/format and diff checks pass.
  A temporary warning-emission check confirms other messages, modules, and categories
  remain visible. Product changes are uncommitted; database configuration is next.


### Wednesday — Product Database Provisioning and Guarded Test Evidence

- Furkan chose new product database names to preserve the Month 02 application:
  opsdesk_product_dev and opsdesk_product_test on 127.0.0.1:5432. The older
  opsdesk_dev/opsdesk_test databases remain unchanged and are rejected by the new
  integration guard. The explicit decision supersedes earlier test-target names.
- Furkan provisioned separate non-superuser owners opsdesk_product_app and
  opsdesk_product_test_runner, set passwords interactively, and revoked PUBLIC
  database access. Read-only checks confirmed ownership and denied cross-access
  between the two new roles/databases. This does not establish server password
  authentication policy or isolation from every legacy database.
- Preserved fresh-install provisioning in scripts/postgresql/bootstrap_local.sql:
  preflight target/name checks, no stored passwords, no automatic drop/reset, and
  no business tables. The script was reviewed, not rerun on the provisioned server.
- Furkan implemented separate environment-based database settings, URL.create,
  synchronous engine/session factories, an exact test target guard, explicit caller
  commits, and Session closure. Added SQLAlchemy/psycopg dependencies and lock updates.
- Real PostgreSQL tests verify target identity, committed writes through independent
  Sessions, rollback of uncommitted writes, exception cleanup, and pool return.
  Probe isolation uses separate committed DELETE transactions before/after scopes;
  only public.integration_probe is touched. A final read-only check found zero
  remaining probe rows and no business tables in the new test database.
- Subprocess tests verify cleanup failure interrupts subsequent tests, including
  failures before the body and after it; ExceptionGroup retains body/cleanup errors.
  Tests run sequentially with one suite per database; no cross-process lock exists.
- Synthetic-secret checks cover connection/statement failures and cleanup reports.
  Pytest enhanced tracebacks exposed exception argument values despite from None.
  The reviewed --tb=native --no-showlocals policy retains standard tracebacks and
  exception groups. A temporary negative check without chain suppression still
  detected leakage. This is a bounded reporting policy, not universal log safety.
- Furkan's final terminal evidence: Ruff lint passes, 20 files formatted, 37 tests
  pass with six integration tests skipped by default; explicit integration opt-in
  passes all six against the product test database. These are local results.
  The existing hosted workflow still selects only the seven foundation tests.
- README now records provisioning, required DB settings, hidden password input,
  opt-in execution, transaction/cleanup ownership, and error-reporting limitations.
  Local B02/F01 scope amendments record the new target; publishing the amendment to
  GitHub remains Furkan's task. No issue closure, commit/push, PR, schema migration,
  or business endpoint completion is claimed for this infrastructure work yet.
- Grouped Wednesday learning review subsequently completed, with corrections below.
  Git closure remains pending; no actual total session duration was measured.


### Wednesday — Grouped Learning Review

- Furkan explained explicit transaction ownership, separate-session verification,
  independent cleanup transactions, paired body/cleanup errors, stopping after
  cleanup failure, and the limits of exception-chain suppression.
- Exact database/host/port allowlisting rejects mismatching configured targets;
  it is not absolute server authentication or proof of isolation. Local tunnels,
  server replacement, privileges, and overlapping runs remain separate concerns.
- Caller-owned commits are this project's explicit policy. Correctly scoped
  commit-on-success context managers can also be valid; automatic commit is not
  inherently unsafe. Session closure rolls back unfinished transactional work,
  not previously committed data or external side effects.
- A Session is not a general query-result cache. Our probe uses SQL text, which
  executes against PostgreSQL even in the same Session. The key reason for the
  independent read is that a transaction can see its own uncommitted writes.
  A fresh Session/transaction verifies visibility after commit and may reuse the
  same physical connection from the pool.
- A Python RuntimeError alone does not put PostgreSQL into the failed-transaction
  state. Database statement errors can do so. Closing test Sessions first and
  cleaning in a separate committed transaction separates cleanup from both normal
  and failed test transaction lifecycles; it cannot guarantee cleanup succeeds.
- Cleanup failure means isolation is uncertain, not necessarily that rows remain.
  Preserve both failures and stop later tests rather than trust that uncertain state.
- from None suppresses displayed implicit chaining; it does not erase exception
  context, redact the replacement message, or control custom logs/debug output.
- Staging revealed trailing whitespace in a newly added test's embedded source.
  Earlier unstaged diff checks did not cover untracked files. Removed only those
  three whitespace runs, checked Ruff, and Furkan re-staged the file. Final staged
  diff --check is clean; the existing 37+6 test evidence is unchanged.


### Wednesday — PostgreSQL Infrastructure Commit and Push

- Furkan committed the 21 reviewed OpsDesk files as `a91e2fd`
  (`week-10: establish guarded PostgreSQL test infrastructure`) and pushed
  feature/week-10-postgresql-tests with upstream tracking. Supplied terminal output
  and local inspection confirm a clean checkout synchronized with its tracking ref.
- Prepared an issue #6 target-amendment/evidence comment and PR description for
  Furkan to publish. Neither publication nor PR creation/merge is claimed yet.
  Issue #6 was verified OPEN before the commit; passing local tests do not close it.
- Hosted [Backend CI run 35140729238](https://github.com/ozdemirr1/opsdesk/actions/runs/35140729238)
  passed for full head a91e2fdc024557cd842e5d35baa512e64f78be00. This verifies
  the existing Ruff checks and seven foundation tests, not the expanded local suite.

- Furkan published the [#6 target amendment and evidence](https://github.com/ozdemirr1/opsdesk/issues/6#issuecomment-5703322462)
  and created [PR #29](https://github.com/ozdemirr1/opsdesk/pull/29).
  Read-only review confirms main as base, head a91e2fdc024557cd842e5d35baa512e64f78be00,
  recognized closing reference to #6, and CLEAN/MERGEABLE status.
  PR [CI run 35140889645](https://github.com/ozdemirr1/opsdesk/actions/runs/35140889645)
  passed. Merge and issue closure remain pending Furkan's action.


### Wednesday — PostgreSQL Infrastructure Merged

- Furkan merged PR #29 with the reviewed head-commit match, switched to main,
  and pulled with --ff-only. Merge commit: 3f855717bfe0b893e46e107fa1b43151b3262e94.
- Supplied GitHub CLI output confirms #6 CLOSED at 2026-09-16T19:30:43Z.
  Terminal evidence confirms clean main synchronized with origin/main; local
  inspection also confirms the merge commit and clean working tree.
- The #6 target amendment and evidence are published. Branch cleanup and the
  bootcamp closing commit/push remain the final housekeeping steps. Main-branch
  post-merge CI has not been independently checked in this closing entry; the
  recorded successful push/PR checks concern the reviewed feature head.
- Next scheduled product work is #7 identity/Organization schema, with a bounded
  fast-CI selection follow-up still tracked. No schema implementation is claimed.

## Week 10 Thursday Opening and Monthly Review — 17 September

- Furkan's Wednesday closing output confirms deletion of the merged PostgreSQL
  feature branch locally/remotely and bootcamp commit/push ec55874 on clean,
  synchronized main. OpsDesk's verified handoff remains merged PR #29 / 3f85571
  and closed issue #6.
- At Furkan's request, recorded the external September market research in
  monthly-reports/2026-09-market-review.md and checked its cited claim families
  against publisher/official sources. Preserved sampling and verification limits;
  this is not a fresh labor-market census or proof of individual job prospects.
- Updated ROADMAP.md, README.md, and Decision 015: retain backend/product focus,
  start AI evals in Month 06, extend them through RAG, and keep later agent/MCP
  work bounded. Official sources confirm Agents API public beta and the announced
  DVA-C03 update; neither creates an immediate implementation/certification task.
- React/TypeScript, security, and testing were already planned. Docker/Redis stay
  Month 05; current persistence stays synchronous. A bounded async HTTP exercise
  follows lifecycle understanding. Junior/internship applications remain appropriate.
- The supplied October beginner checklist does not reset completed FastAPI and
  PostgreSQL work. Today's next technical task remains #7 schema/Alembic; the
  monthly review introduced no code, migrations, or completed feature claims.
- Roadmap review documentation is prepared for Furkan's review/commit; it has not
  been committed or pushed by the assistant.


## Week 10 Thursday Work and Friday Carry-over — 17–18 September

- On feature/week-10-identity-schema, Furkan implemented Alembic configuration,
  separate SQLAlchemy persistence models, and revision 6a3066cd5538 for Users,
  Organizations, and Memberships. Online migrations use the exact guarded product
  test target; offline SQL generation requires no credentials or connection.
- Reviewed the Organization-name subset of #3 needed by #7. Remaining #3 decisions
  and endpoint implementation are still open. Schema checks do not replace request
  normalization, authorization, or coordinated ownership-transfer rules.
- Thursday's work exceeded the mentoring estimate and was not committed/pushed.
  Friday resumed the remaining acceptance work in batches rather than treating #7
  as complete. Same-file tests are now grouped and explained together; completion
  estimates are updated at package boundaries. No measured Thursday active-work
  total is claimed.
- Corrected the mentor-supplied expected SQLSTATE for RESTRICT deletion to 23001;
  missing-parent inserts retain 23503. Constraint tests verify unchanged persisted
  state after rejected writes using fresh sessions.
- Identity cleanup uses a revision-checked fixed DELETE allowlist. Subprocess tests
  verify stopping after initial/final cleanup failure, both body/cleanup errors,
  synthetic-secret masking under the documented traceback policy, and rejection of
  an unexpected revision before DELETE.
- Separate schema tests require empty identity tables, expected role/server/revision,
  and no unexpected public tables. Both the ordinary downgrade/re-upgrade cycle and
  restoration after an injected post-downgrade test error passed. Restoration-failure
  stopping/error preservation was code-reviewed; no live restoration failure was
  intentionally induced. Forceful termination and concurrent suites remain unsupported.
- Furkan's 18 September terminal evidence: 2 schema tests passed, followed by all
  60 PostgreSQL data tests. Final local review: Ruff passes, 34 Python files already
  formatted, and 51 non-database tests pass with 62 database/schema tests skipped.
- README now documents the implemented schema, fresh migration setup, separate
  schema/data test commands, and cleanup boundaries. Existing hosted CI still runs
  only seven foundation tests; expanded fast-test CI and PostgreSQL CI are not claimed.
- GitHub #7 was verified OPEN and no PR existed for this branch at closing review.
  Product commit/push, PR creation/checks/merge, issue closure, and the bootcamp
  commit remain pending Furkan's terminal evidence. Friday's new feature work has
  not started; finish this handoff before continuing #3/#10.

### Friday — Identity Schema Published for Review

- Furkan committed the 26 reviewed product files as
  `6bf2ff1139436e2c420e32b0cf62af810699c04c` and pushed
  `feature/week-10-identity-schema`. Local checkout is clean and the supplied
  terminal output confirms upstream synchronization.
- Created [PR #30](https://github.com/ozdemirr1/opsdesk/pull/30). GitHub confirms
  the expected head, main base, mergeability, and a recognized closing reference
  to #7. At first inspection both hosted checks were running; merge and issue
  closure remain pending.
- Both hosted push/PR checks subsequently passed for the same full head; PR status
  is CLEAN. Runs: [35376542747](https://github.com/ozdemirr1/opsdesk/actions/runs/35376542747)
  and [35376547766](https://github.com/ozdemirr1/opsdesk/actions/runs/35376547766).
  These runs cover the existing workflow, not the local PostgreSQL suites.


### Friday — Identity Schema Merged and Branch Cleaned

- Furkan merged PR #30 with the verified head-commit match. Merge commit:
  `d5147fe25da43736e7ce9778d65852dd142175d3`.
- Supplied GitHub output confirms #7 CLOSED at 2026-09-18T17:51:13Z.
  Furkan switched to main, pulled with --ff-only, and deleted the feature branch
  locally and remotely. Local inspection confirms the merge commit and clean main;
  supplied terminal output confirms synchronization with origin/main.
- Product #7 handoff is complete. The September market review and Week 10 evidence
  remain to be committed/pushed in this bootcamp repository. No new Friday feature
  work or post-merge main CI result is claimed in this entry.
- Friday carry-over resumed around 20:24 Istanbul time; merge evidence arrived at
  20:51 (about 27 minutes elapsed, not a measurement of uninterrupted active work).
  Proceed to the bounded #3/#10 contract/error work after the bootcamp commit.


## Friday — Shared Error Contract and First Implementation Slice

- Furkan committed/pushed the September review and schema handoff as 16b4f09;
  supplied terminal evidence confirms clean synchronized bootcamp main.
- Began feature/week-10-api-errors after #7 closure. Reviewed the #3 subset needed
  for #10: fixed error envelope/messages, safe field paths, transport errors,
  protocol headers, server-generated request IDs, and bounded request diagnostics.
  Remaining #3 feature contracts and business-failure precedence stay open.
- Implemented an ApiError catalog, fixed-message JSON response helper, and factory
  handler registration. The public response has code/message/details; bearer 401
  retains WWW-Authenticate. Test-only routes do not add product endpoints.
- Supplied terminal evidence: Ruff fixes/formatting completed and 23 focused tests
  passed (16 API-error cases plus 7 existing application/configuration cases).
  Code review confirms the factory wiring and no raw exception-cause serialization.
- Catalog entries for validation/JSON/media/framework/500 errors do not mean those
  errors are automatically handled yet. Only explicitly raised ApiError is mapped.
  Request IDs, safe request logging, and runtime access-log configuration are pending.
- Learning corrections: route templates and controlled messages reduce disclosure
  risk but do not secure every logger; 422 covers input validation, 409 business
  state conflict, and 403 authorization. A 500 does not prove prior input validity.
- Ended the session at Furkan's request. Preserve this passing slice with an interim
  feature-branch commit/push; do not merge or close #10. #3 also remains open.
  Product and bootcamp checkpoint commits are pending terminal evidence.

### Next Session — Resume Before Adding New Features

1. Verify checkpoint commits and continue feature/week-10-api-errors.
2. Implement validation/transport and framework mappings with safe field details,
   malformed JSON/media-type cases, and required response headers.
3. Implement unexpected-error handling with request ID and bounded safe diagnostics;
   check runtime access logs as well as application logs and startup reporting.
4. Run grouped tests, update documentation, then review #10 acceptance before PR
   merge/closure. Keep remaining #3/#4 work explicit; registration is not yet ready.


## Monday Carry-over — 21 September 2026

- Friday checkpoints were pushed: OpsDesk c8fbcfe and bootcamp 36109bc, both clean
  at Monday opening. Continue feature/week-10-api-errors; no work is claimed for
  the intervening weekend. Calendar Week 11 begins while Week 10 carry-over closes.
- Agreed a two-day capacity plan of about 6–8 active hours for remaining mandatory
  Week 10 work and review. Registration was capacity-dependent, not a completed or
  mandatory Week 10 deliverable; remaining #3/#4 prerequisites remain explicit.
- Furkan implemented JSON media/syntax gates, safe validation paths/messages,
  framework error mapping, request-ID middleware, and bounded safe diagnostics.
  Corrected a mentor-supplied FastAPI compatibility assumption: ModelField's model
  annotation is accessed through field_info.annotation, not type_.
- Tests progressed to 45, then 57 focused passes. Full non-integration selection
  passed 101 tests with 62 database/schema tests deselected. Ruff passes and 41
  Python files are formatted. Workflow now selects this broader non-database suite
  and includes migrations in lint/format checks; hosted results are still pending.
- Actual Uvicorn request verification with synthetic path/query/Authorization/ID
  markers returned safe 404 and a new UUID. Supplied JSON log matched the response
  ID, used <unmatched>, and excluded the markers. Startup alone was not treated as
  evidence of request-log safety. Runtime startup used --no-access-log.
- README/contract reflect implementation limits: top-level safe field projection,
  bounded details/log metadata, separately configured routers, and no replacement
  response after headers have started. Generic errors are not mapped to business
  conflicts. Existing startup-validation tests remain in the passing suite.
- Prepared #10 PR description. Product commit/push, hosted CI, merge/issue closure,
  Week 10 report, and Week 11 detailed plan remain pending. Do not close #3/#4 or
  claim business endpoints on the strength of these shared infrastructure tests.


### Monday — Shared Errors and Diagnostics Merged

- Furkan committed/pushed completion as 842614d74e1af9ef065ee82ed9fb0b4d3babaa91
  and created [PR #31](https://github.com/ozdemirr1/opsdesk/pull/31). Read-only review
  confirmed main base, the expected head, mergeability, and the #10 closing reference.
- Both expanded hosted CI checks passed for that head:
  [push run 35614549302](https://github.com/ozdemirr1/opsdesk/actions/runs/35614549302)
  and [PR run 35614554549](https://github.com/ozdemirr1/opsdesk/actions/runs/35614554549).
  Workflow selection now covers non-integration tests, with migrations included in
  Ruff checks. These runs do not establish PostgreSQL CI.
- Furkan merged with the reviewed head match. Merge commit:
  c07a48f68f7fdc4b9e6949652a25aa692d85cb18. Supplied output confirms #10 CLOSED at
  2026-09-21T14:49:09Z. Main was pulled with --ff-only and the feature branch deleted
  locally/remotely. Local inspection confirms clean main at that merge commit;
  supplied terminal output confirms upstream synchronization.
- The resumed implementation began around 17:13 Istanbul and merge completed at
  17:49, about 36 minutes elapsed, not uninterrupted active-time measurement.
- #10 is complete. #3/#4 remaining decisions, grouped learning review, Week 10 report,
  and a capacity-bounded Week 11 plan remain. Registration/login/current-user features
  are not claimed complete. Bootcamp evidence changes are not yet committed/pushed.


### Monday — Grouped Error/Diagnostics Learning Review

- Furkan correctly distinguished a known email conflict from infrastructure errors:
  mapping all persistence failures to 409 would mislead clients and hide operational
  failures. OperationalError covers several driver/database conditions; this project's
  currently unmapped operational failures use generic 500, not a universal taxonomy.
- Explained server-issued X-Request-ID correlation and route-template grouping.
  UUIDs are correlation identifiers, not authorization credentials. Templates avoid
  raw path values in this logger but do not eliminate every disclosure path or create
  a metrics/monitoring system by themselves.
- Explained why an already-started final response cannot be replaced with a new
  500 JSON response. Precision: our flag records the ASGI response-start attempt,
  not proof of client receipt. unexpected_error=true with status 200 can indicate a
  partial response or a later failure after the body; it does not prove database
  data loss, rollback, or even a failed business commit. Informational HTTP responses
  are outside this simplified final-response explanation.
- Grouped #10 learning review is complete; no additional code/tests are required
  solely for these wording corrections. Continue the bounded #4 design review.


### Tuesday — Accepted concurrency design recorded

- Recorded Furkan's acceptance of the Organization coordination protocol in OpsDesk
  docs/concurrency-contract.md and aligned the API, logging, access-control, relational
  model, README and D04 references. The decision includes ordered locks, fresh reads,
  owner-transfer flush ordering, 2-second per-lock waits, fixed 503 concurrency_busy,
  full rollback, and no automatic transaction retries.
- This is accepted design, not executable feature evidence. Contention mapping,
  lock-wait measurements and controlled concurrent business tests remain future work.
  Global User lifecycle coordination remains a gate before its deferred endpoint.
- No new tests were needed for these documentation changes; GitHub publication and
  #4 closure remain pending. Remaining #3 choices are not claimed resolved.


### Tuesday — Concurrency merge and remaining-contract handoff

- PR #32 merged as 9bf8726d96bcb13fb69ddee5ddc37bb306616be8; user output confirms
  #4 CLOSED at 2026-09-22T13:57:11Z, main synchronization and branch cleanup.
  Local inspection confirms clean main at that merge. Pre-merge push/PR CI passed
  for 00a7ea8a10697f51f6a87973616150916a2e0728; no concurrency execution is claimed.
- Completed the D03 inventory in [Week 10 handoff](weekly-reports/week-10-plan.md#d03-remaining-prerequisite-inventory):
  inputs, collections/filters, response structures, repeated requests/precedence,
  timestamps and Attachment migration timing. Each group maps to dependent work.
- D03 remains open; independent #11/#12/#13 work is not blocked by unrelated
  Organization/Comment decisions. Weekly report, realistic Week 11 plan and original
  career action remain; documentation changes have not yet been committed/pushed.


### Wednesday — Week 10 report and Week 11 scheduling

- Prepared Week 10 report with distinct historical test runs and merge evidence.
- Completed two career-target investigations and one unsent English enquiry; see
  [career research](weekly-reports/week-10-career-targets.md). Roles and availability
  limitations are explicit; no outreach/application was performed.
- Planned 15–18 active hours over 23–27 September for the bounded identity slice,
  including tests, review and Git work; registration is the fallback completion floor.
- Report, handoff and career research are ready. Bootcamp commit/push remains pending
  user execution; no new product implementation or test run is claimed this session.


### Wednesday — Fixed combined completion scope

- Furkan requested completion of Week 10 carry-over and Week 11 within 23–27
  September, prioritizing completion over the previous hours budget.
- Revised plan includes all six D03 decision groups, Week 10 Git publication,
  registration/login/current-user implementation and Week 11 closure. Estimate:
  25–32 active hours including a Sunday correction buffer, not a guarantee.
- Supersedes the earlier 15–18-hour plan and registration-only fallback. No planned
  transfer of this fixed scope to Week 12; blockers must be surfaced early and no
  tests or acceptance gates are waived. Remaining Month 03 product features are
  distinct backlog work, not silently claimed delivered by this identity slice.


### Late Wednesday — Git-only closing session

- At 23:19 reported local time, Furkan requested only Week 10 Git closure tonight.
- Wednesday's D03 fields/responses and registration schemas/hash work are reassigned
  across 24–27 September. No technical work from that block is claimed completed.
- Revised four-day estimate is 24–31 active hours with unchanged #3/#11/#12/#13
  completion scope and Sunday closure target; no planned Week 12 transfer.
- Bootcamp publication remains pending user command output. Stop after Git closure.
