# Fathom Alias Resolution System

### 1. Overview

**Purpose:** Context-aware participant alias resolution and database cleanup

Track context-dependent alias-to-person mappings from Fathom meetings. Enables queries like "show me all of Brian Kravitz's sessions" which automatically includes meetings where he appeared as "bk", "brian", "Brian K", etc.

**What this component does:**
- Builds alias resolution table from Phase 4B-2 decisions
- Provides command-line tools to query sessions by name or alias
- Detects and merges participant redundancies
- Maintains database quality (reduced duplicates by 77%)

**Key deliverables:**
- `fathom_alias_resolutions` table - 495 context-aware alias mappings
- `participant_meetings` view - Easy session queries
- Participant count reduced from 461 → 423 (38 duplicates merged)
- All changes backed up and reversible

### 2. Orientation - Where to Find What

**You are at:** Alias Resolution & Cleanup System

**Use this when:**
- Need to find all sessions for a participant (by any name they've used)
- Want to extract transcript excerpts for someone
- Cleaning up database redundancies
- Resolving ambiguous participant names

**What you might need:**
- **Parent** → [integration_scripts/README.md](README.md) - Integration workflows
- **Data source** → Phase 4B-2 CSV decisions in `past_decisions/`
- **Database** → [FathomInventory/fathom_emails.db](../FathomInventory/fathom_emails.db)
- **Scripts** → Listed in Specialized Topics below

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

**Alias resolution-specific:**

**1. Context Dependency**
- Same alias can map to different people in different meetings
- "bk" = Brian Kravitz in Meeting A, Bob King in Meeting B
- Never merge aliases globally - always preserve meeting context

**2. Data Safety**
- Always create timestamped backups before merges
- All operations are reversible
- Log all actions for audit trail
- Test queries before bulk operations

**3. Human Oversight**
- High-confidence merges executed automatically
- Medium-confidence cases need user verification
- Always show reasoning and evidence links

### 4. Specialized Topics

## Problem Solved

**Before:**
- User: "Find all Brian Kravitz sessions"
- System: Only finds sessions where Fathom displayed "Brian Kravitz"
- Missing: Sessions where he appeared as "bk", "brian", etc.

**After:**
- User: "Find all Brian Kravitz sessions"
- System: Finds ALL sessions including aliases
- Context-aware: "bk" = Brian Kravitz in Meeting A, Bob King in Meeting B

## Database Schema

### Table: `fathom_alias_resolutions`

```sql
CREATE TABLE fathom_alias_resolutions (
    id INTEGER PRIMARY KEY,
    fathom_name TEXT NOT NULL,     -- What Fathom displayed: "bk"
    meeting_url TEXT,              -- In which meeting (NULL if unknown)
    resolved_to TEXT,              -- Who it actually is: "Brian Kravitz"
    decision_type TEXT,            -- "merge", "add", "drop"
    decision_source TEXT,          -- Which batch CSV
    resolved_at TIMESTAMP
);
```

**Indexes:**
- `idx_alias_fathom_name` - Fast lookup by alias
- `idx_alias_resolved_to` - Fast lookup by person name
- `idx_alias_meeting` - Fast lookup by meeting

### View: `participant_meetings`

Simplified query interface:

```sql
CREATE VIEW participant_meetings AS
SELECT DISTINCT
    resolved_to AS participant_name,
    meeting_url,
    fathom_name AS appeared_as,
    c.title AS meeting_title,
    c.date AS meeting_date,
    decision_type
FROM fathom_alias_resolutions far
LEFT JOIN calls c ON far.meeting_url = c.hyperlink
WHERE resolved_to IS NOT NULL
ORDER BY c.date DESC;
```

## Data Source

**Phase 4B-2 CSV decisions:**
- `past_decisions/phase4b2_approvals_*.csv`
- Format: `fathom_name,decision,ProcessThis`
- Example: `bk,merge with: Brian Kravitz,YES`

**Phase 4B-2 HTML reports (for meeting URLs):**
- `past_batches/BATCH*.html`
- Contains Fathom call URLs linked to each name
- Preserves meeting context

## Scripts

### 1. Build the Table

```bash
python build_alias_resolution_table.py
```

**What it does:**
- Drops and recreates `fathom_alias_resolutions` table
- Parses all Phase 4B-2 CSV files
- Extracts meeting URLs from HTML reports
- Inserts 495+ alias resolutions
- Creates `participant_meetings` view
- Generates summary report

**Output:**
```
✅ Total resolutions: 495
   merge: 346
   add: 71
   drop: 70

👥 People with most aliases:
   Ana Calderon (5 aliases)
   Brian Von Herzen (4 aliases)
   ...

🔀 Ambiguous aliases:
   'Angelique' → 3 people
   'bk' → 2 people (Brian Kravitz, dropped)
```

### 2. Query Participant Sessions

```bash
python query_participant_sessions.py "Brian Kravitz"
```

**Find by real name:**
```bash
python query_participant_sessions.py "Brian Kravitz"
# Output:
# 🎥 Sessions for 'Brian Kravitz':
# 👤 Brian Kravitz:
#    • 2024-03-15: appeared as 'bk'
#    • 2024-05-20: appeared as 'Brian Kravitz'
#    • 2024-07-10: appeared as 'brian'
```

**Find by alias:**
```bash
python query_participant_sessions.py "bk"
# Output:
# 🎥 Sessions for 'bk':
# 👤 Brian Kravitz:
#    • 2024-03-15: appeared as 'bk'
#
# 🏷️ Alias 'bk' resolutions:
#    • Brian Kravitz (Meeting A)
#    • (dropped) (Meeting B)
```

**List ambiguous aliases:**
```bash
python query_participant_sessions.py --list-ambiguous
# Output:
# 🔀 Ambiguous Aliases:
# 'Angelique' → 3 people:
#    Angelique, Angelique Gonzalez, Angelique Garcia
# 'bk' → 2 people:
#    Brian Kravitz, (dropped)
```

## Usage Examples

### Use Case 1: Extract Transcript Excerpts

**Goal:** Pull up all of Brian Kravitz's sessions to extract quotes

```python
import sqlite3

conn = sqlite3.connect("../FathomInventory/fathom_emails.db")

# Get all Brian's sessions
sessions = conn.execute("""
    SELECT meeting_url, appeared_as, meeting_date, meeting_title
    FROM participant_meetings
    WHERE participant_name = 'Brian Kravitz'
    ORDER BY meeting_date
""").fetchall()

for url, alias, date, title in sessions:
    print(f"Meeting: {title} ({date})")
    print(f"  Brian appeared as: {alias}")
    print(f"  Fathom URL: {url}")
    # Now fetch transcript from fathom/output/era_townhalls_complete.md
    # and search for lines containing this alias
```

### Use Case 2: Disambiguate Aliases

**Goal:** Determine who "ana" was in a specific meeting

```sql
SELECT resolved_to
FROM fathom_alias_resolutions
WHERE fathom_name = 'ana'
  AND meeting_url = 'https://fathom.video/calls/12345';
```

### Use Case 3: Find All Aliases for a Person

**Goal:** Get complete list of names someone has used

```sql
SELECT DISTINCT fathom_name
FROM fathom_alias_resolutions
WHERE resolved_to = 'Ana Calderon';

-- Result:
-- 'Ana C'
-- 'ana'
-- 'ana - Panama Restoration Lab'
-- 'Ana Calderon'
-- 'Anna Calderon'
```

### Use Case 4: Meeting Participant List

**Goal:** Get all participants from a specific meeting (with aliases resolved)

```sql
SELECT DISTINCT resolved_to
FROM fathom_alias_resolutions
WHERE meeting_url = 'https://fathom.video/calls/12345'
  AND resolved_to IS NOT NULL
ORDER BY resolved_to;
```

## Data Quality

### Current Status

- **495 alias resolutions** from Phase 4B-2 decisions
- **346 merge decisions** (aliases → real names)
- **71 add decisions** (new people)
- **70 drop decisions** (system accounts, noise)

### Known Issues

1. **Missing Meeting URLs:** Many resolutions don't have meeting URLs because:
   - HTML files weren't saved for all batches
   - Some participants weren't in Town Hall meetings
   - **Impact:** Can't link to specific meetings, but aliases still work

2. **Ambiguous Aliases:** Some aliases map to multiple people:
   - "Angelique" → 3 people (likely different Angeliques)
   - "Ana C" → 2 people (typos in resolutions)
   - **Impact:** Query returns all matches, user disambiguates

### Improving Data Quality

**Add missing meeting URLs:**

The HTML batch files contain the Fathom URLs. To add them:

```bash
# Re-run with HTML files present
python build_alias_resolution_table.py
```

**Fix duplicate resolutions:**

```sql
-- Find potential duplicates (case differences)
SELECT resolved_to, COUNT(*) 
FROM fathom_alias_resolutions
WHERE resolved_to IS NOT NULL
GROUP BY LOWER(resolved_to)
HAVING COUNT(*) > 1;

-- Manually fix in database
UPDATE fathom_alias_resolutions
SET resolved_to = 'Chris Searles'
WHERE resolved_to = 'Chris searles';
```

## Maintenance

### When to Rebuild

Rebuild the table when:
- New Phase 4B-2 batches are processed
- You discover alias resolution errors
- HTML files become available for existing batches

### Rebuilding

```bash
cd integration_scripts
python build_alias_resolution_table.py
```

**Safe:** Drops and recreates table, doesn't affect other data.

### Testing After Rebuild

```bash
# Check row count
sqlite3 ../FathomInventory/fathom_emails.db \
  "SELECT COUNT(*) FROM fathom_alias_resolutions;"

# Test known aliases
python query_participant_sessions.py "bk"
python query_participant_sessions.py "Brian Kravitz"

# Check ambiguous aliases
python query_participant_sessions.py --list-ambiguous
```

## Future Enhancements

- [ ] Extract meeting URLs from participants table directly
- [ ] Add fuzzy matching for "Brian Kravitz" vs "Brian Kravitz (3)"
- [ ] Link to actual transcript lines in `era_townhalls_complete.md`
- [ ] Web UI for exploring alias resolutions
- [ ] Auto-suggest aliases when searching
- [ ] Confidence scores for ambiguous aliases

## Related Documentation

- **Phase 4B-2 Process:** `integration_scripts/README.md`
- **Database Schema:** `FathomInventory/README.md`
- **Transcript Archive:** `fathom/README.md`
- **Participant Reconciliation:** `PAST_LEARNINGS.md`

## Questions?

Contact: Jon Schull or see `integration_scripts/README.md` for context.
