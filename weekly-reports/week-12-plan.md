# Week 12 Plan

## Dates and objective

29 September–4 October 2026 — Month 03 continuation.

Build the first tenant-scoped OpsDesk business vertical slice on the completed identity
foundation: Ticket persistence prerequisites, atomic Organization creation, scoped
Organization reads, and authenticated Ticket creation if the preceding gates close on
schedule. Week 11 has no technical carry-over.

Target capacity: 18–24 active hours across Tuesday–Sunday. This includes explanations,
implementation, meaningful tests, documentation, Git review, and weekly closure.
External CI waits and breaks are additional. The upper bound is a recovery-week load,
not the new normal.

## Completion priorities

1. **B04 / issue #8 — Ticket schema:** SQLAlchemy model, Alembic revision, guarded
   PostgreSQL constraints, migration cycle, and cleanup policy.
2. **F05 / issue #14 — Organization creation:** one atomic Organization plus initial
   active owner membership for the authenticated active User.
3. **F06 / issue #15 — Organization list/detail:** expose only Organizations reachable
   through the caller's active memberships, with the reviewed response envelopes.
4. **F01 / issue #18 — Ticket creation:** begin only after #8 and the Organization
   boundary are merged. Finish within Week 12 when gates and capacity permit; otherwise
   preserve a tested checkpoint and report the exact remaining acceptance criteria.

The first three items form the fixed completion target. Ticket creation is the next
dependency-respecting target, not permission to skip #8/#14/#15 review. Membership
mutation, Ticket listing/workflow, comments, database CI, deployment, Docker, Redis,
frontend, and AI work are outside this week's implementation scope.

## Daily packages

| Date | Estimate | Package and evidence |
| --- | ---: | --- |
| Tue 29–Wed 30 Sep | Completed | Combined Ticket-schema package: model, migration, PostgreSQL constraints, guarded migration cycle, PR/CI/merge #8 |
| Thu 1 Oct | 3–4 h | Explain atomic aggregate creation; implement Organization creation service/repositories/schemas/endpoint and rollback tests |
| Fri 2 Oct | 3–4 h | Real PostgreSQL success/failure/concurrency evidence for Organization creation; PR/CI/merge #14 |
| Sat 3 Oct | 3–4 h | Implement scoped Organization list/detail with pagination/snapshot contract and tenant-safe tests; PR/CI/merge #15 |
| Sun 4 Oct | 2–3 h | Start or complete #18 according to closed gates; full relevant regression, interview review, report, Git closure, next-week handoff |

At the end of each package, record completed behavior, tests, actual remaining work,
and any scope effect. Group changes and tests by file or behavior. Do not repeat the
entire suite after every small edit; run focused tests first and one complete regression
per merge candidate.

## 29–30 September combined outcome

- Added `TicketRow` and Alembic revision `31be9023cfb2` with the reviewed identity,
  tenant-participant, text, status, priority, timestamp, and deletion constraints.
- Kept tenant consistency in composite foreign keys while leaving active membership,
  eligible role, authorization, assignment, and lifecycle transitions to services.
- Extended the guarded cleanup policy and migration revision checks for `tickets`,
  preserving child-before-parent cleanup order.
- Proved catalog structure, valid/invalid boundaries, nullable assignee behavior,
  cross-tenant and missing-membership rejection, restrictive deletion, timestamp
  behavior, and predecessor-data preservation through real PostgreSQL tests.
- Final merge-candidate snapshots passed separately: `222` non-integration tests,
  `127` integration tests, and `3` schema-changing migration tests. Alembic reported
  revision `31be9023cfb2 (head)` with no pending upgrade operations.
- GitHub PR [#37](https://github.com/ozdemirr1/opsdesk/pull/37) passed hosted Backend
  CI at reviewed head `efd2bc5`, merged as `5151c29`, closed issue #8, and left local
  and remote feature branches removed with clean synchronized `main`.
- No Week 12 scope was skipped. The next dependency-respecting package is Organization
  creation in issue #14 on 1 October.

## Architecture and security gates

- Explain schema/service/repository/transaction responsibilities before product code.
- Use synchronous SQLAlchemy and Alembic. Do not introduce async persistence.
- Extend the guarded cleanup allowlist only with the Ticket table introduced by #8.
- Ticket foreign keys establish existence and tenant consistency. Active membership,
  eligible role, permissions, and lifecycle rules remain application checks.
- Organization creation derives the owner User from authenticated state. The client
  cannot submit owner membership ID, role, User ID, or active flags.
- Create Organization and owner membership in one short transaction. Commit before
  201; rollback leaves neither row. No network or external calls while locks are held.
- Organization list/detail must use current active membership and must not reveal
  foreign Organizations. Suspended Organization visibility follows the accepted contract.
- Reuse safe errors, request IDs, route templates, and established 400/401/403/404/
  409/422/500/503 distinctions. Unknown database errors remain 500.
- No password, JWT secret, complete token, connection URL, or raw sensitive input may
  enter source, Git, public responses, or logs.

## Required verification

- Ruff lint and format checks for each changed package.
- Unit tests for pure validation, service ordering, transaction behavior, and error
  translation; HTTP tests for exact request/response contracts.
- PostgreSQL tests for constraints, fresh-session persistence, rollback, tenant
  isolation, and no unintended writes.
- B04 migration predecessor preservation plus upgrade/downgrade/re-upgrade; restore
  head before ordinary tests.
- Hosted CI must pass at the exact reviewed PR head before merge. PostgreSQL evidence
  remains local until issue #25 adds guarded database CI.
- Final report must distinguish successive test snapshots rather than summing them.

## Notes to write

- Why composite foreign keys enforce tenant consistency but not authorization.
- Why server defaults and database constraints complement application validation.
- Why Organization plus owner membership is one transaction boundary.
- Why membership-backed visibility differs from global authentication.
- How schema migration-cycle tests protect existing identity data.

## Planned Git structure

- `feature/week-12-ticket-schema`
- `feature/week-12-organization-creation`
- `feature/week-12-organization-reads`
- `feature/week-12-ticket-creation` only after its dependencies are merged

Use small product-focused commits and one reviewed PR per issue. Remove merged feature
branches locally and remotely after synchronizing `main`.

## Weekly review questions

1. What can a composite foreign key prove, and what authorization facts can it not prove?
2. Why must a migration cycle preserve predecessor data?
3. Where should transaction ownership live for Organization creation, and why?
4. Why is authenticated User identity insufficient for Organization detail access?
5. When should a conflict become 409 instead of 500?
6. Which checks must be repeated after acquiring a coordination lock?
7. How do real PostgreSQL tests differ from service tests with fake repositories?
8. What evidence is required before calling the first tenant business slice complete?

## Week-end decision gate

Sunday records what actually merged and the remaining Month 03 backlog. Do not call the
backend preview deployed or Month 03 complete without its required feature, database-CI,
and delivery evidence. If #18 is incomplete, preserve a clean tested checkpoint and
size the remaining work explicitly; do not hide it by starting React early.
