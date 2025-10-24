-- Add Town Hall agenda storage to avoid repeated Google Drive downloads
-- Each agenda downloaded once, then searched locally

CREATE TABLE IF NOT EXISTS town_hall_agendas (
    agenda_id TEXT PRIMARY KEY,
    meeting_date TEXT,
    meeting_title TEXT,
    agenda_text TEXT,  -- Markdown format (preserves structure)
    format TEXT DEFAULT 'markdown',  -- 'markdown' or 'plain'
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_agenda_date ON town_hall_agendas(meeting_date);

-- Full-text search index for agenda content
CREATE VIRTUAL TABLE IF NOT EXISTS agenda_search USING fts5(
    agenda_id UNINDEXED,
    meeting_title, 
    agenda_text,
    content='town_hall_agendas',
    content_rowid='rowid'
);

-- Trigger to keep FTS index in sync
CREATE TRIGGER IF NOT EXISTS agenda_ai AFTER INSERT ON town_hall_agendas BEGIN
    INSERT INTO agenda_search(rowid, agenda_id, meeting_title, agenda_text)
    VALUES (new.rowid, new.agenda_id, new.meeting_title, new.agenda_text);
END;

CREATE TRIGGER IF NOT EXISTS agenda_au AFTER UPDATE ON town_hall_agendas BEGIN
    UPDATE agenda_search SET meeting_title = new.meeting_title, agenda_text = new.agenda_text
    WHERE rowid = new.rowid;
END;

CREATE TRIGGER IF NOT EXISTS agenda_ad AFTER DELETE ON town_hall_agendas BEGIN
    DELETE FROM agenda_search WHERE rowid = old.rowid;
END;
