# Phase 2: ERA Meeting Analysis - Detailed Plan

**Goal:** Analyze 112 ERA Town Hall and ERA Africa meetings  
**Impact:** Minimal - mostly isolated to analysis/ directory  
**Date:** October 17, 2025

---

## 📋 What Will Be Modified

### Main System Files (Read-Only Access)
**No modifications - only reading:**
- ✅ `fathom_emails.db` - Read calls table to identify ERA meetings
- ✅ `fathom_cookies.json` - Used for authentication (existing)

### Analysis Directory (Active Work Area)
**Will be modified:**
- ⚠️ `era connections.tsv` - Will add "x" marks to Analyze column for 112 ERA meetings
- 📝 `analysis_results.txt` - Will append new analysis results
- 📝 `analyzed_urls.txt` - Will track newly analyzed URLs
- 📝 `participants.csv` - Will append new participant records

### Database (Controlled Changes)
**Will be modified:**
- 🔄 `fathom_emails.db` - participants table only (append new records)
- ✅ Isolated from calls and emails tables
- ✅ Can be rolled back without affecting main system

---

## 🔒 Safety Measures

### 1. Backup Strategy
```bash
# BEFORE starting Phase 2:
cp fathom_emails.db fathom_emails.db.backup_pre_era_analysis
cp analysis/era\ connections.tsv analysis/era\ connections.tsv.backup
cp analysis/participants.csv analysis/participants.csv.backup
```

### 2. Isolation Guarantees
- ✅ Analysis runs in separate `analysis/` directory
- ✅ No modifications to calls or emails tables
- ✅ No changes to authentication files
- ✅ No impact on daily automation (yet)

### 3. Incremental Approach
Instead of analyzing all 112 at once:
- **Test run:** Analyze 3-5 ERA meetings first
- **Validate:** Check results quality
- **Full run:** Only after test validation
- **Import:** Import to database last (after validation)

---

## 📊 Step-by-Step Execution Plan

### Step 1: Preparation (5 minutes)
```bash
# Create backups
cd /Users/admin/FathomInventory
cp fathom_emails.db fathom_emails.db.backup_$(date +%Y%m%d_%H%M)
cd analysis
cp "era connections.tsv" "era connections.tsv.backup_$(date +%Y%m%d_%H%M)"
cp participants.csv participants.csv.backup_$(date +%Y%m%d_%H%M)

# Verify authentication
cd ../authentication
python test_fathom_cookies.py  # Should show ✅ OK
```

**Go/No-Go Decision Point:** Only proceed if auth test passes

---

### Step 2: Mark ERA Meetings (2 minutes)
```python
# Script to mark ERA meetings in TSV (safe - can be undone)
import csv

with open('era connections.tsv', 'r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    rows = list(reader)

# Find ERA/Africa meetings
era_keywords = ['town hall', 'era africa', 'africa town']
marked_count = 0

for row in rows:
    title_lower = row['Title'].lower()
    if any(kw in title_lower for kw in era_keywords):
        row['Analyze'] = 'x'
        marked_count += 1

print(f"Marked {marked_count} ERA meetings")

# Write back (WITH BACKUP FIRST)
with open('era connections.tsv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=reader.fieldnames, delimiter='\t')
    writer.writeheader()
    writer.writerows(rows)
```

**Validation:** Check that ~112 meetings are now marked

---

### Step 3: Test Run (10 minutes)
```bash
# Analyze ONLY 5 meetings as test
# Modify batch_analyze_calls.py to add --limit flag

python batch_analyze_calls.py --limit 5
```

**Expected Output:**
- 5 new entries in `analysis_results.txt`
- 5 URLs in `analyzed_urls.txt`
- ~30-40 new participant records

**Go/No-Go Decision Point:** Only proceed if:
- ✅ All 5 analyses complete successfully
- ✅ Output format looks correct
- ✅ No authentication errors

---

### Step 4: Full Analysis (60-90 minutes)
```bash
# Run full batch analysis on remaining ~107 ERA meetings
# Using watchdog wrapper for reliability

python run_analysis_wrapper.py
```

**Monitor:**
- Progress every ~5 minutes
- Watch for authentication failures
- Check for stuck processes

**Can pause/resume:** Script tracks completed analyses in `analyzed_urls.txt`

---

### Step 5: Parse Results (5 minutes)
```bash
# Extract participant data from new analysis results
python parse_analysis_results.py

# Verify output
wc -l participants.csv  # Should show ~2,100+ lines (1,271 + ~900 new)
```

