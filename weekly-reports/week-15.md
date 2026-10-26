# Week 15 Report — Live preview and mock dashboard

19–25 October 2026, Month 04. Technical weekly package merged; learner review
answers and the explicitly listed operational checks remain open.

## Weekly outcome at 25 October

| Area | Outcome |
| --- | --- |
| Goal | Restore dashboard learning alongside the first hosted identity preview |
| Delivered | Table/badges, combined search/status filters, detail card/focus, session resets, pure display adapter; live recovery at `255f937` |
| Learning | Props/state, derived filtering, conditional detail rendering, session/request ownership, and type-versus-runtime-validation boundaries |
| Validation | Latest local frontend: 141 tests/build/lint on 24 October. Backend: 506 non-integration on 19 October. PR #43 and merge CI passed; no new full regression on Sunday |
| Remaining | Real reads/integration, comments/roles, full visual pass, operational evidence and three learner review answers |
| Next | [Week 16 plan](week-16-plan.md): scoped reads first, then real-data UI and bounded styling |

Earlier “pending” statements below describe their dated checkpoints; the 25 October
closure supersedes them. See [current status](../WEEKLY_STATUS.md) for open work.


## Early setup completed on 18 October

- Product branch: `feature/week-15-railway-preview`.
- Product commit: `cec7ce7954d1cbf912c553eac838b2d67478cdf7`.
- Exact-commit [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39163258790)
  and [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39163258819)
  both succeeded. Local learner evidence: 487 non-integration tests passed,
  160 database tests deselected; Ruff lint/format and whitespace checks passed.
- Added the explicit hosted Alembic target, separate migration settings,
  private-host/port/name guards, connected identity and role-attribute checks,
  transactional migration execution and tests. Default local test and development
  paths remain guarded.
- Railway demo database `opsdesk_demo` is owned by `opsdesk_migrator`.
  Migration and runtime roles have LOGIN but no superuser, CREATEDB, CREATEROLE,
  REPLICATION or BYPASSRLS attributes. Passwords were set interactively, not recorded.
- Learner deployment screenshots show the feature branch and deployment `d81bad4a`.
  This deployment identifier is not a Git commit SHA. Source title matches the
  migration commit; runtime metadata was subsequently confirmed on 19 October (below).
- Supplied logs show both revisions applied, ending at `31be9023cfb2`, followed by
  `Application startup complete` and Uvicorn listening on port 8080.
- A subsequent PostgreSQL query confirmed revision `31be9023cfb2` and all five
  tables owned by `opsdesk_migrator`.
- Explicit SELECT/INSERT/UPDATE grants cover the four product tables; USAGE grants
  cover their four identity sequences. No application grants on `alembic_version`.
  Schema CREATE is denied to `opsdesk_app`. New objects require privilege review.
- `SET LOCAL ROLE opsdesk_app` could read users (zero rows). This establishes role
  permissions, not password authentication or an HTTP application request.
- Both credential sets are currently supplied to the API service; separate prefixes
  do not isolate the migration secret from its runtime process.

## 19 October opening checkpoint

- Local product branch is clean and tracks the pushed feature branch.
- Learner executed the synthetic identity smoke check inside the running API container:
  registration 201, duplicate registration 409, wrong-password login 401, valid login
  200, current User 200 with matching ID/email and active status, tokens omitted 401.
  The script checked runtime database `opsdesk_demo` and role `opsdesk_app` before writes.
  One synthetic account was created; its generated password and token were not printed.
- Runtime `RAILWAY_GIT_COMMIT_SHA` matched
  `cec7ce7954d1cbf912c553eac838b2d67478cdf7`. Evidence is learner-supplied terminal output,
  not an independently repeated remote check. This confirms container-local HTTP and
  application-role database access, not public reachability.
- Next verify usage, implement liveness/readiness, and choose production frontend/origin wiring.
- Learner implemented `/health/live` locally and supplied passing evidence for the
  health and application tests: 8 passed; Ruff lint/format and whitespace checks passed.
  Source review confirms the liveness handler has no database or authentication
  dependency. This change is not yet claimed as deployed. Readiness is the next exercise.
