-- Inspect the query plan before adding the secondary index.
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    ticket_id,
    title,
    priority,
    status
FROM tickets
WHERE status = 'open'
ORDER BY ticket_id ASC
LIMIT 10;

-- Support status-filtered Ticket listing in identifier order.
CREATE INDEX tickets_status_ticket_id_idx
    ON tickets (status, ticket_id);

-- Refresh planner statistics after the schema change.
ANALYZE tickets;

-- Inspect the plan selected naturally for the small seed dataset.
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    ticket_id,
    title,
    priority,
    status
FROM tickets
WHERE status = 'open'
ORDER BY ticket_id ASC
LIMIT 10;

-- Demonstrate that the new index can satisfy the filter and ordering.
SET enable_seqscan = off;

EXPLAIN (ANALYZE, BUFFERS)
SELECT
    ticket_id,
    title,
    priority,
    status
FROM tickets
WHERE status = 'open'
ORDER BY ticket_id ASC
LIMIT 10;

RESET enable_seqscan;
