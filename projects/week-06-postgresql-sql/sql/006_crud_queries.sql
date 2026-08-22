-- List all tickets in identifier order.
SELECT
    ticket_id,
    title,
    priority,
    status
FROM tickets
ORDER BY ticket_id ASC;

-- List open tickets.
SELECT
    ticket_id,
    title,
    priority,
    status
FROM tickets
WHERE status = 'open'
ORDER BY ticket_id ASC;

-- List active high-priority tickets.
SELECT
    ticket_id,
    title,
    priority,
    status
FROM tickets
WHERE priority IN ('high', 'critical')
    AND status IN ('open', 'in_progress')
ORDER BY ticket_id ASC;

-- List the three highest ticket identifiers.
SELECT
    ticket_id,
    title,
    priority,
    status
FROM tickets
ORDER BY ticket_id DESC
LIMIT 3;

-- Demonstrate ungrouped AND and OR precedence.
SELECT
    ticket_id,
    title,
    priority,
    status
FROM tickets
WHERE priority = 'low'
    AND status = 'resolved'
    OR status = 'open'
ORDER BY ticket_id ASC;

-- List low-priority tickets that are resolved or open.
SELECT
    ticket_id,
    title,
    priority,
    status
FROM tickets
WHERE priority = 'low'
    AND (status = 'resolved' OR status = 'open')
ORDER BY ticket_id ASC;

-- Preview the ticket targeted for update.
SELECT
    ticket_id,
    title,
    priority,
    status,
    created_at,
    updated_at
FROM tickets
WHERE ticket_id = 2;

-- Resolve one ticket and update its modification timestamp.
UPDATE tickets
SET
    status = 'resolved',
    updated_at = CURRENT_TIMESTAMP
WHERE ticket_id = 2
RETURNING
    ticket_id,
    title,
    priority,
    status,
    created_at,
    updated_at;

-- Preview the closed ticket targeted for deletion.
SELECT
    ticket_id,
    title,
    priority,
    status,
    created_at,
    updated_at
FROM tickets
WHERE ticket_id = 5
    AND status = 'closed';

-- Delete the selected closed ticket.
DELETE FROM tickets
WHERE ticket_id = 5
    AND status = 'closed'
RETURNING
    ticket_id,
    title,
    priority,
    status;
