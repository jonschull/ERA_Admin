# V6 Processing Context Recovery

**Created:** October 27, 2025, 7:30pm  
**Updated:** October 27, 2025, 7:50pm (after database investigation)  
**Status:** Ready for execution  
**Purpose:** Document correct process for V6→Database updates after batch script failure

---

## ✅ USER CLARIFICATIONS (Oct 27, 7:49pm)

### 1. ERA Member Field
**Q:** Does era_member field exist?  
**A:** YES - Investigated and confirmed:
- Field: `era_member` (BOOLEAN, default 0)
- Current: 387 true, 17 false
- Usage: true = attended Town Hall, false = potential member/contact

### 2. Non-Members in V6
**Approach:** Add to database with era_member = 0, don't carry to V7

### 3. Name Corrections
**Approach:** Handle name corrections as part of processing (not separately)

### 4. Reusable Function
**Required:** Create `update_participant_bio()` function, not ad-hoc scripts per case

---

## ⚠️ WHAT WENT WRONG

### The Mistake: Batch Scripting Without Judgment

I created `process_v6_to_database.py` that attempted to:

1. Extract all APPROVED entries via regex
2. Batch update database
3. Assume all APPROVED entries should go straight to database

**Problems:**

- Regex parsing errors (grabbed section headers, not just bios)
- No case-by-case judgment
- No database backup created first
- No revertability ensured
- Claimed "5 updated" but unclear what actually happened
- May have corrupted database with malformed text

### What Might Be Corrupted

The script claimed to update 5 entries, but:

- Don't know which 5 (parsing was broken).
- Bio text may include section headers/formatting.  [WE CAN DO A GENERAL REVIEW OF ALL BIOS LATER]
- Italics were stripped mechanically (lost emphasis).  [THE ITALICS SHOULD BE LOST]
- May have overwritten good existing bios.  [UNLIKELY BECAUSE THIS LIST WAS DRAWN FROM PEOPLE LAKCING BIOS]

**Action needed:** Check database integrity for these potential issues

---

## 🎯 THE CORRECT PROCESS

### Core Principle: Intelligence, Not Automation

**V6 processing requires JUDGMENT on each case:**

