# Week 16 Plan — Real Ticket reads and a bounded UI pass

## Dates, capacity and starting point

26 October–1 November 2026, Month 04. Prepared on 25 October. Capacity: 18 planned
hours, six three-hour sessions; Wednesday is optional rest/catch-up, not extra
required capacity. Estimates are not measured work logs.

Week 15 delivered the live identity preview and a tested mock Ticket dashboard.
Railway recovered on 25 October at source commit `255f937`; no provider migration
is required for the resolved deployment pause. The adapter is ready, but Ticket
GET endpoints, runtime response validation and real frontend integration are not.
See [Week 15 evidence](week-15.md) and the existing
[F11 contract](https://github.com/ozdemirr1/opsdesk/blob/main/docs/issues/f11.md)
before implementing a new API shape.

The original Week 16 was UI polish. Missing Week 14/15 real-data dependencies now
consume part of that capacity: allocate 12 hours to backend/integration, 3 to
visible UI work, and 3 to final verification/handoff. The backend/integration
estimate is provisional and may reach 15 hours. If it does, reduce the UI slice
and explicitly carry unfinished UI forward; do not quietly claim the original
Month 04 MVP is complete.

## Architecture and learning boundaries

Keep synchronous SQLAlchemy, request-scoped Sessions, explicit transactions and
existing membership guards. Scope database queries by Organization and allowed
requester before pagination/counting. Customers see only their own requester
membership's Tickets; permitted staff see Tickets within their Organization.
A client-supplied Organization ID is not authorization. Use the existing F11
rules for inactive/suspended membership and hidden/foreign-resource responses.

The data path is: authenticated Organization context → bounded Ticket read →
runtime JSON validation → display adapter → existing table/detail components.
TypeScript types and the pure adapter do not validate network input. Reject unsafe
numeric IDs rather than silently rounding PostgreSQL bigint values. Count and
items must use the same scope and consistent database view.

Keep the public mock preview explicitly separate from the authenticated real-data
screen. Clear private data on logout/invalid session/Organization switch and
prevent late requests from restoring stale results. Tokens stay in memory;
reload requires login. A UI guard never replaces backend authorization.

The existing local title search covers only its local collection. Do not label it
as a global search across paginated server results. Use supported server filters;
global title search needs a separately reviewed query contract. Do not introduce
an arbitrary router/state library just to satisfy a checklist. Record protected
screen behavior separately from URL-routing/deep-link support.

Before each product exercise, explain its boundary and demonstrate one small
analogous example. Learner implements the scoped behavior, followed by review and
meaningful tests. Do not generate an entire backend/frontend rewrite at once.

## Daily plan

| Day | Budget | Work | Acceptance evidence |
| --- | --- | --- | --- |
| Mon 26 | 3 h | Verify merged starting state; establish weekly product branch. Review F11 query/envelope and access matrix; implement bounded read inputs and first scoped repository query. | Invalid/duplicate/unknown query inputs rejected according to contract; deterministic order and tenant/requester scope reviewed. |
| Tue 27 | 3 h | Complete list/detail repository/service and endpoint wiring with existing guards. | Real `opsdesk_product_test` cases cover two Organizations, customer/staff scope, foreign/hidden detail, empty results and pagination/count consistency. No demo/dev destructive tests. |
| Wed 28 | Optional | Rest or carry unfinished Tuesday work. | No additional mandatory package or assumed hours. |
| Thu 29 | 3 h | Organization selection, Ticket response guards and fetch/service layer; connect list with loading/empty/error states. | Safe IDs/shapes checked; correct authenticated Organization context; authorization, empty state and network errors kept distinct; mocked response tests. |
| Fri 30 | 3 h | Connect detail and pagination; verify session/Organization changes and stale responses. | Private state clears on logout/invalid session/switch; late results cannot repopulate it. Local end-to-end walkthrough uses synthetic data. |
| Sat 31 | 3 h | Bounded UI pass: Tailwind fundamentals and consistent spacing/type/controls; responsive shell/sidebar and visible focus. | Check desktop/narrow viewport, keyboard navigation and readable empty/error states. Choose one coherent small visual slice if time is tight. |
| Sun 1 Nov | 3 h | Relevant regression, build/lint, CI, normal PR merge and deployment evidence; Month 04 retrospective and handoff. | Record implemented/missing scope, tested source and deployed source, actual UI evidence and next-month dependencies. |

Re-estimate after Tuesday. If tenant-safe reads are not passing, finish that slice
before connecting the browser. Do not replace the missing backend with fixture
responses and call the real-data goal complete. Friday's checkpoint decides how
much Saturday styling is feasible; preserve Sunday verification time.

## Acceptance checklist

- [ ] List/detail routes implement the reviewed contract and tenant-safe tests.
- [ ] Pagination/order/count remain correct under scoped access and empty results.
- [ ] Runtime guards reject malformed responses and unsafe numeric IDs.
- [ ] Authenticated Organization context reaches real list/detail requests.
- [ ] Logout, expired/invalid session and Organization switches clear private data.
- [ ] Slow or failed requests cannot display data for the wrong session/Organization.
- [ ] API loading/error/empty states are understandable; mock versus live is explicit.
- [ ] One bounded visual slice is checked on desktop, narrow screens and keyboard.
- [ ] Relevant test groups, CI and source/deployment SHA evidence are recorded separately.
- [ ] Existing weekly report, README and Month 04 retrospective reflect actual results.

## Explicit backlog and operational follow-up

Use the [carry-over matrix](../notes/react/month-04-alignment.md#25-october-checkpoint-and-carry-over)
as the month-end scope ledger. Within Sunday's three-hour handoff, size and order
F14 comments, F07–F10 membership/role work, F12/F13 Ticket mutations and Q03 database
CI; assign explicit follow-up capacity before changing Month 05 scope. These are
not secretly added to this 18-hour week. R01 remains the broader backend release,
not a synonym for the already-live identity preview.

On Monday, briefly verify trial usage/remaining credit, exposure and the
stop/export decision point. On Tuesday, decide the read-API estimate; on Friday,
decide the feasible styling slice. Reserve Sunday for verification and handoff.
If abuse, backup/restore or rollback work needs more time, record its estimate and
trade-off explicitly rather than treating a green deployment as completion.


- Comments and role-dependent mutation buttons need their own backend contracts,
  authorization and tests. Do not add inert controls or infer authorization from
  button visibility. These original Month 04 goals remain incomplete until delivered.
- Toasts and modals are conditional on a real interaction; full visual polish may
  need a follow-up. No new URL-routing/deep-link milestone is assumed completed.
- Check current Railway trial usage and plan stop/export before credit exhaustion;
  no paid subscription or guaranteed uptime is approved. Keep operational checks
  within the allocated sessions; document interruptions and revise scope.
- Public negative/reload cases, bounded auth abuse controls, provider audit review,
  and an isolated restore/rollback exercise remain tracked. A successful deploy
  does not close those items. Never restore over the live demo or expose secrets.
- A first small open-source documentation/test PR is optional after core gates;
  it is not an additional required session.
- Docker/Redis remain Month 05, AI Month 06. At month-end, record unfinished
  prerequisites explicitly rather than silently shifting the entire roadmap.
- Finish Month 04 evidence and a focused handoff before opening the Month 05
  project-scoped conversation. Stay in the current Month 04 conversation this week.

## Notes, commits and interview practice

Maintain existing React notes and add implementation evidence to `week-16.md`
when work begins; this plan does not claim any Week 16 code is implemented.
Use `feature/week-16-ticket-integration` for the product branch after Week 15's
normal merge. Keep daily meaningful commits and normal PR merges (`--merge`).
Update frontend README when setup or actual capabilities change.

Explain with an OpsDesk example:

1. Why must authorization filtering happen before pagination and count?
2. Why is a TypeScript response type insufficient at an HTTP boundary?
3. How can a late response leak the previous Organization's data into the screen?
4. What does a readiness check prove that a successful frontend build cannot?
5. How do UI role checks differ from server-side authorization?
