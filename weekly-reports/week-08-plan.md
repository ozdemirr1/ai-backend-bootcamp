# Week 08 Plan

## Date

31 August - 6 September 2026

## Main Focus

- User identity and registration
- Secure password hashing and verification
- Login credentials and generic authentication failures
- JWT access-token creation and validation
- Current-user dependency
- Protected Ticket endpoints
- Ticket ownership and object-level authorization
- Bounded role/function-level authorization
- Authentication and authorization tests

## Main Goal

Add a secure, testable identity boundary to the Month 02 Ticket API. A user
should be able to register, log in, retrieve their own identity, and manage only
the Tickets they are authorized to access.

Week 08 is not merely a JWT exercise. Authentication must establish who the
caller is; authorization must separately decide what that caller may do.

## Planned Request Flow

```text
register credentials
    |
    v
validate input --> hash password --> persist User

login credentials
    |
    v
find User --> verify password --> issue short-lived access token

Authorization: Bearer <token>
    |
    v
decode fixed algorithm --> validate claims --> load active User
    |
    v
current-user dependency
    |
    +----> ownership check for one Ticket
    |
    +----> role/function check for privileged operation
```

## Architecture Rules

- Authentication and authorization are separate decisions.
- Plaintext passwords must never be stored, logged, or returned.
- Password hashing must use a maintained password-hashing library and a
  password-specific algorithm; do not implement cryptography manually.
- JWT validation must use an explicitly configured algorithm and secret.
- Tokens must contain only minimal claims and must never contain passwords or
  sensitive user records.
- A valid token does not automatically authorize access to every Ticket.
- Object-level checks must protect resources addressed by identifiers.
- Function/role checks must protect privileged operations explicitly.
- Routes must not query SQLAlchemy models directly.
- User and Ticket workflows must retain service and repository boundaries.
- Alembic migrations must own User and Ticket-ownership schema changes.
- Authentication secrets must come from ignored environment configuration.

## Scope Decisions to Make on Monday

- Choose the minimal User identifier and login field after architecture review.
- Define normalization and uniqueness behavior before writing the migration.
- Define the smallest useful role set for this learning API.
- Decide whether unauthorized access to another user's Ticket returns `403` or
  hides existence with `404`, then apply the rule consistently.
- Define short access-token lifetime and required claims.
- Study refresh-token responsibilities, but implement refresh tokens only if
  the access-token and authorization foundation is complete and reviewed.

## Daily Plan

### Monday - Security Model and Password Foundation

- Explain authentication, authorization, sessions, bearer tokens, and JWT.
- Threat-model registration, login, token theft, password storage, and IDOR.
- Review the existing application boundaries before adding files.
- Verify current compatible security dependencies from primary documentation.
- Add environment-based JWT configuration without tracked secrets.
- Add focused password hashing and verification functions with unit tests.
- Document why passwords are hashed rather than encrypted.

#### Monday Outcome

- Completed the authentication/authorization threat model before adding code.
- Added and verified `pwdlib[argon2]` and PyJWT dependencies.
- Added an Argon2id-backed `PasswordHasher` boundary with five focused tests.
- Added required secret-aware JWT configuration and a bounded 30-minute
  default access-token lifetime with focused validation tests.
- Used only synthetic JWT secrets in tracked tests and documentation.
- Kept integration fixtures independent of a developer's real JWT secret.
- Passed `150` tests with `19` integration skips and all `169` tests with the
  guarded PostgreSQL integration suite enabled.

### Tuesday - User Persistence and Migration

- Design the minimal User domain and persistence representations.
- Add a User repository boundary and SQLAlchemy implementation.
- Add User schema constraints and normalized unique identity behavior.
- Add Ticket ownership through an explicit foreign key.
- Generate and manually review the Alembic migration.
- Verify upgrade, downgrade, re-upgrade, and `alembic check` on the isolated
  migration database.
- Add mapper and repository tests.

#### Tuesday Outcome

- Chose a database-generated, stable `user_id` as the ownership and future JWT
  subject identity instead of a mutable email address.
