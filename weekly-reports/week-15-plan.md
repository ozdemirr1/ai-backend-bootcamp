# Week 15 Plan — Dashboard foundation and bounded preview follow-up

## Dates, capacity and outcome

19–25 October 2026, Month 04. Original plan prepared 18 October; revised
19 October after the live browser checkpoint; corrected 20 October against the
learner's original Month 04 dashboard milestones. Planned capacity: 18 active hours
(3 hours on six days; Wednesday optional). Actual time is not inferred from logs.
The first identity preview is already live. The 19 October revision overallocated
the remaining frontend week to operations and deferred the dashboard. Restore
dashboard learning as the primary remaining outcome: a tested table, local search/
filter behavior, status badges and a bounded detail view, with data provenance
explicit. This is not yet the original complete frontend MVP: real Ticket reads,
comments and organization-role behavior have backend dependencies.

The previous plan is preserved in bootcamp commit `3be0f38`. See the
[Month 04 alignment review](../notes/react/month-04-alignment.md) for the gap analysis.

## Completed before and during Monday

- [x] Week 14 PR #42 normal merge; start the Week 15 feature branch.
- [x] Railway trial selected; API and persistent PostgreSQL provisioned.
- [x] Guarded hosted Alembic target, explicit roles/grants, migrations to `31be9023cfb2`.
- [x] Container-local positive and negative identity smoke on `cec7ce7`.
- [x] Liveness/readiness and bounded connection/pool waits; public HTTPS health.
- [x] Same-origin React build served by FastAPI; optional asset configuration/tests.
- [x] Product head `2f6e00d` pushed; learner reports automatic build.
- [x] Public browser registration/login/profile/session/logout/navigation confirmed.
- [x] Local backend 506 passed / 160 deselected; real frontend build/file-serving check.
- [x] Exact-head Backend and Frontend CI passed at `2f6e00d`, rechecked 19 October.
- [x] LinkedIn draft and two accompanying still images prepared; publication unconfirmed.

Do not repeat provisioning. The completed identity preview supplements the original
dashboard goal; it does not replace it or establish Month 04 completion.

## Revised daily allocation

| Date | Planned time | Work and acceptance evidence |
| --- | --- | --- |
| Mon 19 | 3 h baseline; actual unknown | Completed live identity preview, current-head CI verification, documentation review and LinkedIn draft/images. Bootcamp publication remains pending. |
| Tue 20 | 3 h | Finish yesterday's documentation commit/push and correct the Month 04 scope. Limit preview triage to runtime SHA/usage and recording any exposure issue. Explain table component/props/state design with a small analogous example; learner starts TicketTable and StatusBadge using explicitly labelled fixtures. |
| Wed 21 | Optional | Catch-up selected: verify Tuesday's push and CI, record Railway release outcome, publish bootcamp evidence, and prepare the search/filter exercise. No additional mandatory feature or assumed spare capacity. |
| Thu 22 | 3 h | Learner implements status filter and title search as derived state; test combined conditions, clearing filters, no matches and semantic table output. Search/filter operates on the labelled fixture collection, not an entire remote paginated collection. |
| Fri 23 | 3 h | Bounded Ticket detail selection/view and return navigation; expand fixtures explicitly where detail fields are needed. Add session-aware access to the dashboard and tests for signed-out/logout behavior. Do not present a conditional screen as a completed URL router. |
| Sat 24 | 3 h | Review Ticket-read contract and tenant authorization dependencies, map the table/detail adapter, and estimate the real list/detail package. Review Organization selection/membership context and empty state. Fix dashboard defects; begin a backend slice only if its reviewed scope and tests fit. No mandatory public launch or new artwork. |
| Sun 25 | 3 h | Relevant frontend regression/build/lint and exact-head CI; document implemented versus fixture-backed behavior and outstanding reads/comments/roles. Review weekly changes and normal PR merge only for completed scope; verify deployment if changed. Prepare Week 16 integration/UI plan. |

Preview triage is a bounded secondary task, not the remaining week's main syllabus.
If an actual exposure or cost issue requires more work, record that interruption
and reduce sharing while it is resolved; do not label an unreviewed demo ready.
Backup/restore and abuse controls remain open operations work, not silently completed
or unconditional blockers for local frontend learning. No destructive demo changes.
Docker/Redis remain Month 05 and AI remains later. Real Ticket reads need explicit
backend authorization and database tests before integration. Do not replace them
with local filtering and claim the live Ticket API works.

## Architecture decision

