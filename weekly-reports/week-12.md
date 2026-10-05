# Week 12 Report

## Dates and result

Planned: 29 September–4 October 2026. Evidence-based closure: 5 October 2026.
The Saturday and Sunday packages were completed on Monday, producing a one-day
calendar variance. No acceptance criterion, test group, review gate, or Git cleanup
step was removed to recover the schedule.

Week 12 completed OpsDesk's first tenant-scoped business vertical slice. The Ticket
schema, atomic Organization creation, membership-scoped Organization reads, and
authenticated Ticket creation are merged. Week 13 can therefore be planned from a
clean product `main` without Week 12 technical carry-over.

## Completed scope

- Added the tenant-consistent Ticket persistence model and Alembic migration.
- Proved the Ticket schema, constraints, cleanup policy, and migration cycle against
  PostgreSQL.
- Implemented atomic Organization creation with server-derived active ownership.
- Proved rollback, known lock-failure translation, and independent-actor progress.
- Implemented Organization collection/detail reads restricted by current active
  membership, with exact filtering, ordering, pagination, and snapshot behavior.
- Implemented authenticated Ticket creation with server-derived requester and creator,
  safe initial state, current membership validation, and coordinated locks.
- Completed hosted CI, merge, issue closure, branch cleanup, and synchronized-main
  evidence for all four Week 12 product packages.

## Merged product evidence

| Scope | Issue | Pull request | Merge commit |
| --- | --- | --- | --- |
| Tenant-consistent Ticket schema | [#8](https://github.com/ozdemirr1/opsdesk/issues/8) | [#37](https://github.com/ozdemirr1/opsdesk/pull/37) | `5151c29` |
| Atomic Organization creation | [#14](https://github.com/ozdemirr1/opsdesk/issues/14) | [#38](https://github.com/ozdemirr1/opsdesk/pull/38) | `57ae5f1` |
| Membership-scoped Organization reads | [#15](https://github.com/ozdemirr1/opsdesk/issues/15) | [#39](https://github.com/ozdemirr1/opsdesk/pull/39) | `3355928` |
| Authenticated Ticket creation | [#18](https://github.com/ozdemirr1/opsdesk/issues/18) | [#40](https://github.com/ozdemirr1/opsdesk/pull/40) | `ec418f9` |

Each pull request passed hosted Backend CI at its reviewed head. Supplied terminal
evidence confirms that all four issues are closed, the merged feature branches were
removed locally and remotely, and OpsDesk `main` ended clean and synchronized with
`origin/main`.

## Validation evidence

These are successive merge-candidate snapshots, not numbers to add together:

- Ticket-schema closure: 222 non-integration tests, 127 ordinary PostgreSQL
  integration tests, and 3 guarded schema/migration tests.
- Organization-creation closure: 283 non-integration tests with 141 database/schema
  cases deselected, plus 138 ordinary PostgreSQL integration tests.
- Organization-read closure: 337 non-integration tests with 150 database/schema cases
  deselected, 147 ordinary PostgreSQL integration tests, and 3 guarded schema tests.
- Ticket-creation closure: 439 non-integration tests with 160 database/schema cases
  deselected, 157 ordinary PostgreSQL integration tests, and 3 guarded schema tests.
- Alembic finished at `31be9023cfb2 (head)` with no pending upgrade operations or
  model/migration drift.

The final Ticket-creation evidence includes real PostgreSQL persistence, rollback,
tenant isolation, inactive-state rejection, participant consistency, recognized lock
failures, a lock wait observed through `pg_blocking_pids`, and progress for a different
Organization while one request was blocked.

## Engineering decisions and learning

- Composite foreign keys prove referenced-row existence and tenant consistency. They
  do not prove current activity, permission, eligible role, or workflow authority.
- Application services own the transaction boundary; repositories provide persistence
  operations without independently committing the business operation.
- User identity, membership role, active flags, Ticket requester/creator, initial
  status, and initial assignment are server-owned facts rather than client choices.
- Coordinated writes use a shared Organization lock protocol and repeat current-state
  checks after acquiring locks because state may change while a transaction waits.
- Transactions stay short and contain no AI, email, or other network calls while
  database locks are held.
- Organization collection count and page rows are produced from one SQL statement so
  the response represents one database snapshot.
- Only recognized PostgreSQL contention failures map to the fixed 503 response.
  Unknown database failures remain 500 so infrastructure incidents are not mislabeled
  as business conflicts.
- Fake repositories verify service ordering and rollback intent; PostgreSQL tests prove
  actual constraints, locks, visibility, persistence, and transaction behavior.

## Interview review

1. **What does a composite foreign key prove?** It proves that the referenced
   participant exists in the same Organization. Authorization and current activity
   still require service checks.
2. **Why must a migration cycle preserve predecessor data?** Schema evolution is safe
   only when existing identity rows survive upgrade, downgrade, and re-upgrade as the
   migration contract requires.
3. **Where does transaction ownership belong?** In the application service, because it
   coordinates one complete business operation across repository calls.
4. **Why is authentication insufficient for Organization detail?** A valid User may
   still lack a current active membership in the requested Organization.
5. **When is 409 appropriate?** For an expected, classified business conflict. An
   unknown database or infrastructure failure remains 500.
6. **Why repeat checks after locking?** The request may have waited while membership,
   Organization, or User state changed.
7. **Why run real PostgreSQL tests?** Fakes cannot prove database constraints, lock
   waits, isolation, SQL behavior, or durable rollback.
8. **What closes the first tenant business slice?** Merged schema and endpoint code,
   exact HTTP contracts, unit and PostgreSQL evidence, hosted CI, issue closure, branch
   cleanup, and synchronized clean `main`.

## Variance and remaining product work

The planned Sunday closure moved to Monday. Actual active hours were not measured, so
elapsed calendar time is not presented as focused work time. The one-day variance did
not create Week 12 technical carry-over.

Ticket listing/detail, Ticket workflow and assignment changes, membership mutations,
comments, guarded database CI, deployment, Docker, Redis, frontend, and AI features
remain in the Month 03/product roadmap. They were outside the fixed Week 12 completion
scope and must be ordered during Week 13 planning rather than started ad hoc.

## Closure status

Week 12 implementation, local regression, guarded PostgreSQL and migration evidence,
hosted CI, product merges, issue closures, branch cleanup, interview review, and this
report are complete. Detailed Week 13 planning begins on 6 October from OpsDesk merge
commit `ec418f9`; it is intentionally not invented inside this closure report.
