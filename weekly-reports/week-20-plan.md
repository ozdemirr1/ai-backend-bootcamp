# Week 20 plan — Celery, retry, idempotency and system acceptance

Original roadmap dates: **24–30 November 2026**. Prepared for execution on
**28 November 2026** after Week 19 closure. Implementation has not started.
The [Month 5 agreement](../monthly-plans/month-05.md) remains authoritative.
This plan preserves its scope, daily order and historical target dates.

## Starting point and schedule

Week 19 product PR #53 merged as `2fbe552`; education PR #19 merged as
`3c3051a`. The five product workflows passed after merge. Cache and authentication
limiting remain disabled by default; this plan does not enable them in production.

The planned 23 November checkpoint completed on 28 November: a five-calendar-day
checkpoint lag. The next uncompleted learning slice is 24 November. That slice
is four calendar days earlier than today; this is a different comparison, not a
claim that only four learning sessions remain. All seven Week 20 slices remain.

Estimated active effort remains **24–32 hours**, not time already worked.
At one slice per day starting on 28 November, the illustrative completion date
would be 4 December. This is a capacity scenario, not an approved replacement
schedule. Reassess after the planned 27 and 29 November slices, whenever they
are actually completed. Do not skip tests or overlap unfinished Month 5 work
with Month 6 to meet the original 30 November target.

The linked Railway service had no active deployment and returned HTTP 404 at
Week 19 closure. Track hosted availability separately; local/CI acceptance is
not hosted release evidence. No provider migration, paid service or deployment
configuration change is authorized by this plan.

## Coverage of the original Week 20 brief

| Original goal | Planned delivery and evidence boundary |
| --- | --- |
| Background jobs, queues and workers | A small real Celery task demonstrates producer, broker and separate worker execution before reliability features are added. |
| Email simulation after Ticket creation | A committed Ticket event eventually produces a durable simulated notification through the outbox/worker flow; a rolled-back creation produces no event. |
| An "Email sent" log | Emit `notification_simulated` so logs cannot be mistaken for real email delivery. |
| Worker in Docker Compose | API and worker use the same application image with different commands; the broker has its own Redis instance. |
| Preparation for an AI task queue | Learn reusable background execution, failure handling and delivery boundaries. AI calls, prompts and AI-specific tasks remain Month 6 work. |

The original Month 5 wording mentioned Celery/RQ and cache/rate limit/session.
The approved agreement selected Celery, not both task systems. Cache and rate
limiting are implemented; session/cache distinctions are taught without moving
the existing JWT/session architecture into Redis. React is built into the
application image and served by FastAPI; a separate React container is not
required and will not be claimed.

Retry, durable idempotency and the bounded outbox deepen the notification example:
they address failed delivery and duplicate execution, not a new product domain.

### Linux and networking coverage

Review these concepts through actual Compose and worker debugging rather than
adding an unrelated infrastructure course:

- Process/PID/signals: distinguish API and worker lifecycles and observe shutdown.
- Ports/DNS: resolve broker/DB service names, distinguish container localhost from
  host localhost, and diagnose one controlled connection/configuration failure.
- HTTP/TLS/reverse proxy: explain TLS termination and trusted forwarded headers
  using the existing application boundary. Conceptual review does not claim
  hands-on Nginx or Caddy installation; no new proxy service is required.
- Environment/secrets: identify required configuration, verify safe failure for
  missing values, and keep credentials out of image layers, Git and artifacts.

## Learning method and new terms

Explain purpose and architecture before code. Follow concept → small analogous
example → learner prediction and execution → bounded OpsDesk change → controlled
failure and log diagnosis → tests → learner explanation. Existing test counts
are not a substitute for learning. Introduce these terms when first used:

- **Task:** one unit of background work, such as a simulated Ticket notification.
- **Queue:** messages waiting to be processed.
- **Broker:** the service that transports task messages from producer to worker.
- **Worker:** a separate process that consumes and executes tasks.
- **Celery:** the Python task-processing system connecting producers, broker and workers.
- **Retry:** another attempt after a failure; it is not safe for every operation.
- **Backoff / jitter:** increasing retry delay / randomized variation in that delay.
- **Timeout:** a bound on waiting or execution; connection, task and CI job limits differ.
- **Idempotency:** repeated processing of the same logical event produces one logical result.
- **Outbox:** committed event intent stored in the same database transaction as the business change.
- **Dispatcher:** a small process that publishes committed outbox events to the broker.
- **Acknowledgement:** a worker/broker delivery signal; it is not proof of exactly-once business effects.