- Defined `member` and `admin` as the smallest current role set; ordinary
  registration has no client-controlled role field.
- Added `email-validator` 2.3.0 and a single domain normalization boundary with
  deterministic syntax checks and no DNS dependency.
- Added `NewUser`, `User`, and `UserRole` domain types with focused validation
  tests.
- Added a constrained SQLAlchemy `UserRecord` with a normalized unique email,
  safe database defaults, and timestamps.
- Added explicit `NewUser`/`UserRecord`/`User` mapper functions. Registration
  mapping deliberately leaves role and active-state assignment to trusted
  server defaults.
- Passed Ruff, diff checks, and 29 focused User, persistence-model, and mapper
  tests.
- Stopped before repository, Ticket ownership, and migration work. These
  database-sensitive tasks move to Wednesday rather than being rushed.

### Wednesday - Persistence Completion and Registration Start

- Add the User repository protocol and SQLAlchemy implementation, including
  lookup by normalized email and database-generated defaults. Estimated:
  60-90 minutes.
- Add nullable Ticket `owner_id` metadata and its User foreign key as the
  expand phase for existing Tickets. Estimated: 35-50 minutes.
- Generate and manually review the User/ownership Alembic revision. Estimated:
  45-60 minutes.
- Verify upgrade, downgrade, re-upgrade, and `alembic check` only against
  `opsdesk_migration_dev`. Estimated: 45-60 minutes.
- Add repository integration tests and run the complete quality gates.
  Estimated: 40-60 minutes.
- If the persistence boundary is complete and energy remains, begin the strict
  registration request/response contracts. This is a stretch task, not a
  reason to weaken migration review. Estimated: 45-60 minutes.

#### Wednesday Outcome

- Completed the User repository protocol and both in-memory and SQLAlchemy
  implementations with normalized lookup and duplicate conflict translation.
- Added nullable Ticket ownership metadata, its restrictive User foreign key,
  the ownership listing index, and mapper ownership invariants.
- Generated and reviewed revision `e98825c4d6b6`, then proved upgrade,
  downgrade, legacy-row preservation, re-upgrade, and zero metadata drift on
  the isolated migration database.
- Upgraded guarded `opsdesk_test` and added real PostgreSQL User repository
  coverage while preserving caller-owned transactions and empty test tables.
- Completed the stretch registration slice: strict request/public response
  contracts, injected hashing capability, registration service, dependency
  composition, and `POST /auth/register`.
- Proved successful commit, Argon2id-only persistence, safe response fields,
  normalized duplicate conflict handling, rollback, and exact cleanup through
  the real HTTP/Session/PostgreSQL stack.
- Passed dependency, lint, formatting, migration, and diff gates; passed `205`
  tests with `27` integration skips and all `232` guarded database tests.

### Thursday - Login, JWT, and Current User

- Add a login workflow with generic invalid-credential responses.
- Issue a short-lived JWT access token with minimal claims.
- Decode tokens with a fixed configured algorithm.
- Reject malformed, tampered, expired, or unsupported tokens.
- Load the current active User from persistent storage.
- Add `GET /users/me` and test missing, invalid, and valid credentials.

#### Thursday Outcome

- Added strict login request and bearer token response contracts without
  exposing role selection or password-derived data.
- Added an injectable UTC `Clock` boundary and a production `SystemClock` so
  token issuance can be deterministic in unit tests.
- Implemented HS256 access-token creation and decoding with minimal `sub`,
  `iat`, and `exp` claims, fixed server-selected algorithm validation, and a
  positive configured lifetime.
- Added focused rejection coverage for malformed identities, missing claims,
  expired tokens, wrong secrets, unsupported algorithms, and modified
  signatures. The signature test mutates meaningful Base64URL data instead of
  relying on unused final padding bits.
- Added an `AuthenticationService` behind narrow password-verification and
  token-issuing protocols. Successful login issues a token for the immutable
  `user_id`; missing, incorrect, and inactive identities share one generic
  failure contract.
