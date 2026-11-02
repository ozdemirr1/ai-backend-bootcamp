# Week 16 Report — Month 04 completion work

Planned 26 October–1 November 2026; technical evidence closure continued on
2 November. UI/integration delivered; operational gates and learner reflection
remain explicit, so the full combined Month 04 checklist is not closed.
Follow the [intensive plan](week-16-plan.md). This is the regular weekly report,
not a separate daily work document.

Latest checkpoint: [recovery, release records and Month 04 review](#2-november--recovery-release-records-and-month-04-review).
Earlier pending statements below are dated historical checkpoints.

## 26 October — Monday tasks 1–3

### Baseline inspected

- Bootcamp baseline: `d79e812`, following normal merge of [PR #9](https://github.com/ozdemirr1/ai-backend-bootcamp/pull/9).
- Product baseline: `3d0e10b`, following normal merge of [PR #45](https://github.com/ozdemirr1/opsdesk/pull/45).
- Ticket router/service/repository implement creation only. GET list/detail and
  their validation/repository/service/API tests are absent. Organization read
  code supplies a reusable query-validation and single-snapshot count/page example.
- Frontend TicketResponse/toTicketSummary is a pure display adapter; it performs
  no HTTP request or runtime JSON validation. The public dashboard still uses mocks.
- No current live deployment check or PostgreSQL migration/data run was performed
  in this preparation; the last live evidence remains the 25 October checkpoint.

### Fresh local verification

| Command / check | 26 October result |
| --- | --- |
| `.venv/bin/python -m pytest -q -m 'not integration'` | 506 passed; 160 database/schema tests deselected |
| `.venv/bin/ruff check src tests migrations` | Passed |
| `.venv/bin/ruff format --check src tests migrations` | Passed; 112 files already formatted |
| Frontend `npm test` | Initial run: ENOSPC before any tests executed; not a passed suite |
| Frontend `npm test -- --maxWorkers=1` | Retry: 141 tests / 10 files passed |
| Frontend `npm run lint` / `npm run build` | Both passed |

Frontend commands used the installed Node 24 runtime. Disk inspection after the
initial failure showed about 414 MiB free. No user files were deleted; passing the
one-worker retry does not resolve the disk-capacity limitation. Counts above
verify existing behavior, not the new Ticket read contract. PostgreSQL integration
and schema tests remain separately required when the read implementation exists.

### Access decisions and collection contract

The product's [API contract](https://github.com/ozdemirr1/opsdesk/blob/main/docs/api-contract.md),
[access matrix](https://github.com/ozdemirr1/opsdesk/blob/main/docs/access-control.md) and
[F11 handoff](https://github.com/ozdemirr1/opsdesk/blob/main/docs/issues/f11.md) now
contain the local 26 October contract amendment and pending acceptance cases.
These edits have not yet been committed/published at this checkpoint; links identify
the canonical files, while the local working trees hold this amendment.

- Resolve roles from the selected Organization's current membership. Customer
  reads only requested-by-self Tickets; staff reads within the Organization.
- Apply active actor/membership/Organization and requester scope to actual SQL
  reads before search/filter/count/pagination. Hidden/foreign/missing details share
  a 404 after shared guards. Reading closed/resolved records grants no write right.
- Add optional `q`: title-only contiguous substring, bounded to 255 decoded Unicode
  code points before trim; blank means no search. Preserve internal text, reject
  NUL/LF/CR/TAB and escape wildcard characters as literal input.
- Use database case-insensitive matching, with explicit collation verification;
  do not promise Turkish case folding identical to JavaScript.
- Combine status/priority/assignment/assignee/title with AND; reject duplicate or
  unknown parameters and contradictory assignment filters.
- Default limit/offset are 20/0; limit 1..100, Ticket offset bounded to signed bigint.
  Newest-first ordering uses timestamp then ID. Same-snapshot count and items share
  the same scope; beyond-end pages retain the matching total.

The existing [search/filter note](../notes/react/ticket-search-filter.md) now
explains the change from filtering all mock rows to querying visible server records.
No endpoint, product validator, migration or frontend behavior was changed.
No new feature test is reported as passing; no learner answer is invented.

### Next work

Monday tasks 1–3 are complete as inspection and contract preparation. Continue
with task 4: implement query/envelope schemas, read protocols/service/repository
and GET endpoints in small reviewed increments. Task 5 supplies the new tests;
full PostgreSQL/search/pagination verification continues Tuesday. Use only guarded
`opsdesk_product_test` for destructive database tests. Trial usage review and the
remaining Monday work are not marked complete by this entry.

Documentation validation: 114 Markdown files, 561 local link/image targets and
anchors, and 19 cross-repository file references checked against the local trees.
Both repository whitespace checks pass. All changes in this task are Markdown;
the weekly report is the only new document.


## 26 October — Monday tasks 4–6

The tasks 1–3 section above is the earlier preparation checkpoint. It is retained
as history; the implementation and current results are below.

### Backend implementation

Implemented GET list/detail under `/organizations/{organization_id}/tickets` in
OpsDesk. Query schemas validate title search, exact filter keys, numeric bounds
and contradictory inputs. A separate SQL read repository shares the tenant,
requester and current-access predicate between list/count/detail. One statement
returns access flags, scoped total and page, so empty pages retain the total and
concurrent inserts cannot split a response's count/item snapshot.

The service enforces active actor → active membership → active Organization →
Ticket visibility. Customers see only requested-by-self Tickets; staff remains
Organization-scoped. Hidden, foreign and missing details share a safe 404. No
migration, mutation API or frontend integration was introduced.

### Verification results

| Check | Final local result, 26 October |
| --- | --- |
| Backend non-integration | 583 passed; 181 database/schema cases deselected |
| PostgreSQL data integration | 178 passed, including 21 new Ticket-read cases |
| Ruff lint / format (src, tests, migrations) | Passed |
| Schema/migration tests | Not rerun; no schema change; last evidence is 3 passed on 5 October |
| Frontend | Unchanged; earlier today's 141 tests / build / lint evidence applies |

New unit/API cases total 77. Real PostgreSQL checks cover customer/staff isolation,
foreign/missing/hidden IDs, inactive states, different roles between Organizations,
access changes after authentication, all lifecycle states, literal search and AND
filters, deterministic pagination and an independent-connection concurrent insert.
Snapshots of business tables verify reads make no writes.

Only verified local `opsdesk_product_test` with `opsdesk_product_test_runner` was
used; schema head was checked as `31be9023cfb2` before guarded cleanup. No hosted
or development database was tested destructively. Local libc collation is
`en_US.UTF-8`: I/i and dotted İ/i matched ILIKE; dotless ı/I did not. Hosted
collation verification remains a release/integration check.

### Railway usage and boundary

Chrome's authenticated Usage panel showed **$0.54 current usage**, **$4.46 remaining
credit**, **22 days remaining**, and a **$0.00 current bill**. The project detail
was $0.5411 and both services were online. These are a point-in-time reading, not
a forecast. No plan, service settings, source branch or deployment was changed.
The live source remains the last verified Week 15 checkpoint; no new runtime
smoke or new deployed-commit claim is made by this usage check.

### Close and next checkpoint

Monday's six tasks are complete locally. Changes are on
`feature/week-16-ticket-read-contract` in both repositories and have not been
committed or pushed by this implementation task. The product README, API/access
contract, F11 evidence and project status agree with this report. No extra daily
work document was created.

Next: review/publish the read slice and verify CI, check hosted collation during
release, then runtime response validation, authenticated Organization selection,
protected routes and real Ticket list/detail loading with stale-response tests.
The UI remains explicitly mock-backed. Comments, priority mutation, the complete
UI package and Month 04 handoff still follow the intensive Week 16 plan; this
backend checkpoint does not close the whole monthly MVP or operational backlog.

Documentation close: 114 Markdown files and 565 local link/image targets/anchors
checked; both repository whitespace checks passed.


## 26 October — publication checkpoint

The implementation checkpoint above predates publication. OpsDesk source commit
`a28cff2b83ef8d87a2f8fa608f51875e03bd5833` was pushed on
`feature/week-16-ticket-read-contract` and normally merged through
[PR #46](https://github.com/ozdemirr1/opsdesk/pull/46) as
`fff4e472e19fa64914c7c44d77f2f13428e80f02`. No squash or history rewrite was used.

Both source-head PR workflows passed:
[Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40361480752) and
[Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40361480901).
Merge-commit workflows also passed at `fff4e47`:
[Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40362096944) and
[Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40362096654).
PostgreSQL's 178 passing cases are local evidence, not part of these CI workflows.
The GitHub F11 issue was not automatically closed by this publication.

Railway metadata was rechecked on 26 October: successful application deployment
`e7aa38ac-cb26-46f1-937a-e044241a8405` still references
`255f9374a6506e1e50dfec0181f39c0b93fec2f4` on
`feature/week-15-railway-preview`. The database deployment is also successful.
This task made no source-branch setting or deployment change. Release smoke,
hosted collation and real frontend integration remain separate planned gates.

This bootcamp publication preserves the existing Week 16 report and plan rather
than creating a separate daily file. Monday's implementation, tests, usage check
and Git publication are complete; Month 04 remains in progress.


## 27 October — Tuesday tasks 1–3

Tuesday tasks 1–3 are complete locally: backend read coverage review,
Organization/session flow design, and validated Organization/Ticket HTTP adapters.
The dashboard still uses labelled mocks; protected routes, Organization screens
and real Ticket loading remain the next increment. No deployment was performed.

Fresh checks: 77 focused backend query/service/API tests passed; 209 frontend
tests across 11 files passed with one worker, plus build and lint. The 178
PostgreSQL integration results are from 26 October, not a new run. The API layer
has 68 new cases for malformed data, scope, pagination, query encoding, errors
and cancellation. No new dependency, migration or browser token storage was added.

### Coverage review and implementation

Reviewed the backend input/service/API tests and PostgreSQL read tests against
the access/search/pagination contract. Existing coverage includes customer/staff
scope, foreign/hidden records, inactive identities/memberships/Organizations,
revocation after authentication, literal Unicode/punctuation search, combined
filters, tied ordering, beyond-end pages and concurrent count/item snapshots.
No blocking gap was identified for preparing the frontend API layer. Hosted
collation verification and full UI/session integration remain separate gates.

In OpsDesk, `resources.ts` shares checked collection and transport results;
`organizations.ts` handles list/detail/create and Organization membership context;
`tickets.ts` now adds list/detail HTTP adapters and runtime guards while retaining
the pure display mapper. `resource-boundaries.test.ts` exercises the real request
helper through a mocked fetch boundary. IDs must be safe JavaScript integers;
invalid scope/pagination/role/enum/timestamp data never becomes typed success.

The existing [search/filter note](../notes/react/ticket-search-filter.md#organization-and-session-flow--27-october-2026)
records state transitions, role source, cancellation/request ownership, 401/403/404
behavior and uncertain creation outcomes. It is a design for the next controller,
not a claim that Organization screens or protected routes now exist.

The first frontend run had one failed test because its expected path omitted the
configured `/api` prefix. The assertion was corrected to use API_BASE_URL; the
final full run passed. No backend runtime source changed. No destructive database
test, new browser verification or Railway usage inspection was performed today.
Changes remain local on `feature/week-16-api-boundaries` in both repositories;
no commit/push, current-head CI or new deployed-source evidence is claimed.


## 27 October — Tuesday tasks 4–6

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

### Final verification — 27 October

- Frontend: **231 tests across 12 files passed**, including 22 new UI behavior
  cases and the earlier 68 API-boundary cases. Build and lint passed.
- New cases cover direct detail login/return/reload, unsafe routes, membership
  selection and later-page lookup, empty/create/uncertain-create flows, suspended
  and foreign Organizations, paging/filter reset, stale search and cross-scope
  responses, logout/history guards, HTTP 401/403/404/500, malformed responses and
  inactive-session cleanup. Tests run through App and the real resource adapters
  with synthetic fetch responses; they are not live-database browser tests.
- In-app browser smoke: opening and reloading a private detail hash address while
  signed out showed Login without private data. Chrome automation was unavailable;
  the available in-app browser was used. Authenticated PostgreSQL browser smoke
  and hosted release/collation checks remain pending.
- Backend runtime did not change. Earlier today's focused 77-test result applies;
  the complete backend and PostgreSQL suites retain their 26 October dates.
- No dependencies, migrations, browser token storage or new daily document added.
  No deployment, commit or push performed; both repositories retain the local
  `feature/week-16-api-boundaries` work for review/publication.

### Next gate

Publish after review and current-head CI, then verify the complete flow against
the actual backend/database and the intended deployed source. Newly created
Organizations may legitimately have zero Tickets; this slice does not add a
Ticket creation form. Comments, role-aware mutations, the full Tailwind/UI pass
and Month 04 handoff remain planned work, not completed by this checkpoint.


### 27 October navigation refinement

Workspaces navigation now appears only with a verified session. Normal login
opens the Organization directory; direct protected Ticket addresses retain their
internal destination after login. Sign-out removes the button again. Existing
server authorization and private route guards remain unchanged.

Two additional behavior cases cover normal/failed-login visibility and redirect.
Session-check tests explicitly return to Login after asserting the new directory
landing. The first full run exposed a timing-sensitive 403 assertion holding a
transient alert; it now waits for the final access-denied view. Final verification:
233 frontend tests / 12 files, build and lint passed. In-app browser inspection
confirmed the signed-out navigation contains Tickets, Login and Register only.
No new deployment, commit or push was made.

## 28 October — Wednesday tasks 1–3: real-flow review

### Publication and hosted boundary

Yesterday's pushes are present on `feature/week-16-api-boundaries`: OpsDesk
`0b28946` and bootcamp `20e26d2`. Neither branch has a PR at this check.
[Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40679546209) and
[Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40679546235)
succeeded at exactly `0b28946`; these runs do not cover today's uncommitted changes.
No bootcamp workflow run was returned. No merge, push or deployment was performed
during this review.

The hosted preview still exposes the older public mock dashboard and has no
Workspaces navigation after login. A synthetic account was created through the
hosted API, then browser login, session check and sign-out succeeded. Readiness
returned 200, anonymous Organization access and a wrong password returned 401.
This proves the deployed identity flow, not deployment of the new private UI.
The exact currently deployed SHA was not independently retrieved today.

### Actual local PostgreSQL walkthrough

The local API used `opsdesk_product_dev` with the application role; the frontend
used its `/api` proxy. Two new synthetic local users, three Organizations and 22
Tickets were created through APIs/UI; no existing records were deleted and no
destructive test suite targeted development or the hosted demo. One Organization
was created in the browser. Credentials were temporary and outside Git; no real
customer data was used. Account registration was checked through the API, not
claimed as a completed browser registration walkthrough.

- Browser: login, create/select Organization, real table/detail, 20+1 pagination,
  literal `100%_search` plus open-status filter, no-match and clear filters,
  Organization switch to an empty workspace, detail reload/login return and logout.
- API: anonymous list/detail 401, another user's Organization list/detail 403,
  foreign Ticket ID under an owned Organization 404, invalid limit 422,
  non-overlapping page results, literal wildcard search and empty/status results.
- Role/grant changes, inactive Organizations and out-of-order responses remain
  automated test evidence; they were not simulated by changing live accounts.

### Corrections and verification

The root now shows Login when signed out and Workspaces when signed in. Fixture
Tickets remain isolated learning/test components and are no longer mounted by App.
Authenticated navigation uses Workspaces/Account; Login/Register are anonymous
controls. Private deep links retain their login return destination. Registration
success offers Continue to login; password-length guidance and the tab-only session
rule are visible. Backend authorization and in-memory token handling are unchanged.

Frontend: **234 tests / 12 files passed**, build and lint passed. Obsolete public
fixture App scenarios were replaced by entry/registration/navigation cases and
real-dashboard reset checks for logout, 401 and inactive profiles; fixture component
tests remain. The first build caught an unsupported test-selector option; it was
removed and build passed. The backend suites were not rerun wholesale for this
frontend-only change; the real API smoke above is separate evidence.

Remaining gates: publish the reviewed changes, verify CI at the new commit, then
merge/deploy the intended source and repeat hosted Workspaces/Ticket checks.
A new workspace still has no Ticket creation form in this slice. Comments,
role-aware mutations and the full Month 04 UI package remain planned. Today's
requested first three tasks do not mark the whole Wednesday plan complete.


## 28 October — Wednesday close: Comment persistence foundation

Wednesday's scheduled implementation is complete locally: the real-data walkthrough
above and the Comment schema/model/scoped repository. This is not completion of
F14 or the full Month 04 MVP. No Comment HTTP endpoint or form is wired yet.

- Revision `84c2f9a17d60` follows `31be9023cfb2`, adding Comment identity, content,
  creation time and composite Organization/Ticket/author-membership foreign keys.
  The storage CHECK bounds content to 1..10000 code points. Parent deletion is
  restricted; deactivating an author preserves historical attribution.
- The scoped reader reuses Ticket visibility: active User/membership/Organization,
  customer-owned Tickets or staff visibility. Access, parent visibility, total and
  ordered page come from one SQL statement. A hidden parent is distinguished from
  a visible Ticket with no comments; ordering is `created_at, comment_id` ascending.
- The insert primitive flushes without committing. Its future service must derive
  the author, normalize/validate content, acquire cooperating locks, recheck access
  and reject posting to closed Tickets. Database tenant FKs do not implement those
  application rules. No edit/delete repository operation was added.
- Guarded cleanup now deletes Comments before Tickets and checks the new head.
  Predecessor upgrade/downgrade cycles preserve existing identity/Ticket rows and
  restore the head even after an injected test failure. Alembic metadata check
  reports no drift. Destructive verification used only `opsdesk_product_test`.

Fresh 28 October results: **589 backend non-integration tests passed** (209 database
cases deselected); **204 PostgreSQL data tests and 5 schema tests passed** in one
209-case run. Ruff lint and format passed. The frontend result remains **234 tests
across 12 files**, with build and lint passed. These are separate test groups.

Only the test database was migrated to `84c2f9a17d60`. The development database
used for the browser walkthrough remains at `31be9023cfb2`; no hosted migration,
deployment, commit or push was performed. Yesterday's CI covers `0b28946`, not
these uncommitted changes. No new dependency or daily report file was introduced.

Thursday 29 October: finish Comment service/API authorization, content rules,
posting/closing contention and rollback tests, then CommentForm/list integration
and the scheduled priority boundary. Publication needs review and new-commit CI;
hosted private-workspace verification and Month 04 learning/handoff gates remain.


## 29 October — release verification closing the 28 October work

The interruption left hosted smoke and publication records unfinished, not another
implementation task. This check was completed on 29 October (Europe/Istanbul).
The interrupted registration result was not recovered; a new synthetic account
was registered through the browser and its success message was verified.

- Product [PR #47](https://github.com/ozdemirr1/opsdesk/pull/47) merged normally as
  `2013248`; bootcamp [PR #11](https://github.com/ozdemirr1/ai-backend-bootcamp/pull/11)
  merged as `e94c0a9`. Daily commits were preserved.
- Product merge-commit [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40728800136)
  and [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/40728800380)
  passed. PostgreSQL results remain the separate local 28 October runs; this
  closure does not claim a fresh destructive database test run.
- Railway now follows `main`, replacing `feature/week-15-railway-preview`.
  Deployment `524bd101-54ed-4c3c-a1b3-41c59c8f8dcf` succeeded for `2013248`.
  Its guarded hosted pre-deploy migration upgraded `31be9023cfb2` to
  `84c2f9a17d60`. The development database was not migrated during this closure.
- Hosted browser: anonymous root shows Login without fixture Tickets; register,
  Continue to login, login, empty directory, workspace creation/selection, real
  Ticket table/detail, combined literal `100%_search`/open filter, session check,
  private-detail reload, login return and sign-out passed.
- Hosted API: live/ready returned 200; scoped reads and two non-overlapping
  one-item pages passed; anonymous Organization/list/detail and wrong-password
  login returned 401. Cross-tenant and inactive-state cases retain their prior
  local/automated evidence; they were not repeated against other hosted accounts.
- One synthetic user and one workspace were created in this completion check.
  Two synthetic Tickets were created through the API because the UI does not yet
  offer Ticket creation. No existing records were deleted. The browser was signed
  out and temporary credential material was removed after verification.

The 28 October release-verification gate is closed. Comment service/API/form,
posting-state checks and cooperating locks, priority actions, Ticket creation UI,
and the remaining Month 04 UI/learning gates remain open. Earlier dated pending
statements in this report describe their original checkpoint, not current release
status. No new daily report was added.


## 29 October — Comment service and API, tasks 1–3

Implemented locally: POST and GET
`/organizations/{organization_id}/tickets/{ticket_id}/comments`.
The authenticated User supplies the actor; the service derives the author from
current active Organization membership. Customers can comment on their own
requested Tickets; agent/admin/owner can comment on visible same-Organization
Tickets. Closed Tickets reject posting with `409 state_conflict` but remain
readable. Hidden Tickets return 404 and foreign Organizations return 403.

Content is a strict string: normalize CRLF/CR to LF, reject C0 controls other than
LF/TAB before trimming, trim boundaries and accept 1–10,000 Unicode code points.
Internal whitespace and Unicode remain intact; extra body fields are rejected.
GET validates limit/offset, rejects unknown/duplicate query keys and returns a
chronological page with its authorized total. Public Comment fields are limited
to ID, author membership ID, content and creation time.

Writes reuse the ordered Organization → User → membership locks, then lock and
refresh the scoped Ticket. Commit precedes the response; failures roll back.
PostgreSQL tests observe actual blocking through `pg_blocking_pids` on independent
connections. Closure-first rejects the waiting comment; comment-first preserves
the comment after closure. Closure is a cooperating test transaction, **not a new
status endpoint**. A timeout returns the safe busy error, rolls back, and does not
block an independent Organization from progressing.

Fresh checks: **702 backend non-integration tests passed** (242 database/schema
cases deselected), **237 PostgreSQL data integration tests passed** exclusively
on guarded `opsdesk_product_test`; Ruff lint/format and diff whitespace checks
passed. This adds 113 non-integration and 33 data integration cases. No migration
changed; the 5 schema tests retain their 28 October result. Frontend remains
unchanged; its 234-test/build/lint result also retains its 28 October date.

This increment is local and uncommitted; no push, PR or deployment was performed.
The live preview remains the previously verified release. CommentForm/list,
priority actions and the remaining Month 04 UI tasks are still pending. Only the
requested first three Thursday tasks are complete; the entire day/week is not
marked complete. No separate daily report was created.


## 30 October — completion of Thursday 29 October tasks 4–6

The first three Thursday tasks were committed/pushed by the learner as product
`7a3bb04` and bootcamp `98f4cda` on `feature/week-16-comment-api`; local tracking
branches agree. This checkpoint adds local uncommitted work to that same branch,
not a claim of merge, current-head CI or a new Railway release.

1. **Comment list/form:** the protected real Ticket detail now reads and posts
   persisted comments through validated adapters. The list has chronological
   pagination, empty/loading/error states and plain-text multiline rendering.
   Closed Tickets have readable history without a form. Sending locks out duplicate
   submissions; success clears the draft and refreshes the list. Validation/conflict
   failures retain the draft; ambiguous writes are never automatically retried and
   explicitly tell the user to check history before sending again. Session,
   Organization or Ticket changes discard drafts/history and ignore late results.
   401 expires the session, 403 clears workspace access, and a missing Comment
   route offers manual Ticket refresh rather than an automatic reload loop.
2. **Priority backend subset:** PUT
   `/organizations/{organization_id}/tickets/{ticket_id}/priority` accepts only a
   valid priority. Fresh active actor/membership/Organization, scoped visibility,
   staff role and open/in_progress state are checked under ordered locks before
   mutation or no-op. Customer attempts are denied; resolved/closed changes fail.
   A real change updates priority and `updated_at` in one SQL statement; an
   authorized repeat leaves all fields unchanged. Failure rolls back. PostgreSQL
   tests verify waiting requests observe a cooperating closure, role demotion or
   membership deactivation before deciding. Assignment/status endpoints remain
   outside this subset; issue #20 is not claimed complete.
3. **Verification and record:** 740 backend non-integration tests passed (286
   database/schema cases deselected); 281 PostgreSQL data integration tests passed
   exclusively on guarded `opsdesk_product_test`; 278 frontend tests across 14 files
   passed. Frontend build/lint, backend Ruff lint/format and diff checks passed.
   No schema changed; the 5 schema cases retain their 28 October evidence.
   Frontend checks used real adapters with synthetic HTTP responses; backend
   integration used real PostgreSQL. No new authenticated browser or hosted smoke
   is claimed for this increment.

Thursday's requested implementation is complete locally. The next Friday package
still includes the role-aware priority UI, Tailwind primitives and responsive
shell/sidebar. Ticket creation UI and remaining Month 04 gates also stay open.
No publish, paid service change, new migration or separate daily report was made.


## 30 October — Friday tasks 1–3: priority control

- GitHub review: product `acb5a57` has successful [Backend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/41082922607)
  and [Frontend CI](https://github.com/ozdemirr1/opsdesk/actions/runs/41082922744).
  Neither repository has a PR for `feature/week-16-comment-api`; the bootcamp
  branch has no workflow runs. Thursday's continuation is pushed as product
  `acb5a57` and bootcamp `25f3a23`.
- Real Ticket detail now exposes the priority form only to agent/admin/owner,
  using API membership context. Resolved/closed Tickets cannot be changed;
  backend authorization remains authoritative. PUT responses are checked for
  matching organization, Ticket, priority, state and valid response structure.
- Pending submissions prevent duplicate sends. Successful responses update the
  detail without discarding a comment draft; an authorized no-op reports unchanged
  priority. Unauthorized/missing resources clear private content. Uncertain writes
  and state conflicts require an explicit refresh before another attempt.
- Ticket, organization and session changes abort pending writes and ignore late
  responses. Tests cover role/state visibility, successful/no-op writes, error
  handling, malformed responses, duplicate prevention and scope cleanup.
- Fresh frontend verification: **309 tests across 15 files**, build and lint pass.
  Tests use the real App/adapters with synthetic HTTP responses. Earlier 30 October
  backend evidence remains 740 non-integration and 281 PostgreSQL data tests; no
  backend/schema change or rerun was needed. Schema evidence remains 5 tests from
  28 October. No new manual browser or hosted smoke is claimed.

These Friday changes are local and uncommitted; the successful CI above applies
only to `acb5a57`. Review/publication, Tailwind/responsive shell, Ticket creation UI
and the remaining Month 04 acceptance gates are still pending.


## 31 October — completion of Friday 30 October tasks 4–6

- Added Tailwind CSS 4.3.3 and its Vite plugin using the
  [official Vite integration](https://tailwindcss.com/docs/installation/using-vite).
  Shared theme tokens cover colors, typography and radii; base styles unify
  buttons, fields, focus and disabled/error states. Semantic component styles
  remain in App.css. Explicit source scanning and static tokens keep utilities
  and CSS variable consumers consistent.
- AppShell separates public login/register presentation from authenticated
  navigation. Desktop uses a sidebar; narrow screens use a compact top navigation.
  The same controls remain available without a modal or hidden navigation state.
  No session persistence, role rules or API contracts changed.
- Workspace cards, Ticket filters/table/detail, priority controls and comments
  share spacing and surfaces. Tables scroll within their labelled region;
  long descriptions wrap. Keyboard users can skip to main content without
  changing the hash route. Reduced-motion preferences are respected.
- Verification: **311 frontend tests across 16 files passed on 30 October**,
  including two new shell accessibility/session-cleanup tests; build and lint
  passed. After the interrupted work resumed on 31 October, the final theme
  adjustment passed build/lint again. Both repositories pass diff checks.
- Browser checks covered login/register, workspace selection, Ticket table and
  detail at desktop and narrow layouts. Observed narrow viewport widths included
  355 and 433 CSS pixels; page scroll width matched viewport width while the
  table retained its own horizontal scroll. Authenticated visual checks used
  the real components in an isolated temporary harness with synthetic responses,
  not the production API. The harness was stopped; no hosted smoke or deployment
  is claimed. Existing behavior tests cover permissions and request cancellation.
- Installation initially failed certificate validation; using the system CA
  bundle resolved it without disabling TLS verification. npm audit reports four
  existing development-dependency findings (two moderate, two high): Vitest /
  @vitest/mocker, undici and zod. Their versions are unchanged from HEAD;
  dependency remediation remains a separate follow-up, not a clean-audit claim.

Friday's six requested implementation tasks are complete locally. All Friday
changes remain uncommitted; CI evidence above still belongs to `acb5a57`.
Ticket creation modal, toast, fuller empty states/accessibility, final integrated
release checks and publication remain Month 04 work. No new daily report was made.


## 31 October — Saturday tasks 1–3: Ticket creation UI

- Added New ticket to the authenticated workspace list, including an empty
  workspace. All active member roles can create; backend membership/organization
  checks remain authoritative. The native dialog focuses the title on opening,
  makes the background inert and restores the opener on cancellation. Escape and
  explicit close work while idle; closing is disabled during the bounded request.
- The adapter sends only normalized title, description and priority to the
  existing POST endpoint. Requester/creator remain server-derived. Client limits
  match backend code-point limits; responses require 201 and matching workspace,
  submitted content and creation invariants. There is no backend/schema change.
- A request guard prevents duplicate submits. 422 keeps the draft editable;
  401 expires the session and 403/404 discard workspace access. Network, malformed
  and server failures, including a 30-second client timeout, explain that creation
  is uncertain and offer an unfiltered list check rather than automatic retry.
  Route/organization/session changes abort requests and discard late results;
  cancellation does not imply a server write was rolled back.
- Confirmed creation navigates to the returned Ticket ID and fetches its canonical
  detail. A dismissible live-region success notice stays until dismissal or
  navigation; Back/Forward cannot revive it. Returning to the list fetches again.
- Verification: **347 frontend tests across 17 files**, production build and lint
  pass. The previous backend evidence is unchanged (740 non-integration and 281
  PostgreSQL data tests on 30 October; 5 schema tests on 28 October).
- Browser checks used actual components/adapters with synthetic HTTP responses in
  an isolated local harness: initial focus, native modal background exclusion,
  keyboard navigation, Escape/focus return, creation/detail/notice dismissal and
  updated list. Desktop and 355-CSS-pixel narrow layout showed no horizontal
  overflow. This is not an end-to-end PostgreSQL or hosted smoke result.

Friday's design/priority changes are now committed as product `19dfaff`, matching
its local origin tracking ref. Today's creation work remains uncommitted.
No new CI, PR, merge or deployment is claimed. Railway is deliberately left for
an evening check by the learner; the supplied screenshot shows a queued build.
Saturday's broader empty-state/accessibility review and final integrated release
checks remain open. This increment closes only the requested first three tasks.


## 1 November — completion of Saturday 31 October tasks 4–6

- Empty states now distinguish an empty workspace, no matching Tickets and a
  page emptied by changing results. Recovery actions open Ticket creation,
  reset search/status or return to the first page while preserving filters.
  Empty Organization and Comment states guide focus to their existing forms;
  closed Tickets do not invite new comments. Empty later Organization/Comment
  pages also offer a return to page one.
- Shared loading surfaces announce progress with a polite status region and
  use a static indicator. Read failures remain alerts with bounded recovery
  choices, never successful-empty states. Existing response/session guards stay
  authoritative. Pagination controls now have navigation landmarks.
- The Ticket modal announces validation failures, focuses the first invalid
  field, and contains overscroll. Native Escape restores its actual opener when
  idle; pending writes cannot be hidden by Escape. Resetting filters restores
  focus to search. Existing focus styles, labelled controls and text-based status
  badges are retained; this is a bounded accessibility review, not a WCAG audit.
- Verification on **1 November**: **356 frontend tests across 17 files**, production
  build and lint pass. Nine additional tests cover recovery/focus behavior,
  loading/error separation, closed empty comments and a combined authenticated
  create → detail → comment → priority update → logout flow using real frontend
  adapters with synthetic HTTP responses. Backend/schema were not changed or
  rerun; historical backend evidence retains its original dates.
- Browser review used the same application in an isolated synthetic-response
  harness. Empty-state layouts at **1280, 700 and 320 CSS pixels** had page scroll
  widths equal to their viewport widths. At 320px, the modal's client/scroll
  widths both measured 280px; longer validation content scrolls vertically.
  Keyboard Enter, invalid-field focus, Escape/opener return, failed-read Retry
  and filter-reset focus were checked. The temporary server/tab were closed.

Saturday's six implementation/UI-check tasks are complete locally. This does not
close Sunday's full PostgreSQL/persistence, cross-identity, exact-head CI,
publication, hosted smoke, operational recovery or Month 04 retrospective gates.
Creation and this continuation remain uncommitted. No commit, push, merge or
Railway action was performed; the manual deployment instructions remain a release
step after the intended source is published. No new daily file was introduced.


## 2 November — live flow and authorization acceptance

Scope: the two requested Week 16 checks, not the full Month 04 closure.
Runtime source `8a633d0` was merged in OpsDesk PR #49 and deployed successfully
as Railway deployment `3215ab49-07c6-4b91-9372-59c14d63f47e` on 1 November.
The release-head CI passed 740 backend non-integration and 356 frontend tests;
these are separate from the focused checks below.

### Hosted browser evidence

Using the synthetic account registered on 1 November, the browser completed
login, Organization creation, Ticket creation, canonical detail navigation,
priority change to high, Comment posting, sign-out and sign-in back to the
protected detail. Ticket #3 in Organization #2 retained its title, description,
high priority and one Comment after signing in again. Browser Back after logout
showed Login without private content. Reloading the detail also required login.
No real customer/support data was entered and no hosted data was deleted.

The first Comment GET returned 500. Read-only inspection confirmed that
`opsdesk_app` had neither SELECT nor INSERT on `public.comments`. Using the
existing guarded hosted migration connection, after checking database, role and
revision `84c2f9a17d60`, granted only SELECT/INSERT on that table and USAGE on
`public.comments_comment_id_seq`. No role membership, ownership, UPDATE/DELETE,
schema-wide privileges or application-code change was added. Retry then loaded
the empty list; posting and re-reading the Comment succeeded. A healthy readiness
endpoint alone had not detected this missing table permission.

### Isolated authorization and session evidence

- Fresh real-PostgreSQL run on guarded `opsdesk_product_test`:
  `tests/integration/test_ticket_reads.py`, `test_comment_api.py` and
  `test_ticket_priority.py`: **98 passed**. Coverage includes customer/staff
  scope, hidden/foreign resources, closed-Ticket comments, current-role/state
  rechecks, rollback and cooperating-operation contention.
- Fresh frontend run of `src/WorkspaceFlow.test.tsx` and
  `src/components/Comments.test.tsx`: **88 passed**. Synthetic-response tests
  verify invalid-session cleanup, role visibility, logout/history protection,
  filter/draft reset and ignored late responses. This is not a new full-suite run.
- Separate real local browser/API walkthrough used Alpha and Beta Organizations
  with two synthetic identities: one customer in Alpha/owner in Beta, one staff
  owner in Alpha without Beta membership. Customer saw only its one Alpha Ticket
  and no priority control; staff saw both Alpha Tickets. Switching to Beta showed
  only its Ticket and owner controls, with the Alpha comment draft cleared.
- Direct FastAPI-to-PostgreSQL checks on these fixtures returned 404 for a hidden
  Ticket, 403 for a foreign Organization, 403 for customer priority modification,
  and 401 for missing/invalid tokens. The rejected priority write left the full
  Ticket response unchanged. Other staff roles are covered by the automated matrix;
  no hosted customer membership was fabricated.

Both requested checks are complete with the environment boundaries above.
The temporary local server is stopped. Full backup/restore and rollback evidence,
broader operational review, README/release publication cleanup and the Month 04
retrospective/learner handoff remain separate work. No new daily report was created.

## 2 November — recovery, release records and Month 04 review

Completed the three requested remaining blocks within their documented boundaries:

- Matched runtime `8a633d0`, SUCCESS deployment `3215ab49-07c6-4b91-9372-59c14d63f47e`
  and source/test/hosted revision `84c2f9a17d60`. Migration-role read confirmed the
  revision and runtime Comment SELECT/INSERT/sequence-USAGE grants. Runtime need
  not read `alembic_version`; that inspection was moved to the migration role.
- Isolated recovery on the exact guarded `opsdesk_product_test` preserved 2 Users,
  2 Organizations, 3 Memberships, 3 Tickets, 1 Comment and all sequence values.
  PostgreSQL 18.6 custom dump/transactional restore succeeded. The initial default
  pg_dump 14.19 attempt stopped on version mismatch before any restore.
- Previous app source `b7800e4` read its synthetic Ticket on the restored expanded
  schema (200); data/sequence digest remained unchanged. This is bounded read
  compatibility, not all old write paths or a live rollback.
- After test-fixture cleanup, `.venv/bin/python -m pytest -q tests/schema` with
  schema opt-in: **5 passed**. `alembic check`: no new operations. Separate
  `pytest -q tests/integration` with integration opt-in: **281 passed** (23.76 s).
  Both use guarded test environment settings. Final head `84c2f9a17d60`, business
  tables empty. No destructive test/restore ran on dev or hosted demo.
- Product/frontend READMEs now describe deployed creation/comments/priority and
  show the real 2 November persisted Ticket screenshot. Earlier dated checkpoints
  remain historical; current summaries supersede their pending-release wording.
- Added [Month 04 review](../monthly-reports/month-04.md), original-target evidence,
  variance/carry-over, two learner-supplied explanations and Month 05 handoff.
  The personal difficulty/repeat-target answer was not supplied and is not invented.

The product [recovery record](https://github.com/ozdemirr1/opsdesk/blob/main/docs/release-recovery.md)
contains reproduction preconditions and command options. The dump is temporary,
private and outside Git, not an established hosted backup/retention system.

Fresh npm review found 16 development-tool findings (14 moderate, 2 high), versus
zero with `--omit=dev`; TLS remained enabled using the system CA. Toolchain
maintenance remains separate, with no forced dependency change. Provider audit,
bounded abuse controls, hosted-export restore evidence and current usage review
remain operational follow-ups. The latest supplied credit snapshot was 1 November
($4.08 / 16 days), not a fresh cost check. Do not expand the demo invitation based
only on these technical results. No broad production-readiness claim is made.

Actual study hours were not recorded. Docker/Compose, then Redis and one bounded
background job remain Month 05; AI remains Month 06. Use the monthly handoff in a
new project-scoped Month 05 conversation after reconciling the open gates.
