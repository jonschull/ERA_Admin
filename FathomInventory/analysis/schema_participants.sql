-- Participants table for Fathom AI analysis results
-- Stores extracted participant information from meeting analysis

CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Participant information
    name TEXT NOT NULL,
    location TEXT,
    affiliation TEXT,
    
    -- Relationships (stored as semicolon-separated values)
    collaborating_people TEXT,
    collaborating_organizations TEXT,
    
    -- Source tracking
    source_call_url TEXT NOT NULL,
    source_call_title TEXT,
    
    -- Link to calls table
    call_hyperlink TEXT,
    
    -- Metadata
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Index for quick lookups
    FOREIGN KEY (call_hyperlink) REFERENCES calls(hyperlink)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_participants_name ON participants(name);
CREATE INDEX IF NOT EXISTS idx_participants_call ON participants(call_hyperlink);
CREATE INDEX IF NOT EXISTS idx_participants_source_url ON participants(source_call_url);

-- View for enriched participant data with call information
CREATE VIEW IF NOT EXISTS participants_enriched AS
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
