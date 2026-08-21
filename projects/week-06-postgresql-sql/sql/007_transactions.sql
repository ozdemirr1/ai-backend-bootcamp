BEGIN;

-- Inspect the relationship state before deleting the Ticket.
SELECT
    (SELECT COUNT(*)
     FROM tickets
     WHERE ticket_id = 5) AS ticket_count,
    (SELECT COUNT(*)
     FROM comments
     WHERE ticket_id = 5) AS comment_count,
    (SELECT COUNT(*)
     FROM ticket_tags
     WHERE ticket_id = 5) AS tag_assignment_count,
    (SELECT COUNT(*)
     FROM tags
     WHERE name = 'email') AS reusable_tag_count;

-- Delete the parent Ticket inside the transaction.
DELETE FROM tickets
WHERE ticket_id = 5
RETURNING
    ticket_id,
    title,
    status;

-- Verify the cascade before rolling back.
SELECT
    (SELECT COUNT(*)
     FROM tickets
     WHERE ticket_id = 5) AS ticket_count,
    (SELECT COUNT(*)
     FROM comments
     WHERE ticket_id = 5) AS comment_count,
    (SELECT COUNT(*)
     FROM ticket_tags
     WHERE ticket_id = 5) AS tag_assignment_count,
    (SELECT COUNT(*)
     FROM tags
     WHERE name = 'email') AS reusable_tag_count;

ROLLBACK;

-- Verify that the rollback restored the complete relationship state.
SELECT
    (SELECT COUNT(*)
     FROM tickets
     WHERE ticket_id = 5) AS ticket_count,
    (SELECT COUNT(*)
     FROM comments
     WHERE ticket_id = 5) AS comment_count,
    (SELECT COUNT(*)
     FROM ticket_tags
     WHERE ticket_id = 5) AS tag_assignment_count,
    (SELECT COUNT(*)
     FROM tags
     WHERE name = 'email') AS reusable_tag_count;

-- Commit a related Ticket and Comment write atomically.
BEGIN;

INSERT INTO tickets (
    title,
    priority
)
VALUES (
    'Transaction commit demonstration',
    'low'
)
RETURNING
    ticket_id,
    title,
    priority,
    status;

INSERT INTO comments (
    ticket_id,
    body
)
SELECT
    ticket_id,
    'This comment was created in the same transaction.'
FROM tickets
WHERE title = 'Transaction commit demonstration'
RETURNING
    comment_id,
    ticket_id,
    body;

COMMIT;

-- Verify that both committed rows are visible.
SELECT
    t.ticket_id,
    t.title,
    t.status,
    c.comment_id,
    c.body AS comment_body
FROM tickets AS t
INNER JOIN comments AS c
    ON c.ticket_id = t.ticket_id
WHERE t.title = 'Transaction commit demonstration';

-- Remove the committed demonstration data.
BEGIN;

DELETE FROM tickets
WHERE title = 'Transaction commit demonstration'
RETURNING
    ticket_id,
    title;

COMMIT;

-- Verify that the cleanup and its cascade were committed.
SELECT
    (SELECT COUNT(*)
     FROM tickets
     WHERE title = 'Transaction commit demonstration') AS ticket_count,
    (SELECT COUNT(*)
     FROM comments
     WHERE body = 'This comment was created in the same transaction.')
        AS comment_count;
