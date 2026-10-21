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
