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
