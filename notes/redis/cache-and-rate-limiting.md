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
