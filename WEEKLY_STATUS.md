# Weekly Status

## Current checkpoint — 12 November 2026: readiness/timeout learning closed

Week 18 Compose role/migration implementation was pushed as OpsDesk c18775c;
its backend/frontend/Docker CI passed at the 11 November checkpoint. Today's
learner-run experiments verified delayed startup ordering, local DB outage
live 200 / ready 503, recovery to ready 200 without API restart, missing-config
exit 1 / normal-config exit 0, and two connection timeouts (2.07s, 2.09s; total
5.15s including a one-second interval). End-of-session retry/idempotency reasoning
is recorded in [Week 18](weekly-reports/week-18.md) and the
[Compose note](notes/docker/compose-networking.md).

The 10–12 November learning slices are complete within their recorded scope.
No new product retry code, deployment, destructive test or deletion occurred in
this closure. Next: planned 13 November GitHub Actions PostgreSQL service-container
and guarded schema/data CI learning. Week 18 acceptance remains open.

## Earlier checkpoint — 11 November 2026: Week 17 deployed

With explicit learner approval, OpsDesk PR #51 merged normally as `7dfed5a`.
Railway deployment `7baedb6e-ae13-4903-b00a-d35eb23781a3` succeeded with the
Dockerfile builder, direct installed Uvicorn/Alembic commands and port 8080.
Public HTTPS liveness/readiness/static assets passed. A synthetic account passed
registration, login and authenticated profile/organization reads; it is retained.
No data was deleted and no destructive tests ran. Merge-head backend/frontend/
Docker CI all passed. See the dated [Week 17 release evidence](weekly-reports/week-17.md).

Week 17 release gate is closed. Bootcamp PR #15 had already merged as `d7f7211`.
Week 18 preparation remains ready; Compose implementation has not started.

## Earlier checkpoint — 10 November 2026: Week 17 review and Week 18 preparation

Planned 9 November tasks verified today: independent cached build and isolated
runtime smoke passed, including missing config, non-root, static files, live 200,
expected ready 503 and SIGTERM exit 0 in 0.374s. Reusable smoke script and product
instructions added. Prior product head 5f6f291 passed all three CI workflows.
Current product head 2cda8fb passed all three push and PR workflows. Technical
Week 17 evidence is complete with documented limits. OpsDesk draft PR #51 and
bootcamp PR #15 hold the reviewable changes; product merge/release is not claimed.
Railway follows main, so product merge requires a concrete release decision.

Week 18 preparation reviewed current migration/test guards and selected isolated
Compose service/config boundaries. Existing test guard remains exact; separate
Compose migration target must be implemented/tested. No Compose services, volumes
or databases were created. See [Week 18 plan](weekly-reports/week-18-plan.md) and
[preparation report](weekly-reports/week-18.md). Preserve unrelated LinkedIn assets.

## Earlier checkpoint — 9 November 2026: planned 8 November learning closure

The learner pushed exit-code failure/recovery commits 2c59021 and d9eb142.
GitHub job metadata confirms the failed step skipped its successor, then all
three steps passed after correction. Separate backend/frontend workflows passed
on both commits. Evidence is in notes/ci/github-actions-foundations.md and the
Week 17 report.

Subsequent Docker CI evidence: a35af07 build passed; f294911 deliberately failed
on missing COPY source /frontend/dist-missing after frontend build succeeded;
67500f2 restored the path and passed Docker, backend and frontend CI. Verified
GitHub runs/logs are recorded in the CI note. Planned 8 November technical
exercises are complete. Final learner explanation supplied; review clarified
workflow versus job names and build-only CI limits. Product documentation updated.
The planned 8 November slice is closed on 9 November; documentation commit/push
follows. Week 17 review/PR/handoff remains open, not automatically completed by CI.

## Earlier checkpoint — 9 November 2026: multi-stage verification

The scheduled 7 November scope continued on 9 November, earlier than the
previously stated intention to resume on 10 November. Learner evidence confirms
the small multi-stage/non-root exercises and the OpsDesk Node build/Python runtime
image. UID/GID 10001, selected image exclusions, Node/npm absence, denied /app
writes, static-file HTTP 200, liveness 200, unavailable-DB readiness 503 and
controlled missing-frontend failure passed. SIGTERM exited 0 in 0.478 seconds.
Unchanged rebuild used cached layers. Ruff passed (141 formatted files), backend
740 passed/286 deselected in 9.71 seconds, frontend 356 passed in 16.62 seconds,
frontend lint clean. Evidence came from learner terminal output, not independent
reruns. Product documentation updated; final learner explanation supplied and
reviewed, closing the planned 7 November learning slice on 9 November.
Commit/push follows this closure. GitHub Actions learning/Docker CI has not been
completed. No browser/container DB persistence or new deployment is claimed.

