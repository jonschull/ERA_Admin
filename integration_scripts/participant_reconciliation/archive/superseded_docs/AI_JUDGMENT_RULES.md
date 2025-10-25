# AI Judgment Rules for Phase 4B-2 Reconciliation

**Last Updated:** 2025-10-23 (Batch 1 complete)

## Core Principles

### 1. **Check Airtable FIRST**
❌ **WRONG:** Recommend "add to airtable" without checking
✅ **RIGHT:** Search Airtable people list before recommending add
- If person exists: recommend "merge"
- If similar name (85%+ match): recommend "merge" with note
- Only recommend "add" if truly not in Airtable

**Learned from:** Judith D. Schwartz was already in Airtable as "Judith Schwartz"

### 2. **Device Names + Numbers = Same Person**
❌ **WRONG:** Treat "Lastborn's Galaxy A11" and "Lastborn's Galaxy A11 (3)" as different
✅ **RIGHT:** Recognize both are same device → same person

**Pattern Recognition:**
- `Name` + `Name (2)` + `Name (4)` = same person
- `Device` + `Device (11)` = same device → same person
- Connect ALL variants to the SAME real person

**Learned from:** Missed that both Lastborn's Galaxy entries were Ilarion Merculief

### 3. **Strip Professional Suffixes**
❌ **WRONG:** Add "Kathryn Alexander, MA" with suffix
✅ **RIGHT:** Strip suffix → "Kathryn Alexander"

**Patterns to strip:**
- `, MA` `, PhD` `, MD` `, JD`
- Professional certifications
- Academic degrees

### 4. **Single-Letter Last Names Need Investigation**
⚠️ **UNCERTAIN:** "Kevin A." "Lee G"
- These likely have full last names
- Pre-fill comment: "Need full last name"
- Still recommend "add" but flag for follow-up

### 5. **Town Hall Evidence Must Be Functional**
❌ **WRONG:** Generic Google Doc link that doesn't help
✅ **RIGHT:** Link to specific meeting with anchor/heading

**Requirements:**
- Actual meeting document URLs
- Specific date anchors when possible
- Clear indication of which meeting

### 6. **Always Include Fathom Links**
✅ **MUST:** Every participant should have Fathom recording links
- Query database for call_ids
- Show top 3 most recent
- User wants to see WHO they are

### 7. **Confidence Levels**

**HIGH Confidence** - Auto-approve recommended:
- 3+ Town Hall meetings
- Clear name variants (number suffixes, case changes)
- 85%+ Airtable match
- Well-known community members

**MEDIUM Confidence** - Needs review:
- 1-2 Town Hall meetings
- Partial name matches
- User comments suggest identity
- Some contextual evidence

**LOW Confidence** - Drop or investigate:
- No Town Hall presence
- No Gmail context
- Device names without clear owner
- Generic/incomplete names

### 8. **Merge Patterns**

**Obvious Merges:**
- Number variants: `Name (2)`, `Name (4)`, `Name (7)`
- Case variants: `KALOMBO-MBILIZI` → `Kalombo Mbilizi`
- Spelling variants: `IYAMUREME` → `Iyamuremye`
- Name order: `Mbilizi Kalombo` ↔ `Kalombo Mbilizi`
- Shortened names: `JP` → `John Perlin`, `Lee G` → `Lee Golpariani`

**Check carefully:**
- Similar but different people
- Common names (multiple "John Smith")
- Cultural name variations

### 9. **Drop Criteria**

**Always drop:**
- Device names: "iPhone", "Galaxy", "iPad"
- Test entries
- Clear junk data (admin, phone numbers alone)
- Generic organization names without person

**Organizations → People (from past learnings):**
- `"Organization, Person Name"` → **merge with: Person Name**
  - Example: "Agri-Tech Producers LLC, Joe James" → Joe James
- `"Organization Name"` → Check if person represents it
  - Example: "BioIntegrity" → Chris Searles
  - Look for pattern in previous CSVs or Airtable

**Never drop without investigation:**
- Single names (could be real)
- Unusual names (could be valid)
- Names with some context (even minimal)
- Organizations that might have person identified

### 10. **Pre-fill Guidance**

Pre-fill comment box when:
- Need full name (Kevin A., Lee G)
- Need to verify identity (device names)
- Found similar in Airtable (for user to confirm)
- Unclear context (for user input)

## Mistakes to Avoid

### From Batch 1:

1. ❌ **Missed duplicate device names**
   - Both "Lastborn's Galaxy A11" entries were same person
   - Should have recognized pattern

2. ❌ **Didn't check Airtable first**
   - Judith Schwartz already existed
   - Should query before recommending add

3. ❌ **Generic evidence links**
   - Town Hall links weren't functional
   - User couldn't verify easily

4. ❌ **Missing Fathom links**
   - User wants to see recordings
   - Critical for verification

## Success Patterns

### From Batch 1:

1. ✅ **Recognized number variants**
   - All `(2)`, `(4)`, `(7)` variants correctly merged

2. ✅ **Identified name variants**
   - Jon Schull variants all caught
   - Case changes recognized

3. ✅ **Context-based decisions**
   - Karim → Karim Camara (from Guinea context)
   - Julia → Julia Lindley (from participant list)

4. ✅ **Confidence calibration**
   - HIGH for obvious cases
   - MEDIUM for needing review
   - LOW for drops

## Continuous Improvement

After each batch:
1. Document new patterns learned
2. Update recognition rules
3. Improve evidence gathering
4. Refine confidence thresholds

**Next Review:** After Batch 2
