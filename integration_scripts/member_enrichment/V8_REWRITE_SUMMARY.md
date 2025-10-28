# V8 Rewrite Summary - New Paradigm

**Date:** October 28, 2025
**Action:** Complete paradigm shift from Airtable-centric to Fathom DB-centric

---

## Major Changes Made

### 1. Paradigm Shift: Sources of Truth

**OLD (incorrect):**
- Airtable = Primary source of truth
- Fathom DB = Secondary (bio storage)

**NEW (correct):**
- **Fathom Database** = Primary source of truth for current membership
- **Legacy Airtable** = Historical snapshot (past truth, use for cross-checking)
- **Future: New Airtable** = Will mirror Fathom DB as user-friendly interface

### 2. Database Update

**Mary Ann Edwards:**
- Found in Legacy Airtable with "Author" affiliation
- Added to Fathom DB:
  - Name: Mary Ann Edwards
  - Email: maedwardsrn@gmail.com
  - Bio: "Mary Edwards maintains a food forest in her yard in Irondequoit, New York."
  - Affiliation: Author
  - era_member: 1
  - source_call_url: 'legacy_airtable'
  - source_call_title: 'Legacy Airtable Import'
  - data_source: 'legacy_airtable'

### 3. Critical Distinctions Updated

- **ERA Member** = era_member=1 in Fathom DB (not "in Airtable")
- **Legacy Airtable Member** = New category: Person with bio in old Airtable; likely was a member
- Clarified that Legacy Airtable doesn't have era_africa flag (Fathom DB improvement)

### 4. Workflow Changes

**Research Priority Order:**
1. Check **Fathom Database first** (not Airtable)
2. Search Town Hall transcripts
3. Check **Legacy Airtable** (for historical context)
4. Check emails, LinkedIn, web
5. Use Fathom API for deep dives

**Database Updates:**
- Must record provenance information (new requirement)
- Document changes in version notes

### 5. Provenance Tracking (HIGH PRIORITY)

**New schema fields proposed:**

```sql
ALTER TABLE participants ADD COLUMN provenance_source TEXT;
ALTER TABLE participants ADD COLUMN provenance_date TIMESTAMP;
ALTER TABLE participants ADD COLUMN provenance_added_by TEXT;
ALTER TABLE participants ADD COLUMN provenance_notes TEXT;  -- For social connections!
ALTER TABLE participants ADD COLUMN provenance_verification_status TEXT;
```

**Examples of provenance_notes:**
- "Invited by Russ Speer"
- "Presenter at Town Hall 2024-03-05"
- "ERA Africa attendee"
- "Board member"
- "Founding member"

### 6. Major New Section: Legacy Airtable → Fathom DB Reconciliation

**Goal:** Ensure all historical members from Legacy Airtable are in Fathom DB

**Three phases:**
1. **Discovery** - Query Legacy Airtable for members with bios, cross-check Fathom DB
2. **Verification** - Determine if still active/relevant
3. **Migration** - Add to Fathom DB with provenance tracking

**Expected findings:**
- True members not yet migrated (like Mary Ann Edwards)
- Inactive/past members (document decision)
- Batch 5 mystery solved (correctly in Fathom DB, never in old Airtable)
- Data quality issues

### 7. Workflow Type B Added

**NEW workflow for "Legacy Airtable Members Not Yet in Fathom DB":**
- Cross-check if still active
- If active: migrate to Fathom DB with bio
- Priority: High (data migration)
- Record provenance: "legacy_airtable"

### 8. Database Validation Updated

**OLD:** "Anyone in Airtable should have era_member=1 in Fathom"

**NEW:** "Anyone in Legacy Airtable with bio should be checked against Fathom DB"

Plus new checks:
- Flag members with provenance_source=NULL
- Check: Legacy Airtable count vs Fathom DB era_member=1 count

### 9. Terminology Consistency

Throughout document:
- "Airtable" → "Legacy Airtable" (for old one)
- "New Airtable" (for future mirror)
- Emphasized Fathom DB as authoritative

### 10. Key Learnings Section Updated

**Added:**
- Legacy Airtable members may not be in Fathom DB yet
- Fathom DB participants may not be in Legacy Airtable (Batch 5 example)
- "In Legacy Airtable with bio" = strong signal they WERE a member
- Fathom DB is authoritative for CURRENT membership

---

## User Amendments Incorporated

1. ✅ Clarified Myra's "ERA" = Earth Regeneration Alliance (not generic ERA)
2. ✅ Crossed out "Check Airtable first" in workflow
3. ✅ Added Fathom API date-range trick note
4. ✅ Emphasized "never update speculatively or impulsively"
5. ✅ Added future naming convention note (VN_datetime)
6. ✅ Strengthened "AI must READ user edits intelligently"
7. ✅ Updated ERA Africa language ("not yet ERA members" → clearer distinctions)

---

## Remaining Work in V8

**5 members still need resolution:**

1. **Lauren Miller** - Remove from database
2. **Malaika Patricia** - Verify ERA Africa vs ERA member flags
3. **Stella Nakityo** - ERA Africa, minimal info
4. **Munyembabazi Aloys** - ERA Africa, minimal info
5. Status verification for Malaika

**1 member resolved:**
- ✅ Mary Ann Edwards - Added to Fathom DB

---

## Next Immediate Actions

1. Remove Lauren Miller from Fathom DB
2. Confirm ERA Africa attendee flags
3. Begin Legacy Airtable reconciliation project
4. Consider implementing provenance tracking schema

---

## Document Status

✅ **V8 fully rewritten with new paradigm**
✅ **All Airtable references corrected to "Legacy Airtable"**
✅ **Fathom DB positioned as primary source of truth**
✅ **Provenance tracking expanded with social connections field**
✅ **Major reconciliation project documented**
✅ **Consistent terminology throughout**

The document now accurately reflects reality: Fathom DB is our current source of truth, Legacy Airtable is historical data for cross-checking, and we're working toward a New Airtable that mirrors Fathom DB.
