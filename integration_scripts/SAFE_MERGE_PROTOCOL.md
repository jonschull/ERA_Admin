# Safe Merge Protocol for Database Participants

## The Problem

The `participants` table has a `UNIQUE(name)` constraint, meaning each person can only have ONE record. However, people may attend multiple Town Halls, with attendance stored in a comma-separated `source_call_url` field.

**Unsafe operations risk losing Town Hall attendance data.**

---

## Common Scenarios Requiring Merges

1. **Name variants**: "Jake Kelley" vs "Jake Fairbanks Kelley"
2. **Organization vs person**: "Cosmic Labyrinth" vs "Indy Singh"
3. **Username vs real name**: "afmiller09" vs "Andrea Miller"
4. **Device name vs person**: "Samsung SM-N986U" vs "Edward Paul Munaaba"
5. **Spelling differences**: "Sanmi Olowosile" vs "Olowwosile Sanmi"

---

## ❌ UNSAFE: What NOT To Do

### Anti-Pattern 1: Direct Rename
```python
# BAD - Fails if canonical name already exists
cursor.execute("UPDATE participants SET name = ? WHERE name = ?", 
               (canonical_name, duplicate_name))
# Error: UNIQUE constraint failed: participants.name
```

### Anti-Pattern 2: Direct Delete
```python
# BAD - Loses Town Hall attendance data!
cursor.execute("DELETE FROM participants WHERE name = ?", (duplicate_name,))
# Lost: All unique calls this person attended
```

### Anti-Pattern 3: Merge Without Checking
```python
# BAD - No verification of what data exists
cursor.execute("DELETE FROM participants WHERE name = ?", (old_name,))
# Unknown: Did we lose unique attendance records?
```

---

## ✅ SAFE: The Correct Approach

### Use `merge_participant_safely.py`

**Location:** `/Users/admin/ERA_Admin/integration_scripts/merge_participant_safely.py`

**What It Does:**
1. Checks both names exist in database
2. Extracts call attendance from duplicate
3. Compares with canonical name's attendance
4. Identifies unique calls duplicate attended
5. Merges unique calls to canonical's `source_call_url`
6. Verifies merge before deleting duplicate
7. Reports what data was preserved

**Usage:**

```bash
# DRY RUN (always do this first)
python merge_participant_safely.py "Duplicate Name" "Canonical Name"

# Reviews shows:
# - Current attendance for both names
# - Which calls are unique to duplicate
# - What will be merged
# - Safe to proceed or not

# EXECUTE (after reviewing dry run)
python merge_participant_safely.py "Duplicate Name" "Canonical Name" --execute
```

**Example Output:**

```
================================================================================
MERGING: Jake Fairbanks Kelley → Jake Kelley
================================================================================

CURRENT STATE:
--------------------------------------------------------------------------------
Jake Fairbanks Kelley:
  Bio: 0 chars
  Email: (none)
  Airtable ID: (none)
  ERA member: True

Jake Kelley:
  Bio: 2434 chars
  Email: jake@example.com
  Airtable ID: rec123
  ERA member: True

Jake Fairbanks Kelley: 1 call record(s)
Jake Kelley: 1 call record(s)

📝 Will copy bio from Jake Fairbanks Kelley
📧 Will copy email: jake@example.com
✅ Will set ERA member to True

🔍 DRY RUN - No changes made

To execute, run with dry_run=False
```

---

## The Safe Merge Algorithm

```python
def safe_merge(duplicate_name, canonical_name):
    """
    Safe merge preserving all data.
    """
    # 1. Get duplicate's call URLs
    old_urls = get_source_call_url(duplicate_name)
    
    # 2. Get canonical's call URLs
    canon_urls = get_source_call_url(canonical_name)
    
    # 3. Find unique URLs in duplicate
    old_list = parse_csv_urls(old_urls)
    canon_list = parse_csv_urls(canon_urls)
    unique_urls = [u for u in old_list if u not in canon_list]
    
    # 4. Merge unique URLs to canonical
    if unique_urls:
        merged_urls = canon_urls + ', ' + ', '.join(unique_urls)
        UPDATE canonical SET source_call_url = merged_urls
    
    # 5. Merge other fields (bio, email, etc.) if better
    # (Only if duplicate has data canonical doesn't)
    
    # 6. Delete duplicate ONLY after successful merge
    DELETE FROM participants WHERE name = duplicate_name
    
    # 7. Verify
    ASSERT count(duplicate_name) == 0
    ASSERT canonical has all calls from both names
```