- Added a dummy-hash path to the service contract so a missing account can
  still perform password-verification work and reduce timing-based account
  enumeration. Production dummy-hash composition remains Friday work.
- Passed dependency, Ruff, formatting, diff, fast-test, and guarded database
  gates: `235 passed, 27 skipped` without database tests and all `262` tests
  with them enabled. `opsdesk_test` finished with zero Users and Tickets at
  Alembic revision `e98825c4d6b6`.
- Stopped before dependency composition and HTTP endpoints by choice. Those
  tasks move to a longer Friday session rather than being rushed.

### Friday - Complete Login, Current User, and Begin Ticket Authorization

- Add a cached, real Argon2id dummy hash and compose the production
  authentication service. Estimated: 30-45 minutes.
- Add `POST /auth/login`, generic `401` mapping, fast HTTP tests, and guarded
  PostgreSQL login verification. Estimated: 60-90 minutes.
- Add bearer-token extraction, token decoding, persisted active-User loading,
  and consistent authentication failures. Estimated: 75-100 minutes.
- Add `GET /users/me` with missing, malformed, expired, unknown-User, inactive-
  User, and valid-token tests. Estimated: 60-90 minutes.
- If the authentication boundary is complete and reviewed, begin requiring
  authentication for Ticket operations and derive new Ticket ownership from
  the current User. Estimated: 90-120 minutes; this is a stretch block.
- Preserve the remaining Ticket listing/detail/update/delete ownership and
  horizontal-access tests for Saturday if the security review needs more
  time.

#### Friday Outcome

- Generated and process-cached a valid Argon2id dummy hash, then composed the
  production authentication service from the real repository, verifier,
  configured JWT manager, and UTC clock.
- Added JSON `POST /auth/login` with uniform `401` behavior and verified real
  PostgreSQL plus Argon2 registration-to-login flow.
- Added HTTP Bearer extraction and current active-User resolution. Tokens for
  deleted or deactivated Users are rejected because current database state is
  checked on every protected request.
- Added `GET /users/me` and covered missing headers, wrong schemes, malformed
  and expired JWTs, unknown Users, inactive Users, and valid identities.
- Completed the stretch block for protected Ticket creation: ownership is
  derived from the current User, client-supplied `owner_id` is rejected, and
  PostgreSQL integration tests prove the owner is persisted.
- Preserved Ticket collection/detail/update/delete object authorization for
  Saturday rather than treating authentication as implicit authorization.
- Passed dependency, Ruff, formatting, diff, fast-test, and guarded database
  gates: `255 passed, 33 skipped` without database tests and all `288` tests
  with database tests enabled.

### Saturday - Role Authorization and Complete Verification

- Add the smallest justified privileged role/function check.
- Keep role authorization separate from Ticket ownership checks.
- Verify ordinary users cannot call privileged operations.
- Verify authorized roles can perform only the intended operation.
- Run the complete dependency, Ruff, migration, and test suite.
- Review diffs for secrets, password hashes, token examples, and authorization
  bypasses.
- Add minimal CI only if the authentication foundation and its tests are
  complete; do not let CI or deployment dilute security work.

### Sunday - Review and Transition

- Answer authentication, JWT, password, ownership, and authorization interview
  questions.
- Write the Week 08 report.
- Review and merge the Week 08 pull request only after the security definition
  of done is satisfied.
- Assess readiness for the first backend deployment without exposing secrets
  or starting Month 3 product work prematurely.
- Prepare Week 09 OpsDesk domain design.

## Planned API Surface

