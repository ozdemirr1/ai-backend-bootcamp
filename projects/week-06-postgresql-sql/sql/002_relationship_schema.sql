CREATE TABLE comments (
    comment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ticket_id BIGINT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT comments_ticket_id_fk
        FOREIGN KEY (ticket_id)
        REFERENCES tickets (ticket_id)
        ON DELETE CASCADE,

    CONSTRAINT comments_body_format
        CHECK (
            body = btrim(body)
            AND char_length(body) BETWEEN 3 AND 1000
        )
);

CREATE TABLE tags (
    tag_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT tags_name_format
        CHECK (
            name = lower(btrim(name))
            AND char_length(name) BETWEEN 2 AND 50
        ),

    CONSTRAINT tags_name_unique
        UNIQUE (name)
);

CREATE TABLE ticket_tags (
    ticket_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT ticket_tags_pkey
        PRIMARY KEY (ticket_id, tag_id),

    CONSTRAINT ticket_tags_ticket_id_fk
        FOREIGN KEY (ticket_id)
        REFERENCES tickets (ticket_id)
        ON DELETE CASCADE,

    CONSTRAINT ticket_tags_tag_id_fk
        FOREIGN KEY (tag_id)
        REFERENCES tags (tag_id)
        ON DELETE CASCADE
);
