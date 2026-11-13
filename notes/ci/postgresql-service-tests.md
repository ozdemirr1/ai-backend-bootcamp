# PostgreSQL service tests — Week 18

13 November 2026: service container, needs, env/secrets and minimum-token-permission
learning progressed from the connection lab to guarded product CI.

- needs controls job order; it does not transfer the service database to another job.
- Runner localhost port mapping is not necessarily PostgreSQL inet_server_addr().
  The learner observed loopback from DB and 172.20.0.3 from API on the same database.
- Docker --network container:<id> shares network namespace, including loopback;
  it does not share filesystems. The CI source checkout is mounted separately.
- Each product job creates a fresh test DB and restricted owner, verifies actual
  DB/user/address/port/role flags, migrates, then enables only its selected suite.
- Schema tests change schema; data fixtures delete synthetic rows. Neither belongs
  on a development or hosted DB. Exact guards stay unchanged.
- CI uses no production/repository secrets. A fresh generated password is masked,
  stored in a private temporary file and used with loopback SCRAM. Initial service
  trust is limited to fresh bootstrap; bridge TCP is rejected before tests.
- pg_isready is not password/schema validation. The preflight and tests provide
  additional evidence; a green image build alone proves none of this.

Failure: Path.open(opener=...) raised TypeError before product tests. needs skipped
all data work. Recovery used built-in open and a private-file regression test.
This was a real implementation error, not a deliberately injected experiment.

Verified implementation 72ee274: [PostgreSQL run](https://github.com/ozdemirr1/opsdesk/actions/runs/43417456376)
passed 5 schema and 281 data tests, separately, plus no Alembic drift. Wrong-target
and privileged-role rejection are tested before migration. End-of-session learner
restatement is pending; these automated results do not replace it.

References: [Docker shared container network](https://docs.docker.com/engine/network/),
[GitHub service context](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts).
