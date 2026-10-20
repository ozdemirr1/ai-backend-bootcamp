# Week 15 Plan — Live identity preview and release verification

## Dates, capacity and outcome

19–25 October 2026, Month 04. Original plan prepared 18 October; revised
19 October after the live browser checkpoint. Planned capacity: 18 active hours
(3 hours on six days; Wednesday optional). Actual time is not inferred from logs.
The first identity preview is already live. The remaining outcome is a reviewable,
operable preview with scoped external feedback, accurate documentation and a
normally merged weekly PR. This is not a complete Ticket or AI product launch.

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

These replace the original Tuesday–Friday setup tasks, which were completed early.
Do not repeat provisioning or broaden scope to fill freed calendar space.

## Revised daily allocation

| Date | Planned time | Work and acceptance evidence |
| --- | --- | --- |
| Mon 19 | 3 h baseline; actual unknown | Completed live identity preview, current-head CI verification, documentation review and LinkedIn draft/images. Bootcamp publication remains pending. |
| Tue 20 | 3 h | Verify deployed SHA (recheck CI if head changes); document public registration/login abuse boundaries. Implement a bounded control only after choosing policy, trusted proxy/IP behavior and restart/replica limitations; test allowed requests, rejection and recovery. Keep broad test invitation pending until reviewed. |
| Wed 21 | Optional | Rest or catch-up. No required new feature or assumed spare capacity. |
| Thu 22 | 3 h | Record current trial usage; write shutdown/export steps and code/schema rollback limits. Verify a backup restore in an isolated disposable database, never by resetting the Railway demo. Record what was actually exercised. |
| Fri 23 | 3 h | Hosted browser negative cases (duplicate 409, wrong password 401), reload reset, network-error recovery and narrow/mobile layout. Document demo-only data, no real support content, data reset/contact expectations. Fix confirmed defects with relevant tests. |
| Sat 24 | 3 h | Invite a small manual feedback group; collect usability/error findings without credentials. Address reproducible issues. Recheck the already prepared LinkedIn draft/images against current behavior; publish only when Furkan chooses. |
| Sun 25 | 3 h | Relevant regression and exact-head CI; review weekly PR and merge with `--merge`; choose/verify Railway branch after merge, deployed SHA and smoke. Close report, record usage and hand off to Week 16. |

If abuse-control or restore work exceeds its allocation, defer optional polish and
broad sharing. Record unfinished work explicitly; do not waive checks or change
provider/paid plan just to satisfy the calendar. Docker/Redis remain Month 05;
AI remains later. Organization/Ticket-read UI is a separately planned dependency.

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

## External feedback and release gates

- [x] Current-head Backend and Frontend CI pass at `2f6e00d`.
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

Week 16 planning follows Sunday's evidence. Timebox any unfinished operations work
explicitly instead of letting it absorb the whole frontend month. Prefer one screen
using the existing Organization read API, paired with a small responsive/accessibility
exercise. Select its exact scope at handoff; this is a sequencing recommendation,
not a second weekly implementation commitment. Real Ticket reads remain a backend
dependency. Full redesign, all Ticket workflows and AI do not fit this package.

The three-hour abuse-control and backup/restore allocations include explanation,
implementation and verification. If either is too large, record the incomplete
gate and a narrower next step; do not introduce Redis early or assume a restore
succeeded from a written command alone. Actual study hours remain learner-reported.

## References checked during implementation

- [Railpack configuration](https://railpack.com/config/file/)
- [Vite environment variables](https://vite.dev/guide/env-and-mode)
- [Railway trial](https://docs.railway.com/pricing/free-trial)
- [Railway cost control](https://docs.railway.com/pricing/cost-control)
- [GitHub deployment controls](https://docs.railway.com/deployments/github-autodeploys)

Trial terms were checked on 18 October; the plan does not promise a full month of
uptime or approve a paid subscription.