- Learner subsequently implemented `/health/ready` using the application session
  factory, `SELECT 1`, session cleanup and the shared `service_unavailable` 503
  response. Source review and learner output confirm 30 targeted health/application/
  API-error tests passed with Ruff and whitespace checks clean. Hosted readiness
  remains unverified until these local changes are deployed. Runtime connection and
  pool wait limits are the next bounded change; these are not total request deadlines.
  Frontend publication, public HTTP reachability and browser identity flows are pending.
- Tickets remain mock data. Tokens remain in memory. No paid upgrade is authorized.
- Runtime connect and pool waits now default to 5 seconds, with validated environment
  overrides. Source review confirms wiring and tests; learner full regression output:
  500 passed, 160 integration tests deselected, Ruff lint passed, 110 files formatted,
  whitespace check passed. This is local evidence; publication and hosted health
  checks for these changes remain pending.
- Bootcamp documentation is updated locally; publication is not yet claimed.

## 19 October hosted health checkpoint

- Health and timeout changes published as
  `3df5bfccdb344b8ead0b3ea50ca3c4ba04e66991` on the existing feature branch.
- Exact-commit [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39275302161)
  and [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39275302240)
  succeeded, verified through GitHub CLI.
- Learner reported enabling autodeploy did not start the pending commit. Deploy Latest
  Commit started a successful deployment; screenshot title matches the health change.
  Autodeploy on a subsequent push still needs verification.
- Learner confirmed configuring the requested readiness deployment check; subsequent
  screenshot shows successful ACTIVE deployment. The screenshot does not display the
  configured healthcheck path or timeout values themselves.
- Learner then executed read-only HTTP checks inside the running API container:
  full runtime Git SHA matched `3df5bfccdb344b8ead0b3ea50ca3c4ba04e66991`,
  `/health/live` returned 200 and `{"status":"ok"}`, `/health/ready` returned 200
  and `{"status":"ready"}`. This supersedes earlier pending hosted health status.
- Dashboard displayed USD 4.94 remaining trial credit and 29 days; no monthly
  cost forecast is inferred from that point-in-time display.
- Service remained unexposed in the supplied screenshot. Public HTTPS and frontend
  publication/browser checks are the next steps; neither is claimed complete.

## 19 October public HTTPS checkpoint

- Learner generated `https://opsdesk-production-448f.up.railway.app` targeting port 8080.
- Independent read-only HTTPS checks returned HTTP 200 with `{"status":"ok"}`
  from `/health/live` and HTTP 200 with `{"status":"ready"}` from `/health/ready`.
  The initial sandbox DNS failure was resolved by an approved external-network retry;
  it was not evidence of an application outage.
- Public API health reachability is verified. Frontend publication and browser
  registration/login/session checks remain pending.

## 19 October combined frontend and browser checkpoint

- Product commit `2f6e00d5157d820adbd54dcc20464cee917c6bf3` was committed/pushed;
  supplied status and subsequent local inspection show a clean product tree.
- Optional frontend directory setting, explicit HTML/favicon/asset serving,
  incomplete-build failure and six behavior cases added. Existing API errors and
  liveness remain intact. Local learner run: 506 passed, 160 deselected; Ruff clean.
- Node 24 Railpack build appends npm ci and the same-origin Vite build to Python
  steps. Generated assets stay out of Git. Runtime configuration activates serving.
- Learner built with `VITE_API_BASE_URL=/`; actual HTML/CSS/JS served with HTTP 200
  in a local TestClient check. Public read-only checks independently returned HTML
  200, referenced JavaScript 200 and readiness 200 with the expected body.
- Learner reports automatic build after push. No exact `2f6e00d` runtime SHA check
  has yet been supplied, so distinguish source publication from runtime metadata.
- Learner confirms all requested browser checks worked: three mock Tickets,
  registration, login, Check session, Sign out and Tickets → Login with empty form.
  Supplied Railway network screenshot shows POST /users 201, POST /auth/login 200,
  GET /users/me 200 and a later session check 200. Public negative/reload cases
  remain to be explicitly recorded; earlier container smoke covers negative cases.
- Missing optional favicon.ico/apple-touch icons returned 404 while favicon.svg
  returned 200. These are not failed identity requests. VS Code schema trust warning
  was resolved by adding the actual schema URI to the trusted-domain setting.
