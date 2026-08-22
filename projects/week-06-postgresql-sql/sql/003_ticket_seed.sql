TRUNCATE TABLE
    ticket_tags,
    comments,
    tags,
    tickets
RESTART IDENTITY;

INSERT INTO tickets (
    title,
    priority,
    status
)
VALUES
    ('VPN connection fails', 'high', 'open'),
    ('Printer is unavailable', 'medium', 'in_progress'),
    ('Password reset request', 'low', 'resolved'),
    ('Production API latency', 'critical', 'open'),
    ('Email synchronization fails', 'medium', 'closed'),
    ('Laptop battery drains quickly', 'low', 'open')
RETURNING
    ticket_id,
    title,
    priority,
    status,
    created_at,
    updated_at;
