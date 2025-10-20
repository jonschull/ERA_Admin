# Analysis Module - Context Recovery

**Last Updated:** October 17, 2025  
**Status:** ✅ Phase 2 Complete - Ready for Daily Automation

---

## 🎯 Purpose

Extract participant information from Fathom meeting AI analysis and store in searchable database. Tracks ERA community network, collaboration patterns, and participant affiliations.

---

## 📊 Current State (Oct 17, 2025)

### Data
- **1,560 participant records** in database (`../fathom_emails.db`)
- **619 unique individuals** identified
- **191 source meetings** analyzed
- **1,266 ERA/Africa records** (81% of total)

### Analysis Coverage
- ✅ 204 total meetings analyzed (all time)
- ✅ 103 ERA Town Hall + ERA Africa (2023-2025)
- ⚠️ 56 recent meetings timed out (can retry)

### Top Participants
1. Jon Schull - 85 ERA meetings
2. Ananda Fitzsimmons - 48 meetings
3. Russ Speer - 46 meetings

---

## 🗂️ File Structure

### Data Files
- **`participants.csv`** (1,560 records) - Parsed participant data
- **`analysis_results.txt`** (355KB) - Raw AI analysis output
- **`era connections.tsv`** (1,639 rows) - Master call list, 159 marked for analysis
- **`analyzed_urls.txt`** (160 lines) - Tracking file for crash recovery

### Scripts (Production)
- **`ask_fathom_ai.py`** - Query Fathom AI for single call
- **`batch_analyze_calls.py`** - Batch process marked calls
- **`parse_analysis_results.py`** - Extract structured data from AI responses
- **`import_participants.py`** - Import CSV to database (full)
- **`import_new_participants.py`** - Import CSV to database (incremental)
- **`run_analysis_wrapper.py`** - Watchdog for long-running batches

### Scripts (Project-Specific)
- **`sync_era_meetings.py`** - Mark ERA meetings, add new from database
- **`mark_era_meetings.py`** - Mark ERA meetings in TSV

### Documentation
- **`README.md`** - Script usage and workflows
- **`PHASE2_COMPLETE.md`** - Oct 17 analysis project report
- **`INTEGRATION_STATUS.md`** - Database integration details
- **`analysis_log.md`** - Historical development log

### Backups (Oct 17, 2025)
- `fathom_emails.db.backup_20251017_1220`
- `era connections.tsv.backup_20251017_1220`
- `participants.csv.backup_20251017_1220`

---

## 🔄 Workflows

### 1. Analyze New ERA Meetings (Manual)
```bash
cd /Users/admin/FathomInventory/analysis

# Mark new ERA meetings
python3 sync_era_meetings.py

# Run batch analysis
python3 batch_analyze_calls.py

# Parse and import
python3 parse_analysis_results.py
python3 import_new_participants.py
```

### 2. Analyze Specific Meeting
```bash
cd /Users/admin/FathomInventory/analysis
python3 ask_fathom_ai.py "https://fathom.video/calls/XXXXXX" \
  "I'd like information on each participant..."
```

### 3. Query Participant Database
```bash
cd /Users/admin/FathomInventory
sqlite3 fathom_emails.db

-- Most active participants
SELECT name, COUNT(*) as meetings 
FROM participants 
GROUP BY name 
ORDER BY meetings DESC LIMIT 10;

-- ERA Africa participants
SELECT * FROM participants_enriched 
WHERE source_call_title LIKE '%ERA Africa%';
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE participants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT,
    affiliation TEXT,
    collaborating_people TEXT,        -- semicolon-separated
    collaborating_organizations TEXT,  -- semicolon-separated
    source_call_url TEXT NOT NULL,
    source_call_title TEXT,
    call_hyperlink TEXT,               -- FK to calls table
    analyzed_at TIMESTAMP
);

-- View with call metadata
CREATE VIEW participants_enriched AS
SELECT p.*, c.date, c.public_share_url
FROM participants p
LEFT JOIN calls c ON p.call_hyperlink = c.hyperlink;
```

---

## 🔧 Common Tasks

### Add More Meetings to Analysis
```bash
# Edit era connections.tsv, add 'x' to Analyze column
# Or run:
python3 sync_era_meetings.py  # Auto-marks ERA meetings

# Then analyze
python3 batch_analyze_calls.py
```

### Resume Failed Analysis
```bash
# Script automatically skips completed URLs
python3 batch_analyze_calls.py  # Continues where it left off
```

