# Weekly Status

## Current checkpoint — 25 October 2026

Week 15, Month 04; 19–25 October. Railway deployment recovered today. The
learner reports the latest live interface works. Keep the existing provider;
the conditional 26 October Azure migration is no longer needed for this blocker.
No Azure provisioning or paid upgrade is authorized by this checkpoint.

## Product and verification

- Product branch: `feature/week-15-railway-preview`; source head `255f937`.
- [Week 15 product PR #43](https://github.com/ozdemirr1/opsdesk/pull/43) merged normally at `122c052` on 25 October after both PR CI workflows passed.
  Daily commits are preserved; do not delete the branch while Railway uses it
  as its source. Merge-commit [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40193369253)
  and [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40193369467)
  passed. At the PR #43 checkpoint, `origin/main` and the deployed feature head
  had identical file trees. Later documentation-only changes do not change the
  deployed runtime source.
- Exact-head [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40129941595)
  and [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40129941691)
  passed, rechecked on 25 October. Backend CI covers Ruff and non-integration
  pytest; it does not run PostgreSQL integration/schema tests.
- Last local frontend verification on 24 October: 141 tests across ten files,
  TypeScript/Vite build and ESLint passed. No product code changed on Sunday.
  Historical backend count: 506 passed / 160 deselected on 19 October;
  this is not a fresh Sunday test run.
- Railway deployment `e7aa38ac-cb26-46f1-937a-e044241a8405`, created
  25 October at 15:19:33 Europe/Istanbul, succeeded. Deployment metadata identifies
  source commit `255f9374a6506e1e50dfec0181f39c0b93fec2f4`.
- Independent public checks on 25 October: `/health/live` returned 200 with
  `{"status":"ok"}`; `/health/ready` returned 200 with `{"status":"ready"}`.
  Readiness checks database connectivity, not every permission or identity flow.
- [Live preview](https://opsdesk-production-448f.up.railway.app/): same-origin
  React/FastAPI plus persistent PostgreSQL. Registration/login/session operations
  use the API; access tokens remain in memory. The learner confirmed current live
  behavior, but today's duplicate/wrong-password/reload cases were not separately
  documented or independently retested.

## What is complete and what is still missing

The mock dashboard has a table, readable badges, combined title/status filters,
clear/count/empty states and a detail card below the table. Session termination
reset behavior is tested. The Ticket display adapter has four unit tests; it is
not wired to HTTP and does not validate unknown JSON.

Real Ticket list/detail endpoints and their database authorization tests are still
missing. Organization selection, protected real-data screens, pagination and stale
request handling must precede claiming real Ticket integration. Comments,
role-dependent mutations and the full UI pass remain open. The original complete
frontend MVP is not yet delivered.

The learner reported credential rotation on 23 October. Recovery does not prove
there was no incident exposure. Audit review, public negative/reload evidence,
abuse controls, current trial usage/stop-export procedure and isolated restore/
rollback evidence remain open; do not mark them complete from green health checks.

## Next work

Follow the [Week 16 plan](weekly-reports/week-16-plan.md), starting 26 October:
the learner approved an intensive 26 October–1 November calendar on 25 October,
with 42 focused hours and up to 8 contingency hours. Required deliveries are
scoped Ticket reads/search, real Organization/list/detail integration and protected
routes, persisted comments, a role-aware priority operation, and the full original
Tailwind/responsive/sidebar/empty-state/toast/modal/accessibility package.
Feature tests, release verification and the monthly learning handoff are included.
Assignment, membership administration and the full status workflow remain separate
backend backlog; completing the priority subset does not close all of F12.
Tuesday/Friday checkpoints re-estimate remaining work; no unfinished Month 04
requirement is silently removed. This is planned work, not completion evidence.
Docker/Redis stay in Month 05; AI stays in Month 06.

Sunday's learning review is in the [Week 15 report](weekly-reports/week-15.md).
The [deployment notes](notes/deployment/opsdesk-railway-preview.md) preserve the
incident and recovery evidence. Earlier status history is retained in the
[status archive](weekly-reports/archive/status-before-2026-10-19-preview.md).

The weekly bootcamp documentation is collected in
[PR #7](https://github.com/ozdemirr1/ai-backend-bootcamp/pull/7), including the
Sunday package `a5e1915` and the Week 16 plan.

The subsequent documentation consistency correction is collected in
[bootcamp PR #8](https://github.com/ozdemirr1/ai-backend-bootcamp/pull/8) and
[OpsDesk PR #44](https://github.com/ozdemirr1/opsdesk/pull/44). It aligns README
entry points, historical status boundaries and the carry-over ledger; no runtime
behavior or Railway source-branch setting changes. GitHub shows their publication
and merge state; the Week 15 report records the documentation checks.
