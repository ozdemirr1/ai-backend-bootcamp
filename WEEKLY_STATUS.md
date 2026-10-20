# Weekly Status

## Current checkpoint — 19 October 2026

Week 15, Month 04; 19–25 October. First public identity preview is working.

- Product branch: `feature/week-15-railway-preview`.
- Pushed head: `2f6e00d5157d820adbd54dcc20464cee917c6bf3`.
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
- Learner reports automatic build after push. Exact deployed runtime SHA for
  `2f6e00d` has not yet been checked inside the container.
- Latest GitHub inspection: [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39281732882)
  and [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/39281732888)
  at `2f6e00d` both completed successfully, rechecked through GitHub CLI on
  19 October. This supersedes the earlier queued checkpoint.
- Last supplied credit display: USD 4.94 / 29 days. Not a current balance or
  monthly forecast. Only trial credit is approved; no paid upgrade.

## Next work

1. Confirm deployed runtime SHA and public negative cases; current-head CI passed.
2. Review bounded registration/login abuse controls, cost and demo data handling
   before a broad invitation. Small manual feedback tests are technically possible
   now; do not represent the preview as a production support system.
3. Follow the revised [daily plan](weekly-reports/week-15-plan.md),
   [deployment notes](notes/deployment/opsdesk-railway-preview.md) and
   [LinkedIn draft](notes/career/opsdesk-live-preview-linkedin.md).
4. Record backup/restore and rollback procedure, then normal PR merge and Week 16
   handoff. Do not introduce Docker, Redis, AI or Ticket-read work into this package.

## Evidence and history

- [Week 15 report](weekly-reports/week-15.md) is the chronological evidence log.
- [Week 14 report](weekly-reports/week-14.md): identity integration and PR #42 merge.
- [Previous status snapshot](weekly-reports/archive/status-before-2026-10-19-preview.md)
  preserves the former 1,828-line history. This file now contains current status only.
- Bootcamp documentation edits are local and uncommitted; product code is pushed.
- GitHub heads rechecked on 19 October: bootcamp main `42cf59c`; product main
  `b0e6cab`, feature head `2f6e00d`. Product feature is three commits ahead of main;
  no open PR exists in either repository. No unpublished product files were found.
- [Month 03 retrospective](monthly-reports/month-03.md) consolidates Weeks 09–12;
  [roadmap audit](notes/career/week-15-roadmap-audit.md) records remaining gaps.
