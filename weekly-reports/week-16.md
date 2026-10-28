# Week 16 Report — Month 04 completion work

26 October–1 November 2026. In progress; the week and Month 04 are not complete.
Follow the [intensive plan](week-16-plan.md). This is the regular weekly report,
not a separate daily work document.

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
