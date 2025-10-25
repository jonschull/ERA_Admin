# Phase 4B-2: Review Unmatched Participants with Gmail Research

**Goal:** Process 279 unenriched Fathom participants using Gmail research

---

## The 279 People (Categories)

Based on preliminary analysis:

### **Organizations (15)** - Delete
- Global Earth Repair, MOSES GFCCA, sustainavistas, Cosmic Labyrinth, Flip Town, etc.
- **Gmail research confirms:** These are project names, not people
- **Action:** `drop` comment

### **Duplicates/Variants (59)** - Merge
- "Charlie Shore, Gaithersburg, MD" vs "Charlie Shore"
- "Frederic Jennings, www.bio4climate.org" vs "Fred Jennings"
- **Gmail research reveals:** Same person, different Fathom formatting
- **Action:** `merge with: Canonical Name` comment

### **Phone Numbers (2)** - Delete
- "18022588598", "16319034965"
- **Action:** `drop` comment

### **Single Names (27)** - Research then decide
- "Mtokani", "Karim", "Angelique", etc.
- **Gmail research helps:** Find full names or confirm not ERA-related
- **Actions:** `Correct Name: Full Name` or `drop` or `ignore`

### **Full Names (176)** - Research required
- Real people not in Airtable, or misspellings
- **Gmail research critical:** Find context, emails, relationships
- **Actions:** 
  - `add to airtable` (real ERA person, needs entry)
  - `merge with: Existing Name` (spelling variant)
  - `drop` (contamination from non-ERA meetings)
  - `ignore` (real person but not ERA-related)

---

## Workflow Design

### **Phase A: Generate Enhanced Approval Table**

**Script:** `phase4b2_review_unmatched.py`

**Generates HTML table with:**
```
| Fathom Name | Videos | Gmail Emails | Email Context | Category Hint | Comments | Action |
```

**Features:**
1. **Pre-categorized** - Script auto-categorizes (org/duplicate/phone/name/full)
2. **Gmail button** - "Research in Gmail" button per person (calls gmail_research.py)
3. **Email preview** - Shows count + top email snippet inline
4. **Smart hints** - Suggests likely action based on category
5. **Sortable/filterable** - By category, email count, etc.

---

### **Phase B: Collaborative Review (Human + AI)**

**For each batch of ~20 people:**

1. **Human opens HTML table**
2. **For unclear cases:**
   - Human asks: "Who is 'Mtokani'?"
   - AI clicks "Research Gmail" → Shows email results
   - AI: "Found 6 emails, seems to be Mtokani Saleh, active in meetings"
   - Human: "Check if 'Mtokani Saleh' is already in list"
   - AI: "Yes! It's on the list as enriched. This is a duplicate."
   - Human adds comment: `merge with: Mtokani Saleh`

3. **Discuss edge cases:**
   - "Should we add this person to Airtable?"
   - "Is this person ERA-related or contamination?"
   - Gmail context helps make informed decisions

4. **Human fills out table:**
   - Check Action boxes (✓ for process, ✗ for review later)
   - Add Comments with keywords
   - Export to CSV

---

### **Phase C: Process Decisions**

**Script:** `process_unmatched_decisions.py`

**Reads CSV and executes:**

1. **DELETE** (comment: `drop`)
   - Remove from Fathom database completely

2. **MERGE** (comment: `merge with: Target Name`)
   - UPDATE Fathom: rename all records from "Old Name" to "Target Name"
   - Mark as `validated_by_airtable = 1` if Target is enriched

3. **NAME CORRECTION** (comment: `Correct Name: Full Name`)
   - UPDATE Fathom: rename to correct spelling
   - Re-run fuzzy match to see if now matches Airtable

4. **ADD TO AIRTABLE** (comment: `add to airtable`)
   - Generate CSV row for Airtable import
   - Mark for manual Airtable entry (Phase 4B-3)