---

## Data Loss Prevention Checklist

Before ANY delete operation:

- [ ] Have you backed up the database?
- [ ] Have you checked if the record has unique call attendance?
- [ ] Have you verified the canonical name exists?
- [ ] Have you compared data between duplicate and canonical?
- [ ] Have you tested with dry run first?
- [ ] Have you verified the merge result?

**If you answered NO to any question: STOP. Use `merge_participant_safely.py`.**

---

## Database Schema Reference

```sql
CREATE TABLE participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL COLLATE NOCASE,
    
    -- Multiple calls stored as CSV
    source_call_url TEXT NOT NULL,
    call_hyperlink TEXT,
    
    -- Other fields
    bio TEXT,
    email TEXT,
    airtable_id TEXT,
    
    -- UNIQUE constraint - only ONE record per name
    UNIQUE(name COLLATE NOCASE)
);
```

**Key Points:**
- `UNIQUE(name)` prevents duplicate names
- `source_call_url` is comma-separated (can be multiple calls)
- Simple UPDATE fails if target name exists
- Simple DELETE loses `source_call_url` data

---

## Real Examples from Oct 26, 2025 Session

### ❌ What Went Wrong

**Unsafe merges performed:**
- Deleted "Jake Fairbanks Kelley" without checking unique calls
- Deleted 6 duplicates via script without verifying data
- Lost 7 unique Town Hall attendance records

**Result:** Had to recover from backup, manually restore lost attendance.

### ✅ What We Should Have Done

```bash
# For each duplicate:
python merge_participant_safely.py "Jake Fairbanks Kelley" "Jake Kelley"
# Reviews, shows unique calls
# --execute only after review

python merge_participant_safely.py "Cosmic Labyrinth" "Indy Singh"
# Shows organization → person merge
# Preserves attendance data
```

---

## Recovery from Unsafe Merges

If you've already done unsafe deletes:

1. **Check last backup:**
   ```bash
   ls -lht FathomInventory/fathom_emails*.db | head -5
   ```

2. **Extract deleted records:**
   ```bash
   sqlite3 backup.db "SELECT * FROM participants WHERE name = 'Deleted Name'"
   ```

3. **Use restore script:**
   ```bash
   python restore_lost_attendance.py
   ```

**Script:** `/Users/admin/ERA_Admin/integration_scripts/restore_lost_attendance.py`

---

## Best Practices

1. **Always backup before bulk operations**
   ```bash
   cp fathom_emails.db "fathom_emails_BACKUP_$(date +%Y%m%d_%H%M%S).db"
   ```

2. **Use safe merge script for ALL duplicates**
   - Even if you think it's "simple"
   - Even if names don't conflict
   - Better safe than sorry

3. **Dry run first, execute after review**
   - Never skip the dry run
   - Verify what will happen
   - Then execute

4. **Document merge decisions**
   - Keep CSV of merges performed
   - Note why names were considered duplicates
   - Reference in PAST_LEARNINGS

5. **Test on backup first**
   - For large batch operations
   - Copy database, test merge
   - Verify results before production

---

## Automation Considerations

**For future automation:**

```python
# Good pattern for batch merges:
merges = load_merge_decisions_csv()

for duplicate, canonical in merges:
    # Run safe merge with logging
    result = safe_merge(duplicate, canonical, dry_run=False)
    
    # Log result
    log_merge(duplicate, canonical, result)
    
    # Verify after each
    assert_merge_success(duplicate, canonical)
```

**Never:**
- Batch DELETE without verification
- Skip dry runs in automation
- Trust merge decisions without data checks

---

## Related Documentation

- **Session Summary:** `integration_scripts/member_enrichment/BIO_SYNC_SESSION_SUMMARY.md`
- **PAST_LEARNINGS:** `integration_scripts/participant_reconciliation/PAST_LEARNINGS.md`
- **Safe Merge Script:** `integration_scripts/merge_participant_safely.py`
- **Recovery Script:** `integration_scripts/restore_lost_attendance.py`

---

**Last Updated:** Oct 26, 2025  
**Author:** Claude (after making this mistake and learning from it)  
**Reviewed By:** User (after catching the mistake and guiding recovery)