### Export Participant Data
```bash
sqlite3 fathom_emails.db << SQL
.mode csv
.headers on
.output era_participants.csv
SELECT * FROM participants_enriched 
WHERE source_call_title LIKE '%ERA%';
SQL
```

### Retry Timed-Out Meetings
```bash
# Get list of failed meetings from PHASE2_COMPLETE.md
# Mark them in era connections.tsv
# Remove their URLs from analyzed_urls.txt
# Re-run batch_analyze_calls.py
```

---

## ⚠️ Known Issues

### Timeout Errors (35% of recent meetings)
- **Symptom:** `Failed to access or interact with the URL`
- **Cause:** Fathom AI slow response or page changes
- **Workaround:** Individual retry or wait for Fathom improvements
- **Impact:** 56 recent ERA Africa meetings not analyzed

### TSV File Encoding
- Use UTF-8 encoding
- Tab-delimited, not comma
- Headers: Title, Nickname, ERA, Analyze, Date, Duration, Hyperlink...

---

## 🚀 Future: Daily Automation (Phase 3)

**Goal:** Automatically analyze new ERA meetings daily

**Plan:**
1. Create `analyze_new_era_calls.py` script
2. Integrate into `../run_all.sh` (after email download)
3. Update daily report to include participant stats
4. Test on one meeting before going live

**Benefits:**
- New ERA meetings analyzed within 24 hours
- Participant database stays current
- No manual intervention

---

## 📝 Recovery Procedures

### If Database Corrupted
```bash
# Restore from backup
cp fathom_emails.db.backup_YYYYMMDD_HHMM ../fathom_emails.db

# Re-import participants
python3 import_participants.py
```

### If Analysis Results Lost
```bash
# Restore analysis_results.txt from backup
# Re-run parse
python3 parse_analysis_results.py
python3 import_new_participants.py
```

### If Need to Start Over
```bash
# Clear participants table
sqlite3 ../fathom_emails.db "DELETE FROM participants;"

# Re-import from CSV
python3 import_participants.py
```

---

## 📊 Key Metrics

### Data Quality
- **100% call linkage** - All participants linked to source calls
- **619 unique names** - Deduplicated at query time
- **81% ERA focus** - 1,266 of 1,560 records
- **65% analysis success rate** - 103 of 159 marked meetings

### Coverage (as of Oct 17, 2025)
- ERA Town Hall: 83 meetings analyzed
- ERA Africa: 37 meetings analyzed  
- Date range: Apr 2023 - Oct 2025

---

## 🔍 Sample Queries

```sql
-- Collaboration network (who works with whom)
SELECT p1.name, p2.name, COUNT(*) as times
FROM participants p1, participants p2
WHERE p1.call_hyperlink = p2.call_hyperlink 
  AND p1.id < p2.id
GROUP BY p1.name, p2.name
HAVING times > 3
ORDER BY times DESC;

-- Geographic distribution
SELECT location, COUNT(DISTINCT name) as people
FROM participants
WHERE location NOT IN ('Unknown', '')
GROUP BY location
ORDER BY people DESC;

-- Organization affiliations
SELECT affiliation, COUNT(*) as count
FROM participants
WHERE affiliation NOT IN ('Unknown', '', 'This participant''s company is not listed in the calendar event')
GROUP BY affiliation
ORDER BY count DESC
LIMIT 20;

-- Activity over time
SELECT DATE(call_date) as month, COUNT(*) as participants
FROM participants_enriched
WHERE call_date IS NOT NULL
GROUP BY month
ORDER BY month DESC
LIMIT 12;
```

---

## ✅ Success Indicators

- [x] Participants table populated and linked
- [x] Can query collaboration networks
- [x] Can track participant engagement over time
- [x] Crash-resistant batch processing
- [x] Incremental import prevents duplicates
- [x] Ready for daily automation

---

## 📞 Questions to Ask When Resuming

1. How many participants in database? (Should be ~1,560)
2. Any new ERA meetings in calls table?
3. Are there failed analyses to retry?
4. Is daily automation integrated yet?
5. When was last analysis run?

```bash
# Quick health check
cd /Users/admin/FathomInventory/analysis
echo "Participants in DB:"
sqlite3 ../fathom_emails.db "SELECT COUNT(*) FROM participants;"
echo "Last analysis:"
tail -20 analysis_results.txt | grep "^## Call:"
```

---

**Status:** ✅ Phase 2 complete, ready for Phase 3 (daily automation)  
**Last Major Work:** Oct 17, 2025 - Analyzed 103 ERA meetings, added 289 participants  
**Next Step:** Integrate into daily automation cycle
