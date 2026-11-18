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