Use one API runtime plus one persistent PostgreSQL service. FastAPI serves `/`,
`/favicon.svg` and `/assets`; existing API routes retain their root paths. Railpack
builds React with Node 24 and `VITE_API_BASE_URL=/`, then runs Python/Uvicorn.
This avoids a second frontend runtime and cross-origin configuration; the tradeoff
is a combined frontend/backend release. Local Vite still proxies `/api` only in dev.
An enabled but incomplete frontend build prevents application startup.

Application and migration roles have different privileges, but both credentials
currently enter the same service. Separate prefixes alone are not secret isolation.
No browser-persisted tokens, refresh flow, broad redesign or new technology is added.

## Dashboard acceptance evidence

- [x] Semantic Ticket table and status badges preserve typed inputs and clear labels.
  Implemented locally on 20 October; frontend suite: 116 passed. Desktop screenshot
  reviewed; learner confirmed narrow-screen scrolling and keyboard/navigation checks.
  Pushed as `30e5d03`; both CI workflows passed. Railway publication is blocked by
  the provider's 21 October deployment pause; the previous release remains active.
- [ ] Search/filter combinations and empty/no-match states have behavior tests.
  Title search completed locally on 21 October; 123 frontend tests passed, including
  empty/no-match and navigation-reset coverage. Browser layout confirmed and
  product commit `3a5b11b` pushed. Status filtering and combined
  conditions are still pending; this checkbox remains open.
- [ ] Detail view and return navigation have explicit fixture/real-data provenance.
- [ ] Session-aware dashboard visibility and logout behavior are tested; token remains in memory.
- [ ] Real Ticket list/detail dependency is scoped with tenant-safe API tests; completion is not assumed.
- [ ] Comment submission and organization-role mutations remain unavailable until their APIs exist.

## Open external feedback and release gates

- [x] Current-head Backend and Frontend CI pass at `30e5d03`, verified 21 October.
- [ ] Deployed runtime SHA is checked; CI is repeated if code changes.
- [ ] Public duplicate/wrong-password/reload cases and recovery are recorded.
- [ ] Registration/login abuse policy, control and limitations are reviewed and tested.
- [ ] Trial usage and a stop/export procedure are recorded; no uptime guarantee is made.
- [ ] Demo account/data handling and a contact route are clear to testers.
- [ ] Backup/restore and rollback evidence distinguish instructions from executed steps.
- [ ] Weekly PR reviewed/merged normally; post-merge deployment verified.

A public URL permits external visitors now. Technical reachability is not a claim
of production readiness. Start with synthetic test accounts and a password used
only for this demo; Tickets are mock data. No load testing against the trial service.
Destructive integration/schema tests remain restricted to the dedicated test DB.

## Notes, commits and interview review

Keep deployment reasoning in [deployment notes](../notes/deployment/opsdesk-railway-preview.md),
daily evidence in [the report](week-15.md), and current status in
[WEEKLY_STATUS](../WEEKLY_STATUS.md). Product README must describe tested setup and
current limits. Commit each reviewed behavior separately with `week-15:` wording;
update bootcamp evidence in a separate documentation commit.

Explain in your own words:

1. Why does Vite's development proxy not ship in the built bundle?
2. What changes when frontend and API share one origin?
3. What does `SELECT 1` prove, and what does it not prove about schema/permissions?
4. Why separate migration and runtime roles? What is still shared in this deployment?
5. Why can rate limits based on IP be wrong behind a reverse proxy?
6. What does a code rollback fail to undo after a schema migration?
7. Why can a zero-visitor service still consume credit?

Week 16 prioritizes the reviewed real Ticket-read integration dependency and a
bounded UI pass: Tailwind fundamentals, responsive layout/sidebar, keyboard/focus
behavior and state feedback. Toast/modal work needs a real interaction that benefits
from it; do not add decorative components to tick boxes. Comments and role-dependent
actions require their own backend capability and authorization evidence. At Sunday's
handoff, publish a realistic split if this exceeds capacity; do not declare the
original frontend MVP complete or silently drop its missing features.

## References checked during implementation

- [Railpack configuration](https://railpack.com/config/file/)
- [Vite environment variables](https://vite.dev/guide/env-and-mode)
- [Railway trial](https://docs.railway.com/pricing/free-trial)
- [Railway cost control](https://docs.railway.com/pricing/cost-control)
- [GitHub deployment controls](https://docs.railway.com/deployments/github-autodeploys)

Trial terms were checked on 18 October; the plan does not promise a full month of
uptime or approve a paid subscription.
