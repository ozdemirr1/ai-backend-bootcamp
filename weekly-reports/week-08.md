# Week 08 Report

## Date

31 August - 6 September 2026

## Main Focus

- User identity, registration, and login
- Argon2id password hashing and verification
- JWT access-token creation and validation
- Persisted current-User resolution
- Protected Ticket endpoints
- Server-derived Ticket ownership
- Object-level and role/function-level authorization
- Authentication and authorization testing

## What I Completed

- [x] Added `pwdlib` with Argon2 support, PyJWT, and email validation
- [x] Added secret-aware JWT configuration and bounded token lifetime
- [x] Isolated password hashing behind a focused application boundary
- [x] Added User domain and SQLAlchemy persistence models
- [x] Normalized email identities and enforced database uniqueness
- [x] Prevented ordinary registration from selecting a privileged role
- [x] Added User repository protocols plus in-memory and SQLAlchemy adapters
- [x] Added Alembic revision `e98825c4d6b6` for Users and Ticket ownership
- [x] Verified migration upgrade, downgrade, re-upgrade, and schema drift
- [x] Added registration with hashed-password persistence
- [x] Added generic login failure behavior and dummy-hash verification
- [x] Added deterministic clock and JWT boundaries
- [x] Added persisted active-User resolution and `GET /users/me`
- [x] Protected every Ticket endpoint with Bearer authentication
- [x] Derived Ticket ownership from the authenticated User
- [x] Scoped ordinary Ticket collections to their owner in SQL
- [x] Prevented cross-User Ticket read, update, and delete operations
- [x] Added a separate admin-only cross-owner Ticket collection
- [x] Verified current persisted roles rather than trusting stale token roles
- [x] Completed the authentication and authorization interview review
- [x] Merged pull request #6 and removed the feature branches

## What I Learned

### Authentication and Authorization

- Authentication establishes who the caller is; authorization separately
  decides which resources and functions that identity may access.
- A valid JWT is not proof that its subject may access an arbitrary Ticket.
- Object-level authorization protects individual resources addressed by IDs.
- Function-level authorization protects privileged operations such as an
  administrator's cross-owner listing endpoint.
- Missing and foreign-owned Ticket identifiers can share the same `404`
  response to avoid disclosing whether another User's object exists.

### Password Storage

- Passwords are hashed, not encrypted, because the application never needs to
  recover the original value.
- Argon2id stores the algorithm parameters and salt in the encoded hash so a
  submitted password can be checked without decrypting the stored value.
- A random salt makes equal passwords produce different hashes and defeats
  direct reuse of precomputed rainbow tables.
- Argon2's work factor makes offline guessing deliberately expensive but does
  not make weak passwords impossible to crack.
- A dummy hash makes missing-account and wrong-password paths perform similar
  expensive work, reducing timing-based account-enumeration signals without
  promising identical response times.

### JWT Boundaries

- The access token carries only `sub`, `iat`, and `exp`; it does not contain
  passwords, hashes, complete User records, or authorization decisions.
- The accepted signing algorithm is fixed by server configuration instead of
  being trusted from an unverified token header.
- Signature verification detects meaningful token modification, while claim
  validation rejects expired, incomplete, or invalid identities.
- A correctly signed token can still be rejected when the User has been
  deleted or deactivated because protected requests reload current state from
  persistence.

### Identity and Ownership

- Stable database-generated `user_id` values are safer relationship keys than
  mutable email addresses.
- Email normalization and email syntax validation solve different problems.
- Role and ownership fields must be assigned by trusted server logic rather
  than accepted from ordinary client input.
- Collection filtering at SQL level reduces both unnecessary work and the
  amount of unrelated data crossing the persistence boundary.
- SQL filtering is one defense, not a claim that all authorization risk has
  been eliminated.

### Transactions and Constraints

- The database unique constraint is the final authority for duplicate email
  races that application-level pre-checks cannot resolve atomically.
- Repository methods may `flush()` to obtain generated values and detect
  constraints but do not own request-level `commit()` or `rollback()`.
- Exceptions propagate to the request-scoped Session dependency, which rolls
  back the complete request transaction and prevents partial persistence.

