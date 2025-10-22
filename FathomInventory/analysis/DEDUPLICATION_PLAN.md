# Participant Deduplication Plan

## Problem
FathomInventory creates one record per person per meeting, leading to massive duplication:
- Jon Schull: 186 records
- Leonard Iyamuremye: 65 records
- Philip Bogdonoff: 60 records

**Result:** 2,507 records for only 696 unique people (1,811 duplicates!)

## Root Cause
1. **Import design:** Creates one record per (name, meeting) combination
2. **No constraint:** Database allows unlimited duplicate names
3. **Daily automation:** Cron job runs analysis → import every day

## Solution

### Step 1: Deduplicate Existing Data (ONE-TIME)

**Run:**
```bash
cd /Users/admin/ERA_Admin/integration_scripts
python3 deduplicate_participants.py --execute
```

**What it does:**
- Backs up database first
- For each unique name (case-insensitive):
  - Keeps enriched record if exists, otherwise earliest
  - Merges all source_call_urls (comma-separated)
  - Deletes duplicates
- Result: 2,507 → 696 unique records

### Step 2: Add Database Constraint (PREVENTS FUTURE)

**Option A: UNIQUE Constraint on Name (RECOMMENDED)**

```bash
cd /Users/admin/ERA_Admin/FathomInventory/analysis
sqlite3 ../fathom_emails.db < add_unique_constraint.sql
```

**Effect:**
- Database enforces ONE record per unique name
- Future imports will UPDATE existing record instead of INSERT
- source_call_urls automatically merged

**Option B: Modify Import Logic**

Change `import_new_participants.py` to:
```python
# Check if NAME already exists (not just name+url combo)
cursor.execute("SELECT id FROM participants WHERE LOWER(TRIM(name)) = ?", 
               (p['Name'].lower().strip(),))
existing = cursor.fetchone()

if existing:
    # UPDATE: append new source_call_url
    cursor.execute("""
        UPDATE participants 
        SET source_call_url = source_call_url || ', ' || ?
        WHERE id = ?
    """, (p['Source_Call_URL'], existing[0]))
else:
    # INSERT: new person
    cursor.execute("INSERT INTO participants (...) VALUES (...)")
```

## Recommendation

**Use Option A (UNIQUE constraint)** because:
- ✅ Database-level enforcement (foolproof)
- ✅ Works even if import scripts have bugs
- ✅ Automatic INSERT → UPDATE behavior
- ✅ No code changes needed

## Execution Plan

1. **Backup current database** (automatic in step 1)
2. **Run deduplication script** → 696 unique records
3. **Apply UNIQUE constraint** → prevents future duplicates
4. **Test:** Run import again, verify no duplicates created
5. **Monitor:** Check participant count stays reasonable

## Testing

After applying constraint, test with:
```bash
cd /Users/admin/ERA_Admin/FathomInventory/analysis
python3 import_new_participants.py
```

Should see: "UNIQUE constraint failed" OR automatic UPDATE behavior.

## Rollback

If something goes wrong:
```bash
# Restore from backup
cp FathomInventory/fathom_emails.db.backup_before_dedup_TIMESTAMP \
   FathomInventory/fathom_emails.db
```

## Next Steps

After deduplication:
1. ✅ Continue Phase 4B-2 with clean 696 unique people
2. ✅ ~200 remaining to enrich (not 1,314!)
3. ✅ Much faster reconciliation process