Docker API had stalled; after the learner rebooted the Mac, direct checks
confirmed Engine 28.5.1 answered and existing containers remained listed. No
deletion/reset was performed. Disk free rose to 7.6 GiB after reboot, then 5.5 GiB
before the runtime checks. Historical no-space log matches do not prove root cause.

## Earlier checkpoint — 9 November 2026: basic product image learning closure

Continuing the scheduled 6 November task on the actual date of 9 November.
The learner created the product branch `feature/week-17-docker-foundation` and
the initial single-stage Dockerfile plus allowlist .dockerignore. Actual local
file review confirmed the intended content and valid whitespace/continuations;
the files are included in this closure. Learner build output confirms a successful
`opsdesk:week17-basic` image build with exit 0, Python 3.14.7 and 31 installed
runtime packages. Network-disabled import checks passed (pytest absent), and
default startup without config failed as expected on missing JWT secret with
exit 1. Learner's isolated runtime check then passed: PID 1 startup, liveness
200, expected unavailable-DB readiness 503, and SIGTERM shutdown in 0.456 seconds
with exit 0. No successful real-DB readiness or persistence is claimed.

Host disk initially had only 513 MiB available. After the learner's restart/cleanup
pause, a fresh check showed about 2.4 GiB. Docker Desktop was opened and Engine
28.5.1 responded. No agent cleanup or volume deletion was performed. Capacity
remains constrained: the latest check showed 442 MiB free. Scoped image-filesystem
exclusion checks passed; full layer-secret scanning is not claimed. Local regression
passed on learner evidence: Ruff clean, 141 files formatted, 740 tests passed and
286 deselected in 9.98 seconds. Product Docker documentation, README and dated
project status now describe the verified scope. Final learner review was supplied
and corrected for the limited health-check and image-secret evidence. The planned
6 November learning slice is closed on 9 November; commit/push is authorized.
The learner plans to continue the 7–8 November scope on 10 November, subject to
learning checks and disk capacity, without treating those tasks as completed.
Multi-stage/frontend, non-root and Docker CI remain later
work. See the [Week 17 report](weekly-reports/week-17.md).

## Earlier checkpoint — 6 November 2026: systems-plan continuation

The 4 November closure was pushed as `c908860`. Continuing the remaining
5 November learning scope on the actual date of 6 November: the product venv
(Darwin/Python 3.14.7/FastAPI present) and base container
(Linux/Python 3.14.10/FastAPI absent) comparison passed on learner evidence.
A Docker version probe initially timed out; subsequent client/server and tiny
container checks succeeded. Root cause/recovery action are not established.
TLS/HTTPS experiments also passed on learner output: verified public TLS 1.3 and
HTTP/2 200, plus a local HTTP/TLS mismatch (curl 35 and server malformed-request
logs). The example server was stopped. Final review was supplied and corrected:
container isolation is not absolute, base-image contents are not standard-library
only, and -k cannot fix HTTPS sent to a plain-HTTP server. No independent revised
answer is claimed. The 5 November systems session is closed on 6 November.
No product image implementation or new product test run
is claimed; see the [Week 17 report](weekly-reports/week-17.md).

## Earlier checkpoint — 6 November 2026: 4 November learning closure

The learner supplied the final review for the 4 November session and requested
closure without another experiment. Image/source snapshots, rebuilds and command
defaults; build-context exclusion/cache recovery; HTTP/connection/exit-code
distinctions; port conflict/name resolution; and bounded shutdown behavior have
learner-supplied exercise evidence. The final explanation was accepted with
clarifications about bind-mount reload and configured access logging.

