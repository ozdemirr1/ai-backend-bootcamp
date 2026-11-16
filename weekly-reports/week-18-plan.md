# Week 18 plan — Compose and isolated database CI

10–16 November 2026. Planning status: not implemented. The [Month 5 agreement](../monthly-plans/month-05.md) is the authoritative source for scope and safety boundaries.

## 10 November preparation decision — not implementation yet

Week 17 closure verification moved to 10 November. Existing guard/config/migration
code was reviewed today; no service, volume, database or Compose file was created.
The first implementation session will begin with a small Compose DNS example,
followed by a bounded product skeleton. Acceptance tests will not be dropped if
the schedule becomes tight.

| Component | Planned boundary |
| --- | --- |
| API | Existing non-root image; port published only on host loopback; same-origin React/API |
| PostgreSQL | Separate Compose project and new named volume; do not use existing host or visaassist volumes; no host port published by default |
| Redis | Internal-network service; no host port; connectivity/service foundation in Week 18, product cache/limiter in Week 19 |
| Migration | One-shot service; starts after DB health succeeds; API requires successful completion |
| Config | Tracked .env.example contains only empty/example fields; local .env is ignored; fail early if a required secret is missing |
| Privileges | Separate bootstrap administration, migration and runtime roles; do not pass migration/admin passwords to the API |
| CI test DB | From the runner: 127.0.0.1:5432 / opsdesk_product_test; preserve the existing test runner role and guard |

The proposed Compose development DB is `opsdesk_compose_dev`, with roles
`opsdesk_compose_migrator` and `opsdesk_compose_app`. These have not been created
yet. Do not run destructive tests on this DB. Tests target only the guarded
`opsdesk_product_test` database.

Existing development migration code accepts only the host/port/DB/role combination
127.0.0.1:5432 / opsdesk_product_dev / opsdesk_product_app; the test guard also
rejects service names. Rather than changing existing targets, design a separate
`compose` migration target and review it with target/role/connection verification
and rejection tests. Keep the existing test target unchanged for CI.

CI preparation: order schema and data jobs with `needs`. Jobs do not share a
database; each bootstraps/migrates its own disposable PostgreSQL service. Tests
run on the runner; do not confuse this with localhost inside a container. Do not
run schema/data suites concurrently on the same DB. Use no production secrets;
do not expose privileged tokens/secrets to untrusted PR code. Close Q03 #25 only
after acceptance evidence. Align PostgreSQL 18 compatibility with existing test
documentation; verify the image patch/digest choice during implementation.

Deletion rule: prefer `docker compose stop` for normal session shutdown. `down`
removes containers/networks, and `down -v` also deletes volume data; do not use
either for cleanup without user permission. Preserve existing resources. Rendered
`docker compose config` output may contain secrets; do not share or log it.

Initial sequence: small DNS example → product service/config skeleton → separate
migration target and role/bootstrap setup → readiness/cold start → guarded DB CI
→ restart/restore evidence. Preserve existing backend/frontend/Docker CI. Today's
preparation does not mark these outputs complete.

