# ERA Admin Integration Scripts

Scripts for reconciling data between ERA's various systems.

---

## The Problem

ERA has people scattered across multiple systems:
- **Fathom:** 650+ video call participants (AI-generated names, often misspelled)
- **Airtable:** 590+ members (authoritative, curated database)
- **Gmail:** Email history with context about people

**Challenge:** Match Fathom participants to Airtable members, enrich Fathom data, handle the ambiguous cases.

---

## The Solution: Collaborative Human-AI Review

**Phase 4B** builds an interactive system where:

1. **Script generates** HTML approval table with fuzzy-matched candidates
2. **Human reviews** with AI assistance, checking video links, adding comments
3. **Human & AI discuss** ambiguous cases, research via Gmail, make decisions together
4. **Human exports** CSV with decisions (approve/reject/delete/merge)
5. **Script processes** only the approved actions

**Key principle:** AI proposes, human disposes, collaboration decides.

👉 **See [README_PHASE4B.md](README_PHASE4B.md) for the complete Phase 4B system**

---

## Current Status

### ✅ Phase 4B-1: Completed (2025-10-19)
**Interactive fuzzy matching & enrichment**

**What it does:**
- Fuzzy matches Fathom participants to Airtable members (80% threshold)
- Generates sortable HTML table with video links
- Exports to CSV for collaborative review
- Processes approved matches safely (backups, transactions)
- Skips already-enriched participants in future runs

**Results:**
- 364 participants enriched
- 188 AI-misspelled names corrected
- 351 members identified, 64 donors
- 9 contamination entries deleted
- 279 unenriched participants remain → Phase 4B-2

**Files:**
- `phase4b1_enrich_from_airtable.py` - Main pipeline
- `process_approved_matches.py` - CSV processor

---

### ✅ Phase 4B-2: COMPLETED (2025-10-20)
**Review unmatched participants with Gmail research - 8 rounds**

**What we built:**
- Interactive HTML table generator with Gmail integration
- CSV parser for collaborative decision-making
- Automated execution scripts with safety checks
- Reusable Airtable addition module

**Results:**
- **409 participants validated** (8 rounds × ~51 avg)
- **58 new people added to Airtable** (+10% growth)
- **198 actions executed** (merges, adds, drops)
- **255 participants remain** (87% complete, up from 64%)
- **Process stabilized** - production-ready workflow

**Key achievements:**
- Handled phone numbers as names (3 cases)
- Resolved device names (John's iPhone, etc.)
- Merged organization names to people
- Fixed Bio field usage (now empty, provenance in Provenance field)
- Processed joint entries, duplicates, variants

**Files:**
- `generate_batch_data.py` - Select next 25 people
- `generate_phase4b2_table.py` - Create HTML review interface
- `parse_phase4b2_csv.py` - Parse decisions, flag custom comments
- `execute_roundN_actions.py` - 8 round execution scripts
- `add_to_airtable.py` - Reusable addition module

👉 **See [PHASE4B2_PROGRESS_REPORT.md](PHASE4B2_PROGRESS_REPORT.md) for complete 8-round analysis**

---

### ⏭️ Phase 4B-3: Next
**Add Airtable-only members to Fathom**

Insert Airtable members who haven't appeared in Fathom videos yet.

**Readiness:** Phase 4B-2 is 87% complete (255 remaining). Estimated 5 more rounds to reach 95%+ before starting Phase 4B-3.

---

## Quick Start

### Phase 4B-1 (Re-run to test)
```bash
cd /Users/admin/ERA_Admin
source ERA_Admin_venv/bin/activate
python3 integration_scripts/phase4b1_enrich_from_airtable.py
```

Opens HTML table → Review → Export CSV → Process

### Phase 4B-2 (Current - 8 rounds completed)
```bash
# Generate batch
python3 integration_scripts/generate_batch_data.py
python3 integration_scripts/generate_phase4b2_table.py

# Review in browser → Export CSV

# Parse and execute
python3 integration_scripts/parse_phase4b2_csv.py <csv_file>
# Discuss custom comments with AI
python3 integration_scripts/execute_roundN_actions.py
```

Includes Gmail research, interactive HTML, collaborative review.

---

## Philosophy

**This is NOT traditional ETL.** It's collaborative data curation:

- **No black-box automation** - Every decision explained and justified
- **Human expertise + AI research** - Best of both worlds
- **Iterative discussion** - Review ambiguous cases together before acting
- **Auditable** - CSV records all decisions with comments
- **Safe** - Backups, transactions, rollback on error

**The AI's role:** Propose matches, research people, explain options, execute approved decisions.  
**The human's role:** Verify identities, make judgment calls, decide on edge cases, approve actions.

---

## Templates for Future Scripts

### **TEMPLATE_database_script.py**
Template for any script that modifies `fathom_emails.db`.

**Enforces:**
- Automatic backup before modifications
- Transaction safety (rollback on error)
- Integrity checks
- Standard error handling

**Usage:**
```bash
cp TEMPLATE_database_script.py your_new_script.py
# Edit to add your modification logic
```

Phase 4B scripts follow this pattern.

---

## Documentation

### For Humans:
- **[README_PHASE4B.md](README_PHASE4B.md)** - Complete Phase 4B system guide
- **[PHASE4B2_PROGRESS_REPORT.md](PHASE4B2_PROGRESS_REPORT.md)** - 8-round progress analysis
- **[CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md)** - Quick orientation for resuming work
- **[COMMIT_PHASE4B1.md](COMMIT_PHASE4B1.md)** - What was built & why

### For AI Assistants:
- **[AI_WORKFLOW_GUIDE.md](AI_WORKFLOW_GUIDE.md)** - Complete workflow for naive AI
  - Makes implicit habits explicit
  - 6-phase collaboration cycle
  - Mental states for each phase
  - Common patterns & decision trees
  - Critical rules & troubleshooting

### Archives:
- **[archive/early_rounds/](archive/early_rounds/)** - Historical scripts (Rounds 1-3)

---

## Configuration

Paths configured in `../era_config.py`:
```python
from era_config import Config
airtable_csv = Config.AIRTABLE_PEOPLE_CSV
fathom_db = Config.FATHOM_DB_PATH
```

For server deployment, edit `era_config.py` or set environment variables.
