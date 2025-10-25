# fathom/README.md

# Fathom Component

**Purpose:** Download and aggregate Fathom meeting transcripts from the Fathom API

## Overview

This component provides tools to:
1. Download transcripts from Fathom API for ERA Town Hall meetings
2. Collect manually downloaded transcripts when API unavailable
3. Aggregate all transcripts with existing meeting data (agendas, summaries)
4. Generate comprehensive chronological markdown archive

## Data Sources

For each ERA Town Hall meeting, we combine:
- **Meeting metadata** from `FathomInventory/fathom_emails.db` (calls table)
- **Town Hall agendas** from Google Docs (town_hall_agendas table)
- **Fathom AI summaries** from email processing (emails.body_md)
- **Full transcripts** from Fathom API (downloaded by this component)

## Files

**Scripts:**
- `download_transcripts.py` - Main script to download and aggregate transcripts via API
- `interleave_transcripts.py` - Script to interleave manually-collected transcripts into complete file

**Data:**
- `progress.json` - Resumability state (auto-generated)
- `failures.log` - Detailed failure tracking for API failures

**Output:**
- `output/era_townhalls_complete.md` - Final aggregated output (183K+ lines, 65 meetings)
- `output/era_townhalls_complete.md.backup` - Backup before manual transcript interleaving

## Usage

### Initial Setup
```bash
# API key is hardcoded from existing test_api2.py
# No additional configuration needed
```

### Download Transcripts
```bash
# Test mode - first 3 meetings only
python download_transcripts.py --test

# Full run - all 66 ERA Town Hall meetings
python download_transcripts.py --all

# Resume from interruption
python download_transcripts.py --resume
```

### Features

**Conservative Rate Limiting:**
- Sequential processing (one at a time)
- Waits for each API response confirmation before next request
- 3-second delay between successful requests
- Exponential backoff on errors (3s → 6s → 12s → 24s)

**Failure Handling:**
- Records all failures with reasons in `failures.log`
- Continues processing remaining meetings
- Supports resumability via `progress.json`
- Detailed error reporting for manual mop-up

**Output Format:**
- Chronological markdown compilation
- Meeting headers with metadata
- Agendas (when available)
- AI summaries (when available)
- Full transcripts with speaker attribution and timestamps

## Rate Limiting Strategy

To avoid overwhelming Fathom API:
1. **Sequential only** - No parallel requests
2. **Confirmation before proceed** - Verify response success
3. **Polite delays** - 3s minimum between requests
4. **Backoff on errors** - Exponential delay if issues occur
5. **Abort on repeated failures** - Stop after 5 consecutive errors

### 4. Specialized Topics

#### Complete Workflow

**Phase 1: Automated API Download**
```bash
# Test on first 3 meetings
python download_transcripts.py --test

# Full run on all meetings
python download_transcripts.py --all
```

**What happens:**
- Queries Fathom API using date-range search (not pagination)
- Retrieves meetings from 2023-04-26 to 2025-10-01
- Includes: meeting metadata, agendas, AI summaries, transcripts
- Strips base64-encoded images from agendas
- Saves progress after each meeting (resumable)
- Creates `output/era_townhalls_complete.md`

**Phase 2: Manual Collection for API Gaps**

Some meetings aren't accessible via API but are available on Fathom website:

```bash
# Manually visit each failed meeting URL
# Click download/copy transcript
# Aggregate into output/Missing 7.md
```

**Phase 3: Interleave Manual Transcripts**
```bash
python interleave_transcripts.py
```

**What happens:**
- Creates backup: `era_townhalls_complete.md.backup`
- Parses manually-collected transcripts from `Missing 7.md`
- Finds corresponding "Transcript not available" sections in complete file
- Replaces with actual transcript content
- Deletes `Missing 7.md` (now integrated)

**Final Result:**
- 65 ERA Town Hall meetings (2023-2025)
- 100% transcript coverage
- 183,568 lines of aggregated content
- Chronologically organized
- Searchable, shareable single file

#### API Strategy: Date-Range Queries

**Why not pagination?**
- Fathom API pagination has ~2 year historical limit
- Older meetings (2023-2024) not accessible via cursor-based pagination

**Date-range solution:**
- Query API with `created_after` and `created_before` parameters
- Each meeting's date used to query ±1 day window
- Finds meetings regardless of age
- Much more efficient than paginating through thousands of meetings

**Implementation:**
```python
params = {
    'created_after': '2023-04-25T00:00:00Z',
    'created_before': '2023-04-27T23:59:59Z',
    'limit': 100,
    'include_transcript': 'true'
}
```

#### Image Stripping

Town Hall agendas from Google Docs contain base64-encoded images that bloat the output.

**Removal patterns:**
```python
# Markdown image references: [image1]: <data:image/...>
text = re.sub(r'\[image\d+\]:\s*<data:image/[^>]+>', '', text)

# Inline images: ![alt](data:image/...)
text = re.sub(r'!\[([^\]]*)\]\(data:image/[^)]+\)', '', text)

# Image references: ![][imageN]
text = re.sub(r'!\[\]\[image\d+\]', '', text)
```

**Result:** Clean, readable agendas without binary bloat

#### Resumability

**progress.json tracks:**
```json
{
  "completed": ["19714472", "20977039", ...],
  "failed": {
    "426784451": {
      "reason": "No transcript available",
      "timestamp": "2025-10-24T21:50:26",
      "details": "API returned no transcript data"
    }
  },
  "last_processed_date": "2025-10-01"
}
```

**On resume:**
- Skips completed meetings
- Appends to existing output file
- Retries failed meetings
- Handles Ctrl+C gracefully

#### Database Integration

**Source:** `/FathomInventory/fathom_emails.db`

**Query joins three tables:**
```sql
SELECT 
  c.hyperlink, c.title, c.date, c.duration,
  t.agenda_text,  -- from town_hall_agendas
  e.body_md       -- from emails (Fathom summaries)
FROM calls c
LEFT JOIN town_hall_agendas t ON DATE(c.date) = DATE(t.meeting_date)
LEFT JOIN emails e ON DATE(c.date) = DATE(e.meeting_date)
WHERE c.title LIKE '%ERA Town Hall%'
ORDER BY c.date
```

**Database maintenance:**
- Remove mislabeled meetings: `DELETE FROM calls WHERE hyperlink = '...'`
- Check count: `SELECT COUNT(*) FROM calls WHERE title LIKE '%ERA Town Hall%'`

## Back to: [/README.md](../README.md)