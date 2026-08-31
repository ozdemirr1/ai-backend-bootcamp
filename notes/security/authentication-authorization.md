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

## Not Implemented Yet

- User domain and persistence models
- User repository and mapper
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
