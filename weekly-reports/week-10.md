# Week 10 Report

## Dates and result

Planned: 14–20 September 2026. Carry-over completed through 22 September;
report and career research prepared 23 September. Illness reduced available time.
Actual total active hours were not measured; the calendar is not relabeled.

OpsDesk now has an executable FastAPI foundation, guarded synchronous PostgreSQL
infrastructure, identity schema/migrations, shared API errors and request diagnostics.
Concurrency rules are accepted design, not executable business locking.

## Merged evidence

| Scope | PR | Merge |
| --- | --- | --- |
| #1/#2 contracts, #5 foundation, #9 fast CI | [#28](https://github.com/ozdemirr1/opsdesk/pull/28) | 64b14eb |
| #6 guarded PostgreSQL infrastructure | [#29](https://github.com/ozdemirr1/opsdesk/pull/29) | 3f85571 |
| #7 identity/Organization schema | [#30](https://github.com/ozdemirr1/opsdesk/pull/30) | d5147fe |
| #10 shared errors and request diagnostics | [#31](https://github.com/ozdemirr1/opsdesk/pull/31) | c07a48f |
| #4 cooperating transaction design | [#32](https://github.com/ozdemirr1/opsdesk/pull/32) | 9bf8726 |

User terminal evidence confirms these issue closures and branch cleanup. Latest
product inspection found clean main at 9bf8726d96bcb13fb69ddee5ddc37bb306616be8.

## Validation and limits

- Latest HTTP-foundation run: 101 non-integration tests passed; 62 database/schema
  cases deselected. Ruff passed with 41 files formatted.
- Earlier schema milestone: 60 PostgreSQL integration tests and 2 isolated migration
  tests passed. These were separate runs; do not present them as one new 163-test run.
- Expanded fast CI passed on #31 and both checks passed on #32. PostgreSQL CI is not
  implemented. Documentation-only #32 did not require new local runtime tests.
- Real Uvicorn 404 verification matched the server-issued response/log ID without
  synthetic path/query/header secrets; it does not prove all server failure paths.
- No registration, login, current-user endpoint, Ticket business schema, deployment,
  or executable Organization concurrency protocol is claimed complete.

## Engineering decisions and learning

- Application factories/settings separate startup validation and test configuration.
- Exact product test target and restricted roles protect the old Month 02 databases.
- Explicit transaction ownership; real-commit tests use independent reads and cleanup.
- Alembic governs schema changes. An at-most-one owner index does not ensure an owner
  exists or that its User is active; the application must enforce those invariants.
- Expected business conflicts differ from unknown database failures. Fixed errors,
  bounded metadata and route templates reduce disclosure; they do not secure every logger.
- Response-start logging is not proof of client delivery or database commit outcome.
- Organization coordination, ordered locks, fresh checks and transfer flush ordering
  are accepted. Per-lock timeout is 2 seconds; recognized contention maps to 503
  concurrency_busy with rollback and no automatic retry, when implemented.

## Process review

Early estimates underestimated schema/test work and fragmented same-file exercises
into too many turns. Future work uses grouped test packages, concept explanations
before code, explicit daily budgets and progress at each completed package. Scope
changes must be explained before extending the day; tests are not skipped to catch up.

## Carry-over and closure

- #3 remains open and is explicitly assigned to the combined Week 11 completion
  scope, with six bounded decision groups and affected features recorded in
  [the handoff inventory](week-10-plan.md#d03-remaining-prerequisite-inventory).
- Registration/login/current-user work moves to [Week 11](week-11-plan.md); it was
  conditional/stretch Week 10 scope, not silently counted as delivered.
- [Two career targets and an unsent outreach draft](week-10-career-targets.md)
  complete the research/drafting action. No application or message was sent.
- Technical review, report and handoff preparation are complete. Bootcamp commit/push
  remains a separate user verification step.
