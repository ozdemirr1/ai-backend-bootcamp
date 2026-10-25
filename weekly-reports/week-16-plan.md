# Week 16 Plan — Complete the Month 04 frontend MVP

## Commitment, dates and capacity

26 October–1 November 2026. Revised on 25 October at the learner's request to
include **all original Month 04 learning/product outcomes**, not only real reads
and a small UI pass. The learner selected an intensive calendar for these dates.

Plan **42 focused hours**, six hours on each of seven days, plus **up to 8 hours
of contingency** (two hours each on Tuesday, Thursday, Saturday and Sunday if
needed). Split core days into two three-hour blocks with breaks. Wednesday is a
working day in this revision. Estimates include explanation, implementation,
review and feature tests; they are not measured work logs or a delivery guarantee.

This replaces the earlier 18-hour plan. Do not achieve the deadline by dropping
comments, role controls, styling, learning review or tests. Re-estimate at the
Tuesday and Friday checkpoints. If the full acceptance gates cannot fit in the
50-hour ceiling, report the specific blocker and remaining estimate and agree an
explicit calendar correction; do not mark Month 04 complete or silently move its
missing work into Month 05.

Starting evidence: [Week 15](week-15.md), merged product documentation at
`3649a14`, runtime source `255f937`. Identity works; the Ticket dashboard still
uses fixtures. The display adapter is implemented, but Ticket reads, Comment
persistence/API and the real-data UI are not. This document is a plan, not a
claim that any new Week 16 feature has shipped.

## Original Month 04 outcomes and completion evidence

| Original outcome | Week 16 completion requirement |
| --- | --- |
| Components, props, state, events, conditional/list rendering, form handling | Retain Week 13 evidence; learner explains and applies these concepts to Organization selection, CommentForm and TicketDetail without skipping review |
| Fetch/API service layer, token handling | Real Organization/Ticket/Comment requests through typed adapters and runtime guards; tokens remain in memory, no refresh-token or localStorage expansion |
| Protected route | Real dashboard/detail URLs require a verified session; reload/direct navigation leads to login and a safe in-app return target; mock preview is separately labelled and public |
| Loading/error state and form validation | Registration/login, Organization/Ticket creation, reads, comments and priority mutation have explicit loading, validation, error and success handling |
| Ticket table and real API list | Authenticated Organization context, scoped paginated records, deterministic ordering and consistent count; no fixtures in the real dashboard |
| Filter and search | Combined status filter and reviewed server-side title search across the caller's visible records; reset page when inputs change; no claim that searching one page searches all records |
| Status badge and detail page | Readable badges and a real detail URL/card; wrong-tenant/hidden/not-found states do not reveal private data; browser Back works |
| Comment form | Persisted append-only comments; authorized list/post, form validation, safe failure/uncertain-outcome feedback and closed-Ticket restrictions |
| Role-dependent buttons | Working priority-change action for agent/admin/owner on permitted Ticket states; hidden for customer, enforced again by backend; no client-controlled role grants |
| Tailwind and coherent visual design | Shared colors, spacing, typography, form/button/table/card styles across identity, dashboard and detail screens; replace conflicting CSS deliberately |
| Responsive layout and sidebar | Coherent application shell; desktop sidebar and keyboard-accessible narrow-screen navigation; usable controls/table on mobile, tablet and desktop |
| Empty states | Distinguish no memberships, no Tickets, no search matches and no comments from loading, forbidden access and failed requests |
| Toast notification | Accessible success feedback for actual writes; failures remain understandable near the affected form; essential feedback does not vanish only in a toast |
| Modal | Working create-Ticket modal using the existing creation API, with field validation, duplicate-submit prevention, focus management, Escape/close and focus return |
| Basic accessibility | Labels, semantic headings/table, keyboard-only operation, visible focus, readable contrast, non-color status cues and accessible errors/status messages |
| Month-end demo, README and repository | Backend/frontend run locally; deployed source and smoke evidence recorded; actual screenshots in README; normal PR merge/CI, clean Git state and Month 04 retrospective/handoff |