## Product boundaries and staged architecture

Keep `src/opsdesk`, the existing React behavior and the shared application image.
API and worker use different commands from that image. Start with a logging-only
notification simulation, not real email, AI or a new frontend feature.

Use a separate Redis broker instance from cache/limiter storage. Separate logical
DB numbers or key prefixes do not isolate eviction, memory pressure or process
failure. Review persistence and eviction needs before relying on broker recovery.
Use environment configuration, internal networking and existing secret hygiene.
Do not add a result backend unless an observed requirement justifies it; durable
simulation outcomes belong in PostgreSQL.

The final bounded flow is Ticket + outbox event in one PostgreSQL transaction →
small dispatcher → broker → worker → one durable simulated-notification result.
Build this in stages, not on the first day. Task payloads carry an event ID rather
than credentials or Ticket text. The worker reads the persisted event and checks
its Ticket/organization relationship; no request-scoped Session crosses processes.
Keep explicit synchronous transaction ownership and Alembic migrations.

A unique event constraint and transaction enforce one logical persisted result,
including duplicate/concurrent delivery. Logs explicitly say
`notification_simulated`; neither exactly-once log output nor exactly-once external
email is promised. Task idempotency does not prevent duplicate HTTP Ticket creation.

Before implementing the dispatcher, document event states, claiming/recovery,
retry limits and the meaning of published versus completed. Broker acceptance is
not worker completion. Publishing then crashing before recording publication can
cause redelivery; durable idempotency must tolerate it. Never mark an event sent
before attempting publication. Keep the dispatcher bounded, without building a
general-purpose event platform. Distinguish temporary broker outage from permanent
business failure, and make exhausted retries observable and recoverable by an
explicit procedure rather than silently discarded.

## Daily work in original roadmap order

| Planned slice | Learning and bounded implementation | Completion evidence |
| --- | --- | --- |
| 24 November | Learn task/queue/broker/worker with a small real-broker logging task. Add an isolated broker and Compose worker using the application image. | Show execution outside the API process; identify producer, broker and worker logs. Explain why the notification is only a simulation. |
| 25 November | Produce temporary and permanent failures. Select bounded retries, backoff/jitter and timeout behavior before implementing them. | Observe retry count, eventual success and exhaustion; permanent failures are not blindly retried. Explain connection versus execution versus CI timeout. |
| 26 November | Introduce an event ID and durable simulated-notification result through Alembic. Enforce uniqueness transactionally. | Repeated and concurrent processing of the same event yields one logical result; separate events and organizations remain independent. No real email. |
| 27 November | Review retry/idempotency learning. Reproduce Ticket commit followed by failed publication. Introduce the small outbox in the Ticket transaction. | Committed Ticket and event persist together; rollback leaves neither new record. Explain the commit/publish gap and HTTP versus task idempotency. |
| 28 November | Add the bounded dispatcher. Exercise broker outage, publish-before-record crash, worker restart and redelivery. | Pending work is recoverable after broker return; duplicate delivery has one durable outcome. Published does not mean completed; failed/exhausted work remains visible. |
| 29 November | Add real worker/broker CI smoke coverage and safe failure-log artifacts. Exercise full Compose startup and request/event/task correlation. | A real worker executes a task; eager-only tests are insufficient. Job timeouts, readiness, failure logs and scoped cleanup are explained. |
| 30 November | Run Month 5 acceptance, update README, weekly/monthly evidence and handoff, and explain the architecture independently. | Missing gates delay closure. Publish only observed results; normal PR merges preserve daily history. Do not start Month 6 before required dependencies pass. |

## Test, CI and safety contract

Destructive product tests remain restricted to guarded `opsdesk_product_test`.
Never use development or hosted data, weaken guards for container DNS, or run
competing DB suites against the same target. CI services and synthetic namespaces
are isolated; local resource deletion still requires the user's permission.

