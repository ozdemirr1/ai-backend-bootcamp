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


## 21 November — planned 19 November generation invalidation

The learner reproduced stale cache reads, commit/rollback ordering and delayed
stale-fill with small in-memory examples, then demonstrated generation 7 keeping
the old count 2 while generation 8 returned 3. These are learning examples, not
Redis or PostgreSQL integration evidence.

OpsDesk now captures an Organization generation before counting and fills only
that generation. Successful Ticket creation rotates it after commit; rollback
leaves it unchanged. Result keys retain actor, membership and visibility scope.
Missing generation metadata uses fresh random tokens with SET NX; initialization
losers use the winning token. Metadata expires at twice the result TTL. Read
failure bypasses cache; rotation failure preserves committed creation and logs
only a fixed event name. This is best-effort freshness, not cross-store atomicity.
A delayed fill after failed invalidation means TTL is not a hard commit-relative
freshness bound. Cache remains disabled by default.

Local verification: 828 non-integration tests passed (9.20s), followed by 37
focused tests after metadata-expiry adjustment (0.42s). Guarded PostgreSQL tests:
288 passed, 3 Redis tests skipped (24.62s), no schema drift. The deterministic SQL
race commits a second Ticket between count and cache fill; the next read sees 2
instead of the old 1. Ruff and formatting checks passed. Real Redis validation
remains pending: Docker start stalled and an 8-second server probe timed out.
No resources were deleted. No commit, push, merge or deployment in this increment.
Remaining: run the three Redis cases, learner review and publication closure.


### Redis verification recovered — 21 November

After the learner restarted macOS, Docker Engine 28.5.1 responded again. The
existing isolated `week19-cache-verification` container was started with its
loopback-only ephemeral port. All three real Redis tests passed in 1.51s:
miss/hit/expiry and malformed payload, bounded timeout against an unresponsive
TCP peer, and generation rotation isolating a delayed stale fill. This resolves
the Redis verification blocker above. No resources were deleted. Learner review
and commit/push closure remain pending; cache is still disabled by default.


### Learner review and publication — 21 November

The learner correctly explained why a reader captures its generation before
counting and writes to that same generation: fetching the new generation after
counting would label an old result as current. They also explained that a
successful Ticket commit must not be retried after Redis invalidation failure,
because creation has already persisted and repetition could create duplicates.
Review clarified that TTL starts at cache write time, not database commit time;
a delayed stale fill prevents a hard commit-relative freshness guarantee.

Product commit `44374f0` publishes the generation implementation and tests on
`feature/week-19-redis-cache-limits`. Local evidence above closes the planned
19 November learning checkpoint. Remote CI is tracked separately; no main merge
or deployment is included. Cache remains disabled by default.


## 24 November — planned 20 November limiter policy and learner review

The learner supplied successful output for the sequential three-requests-per-ten-
seconds lab, including rejected attempts, expiry and separate client keys. Login
and register policy decisions 3–5 and thresholds are recorded in the
[Redis notes](../notes/redis/cache-and-rate-limiting.md#24-november--planned-20-november-limiter-contract).
The local starting contract is IP-scoped login 5/60s and register 3/600s, separate
operation keys, admitted successes/failures counted after body validation, no
window extension on rejection, 429/Retry-After on exhaustion and safe fail-closed
503 on store failure. Only explicitly trusted proxy sources may supply forwarded
client information. Shared-IP collateral blocking and distributed-source bypass
are acknowledged limitations. Concrete proxy addresses and key encoding remain
implementation details to verify, not established live configuration.

The learner correctly explained all three review questions: forged
X-Forwarded-For can bypass naive IP counters; unavailable limiter state cannot be
replaced with independent process counters; shared public IPs share quota.
Planned 20 November learning and contract work is complete locally. No product
limiter, runtime test, live setting or revised roadmap was introduced. Subsequent
implementation remains the planned 21 November work. This documentation
checkpoint closes the planned 20 November learning and policy scope.


## 24 November — planned 21 November atomic authentication limiter

Learner lab evidence: the split check/increment example admitted two requests for
one remaining slot (counter 4, limit 3). The Lua lab admitted only the last slot;
10 parallel requests produced exactly 3 admissions and 7 rejections. The expiry
lab reopened quota after expiry and rejected a counter missing its expiry. These
were isolated Redis examples, not yet product evidence.

The product now has an optional authentication limiter, disabled by default.
POST /auth/login and POST /users enforce the agreed IP quotas after valid body
parsing and before the service business method. The Lua adapter validates state
before mutation; exhaustion is 429 with rounded-up Retry-After, while Redis errors,
invalid counters/replies and unusable client addresses fail closed with safe 503.
Keys separate operation/environment and hash canonical IPs (not anonymization).
The application does not parse forwarded headers itself. Direct spoofing and
Uvicorn trusted/untrusted peer behavior are tested. No live proxy trust or Redis
service was configured, and no hosted enablement occurred.

Verification: 853 non-integration tests passed (10.06s), followed by the expanded
26-test limiter suite (0.98s), including owned-client lifecycle. The final real
Redis run passed 10 tests (3.95s): 7 limiter and 3 cache tests, including parallel
admission, expiry, corrupt state and HTTP enforcement. Guarded PostgreSQL data
regressions passed 288 tests (25.01s); 10 opt-in Redis cases were skipped in that
separate run, and Alembic detected no drift. Ruff and formatting checks passed.
One intermediate Redis rerun used an obsolete ephemeral port and failed during
fixture setup; querying the container's current port corrected the test setup.
No application change was needed for that connection failure.

Implementation and local verification are complete for this slice. Learner final
review and commit/push remain pending. Remote Redis CI is still planned 22 November
work. Resource deletion, main merge and deployment were not performed.


### Learner closure and product publication — 24 November

The learner correctly explained that atomic INCR alone cannot protect a separate
check/admission/update sequence or the gap before expiry assignment. They also
explained that missing expiry is invalid store state (503), not known exhausted
quota (429), and that trusting arbitrary forwarded headers at Uvicorn can rewrite
request.client.host before application code sees it. Review clarified that expiry
is assigned for a new window, not refreshed for every accepted request.

Product commit `d19e502` publishes the optional atomic limiter and its tests on
`feature/week-19-redis-cache-limits`. The planned 21 November learning checkpoint
is complete. Remote CI results are tracked separately; the ten Redis integration
cases remain local opt-in evidence until planned 22 November Redis CI work.
Limiter stays disabled by default. No main merge or hosted deployment occurred.