- GitHub inspection during planning: [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39281732882)
  and [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39281732888)
  are queued at `2f6e00d`, not confirmed passing. Previous head CI passed.

## 19 October plan, repository and communication review

- Week 15 plan already existed locally from 18 October, but had not been committed.
  Replaced the obsolete setup schedule with remaining release/operations work;
  preserved 18-hour planned capacity without inventing actual hours.
- Local ignored AGENTS.md now points to Week 15, 19–25 October, and the live preview.
- Archived the former 1,828-line WEEKLY_STATUS without discarding its history;
  rebased archive links and made the live status file concise. Historical laboratory
  directories remain unchanged; product code is still separate from bootcamp.
- README navigation and ROADMAP now distinguish the live identity preview from the
  remaining Ticket/AI product work. Added deployment notes and an English LinkedIn
  draft continuing the supplied prior posts. Nothing was published to LinkedIn.
- External visitors can test the identity flow now. Source review found no
  registration/login rate-limiting implementation; edge controls are unverified.
  Scoped manual feedback is possible; broad invitation follows current-head CI,
  abuse/cost/data review. No paid upgrade, backup restore or production readiness
  is claimed. No product code was changed during this planning task.

## 19 October roadmap and GitHub audit

- Rechecked live GitHub branch heads: bootcamp main remains `42cf59c`, product main
  `b0e6cab`, and product Week 15 feature `2f6e00d`. Each matches its local branch.
  OpsDesk is clean; the feature is three commits ahead of main. No open PR exists
  in either repository. Bootcamp has uncommitted documentation and publication assets.
- Exact-head [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39281732888)
  and [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39281732882)
  both completed successfully. This supersedes the earlier queued status; it does
  not supply the still-missing exact runtime-SHA confirmation for this release.
- Updated current status/roadmap/plan and publication notes. Added a retrospective
  Month 03 summary from existing reports, with unfinished product work and delayed
  hosting explicitly retained. No historical tests were rerun or relabelled as new.
- Two LinkedIn images and an expanded draft are prepared; publication is unconfirmed.
  The roadmap review keeps Week 15 bounded and makes the next frontend integration
  priority explicit. See [audit](../notes/career/week-15-roadmap-audit.md).
- No commit, push, PR creation, branch deletion, merge or deployment was performed
  during this audit. The bootcamp publication package remains for review and commit.

## 20 October interrupted publication and Month 04 correction

- The previous session stopped after creating `feature/week-15-documentation`;
  no commit/push had completed. Resumed the 14-file package, corrected one trailing
  blank line caught by the staged whitespace check, committed `3be0f38`, and pushed
  the branch with upstream tracking. Main was not merged and OpsDesk was unchanged.
- Learner supplied the original Month 04 dashboard/UI milestones. Source comparison
  confirmed the real Ticket list, protected routing, dashboard detail/comments and
  role controls are not complete. A live identity preview is an additional outcome,
  not a substitute for these milestones.
- Corrected the operations-heavy Week 15 plan to resume bounded dashboard exercises
  with honest fixture labels, explicit Ticket-read dependencies and a Week 16 UI/
  integration priority. No complete MVP or catch-up date is claimed without scope
  estimates. See [alignment review](../notes/react/month-04-alignment.md).
- Next learner exercise: explain table/props/state through a small example, then
  implement TicketTable and StatusBadge with behavioral tests. This review did not
  implement the learner's exercise or rerun application suites.

## 20 October Ticket table and status badges

- Replaced the mock TicketList with TicketTable. App supplies TicketSummary[]
  through props; the table has a caption, column/row headers and an explicit empty
  state. StatusBadge maps all four TicketStatus values to readable labels with
  supplementary color. Neither component owns state or makes API requests.
- Preserved the mock-data notice and existing identity/session behavior. Added
  table container scrolling and keyboard focus styling. Search/filter, details,
  comments and real Ticket API integration remain pending.
- Added tests for table row associations, headers, empty/changed props and all
  status labels. Updated App navigation assertions and product documentation.
- Local Node.js 24.21.0 checks: 116 frontend tests passed across eight files;
  TypeScript/Vite production build, ESLint and whitespace checks passed. Backend
  tests were not rerun for this frontend-only increment.
