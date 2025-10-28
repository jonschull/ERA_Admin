# Batch Bio Review Workflow

**Pattern:** AI writes batch → Human reviews → AI processes feedback

---

## Workflow

### Step 1: Generate Batch (AI)

User tells Claude: "Generate batch 4 bios for: [6 names]"

Claude:
1. Reads aggregated data for each member
2. Writes bio following standards (600-950 chars)
3. Creates `batch4_review.md` with all 6 bios

Output: Single file with 6 bio review sections

---

### Step 2: Review Batch (Human)

Human opens `batch4_review.md` and for each bio:

**Edit bio directly** (in place)
**Mark status:**
- `STATUS: APPROVED` - Ready for Airtable
- `STATUS: NEEDS_REVISION` - See comments
- `STATUS: SKIP` - Don't add to Airtable

**Add comments:**
```
## COMMENTS
- Change "consultant" to "advisor"
- Add mention of XYZ project
- Too long, trim by 100 chars
```

Save file when done.

---

### Step 3: Process Feedback (AI)

User tells Claude: "Process batch 4 feedback"

Claude:
1. Reads `batch4_review.md`
2. Finds all edits (compares char counts, looks for COMMENTS sections)
3. For APPROVED bios:
   - Adds to `approved_bios.md`
   - Queues for Airtable update
4. For NEEDS_REVISION:
   - Applies edits from comments
   - Re-submits for review
5. For SKIP:
   - Notes reason, skips

Output: `batch4_approved.md` ready for Airtable update

---

## File Structure

```
batches/
  batch_reviews/
    batch4_review.md       ← AI creates, Human edits
    batch4_approved.md     ← AI creates from approved items
    batch4_queue.json      ← Ready for Airtable
  approved_bios.md         ← Running collection of all approved
```

---

## Example Review Section

```markdown
## 1. Jacob Denlinger

**STATUS:** APPROVED

### Bio (835 chars)

Jacob Denlinger is a junior at Brophy College Preparatory...

### Contact Info
- Email: jdenlinger26@brophybroncos.org
- Location: Phoenix, Arizona
- Phone: 480 299 0865

### Affiliated Orgs
- Brophy College Preparatory
- EcoRestoration Alliance

### Data Concerns
- LinkedIn shows Jun 2024 start, transcripts show July 2024
- All sources align well

### Comments
(none - looks good)

---
```

Human can edit bio, change status, add comments all in one place.
