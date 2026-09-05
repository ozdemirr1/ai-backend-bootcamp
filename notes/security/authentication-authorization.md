# Authentication and Authorization

## Purpose

These notes record the Week 08 security model for the Month 02 Ticket API.
They describe the implemented password, User persistence, Ticket ownership
expand phase, registration boundaries, JWT implementation, and login-service
contract. Production login composition, current-user resolution, and
authorization remain later steps.

## Authentication and Authorization Are Different Decisions

Authentication answers: "Who is making this request?"

Authorization answers: "May this authenticated caller perform this action on
this resource?"

A valid bearer token can establish a user identity, but it does not authorize
that user to read or modify every Ticket. Identified resources still require
an object-level ownership decision, and privileged functions require an
explicit role or permission decision.

## Threats Considered Before Implementation

- A database leak must not expose plaintext passwords.
- A missing user and an incorrect password must not produce distinguishable
  public login failures that enable account enumeration.
- A stolen bearer token lets its holder act as the represented user until the
  token expires, so access tokens must be short-lived and never logged.
- A JWT payload is readable; signing detects tampering but does not encrypt
  claims.
- Changing `/tickets/{ticket_id}` must not let one authenticated user access
  another user's Ticket. This is an IDOR/BOLA risk.
- Supplying an elevated role in client input must not grant privilege. Roles
  and ownership must come from trusted server state.

## Password Hashing

Password hashing is one-way. The application stores an encoded Argon2id value,
not plaintext and not reversible encrypted text. During login, verification
does not recover the original password. It reads the algorithm parameters and
salt from the stored encoding, hashes the submitted password under those
conditions, and compares the result.

Argon2id is designed to consume configurable time and memory. This makes
large-scale guessing more expensive than using a fast general-purpose digest
such as SHA-256 directly. A unique random salt produces different stored
values for identical passwords and defeats reusable precomputed hash tables.
The salt is not a secret; it is stored with the encoded hash.

`ticket_api.passwords.PasswordHasher` contains the pwdlib dependency. This is
a local library boundary: higher layers ask to hash or verify without knowing
pwdlib's construction or method details. `RegistrationService` depends on the
smaller injected `PasswordHashing` protocol, so fast service tests can use a
recording fake without invoking Argon2 while production composition supplies
the maintained pwdlib-backed implementation.

## Password Behavior Proven on Monday

- A generated hash is different from the plaintext password.
- The correct password verifies successfully.
- An incorrect password fails verification.
- Repeated hashing of the same password produces distinct salted values.
- Both distinct values still verify against the original password.
- The selected encoded format identifies Argon2id.

Password policy is a separate concern. Minimum length, maximum length, and
request validation belong to registration input/domain rules rather than the
low-level hashing utility.

## JWT Configuration Foundation

JWT is a compact signed representation of claims. It is not encrypted. A
client may read the header and payload, but changing either invalidates the
signature unless the attacker knows the signing secret.

`JWT_SECRET` is required environment configuration. `SecretStr` masks it in
ordinary Pydantic representations but does not encrypt it or prevent explicit
access. The value must therefore remain outside source code, logs, responses,
screenshots, and documentation.

The minimum-length validation catches obvious short placeholders. It cannot
measure entropy: a repeated or predictable 32-character value is still weak.
A real local value should be generated with a cryptographically secure random
generator. `.env.example` deliberately contains a short invalid placeholder
so an unchanged copy fails rather than silently using a shared secret.

Access-token lifetime defaults to 30 minutes and is constrained to 1 through
1,440 minutes. The signing algorithm will be selected explicitly in code when
token issuance is implemented; it will not be trusted from an unverified token
header.

## Test Isolation

Configuration unit tests disable `.env` loading with `_env_file=None` and
prepare only synthetic environment values. A shared fixture establishes a
valid baseline, while missing/invalid tests remove or replace exactly one
field. This ensures failure comes from the behavior under test rather than an
unrelated missing setting.

PostgreSQL integration fixtures also provide a synthetic JWT secret. They read
the local database URL only to derive the guarded `opsdesk_test` connection;
they do not need or reveal the developer's real JWT secret.