Sources: [Compose startup conditions](https://docs.docker.com/compose/how-tos/startup-order/),
[PostgreSQL service with a runner job](https://docs.github.com/en/actions/tutorials/use-containerized-services/create-postgresql-service-containers).

## 16 November review reference

The initial plan and unchecked boxes below are preserved as historical planning.
Completed work and publication boundaries are listed in the
[16 November weekly review](week-18.md). Learning/local acceptance is complete;
Q03 awaits closure through the normal PR/merge process.

## Learning and implementation method

Follow concept → small example → OpsDesk implementation → controlled failure →
test → learner explanation. Do not skip GitHub Actions fundamentals because CI
already exists. The daily table sets the initial sequence; do not start dependent
work before the learning checkpoint is passed.

## Daily work

| Day | Work | Expected evidence |
| --- | --- | --- |
| 10 November | API/PostgreSQL/Redis services and internal DNS/port/volume design. | docker-compose.yml skeleton and .env.example. |
| 11 November | Separate DB bootstrap roles and a one-shot Alembic migration service. | Setup from an empty volume; API does not start if migration fails. |
| 12 November | Healthcheck/readiness and application connection retry boundaries. | Cold-start, delayed-DB and missing-config experiments. |
| 13 November | Learn Actions needs/service containers/env/secrets/minimum permissions; implement Q03 guarded PostgreSQL schema/data CI. | Sequential migration/data jobs; test-target rejection check. |
| 14 November | Volume persistence across restart and isolated backup restore; Linux log reading. | Data is preserved; ordinary down does not delete volumes. |
| 15 November | Single-command acceptance; diagnose a failed CI DB connection; examine reverse proxy and HTTP/TLS concepts. | Notes on ports, service DNS and HTTP/TLS boundaries; no new live proxy. |
| 16 November | README and weekly report; CI/review; check Q03 acceptance. | Close #25 if evidence is sufficient; no automatic closure. |

## 15 November update — combined 14–15 November work

Preserve the original daily schedule as historical planning. The tasks below are
not yet considered complete; they are combined into one session sequence based
on the 13 November evidence.

1. Check disk/Docker/Compose status and existing Git changes.
2. Start with a small named-volume example, then verify that a synthetic OpsDesk
   record retains the same identity and content after stop/start. Earlier readiness
   recovery alone does not prove data persistence. No deletion/recreation experiment.
3. Take a backup and restore only to a new, isolated target. Verify source/target
   identities first; compare records, relationships and sequence behavior. Do not
   overwrite existing development/live data or put backups in Git/logs. Do not
   delete resources without permission.
4. Read timestamped Linux/container logs alongside earlier experiments. Introduce
   a separate controlled CI DB connection failure, diagnose it from logs and
   verify recovery. The earlier Path.open error does not count as a DB connection failure.
5. Build a single-command acceptance check from existing health/static/role checks;
   actually run it and record results. Do not run a destructive suite on the dev DB.
6. Explain reverse proxy, HTTP/TLS and forwarded-header trust boundaries using the
   existing OpsDesk deployment; do not add a live proxy or perform a deployment.
7. At the end of the day, collect the outstanding 13 November needs/network/guard
   explanation and the combined session's learning review; update existing weekly
   report/notes, then commit/push.

Do not add already completed schema/data CI setup and timeout/missing-config
experiments back to the task list. Run required regression checks according to
the changes. The 16 November weekly review, Q03 acceptance and PR/merge decision
remain separate. If disk space or learning evidence is insufficient, carry work
to the next session; do not close it merely to meet the date.

## Tests and acceptance

- [ ] fresh volume startup; restart persistence; migration failure; missing env; bounded connection failure; schema then data tests
- [ ] Preserve relevant regression checks, Ruff and existing frontend CI.
- [ ] Do not run destructive tests against local development or hosted data.
- [ ] The learner can explain the code's failure and data boundaries.

## Learning evidence

- [ ] The learner repeats a small implementation step and explains its rationale.
- [ ] A controlled application/CI failure is diagnosed from logs and corrected.
- [ ] Notes distinguish predictions, observed results and lessons learned.
- [ ] Why does runner localhost differ from localhost inside a service? How are CI secrets separated from local environment configuration?

Planned topic notes: notes/docker/compose-networking.md; notes/ci/postgresql-service-tests.md. This plan does not claim that these notes are complete.

## Notes and closure

Keep weekly concept notes organized by topic under `notes/`; create the Week 18
report when actual work begins. Do not create separate daily reports.
`feature/week-18-compose-postgres-ci` is the suggested feature branch name;
this plan does not create the branch. Use small, meaningful commits, review and
normal PR merges. Record test counts, durations and release results only after
execution.

## Learning questions

- Why does a running container not mean the DB is ready?
- How does a volume differ from an image?
- Why separate migration privileges from runtime privileges?

Reassess remaining work and capacity midway through the week. Starting the next
week requires verification of this week's dependencies; the schedule does not
take precedence over safe testing.
