# SQL Queries, Indexes, and Transactions

## Goal

This note records the Week 06 query-planning and transaction exercises. The
examples use the OpsDesk learning schema directly so that later ORM behavior
can be connected to observable PostgreSQL behavior.

## Query Shape Before Index Design

An index should support a real access pattern rather than being added to every
column. The future Ticket-listing query filters by status, orders by identifier,
and applies a limit:

```sql
SELECT
    ticket_id,
    title,
    priority,
    status
FROM tickets
WHERE status = 'open'
ORDER BY ticket_id ASC
LIMIT 10;
```

The matching secondary index is:

```sql
CREATE INDEX tickets_status_ticket_id_idx
    ON tickets (status, ticket_id);
```

Column order is intentional. `status` supports the equality predicate, while
`ticket_id` preserves the requested order inside one status value. The primary
key already indexes `ticket_id`, but it does not directly organize rows by
status.

## Reading `EXPLAIN`

The baseline plan on the six-row seed dataset used this shape:

```text
Limit
  -> Sort by ticket_id
       -> Seq Scan on tickets
            Filter: status = 'open'
```

The sequential scan read six rows, kept three open Tickets, and removed three
rows through the filter. A separate quicksort ordered the matches.

After index creation, PostgreSQL naturally retained the sequential scan. Its
estimated cost was lower than the index-scan cost because scanning six rows is
cheaper than traversing an additional index structure. This is correct planner
behavior, not evidence that the index is invalid.

`ANALYZE tickets` refreshed table statistics. The large reduction in estimated
cost after `ANALYZE` came primarily from accurate row-count and width estimates,
not from treating the index as automatic acceleration.

Disabling sequential scans temporarily produced:

```text
Limit
  -> Index Scan using tickets_status_ticket_id_idx
       Index Cond: status = 'open'
```

The forced plan had no separate sort because the composite index satisfied both
the filter and ordering. `enable_seqscan = off` was used only as an educational
diagnostic and was immediately reset. It is not an application or production
setting.

Important plan fields include:

| Field | Meaning |
| --- | --- |
| `cost` | Planner estimate used to compare alternative plans; it is not elapsed time. |
| `actual time` | Measured timing from the executed plan node. |
| `rows` | Estimated and actual row counts at a node. |
| `Rows Removed by Filter` | Rows scanned but rejected by the predicate. |
| `Buffers: shared hit` | Pages found in PostgreSQL's shared buffer cache. |
| `Buffers: shared read` | Pages read into shared buffers. |
| `Planning Time` | Time spent constructing the execution plan. |
| `Execution Time` | Time spent executing the selected plan. |

Tiny, cached datasets are unsuitable for performance conclusions. Their plans
are still useful for learning operators, predicates, sort behavior, and index
eligibility.

## Transaction Boundaries

A transaction groups related statements into one atomic unit:

```sql
BEGIN;
-- related writes
COMMIT;
```

`COMMIT` makes every successful statement in the transaction durable and
visible to later transactions. `ROLLBACK` cancels every uncommitted write in
the transaction, including changes produced indirectly by cascade rules.

The cascade exercise deleted Ticket 5 inside a transaction. Before rollback:

```text
Ticket rows:          0
Comment rows:         0
Ticket-Tag rows:      0
Reusable email Tags:  1
```

This proved that deleting a Ticket cascades to its dependent Comment and
junction rows without deleting the reusable Tag. `ROLLBACK` restored the
complete `1 / 1 / 1 / 1` relationship state.

## Atomic Related Writes

The commit exercise created a Ticket and its first Comment through two separate
statements inside one transaction. Both rows used the same generated
`ticket_id`. `COMMIT` made the complete relationship visible afterward.

A foreign key prevents a Comment from referencing a missing Ticket, but it does
not require every new Ticket to receive an initial Comment. The transaction
protects that multi-step application workflow from a half-completed state.

A second committed transaction deleted the demonstration Ticket. The cascade
removed its Comment, and the final verification returned zero Ticket and zero
Comment rows for the demonstration data.

Identity sequences are not gapless row counts. Committing and later deleting a
generated row does not rewind the sequence, and a failed or rolled-back insert
may also consume a sequence value depending on when it was generated.

## Verification Requires a Known Starting State

Mutation scripts are stateful. Running the CRUD exercise twice does not prove
the same behavior twice: the first run resolves Ticket 2 and deletes Ticket 5,
so a second run updates an already resolved Ticket and reports `DELETE 0`.

The clean verification therefore restores `003_ticket_seed.sql` and
`004_relationship_seed.sql` before exercises that depend on particular rows.
In particular, the seed must be restored after `006_crud_queries.sql` and before
`007_transactions.sql`, because the transaction exercise expects closed Ticket
5 and its relationships to exist.

`TRUNCATE ... RESTART IDENTITY` makes the learning dataset deterministic again.
It restores Ticket identifiers 1 through 6 even after failed inserts and
rolled-back transactions have consumed sequence values.

## Transaction-Stable Timestamps

PostgreSQL evaluates `CURRENT_TIMESTAMP` at the start of the current
transaction. It remains stable until that transaction ends. If a seed insert
and a later update run inside the same transaction, `created_at` and
`updated_at` can therefore remain equal even though the update succeeded.

The reliable evidence for that exercise is the changed status and the
`UPDATE 1` command tag. `updated_at > created_at` is only expected when the
operations occur at different transaction times. A changing wall-clock value
can be obtained with `clock_timestamp()`, but the learning schema deliberately
keeps the conventional transaction timestamp behavior.

## Clean-Database Verification Result

The complete schema was recreated with four application-owned tables, sixteen
columns, fourteen named primary-key, foreign-key, unique, and check constraints,
and the expected deterministic seed counts:

```text
Tickets:             6
Comments:            6
Tags:                5
Ticket-Tag links:    6
```

Expected failures verified title normalization, allowed priority values,
foreign-key integrity, composite-key uniqueness, and normalized Tag-name
uniqueness. An intentional invalid priority in a multi-statement transaction
also confirmed that `ON_ERROR_STOP=1` prevents later statements and that the
single transaction rolls back the earlier valid insert.

## Script Execution Rules

`sql/007_transactions.sql` contains explicit `BEGIN`, `COMMIT`, and `ROLLBACK`
boundaries, so it must not be wrapped with `psql --single-transaction`.

`sql/008_indexes.sql` does not manage its own transaction. It is executed with
`--single-transaction` so an unexpected failure also rolls back index creation.

Both scripts use `ON_ERROR_STOP=1` so `psql` stops after an unexpected SQL
error instead of continuing through later verification statements.
