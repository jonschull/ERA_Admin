# integration_scripts/README.md

### 1. Overview

**Purpose:** Scripts for reconciling data between ERA's various systems

This component provides cross-component integration workflows for enriching participant data. It is one of four components in ERA_Admin and serves as the **integration layer** connecting FathomInventory (AI-generated) with Airtable (human-curated).

**The Problem:**
ERA has people scattered across multiple systems:
- **Fathom**: 682 video call participants (AI-generated names, often misspelled)
- **Airtable**: 630 members (authoritative, curated database)
- **Gmail**: Email history with context about people

**Challenge**: Match Fathom participants to Airtable members, enrich Fathom data, handle ambiguous cases.

**The Solution: Collaborative Human-AI Review**

Phase 4B builds an interactive system where:
1. **Script generates** HTML approval table with fuzzy-matched candidates
2. **Human reviews** with AI assistance, checking video links, adding comments
3. **Human & AI discuss** ambiguous cases, research via Gmail, make decisions together
4. **Human exports** CSV with decisions (approve/reject/delete/merge)
5. **Script processes** only the approved actions

**Key principle:** AI proposes, human disposes, collaboration decides.

**Current Status:**

*Phase 4B-1* ✅ COMPLETE (Oct 19, 2025)
- 364 participants enriched via automated fuzzy matching (80% threshold)
- 188 AI-misspelled names corrected
- 351 members identified, 64 donors

*Phase 4B-2* ✅ COMPLETE (Oct 23, 2025)
- 459 participants validated via collaborative review (11 batches)
- 59 new people added to Airtable (+10% growth)
- 650+ total participants processed across all batches
- Production-ready workflow established
- Discipline learnings documented in /future_discipline/

*Phase 5T* 🎯 READY NOW
- Town Hall visualization in ERA Landscape
- Export script reinstated: export_townhalls_to_landscape.py
- Ready to execute

*Phase 4C* (Future)
- Process 223 new participants from continued Fathom automation
- Can use established Phase 4B-2 workflow

### 2. Orientation - Where to Find What

**You are at:** integration_scripts component README

**Which README to read:**
- **This file**: Overview and quick start
- **README_PHASE4B.md**: Complete Phase 4B system guide (detailed)
- **README_PHASE4B_DETAILED.md**: Technical deep dive (implementation)

**First-time users:**
1. Read this Overview (Section 1)
2. Read README_PHASE4B.md for system details
3. Follow Quick Start in Section 4

**Current Work (Phase 5T - Ready):**
1. Read [README.md](../README.md) - System overview
2. Check Phase 5T section below - Town Hall visualization ready
3. Script: export_townhalls_to_landscape.py
4. Prerequisites: ✅ Phase 4B-2 complete, ✅ 459 validated participants

**Future Work (Phase 4C):**
1. Process 223 new participants (from continued Fathom automation)
2. Can adapt Phase 4B-2 workflow (see archive/superseded_docs/)
3. Use PAST_LEARNINGS.md (300+ patterns) for efficiency

