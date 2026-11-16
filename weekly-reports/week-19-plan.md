# Week 19 plan — Redis cache and rate limiting

17–23 November 2026. Planning status: not implemented. The [Month 5 agreement](../monthly-plans/month-05.md) is the authoritative source for scope and safety boundaries.

## 16 November preparation — implementation has not started

Week 18 local Compose, role/migration, persistence/restore and CI learning evidence
was reviewed. Four workflows passed for product branch commit ec645a4; #25 and
PR/merge publication remain open. Check merge status and the branch base before
starting product code; do not lose Week 18 dependencies. The new branch name is
`feature/week-19-redis-cache-limits`; no branch or Redis feature is created today.

### Bounded product contract

- Start without caching: `GET /organizations/{organization_id}/ticket-stats`
  counts Tickets by existing status. Customers see only their own Tickets; staff
  see records within the same organization. Test empty results, foreign organizations,
  missing/invalid sessions and customer/staff separation. Preserve the existing
  error contract.
- Every request checks current authorization before accessing the cache. Keys
  separate organization, user/visibility scope and contract version. A role change
  or switch to another user must not obtain authorization through stale cache data.
  No new React screen.
- Learn cache-aside through a small key/value/TTL example. Choose and justify TTL
  and connection timeout before implementation. Redis outages allow bounded DB
  fallback; authorization is not skipped. Hit/miss tests observe actual query behavior.
- Invalidate after a Ticket creation commit, not after rollback. Use a deterministic
  race test for an old query repopulating the cache after a new commit. Priority
  changes do not trigger unnecessary invalidation for status-only counts.
- Specify login/register limiter thresholds, windows, keys, trusted proxy sources
  and Redis outage behavior first. Proposed policy: 429/Retry-After at the limit,
  safe 503 on store failure. Test atomic counter+expiry behavior and parallel requests.
  Do not log passwords/tokens or raw sensitive keys; do not change JWT/session design.

### Experiment and CI boundaries

Each topic follows rationale → small example → bounded product implementation →
controlled failure/logs → tests; collect the learner's explanation at the end of
the day. Examine GitHub Actions dependency cache, artifacts and Redis application
cache separately. Run Redis integration tests in an isolated CI service; do not
mix test data/keys into the existing development service. PostgreSQL destructive
tests remain restricted to guarded `opsdesk_product_test`. Separate eviction and
persistence responsibilities for cache/limiter and next week's broker; Celery
does not start today.

Review capacity on 20 November. If authorization, race or outage tests are missing,
do not mark the scope complete; extend the schedule. This plan does not authorize
live Redis/proxy setup, a new paid service or automatic deployment.

## Learning and implementation method

Follow concept → small example → OpsDesk implementation → controlled failure →
test → learner explanation. Do not skip GitHub Actions fundamentals because CI
already exists. The daily table sets the initial sequence; do not start dependent
work before the learning checkpoint is passed.

## Daily work

| Day | Work | Expected evidence |
| --- | --- | --- |
| 17 November | Scoped ticket-stats endpoint contract and uncached query. | Organization/customer/staff count tests; no frontend change. |
| 18 November | Redis key/value, TTL and cache-aside; key scope design. | Hit/miss after authorization checks and bounded timeout. |
| 19 November | Post-commit invalidation; concurrent stale cache write race. | Create/rollback/TTL and stale-fill tests. |
| 20 November | Login/register rate-limit contract; choose thresholds, keys, proxy and store-failure behavior. | Written 429/Retry-After/503 policy. |
| 21 November | Atomic limiter implementation and parallel-request tests. | Expiry, correct counters, proxy-spoofing and outage tests. |
| 22 November | Actions dependency cache/artifacts versus Redis cache; Redis integration CI and connection-failure diagnosis; broker isolation. | Cache fallback and limiter failure behavior verified separately. |
| 23 November | Notes, regressions, PR and weekly report. | Learner explains TTL/invalidation and the session/cache distinction. |

## Tests and acceptance

- [ ] tenant/customer/staff separation; hit/miss; TTL; post-commit invalidation; rollback; race; Redis unavailable; concurrent limiter
- [ ] Preserve relevant regression checks, Ruff and existing frontend CI.
- [ ] Do not run destructive tests against local development or hosted data.
- [ ] The learner can explain the code's failure and data boundaries.

## Learning evidence

- [ ] The learner repeats a small implementation step and explains its rationale.
- [ ] A controlled application/CI failure is diagnosed from logs and corrected.
- [ ] Notes distinguish predictions, observed results and lessons learned.
- [ ] How does dependency cache differ from application cache? Why is a cache miss not necessarily a test failure?

Planned topic notes: notes/redis/cache-and-rate-limiting.md; notes/ci/cache-artifacts.md. This plan does not claim that these notes are complete.

## Notes and closure

Keep weekly concept notes organized by topic under `notes/`; create the Week 19
report when actual work begins. Do not create separate daily reports.
`feature/week-19-redis-cache-limits` is the suggested feature branch name;
this plan does not create the branch. Use small, meaningful commits, review and
normal PR merges. Record test counts, durations and release results only after
execution.

## Learning questions

- Why does cache not replace authorization?
- Why is TTL alone not invalidation?
- Why must limiter INCR and expiry be considered together?

Reassess remaining work and capacity midway through the week. Starting the next
week requires verification of this week's dependencies; the schedule does not
take precedence over safe testing.
