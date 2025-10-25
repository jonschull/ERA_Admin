# Phase 4B: Collaborative Fathom-Airtable Reconciliation

**Human + AI working together to match, verify, and enrich people data across systems.**

---

## What We're Solving

**The Situation:**

- Fathom has 650+ video call participants (AI-generated names like "Myhan", "Abdulganiyu Jimoh")
- Airtable has 590+ ERA members (verified: "Moo Young Han", "Logan")
- Many Fathom names are misspelled or ambiguous

**The Goal:**
Link each Fathom participant to their correct Airtable identity, enrich Fathom with authoritative data.

**The Challenge:**
Fuzzy matching isn't perfect. Humans need to verify, and humans need AI help researching unfamiliar names.

---

## The Collaborative Workflow

### **Phase 4B-1: Match Clear Cases** ✅ COMPLETE

**1. AI Proposes Matches**

```bash
python3 phase4b1_enrich_from_airtable.py
```

- Fuzzy matches Fathom → Airtable (80% threshold)
- Generates sortable HTML table
- Shows: Fathom name | Video links | Airtable match | Score | Member/Donor flags

**2. Human Reviews in Browser**

- Click video links (🎥) to verify identities
- Sort by score/name/comments
- Check ☑ to approve good matches
- Uncheck ☐ for bad matches
- Add comments: `drop`, `Correct Name: ...`, `needs reunion`, etc.

**3. Human Exports Decisions**

- Click "📥 Export to CSV" button
- Saves all decisions + comments

**43. Human & AI Discuss (via Chat)**

- "This 'Abdulganiyu Jimoh' matched to 'Logan' at 80% - that's wrong"
- AI: "Got it, I'll mark those as 'drop' - they're bad fuzzy matches"
- Human adds comments in HTML table

**5. AI Processes Approved Actions by revising process_approved_matches.py or engaging in AI-manual operations.**

for example....

```bash
python3 process_approved_matches.py
```

- Reads CSV
- Deletes entries marked `drop`
- Enriches approved matches with Airtable data
- Updates Fathom database safely (backups, transactions)

**Result:** 364 participants enriched, 9 deleted, 279 remain for Phase 4B-2

---

### **Phase 4B-2: Research Unclear Cases** ✅ COMPLETED (8 rounds, Oct 20, 2025)

**The Challenge:** 279 remaining people after Phase 4B-1

- 53 rejected (low scores, ambiguous)
- 226 never matched (< 80% or not in Airtable)

**What We Built:**

1. **Interactive HTML Generator**
   - Sortable table with all Fathom participant data
   - Fuzzy matching against Airtable
   - Gmail research integration
   - Export to CSV for decisions

2. **CSV Parser**
   - Categorizes standard actions (merge, drop)
   - Flags custom comments for human-AI discussion
   - Validates before execution

3. **Execution Framework**
   - Safe database operations with backups
   - Add new people to Airtable
   - Merge variants and duplicates
   - Comprehensive error handling

**Workflow (Production-Ready):**

1. Generate batch (25 people) → HTML table
2. Human reviews with Gmail context
3. AI parses decisions, flags custom comments
4. Human & AI discuss ambiguous cases
5. AI executes approved actions
6. Commit & document results

**Results (8 Rounds):**
- **409 participants validated** (58% of starting pool)
- **58 new people added to Airtable** (+10% growth)
- **198 actions executed** (merges, adds, drops)
- **255 participants remain** (87% total completion)
- **Process stabilized** - ready for final 5 rounds

---

### **Phase 4B-3: Add Airtable-Only** 📅 FUTURE

Insert Airtable members who haven't appeared in Fathom videos yet.

---

## Key Principles

### **1. Collaboration, Not Automation**

- AI proposes, human verifies
- Discuss ambiguous cases before acting
- CSV records all decisions with rationale

### **2. Airtable is Ground Truth for now**

- Fathom names get corrected to match Airtable
- "Myhan" → "Moo Young Han"
- "Abdulganiyu" → rejected (wrong match to "Logan")

### **3. Safe & Auditable**

- Automatic backups before any database changes
- Transactions with rollback on error
- CSV export = permanent record of decisions
- Already-enriched participants skipped in future runs

### **4. Comment-Driven Actions**

Human adds keywords in Comments column:

- `drop` - Delete from Fathom (contamination)
- `Correct Name: Full Name` - Use this name instead
- `needs reunion` - Multiple accounts to merge
- `add to airtable` - Create new Airtable entry
- Free-form text OK too

