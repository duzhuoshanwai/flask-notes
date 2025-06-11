DROP TABLE IF EXISTS notes;

CREATE TABLE notes (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    edited_at TIMESTAMP DEFAULT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);