The exact contracts will be finalized after Monday's architecture review.
Expected additions are:

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/auth/register` | Create a User with a hashed password |
| `POST` | `/auth/login` | Verify credentials and return an access token |
| `GET` | `/users/me` | Return the authenticated User's public identity |
| `GET` | `/tickets` | Return only Tickets visible to the caller |
| `POST` | `/tickets` | Create a Ticket owned by the caller |

Existing detail, update, and delete Ticket endpoints will receive ownership
checks instead of parallel duplicate routes.

## Test Plan

### Password and Token Tests

- Stored password value is not equal to the submitted password.
- Correct password verifies and incorrect password fails.
- Password or hash never appears in User responses.
- JWT contains only intended claims.
- Missing bearer credentials return `401`.
- Malformed, tampered, expired, and unsupported tokens return `401`.
- Login failure does not reveal whether the user exists.

### Registration and Login Tests

- Valid registration creates one User.
- Invalid registration reaches no repository write.
- Duplicate identity returns the chosen conflict contract.
- Valid login returns the token response contract.
- Invalid identity and invalid password use the same public error.
- Transaction failures leave no partial User state.

### Authorization Tests

- Authenticated User A can create and access User A's Ticket.
- User B cannot read, update, or delete User A's Ticket by changing its ID.
- Ticket listing does not expose another user's Tickets.
- Client input cannot assign ownership to another User.
- Ordinary users cannot call privileged functions.
- The intended role can call only the explicitly permitted function.
- Authorization failure leaves database state unchanged.

### Regression and Isolation Tests

- Existing domain invariants remain protected.
- Fast tests remain independent of PostgreSQL when intentionally overridden.
- PostgreSQL tests run only against `opsdesk_test`.
- Migration tests run only against the isolated migration database.
- Each integration test removes only its own committed records.
- Final test database state is predictable and empty where required.

## Interview Questions

- What is the difference between authentication and authorization?
- Why are passwords hashed rather than encrypted?
- What properties should a password-hashing algorithm provide?
- What are salt and work factor?
- What are the three encoded sections of a JWT?
- Is a signed JWT encrypted?
- What should and should not be stored in JWT claims?
- What do `sub`, `exp`, `iat`, and `jti` represent?
- What is the difference between an access token and a refresh token?
- Why must the decoding algorithm be fixed by server configuration?
- What is the difference between `401` and `403`?
- What is object-level authorization and how does IDOR/BOLA occur?
- Why is a valid token insufficient for Ticket access?
- Where should Ticket ownership be enforced?
- How can role checks remain testable and independent of route code?

## Likely Commit Themes

- `week-08: add password and token configuration foundation`
- `week-08: add user persistence and ownership migration`
- `week-08: add user registration workflow`
- `week-08: add JWT login and current user dependency`
- `week-08: protect ticket ownership boundaries`
- `week-08: add role authorization and security tests`

Commit messages will follow actual completed boundaries rather than a fixed
quota.

## Definition of Done

Week 08 is complete when:

- Passwords are securely hashed and never stored or returned in plaintext.
- Registration and login use explicit application and persistence boundaries.
- Access tokens are short-lived, minimally scoped, and safely validated.
- `GET /users/me` resolves a persisted active User.
- Ticket creation derives ownership from the authenticated User.
- Collection and object endpoints enforce ownership consistently.
- At least one bounded role/function-level check is implemented and tested.
- Horizontal-access attempts are denied and leave state unchanged.
- Alembic owns User and ownership schema evolution.
- Authentication secrets and complete token values are absent from Git.
- Fast, integration, migration, lint, formatting, and dependency checks pass.
- The Week 08 architecture can be explained in the interview review.
- The reviewed feature branch is merged through a pull request.

## Guardrails

- Do not implement password hashing or JWT cryptography manually.
- Do not store plaintext passwords, access tokens, or JWT secrets.
- Do not print credentials or complete tokens in tests, logs, screenshots, or
  documentation.
- Do not place sensitive user data in JWT claims.
- Do not trust an algorithm selected only from an unverified token header.
- Do not accept an ordinary client's requested Ticket owner.
- Do not treat authentication as authorization.
- Do not rely only on hidden UI controls; enforce authorization in the backend.
- Do not run destructive tests against `opsdesk_dev`.
- Do not add OAuth providers, refresh-token rotation, password reset, MFA, or
  account recovery before the core access-token workflow is complete.
- Do not start Docker, Redis, background jobs, React, or AI features early.