For a first-time account, provide Organization selection plus an empty-state
create-Organization path through the existing API. This makes the real dashboard
usable without manually pasting database IDs. Ticket creation uses the existing
POST API; it is not another new backend CRUD package.

## Backend dependencies and scope boundaries

1. **F11 / #19:** implement list/detail, the reviewed visibility/filter/pagination
   envelope, and real PostgreSQL authorization tests. Review and document the
   title-search contract amendment before implementing it; retain current query
   validation and error precedence. Proposed `q` searches titles only: define
   bounded input, normalization, case handling and literal wildcard treatment.
   Apply it inside tenant/requester scope before count and pagination. Parameterize
   queries; cover punctuation, Unicode, blank input and combined filters.
2. **F14 / #24:** Comment model/Alembic migration, tenant-consistent foreign keys,
   cleanup/schema guards, list/post repository/service/routes, actor-derived
   author, validation, pagination, rollback and shared-lock protocol. Test posting
   against a coordinated closing operation with independent transactions, even
   while the public workflow endpoint remains future work.
3. **F12 / #20 — priority subset:** implement the reviewed priority endpoint with
   current role/resource/status checks, no-op timestamp behavior, ordered locks,
   rollback and safe errors. This supplies a real role-dependent UI action.
   **Do not close all of #20**: assignment endpoints remain outside this subset.