## User Identity and Email Normalization

The durable User identity is the database-generated `user_id`. Email is a
login identifier and may change, so it is not used as a Ticket foreign key or
as the long-lived identity represented by a future JWT `sub` claim.

Account emails follow an explicit application policy: surrounding whitespace
is removed and the validated normalized form is case-folded before storage or
lookup. This is a product identity decision rather than a universal statement
that every email local part is case-insensitive.

`email-validator` owns maintained email syntax parsing. Domain validation uses
`check_deliverability=False`, so registration and login do not perform DNS or
MX lookups. Syntax validation cannot prove mailbox ownership; that would
require a separate email-verification workflow, which is outside the current
scope.

`normalize_user_email` is the single domain boundary for this policy. It
translates the third-party `EmailNotValidError` into a domain-facing
`ValueError`, preventing higher layers from depending on library-specific
exceptions.

## User Domain and Persistence Representations

`NewUser` contains only normalized email and a password hash. It deliberately
has no role or active-state field, so ordinary registration cannot request an
elevated role. `User` contains the persisted identity, internal password hash,
bounded `member`/`admin` role, and active state. Future public response schemas
must omit the password hash even though the internal authentication domain
needs it for verification.

`UserRecord` defines the PostgreSQL representation. The database owns the
identity and applies `member` and active defaults. A named unique constraint
protects normalized email identity, while check constraints defend the email
format, allowed roles, and timestamp order even when writes bypass ordinary
application construction.

The registration mapper copies only email and password hash into a new record.
It does not assign role or active state. After an INSERT, the repository will
use `flush()` and `refresh()` to obtain the database-generated identity and
trusted defaults. The record-to-domain mapper converts raw role text into a
`UserRole`; unknown persisted roles fail rather than silently entering the
domain.

Ticket ownership references `users.user_id`. Because existing Ticket rows have
no trustworthy owner, revision `e98825c4d6b6` adds nullable `owner_id` as the
expand phase. Its restrictive foreign key prevents deletion of an owning User,
and the ownership/status/Ticket-id index supports future authorized listings.
Backfill and a later non-null contract remain explicit; no fabricated owner is
silently assigned during schema creation.

## Registration Boundary

`UserRegisterRequest` accepts only email and plaintext password. Extra input is
forbidden, so a client cannot select `admin`, active state, identity, or Ticket
ownership. Email is syntactically validated and case-folded. Password length is
bounded, all-whitespace input is rejected, and meaningful surrounding spaces
are preserved rather than silently changing the credential.

The plaintext password exists only at the HTTP and hashing boundary. The
registration service validates and normalizes email first, asks the injected
hashing capability for an Argon2id encoding, constructs `NewUser` with that
encoding, and passes it to the repository. `UserResponse` deliberately contains
only `user_id`, email, role, and active state; Pydantic rejects password fields
instead of serializing them accidentally.

The database unique constraint is the final authority for duplicate identity.
The SQLAlchemy repository translates `IntegrityError`, the service translates
the storage-facing conflict, and the route raises HTTP `409`. Raising the HTTP
exception allows the request-scoped Session dependency to roll back the failed
transaction. PostgreSQL HTTP tests prove that the original User survives, no
duplicate row appears, and cleanup returns both guarded tables to zero rows.

## Access-Token Implementation

The access-token manager signs with server-configured HS256 and accepts only
that same explicit algorithm while decoding. It does not trust an algorithm
named by the unverified token header. Tokens contain only `sub`, `iat`, and
`exp`: the immutable User identifier, issuance time, and expiration time.
Email, role, password hashes, database records, and secrets are deliberately
absent.

`Clock` is a narrow time-source protocol. Production uses a timezone-aware UTC
`SystemClock`; tests use a frozen implementation. This keeps production time
real while making exact `iat` and `exp` assertions deterministic. A naive
datetime is rejected because a timestamp without timezone context can be
interpreted inconsistently.

