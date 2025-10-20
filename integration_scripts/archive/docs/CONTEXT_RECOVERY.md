# Context Recovery Guide - Phase 4B

**If you're coming back to this project after a break, start here!**

---

## Quick Status (As of 2025-10-19)

✅ **Phase 4B-1: COMPLETE**
- Interactive fuzzy matching system built
- 364 participants enriched with Airtable data
- Enhanced HTML approval interface working
- Database safely modified with backups

⏭️ **Phase 4B-2: NEXT**
- 279 unenriched participants need review
- Gmail API integration for research
- Categorize: delete/merge/add/ignore

---

## What We Built

### **The Problem**
- Fathom has 651 video participants (AI-generated names, often misspelled)
- Airtable has 592 ERA members (ground truth)
- Need to: Match them, enrich Fathom with Airtable data, handle unmatched

### **The Solution**
**Phase 4B-1:** Interactive reconciliation system

1. **Fuzzy match** Fathom → Airtable (80% threshold)
2. **Human review** via sortable HTML table
3. **Export CSV** with approvals/rejections/comments
4. **Batch process** CSV to enrich database
5. **Skip enriched** in future runs

### **Key Innovation**
**Comment-driven actions:** User adds keywords in Comments column:
- `drop` → Delete from Fathom
- `Correct Name` → Use this name instead
- `needs reunion` → Multiple accounts to merge
- etc.

---

## File Map (What to Read)

### **Start Here**
1. `README_PHASE4B.md` - Complete documentation
2. `COMMIT_PHASE4B1.md` - What was built & why
3. This file - Quick orientation

### **Main Scripts**
- `phase4b1_enrich_from_airtable.py` - Main pipeline
- `process_approved_matches.py` - CSV batch processor

### **Supporting Docs**
- `PHASE4B1_ENHANCEMENTS_SUMMARY.md` - Feature list
- `needs_reunion_email.md` - Email template

---

## How to Resume Work

### **Verify Current State**

```bash
cd /Users/admin/ERA_Admin
source ERA_Admin_venv/bin/activate
```

Check database:
```sql
sqlite3 FathomInventory/fathom_emails.db "
SELECT 
  COUNT(DISTINCT CASE WHEN validated_by_airtable = 1 THEN name END) as enriched,
  COUNT(DISTINCT CASE WHEN validated_by_airtable IS NULL OR validated_by_airtable = 0 THEN name END) as unenriched,
  COUNT(DISTINCT name) as total
FROM participants;
"
```

Expected output:
```
enriched|unenriched|total
248|279|527
```

### **Run Phase 4B-1 Again (Test)**

```bash
/Users/admin/ERA_Admin_venv/bin/python3 integration_scripts/phase4b1_enrich_from_airtable.py
```

Should show:
```
Skipping 248 already-enriched participants
Matching 279 unenriched participants...
```

**If it shows 0 matches:** ✅ Good! All current participants are either enriched or below 80% threshold. Ready for Phase 4B-2.

---

## Next Steps (Phase 4B-2)

### **Goal**
Review 279 unenriched participants:
- 53 you rejected in Phase 4B-1 (saw them, said no)
- 226 never matched (< 80% or not in Airtable)

### **Categories to Handle**
1. **Organizations** (15) - Delete (e.g., "Global Earth Repair")
2. **Phone numbers** (2) - Delete
3. **Duplicates/variants** (59) - Merge (e.g., "Charlie Shore, MD")
4. **Low-score matches** - Manual review
5. **Not in Airtable** (176) - Research with Gmail API

### **Workflow**
1. **Setup Gmail API** for email research
2. **Generate approval table** for unenriched participants
3. **Use Gmail lookup** to research unknown people
4. **Categorize** using comment keywords:
   - `drop` - Delete
   - `merge with: Person Name` - Consolidate
   - `add to airtable` - Create Airtable entry
   - `ignore` - Not ERA-related

5. **Export CSV** and process

---

## Important Numbers

**Database totals:**
- Started: 651 unique participants (1624 records)
- Deleted: 9 participants (11 records)
- Merged: ~116 (due to name corrections)
- Current: 527 unique participants (1613 records)

**Enrichment status:**
- Enriched: 248 unique names (1229 records)
- Unenriched: 279 unique names (384 records)

**Quality:**
- Name corrections: 188 (AI → Airtable)
- Members identified: 351
- Donors identified: 64
- Emails added: 360

---

## Key Principles

1. **Airtable is ground truth** - Fathom names get corrected to match
2. **Human in the loop** - No automatic decisions on fuzzy matches
3. **Skip enriched** - Don't re-process validated participants
4. **Comment-driven** - User keywords drive batch actions
5. **Safety first** - Backups, transactions, rollback

---

## If Things Look Wrong

### **Too many matches (should be ~0-50 max)**
Something reset `validated_by_airtable` flags. Check:
```sql
SELECT COUNT(*) FROM participants WHERE validated_by_airtable = 1;
```

Should be ~1229 records.

### **Database corruption**
Restore from backup:
```bash
ls -lt FathomInventory/backups/
cp FathomInventory/backups/fathom_emails.backup_YYYYMMDD_HHMM.db \
   FathomInventory/fathom_emails.db
```

### **Lost CSV approvals**
Check Downloads folder:
```bash
ls -lt ~/Downloads/phase4b1_approvals*.csv
```

### **Can't remember what you decided**
Check git history:
```bash
git log --oneline --all -20
git show 9dc17fe  # Phase 4B-1 commit
```

---

## Technical Details

### **Fuzzy Matching Algorithm**
Uses three methods, takes highest score:
- `fuzz.ratio` - Full string comparison
- `fuzz.partial_ratio` - Substring matching
- `fuzz.token_sort_ratio` - Word-order independent

Threshold: 80% (configurable in `MATCH_THRESHOLD`)

### **Database Schema Changes**
Added to `participants` table:
```sql
validated_by_airtable BOOLEAN  -- Flag to skip re-matching
era_member BOOLEAN            -- From Airtable
is_donor BOOLEAN             -- From Airtable
email TEXT                   -- From Airtable
airtable_id TEXT            -- Airtable record ID
projects TEXT               -- From Airtable
data_source TEXT            -- Set to 'both'
landscape_node_id TEXT      -- Future use
```

### **Safety Mechanisms**
1. Automatic backups before any DB writes
2. Transactions with rollback on error
3. Integrity checks before/after
4. No in-place edits (reads, then writes)

---

## Contact / Questions

**Human:** Jon Schull (jschull@gmail.com)  
**AI Assistant:** Claude (Anthropic)  
**Project:** ERA Admin / Fathom-Airtable Integration  
**Repository:** `/Users/admin/ERA_Admin`  

---

**Last Updated:** 2025-10-19  
**Phase:** 4B-1 Complete ✅ | 4B-2 Next ➡️  
**Status:** Ready for Gmail API integration
