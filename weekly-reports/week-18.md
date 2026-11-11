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