**Validation:**
- Check participant count increased
- Spot-check 3-5 random entries for quality

---

### Step 6: Import to Database (5 minutes)
```bash
# Import new participants only
# Script will skip duplicates based on (name, source_call_url)

python import_participants.py --incremental
```

**Validation:**
```sql
-- Check new records
SELECT COUNT(*) FROM participants WHERE analyzed_at > datetime('now', '-1 hour');

-- Verify call linkage
SELECT COUNT(*) FROM participants WHERE call_hyperlink IS NOT NULL;
```

---

## ⚠️ Risk Assessment

### Low Risk
- ✅ Analysis runs in isolated directory
- ✅ Database changes are additive only (INSERT, no UPDATE/DELETE)
- ✅ Original calls/emails tables untouched
- ✅ Daily automation not yet affected

### Medium Risk
- ⚠️ Long runtime (~1.5 hours) - could hit cookie expiration
  - **Mitigation:** Use watchdog wrapper, can resume
  
- ⚠️ Batch process could hang
  - **Mitigation:** Watchdog restarts after 5 min timeout
  
- ⚠️ Database could get participant duplicates
  - **Mitigation:** Schema allows duplicates (same person in multiple calls is valid)

### Mitigated Risks
- 🛡️ Backups created before each step
- 🛡️ Test run validates process before full run
- 🛡️ Incremental approach allows stopping at any point

---

## 🔄 Rollback Plan

### If Test Run Fails
```bash
# Restore TSV
cp "era connections.tsv.backup_*" "era connections.tsv"

# Remove test analysis results
# (analyze_urls.txt and analysis_results.txt can be edited manually)
```

### If Full Analysis Fails
```bash
# Database: Remove new participants
sqlite3 fathom_emails.db << SQL
DELETE FROM participants WHERE analyzed_at > 'YYYY-MM-DD HH:MM:SS';
SQL

# Files: Restore from backups
cp participants.csv.backup_* participants.csv
```

### Nuclear Option (Full Rollback)
```bash
# Restore entire database
cp fathom_emails.db.backup_* fathom_emails.db

# Restore all analysis files
cp *.backup_* .
```

---

## ✅ Success Criteria

### After Test Run (5 meetings)
- [ ] 5 analyses complete without errors
- [ ] Participant extraction works correctly
- [ ] Database import successful
- [ ] No impact on main system tables

### After Full Run (112 meetings)
- [ ] ~112 new analysis entries
- [ ] ~900-1,200 new participant records
- [ ] All linked to source calls in database
- [ ] Main system still operational

### Final Validation
```sql
-- Total participants should be ~2,100+
SELECT COUNT(*) FROM participants;

-- ERA meetings should be represented
SELECT COUNT(DISTINCT source_call_title) 
FROM participants 
WHERE source_call_title LIKE '%Town Hall%'
   OR source_call_title LIKE '%Africa%';

-- No orphaned records
SELECT COUNT(*) FROM participants WHERE call_hyperlink IS NULL;
```

---

## 📅 Estimated Timeline

| Step | Duration | Can Pause? |
|------|----------|------------|
| 1. Preparation | 5 min | Yes |
| 2. Mark meetings | 2 min | Yes |
| 3. Test run (5 meetings) | 10 min | No |
| **Decision Point** | - | - |
| 4. Full analysis (107 meetings) | 60-90 min | Yes (auto-resume) |
| 5. Parse results | 5 min | Yes |
| 6. Import to database | 5 min | Yes |
| **Total** | **~2 hours** | |

---

## 🚦 Go/No-Go Checklist

**Before Starting:**
- [ ] Backups created
- [ ] Authentication tested (✅ OK)
- [ ] Understand rollback plan
- [ ] Time available (~2 hours)

**After Test Run:**
- [ ] 5 analyses successful
- [ ] Results quality acceptable
- [ ] No errors in console
- [ ] User approval to proceed

**Before Database Import:**
- [ ] Participant count looks reasonable
- [ ] Spot-checked data quality
- [ ] User approval to modify database

---

## 💬 Questions to Resolve

1. **Timing:** Run now or schedule for later?
2. **Scope:** All 112 ERA meetings or start smaller?
3. **Validation:** What specific checks would you like before proceeding?
4. **Automation:** Wait on Phase 3 (daily automation) until Phase 2 validates?

---

**Recommendation:** Start with test run (5 meetings), validate, then proceed with user approval at each decision point.

**Ready to proceed with Step 1 (Preparation)?**
