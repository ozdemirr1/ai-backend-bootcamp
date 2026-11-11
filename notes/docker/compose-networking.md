# Compose networking — Week 18

## 11 November 2026 lab evidence

Compose creates a project network and registers service names. In the learner's
two-service lab, client requested web:8000 and received 200 without publishing any
host port. web resolved to 172.19.0.2; this address is an observation, not a value
to hardcode. Client localhost:8000 refused the connection because no HTTP server
was running in that client container. The web log contained only the successful
GET, from 172.19.0.3. Both containers were stopped, not deleted.

In OpsDesk the corresponding addresses are db:5432 and redis:6379. The Mac reaches
API through loopback 8089 -> container 8000. Container-to-container traffic uses
the service port; it does not need a published host port. The product configuration
is currently a skeleton, not observed runtime behavior.

PostgreSQL's named volume stores data separately from the container. PostgreSQL 18
uses /var/lib/postgresql as the mount target. Redis is ephemeral for this initial
connectivity exercise. Volume persistence will need an actual restart test later.

An application profile selects a service; it does not check readiness. A running
DB container is not proof that roles, migrations or application permissions exist.
Those checks belong to the next bounded exercise.

## Migration startup dependency

The product now waits for TCP PostgreSQL health, then runs the guarded migration
and explicit permission setup. API depends on migration's successful completion.
Observed positive case: healthy DB -> migrate exit 0 -> API running/readiness 200.
Observed negative case: unsafe target -> migrate exit 1 -> API never started.
This dependency is a startup condition, not continuous supervision if DB fails later.

Admin, migration and API credentials are independent. API cannot create schema,
delete business rows, write Alembic's version table or assume the migrator role.
Existing row-lock queries require column-level UPDATE grants even for some read
paths; this is a database privilege detail, not a substitute for API authorization.
