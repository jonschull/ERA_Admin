-- Non-destructive migration: create a standalone calls table for tracking
-- Safe to run multiple times due to IF NOT EXISTS guards.

BEGIN;

CREATE TABLE IF NOT EXISTS calls (
    hyperlink TEXT PRIMARY KEY,
    title TEXT,
    date TEXT,
    duration TEXT,
    share_status TEXT DEFAULT '',
    shared_with TEXT,
    share_timestamp TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_calls_created_at ON calls(created_at);

COMMIT;