---

## Files

### **Scripts**

- `phase4b1_enrich_from_airtable.py` - Main matching pipeline
- `process_approved_matches.py` - CSV processor
- `phase4b2_review_unmatched.py` - Coming soon (Gmail research)

### **Data**

- Input: `/Users/admin/ERA_Admin/airtable/people_export.csv`
- Database: `/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db`
- Output: `phase4b1_APPROVALS_YYYYMMDD_HHMM.html`
- CSVs: Exported from HTML interface

### **Docs**

**For Humans:**
- `README_PHASE4B.md` - This file - system overview
- `PHASE4B2_PROGRESS_REPORT.md` - 8-round progress analysis
- `README_PHASE4B_DETAILED.md` - Technical details (database schema, API reference)
- `CONTEXT_RECOVERY.md` - Quick orientation for resuming work
- `COMMIT_PHASE4B1.md` - What was built & why

**For AI Assistants:**
- `AI_WORKFLOW_GUIDE.md` - Complete workflow for naive AI
  - Makes implicit collaboration habits explicit
  - 6-phase cycle with mental states
  - Decision trees & common patterns
  - Critical rules & troubleshooting

**Archives:**
- `archive/early_rounds/` - Historical execution scripts (Rounds 1-3)

---

## Current Status (2025-10-20)

### **Database:**

- Total participants: 1,953
- Validated: 1,698 (87%)
  - Phase 4B-1: 1,289
  - Phase 4B-2: +409 (8 rounds)
- Remaining: 255 (13%)
- Progress: 64% → 87% in one day

### **Airtable Growth:**

- Before Phase 4B-2: 572 people
- After 8 rounds: 630 people
- Added: 58 new ERA members/participants (+10%)
- Geographic diversity: Netherlands, Florida, Uganda, Kenya, Pakistan, Panama, Israel

### **Enrichment Quality:**

- 409 additional validations in Phase 4B-2
- Handled edge cases: phone numbers, device names, organizations
- Fixed Bio field usage (now properly empty)
- Merged multiple variants per person (Mbilizi Kalombo: 3+ variants)

### **Process Maturity:**

✅ **Production-Ready**
- Stable workflow (8 rounds, 0 failures)
- Clear documentation
- Comprehensive error handling
- Human-AI collaboration optimized

### **Next:**

- Complete remaining 255 participants (~5 more rounds)
- Target 95%+ completion
- Then proceed to Phase 4B-3 (Airtable → Fathom)

---

## Why This Approach Works

**Traditional ETL would fail here** because:

- Fuzzy matching has false positives ("Abdulganiyu" → "Logan")
- Low-confidence matches need human judgment
- Unknown people need research (Gmail, context)
- Duplicates/variants need domain knowledge

**Our collaborative approach succeeds** because:

- AI does the heavy lifting (matching, research, processing)
- Human provides judgment (verify videos, assess context)
- Discussion resolves ambiguity (chat before acting)
- CSV audit trail (every decision documented)

**Result:** High-quality data enrichment without black-box risk.

---

## Quick Reference

### Re-run Phase 4B-1 (test skip logic)

```bash
cd /Users/admin/ERA_Admin
source ERA_Admin_venv/bin/activate
python3 integration_scripts/phase4b1_enrich_from_airtable.py
# Should skip 248 already-enriched, match remaining unenriched
```

### Check Database Status

```bash
sqlite3 FathomInventory/fathom_emails.db "
SELECT 
  COUNT(DISTINCT CASE WHEN validated_by_airtable = 1 THEN name END) as enriched,
  COUNT(DISTINCT CASE WHEN validated_by_airtable IS NULL OR validated_by_airtable = 0 THEN name END) as unenriched,
  COUNT(DISTINCT name) as total
FROM participants;
"
```

### Restore from Backup (if needed)

```bash
ls -lt FathomInventory/backups/
cp FathomInventory/backups/fathom_emails.backup_YYYYMMDD_HHMM.db \
   FathomInventory/fathom_emails.db
```

---

**Last Updated:** 2025-10-20
**Status:** Phase 4B-1 ✅ | Phase 4B-2 ✅ (8 rounds) | Phase 4B-3 ⏭️
**Progress:** 87% Complete (1,698/1,953 validated)
**See:** [PHASE4B2_PROGRESS_REPORT.md](PHASE4B2_PROGRESS_REPORT.md) for detailed analysis
