# Authentication and Authorization

## Purpose

These notes record the Week 08 security model for the Month 02 Ticket API.
They describe the current password and token-configuration foundation without
claiming that registration, login, JWT issuance, or authorization are already
implemented.

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
pwdlib's construction or method details. Full dependency inversion will be
introduced only when a service depends on an injected protocol rather than a
concrete implementation.

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

Ticket ownership will reference `users.user_id`. Because existing Ticket rows
have no owner, the first ownership migration will add nullable `owner_id` as
the expand phase. Backfill and a later non-null contract must be explicit; a
fabricated owner must not be silently assigned during schema creation.

## Not Implemented Yet

- User repository
- Registration and login routes
- JWT creation and decoding
- Current-user dependency
- Ticket ownership
- Object-level and role/function-level authorization

## Primary References

- FastAPI, OAuth2 with Password and Bearer JWT:
  <https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/>
- pwdlib API reference:
  <https://frankie567.github.io/pwdlib/reference/pwdlib/>
- OWASP Password Storage Cheat Sheet:
  <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>
- email-validator documentation:
  <https://github.com/JoshData/python-email-validator>
