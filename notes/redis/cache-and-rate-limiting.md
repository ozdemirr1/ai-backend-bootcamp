# Cache and rate limiting

## 17 November — establish an uncached baseline

A cache can preserve incorrect data efficiently. First establish the authorized
SQL result and tests before adding cache-aside.

For Ticket statistics, apply Organization and requester visibility before GROUP BY
and COUNT. An empty authorized result is a successful zero response; missing access
is an error. Counts themselves can disclose another customer's activity.

OpsDesk reuses its current Ticket visibility query. Actor, membership and
Organization state and counts share one database statement snapshot; a previously
loaded ORM membership must not grant stale staff visibility after role demotion.
The service fills all four known status counters, including zeroes.

The learner's small SQLite experiment demonstrated 2 customer / 3 staff / 4
unscoped Tickets. Product PostgreSQL tests are recorded separately in Week 19.
TTL, cache keys, invalidation and limiter behavior remain planned, not implemented.

## 19 November — cache-aside and bounded fallback

Redis is a separate data service that primarily keeps working data in RAM. Here,
PostgreSQL remains authoritative and Redis stores short-lived derived counts.
A key identifies a value; TTL limits its lifetime. Hit means a usable value is
present, miss means the application must compute it. Zero counts are valid hits.
Cache-aside means the application manages lookup, DB fallback and cache population.

Current access is checked before every lookup. Cache keys are scoped by environment,
contract version, Organization, actor, membership and own/all visibility. A cache
hit avoids aggregation but does not avoid the fresh authorization query. Role
changes between authorization and counting must not populate the wrong scope.

Initial local defaults: 30-second TTL, 200 ms connect/socket timeouts, no retries,
10 pooled connections. These are starting tradeoffs, not measured production SLAs.
A socket timeout is per operation, not an absolute request deadline. Cache failure
falls back to PostgreSQL, without hiding DB errors or bypassing authorization.
Only fixed event names are logged; no raw keys, payloads or exception credentials.

TTL bounds staleness but does not refresh counts after writes. Commit-aware
invalidation and stale-fill races remain the next learning slice. Redis CI and
rate limiting are not implemented in this increment.

Learner review completed on 19 November: current authorization precedes cache use,
even on a hit; bounded waiting prevents an unavailable cache from indefinitely
blocking DB fallback. The 200 ms setting is per operation, not an end-to-end SLA.
The learner independently passed all 13 focused cache tests in 0.31s.


## 24 November — planned 20 November limiter contract

Status: agreed learning contract; no product limiter implementation yet. The
original daily plan remains unchanged. Atomic Redis implementation and concurrent
request tests belong to the planned 21 November work.

### Window and counting rules

A window groups requests into a bounded time interval. The sequential in-memory
lab allowed three requests in ten seconds, starting with the first accepted
request. Attempts at t=0,1,2 succeeded; t=3,9 were rejected with remaining waits of
7 and 1 seconds; t=10 began a new window. Another client key had independent quota.
The learner supplied the expected output and PASS. This is not concurrency or
Redis integration evidence.

| Rule | Login | Register |
| --- | --- | --- |
| Initial local threshold | 5 attempts / 60 seconds | 3 attempts / 10 minutes |
| Counted outcomes | Successful and unsuccessful attempts | Successful and unsuccessful attempts |
| Admission point | After request-body validation, before credential verification | After request-body validation, before account creation |
| Quota scope | Client IP | Client IP |
| Exhausted quota | 429 with Retry-After | 429 with Retry-After |
| Store unavailable | Safe 503; do not execute login | Safe 503; do not create account |

These thresholds are local starting choices, not validated production settings.
Validation-rejected bodies are outside this application counter; it is not a
complete HTTP traffic limiter. Rejected requests do not extend the window.
The initial window begins at the first admitted attempt and is renewed after
expiry. Login and register use separate quotas. An admitted attempt consumes a
slot regardless of the eventual authentication or registration outcome.

### Decision 3 — key scope and limitations

Keys separate environment, policy version, operation and client-IP identity:
`opsdesk:<environment>:auth-limit:v1:<login-or-register>:ip:<client-identity>`.
This is conceptual notation. The exact IP encoding/privacy representation is an
implementation detail still to be specified. Passwords and JWTs never enter keys;
raw IPs and sensitive keys are not logged. No account-scoped quota is included in
this first bounded implementation.

Users behind a shared school/office/Wi-Fi public IP share quota and can block one
another. Distributed sources receive separate quotas. IP-only limiting is not
complete account protection; this limitation is explicit rather than hidden.

### Decision 4 — proxy trust

Direct local connections use the transport client address. Application code must
not manually trust a client-supplied X-Forwarded-For value. Only explicitly trusted
proxy sources may supply forwarded client information through the configured
server/proxy boundary. Concrete trusted addresses and deployment configuration
require verification during implementation; no live proxy settings change here.
A caller must not acquire a new quota simply by changing a forged header.

### Decision 5 — rejection and outage behavior

429 means the limiter was reachable and quota was exhausted. Retry-After conveys
remaining window time in whole seconds, rounded up; it is not an instruction the
client is forced to obey. Each repeated request is checked again.

503 means the limiter could not establish quota safely. This fail-closed policy
prevents login/register execution during store failure. A per-process fallback
counter cannot preserve the shared quota. By contrast, statistics cache failure
can fall back to PostgreSQL because authoritative counts remain computable.
An outage must not be mislabeled as a known quota exhaustion. Response bodies
preserve the product's safe error contract and never expose connection details.

### Learner review

The learner correctly explained forged forwarded headers and quota bypass,
fail-closed 503 versus cache DB fallback, and shared-IP collateral blocking.
The planned 20 November learning review is complete. The written policy is not
proof of enforcement; atomicity, expiry, concurrent requests, spoofing and outage
behavior still require the planned implementation and tests.