Extend the existing CI structure where appropriate rather than copying parallel
workflows for the same checks. Preserve Ruff, non-integration pytest, frontend,
Docker build, PostgreSQL and Redis checks. Use a real broker and worker integration
path in addition to fast unit tests. An eager test runs the task in the caller's
process and cannot prove broker delivery or worker lifecycle behavior.

Failure artifacts contain bounded, secret-safe service logs and test reports,
not environment dumps or credentials. Explain PR checks versus branch protection;
no paid feature or repository-policy change is assumed. Docker build alone does
not prove startup, readiness or successful task processing.

- [ ] Real broker/worker delivery and worker process separation demonstrated.
- [ ] Temporary/permanent failures, timeout, bounded retry and exhaustion verified.
- [ ] Duplicate/concurrent delivery produces one durable simulated result.
- [ ] Ticket/outbox commit and rollback boundaries tested.
- [ ] Broker outage and publish-gap recovery tested; worker restart behavior observed.
- [ ] Unrelated events and tenants remain unchanged; task payload/log privacy checked.
- [ ] Migration success gates DB-dependent API/worker startup; failed migration blocks them.
- [ ] Documented configuration followed by Compose startup and restart succeeds without deleting volumes.
- [ ] Existing regressions and real worker CI pass at the published commit.
- [ ] Learner diagnoses a controlled failure and explains the architecture without relying on green checks alone.

## Notes, publication and Month 5 handoff

Keep concept notes in `notes/celery/retry-idempotency.md` and
`notes/celery/commit-publish-gap.md`; create them when learning starts. Record actual
evidence in one `weekly-reports/week-20.md`, not separate daily reports. This plan
does not claim those notes, a worker or tests already exist.

Use `feature/week-20-celery-reliable-jobs` in each repository, based on verified
Week 19 main. The education branch carries this plan; create the product branch
when product work begins. Keep English repository documentation and meaningful
week-based commits. Review changes and use normal PR merges. Keep unrelated
LinkedIn assets out of scope.

At closure reconcile the Month 5 checklist against evidence, identify operational
carry-over including hosted availability, record the monthly report/handoff and
then start the next month in a new project-scoped conversation. CV claims must
match tested functionality; do not claim deployment from CI success.

## Month 5 closure gate and CV wording

Completing Week 20 closes roadmap Month 5 only after required acceptance gates
pass. Calendar dates alone do not establish completion. Before closure:

- [ ] Rebuild the documented development environment and verify restart/persistence.
- [ ] Demonstrate Ticket → committed event → worker → durable simulation outcome.
- [ ] Verify broker outage recovery, retry exhaustion and duplicate delivery.
- [ ] Preserve cache, limiter, authorization, frontend and CI regressions.
- [ ] Independently explain architecture and diagnose a controlled failure.
- [ ] Publish weekly/monthly evidence and handoff, separating completed work from
  operational carry-over with explicit next actions.

Hosted availability remains an open operational item. Automatic production deploy
is not a mandatory Month 5 learning gate, but a working live demo cannot be claimed
while the observed Railway endpoint returns 404. Required local/CI failures still
block closure; do not relabel them as optional carry-over to meet a date.

Proposed CV bullet, usable only after the corresponding evidence passes:

> Built a Docker Compose development environment with FastAPI, PostgreSQL, Redis
> and Celery workers serving a React frontend; implemented authorization-scoped
> caching, rate limiting and a retry-safe notification simulation.

This describes development and simulation evidence, not real email delivery,
separate React service deployment, production Redis rollout or exactly-once
external effects. Narrow the wording if any claimed capability remains unverified.

## Final learner questions

- Why does a worker run separately from the API, and what does the broker retain?
- Why can retries or acknowledgement timing cause duplicate execution?
- Which constraint makes one durable simulation outcome safe under concurrency?
- What happens if the process stops between database commit and publication?
- What does the outbox solve, and what delivery/recovery problems remain?
- Why are task idempotency, HTTP idempotency and real email exactly-once different?
- What does a real worker CI test prove that an eager test cannot?
