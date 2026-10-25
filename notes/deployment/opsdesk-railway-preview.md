# OpsDesk Railway preview — deployment notes

Recorded 19 October 2026. Learning notes, not a promise of production readiness.

## Request path and build

The browser loads `/` and `/assets/...` from FastAPI on the public Railway domain.
The built client uses `/users`, `/auth/login` and `/users/me` on that same origin.
Locally, Vite's `/api` proxy strips the prefix before contacting FastAPI; that
development proxy is not included in the production bundle.

`VITE_API_BASE_URL=/` is a build-time public setting. Runtime variables cannot
rewrite a bundle already built with another value. Secrets do not belong in
`VITE_*` variables. Node 24 builds the frontend; Uvicorn serves the resulting
files and Python API. `OPSDESK_FRONTEND_DIST_DIR` enables static serving; missing
required build files fail startup. Unknown API paths retain JSON 404 responses.

The single runtime simplifies origin handling and avoids another always-running
frontend process, but couples frontend and backend releases. Browser tokens stay
in memory: navigation preserves a session, full reload starts without it. Logout
clears client state; it is not a server-side JWT revocation system.

## Persistence and health

Alembic runs against an explicitly guarded hosted target. Migration and runtime
roles have different grants; schema changes are not delegated to normal requests.
Both credentials currently exist in the same service environment, which limits
secret isolation despite separate configuration prefixes.

Liveness checks application response. Readiness runs `SELECT 1` with bounded
connection/pool waits. It does not certify every table, grant or business flow;
actual registration/login smoke checks supply separate evidence. A deployment
healthcheck is not continuous uptime monitoring.

## Tester scope

External visitors can open the public panel, register a synthetic account, log in,
check their session and sign out. Use an invented unique address under example.com
and a password used only for this demo. Account data persists in the demo database;
there is no verified self-service account deletion flow. Demo data may be reset.
Do not enter real customer, support or confidential data. Tickets show mock records;
Ticket creation/listing integration and AI features are not part of this preview.

Source inspection on 19 October found no registration/login rate-limiting control.
Edge protection was not verified. Small manual feedback sessions are possible;
a broad invitation should follow the bounded exposure/cost review in the weekly plan.
Do not use the public trial service for load testing.

## Remaining operations work

- Current-head Backend and Frontend CI passed at `2f6e00d` on 19 October.
  Confirm runtime Git SHA and hosted negative/reload cases; recheck CI after changes.
- Define/test registration/login abuse policy and trusted proxy handling; document
  restart and replica limitations rather than implying a global guarantee.
- Record current credit usage and shutdown/export steps. USD 4.94 was an earlier
  screenshot value, not a live balance. No paid plan or uptime period is approved.
- Document export/restore with an isolated restore target; never run destructive
  integration tests on the demo. Backups have not yet been restore-verified.
- Distinguish code rollback from reversing database migrations and data changes.

## References

- [Railpack configuration](https://railpack.com/config/file/)
- [Vite environment variables](https://vite.dev/guide/env-and-mode)
- [Week 15 evidence](../../weekly-reports/week-15.md)

## 23 October Railway security incident decision

Railway [disclosed possible unauthorized access to customer environment variables](https://blog.railway.com/p/security-disclosure-wednesday-october-21st)
on 21 October. This is a provider incident, not evidence that this particular
OpsDesk project was accessed. Railway recommends rotating every secret stored in
Railway and reviewing logs. Its [23 October status update](https://status.railway.com/)
states that Trial and Free builds/deploys are running again; the security
investigation and customer notifications were still in progress at the checkpoint.
The dashboard's “Limited Access” banner is not sufficient evidence that the
current branch cannot deploy. Railway also warns that GitHub may need reconnecting.

Decision: keep the existing Railway preview for this Week 15 recovery, rather
than start an unplanned Azure migration during incident response. The
[GitHub Education Azure offer](https://education.github.com/pack) includes a
possible USD 100 student credit, but eligibility approval is not proof that an
Azure subscription is activated or that the app plus managed PostgreSQL will
fit a desired monthly budget. Reassess Azure after the Railway rotation, latest
deployment and a measured cost/backup review. Changing providers alone does not
invalidate potentially exposed database or JWT credentials.

Recovery checklist (planned, not yet executed):

1. Preserve available incident/audit evidence; review Railway deploy and service
   logs, unexpected database connections/roles, GitHub security log and connected
   apps. Do not copy values of secrets into notes or chat.
2. Inventory all Railway variables and their consumers, including
   `OPSDESK_DB_PASSWORD`, `OPSDESK_MIGRATION_PASSWORD`, `OPSDESK_JWT_SECRET`
   and the Railway PostgreSQL template credentials. The app and migration roles
   are custom PostgreSQL roles, so the template's [Regenerate procedure](https://blog.railway.com/p/security-disclosure-recommendation-rotate-postgresql-database-credentials)
   cannot be assumed to rotate those two role passwords. Coordinate each role's
   database password and matching service variable, then redeploy consumers.
   Use Regenerate for the template's own password; do not edit only one side.
3. Rotate the JWT signing secret and expect existing sessions to require login
   again. Confirm that old tokens no longer authenticate. Reconnect the Railway
   GitHub integration if needed using the [provider guide](https://blog.railway.com/p/security-disclosure-recommendation-redeploy-buckets-and-reconnect-github-after-the-credential-reset).
4. Deploy the latest reviewed product commit once, verify its runtime SHA,
   readiness and synthetic registration/login/session/logout cases, then review
   error and database-authentication logs. Do not invite broader testers until
   rotation and deployment are verified. Backups and restore remain unproven.

No credential rotation, GitHub reconnection, Azure provisioning or new public
deployment was performed as part of this research checkpoint.

## 25 October recovery checkpoint

The checklist above records the 23 October research state. The learner subsequently
reported rotation of template/custom-role passwords and the JWT secret, with matching
service variables updated. Do not repeat completed rotations solely because of
this documentation update. Audit review and complete revocation evidence are not
inferred from a successful deployment.

Railway support said paused-period commits were not queued and recommended
**Deploy Latest Commit** in the Command Palette. The learner executed a manual
deployment. Metadata confirms deployment `e7aa38ac-cb26-46f1-937a-e044241a8405`
succeeded from `255f9374a6506e1e50dfec0181f39c0b93fec2f4`, created at
2026-10-25 12:19:33 UTC (15:19:33 Europe/Istanbul). Both public health probes now
return 200. The learner reports the latest interface works. Separate public
negative/reload cases remain unrecorded at this checkpoint.

Product PR #43 merged normally at `122c052`, while Railway's source is still
`feature/week-15-railway-preview`. Preserve that branch. A future source switch
to `main` needs explicit deployment metadata and smoke evidence; do not use the
merge SHA as proof of the currently deployed source.

The conditional Azure move is unnecessary for the resolved blocker. Current
credit/stop-export planning, abuse controls, audit review and an isolated restore
exercise remain open. No paid plan, provider migration or live database restore
was performed.
