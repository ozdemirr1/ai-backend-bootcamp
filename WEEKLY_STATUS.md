# Weekly Status

## Current checkpoint — 30 October 2026, Thursday tasks 4–6

CommentForm/list is connected to real Ticket detail; role/state-guarded priority
PUT is implemented in the backend. Fresh results: 740 non-integration, 281
PostgreSQL data integration and 278 frontend tests / 14 files; build/lint/Ruff pass.
The first three Thursday tasks were pushed as product `7a3bb04` and bootcamp
`98f4cda`; this continuation is local and uncommitted. No new release is claimed.
Friday priority UI, Tailwind/responsive shell and remaining Month 04 gates are open.
See the existing Week 16 report for verification limits and the Thursday closure.

## Earlier checkpoint — 29 October 2026, Comment API tasks 1–3

Comment service authorization, GET/POST routes, content validation, rollback and
real PostgreSQL contention tests are implemented locally in OpsDesk. Fresh results:
702 backend non-integration and 237 PostgreSQL data tests passed; Ruff passed.
Schema/frontend checks retain their 28 October results. No commit/push/deployment
was performed for this increment; CommentForm/list and priority work remain open.
See the [task evidence](weekly-reports/week-16.md#29-october--comment-service-and-api-tasks-13).

## Earlier checkpoint — 29 October 2026, closing the 28 October release

[OpsDesk PR #47](https://github.com/ozdemirr1/opsdesk/pull/47) and
[bootcamp PR #11](https://github.com/ozdemirr1/ai-backend-bootcamp/pull/11) merged
normally. Product runtime `2013248` passed both CI workflows and deployed on
Railway from `main`; its pre-deploy migrated the hosted schema to `84c2f9a17d60`.
The last verified development schema is still `31be9023cfb2`.

Hosted browser smoke on 29 October passed register, login, workspace creation and
selection, real Ticket list/detail, combined search/status filter, session check,
private-detail reload/login return and logout. Anonymous root shows Login; private
API requests without a token return 401. Two synthetic Tickets were created by API
because Ticket creation UI is not implemented. No existing data was deleted.

28 October test evidence remains: 234 frontend tests, build/lint; 589 backend
non-integration, 204 PostgreSQL data and 5 schema tests; Ruff passed. This closure
adds hosted smoke, not a new run of all suites. See the
[release record](weekly-reports/week-16.md#29-october--release-verification-closing-the-28-october-work).

The 28 October publication/check gate is closed. Comment service/API/form,
cooperating locks, role mutations and the full Month 04 UI/learning gates remain.
No separate daily report was introduced.

## Earlier checkpoint — 27 October 2026, Tuesday close

Tuesday tasks 4–6 are complete as local implementation and automated verification.
The Workspaces screen lists current memberships, displays Organization-specific
roles and supports creation with a name-only request. Protected hash addresses
cover the directory, real Ticket dashboard and Ticket detail. Anonymous entry
shows Login at the intended internal address; successful login resumes it. Reload
clears the in-memory session and requires login again. Unknown/external/unsafe
paths never become redirect destinations.

The private dashboard uses the real validated HTTP adapters, server title/status
filters, total counts and pagination. The public mock dashboard remains separate.
Changing Organization resets private filters/detail/results. Session-scoped keys,
loader identity and effect cleanup prevent old responses from reappearing after
scope change, logout or a newer query, even when fetch ignores cancellation.
401 clears the session; 403 removes inaccessible workspace context; missing details
show a safe unavailable state; network/malformed responses offer retry without
turning into empty success. Organization creation is never automatically retried.

Fresh frontend verification: 233 tests / 12 files, build and lint passed.
The in-app browser confirmed signed-out direct-route/reload protection. Actual
PostgreSQL browser integration and hosted deployment remain separate checks.
Changes are local and uncommitted; the public Railway preview is unchanged.

Navigation refinement: Workspaces is hidden before login and after sign-out.
Normal login opens the directory; guarded deep links keep their intended route.

## Earlier checkpoint — 27 October 2026, tasks 1–3

Tuesday tasks 1–3 are complete locally: backend read coverage review,
Organization/session flow design, and validated Organization/Ticket HTTP adapters.
The dashboard still uses labelled mocks; protected routes, Organization screens
and real Ticket loading remain the next increment. No deployment was performed.

Fresh checks: 77 focused backend query/service/API tests passed; 209 frontend
tests across 11 files passed with one worker, plus build and lint. The 178
PostgreSQL integration results are from 26 October, not a new run. The API layer
has 68 new cases for malformed data, scope, pagination, query encoding, errors
and cancellation. No new dependency, migration or browser token storage was added.

See the [flow design](notes/react/ticket-search-filter.md#organization-and-session-flow--27-october-2026) and [Week 16 report](weekly-reports/week-16.md).

## Previous checkpoint — 26 October 2026

Week 16, Month 04; 26 October–1 November. Monday tasks 1–6 are complete locally:
baseline/access/search contract, scoped Ticket list/detail implementation, new
tests and Railway usage review. See the [Week 16 report](weekly-reports/week-16.md).

Final backend checks: 583 non-integration tests passed / 181 deselected; 178
PostgreSQL data tests passed on guarded local `opsdesk_product_test`; Ruff lint
and format passed. The three schema tests were not rerun (no migration change).
Frontend is unchanged: today's earlier 141-test/10-file one-worker run, lint and
build passed after an initial ENOSPC failure. Disk capacity remains a limitation.

Railway Usage in Chrome: $0.54 current usage, $4.46 remaining, 22 days; two services
online. No paid upgrade or deployment/settings change was made. The public preview
continues to use mock Tickets. GET reads are published and normally merged through
[OpsDesk PR #46](https://github.com/ozdemirr1/opsdesk/pull/46) at `fff4e47`.
Backend and frontend PR CI passed at source `a28cff2`. The new reads are not
deployed; Railway metadata still identifies `255f937` on the Week 15 branch.
Next: the Tuesday read-integration checkpoint, including hosted collation and
frontend runtime guards.

The 25 October intensive plan was published through normally merged bootcamp
PR #9 and OpsDesk PR #45. Current Week 16 product code is in PR #46; this bootcamp update records its evidence.

## Previous checkpoint — 25 October 2026

Week 15, Month 04; 19–25 October. Railway deployment recovered on 25 October. The
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