- The supplied desktop screenshot shows aligned columns, three mock records,
  readable badges and the mock-data notice. Learner subsequently confirmed both
  manual checks: narrow-screen table scrolling and keyboard focus/Login → Tickets
  navigation. These are learner-reported browser results, separate from jsdom tests.
- The increment was committed and pushed as `30e5d03` on 20 October. The session
  ended before CI/deployment verification and the bootcamp evidence commit.

## 21 October catch-up and search/filter preparation

- Confirmed local product HEAD and the remote Week 15 branch both point to
  `30e5d035bb82e86b213bdbc9816577cb1dc9873a`; product working tree is clean.
- Exact-head [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39470599975)
  and [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39470600124)
  completed successfully. The local 116-test result belongs to 20 October;
  application suites were not unnecessarily rerun today.
- Railway deployment metadata still identifies `2f6e00d` as the successful release.
  A request to deploy the latest configured source returned `Deploys have been
  paused temporarily`. The [official incident page](https://status.railway.com/)
  reports paused builds/deployments and dashboard/API disruption on 21 October.
  This establishes today's external release blocker, not the cause of yesterday's
  missing automatic deployment. No successful new deployment is claimed.
- Public `/health/live` and `/health/ready` requests succeeded with the expected
  `ok` and `ready` JSON statuses. These checks cover the existing service, not the
  unpublished table release or its exact runtime SHA. Retry the release after the
  provider recovers; no automatic monitoring was configured.
- Wednesday remains optional catch-up. Prepared a bounded
  [search/filter exercise](../notes/react/ticket-search-filter.md) for the next
  dashboard step: input state versus derived rows, combined conditions and
  distinct empty/no-match behavior. Product implementation remains pending.

## 21 October title-search implementation review

- Reviewed TicketDashboard and its App integration. Query is local state; visible
  rows are derived from typed props. Comparison trims and lowercases the query
  without changing displayed input. Empty source and zero matches are distinct.
  No application-logic correction was needed.
- Added six dashboard test cases and one App navigation test. Coverage includes
  substring/case/whitespace matching, clearing, no matches, empty source, changed
  props and reset after leaving/returning to Tickets. Mock labels remain visible.
- Node.js 24 verification passed 123 tests across nine files, TypeScript/Vite build,
  ESLint and whitespace checks. Product documentation was updated. Backend suites
  were not rerun for this frontend-only increment.
- At this earlier checkpoint, search changes and evidence were local and
  uncommitted. Subsequent browser checks, commits and CI are recorded below.

## 21 October search browser check and field layout

- Learner-provided Chrome screenshots confirm local title search with `EMAIL` and
  `email` narrowing to #102, an unmatched query showing `No matching tickets.`,
  and clearing the field restoring all three mock rows. These are local browser
  observations, not evidence that the change is deployed.
- The search label and browser-default input appeared cramped and ran into the
  table. Added a vertical control layout, consistent input sizing, narrow-screen
  width and visible keyboard focus. TypeScript/Vite build, ESLint and whitespace
  checks passed after this presentation change. Learner's subsequent Chrome screenshot
  confirmed the revised desktop layout. The full frontend suite was rerun after
  the layout change: 123 tests across nine files, build and lint passed.
- Product title search was committed and pushed as `3a5b11b`. Public deployment
  and exact-head CI for this commit remain unverified at this checkpoint.
- Subsequent exact-head [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39639022621)
  and [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39639022552)
  at `3a5b11b` completed successfully. Public deployment remains unverified.

## 21 October status-filter completion

- Reviewed the learner's checked status options and AND filtering with title search.
  Preserved local state and derived rows; added a visible result count and responsive
  search/status/reset controls with keyboard focus styling.
- Added behavior coverage for each status, combined title/status matches and misses,
  Clear filters, empty source and navigation reset. Node.js 24 verification passed
  129 frontend tests across nine files, TypeScript/Vite build, ESLint and whitespace
  checks. Backend suites were not rerun locally for this frontend-only change.
- Local browser check confirmed `email` + Open shows zero of three and a no-match
  message; Clear filters restored all three rows. Desktop control layout was
  visually inspected. Narrow-screen visual inspection remains open.
- Product commit `a031633` was pushed to the Week 15 feature branch. Public
  deployment and exact-head CI were still unverified at this checkpoint.
- Subsequent exact-head [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39650552429)
  and [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39650552567)
  completed successfully at `a031633`. Public deployment remains unverified.

## 22 October mock Ticket detail

- Added optional descriptions to the three labelled Ticket fixtures and a local
  detail view. Selecting a title keeps the semantic table visible, highlights the
  row and opens a detail card below it. The card shows ID, status, priority and
  description. Close details returns keyboard focus to the selected title;
  changing search or status closes the card. Leaving Tickets resets the local
  selection and filters. No URL route or real Ticket API is claimed.
- Local Node.js 24 checks passed 134 frontend tests across nine files,
  TypeScript/Vite production build, ESLint and whitespace checks. A browser check
  at a narrow viewport showed the table, highlighted row and detail card. The
  product README and frontend README describe the fixture-backed behavior.
- Product commit `daa912f` (`week-15: show ticket details below the table`) is
  pushed on `feature/week-15-railway-preview`; the product worktree is clean.
  Exact-head [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39837133817)
  and [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39837133772)
  both passed, checked on 23 October. Railway deployment for this commit has
  not been verified.
- Friday's planned detail exercise was completed early. Session-aware dashboard
  access, real Ticket reads, comments and role-dependent actions remain open.

## 23 October Railway incident review

- Railway's 21 October disclosure reports possible unauthorized access to
  customer environment variables. The project's own exposure is not confirmed.
  Its 23 October status says builds and deploys for Trial/Free have resumed,
  while the incident investigation remains open. The visible “Limited Access”
  banner may be stale or may require GitHub reconnection; no successful OpsDesk
  redeploy is inferred from the provider-wide update.
- Chose to recover the existing Railway preview before considering a move to
  Azure. The GitHub Education offer advertises USD 100 Azure credit, but neither
  subscription activation nor OpsDesk deployment cost has been verified.
- Documented the tailored rotation and verification checklist in the existing
  [deployment notes](../notes/deployment/opsdesk-railway-preview.md). OpsDesk has
  separate custom `opsdesk_app` and `opsdesk_migrator` database roles, plus a JWT
  signing secret. Their rotation, GitHub reconnection and latest-source release
  remain pending; no secret values were recorded.

## 23 October recovery checkpoint and work decision

- The learner reports regenerating the Railway template Postgres password, rotating the
  custom application/migration role passwords and JWT signing secret, and updating
  the corresponding service variables. Secret values were not recorded here.
- Railway CLI showed a successful Postgres deployment at 18:14 local time. The
  latest listed OpsDesk deployment remained the 19 October release; no new app
  deployment was visible after the variable changes. Public `/health/live`
  returned 200, while `/health/ready` returned 503. This proves that the current
  app process responds but does not establish a working database connection; the
  specific connection failure has not been confirmed.
- Keep the public identity preview out of active sharing while readiness fails.
  The learner will reassess Railway on 26 October. If deployment remains blocked,
  compare an Azure migration against the existing setup and available education
  credit before making infrastructure changes. Do not count Azure as deployed.
- Continue the Week 15 dashboard exercises locally. The Week 15 branch is clean
  and exact-head CI passed for `daa912f`; those results do not verify the old
  Railway runtime.

## 23 October dashboard session regression and Ticket-read preparation

- Added three App regression cases for sign-out, session-check 401 and an
  inactive current User. Each begins with title/status filters and an open detail,
  then verifies Login, removal of session controls, and a fresh public mock
  dashboard on return. The existing App behavior already satisfied these cases;
  no production component change was required.
- The mock preview remains public. These tests do not implement protected URL
  routing or authorization for real Ticket data.
- Extended OpsDesk's existing F11 planning record with the reviewed list/detail
  scope, pagination/count consistency, membership/requester isolation, frontend
  adapter boundaries and required database test evidence. Real Ticket reads are
  still unimplemented; title search needs a separate server-side contract.
- Node.js 24 verification: App tests 21 passed; complete frontend suite 137 passed
  across nine files; TypeScript/Vite build, ESLint and whitespace checks passed.
  No backend behavior changed, so backend suites were not rerun.
- Product tests, frontend README and F11 notes were committed and pushed as
  `5cfa65e` (`week-15: verify dashboard session resets and scope ticket reads`).
  [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39981897780) and
  [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39981897714)
  both passed for `5cfa65edf1b3d1b2b279c84ce3996b31b19d2e97` on 23 October.
  No deployment success is claimed. Railway follow-up remains deferred to
  26 October under the learner's decision.

## 24 October Ticket adapter and integration preparation

- Added `frontend/src/api/tickets.ts`: the existing backend TicketResponse wire
  shape and a pure `toTicketSummary` projection. The adapter selects display
  fields and preserves descriptions; it does not fetch, authorize or validate
  unknown JSON. The dashboard continues to use labelled fixtures.
- Four tests cover exact display projection, empty and multiline Unicode
  descriptions, source immutability and independent result objects. Node.js 24
  checks passed 141 frontend tests across ten files, TypeScript/Vite build and
  ESLint. Backend behavior was unchanged; backend suites were not rerun.
- Extended the existing F11 record with the Organization/membership visibility
  matrix, suspended/no-membership/empty/error UI distinctions, stale-response
  boundaries and five implementation packages. The provisional estimate is
  2–3 sessions for backend contracts/reads/tests plus 1–2 for integration, to be
  revised after the first package; this is not a Week 15 completion claim.
- Recorded that PostgreSQL bigint IDs exceed JavaScript's safe integer range.
  Future runtime validation must reject unsafe numeric IDs; full-range string
  IDs would require a reviewed wire-contract change. No validator or real Ticket
  GET endpoint was implemented today.
- Updated frontend README. The multiline test example now uses English text
  with café to retain Unicode coverage; all four adapter tests passed again.
- Product changes were committed and pushed as `255f937`
  (`week-15: add ticket display adapter and plan read integration`).
  [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40129941595) and
  [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40129941691)
  both passed for `255f9374a6506e1e50dfec0181f39c0b93fec2f4` on 24 October.
  Product working tree is clean. No browser integration or deployment success
  is claimed. Railway follow-up remains in the plan for 26 October, with no
  automatic monitor configured.

## 25 October recovery and weekly review

- Railway support explained that commits pushed during the pause were not queued
  and requested a manual latest-commit deployment. The learner performed that
  deployment and confirmed the latest interface works.
- CLI deployment metadata verifies successful deployment
  `e7aa38ac-cb26-46f1-937a-e044241a8405`, created 25 October at 15:19:33
  Europe/Istanbul, from `255f9374a6506e1e50dfec0181f39c0b93fec2f4`. The previous
  `2f6e00d` deployment is removed. Independent public health checks returned
  liveness 200 / `{"status":"ok"}` and readiness 200 / `{"status":"ready"}`.
- The source branch is clean and matches its remote. Latest source Backend and
  Frontend CI passed. Fresh PR [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40193232937)
  and [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40193232976)
  also passed on 25 October. CI includes frontend tests/build/lint and backend
  Ruff/non-integration tests; it does not run PostgreSQL integration/schema tests.
- Reviewed the weekly change set, including migration-target guards, safe health
  errors/static assets, dashboard state and the adapter boundary. Whitespace
  checks passed. No new product behavior was added and no destructive database
  test or schema operation was run. The unchanged local frontend evidence remains
  141 tests/build/lint from 24 October; historical backend counts are not relabelled
  as Sunday runs.
- Product [PR #43](https://github.com/ozdemirr1/opsdesk/pull/43) merged normally at
  `122c0528be371d8e68698323ea171dfa2272379e`, preserving all daily commits.
  Railway still uses the weekly feature branch; it is retained. Its deployed
  source remains `255f937`, not the merge commit.
- Keep Railway for now: the blocker behind the conditional 26 October Azure
  decision has cleared. No new infrastructure or paid plan was provisioned.
- Updated current status and prepared the [Week 16 plan](week-16-plan.md). Existing
  weekly evidence was used; no separate daily working file was introduced.

Merge follow-up: [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40193369253)
and [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40193369467)
both passed at `122c052`. After fetching `origin/main`, a full tree comparison
against feature head `255f937` showed no file differences. Merge history differs,
but the deployed source content is the merged product content.

### Delivered scope and carry-over

Delivered: hosted identity preview, table/status badges, combined local filters,
result counts, mock detail card/focus return, session-reset regression and typed
display adapter. Tickets remain fixtures. Real Ticket reads, runtime JSON guards,
Organization selection, authenticated real-data screens, comments, role-dependent
mutations and the full visual pass remain incomplete. The original frontend MVP
is not claimed complete. Week 16 explicitly prioritizes the read dependency.

Public wrong-password/duplicate/reload evidence, current trial usage and stop/export
procedure, abuse controls, provider audit review and isolated restore/rollback
remain open. The learner reported credential rotation on 23 October; green health
and the new deployment do not prove absence of compromise or complete all checks.

### Sunday learning review — learner response pending

1. Explain why a green readiness check does not prove Ticket authorization works.
2. Describe the difference between a TypeScript response type, runtime validation
   and the display adapter using one Ticket example.
3. Explain why Organization/requester filtering must happen before pagination.

These are review questions, not completed learner answers. Start Monday with the
F11 access matrix and one small scoped-query example before implementation.

Bootcamp publication: the Sunday evidence/plan package was committed and pushed
as `a5e1915` on `feature/week-15-documentation`.
[Bootcamp PR #7](https://github.com/ozdemirr1/ai-backend-bootcamp/pull/7)
collects the weekly documentation and preserves its daily history through a
normal merge. Sunday document links resolve and whitespace checks pass.

## 25 October documentation consistency review

- Reorganized both repository entry points around actual current scope, with
  chronological Month 01–04 evidence navigation in bootcamp and a real deployed
  dashboard capture in OpsDesk. Backend setup/test instructions moved to the
  product development guide; original implementation history remains in Git.
- Added a dated product status/issue-closure matrix. Contract inventories and
  historical issue snapshots no longer imply all endpoints are delivered or
  completed issues are still unpublished. Closed design does not mean complete CRUD.
- Corrected Week 16's destructive-test target to `opsdesk_product_test` and
  separated product, historical learning and hosted databases. Local ignored
  mentoring instructions received the same guardrail correction.
- Added weekly outcome summaries and an explicit carry-over/dependency ledger.
  No daily work file was created. No learner answers, product feature completion,
  new full regression run or operational acceptance results were invented.
- Documentation publication uses separate weekly alignment branches, preserving
  the Railway source branch. Validation passed: 113 Markdown files, 548 local
  link/image targets and Markdown anchors, plus 11 cross-repository main-branch
  file references checked against the proposed trees. Both whitespace checks pass.
  Application code, migrations, dependencies and CI configuration are unchanged.
  Runtime test groups above remain dated evidence; hosted PR CI is checked
  separately during publication. Normal PR merge history is retained.

Publication references: [OpsDesk PR #44](https://github.com/ozdemirr1/opsdesk/pull/44)
and [bootcamp PR #8](https://github.com/ozdemirr1/ai-backend-bootcamp/pull/8).
These collect the consistency corrections separately from the earlier feature
release and weekly closure. GitHub provides the final CI/merge state.


## 25 October Week 16 scope revision

The learner requested a plan covering every original Month 04 outcome and chose
an intensive 26 October–1 November calendar. The revised
[Week 16 plan](week-16-plan.md) supersedes the earlier 18-hour proposal: 42 focused
hours plus up to 8 contingency hours, with Tuesday/Friday estimate checkpoints.
Required work includes real Ticket reads/search and protected routes, persisted
comments, the role-aware priority subset, the complete original UI package, tests
and release/learning evidence. Broader membership administration, assignment and
status workflow remain explicit backend backlog; this does not close R01 or F12.

This entry records a planning decision only. No Week 16 code, passing test results,
learner answers or monthly completion are claimed. Current README/status/roadmap
pointers were aligned; earlier dated evidence remains historical. No daily work
file was added. Month 04 closes only after the plan's acceptance gates pass.

Planning validation: local Markdown links/anchors and cross-repository file
references resolve in the proposed trees; both repository whitespace checks pass.
Package hours total 42, matching seven six-hour days; four optional two-hour
reserves bring the ceiling to 50. This documentation change did not run or alter
application tests.