Reference the existing [F11](https://github.com/ozdemirr1/opsdesk/blob/main/docs/issues/f11.md),
[F14](https://github.com/ozdemirr1/opsdesk/blob/main/docs/issues/f14.md),
[F12](https://github.com/ozdemirr1/opsdesk/blob/main/docs/issues/f12.md),
[API contract](https://github.com/ozdemirr1/opsdesk/blob/main/docs/api-contract.md)
and [access rules](https://github.com/ozdemirr1/opsdesk/blob/main/docs/access-control.md).

The original Month 04 requirement is role-aware frontend behavior, not a complete
membership-administration product. Membership directory/addition/reactivation,
role/deactivation/ownership-transfer APIs (F07–F10), assignment (rest of F12), full
status workflow (F13), Attachments and the broad R01 release stay separately tracked.
Do not add their buttons or mark their issues done. Demonstrate customer versus
staff using separate synthetic identities and controlled local fixtures; never
add a client-side role selector or an unguarded production seed shortcut.

Q03 database CI remains an identified engineering backlog item. Required local
PostgreSQL and migration tests still run this week; excluding Q03 does not permit
skipping them. Docker/Redis/background jobs remain Month 05 and AI Month 06.
The optional first open-source contribution is still optional after core gates.

## Architecture and learning boundaries

Data flow: verified session → API-backed Organization/own membership → scoped
repository/service/route → runtime response validation → display adapter → UI.
A selected Organization ID or hidden button is never authorization. Customers see
only their requested Tickets; staff see in-Organization Tickets. Queries must
apply access scope before pagination/count. Count and items use a consistent view.

Keep synchronous SQLAlchemy, request-scoped Sessions and explicit transaction
ownership. Alembic owns new schema changes. Destructive tests use only the guarded
`opsdesk_product_test`; never `opsdesk_product_dev`, `opsdesk_demo` or the old
learning database `opsdesk_test`. Extend exact revision/cleanup/schema expectations
when adding Comments; do not keep claiming the old head is current after migration.

Validate unknown JSON before mapping it; reject unsafe numeric IDs and malformed
response shapes. Keep error, empty and denied outcomes distinct. Clear private data
and cancel/ignore stale results on logout, invalid session, Organization change,
route change and replacement requests. Changing search/status resets pagination.

Add a small routing layer for real dashboard/detail URLs; review the dependency
choice before installing it. Handle direct URLs and refresh in both Vite and the
hosted FastAPI static-serving path without swallowing API/asset 404s. Accept only
safe internal return paths; never put tokens in URLs. Do not add a state framework.

Role-aware UI uses the selected Organization's checked own-membership role and
Ticket state; every mutation rechecks current server state. Abort is not proof a
write rolled back. Preserve entered content when retry is uncertain and avoid
blind duplicate comment/ticket writes. No secret, password or token in Git/logs.

Each package starts with a short architectural explanation and one analogous
example. Learner implements the exercise; mentor reviews. Include a small
independent change or verbal walkthrough before declaring its learning goal met.
No bulk code generation or invented learner answers to meet the calendar.

## Work packages and hours

| Package | Core hours | Includes |
| --- | ---: | --- |
| A — Scoped reads and title-search contract | 8 | Contract review, repository/service/routes, validation, tenant/pagination tests |
| B — Real-data UI and navigation | 6 | Organization selection/creation, runtime guards, list/detail/filter/search, protected routes and stale-request tests |
| C — Persistent comments | 8 | Migration/guards, read/write API and concurrency tests, CommentForm/list and behavior tests |
| D — Role-aware priority operation | 4 | API subset, role/state/no-op tests, real UI action and forbidden direct-request checks |
| E — Complete Month 04 UI package | 8 | Tailwind, shared visual styles, responsive shell/sidebar, empty states, create-Ticket modal, toast and accessibility |
| F — Integrated verification | 4 | Multi-user/tenant walkthrough, relevant regression suites, build/lint, keyboard/viewport review and corrections |
| G — Release and learning handoff | 4 | CI/normal merge, deploy/smoke checks, screenshots/setup docs, retrospective and learner review |
| **Core total** | **42** | Feature tests and review are included within their packages |
| **Contingency ceiling** | **8** | Actual defects, migration/routing issues and review corrections; no new features |

## Daily schedule — intensive calendar

| Day | First 3-hour block | Second 3-hour block | Exit evidence |
| --- | --- | --- | --- |
| Mon 26 | A: baseline/contract/access review; scoped query | A: list/detail service/routes and initial tests | Reviewed search/visibility contract and first passing vertical slice; inspect trial usage/stop-export decision point |
| Tue 27 | A: 2 h complete database/pagination/search tests; B: 1 h Organization/session design | B: 3 h Organization selection/creation, route shell and guards | F11 tests pass before private UI requests; selected Organization/role comes from API; use up to 2 h reserve if needed |
| Wed 28 | B: 2 h real table/detail/search integration and request-race tests; C: 1 h schema review | C: 3 h Comment migration/model and scoped repository | Real-data walkthrough works; Comment migration/guard update tested locally |
| Thu 29 | C: 3 h Comment service/API, contention and authorization tests | C: 1 h CommentForm/list; D: 2 h priority API/service | Persisted comments and deny/rollback cases pass; priority boundary reviewed; up to 2 h reserve |
| Fri 30 | D: 2 h role-aware UI and priority tests; E: 1 h Tailwind/style primitives | E: 3 h responsive shell/sidebar and identity/dashboard/detail styling | Real customer/staff contrast demonstrated; shared visual structure in place; review remaining estimate |
| Sat 31 | E: 3 h create-Ticket modal, toast, empty states and accessibility | E: 1 h finish visual consistency; F: 2 h integrated/viewport/keyboard tests | Every original UI item exists and has meaningful behavior; up to 2 h reserve for defects |
| Sun 1 Nov | F: 2 h final regression/corrections; G: 1 h PR/CI readiness | G: 3 h merge/deploy/smoke, screenshots/docs, retrospective and learning review | All acceptance gates below evidenced; source/deployment hashes recorded; up to 2 h reserve |

Tuesday gate: assess backend scope using actual tests, not file count. Friday gate:
verify comments and the priority action before spending the final UI block. If a
package overruns, consume explicitly recorded reserve and recalculate the remainder;
do not silently delete an acceptance row. External deployment failure is recorded
as a blocker, not application completion or a reason to change providers implicitly.

## Month 04 completion gates

- [ ] All original-outcome rows above have concrete code and verification evidence.
- [ ] A synthetic account can register/login, create/select an Organization, create
      a Ticket, find it through real search/filter/pagination, open its URL and post
      a persisted Comment; reloading/relogging reads persisted data.
- [ ] Two Organizations and separate customer/staff identities demonstrate read
      isolation, priority controls, denied direct API attempts and unchanged state
      after rejected/failed mutations. Closed-Ticket comments are rejected.
- [ ] Protected direct URLs, browser Back, logout, reload, invalid sessions,
      Organization changes and late responses cannot restore another scope's data.
- [ ] Comment schema and data suites pass separately against `opsdesk_product_test`;
      record exact commands/counts/revision and no drift. No demo/dev destructive tests.
- [ ] Relevant backend/frontend regressions, frontend build/lint, backend Ruff and
      exact-head Backend/Frontend CI pass; do not sum historical test groups.
- [ ] Tailwind styles cover all scoped screens; sidebar/navigation, table/detail,
      forms, empty/loading/error states, modal and toast work at desktop/tablet/mobile
      widths and with keyboard-only operation. Record actual viewport evidence.
- [ ] Safe demo smoke: happy path, duplicate registration, wrong password, missing/
      invalid token, forbidden scope and reload. Record current hosting usage and
      operational limits; no real customer data or credentials in screenshots.
- [ ] Review release recovery: new migration permissions, backup before migration,
      old/new app compatibility and a tested recovery path in an isolated environment;
      never restore over the live demo or automatically downgrade populated tables.
- [ ] Remaining abuse/audit/backup findings are explicitly assessed before expanding
      the public demo invitation. Unresolved release-blocking findings stop publication;
      a green health endpoint alone does not satisfy this gate.
- [ ] Normal PR merge preserves daily commits; verify deployed source contains the
      intended runtime changes and run post-deploy checks. Coordinate the Railway
      source branch explicitly; pushing an unrelated branch is not deployment.
- [ ] Update product/frontend README with reproducible setup and real screenshots;
      both repositories have clear status and clean, synchronized Git state.
- [ ] Complete `week-16.md`, `monthly-reports/month-04.md` and learner review only
      after evidence exists. Record original targets, delivered results, measured
      hours if available, remaining non-Month-04 backlog and the Month 05 handoff.

## Notes, commits and interview practice

Maintain the existing React foundations/search notes; add scoped learning sections
for routing, response guards, CommentForm, role checks, Tailwind and accessibility.
Use the existing Week 16 plan and the normal weekly report when work begins; no
ad hoc daily work documents. Contract amendments belong in OpsDesk's existing API,
access, migration and feature documents. Keep a completed/planned distinction.

Product branch: `feature/week-16-month-04-completion` from current merged main.
Use meaningful daily commits for A–G and normal PR merges (`--merge`); keep the
Railway source branch until its replacement is verified. Close #19/#24 only when
all issue acceptance criteria pass; mark only the priority subset of #20 complete.
Do not close R01 or membership/workflow issues from frontend MVP completion alone.

Learner review questions:

1. Why must requester/tenant/search filters be applied before pagination/count?
2. What does runtime validation protect that a TypeScript type cannot?
3. How do protected routes, button visibility and server authorization differ?
4. What happens if logout or an Organization change occurs during a read or write?
5. Why do Comment posting and Ticket closing need cooperating locks?
6. How do modal focus handling, accessible feedback and color-independent badges help?
7. What do local tests, CI, readiness and a public browser smoke test each prove?

Keep the current Month 04 conversation until the completion gates and retrospective
are finished, then start Month 05 with its focused handoff. No Month 05/06
implementation or claimed completion is created by this planning change.
