# Week 11 Report

## Dates and result

Planned: 21–27 September 2026. Evidence-based closure: 28 September 2026.
Illness and the Week 10 carry-over moved the final completion day by one day. The
calendar variance is explicit; no test, review, or acceptance criterion was removed.

Week 11 completed the OpsDesk identity boundary and the remaining API-contract design
gate. Registration, login/access-token issuance, protected current-user resolution,
and the reviewed D03 contract are merged. Week 12 therefore starts without Week 11
technical carry-over.

## Completed scope

- Published the Week 10 report, evidence, career research, and revised Week 11 plan.
- Published the fourth LinkedIn project update and updated the necessary profile
  sections around the current Python backend direction.
- Completed guarded registration with canonical email, Argon2id hashing, explicit
  transaction ownership, safe duplicate handling, and a controlled concurrent race.
- Completed login with generic credential failures, dummy-hash verification for
  unknown Users, environment-backed HS256 configuration, and a five-claim token.
- Completed the remaining D03 decisions for collection filters/counts, nested
  responses, repeat behavior, error precedence, timestamps, and Attachment timing.
- Completed strict bearer validation and `GET /users/me`, reloading the active User
  from PostgreSQL for every protected request.
- Proved the full `register -> login -> /users/me` flow against PostgreSQL.

## Merged product evidence

| Scope | Issue | Pull request | Merge commit |
| --- | --- | --- | --- |
| Guarded user registration | [#11](https://github.com/ozdemirr1/opsdesk/issues/11) | [#33](https://github.com/ozdemirr1/opsdesk/pull/33) | `4d8a9f1` |
| Login and access-token issuance | [#12](https://github.com/ozdemirr1/opsdesk/issues/12) | [#34](https://github.com/ozdemirr1/opsdesk/pull/34) | `d321e14` |
| Remaining API contracts | [#3](https://github.com/ozdemirr1/opsdesk/issues/3) | [#35](https://github.com/ozdemirr1/opsdesk/pull/35) | `03f689c` |
| Authenticated current User | [#13](https://github.com/ozdemirr1/opsdesk/issues/13) | [#36](https://github.com/ozdemirr1/opsdesk/pull/36) | `1641bc2` |

Each PR passed both hosted Backend CI checks at its reviewed head. Supplied terminal
evidence confirms the four issues are closed, product `main` is synchronized, and all
four feature branches were removed locally and remotely.

## Validation evidence

These are successive merge-candidate snapshots, not numbers to add together:

- Registration closure: 147 non-integration tests and 67 PostgreSQL integration tests.
- Login closure: 181 non-integration tests and 71 PostgreSQL integration tests.
- Final current-user closure: Ruff passed, 67 Python files were already formatted,
  218 non-integration tests passed with 80 database/schema cases deselected, and all
  78 ordinary PostgreSQL integration tests passed.
- The final seven current-user integration cases covered controlled signed tokens,
  invalid signatures, expiration, missing Users, deactivation after token issuance,
  absence of Organization/Membership writes, and the complete identity flow.
- No schema changed during the login/current-user slices, so destructive migration
  cycle tests were not rerun without cause.

## Engineering decisions and learning

- Authentication proves the current global identity; authorization still requires
  current Organization membership, Organization state, visibility, and permission.
- A valid JWT is insufficient by itself. Reloading the User makes account deactivation
  effective without waiting for token expiry.
- The server fixes HS256 and validates the signature before trusting `sub`. Token
  input never chooses the permitted algorithm.
- Tokens contain identity/time claims only. Roles and tenant permissions remain
  current database state rather than stale bearer claims.
- Unknown email, wrong password, and inactive User share one public login failure.
  Database and signing failures remain infrastructure errors instead of false 401s.
- Hashing happens before the short write transaction. PostgreSQL uniqueness remains
  the final authority for concurrent duplicate registration.
- Controlled signed fixtures isolate token validation from login; a separate end-to-
  end test proves the assembled registration, login, and protected endpoint flow.

## Interview review

1. **Authentication versus authorization?** Authentication resolves who the caller
   currently is. Authorization decides whether that identity may perform one operation
   on one scoped resource.
2. **Why reload the User after JWT validation?** A signed token can remain valid after
   the persisted account is deactivated; current state must win.
3. **Why fix the accepted JWT algorithm server-side?** An untrusted token header must
   not weaken or select the verification method.
4. **Why use one response for unknown email, wrong password, and inactivity?** It
   reduces account-state disclosure while keeping client behavior predictable.
5. **Why is a pre-insert email lookup insufficient?** Concurrent requests can both
   observe absence; the database UNIQUE constraint decides the race atomically.
6. **Why is a database failure not 401?** Authentication did not fail because of bad
   credentials; hiding an outage as 401 corrupts observability and client behavior.
7. **Why omit roles from the token?** Organization roles can change and are tenant
   specific. Loading them at authorization time prevents stale cross-tenant privilege.
8. **What does the PostgreSQL identity-flow test add?** It verifies the real Session,
   repository, password hash, token, HTTP dependency, and persisted-state composition.

## Variance and remaining product work

The Sunday target was missed and closed Monday. Actual active hours were not measured,
so elapsed calendar time is not presented as focused work time. Grouped test packages
and fixed completion blocks reduced request fragmentation during the recovery day.

Week 11 did not implement Ticket schema, Organization endpoints, membership workflows,
Ticket workflows, comments, database CI, or deployment. These are existing Month 03
backlog items rather than hidden Week 11 carry-over. Week 12 begins with the first
tenant-scoped business vertical slice and will report any remaining monthly variance
instead of claiming an unverified backend preview.

## Closure status

Week 11 implementation, local regression, hosted CI, product merges, issue closures,
branch cleanup, learning review, and this report are complete. The remaining action is
to commit and push this bootcamp evidence together with the Week 12 handoff.
