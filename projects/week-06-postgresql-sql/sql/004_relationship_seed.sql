-- Insert reusable tags.
INSERT INTO tags (
    name
)
VALUES
    ('network'),
    ('hardware'),
    ('authentication'),
    ('performance'),
    ('email')
RETURNING
    tag_id,
    name,
    created_at;

-- Insert comments belonging to tickets.
INSERT INTO comments (
    ticket_id,
    body
)
VALUES
    (1, 'Users cannot establish a VPN connection.'),
    (1, 'Authentication succeeds after reconnecting to the office network.'),
    (2, 'The printer is reachable by IP but does not accept jobs.'),
    (4, 'Latency increased after the latest deployment.'),
    (4, 'The API response time exceeds two seconds.'),
    (5, 'Synchronization resumed after reconnecting the mailbox.')
RETURNING
    comment_id,
    ticket_id,
    body,
    created_at;

-- Assign reusable tags to tickets.
INSERT INTO ticket_tags (
    ticket_id,
    tag_id
)
VALUES
    (1, 1),
    (1, 3),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
RETURNING
    ticket_id,
    tag_id,
    assigned_at;
