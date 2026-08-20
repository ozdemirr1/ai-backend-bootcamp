-- List tickets together with their comments.
SELECT
    t.ticket_id,
    t.title,
    c.comment_id,
    c.body AS comment_body
FROM tickets AS t
INNER JOIN comments AS c
    ON c.ticket_id = t.ticket_id
ORDER BY
    t.ticket_id ASC,
    c.comment_id ASC;

-- List every ticket, including tickets without comments.
SELECT
    t.ticket_id,
    t.title,
    c.comment_id,
    c.body AS comment_body
FROM tickets AS t
LEFT JOIN comments AS c
    ON c.ticket_id = t.ticket_id
ORDER BY
    t.ticket_id ASC,
    c.comment_id ASC;

-- List tickets together with their assigned tags.
SELECT
    t.ticket_id,
    t.title,
    tg.tag_id,
    tg.name AS tag_name
FROM tickets AS t
INNER JOIN ticket_tags AS tt
    ON tt.ticket_id = t.ticket_id
INNER JOIN tags AS tg
    ON tg.tag_id = tt.tag_id
ORDER BY
    t.ticket_id ASC,
    tg.tag_id ASC;

-- Count comments for every ticket.
SELECT
    t.ticket_id,
    t.title,
    COUNT(c.comment_id) AS comment_count
FROM tickets AS t
LEFT JOIN comments AS c
    ON c.ticket_id = t.ticket_id
GROUP BY
    t.ticket_id,
    t.title
ORDER BY
    t.ticket_id ASC;

-- Count assigned tags for every ticket.
SELECT
    t.ticket_id,
    t.title,
    COUNT(tt.tag_id) AS tag_count
FROM tickets AS t
LEFT JOIN ticket_tags AS tt
    ON tt.ticket_id = t.ticket_id
GROUP BY
    t.ticket_id,
    t.title
ORDER BY
    t.ticket_id ASC;

-- Summarize assigned tag names for every ticket.
SELECT
    t.ticket_id,
    t.title,
    COUNT(tg.tag_id) AS tag_count,
    COALESCE(
        STRING_AGG(tg.name, ', ' ORDER BY tg.name),
        'no tags'
    ) AS tag_names
FROM tickets AS t
LEFT JOIN ticket_tags AS tt
    ON tt.ticket_id = t.ticket_id
LEFT JOIN tags AS tg
    ON tg.tag_id = tt.tag_id
GROUP BY
    t.ticket_id,
    t.title
ORDER BY
    t.ticket_id ASC;
