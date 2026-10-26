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
