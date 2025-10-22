-- Add UNIQUE constraint to prevent duplicate participant names
-- This enforces ONE record per unique person (case-insensitive)

-- First, deduplicate existing data (run deduplicate_participants.py)
-- Then apply this constraint to prevent future duplicates

BEGIN TRANSACTION;

-- Drop view first (it depends on participants table)
DROP VIEW IF EXISTS participants_enriched;

-- Create new table with constraint
CREATE TABLE participants_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Participant information
    name TEXT NOT NULL COLLATE NOCASE,  -- Case-insensitive
    location TEXT,
    affiliation TEXT,
    
    -- Relationships (stored as semicolon-separated values)
    collaborating_people TEXT,
    collaborating_organizations TEXT,
    
    -- Source tracking (now comma-separated for multiple meetings)
    source_call_url TEXT NOT NULL,
    source_call_title TEXT,
    
    -- Link to calls table
    call_hyperlink TEXT,
    
    -- Metadata
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validated_by_airtable BOOLEAN DEFAULT 0,
    era_member BOOLEAN DEFAULT 0,
    is_donor BOOLEAN DEFAULT 0,
    email TEXT,
    airtable_id TEXT,
    projects TEXT,
    data_source TEXT DEFAULT 'fathom_ai',
    landscape_node_id TEXT,
    
    -- UNIQUE constraint on name (case-insensitive)
    UNIQUE(name COLLATE NOCASE)
);

-- Copy data from old table
INSERT INTO participants_new 
SELECT * FROM participants;

-- Drop old table
DROP TABLE participants;

-- Rename new table
ALTER TABLE participants_new RENAME TO participants;

-- Recreate indexes
CREATE INDEX idx_participants_name ON participants(name COLLATE NOCASE);
CREATE INDEX idx_participants_call ON participants(call_hyperlink);
CREATE INDEX idx_participants_source_url ON participants(source_call_url);
CREATE INDEX idx_participants_airtable ON participants(airtable_id);

-- Recreate view
CREATE VIEW participants_enriched AS
SELECT 
    p.id,
    p.name,
    p.location,
    p.affiliation,
    p.collaborating_people,
    p.collaborating_organizations,
    p.source_call_title,
    p.source_call_url,
    c.title as call_title,
    c.date as call_date,
    c.hyperlink as call_hyperlink,
    c.public_share_url,
    p.analyzed_at
FROM participants p
LEFT JOIN calls c ON p.call_hyperlink = c.hyperlink
ORDER BY p.analyzed_at DESC;

COMMIT;
