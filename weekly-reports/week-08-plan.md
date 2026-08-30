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

### Tuesday - User Persistence and Migration

- Design the minimal User domain and persistence representations.
- Add a User repository boundary and SQLAlchemy implementation.
- Add User schema constraints and normalized unique identity behavior.
- Add Ticket ownership through an explicit foreign key.
- Generate and manually review the Alembic migration.
- Verify upgrade, downgrade, re-upgrade, and `alembic check` on the isolated
  migration database.
- Add mapper and repository tests.

### Wednesday - Registration

- Add a strict registration request contract.
- Reject malformed and extra input before persistence.
- Hash the password before creating the persistence record.
- Prevent plaintext or hash values from entering the response model.
- Translate duplicate identity into a stable application and HTTP conflict.
- Add unit, service, HTTP, and PostgreSQL integration tests.

### Thursday - Login, JWT, and Current User

- Add a login workflow with generic invalid-credential responses.
- Issue a short-lived JWT access token with minimal claims.
- Decode tokens with a fixed configured algorithm.
- Reject malformed, tampered, expired, or unsupported tokens.
- Load the current active User from persistent storage.
- Add `GET /users/me` and test missing, invalid, and valid credentials.

### Friday - Ticket Ownership and Object Authorization

- Require authentication for Ticket operations.
- Assign newly created Tickets to the current User on the server.
- Never accept a client-selected owner during ordinary Ticket creation.
- Filter collection results to authorized Tickets.
- Protect detail, update, and delete operations with ownership checks.
- Add horizontal-access tests proving one user cannot access another user's
  Ticket by changing the URL identifier.

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
