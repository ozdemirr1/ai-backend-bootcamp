CREATE TABLE tickets (
    ticket_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT tickets_title_format
        CHECK (
            title = btrim(title)
            AND char_length(title) BETWEEN 3 AND 100
        ),

    CONSTRAINT tickets_priority_allowed
        CHECK (
            priority IN ('low', 'medium', 'high', 'critical')
        ),

    CONSTRAINT tickets_status_allowed
        CHECK (
            status IN ('open', 'in_progress', 'resolved', 'closed')
        ),

    CONSTRAINT tickets_timestamp_order
        CHECK (updated_at >= created_at)
);