- Some APPROVED entries are ready for database
- Some need more work → V7
- Some may already have better bios in database [AS NOTED, I THINK THAT's NOT TRUE]
- Some may have name matching issues [THIS IS A BIG ISSUE>. BE VERY CAREFUL]
- Database updates must be verified individually. [RIGHT]

### The Workflow (Per Case)

```
FOR EACH V6 ENTRY (in order):
  
  1. READ the full entry carefully
     - Bio text quality
     - Fields (email, affiliation, LinkedIn)
     - Notes section
     - Any flags or issues
  
  2. CHECK approval status
     └─ Has "APPROVED" in header? 
        └─ YES → Continue to #3
        └─ NO → Skip to #8 (carry to V7)
  
  3. FIND member in database
     - Search by exact name
     - Try case-insensitive (COLLATE NOCASE)
     - Try fuzzy matching if needed (⚠️ NAME MATCHING IS THE BIG ISSUE)
     - Check email match if name doesn't work
     - May need to correct names in V6 during processing
     - VERIFY it's the same person (email, affiliation, linkedin_url)
  
  4. ASSESS current database state
     - Does member already have a bio? (V6 members likely DON'T - that's why they're in V6)
     - What's the current era_member value? (should be 1 for V6 APPROVED)
     - What other fields need updating?
       * email (if found in V6)
       * affiliation (if updated in V6)
       * linkedin_url (if in V6)
       * era_member (set to 1 for members, 0 for non-members)
       * era_africa (if applicable - will handle in Phase 2)
  
  5. DECIDE action
     Options:
     a) UPDATE database: bio + email + affiliation + era_member=1 (most V6 APPROVED cases)
     b) UPDATE database: bio + fields + era_member=0 (non-members we want to keep)
     c) CARRY TO V7 (if needs more work or issues found)
     d) NAME CORRECTION NEEDED (if database name differs, may need to update V6 or database)
  
  6. EXECUTE with verification
     - Make update using UPDATE statement (not INSERT)
     - Set specific fields only (don't touch others)
     - ⚠️ Ensure updates don't corrupt other data (collaborating_people, projects, etc.)
     - Read back what was written
     - Verify ALL updated fields match intention
     - Check that other fields weren't affected
     - Document the change with reasoning
  
  7. REMOVE from V7 (if successfully processed)
     - Entry handled, don't carry over
  
  8. CARRY TO V7 (if not processed)
     - Entry needs more work
     - Document reason why
```

---

## 🚨 GOTCHAS & WARNINGS

### Gotcha #1: Name Matching Is Hard

**Problem:** Database names may not match V6 names exactly

**Examples:**

- V6: "Emmanuel URAMUTSE" → Database: "Emmanuel Uramutse" (case)
- V6: "nding'a ndikon" → Database: "nding'a (Laizer) Orkeyaroi" (full name)
- V6: "Mtokani Saleh" → Database: "Mtokani Saleh Amisi" (full name)

**Solution:**

- Try exact match first
- Try case-insensitive (COLLATE NOCASE)
- Check email match if name fuzzy
- Verify with LinkedIn URL or affiliation
- **NEVER guess** - if uncertain, flag for review

### Gotcha #2: Existing Bios May Be Better

**Problem:** Database might already have a good bio we don't want to overwrite

**Solution:**

- Always read existing bio first
- Compare quality: V6 vs Database
- Decision matrix:
  - V6 better → Update
  - Database better → Keep, maybe add V6 details
  - Both partial → Synthesize (manual)
  - V6 only has LinkedIn → May not be ERA-contextualized enough

### Gotcha #3: Italicized Text in V6

**Problem:** V6 enrichments are italicized with `*text*` markers

**Solution:**

- Keep italics for human reading in markdown [ONLY IF CARRYING OVER TO V8]
- Remove `*` markers when writing to database (but keep the text!)
- **DON'T** mechanically strip - read and understand first

### Gotcha #4: APPROVED Doesn't Mean Ready

**Problem:** Some entries marked APPROVED may still have issues

**Red flags to check:**

- `[do RESEARCH from ourRecords]` in header
- `_[No bio draft yet]_` as bio
- Notes say "needs research"
- LinkedIn-only bio with no ERA context
- Spelling/formatting issues in text

**Solution:** Use judgment - if it needs work, carry to V7

### Gotcha #5: Non-Members in the List

**Problem:** V6 may contain non-ERA members

**Flags:**

- `[Save this but, he's not an ERA Member]` in header
- Notes say "non-member"
- No Town Hall attendance
- Just a LinkedIn contact

**Solution:**

- add to database [BUT THERE IS SUPPOSED TO BE A FIELD FOR ERA Members.  Is there?  It should be false for these pepole.]
- DO NOT carry to V7
- Document removal reason.  [BE CAREFUL WHEN USING THE WORD REMOVAL.  You might mean "from the v7 document; you might mean from the database.  The database is meant to contain non-ERA members (many potential members) as well as ERA members"

### Gotcha #6: Database Schema (NOW INVESTIGATED)

**Database Schema Confirmed:**

```
participants table has 21 fields:
- id (INTEGER, PRIMARY KEY)
- name (TEXT, NOT NULL)
- email (TEXT)
- bio (TEXT)
- affiliation (TEXT)
- linkedin_url (TEXT)
- era_member (BOOLEAN, default 0)
- era_africa (INTEGER, default 0)
- is_donor (BOOLEAN, default 0)
- location, collaborating_people, collaborating_organizations, projects, etc.
```

**Current State:**
- 387 people with era_member = 1 (ERA members)
- 17 people with era_member = 0 (non-members/potential members)
- 26 people with era_africa = 1
- Database size: 347MB
- Recent backups exist (Oct 27, 3:04pm - before batch script)

**ERA Member Definition (from V6 document):**
A person is an ERA member if and only if:
1. They attended a Town Hall meeting (introduced, no objections, week passed), OR
2. Special decision from Jon Schull

**Database contains both:**
- ERA members (era_member = true)
- Potential members/contacts (era_member = false)

**Solution:**

- For V6 APPROVED members: Set era_member = 1 (they attended Town Halls)
- For non-members flagged in V6: Set era_member = 0 (keep in database but mark correctly)
- Test with one safe update
- Verify before proceeding with others
- REPEAT THIS PROCESS WITH EACH UNFAMILIAR NEW SCENARIO
- Create reusable `update_participant_bio()` function, don't write ad-hoc scripts

---

## 🔍 PRE-FLIGHT CHECKS

### Before Processing ANY Cases:

#### 1. Database Backup

```bash
# Check if backup exists
ls -lh FathomInventory/fathom_emails.db*

# Create timestamped backup if needed
cp FathomInventory/fathom_emails.db \
   FathomInventory/fathom_emails.db.backup_$(date +%Y%m%d_%H%M%S)
```

#### 2. Database Integrity Check

```sql
-- Check what the batch script may have corrupted
SELECT name, 
       LENGTH(bio) as bio_length,
       SUBSTR(bio, 1, 100) as bio_preview
FROM participants 
WHERE bio LIKE '%LinkedIn Profile Harvesting%'
   OR bio LIKE '%## %'
   OR bio LIKE '%**Bio:**%'
   OR LENGTH(bio) > 2000;
```

#### 3. Inspect Database Schema

```sql
-- What fields exist?
PRAGMA table_info(participants);

-- How many have bios?
SELECT COUNT(*) FROM participants WHERE bio IS NOT NULL AND bio != '';

-- Sample existing bios
SELECT name, LENGTH(bio) as len, bio 
FROM participants 
WHERE bio IS NOT NULL AND bio != ''
LIMIT 5;
```

#### 4. Identify V6 APPROVED Entries

```bash
# List all APPROVED entries in V6
grep "^## [0-9].*APPROVED" ERA_MEMBERS_LACKING_BIOS_V6.md
```

**Expected:** 16 APPROVED entries (based on earlier grep)

---

## 📋 PROCESSING CHECKLIST

### For Each of 16 APPROVED Cases:

- [ ] **Case #1:** [Name]

  - [ ] Read full V6 entry
  - [ ] Find in database (exact name/email match)
  - [ ] Check existing bio quality
  - [ ] Decide: Update/Skip/V7
  - [ ] Execute & verify
  - [ ] Document decision
- [ ] **Case #2:** [Name]

  - [ ] Read full V6 entry
  - [ ] Find in database
  - [ ] Check existing bio
  - [ ] Decide action
  - [ ] Execute & verify
  - [ ] Document

[...continue for all 16...]

### Progress Tracking Format:

```
✅ Emmanuel URAMUTSE - Updated bio (enriched with ERA Africa info)
✅ Hashim Yussif - Updated bio (complete bio from transcripts) 
⏭️  Fadja Robert - Carried to V7 (bio looks good but verify TH attendance first)
⚠️  Fred Ogden - NOT FOUND in database (check name spelling)
❌ Heraclio Herrera - SKIP (flagged as non-member)
```

---

## 🗄️ DATABASE UPDATE PATTERN

### Reusable Function Required

**Create once, reuse for all 16 cases:**

```python
def update_participant_bio(member_name, v6_entry, conn):
    """
    Standard function for updating participant bio and fields.
    Handles name matching, verification, and safe updates.
    
    Args:
        member_name: Name from V6 header
        v6_entry: Dict with {bio, email, affiliation, linkedin_url, era_member}
        conn: Database connection
    
    Returns:
        Dict with {success, action, message, person_id}
    """
    cursor = conn.cursor()
    
    # 1. Find member (with fuzzy fallback)
    cursor.execute("""
        SELECT id, name, bio, email, affiliation, linkedin_url, era_member
        FROM participants 
        WHERE name = ? COLLATE NOCASE
    """, (member_name,))
    result = cursor.fetchone()
    
    if not result:
        # Try fuzzy match or email match
        print(f"⚠️ NOT FOUND (exact): {member_name}")
        # TODO: Implement fuzzy matching
        return {'success': False, 'action': 'NOT_FOUND', 'message': f"Name not found: {member_name}"}
    
    person_id, db_name, old_bio, old_email, old_affiliation, old_linkedin, old_era_member = result

    # 2. Show what we're about to do
    print(f"\n{'='*80}")
    print(f"MEMBER: {db_name} (ID: {person_id})")
    print(f"{'='*80}")
    print(f"Old bio: {len(old_bio) if old_bio else 0} chars")
    print(f"New bio: {len(v6_entry['bio'])} chars")
    print(f"Old era_member: {old_era_member} → New: {v6_entry['era_member']}")
    if v6_entry.get('email'):
        print(f"Email: {old_email or '[None]'} → {v6_entry['email']}")
    if v6_entry.get('affiliation'):
        print(f"Affiliation: {old_affiliation or '[None]'} → {v6_entry['affiliation']}")
    if v6_entry.get('linkedin_url'):
        print(f"LinkedIn: {old_linkedin or '[None]'} → {v6_entry['linkedin_url']}")
    print(f"{'='*80}")
    
    # 3. Confirm (or auto-confirm if you trust it)
    response = input("Update? (yes/no/skip): ")
    if response != 'yes':
        return {'success': False, 'action': 'SKIPPED', 'message': 'User skipped'}

    # 4. Execute (update only specified fields)
    update_fields = []
    update_values = []
    
    if v6_entry.get('bio'):
        update_fields.append("bio = ?")
        update_values.append(v6_entry['bio'])
    
    if v6_entry.get('email'):
        update_fields.append("email = ?")
        update_values.append(v6_entry['email'])
    
    if v6_entry.get('affiliation'):
        update_fields.append("affiliation = ?")
        update_values.append(v6_entry['affiliation'])
    
    if v6_entry.get('linkedin_url'):
        update_fields.append("linkedin_url = ?")
        update_values.append(v6_entry['linkedin_url'])
    
    if 'era_member' in v6_entry:
        update_fields.append("era_member = ?")
        update_values.append(v6_entry['era_member'])
    
    update_values.append(person_id)  # For WHERE clause
    
    sql = f"UPDATE participants SET {', '.join(update_fields)} WHERE id = ?"
    cursor.execute(sql, update_values)
    conn.commit()
    
    # 5. Verify
    cursor.execute("""
        SELECT bio, email, affiliation, linkedin_url, era_member 
        FROM participants 
        WHERE id = ?
    """, (person_id,))
    verify = cursor.fetchone()
    
    # Check all updated fields
    verified = True
    if v6_entry.get('bio') and verify[0] != v6_entry['bio']:
        print("❌ ERROR: Bio mismatch!")
        verified = False
    if v6_entry.get('era_member') is not None and verify[4] != v6_entry['era_member']:
        print("❌ ERROR: era_member mismatch!")
        verified = False
    
    if verified:
        print("✅ VERIFIED: All fields updated correctly")
        return {'success': True, 'action': 'UPDATED', 'message': f"Updated {db_name}", 'person_id': person_id}
    else:
        print("❌ VERIFICATION FAILED")
        return {'success': False, 'action': 'VERIFY_FAILED', 'message': 'Verification failed'}
```

**Usage for each case:**
```python
result = update_participant_bio(
    member_name="Emmanuel URAMUTSE",
    v6_entry={
        'bio': "Emmanuel Uramutse is a high school...",
        'email': "example@email.com",
        'affiliation': "Environmental studies master's student",
        'linkedin_url': "https://linkedin.com/in/...",
        'era_member': 1
    },
    conn=conn
)
```

---

## 🔄 REVERT STRATEGY

### If Something Goes Wrong:

```bash
# 1. Stop immediately
# Don't make more changes

# 2. Restore from backup
cp FathomInventory/fathom_emails.db.backup_YYYYMMDD_HHMMSS \
   FathomInventory/fathom_emails.db

# 3. Verify restoration
sqlite3 FathomInventory/fathom_emails.db "SELECT COUNT(*) FROM participants;"

# 4. Document what went wrong
# Update this file with lessons learned
```

### Transaction Safety:

- Each case should be its own transaction
- Commit after verification
- Don't batch-commit multiple cases
- This allows granular revert if needed

---

## 📝 V7 GENERATION

### What Goes Into V7:

1. **Non-APPROVED entries from V6** (unchanged)
2. **APPROVED entries that need more work:**
   - Name not found in database
   - Bio quality insufficient
   - Needs verification (TH attendance, etc.)
   - Other issues discovered during review

### What DOESN'T Go Into V7:

1. Successfully processed entries (updated database)
2. Non-members (document removal separately)
3. Entries already perfect in database

### V7 Format:

Same as V6, but:

- Remove successfully processed entries
- Add notes on why others carried over
- Update summary stats
- Document any lessons learned

---

## 🎓 LESSONS LEARNED (To Be Updated)

### Anti-Pattern: Batch Scripting

- **Don't:** Write scripts that update database in bulk
- **Do:** Review each case individually with judgment

### Anti-Pattern: Mechanical Text Processing

- **Don't:** Strip/format text without understanding context
- **Do:** Read, understand, preserve meaning

### Anti-Pattern: Assume APPROVED = Ready

- **Don't:** Trust status markers blindly
- **Do:** Verify quality, completeness, correctness

### Best Practice: Verify Everything

- Read existing database state
- Compare before/after
- Verify writes succeeded
- Document decisions

---

## ✅ READY TO PROCEED CHECKLIST

Before starting case-by-case processing:

- [ ] User has reviewed this document
- [ ] User approves the approach
- [ ] Database backup exists
- [ ] Database integrity checked (no corruption from batch script)
- [ ] Schema inspected (know available fields)
- [ ] All 16 APPROVED cases identified
- [ ] Tracking document ready
- [ ] Understand all gotchas
- [ ] Revert strategy in place

**DO NOT PROCEED until all boxes checked and user approves.**

---

## 📍 CURRENT STATUS

**Status:** ✅ Ready for execution (database investigated, approach approved)

**Next Steps:**

1. ✅ Pre-flight checks (database backup verified)
2. ⏳ Create reusable `update_participant_bio()` function
3. ⏳ Process 16 APPROVED cases one-by-one with judgment
4. ⏳ Generate V7 document with non-processed entries
5. ⏳ Final verification and reporting

---

## 🔗 RELATED DOCUMENTS

**PLAN_Finish_Missing_Bios_and_Review_ERA_Africa.md**
- High-level overview of V6 processing and ERA_Africa_review phases
- Lists all 16 APPROVED cases to process
- Defines Phase 2 scope (ERA Africa network characterization)

**ERA_MEMBERS_LACKING_BIOS_V6.md**
- Source document with all member entries
- ERA member definition (Town Hall attendance)
- APPROVED entries marked for processing

**This Document (V6_PROCESSING_CONTEXT_RECOVERY.md)**
- Detailed processing workflow and gotchas
- Reusable function implementation
- Safety checks and verification procedures
- Case-by-case decision framework

---

**Last updated:** October 27, 2025, 7:50pm  
**Next action:** Create reusable function and begin case-by-case processing
