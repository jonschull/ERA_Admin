# Phase 4B-2 Execution Workflow

## Overview
After reviewing the HTML approval table and exporting decisions to CSV, this workflow executes the approved reconciliation actions (merges, drops, additions).

## Prerequisites

### Required Files
- ✅ CSV exported from HTML table (`phase4b2_approvals_*.csv`)
- ✅ Database with UNIQUE constraint on `participants.name` (added in PR #17)
- ✅ Learned mappings file (`phase4b2_learned_mappings.json`)
- ✅ Airtable people export (`../airtable/people_export.csv`)

### Database State
- FathomInventory database has UNIQUE constraint on participant names
- This prevents duplicate names and affects merge logic (see below)

---

## Execution Steps

### 1. Copy CSV to integration_scripts/
```bash
cp ~/Downloads/phase4b2_approvals_*.csv integration_scripts/
```

### 2. Run execution script
```bash
cd integration_scripts
python3 execute_phase4b2_actions.py
```

**What it does:**
- Finds most recent `phase4b2_approvals_*.csv` in directory
- Creates database backup before changes
- Executes merges, drops, and additions
- Commits changes (or rolls back on error)

### 3. Handle custom comments (if script pauses)

If script detects non-standard comments, it will **pause and show flagged items**.

**Standard comment formats:**
- `merge with: Target Name` - Merge with Airtable person
- `drop` - Delete from Fathom database
- `add to airtable - Description` - Add as new Airtable entry
- `ignore` - Skip (not ERA-related)

**To fix:**
1. Review flagged items in output
2. Update CSV with standard format
3. Re-run script

---

## How Execute Script Works

### Merge Logic (UNIQUE Constraint Aware)

The script handles the UNIQUE constraint intelligently:

```python
# If target name already exists in database:
#   → DELETE the duplicate variant (can't UPDATE to duplicate name)
# 
# If target doesn't exist:
#   → UPDATE name to target (safe, no conflict)
```

**Example:**
- Database has: "Brian Von Herzen" (enriched)
- CSV says: merge "Dr Brian von Herzen" → "Brian Von Herzen"
- Action: **DELETE** "Dr Brian von Herzen" (target already exists)

This prevents UNIQUE constraint violations while preserving data.

### CSV Name Cleaning

Script automatically removes emoji badges from names:
- Input: `Aimee Samara (Krouskop)🔁 Organization mapping from earlier round`
- Cleaned: `Aimee Samara (Krouskop)`

### Probe Results (Optional)

The script includes a `process_probe_results()` function with hardcoded probe decisions from earlier investigations:

```python
probe_merges = [
    ("MOSES, GFCCA", "Moses Ojunju"),
    # ... etc
]
```

Update this function if you have new probe results to include.

---

## Common Issues & Solutions

### Issue: UNIQUE Constraint Violation
**Error:** `sqlite3.IntegrityError: UNIQUE constraint failed: participants.name`

**Cause:** Script tried to UPDATE to a name that already exists

**Solution:** ✅ Fixed as of PR #17
- Script now checks if target exists first
- Deletes duplicate instead of UPDATE when target is present

### Issue: Custom Comments Block Execution
**Error:** Script pauses with "CUSTOM COMMENTS - NEED DISCUSSION"

**Cause:** Comments don't match standard patterns

**Solution:**
1. Review flagged items in output
2. Clarify intended action:
   - Phone numbers → `merge with: Person Name`
   - New members → `add to airtable - Name (ERA member)`
   - Not ERA → `ignore`
3. Update CSV to standard format
4. Re-run script

### Issue: Airtable Field Errors
**Error:** `dict contains fields not in fieldnames: 'ERA Africa'`

**Cause:** Airtable CSV export has unexpected fields

**Solution:**
- Note person needs manual Airtable addition
- Track in `FOLLOWUP_REMINDERS.md`
- Add to Airtable manually via web interface

### Issue: No Records Found for Name
**Warning:** `⚠️ No records found for 'PersonName'`

**Cause:** Name in CSV doesn't match database (typo, emoji, or already processed)

**Solution:**
- Check database: `sqlite3 FathomInventory/fathom_emails.db "SELECT name FROM participants WHERE name LIKE '%PartialName%'"`
- Verify CSV name matches database exactly (minus emoji badges)
- If already processed in earlier round, this is expected

---

## Post-Execution

### Verify Results
```bash
sqlite3 FathomInventory/fathom_emails.db "
SELECT 
  COUNT(*) as total,
  SUM(CASE WHEN validated_by_airtable = 1 THEN 1 ELSE 0 END) as enriched,
  SUM(CASE WHEN validated_by_airtable = 0 THEN 1 ELSE 0 END) as remaining
FROM participants"
```

### Archive CSV
```bash
mv integration_scripts/phase4b2_approvals_*.csv \
   integration_scripts/archive/csv_exports/
```

### Update Learned Mappings

As you process more rounds, the learned mappings file accumulates decisions:
- Phone number mappings
- Drop patterns
- Organization → person mappings
- Name corrections

**These are automatically applied in future rounds** to reduce manual review time.

---

## Backup & Recovery

### Automatic Backups
Script creates backup before changes:
```
FathomInventory/backups/fathom_emails.backup_YYYYMMDD_HHMM.db
```

### Restore from Backup
```bash
cp FathomInventory/backups/fathom_emails.backup_YYYYMMDD_HHMM.db \
   FathomInventory/fathom_emails.db
```

### Rollback on Error
Script uses transactions - if any operation fails, **all changes roll back automatically**.

---

## Related Documentation

- **Generate batch:** `generate_batch_data.py` - Creates next 50 people to review
- **Generate table:** `generate_phase4b2_table.py` - Creates HTML approval table with Gmail research
- **Learned mappings:** `apply_learned_mappings.py` - Auto-fill logic from previous rounds
- **Deduplication:** `deduplicate_participants.py` - One-time cleanup of duplicate records
- **Overall workflow:** `README_PHASE4B.md` - High-level Phase 4B process

---

## Tips for Efficient Processing

1. **Review green badges** - Auto-filled from learned mappings, just verify
2. **Use Gmail links** - Click to see email context before deciding
3. **Batch similar decisions** - Process all "drop" entries together, then merges
4. **Add custom notes** - Comments field preserved for context
5. **Mark unclear for probe** - Use "Probe" checkbox for items needing investigation

---

## Workflow Summary

```
┌─────────────────────────────────────────────────────┐
│ 1. Generate batch (50 people)                      │
│    python3 generate_batch_data.py                  │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│ 2. Generate HTML table (with learned mappings)     │
│    python3 generate_phase4b2_table.py              │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│ 3. Review in browser, update comments               │
│    • Auto-filled items have green badges            │
│    • Verify suggestions with Gmail context          │
│    • Export to CSV when done                        │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│ 4. Execute actions (THIS WORKFLOW)                  │
│    cp ~/Downloads/*.csv integration_scripts/        │
│    python3 execute_phase4b2_actions.py             │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│ 5. Verify & commit                                  │
│    • Check database counts                          │
│    • Archive CSV                                    │
│    • Commit to git                                  │
└─────────────────────────────────────────────────────┘
```