Decoding requires all three claims, verifies the signature and expiration,
and converts `sub` back to a positive integer. Malformed, modified, expired,
wrong-secret, wrong-algorithm, missing-claim, and invalid-subject tokens cross
one local `InvalidAccessTokenError` boundary rather than leaking PyJWT-specific
exceptions upward.

A compact JWT uses Base64URL text. Changing its final encoded character is not
always a valid tampering test because that character may contain unused
padding bits and still decode to the same bytes. The signature test therefore
changes a meaningful leading signature character and proves that verification
rejects the altered byte sequence.

## Login Application Boundary

`AuthenticationService` depends on three capabilities: User lookup, password
verification, and access-token issuance. It does not import SQLAlchemy,
pwdlib, PyJWT, environment configuration, or HTTP types. Recording fakes prove
the orchestration quickly, while the dependency layer supplies the real
implementations.

Login normalizes the email, looks up the User, verifies the submitted password,
rejects inactive accounts, and issues a token only for a successful active
identity. Missing users, incorrect passwords, and inactive users all raise the
same `InvalidCredentialsError` message and never reach token issuance. This
generic contract prevents response text from revealing which account state
was encountered.

Generic text alone is insufficient if a missing User returns much faster than
a wrong password. The service therefore selects a dummy password hash when no
User exists and still invokes the password verifier. The dummy hash must be a
valid Argon2id encoding in production. The application generates it from a
random synthetic value once per process and caches it. Every missing-account
login therefore performs a real Argon2 verification without paying an
additional Argon2 hash-generation cost on every request.

## HTTP Login and Current-User Boundary

`POST /auth/login` accepts the project's strict JSON login schema and returns
only a bearer access token. It maps all credential failures to the same public
`401` response. The dependency graph composes the SQLAlchemy User repository,
pwdlib verifier, cached dummy hash, configured JWT secret and lifetime, and
timezone-aware system clock; the route itself knows none of those details.

Protected endpoints use FastAPI's HTTP Bearer parser only to extract the
credential. The application still verifies the fixed JWT algorithm, signature,
required claims, expiration, and positive subject. It then reloads the User by
`user_id` and checks `is_active`. A signed token is therefore insufficient on
its own: deleting or deactivating the User immediately causes later requests
with that token to fail.

## Server-Derived Ticket Ownership

`POST /tickets` requires an authenticated current User. The route obtains
`owner_id` from that server-controlled identity rather than accepting it in
request JSON. Strict Pydantic input rejects an injected ownership field, and
the value travels through `TicketService`, `NewTicket`, and the repository to
the nullable database foreign key.

This completes safe ownership assignment for new Tickets, not all Ticket
authorization. Detail, update, and deletion still need explicit owner-aware
queries and cross-user tests. Those are object-level authorization decisions
and cannot be inferred merely from successful authentication.

## Owner-Scoped Ticket Collection

The ordinary `GET /tickets` endpoint now requires a current active User. Its
service calls the explicit `list_by_owner(owner_id)` repository capability,
and the SQLAlchemy adapter includes the owner predicate in the database query.
This is intentionally stronger than loading every Ticket and filtering in
Python: unrelated records never cross the persistence boundary, and forgetting
a later in-memory filter cannot expose the whole collection.

Fast tests cover missing Bearer credentials and in-memory cross-owner
isolation. A guarded PostgreSQL test registers and authenticates two Users,
creates one Ticket with each token, proves that the first User sees only their
own identifier, confirms two distinct owners were persisted, and deletes the
exact test records afterward.

## Not Implemented Yet

- Object-level Ticket detail, update, and delete authorization
- Bounded role/function-level authorization
- Ticket ownership backfill and non-null contract

## Primary References

- FastAPI, OAuth2 with Password and Bearer JWT:
  <https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/>
- pwdlib API reference:
  <https://frankie567.github.io/pwdlib/reference/pwdlib/>
- PyJWT API reference:
  <https://pyjwt.readthedocs.io/en/stable/api.html>
- OWASP Authentication Cheat Sheet:
  <https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html>
- OWASP Password Storage Cheat Sheet:
  <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>
- email-validator documentation:
  <https://github.com/JoshData/python-email-validator>
