# Weekly Status

## Current checkpoint — 24 October 2026

Week 15, Month 04; 19–25 October. Local dashboard work continues; the public
identity preview is degraded after credential rotation (liveness 200, readiness
503 on 23 October). Railway follow-up is deferred to 26 October; if deployment
remains blocked, the learner plans to move to Azure after checking setup and costs.

- Product branch: `feature/week-15-railway-preview`.
- Pushed head: `255f937` on the Week 15 product branch; product working tree is clean.
  [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40129941595) and
  [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40129941691)
  both passed for this commit on 24 October.
- Previous checkpoint `5cfa65e`: session regression tests
  and Ticket-read preparation are committed and pushed: 137 frontend tests across
  nine files, build, lint and whitespace checks passed locally on 23 October.
  [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39981897780) and
  [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39981897714)
  both passed for that commit.
- Added a typed TicketResponse-to-TicketSummary adapter and four tests. Local
  Node.js 24 verification passed 141 tests across ten files, build and lint.
  Existing F11 notes now map Organization context, empty/error states, safe ID
  validation and the backend/frontend implementation packages. The adapter is not
  wired to HTTP or the dashboard; Tickets remain labelled fixtures.
- Demo: https://opsdesk-production-448f.up.railway.app/
- One FastAPI service serves the built React frontend and API on the same origin;
  PostgreSQL is a separate persistent service. Node 24 builds frontend assets;
  Uvicorn runs the application. No Vite development server is hosted.
- Learner local evidence: 506 non-integration backend tests passed; 160 database
  tests deselected; Ruff and whitespace checks passed. Frontend production build
  with `VITE_API_BASE_URL=/` passed. Actual HTML/CSS/JS were served by TestClient.
- Earlier public checks returned 200 for HTML, the referenced JavaScript,
  and readiness. Learner confirms Tickets, registration, login, session check,
  logout and Tickets → Login navigation. Supplied network screenshot shows
  registration 201, login 200, profile/session check 200.
- Tickets still show three mock records. No real Ticket workflow or AI is in the UI.
  Tokens remain in memory; reload requires login. Latest public-browser negative
  cases and reload behavior still need explicit evidence.
- Railway's latest successful deployment metadata checked on 21 October pointed
  to `2f6e00d`. The latest-source deployment request was rejected with `Deploys have
  been paused temporarily`; [Railway's incident page](https://status.railway.com/)
  confirms a platform deployment pause. Table release and runtime-SHA verification
  remain pending. Public liveness/readiness checks on 21 October returned expected JSON.
- Earlier exact-head [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39470600124)
  and [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39470599975)
  at `30e5d03` both completed successfully, verified 21 October.
- Exact-head [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39639022621)
  and [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39639022552)
  at `3a5b11b` also completed successfully on 21 October.
- Exact-head [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39650552429)
  and [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39650552567)
  at `a031633` completed successfully on 21 October.
- The mock Ticket detail card was pushed as `daa912f` on 22 October. The table
  remains visible with the selected row highlighted. Local checks passed 134
  frontend tests across nine files, build, lint and whitespace checks; a narrow
  browser check showed the table and card. Exact-head Frontend and Backend CI
  both passed at `daa912f`, checked on 23 October. Public deployment of this
  newer commit remains unverified.
- Last supplied credit display: USD 4.94 / 29 days. Not a current balance or
  monthly forecast. Only trial credit is approved; no paid upgrade.
- Railway's 21 October security disclosure reports possible access to customer
  environment variables. On 23 October Railway says Trial/Free builds have
  resumed, but its investigation is ongoing. OpsDesk-specific impact is unknown.
  The learner reports rotation of custom database-role credentials and the JWT
  secret and updates to service variables. Postgres redeployed successfully on
  23 October; OpsDesk still lists the 19 October deployment and readiness fails.
  GitHub connection and a successful new deployment remain unverified.
  The [deployment notes](notes/deployment/opsdesk-railway-preview.md)
  record the procedure. Azure Student credit is an option to cost later, not an
  activated migration or a fix for possibly exposed secrets.

## Next work

1. TicketTable/StatusBadge are implemented locally; 116 frontend tests, build and
   lint passed on 20 October. Desktop screenshot reviewed; learner confirmed narrow-screen
   scrolling and keyboard/navigation checks. The increment is pushed with passing CI.
   Title search is now implemented locally: 123 frontend tests, build and lint
   passed on 21 October. Chrome screenshots confirmed matching, no-match feedback
   and clearing. A subsequent screenshot confirmed the restyled search field.
   The title search was pushed as `3a5b11b`. Status filtering, combined conditions,
   a visible count and Clear filters are now pushed as `a031633`: 129 frontend tests,
   build and lint passed. Local browser checks confirmed no-match and reset behavior.
   The bounded mock detail behavior is now pushed as `daa912f`, with the table
   still visible and keyboard focus returning on close. Next: session-aware
   dashboard behavior with tests. Public deployment of these increments remains
   unverified.
   Explicitly label fixture-backed screens.
2. Retry the latest-source release after Railway recovers, then verify runtime SHA
   and public assets. No automatic monitoring is configured. Timebox usage/exposure triage. Review abuse and data controls before
   broad sharing; pending operations work is not a blanket blocker for local UI learning.
3. Follow the revised [daily plan](weekly-reports/week-15-plan.md),
   [deployment notes](notes/deployment/opsdesk-railway-preview.md) and
   [LinkedIn draft](notes/career/opsdesk-live-preview-linkedin.md).
4. Scope the missing real Ticket list/detail API and organization membership context
   for integration. Record remaining comments/roles and UI work at Week 16 handoff.
   Docker/Redis and AI stay in their scheduled phases. Restore evidence remains open.

## Evidence and history

- [Week 15 report](weekly-reports/week-15.md) is the chronological evidence log.
- [Week 14 report](weekly-reports/week-14.md): identity integration and PR #42 merge.
- [Previous status snapshot](weekly-reports/archive/status-before-2026-10-19-preview.md)
  preserves the former 1,828-line history. This file now contains current status only.
- Yesterday's 14-file bootcamp package was committed and pushed on 20 October as
  `3be0f38` on `feature/week-15-documentation`; main is not merged. The follow-up
  Month 04 alignment correction was pushed as `3afb5f1` on the same branch.
  TicketTable/StatusBadge was pushed as `30e5d03` on 20 October. Bootcamp
  evidence for 20–21 October is maintained on the documentation branch; the product
  release is externally blocked as described above.
- GitHub heads rechecked on 19 October: bootcamp main `42cf59c`; product main
  `b0e6cab`, feature head `2f6e00d`. Product feature is three commits ahead of main;
  no open PR exists in either repository. No unpublished product files were found.
- [Month 03 retrospective](monthly-reports/month-03.md) consolidates Weeks 09–12;
  [roadmap audit](notes/career/week-15-roadmap-audit.md) records remaining gaps.
