# Ticket search and status filtering

Prepared 21 October 2026 as optional Week 15 catch-up. Title search was subsequently
implemented and reviewed locally: 123 frontend tests, build and lint passed.
Status filtering and combined-condition behavior below were implemented locally
and pushed as OpsDesk commit `a031633` after review. The 129-test frontend suite,
build and lint passed; local browser checks covered zero matches and reset.
Chrome screenshots later confirmed case-insensitive matching, no-match feedback
and clearing to all mock rows. A later screenshot confirmed the revised field
layout. The title-search change was pushed as OpsDesk commit `3a5b11b`; public
deployment remains unverified.

## Reasoning and component boundaries

Keep the entered search text and selected status in state because the user changes
them. Derive visible tickets from the original collection and those two inputs on
each render. Storing another filtered array would create a second copy that must
be synchronized whenever an input changes. This small fixture collection needs
neither an effect nor memoization.

Use a `TicketDashboard` component receiving `tickets: TicketSummary[]`. It owns
the search/filter inputs and passes the derived array to the existing TicketTable.
App continues to own screen selection and the session; StatusBadge stays
presentational. Leaving Tickets may reset the inputs when the dashboard unmounts;
make that behavior explicit in a navigation test. Do not persist filters or tokens.

## Small analogous example

This book example demonstrates combining conditions without introducing React
state or writing the real Ticket component:

```ts
const books = [
  { title: 'HTTP Basics', available: true },
  { title: 'Database Basics', available: false },
];
const query = '  BASICS  ';
const onlyAvailable = true;
const normalizedQuery = query.trim().toLowerCase();
const visibleBooks = books.filter((book) =>
  book.title.toLowerCase().includes(normalizedQuery) &&
  (!onlyAvailable || book.available)
);
// Only HTTP Basics matches both conditions. The original books array is intact.
```

## First product exercise

Create `frontend/src/components/TicketDashboard.tsx` with a typed tickets prop.
Start with only a labelled `Search tickets` input and a query state initialized to
an empty string. Trim/lowercase the query for comparison without rewriting the
user's input. Render TicketTable with title matches. Keep the mock-data notice.

For the first review, searching `EMAIL` should show only #102; clearing the input
should restore all three rows. Add behavior tests through the labelled input and
table rows, rather than testing a duplicated filtering implementation.

## Next increment and acceptance cases

Add a labelled status select with All statuses, Open, In progress, Resolved and
Closed. The state type is `TicketStatus | 'all'`. Narrow the select's string value
with a checked mapping/type guard instead of asserting an arbitrary string is a
TicketStatus. Combine status and title conditions with AND.

| Case | Expected behavior |
| --- | --- |
| Empty query and All statuses | All supplied rows |
| `  EMAIL  ` and All statuses | #102 only |
| Empty query and Open | #101 only |
| `email` and In progress | #102 only |
| `email` and Open | No matching tickets |
| Closed with the current fixtures | No matching tickets |
| Clear filters | Empty query, All statuses, all rows restored |
| Original collection is empty | No tickets yet. |
| Leave Tickets and return | Inputs reset; session behavior unchanged |

Distinguish source data absence from zero filter matches in TicketDashboard.
TicketTable's existing empty message remains valid for a genuinely empty source;
show `No matching tickets.` when a nonempty collection has zero matches. The clear
action should be available in this state. Use labels, native inputs/selects/buttons
and a visible result count. Do not announce each status badge as a live region.

## Scope and checks

This filters only the explicitly labelled mock collection. It does not implement
backend search, pagination, tenant authorization or a real Ticket-list API. Do not
add dependencies, network calls, debounce, URL routing or a broad style redesign.
Keep later API integration and membership context as separate reviewed work.

After implementation, run frontend tests, build and lint. Manually check typing,
selecting status, clearing filters, keyboard operation and a narrow viewport.
Record actual results; this brief does not establish those checks as passed.


## Week 16 server-search boundary — 26 October 2026