5. **IGNORE** (comment: `ignore`)
   - Mark as reviewed but not ERA-related
   - Skip in future processing

---

## Implementation Plan

### **Week 1: Build Tools**

**Day 1-2:** Enhanced approval table generator
- Load 279 unenriched participants
- Auto-categorize using patterns
- Pre-run Gmail research (async, cache results)
- Generate HTML with Gmail insights

**Day 3:** Gmail integration
- Add "Research" button that shows cached results
- Format email contexts nicely
- Add "Refresh Research" option

**Day 4:** Decision processor
- Parse CSV actions
- Implement delete/merge/rename/ignore logic
- Safe transactions with rollback

**Day 5:** Testing & refinement
- Test on 20-person batch
- Fix UX issues
- Iterate on workflow

---

### **Week 2: Process 279 People**

**Batch approach:**
- Process ~30 people per session
- Review → Discuss → Export → Process
- Iterate until all 279 done

**Categories order:**
1. Organizations (15) - Easy, just delete
2. Phone numbers (2) - Easy, just delete  
3. Duplicates (59) - Medium, merge with enriched names
4. Single names (27) - Hard, research required
5. Full names (176) - Mix of hard cases

**Expected results:**
- ~50 deleted (orgs, junk, contamination)
- ~60 merged (duplicates, variants)
- ~20 renamed (spelling corrections)
- ~50 ignored (not ERA-related)
- ~100 candidates for "add to airtable" (Phase 4B-3)

---

## Technical Details

### **Auto-categorization Logic**

```python
def categorize_person(name):
    if contains_org_keywords(name):  # Global, Earth, Labyrinth, Town, etc.
        return "organization"
    if is_phone_number(name):
        return "phone"
    if has_location_suffix(name):  # ", MD", ", www."
        return "duplicate"
    if is_single_name(name):  # No spaces
        return "single_name"
    return "full_name"
```

### **Gmail Research Caching**

```python
# Pre-run research on all 279 people (takes ~10 minutes)
# Cache results in JSON file
# Load into HTML table for instant display
cache = {
    "Mike Lynn": {
        "email_count": 3,
        "top_snippet": "Panama Restoration Lab meetings...",
        "emails": [...]
    }
}
```

### **Merge Logic**

```sql
-- Merge "Charlie Shore, MD" into "Charlie Shore"
BEGIN TRANSACTION;

UPDATE participants 
SET name = 'Charlie Shore'
WHERE name = 'Charlie Shore, Gaithersburg, MD';

-- If target is enriched, mark merged records as validated
UPDATE participants
SET validated_by_airtable = 1
WHERE name = 'Charlie Shore' 
  AND validated_by_airtable IS NULL;

COMMIT;
```

---

## Success Criteria

### **Quality Metrics**
- < 5% false negatives (missed ERA people)
- < 1% false positives (kept non-ERA contamination)
- All decisions documented with rationale

### **Efficiency Metrics**
- Process 279 people in < 10 hours total human time
- < 30 minutes per batch of 30 people
- Gmail research reduces uncertainty by 80%

### **Outcome**
- Clean Fathom database with only ERA-related, enriched entries
- List of ~100 candidates to add to Airtable (Phase 4B-3)
- Documented decisions for audit trail

---

## Next Actions

### **Immediate (Today)**
1. ✅ Commit Gmail research tool
2. ✅ Create this plan
3. ⏭️ Test on 20-person sample batch

### **This Week**
1. Build `phase4b2_review_unmatched.py` (approval table generator)
2. Build `process_unmatched_decisions.py` (decision processor)
3. Pre-run Gmail research cache
4. Test workflow on sample

### **Next Week**
1. Process all 279 in batches
2. Generate "add to airtable" candidate list
3. Prepare for Phase 4B-3

---

**Status:** Planning complete, ready to build  
**Owner:** Jon Schull + Claude  
**Est. Completion:** 2 weeks from start