The 4 November work is closed; Week 17 remains in progress. This is not evidence
of work on 5 November or completion of the scheduled 6 November product image.
OpsDesk remains unchanged; no product Dockerfile, new CI job, product test run
or deployment is claimed. GitHub Actions foundations still require full teaching.
Next session resumes the weekly prerequisites before a bounded basic product image.
See the [Week 17 closure](weekly-reports/week-17.md#6-november--review-and-closure-of-the-4-november-session).

## Earlier checkpoint — 4 November 2026

Month 05's main working conversation has begun. Week 17's repository/build/CI
and local Docker baseline is inspected; product implementation has not started.
After fetching both origins, bootcamp main matched `8e2408a` and OpsDesk main
matched `f8f42be`. Existing untracked LinkedIn assets were preserved.

Docker Desktop was started and Engine 28.5.1 now responds as Linux/ARM64;
Compose v2.40.2 is available. About 5 GiB host disk space remains, so image-build
capacity needs attention. No product tests or deployment ran.
The first container exercise succeeded in learner-supplied terminal evidence:
Linux, PID 1, retained logs and Exited (0), matching the accepted prediction.
Controlled failure diagnosis and recovery also passed on learner-supplied output
(RuntimeError/exit 1 → corrected command/exit 0). The learner removed the two
failure/recovery containers only. A later minimal custom learning image,
`week17-python-demo:v1`, built and ran successfully with `/app` and exit 0 in
learner-supplied output. No OpsDesk product image has been built.
HTTP exercises verified port forwarding, wrong-port connection failure and
HTTP status versus curl exit code (including `--fail`). The learner stopped the
HTTP container and investigated Exited (137): a three-second SIGTERM stop took
3.235 seconds with exit 137/OOM false; SIGINT took 0.250 seconds with exit 0 and
an explicit shutdown log. The comparison supports timeout escalation; the
container is now stopped. This is not an OpsDesk SIGTERM acceptance result.
See the [Week 17 report](weekly-reports/week-17.md)
and [Docker foundations](notes/docker/docker-foundations.md).

## Earlier checkpoint — 3 November 2026

Month 05 scope and Week 17–20 plans are prepared, not implemented. GitHub Actions fundamentals, incremental examples and
independent failure diagnosis are included; existing test counts do not replace learning. Follow the
[monthly plan](monthly-plans/month-05.md). Celery is selected; existing CI will be
extended with Docker build and isolated integration checks. Product #19/#24 were
closed with evidence; #25 is targeted in Week 18. Other product backlog and the
Month 04 operational follow-ups remain visible; no broad completion claim.

Month 05 starts on **4 November 2026**; planned closure is 30 November.
Continue in a new month-scoped conversation using the
[Month 05 handoff](monthly-plans/month-05-handoff.md).

## Earlier checkpoint — 2 November 2026, release evidence and handoff

Month 04 UI/integration is delivered through OpsDesk PR #49 (`8a633d0`). The
documentation follow-up PR #50 (`f8f42be`) passed main CI, deployed successfully
and passed post-deploy health/root checks. Hosted
persistence, scoped access, isolated backup/restore and prior-runtime read checks
are recorded. Fresh PostgreSQL results: 281 data tests and 5 schema tests; no drift.
The [Month 04 review](monthly-reports/month-04.md) contains two learner answers,
schedule variance and the Month 05 handoff. Personal reflection remains open.

This closes the technical evidence package, not all operational acceptance gates:
hosted-export recovery, abuse controls, provider audit/current usage and development
dependency maintenance remain explicit follow-ups before broader demo exposure.
See the [Week 16 closure](weekly-reports/week-16.md#2-november--recovery-release-records-and-month-04-review).

## Earlier checkpoint — 2 November 2026, two acceptance checks completed

The deployed OpsDesk source `8a633d0` passed the hosted create-Ticket, Comment,
priority and logout/relogin persistence walkthrough. A real release defect was
fixed: the runtime database role lacked SELECT/INSERT on Comments; narrow table
and identity-sequence grants restored the flow without a code redeploy.

Customer/staff and two-Organization acceptance passed against the guarded local
product test database: 98 focused PostgreSQL tests, 88 focused frontend tests,
plus a real browser/API fixture walkthrough. Invalid sessions and late-response
cleanup are covered by the frontend tests; hosted role mutation was not performed.
See the [dated evidence](weekly-reports/week-16.md#2-november--live-flow-and-authorization-acceptance).

These results close the two requested checks, not all Month 04 gates. Operational
recovery, publication/documentation cleanup and the retrospective remain open.

## Earlier checkpoint — 1 November 2026, Saturday 31 October tasks completed

Ticket creation, safe POST handling and success/detail navigation are implemented.
The remaining Saturday work adds actionable empty states, distinct loading/error
surfaces, page/filter recovery, accessible validation feedback and keyboard focus
handling. Closed empty Tickets no longer invite comments. Pagination has named
navigation landmarks.

Frontend: **356 tests / 17 files**, build and lint passed on 1 November. Browser
checks at 1280/700/320 CSS pixels and keyboard/error recovery passed in an isolated
synthetic-response harness. The combined create/detail/comment/priority/logout
UI test uses real adapters with synthetic HTTP responses; no fresh PostgreSQL or
hosted walkthrough is claimed. Backend evidence remains dated 30 October (740
non-integration, 281 data) and 28 October (5 schema).

Friday's package is committed as product `19dfaff`. Saturday's implementation and
this continuation remain uncommitted. No new GitHub/CI or Railway action was taken.
Sunday's final persistence/cross-identity regression, PR/CI, deployment/smoke,
operational recovery and Month 04 retrospective gates remain open. Existing
development-dependency audit findings still require their separate review.

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