**What you might need:**
- **Parent system** → [/README.md](../README.md) - Overall ERA Admin architecture
- **System-wide status** → [/CONTEXT_RECOVERY.md](../CONTEXT_RECOVERY.md) - Integration status
- **System principles** → [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) - Overall philosophy
- **Phase 4B-2 history** → archive/superseded_docs/ - Completed workflows (archived)
- **Discipline learnings** → [/future_discipline/](#file-future_disciplinereadmemd) - AI collaboration lessons
- **FathomInventory** → [/FathomInventory/README.md](../FathomInventory/README.md) - Participant database
- **Airtable** → [/airtable/README.md](../airtable/README.md) - Member database

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

**integration_scripts-specific:**

**1. Collaborative Human-AI Workflow**
- **AI proposes, human disposes** - AI generates candidates, human makes final decisions
- **Collaboration decides** - Ambiguous cases discussed before action
- **Iterative review** - Batch processing with human approval at each step
- **6-phase cycle** - Generate, review, parse, discuss, execute, document

**2. Data Validation with Human Approval**
- **No black-box automation** - Every decision explained and justified
- **CSV records all decisions** - Auditable trail with comments
- **Custom comments flagged** - AI identifies cases needing discussion
- **Human expertise + AI research** - Best of both worlds (Gmail context)

**3. Safe Database Operations**
- **Automatic backups** - Before every modification
- **Transaction safety** - Rollback on error
- **Integrity checks** - Validate before and after
- **Template enforcement** - TEMPLATE_database_script.py for consistency

**4. Batch Processing**
- **25 people per batch** - Manageable review sessions
- **Sequential processing** - Complete each batch before next
- **Progress tracking** - PHASE4B2_PROGRESS_REPORT.md updated after each round
- **Incremental improvement** - Each round refines the workflow

**5. NOT Traditional ETL**
- **Collaborative data curation** - Not automated pipeline
- **Judgment calls required** - Edge cases need human expertise
- **Context matters** - Gmail research, video links, meeting history
- **Quality over speed** - Thorough validation vs bulk processing

### 4. Specialized Topics

#### Quick Start

**Phase 5T (Current - Ready to execute):**
```bash
cd /Users/admin/ERA_Admin
source ERA_Admin_venv/bin/activate

# Export Town Hall meetings to landscape
python3 integration_scripts/export_townhalls_to_landscape.py

# Exports:
# - 17 TH meetings as project nodes
# - 459 validated participants
# - Person-to-meeting edges
# - Direct to Google Sheet (landscape auto-updates)
```

**Phase 4B-1 (Historical - can re-run if needed):**
```bash
python3 integration_scripts/phase4b1_enrich_from_airtable.py
# Opens HTML table → Review → Export CSV → Process
```

**Phase 4B-2:** ✅ Complete (Oct 23, 2025). Learnings documented in /future_discipline/.

#### Phase Details

**Phase 4B-1: Automated Fuzzy Matching** ✅ COMPLETE (Oct 19, 2025)

*What it does:*
- Fuzzy matches Fathom participants to Airtable members (80% threshold)
- Generates sortable HTML table with video links
- Exports to CSV for collaborative review
- Processes approved matches safely (backups, transactions)
- Skips already-enriched participants in future runs

*Results:*
- 364 participants enriched
- 188 AI-misspelled names corrected
- 351 members identified, 64 donors
- 9 contamination entries deleted
- 279 unenriched participants remained → Phase 4B-2

*Files:*
- `phase4b1_enrich_from_airtable.py` - Main pipeline
- `process_approved_matches.py` - CSV processor

**Phase 4B-2: Collaborative Review** ✅ COMPLETE (Oct 23, 2025)

*What we built:*
- Interactive HTML table generator with Gmail integration
- CSV parser for collaborative decision-making
- Automated execution scripts with safety checks
- Reusable Airtable addition module
- Discipline documentation and architectural proposals

*Results (11 batches):*
- **459 participants validated** (100% of Oct 23 scope)
- **59 new people added to Airtable** (+10% growth)
- **650+ participants processed** across all batches
- **Process stabilized** - production-ready workflow
- **Lessons documented** - /future_discipline/ component created

*Key achievements:*
- Handled phone numbers as names (3 cases)
- Resolved device names (John's iPhone, etc.)
- Merged organization names to people
- Fixed Bio field usage (now empty, provenance in Provenance field)
- Processed joint entries, duplicates, variants

*Historical Files (in archive/):*
- `experimental/generate_batch_data.py` - Batch selection (archived)
- `experimental/generate_phase4b2_table.py` - HTML generator (archived)
- `experimental/parse_phase4b2_csv.py` - CSV parser (archived)
- Past decisions: `past_decisions/` - All 11 batch CSVs
- Past batches: `past_batches/` - All HTML review files

*Active Files:*
- **PAST_LEARNINGS.md** - 300+ patterns (actively used for future work)
- `generate_batch_CANONICAL.py` - Production batch generator

*Historical Documentation (in archive/superseded_docs/):*
- PHASE4B2_PROGRESS_REPORT.md - 11-batch analysis (archived)
- AI_WORKFLOW_GUIDE.md - Collaborative workflow guide (archived)

**Phase 4B-3: Add Airtable-Only Members** ⏭️ NEXT

*Goal:* Insert Airtable members who haven't appeared in Fathom videos yet.

*Readiness:* Phase 4B-2 COMPLETE (Oct 23, 2025). Ready when needed for future participant processing.

#### Philosophy

**This is NOT traditional ETL.** It's collaborative data curation:

- **No black-box automation** - Every decision explained and justified
- **Human expertise + AI research** - Best of both worlds
- **Iterative discussion** - Review ambiguous cases together before acting
- **Auditable** - CSV records all decisions with comments
- **Safe** - Backups, transactions, rollback on error

**The AI's role:**
- Propose matches based on fuzzy matching
- Research people via Gmail for context
- Explain options and trade-offs
- Execute approved decisions

**The human's role:**
- Verify identities using video links, Gmail context
- Make judgment calls on ambiguous cases
- Decide on edge cases (phone numbers, devices, organizations)
- Approve actions before execution

#### Templates for Future Scripts

**TEMPLATE_database_script.py** - Template for any script that modifies `fathom_emails.db`

*Enforces:*
- Automatic backup before modifications
- Transaction safety (rollback on error)
- Integrity checks
- Standard error handling

*Usage:*
```bash
cp TEMPLATE_database_script.py your_new_script.py
# Edit to add your modification logic
```

Phase 4B scripts follow this pattern.

#### Utility Scripts

**Setup & Configuration:**
- `setup_gmail_auth.py` - One-time Gmail OAuth setup for gmail_research.py
  - Run once to authorize Gmail access for research features
  - Creates token file for automated Gmail queries

**Archive:**
- `archive/` - Historical scripts from early development
  - `early_rounds/` - Rounds 1-3 execution scripts
  - `rounds_4_8/` - Rounds 4-8 (reference implementations)
  - `dev_scripts/` - Development and testing utilities

#### Documentation

**For Humans:**
- **This README** - Overview and quick start
- **[README_PHASE4B.md](README_PHASE4B.md)** - Complete Phase 4B system guide
- **[README_PHASE4B_DETAILED.md](README_PHASE4B_DETAILED.md)** - Technical deep dive
- **[PHASE4B2_PROGRESS_REPORT.md](PHASE4B2_PROGRESS_REPORT.md)** - 8-round progress analysis
- **[CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md)** - Quick orientation for resuming work
- **[COMMIT_PHASE4B1.md](COMMIT_PHASE4B1.md)** - What was built & why

**For AI Assistants:**
- **[AI_WORKFLOW_GUIDE.md](AI_WORKFLOW_GUIDE.md)** - Complete workflow for naive AI
  - Makes implicit habits explicit
  - 6-phase collaboration cycle
  - Mental states for each phase
  - Common patterns & decision trees
  - Critical rules & troubleshooting

**Archives:**
- **[archive/early_rounds/](archive/early_rounds/)** - Historical scripts (Rounds 1-3)
- **[archive/rounds_4_8/](archive/rounds_4_8/)** - Rounds 4-8 execution scripts

#### Configuration

Paths configured in `../era_config.py`:
```python
from era_config import Config
airtable_csv = Config.AIRTABLE_PEOPLE_CSV
fathom_db = Config.FATHOM_DB_PATH
```

For server deployment, edit `era_config.py` or set environment variables.

#### Key Files

**Phase 4B-1 Scripts:**
- `phase4b1_enrich_from_airtable.py` - Main fuzzy matching pipeline
- `process_approved_matches.py` - CSV processor with safety checks

**Phase 4B-2 Scripts:**
- `generate_batch_data.py` - Select next 25 unenriched people
- `generate_phase4b2_table.py` - Create HTML review interface with Gmail links
- `parse_phase4b2_csv.py` - Parse CSV, flag custom comments for discussion
- `execute_round4_actions.py` through `execute_round8_actions.py` - Round-specific execution
- `add_to_airtable.py` - Reusable Airtable addition module
- `gmail_research.py` - Gmail context retrieval

**Templates:**
- `TEMPLATE_database_script.py` - Standard pattern for DB modifications

**Documentation:**
- `README_PHASE4B.md` - Complete system guide
- `README_PHASE4B_DETAILED.md` - Technical implementation details
- `PHASE4B2_PROGRESS_REPORT.md` - 8-round analysis with metrics
- `AI_WORKFLOW_GUIDE.md` - AI assistant workflow guide
- `CONTEXT_RECOVERY.md` - Component state and resuming work
- `COMMIT_PHASE4B1.md` - Phase 4B-1 implementation notes

**Archives:**
- `archive/early_rounds/` - Rounds 1-3 (learning phase)
- `archive/rounds_4_8/` - Rounds 4-8 (production phase)

#### Integration With Other Components

**Reads from:**
- **Airtable** (via [airtable/README.md](../airtable/README.md))
  - `people_export.csv` - 630 members (ground truth)
  - `people_for_matching.csv` - Cleaned for fuzzy matching

- **FathomInventory** (via [FathomInventory/README.md](../FathomInventory/README.md))
  - `fathom_emails.db` - 1,953 participants
  - Participant table for enrichment

**Writes to:**
- **FathomInventory database**
  - Updates participant records (member_status, donor_flag, etc.)
  - Adds provenance tracking (data_source column)

- **Airtable** (via API)
  - Adds new people discovered in Fathom
  - Updates only when explicitly approved

**Exports for:**
- **ERA Landscape** (Phase 5T - future)
  - Town Hall meeting chain visualization
  - Export enriched participants to Google Sheet

**Back to:** [/README.md](../README.md)