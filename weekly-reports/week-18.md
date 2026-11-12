# Week 18 — Compose and guarded PostgreSQL CI

## 10 November 2026 — preparation only

Week 17 closure verification took place today. Docker Engine 28.5.1 and Compose
v2.40.2-desktop.1 answered; 7.4 GiB was free before the repeat build and no
containers were initially running. No existing resources were deleted.

Reviewed existing settings, local bootstrap, Alembic target selection, exact
integration guard and development connection verification. The existing guards
reject a Compose service hostname. Planned separate Compose migration target,
role separation, internal DNS, isolated named volume, fail-fast local secrets,
and runner-hosted PostgreSQL tests are described in the
[Week 18 plan](week-18-plan.md).

No Compose YAML, env file, database, role, volume, Redis integration, migration
implementation or PostgreSQL CI job was created. Q03 remains open. First learning
step is a small Compose DNS example before implementing the product skeleton.
Remaining dates are targets, not completion evidence.

## 11 November 2026 — planned 10 November DNS lab and product skeleton

Learner terminal evidence: Compose v2.40.2-desktop.1 created a separate temporary
lab network and web/client containers. `web` resolved to 172.19.0.2 and returned
HTTP 200; client loopback refused the connection. Web logs recorded the successful
GET from 172.19.0.3, not the failed client-local request. Both services were stopped
without deletion. This verifies the small example, not product DB connectivity.

OpsDesk branch feature/week-18-compose-postgres-ci starts at published main
7dfed5a. Added docker-compose.yml, empty .env.example and docs/compose.md with a
README link. API uses loopback 8089 and the application profile; DB/Redis have no
host ports and share an internal data network. PostgreSQL 18 volume target is
/var/lib/postgresql; Redis storage is ephemeral. API receives no bootstrap admin
password. The app/migrator roles, bootstrap and migration gating are not built.

Config-only checks passed using in-memory dummy values: service set, loopback
binding, network isolation declaration, volume target, admin-secret separation,
and missing/empty required-value rejection. Full rendered config was not printed.
Git ignores .env/.env.local but permits .env.example. No image was pulled, no
product service/volume/DB was created, no integration test was run. Disk had only
944 MiB free at inspection; runtime work must reassess capacity. Official image
tags were inspected; registry digest/pull/runtime validation remains pending.

The next step is learner review of the skeleton, then separate role/bootstrap and
compose migration target implementation. Existing exact test/dev guards remain
unchanged. This is not a complete working Compose stack or a Week 18 acceptance.

## 11 November — role separation, migration gating and runtime

After user disk cleanup, free space was 5.2 GiB. Docker Desktop was stopped; it was
opened and Engine 28.5.1 responded. Existing visaassist and all other resources were
preserved. Image pulls/build and two isolated local PostgreSQL setups left 3.3 GiB.

Added a separate compose migration target, strict db:5432 / opsdesk_compose_dev /
opsdesk_compose_migrator guards, connected identity/role checks, explicit runtime
grants, and one-shot migration success gating API startup. Existing hosted/dev/test
guards were not widened. Ignored mode-600 .env was created with independent random
local credentials; no secrets were printed or committed.

Focused guard/migration tests: 100 passed. Backend non-integration regression:
773 passed, 286 deselected (10.21s). Additional permissions tests: 3 passed.
Final Ruff lint/format passed (145 files). No destructive DB tests were run.

First bootstrap encountered bad-interpreter permission denied on the bind-mounted
shell file; PostgreSQL init had already created the volume. The volume was kept,
role absence verified, and initialization explicitly completed without reset.
The final configuration mounts SQL directly. A second fresh project/volume then
proved bootstrap -> DB healthy -> migration exit 0 -> API started automatically.
Both setups returned readiness 200. Primary setup passed root HTML/liveness,
synthetic registration/login/profile/organization list and creation. Redis PONG.
App-role SQL checks verified absence of schema CREATE, DELETE, migration-table
write and migrator membership. Generated secrets were absent from captured logs.

A separate no-network/no-DB rejection experiment used an unsafe migration target:
migration exit 1 and API remained Created. No dummy DB operation occurred. Main
local project opsdesk-compose-dev remains running on 8089. Fresh proof project
opsdesk-compose-fresh-20261111 was stopped; failure project
opsdesk-migration-reject-c59ded is retained. No containers/volumes/images deleted.

This closes implementation evidence for the planned 10–11 November slice, not
Week 18 acceptance or independent learner mastery of the new code. Learner should
inspect depends_on, dedicated credentials and the rejection result next. Delayed
DB/retry, restart persistence, restore and PostgreSQL CI remain pending.

## 12 November 2026 — readiness, timeout and bounded retry learning closure

Evidence source: Furkan's supplied terminal outputs and end-of-session explanation.
These experiments were run by the learner; they were not independently rerun during
this documentation closure. No new product code or regression run is claimed.

### Predictions and observations

| Exercise | Expected behavior | Observed evidence |
| --- | --- | --- |
| Delayed dependency simulation | Migration waits for health; API waits for migration success | Dependency ready at 14:16:41.016 UTC, migration completed at 14:16:41.481, API started at 14:16:42.092; Compose exit 0 |
| Local OpsDesk DB outage | API stays alive but loses readiness | Before stop: readiness 200 (0.155451s). During outage: liveness 200 (0.018921s), readiness 503 (0.020214s); API remained Up |
| DB recovery | Readiness recovers without restarting API | First polling attempt returned ready; DB healthy and API retained its uptime |
| Missing required configuration | Fail before startup | With env-file disabled and four variables unset, JWT interpolation failed; exit 1. Normal config validation exited 0 |
| Accepted TCP connection without PostgreSQL response | Connection timeout and bounded experiment retry | Two timeouts: 2.07s and 2.09s, one 1s retry delay, total 5.15s; assertions passed and container command exited 0 |

The delayed-dependency lab used Python and a readiness marker, not a delayed real
PostgreSQL server. It verified Compose startup conditions. The real outage exercise
stopped and restarted only the local Compose DB; no deletion/reset occurred. The
lab services were stopped and retained. The timeout lab used an isolated network-none
container and its loopback fake listener with the actual OpsDesk connection factory;
random synthetic credentials were not printed. It did not connect to a real DB.

Structured API logs recorded ready 200 -> live 200 -> ready 503 -> ready 200 with
unexpected_error=false. This is handled dependency failure, not an API crash.
The initial rg command was unavailable in the learner's shell; grep -nE provided
the equivalent configuration inspection without installing a new tool.

### Learning review and implementation decision

Furkan explained why whole-Ticket-write retry can duplicate a successfully committed
operation after its response is lost, distinguished connection establishment from
writing/commit, and identified cumulative waiting/resource cost. Clarifications:
not every failure stage is ambiguous; a known pre-connection failure differs from
an unknown commit outcome. Waiting consumes request resources but does not imply
that every API worker is blocked. Persistent idempotency remains later work.

Timeout is a bound, not a mandatory delay: connection refusal can return promptly.
The two-attempt loop belonged to the experiment, not automatic product retry.
First-attempt readiness recovery did not exercise the polling loop's retry branch.
The observed connection timeout does not establish a SQL statement deadline or an
end-to-end HTTP request deadline. Existing pg_isready health does not verify app
credentials, schema or table privileges; /health/ready currently probes SELECT 1.

No new retry implementation is justified by these results. The planned 12 November
experiments and learner review are complete within these limits. Week 18 still
requires PostgreSQL schema/data CI, dedicated persistence/restore evidence and
weekly acceptance; simple DB restart/readiness is not row-persistence verification.