The earlier sections describe the Week 15 mock exercise. The 25 October live
checkpoint verified that mock dashboard; this does not establish real-data search.
The new [Ticket read contract](https://github.com/ozdemirr1/opsdesk/blob/main/docs/api-contract.md)
defines the server query. The backend is now implemented and locally tested;
the frontend still uses mocks and has not been wired to these endpoints.

In the book analogy, filtering ten books already downloaded cannot tell us how
many matching books exist in a library of one thousand. The server must first
select books the member can see, then search, count and return a page.

OpsDesk will send `q` plus filters and pagination. Blank input omits `q`; an
All statuses selection omits `status` instead of sending `all`. Changing query,
filter or Organization resets offset; logout/Organization changes also discard
old data and invalidate in-flight responses. `total_count` comes from the server,
not `items.length`. Do not apply the mock filter again to a returned page.

Search targets titles only; wildcard characters are literal. Case behavior comes
from the database collation, not frontend `toLowerCase()`. Runtime validation of
the envelope/items precedes mapping. Authentication and Organization membership
are checked by the server on every read, regardless of hidden buttons.


## Organization and session flow — 27 October 2026

This is the design for the next UI increment. Organization/Ticket HTTP adapters
and their runtime guards are implemented; the screen controller and protected
routes are not implemented by this checkpoint. The public mock view stays separate.

A library analogy: a person can be a librarian at one library and a reader at
another. The selected library's membership determines the controls; a global user
role or a library ID typed in the URL cannot establish permission.

| Event | Required controller behavior |
| --- | --- |
| No verified session | Public mock view remains available; private routes require login and a validated internal return destination |
| Successful login | Keep token in memory; advance session generation, clear previous private state and load Organizations |
| Organization list | Separate loading, failed and genuinely empty results; paginate using server total; use the returned own_membership role, never a client-selected role |
| No memberships | Offer Organization creation; send name only; accept the 201 Organization/owner-membership pair supplied by the API |
| Select Organization | Use matching active membership context from the list/create response; GET Organization detail alone has no membership role; do not load Tickets for a suspended Organization |
| Change Organization | Abort prior reads, advance scope generation, clear private rows/detail/filters and reset offset before fetching the new scope |
| Change Ticket filters/search | Reset offset; serialize server query once and replace the list only for the newest request; do not filter the returned page again |
| Sign out / protected HTTP 401 / inactive current user | Invalidate pending requests and clear token, Organization, role, private rows/detail and filters; return to Login |
| HTTP 403 | Remove inaccessible Organization data, refresh membership context and show access feedback; do not treat every 403 as global logout |
| Detail HTTP 404 | Show an unavailable detail without disclosing another tenant; return to the authorized list |
| Network / 5xx / malformed response | Show a retryable error, preserve a still-valid session, and never replace failure with an empty-success result or display data from a previous scope |

Before applying a response, compare session generation, Organization ID and request
generation with the active controller state. Abort helps release work, but is not
by itself the complete UI race guard. The new HTTP helper rejects responses whose
signal was aborted; controller race tests remain part of UI integration.

Organization creation is not automatically retried. A cancelled/lost response
may follow a committed write; preserve input and explain uncertain completion
rather than promising rollback. Refresh the Organization list before retrying.
The backend remains authoritative for all access and role checks.

Runtime guards validate safe numeric IDs, exact roles/statuses/priorities,
Organization/membership pairing, calendar timestamps and collection counts.
Returned Ticket scope and pagination must match the request. Unsafe JavaScript
integers are rejected rather than rounded into a resource lookup; supporting the
full PostgreSQL bigint range would need a coordinated string-ID wire contract.
Search text is encoded once and is not lowercased or Unicode-normalized in the
HTTP layer. Empty string is omitted; other whitespace is preserved for the
backend's own normalization rule.

Verification: 209 frontend tests across 11 files, build and lint passed on
27 October; 68 new cases cover these API boundaries. The focused backend
query/service/API suite also passed all 77 cases. The unchanged PostgreSQL suite
retains its 26 October evidence (178 passed); hosted collation and end-to-end
Organization selection remain unverified here.


## Organization/session implementation checkpoint — 27 October 2026

The design above was implemented in the subsequent tasks 4–6. Organization and
Ticket screens now call the validated HTTP adapters. Hash routes keep reloads
compatible with the existing same-origin host without a new router dependency:
`#/organizations`, `#/organizations/{id}/tickets`, and
`#/organizations/{id}/tickets/{ticketId}`. Only recognized internal patterns are
accepted. The guard renders Login at the requested address and resumes the same
route after verified login; it does not accept a free-form return URL.

App's session epoch and Organization component key isolate private state. Each
resource loader identity represents the current query/scope; old results are
hidden immediately when that identity changes. Effect cleanup both aborts and
invalidates the request closure. This implements response ownership without
placing tokens or private results in browser storage.

Organization detail alone has no role, so direct addresses resolve membership
through the paginated Organization list until a match or the end. This is correct
for the current API; many memberships can add lookup latency. Future optimization
should use a reviewed context endpoint rather than trusting a client role. A new
Organization may have an empty Ticket list because the Ticket creation UI is a
separate feature. The public mock view remains explicitly labelled.

Final evidence: 231 frontend tests / 12 files, build and lint passed. Tests use
synthetic HTTP responses through real adapters; signed-out guard/reload behavior
was also checked in the in-app browser. No authenticated live-database browser
check or hosted deployment is established by this entry.
