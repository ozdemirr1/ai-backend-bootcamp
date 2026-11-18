# Week 19 — Redis cache and rate limiting

## 17 November — uncached Ticket statistics

Implementation starts on `feature/week-19-redis-cache-limits`, based on the
Week 18 merge (OpsDesk 4cc7bbe). No Redis cache or limiter is implemented yet.

### Learning evidence

The learner ran an in-memory SQLite GROUP BY/COUNT example: customer scope counted
two Tickets, Organization staff scope counted three, and the deliberately unscoped
query included a fourth Ticket from another Organization. All assertions passed.
This was a SQL learning exercise, not PostgreSQL acceptance.

### Product increment

Added GET `/organizations/{organization_id}/ticket-stats`. Existing active
User/Organization/membership checks and requester-membership visibility apply.
Staff roles see their Organization; customers see only requested Tickets.
Access metadata and aggregation share one SQL statement snapshot. The service
rejects invalid access before returning counts, fills absent statuses with zero,
and computes the total. The API accepts no query parameters and keeps safe errors.
No new React UI, migration, dependency, cache or hosted configuration change.

### Verification

- Backend non-integration: 808 passed, 291 deselected in 15.82s.
- Real PostgreSQL data suite: 286 passed in 27.94s on verified loopback port 5432,
  exact `opsdesk_product_test` and restricted `opsdesk_product_test_runner`.
- Existing runner verified target/privileges, applied Alembic head and found no
  upgrade drift. The separate five schema tests were not rerun.
- Ruff lint/format and diff whitespace checks passed in the implementation turn.
- New data coverage checks all four roles, zero counts, foreign membership denial,
  current role after demotion, and no read-side mutation. Existing access-denial
  cases now also exercise statistics.

Initial test collection failed because a sibling test module was not importable;
the new test now owns its client fixture. Invalid-token testing initially returned
500 because the fixture omitted JWT configuration; synthetic test configuration
fixed it and the complete non-integration rerun passed.

A proposed temporary PostgreSQL cluster refused to start because port 5432 was
occupied; no cluster was created. A read-only probe then verified the existing
exact test target. Credentials were not printed or committed. Development/hosted
DBs and retained resources were not deleted or modified by these test commands.
Disk had approximately 2.1 GiB available; no image build was needed.

### Remaining gates

OpsDesk commit `7c9661c` and bootcamp evidence commit `509e53e` were pushed to
`feature/week-19-redis-cache-limits`. All four product workflows passed at that
exact product head: [Backend](https://github.com/ozdemirr1/opsdesk/actions/runs/44126223263),
[Frontend](https://github.com/ozdemirr1/opsdesk/actions/runs/44126223278),
[Docker](https://github.com/ozdemirr1/opsdesk/actions/runs/44126225010), and
[PostgreSQL schema/data](https://github.com/ozdemirr1/opsdesk/actions/runs/44126222976).
No PR merge or deployment occurred. The separate schema suite ran in CI; the
statement above about not rerunning it refers to local execution.
Learner end-of-day explanation remains pending. Redis work begins with the next
planned key/value, TTL and cache-aside exercise, not from these passing SQL tests.

## 19 November — planned 18 November Redis foundation and cache-aside

Learner supplied successful isolated Redis key/value evidence: PING/PONG,
SET EX 10, GET, TTL 10, expired TTL -2 and EXISTS 0; synthetic statistics JSON
was written with EX 60 and read twice. The lab was stopped, not deleted.
New terminology will be introduced as definition → purpose → OpsDesk use before
commands. The 17 November learner explanation was accepted with clarifications:
tenants are Organizations, customer is a membership role, aggregate counts are
private data, and missing authorization differs from an authorized empty result.

Disk verification found 4.4 GiB available, up from the learner's 1.6 GiB. Docker
was stopped; Docker Desktop was opened and Engine 28.5.1 responded. No cleanup or
deletion was performed; existing untracked LinkedIn assets were preserved.

Implemented an optional Redis adapter (redis-py 8.1.0, locked), default disabled.
Cache-aside checks current access before GET and separates environment/version,
Organization, actor, membership and own/all visibility. Aggregation returns its
own scope so a between-query role change cannot populate the initial wrong key.
TTL defaults to 30 seconds, socket/connect timeouts to 0.2 seconds, retries to zero
and pool size to 10. A cache read error falls back to SQL without attempting a
write; write errors preserve the SQL response. Invalid cached JSON/counts are
misses. This is not post-commit invalidation or stale-fill race protection.

Fresh local evidence:

- Focused cache/statistics tests: 31 passed in 1.96s.
- Backend non-integration regression: 821 passed in 9.45s; 292 deselected at that
  run (before adding the two opt-in Redis integration cases).
- Guarded PostgreSQL data plus opt-in Redis checks: 289 passed in 26.60s
  (287 PostgreSQL data and 2 Redis cases); Alembic found no drift.
- SQL instrumentation confirmed the second read skipped the actual aggregate,
  while fresh authorization and role demotion still affected visibility. The SQL
  test used a memory cache transport, while two separate tests exercised real
  Redis expiry/invalid payload and a controlled unresponsive TCP peer.
- Ruff check/format and diff whitespace checks passed.

The Redis lab `week19-cache-verification` used an ephemeral loopback-only host
port and unique expiring synthetic keys. No FLUSH or resource deletion occurred.
The test container was stopped after verification. PostgreSQL target and restricted
role were checked before using the existing guarded runner. No dev/hosted DB tests.

Implementation is local and uncommitted at this checkpoint. No new CI, PR merge,
live cache enablement or deployment is claimed. Remaining: learner walkthrough,
publication, post-commit invalidation/stale-fill exercise, limiter and Redis CI.

### Learner closure — 19 November

The learner independently reran the 13 focused cache tests: all passed in 0.31s.
The learner explained that revoked membership or reduced scope must be checked
before cache lookup, and key design cannot replace authorization. They also
explained that bounded Redis waiting enables timely PostgreSQL fallback. Review
clarified that 200 ms is a per-operation timeout, not a whole-request deadline.
The planned 18 November learning checkpoint is complete. Publication follows;
post-commit invalidation and stale-fill races remain the planned 19 November work.

### Publication — planned 18 November checkpoint closed on 19 November

Product commit `99bd2c25aca10d271951eaa8d4556851e8ee164a` was pushed to
`feature/week-19-redis-cache-limits`. All four exact-head workflows passed:
[Backend](https://github.com/ozdemirr1/opsdesk/actions/runs/44403892154),
[Frontend](https://github.com/ozdemirr1/opsdesk/actions/runs/44403892743),
[Docker](https://github.com/ozdemirr1/opsdesk/actions/runs/44403891965), and
[PostgreSQL](https://github.com/ozdemirr1/opsdesk/actions/runs/44403891947).
The two Redis integration cases remain local opt-in evidence; this workflow does
not run a Redis service yet. Learning, local verification and publication close
the planned 18 November scope. Cache remains disabled by default. No main merge,
live enablement, deployment, resource deletion or next-day implementation occurred.