## Architecture Built

```text
HTTP credentials
      |
      v
Pydantic request contract
      |
      +----> RegistrationService ----> PasswordHashing
      |              |                       |
      |              v                       v
      |        UserRepository            Argon2id
      |
      +----> AuthenticationService ----> token issuer
                                             |
                                             v
                                       signed JWT

Authorization: Bearer <token>
      |
      v
fixed-algorithm decode --> positive user_id --> persisted active User
      |
      +----> owner-scoped Ticket service/repository
      |
      +----> explicit admin dependency and privileged endpoint

request-scoped Session --> commit on success / rollback on failure / close
```

## Migration Evidence

- Revision: `e98825c4d6b6`
- Purpose: add the `users` table and nullable Ticket `owner_id`
- User email unique constraint: verified
- Ticket ownership foreign key: verified with `ON DELETE RESTRICT`
- Ownership listing index: verified
- Upgrade to head: passed
- Downgrade to `e07f08d4399d`: passed
- Legacy Ticket preservation during downgrade: passed
- Re-upgrade to head: passed
- `alembic current`: `e98825c4d6b6 (head)`
- `alembic check`: no new upgrade operations detected

The nullable column is an intentional expand phase. Historical Tickets have no
trustworthy ownership source, so the migration does not invent a User. A
future `NOT NULL` contract requires a real backfill, proof that no rows remain
unowned, and application verification.

## Test Evidence

- Final run with database tests disabled: 274 passed, 37 skipped
- Final run with database tests enabled: 311 passed
- Ruff lint: passed
- Ruff formatting: 107 files already formatted
- Dependency lock, synchronization, and compatibility checks: passed
- Git diff checks: passed
- Alembic head and schema-drift checks: passed
- Final `opsdesk_test` User count: 0
- Final `opsdesk_test` Ticket count: 0

The complete suite covers password behavior, strict auth schemas, registration,
login, token tampering and expiry, current-User resolution, stale-token
rejection, server-derived ownership, owner-scoped listing, BOLA attempts,
member/admin boundaries, transaction failures, and precise database cleanup.

## Interview Review

I explained and corrected the important distinctions among:

- authentication and authorization
- hashing and encryption
- salt, work factor, and Argon2id
- JWT encoding, signing, and encryption
- access tokens and refresh tokens
- `401`, `403`, and non-disclosing `404` responses
- timing-signal reduction and guarantees that cannot be made
- object-level authorization and BOLA/IDOR
- SQL owner filtering and service-side identified-resource checks
- application duplicate checks and database uniqueness
- repository persistence and request-owned transactions
- expand, backfill, and contract migration phases

The review confirmed that I can describe the security boundaries without
overclaiming that a single control eliminates brute force, timing analysis, or
authorization risk.

## GitHub Output

- Branch: `feature/week-08-auth-authorization`
- Pull request: #6, `Week 08: add authentication, Ticket ownership, and authorization`
- Feature commits: 8
- Changed files in the pull request: 43
- Final feature commit: `a1cf847`
- Merge commit: `9876703`
- Local and remote feature branches removed after merge
- Final `main` branch synchronized with `origin/main`

## Known Limitations

- Historical Ticket ownership remains nullable until a trustworthy backfill
  source exists.
- The learning API has only a small global `member`/`admin` role model; real
  OpsDesk roles will be scoped through organization membership.
- Refresh tokens, token revocation, password reset, account recovery, MFA, and
  external identity providers are outside this learning scope.
- The implementation remains deliberately synchronous.
- Comments, attachments, organization membership, audit history, rate
  limiting, and standardized error responses belong to later product phases.
- The repository still has no GitHub Actions workflow or deployed backend.

## Next Week

Week 09 begins Month 03 and the real OpsDesk product in a separate repository.
The first week is design-first: requirements, domain vocabulary, organization
membership, role and access matrices, relational ERD, endpoint inventory, and
an implementation-ready GitHub issue backlog. CI will be added only when a
minimal executable project and meaningful tests exist; Docker remains in its
scheduled later phase.
