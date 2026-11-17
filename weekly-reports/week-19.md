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

Commit/push and exact-head CI publication are separate from these local results.
Learner end-of-day explanation remains pending. Redis work begins with the next
planned key/value, TTL and cache-aside exercise, not from these passing SQL tests.
