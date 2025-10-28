# Batch 5 Learnings

**Date:** October 26, 2025  
**Bios Reviewed:** 6 (Leticia, Mahangi, Sandra, Scott, Alfredo, Ilana)  
**Method:** AI generated → Human edited → Diff analysis → Rule extraction

---

## Editorial Patterns Identified

### 1. Check ERA Membership Status
**Pattern:** Alfredo Quarto flagged "[NOT AN ERA MEMBER]"  
**AI Miss:** Database shows `"era_member": false` - I should have caught this myself  
**Rule:** Always check `era_member` field before writing bio. Flag non-members for review.

**Example:**
- ❌ AI: Wrote bio without checking membership status
- ✅ Human: Flagged "[NOT AN ERA MEMBER]" in header

**New check:**
```python
if data['database']['era_member'] == False:
    FLAG: "Not an ERA member - skip or note membership status?"
```

---

### 2. Fuzzy LinkedIn Matching Can Fail
**Pattern:** Scott Edmundson - automated 81% match was completely wrong person  
**Reality:** Human found correct LinkedIn manually  
**Rule:** Be skeptical of fuzzy matches <90%, flag for manual verification

**Example:**
- ❌ AI: "Scott Hudson" (81% fuzzy match) - completely wrong
- ✅ Human: Found https://www.linkedin.com/in/scott-edmundson-91865935/

**New threshold:**
- <85%: High risk, likely wrong
- 85-90%: Medium risk, flag for verification
- >90%: Generally reliable but still verify

---

### 3. Add Member Connections When Known
**Pattern:** Sandra Garcia - added collaboration with Indy Rishy Singh  
**Question:** How to discover these connections proactively?

**Example:**
- AI: "based in the San Jose Bay Area."
- Human: "based in the San Jose Bay Area **who collaborates with ERA Member Indy Rishy Singh.**"

**Open questions:**
1. Is this from transcripts (co-mentions)?
2. From user's personal knowledge?
3. Should I search for co-attendance/co-mentions automatically?

---

### 4. Use Their Own Words (Don't AI-Rewrite)
**Pattern:** Scott's bio adopted LinkedIn verbatim  
**Learning:** If LinkedIn is only source, use their words—don't paraphrase unnecessarily

**Example:**
- ❌ AI (first attempt): "environmental and climate research" (generic AI rewrite)
- ✅ Human-corrected: Used LinkedIn About section directly with their specific skills

**Rule:** When LinkedIn is the only substantive source and it's well-written, use it verbatim or lightly edited. Don't "AI-wash" their self-description.

**When to synthesize vs. use verbatim:**
- **Synthesize:** When you have multiple sources (transcripts + LinkedIn + database) and can add ERA-specific context
- **Verbatim:** When LinkedIn is only source and you have nothing meaningful to add

---

## Changes Applied to Each Bio

### Leticia Bernardes
- ✅ No changes (approved as-is)

### Mahangi Munanse
- ✅ No changes (correctly flagged as insufficient data)

### Sandra Garcia (1 change)
- Added: "who collaborates with ERA Member Indy Rishy Singh"

### Scott Edmundson (MAJOR REVISION)
- Found correct LinkedIn (automated match failed)
- Rewrote entire bio with specific expertise:
  - Algae cultivation
  - Interdisciplinary ecology (MS from UF)
  - Plant sciences background
  - Organic agriculture, philosophy of science
- Increased from 285 → 523 chars with actual substance

### Alfredo Quarto
- Flagged: "[NOT AN ERA MEMBER]"
- AI should have caught `era_member: false`

### Ilana Milkes
- ✅ No changes (approved as-is)

---

## Rules to Apply Going Forward

### ✅ BEFORE WRITING BIO, CHECK:

1. **Membership status**
   ```
   if era_member == false:
       FLAG for review or skip
   ```

2. **LinkedIn match quality**
   ```
   if fuzzy_score < 90:
       FLAG as "uncertain match - verify manually"
   ```

3. **Affiliated org IDs**
   ```
   if org shows as "recXXXXX":
       Look up actual org name
   ```

### ✅ WHEN WRITING BIO:

1. **Respect their own words**
   - If LinkedIn is only source: use verbatim or lightly edited
   - Don't AI-rewrite unless you can add value
   - Only synthesize when you have multiple sources + ERA context

2. **Use specific skills from LinkedIn**
   - NOT: "environmental research"
   - YES: "algae cultivation, interdisciplinary ecology"

3. **Note member connections if known**
   - Collaborations, co-projects
   - But unclear how to discover these proactively

4. **Be honest about data limitations**
   - "INSUFFICIENT DATA" when appropriate
   - Conservative when only database description available

---

## New Questions Raised

### Question 1: Member Connections
How should I discover collaborations like Sandra/Indy?
- **Option A:** Search transcripts for co-mentions
- **Option B:** Rely on human to add them
- **Option C:** Ask explicitly when writing bio

### Question 2: Non-Members Policy
What to do with non-members in database?
- **Option A:** Skip entirely
- **Option B:** Write bio but note non-member status
- **Option C:** Flag for human decision (current approach)

### Question 3: LinkedIn Search Strategy
When fuzzy match fails, should I:
- **Option A:** Flag for manual search (current approach)
- **Option B:** Try alternate search patterns (first name + employer)
- **Option C:** Note limitation and proceed without LinkedIn

---

## Impact on Future Batches

**Batch 6+ should:**
1. Check `era_member` field before writing
2. Flag fuzzy matches <90% as uncertain
3. **Use LinkedIn verbatim when it's the only source** (don't AI-rewrite)
4. Only synthesize when multiple sources + ERA context to add
5. Note when automated matching fails
6. Continue conservative approach when data limited

**This should result in:**
- Fewer non-member bios slipping through
- Fewer wrong LinkedIn matches
- More authentic bios (their words, not AI paraphrase)
- Better value-add (only rewrite when we have something to contribute)
- Clearer flagging of data quality issues

---

## Files Updated

- `batch5_review.AI.md` - Updated Scott's bio with correct LinkedIn
- `batch5_review.JS.md` - Human edits + Scott revision
- `BATCH5_LEARNINGS.md` - This document

---

## Success Metrics

**Batch 4 → Batch 5 improvements:**
- ✅ Applied all Batch 4 rules (no "leads", no TH mentions, timeless)
- ✅ Correctly flagged insufficient data (2 members)
- ✅ Conservative bios when limited data
- ❌ Missed non-member flag (need new check)
- ❌ LinkedIn fuzzy match failed (need better validation)

**Overall:** 4 good bios, 2 correctly flagged as insufficient, 1 major learning (check membership), 1 process improvement (validate fuzzy matches)
