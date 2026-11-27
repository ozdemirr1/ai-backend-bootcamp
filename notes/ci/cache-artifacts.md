# CI dependency cache, artifacts and Redis application state

27 November 2026 — planned 22 November learning slice.

- Dependency cache reuses downloadable package data; the existing frontend
  setup-node npm cache does not replace npm ci or store node_modules.
- An artifact preserves a specific run output, such as JUnit XML. Uploading a
  report does not make failed tests successful.
- Redis application cache holds derived runtime data, independent of CI packages.
- The learner produced a local auth-limit XML report: 26 tests passed in 0.77s,
  zero failures/errors/skips and exit code 0. This is not a GitHub artifact yet.

The prepared Redis CI workflow uses a fresh service container, health checking,
runner loopback plus the dynamically assigned port, explicit Redis opt-in, and
only the two Redis integration modules. A report check rejects zero tests or skips.
Only the XML report is uploaded, including after test failure, for seven days.
Workflow publication and actual artifact inspection remain pending. No remote
success is inferred from writing YAML.

References:
- https://github.com/actions/setup-node
- https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts
- https://docs.github.com/en/actions/tutorials/use-containerized-services/create-redis-service-containers


Observed publication: Redis run 45917707971 on product commit f5144be passed.
The artifact was downloaded and parsed: 10 tests, no errors/failures/skips. This
checks the content of the saved report, not merely the workflow's green badge.


## Controlled connection failure — 27 November

Product commit aad1c10 deliberately changed only the CI test port to 1. Redis
service initialization succeeded, but run 45918303442 failed with ConnectionError:
127.0.0.1:1 refused the connection. The downloaded XML had 10 tests, 10 errors,
zero failures and zero skips. These are fixture setup errors, not failed business
assertions. Upload still succeeded; the subsequent no-skip check was skipped
because pytest had already failed. A healthy service does not prove the client
uses its mapped port. Commit c0d08f0 restores job.services.redis.ports[6379].

## Cache, limiter and future broker responsibilities

A broker holds messages describing work for a worker to execute. This is a future
Celery responsibility, not implemented today. Eviction removes keys under memory
pressure; persistence writes Redis state to disk for restart recovery. They solve
different problems and neither alone guarantees exactly-once job execution.

- Statistics cache contains derived counts: missing entries can be recomputed from
  PostgreSQL after authorization. Cache outage has bounded DB fallback.
- Limiter counters are admission state: silent eviction can grant fresh quota.
  Store errors fail closed with 503, but successful reads of lost state are not
  errors. Capacity, eviction and restart behavior need separate operational review.
- Broker messages represent pending work: dropping them like disposable cache can
  lose tasks. Separate broker instance/configuration is the intended future boundary,
  with persistence, capacity and delivery/idempotency reviewed in the Celery slice.

Prefixes or logical Redis database numbers separate names, not process memory,
eviction policy or crash/restart failure domains. Do not assume cache /0 and broker
/1 on one server provide infrastructure isolation. No broker, new service or live
configuration was created in this exercise.

Sources:
- https://redis.io/docs/latest/reference/eviction/
- https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
- https://docs.celeryq.dev/en/main/getting-started/backends-and-brokers/redis.html


## Learner review — planned 22 November

Dependency cache misses allow normal installation; missing Redis connectivity
prevents integration verification and must fail CI. Artifact upload preserves
evidence without changing test outcomes.

Pending tasks are not automatically reconstructible like derived statistics.
Recovery requires separately persisted intent and an explicit replay mechanism;
this will be revisited with the bounded outbox topic.
