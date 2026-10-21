# Weekly Status

## Current checkpoint — 21 October 2026

Week 15, Month 04; 19–25 October. First public identity preview is working.

- Product branch: `feature/week-15-railway-preview`.
- Pushed head: `3a5b11b` on the Week 15 product branch; product tree is clean.
- Demo: https://opsdesk-production-448f.up.railway.app/
- One FastAPI service serves the built React frontend and API on the same origin;
  PostgreSQL is a separate persistent service. Node 24 builds frontend assets;
  Uvicorn runs the application. No Vite development server is hosted.
- Learner local evidence: 506 non-integration backend tests passed; 160 database
  tests deselected; Ruff and whitespace checks passed. Frontend production build
  with `VITE_API_BASE_URL=/` passed. Actual HTML/CSS/JS were served by TestClient.
- Independent public checks returned 200 for HTML, the referenced JavaScript,
  and readiness. Learner confirms Tickets, registration, login, session check,
  logout and Tickets → Login navigation. Supplied network screenshot shows
  registration 201, login 200, profile/session check 200.
- Tickets still show three mock records. No real Ticket workflow or AI is in the UI.
  Tokens remain in memory; reload requires login. Latest public-browser negative
  cases and reload behavior still need explicit evidence.
- Railway's latest successful deployment metadata still points to `2f6e00d`.
  The 21 October latest-source deployment request was rejected with `Deploys have
  been paused temporarily`; [Railway's incident page](https://status.railway.com/)
  confirms a platform deployment pause. Table release and runtime-SHA verification
  remain pending. Today's public liveness/readiness requests returned expected JSON.
- Earlier exact-head [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39470600124)
  and [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39470599975)
  at `30e5d03` both completed successfully, verified 21 October.
- Exact-head [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39639022621)
  and [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39639022552)
  at `3a5b11b` also completed successfully on 21 October.
- Last supplied credit display: USD 4.94 / 29 days. Not a current balance or
  monthly forecast. Only trial credit is approved; no paid upgrade.

## Next work

1. TicketTable/StatusBadge are implemented locally; 116 frontend tests, build and
   lint passed on 20 October. Desktop screenshot reviewed; learner confirmed narrow-screen
   scrolling and keyboard/navigation checks. The increment is pushed with passing CI.
   Title search is now implemented locally: 123 frontend tests, build and lint
   passed on 21 October. Chrome screenshots confirmed matching, no-match feedback
   and clearing. A subsequent screenshot confirmed the restyled search field.
   The change is committed and pushed as `3a5b11b`. Next: status filtering and
   combined conditions in the [search/filter exercise](notes/react/ticket-search-filter.md),
   then detail/session behavior with tests. Public deployment remains unverified.
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
