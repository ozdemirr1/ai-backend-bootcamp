# Month 04 alignment review — 20 October 2026

The learner supplied the original weekly milestones: React foundations, API
integration, dashboard, then UI polish. Compare against actual code, not only the
later revised weekly plans. Career direction is aligned; delivery against that
original feature schedule is incomplete.

| Original outcome | Current evidence | Remaining gap |
| --- | --- | --- |
| Week 13: components, props/state, events, lists and forms | Typed components, controlled forms, mock Ticket list and tests | Continue independent exercises; test counts do not establish learner mastery |
| Week 14: API service, identity flow, loading/errors and validation | Fetch boundary, registration/login/current User, in-memory token and session tests | Real Ticket reads and protected URL routing are not implemented |
| Week 15: table, filters/search, badges, detail, comments and role controls | Current UI is an unfiltered mock list; status is rendered as text | Dashboard work is outstanding; list/detail and Comment APIs have dependencies |
| Week 16: Tailwind, responsive shell/sidebar, empty states, toast/modal, accessibility | Basic CSS/forms and a simple empty-list message exist | Full UI package and screenshots of that package are not complete |

## Source observations

OpsDesk at `2f6e00d`: `frontend/src/App.tsx` switches among three screens via local
state and renders `mockTickets`; it is not a URL-based router. `TicketList.tsx`
renders a list, not a table with filters/search/detail selection. Conditional
session buttons are not proof of organization-role authorization.

`src/opsdesk/tickets/router.py` exposes Ticket creation only. Planned list/detail
work is described in [F11 / issue 19](https://github.com/ozdemirr1/opsdesk/blob/2f6e00d5157d820adbd54dcc20464cee917c6bf3/docs/issues/f11.md).
Comment persistence, migration and read/write APIs are a separate
[F14 / issue 24](https://github.com/ozdemirr1/opsdesk/blob/2f6e00d5157d820adbd54dcc20464cee917c6bf3/docs/issues/f14.md)
package. These are source planning records, not a fresh assertion of GitHub issue status.
The current User profile has no global organization role; controls need the selected
Organization's membership context, and server checks remain authoritative.

## Correction to the previous assessment

The 19 October audit correctly recognized the backend-focused career direction,
but understated the variance from the original frontend plan. Hosting a working
identity preview does not replace a working Ticket dashboard. Moving every missing
feature to a vaguely defined later phase would hide accumulated scope.

The original Week 14 expectation assumed the Ticket-read API was ready; it was not.
Comments likewise require backend work beyond a React form. This dependency gap,
together with the early hosting work, explains the variance without erasing it.

## Bounded recovery

1. Finish the interrupted documentation publication first (pushed as `3be0f38`).
2. Restore dashboard learning to the remaining Week 15 sessions. Explain a small
   analogous table/state example, then let the learner implement Ticket components.
   Keep all fixture data visibly marked; do not fake persisted changes or role grants.
3. Scope the real list/detail backend with organization/requester isolation,
   pagination and database tests. Client filters on one page cannot be advertised
   as searching all remote records. Add API-backed Organization context as needed.
4. Prioritize real Ticket integration plus a bounded UI pass in Week 16. Record
   realistic remaining Comment/role work if the original MVP exceeds capacity.
5. Retain deployment exposure/cost/recovery follow-up, but timebox it separately
   from local React learning. Do not promise unrestricted/public-production readiness.

Keep in-memory token handling; the old generic phrase "token storage" does not
require localStorage. Protected navigation is a UX boundary, not server security.
Tailwind follows component/CSS understanding. Toasts and modals should solve a real
interaction, not be added solely for a checklist. The optional small open-source
documentation/test contribution remains optional after the core month deliverables.

## Honest Month 04 exit evidence

- Backend/frontend run locally with documented setup and meaningful behavior tests.
- Clearly distinguish the live identity flow from fixture-backed Ticket screens.
- Verify the implemented real Ticket slice before claiming frontend MVP completion.
- Record responsive/keyboard/error-state review and current UI screenshots in the
  product README. Marketing artwork alone is not this evidence.
- List deferred features, their dependencies and revised estimates at monthly handoff.

No application code or new regression run was produced during this planning review.
