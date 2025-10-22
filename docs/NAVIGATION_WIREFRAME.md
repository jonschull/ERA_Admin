# ERA Admin Documentation Wireframe

**Purpose:** Script-parseable wireframe for generating folder structure
**Format:** Each `## FILE: path` section → create that file
**Date:** October 20, 2025

---

## How to Parse This

```python
# Pattern: ## FILE: path/to/file.md
# Content until next ## FILE: → file contents
# Script extracts paths and generates folder structure
```

**Test navigation:** Click links below to validate structure

---

## Navigation Tree Integrity Principles

**Structural guarantees:**

1. **No Orphans** - Every document is reachable from a README
2. **Always Navigate Up** - Every README references its parent README
3. **Mandatory TOC** - All files in folder listed in that folder's README "Specialized Topics"

**Result:** Tree structure rooted at `/README.md`, no dead ends

**Testable:**
```python
# Test: No orphan documents
def test_no_orphans():
    all_md_files = find_all_markdown_files()
    all_referenced = extract_links_from_all_readmes()
    orphans = all_md_files - all_referenced
    assert orphans == set(), f"Orphaned files: {orphans}"

# Test: Every component README links to parent
def test_readmes_reference_parent():
    component_readmes = find_component_readmes()
    for readme in component_readmes:
        parent_link = extract_parent_reference(readme)
        assert parent_link, f"{readme} missing parent reference"
```

---

## FILE: README.md

**Path:** `README.md`

### 1. Overview

**Purpose:** Coordinate integration between ERA's data systems

ERA Admin is the **integration hub** for connecting four separate ERA data systems:

1. **Google Docs Agendas** - Meeting notes with participant lists (ground truth)
   - Manual scribe notes from ERA Town Hall meetings
   - Source of truth for who attended which meetings

2. **Airtable** - Membership database (630 people)
   - Manual tracking of members and donors
   - 17 Town Hall attendance columns
   - Member/donor status, contact information

3. **Fathom Inventory** - Automated meeting analysis (1,953 participants)
   - AI-powered meeting discovery and analysis
   - Automated participant extraction from Fathom summaries
   - Daily automation at 3 AM

4. **ERA Landscape** - Network visualization (350+ organizations/people/projects)
   - Interactive network graph of ERA ecosystem
   - Live at: https://jonschull.github.io/ERA_Admin/ERA_Landscape/
   - Organizations, people, projects + relationships
   - Core component under ERA_Admin

**Goal:** Connect these systems to create a unified view of the ERA community.

**How They Connect:**
```
Google Docs Agendas (scribe notes)
    ↓ (manual extraction)
Airtable (630 people, TH attendance)
    ↓ (Phase 4B - enrichment scripts)
Fathom Inventory DB (1,953 participants)
    ↓ (Phase 5T - export scripts)
Google Sheet
    ↓ (automatic)
ERA Landscape (visualization)
```

**Integration Status:**
- **Phase 4B-1:** ✅ Automated fuzzy matching (364 enriched)
- **Phase 4B-2:** 🔄 87% complete - Collaborative review (409 enriched, 8 rounds)
- **Phase 5T:** Next - Town Hall visualization
- **Future:** Unified MySQL database (Q1 2026)

### 2. Orientation - Where to Find What

**You are at:** Main entry point (root README)

**This is a Windsurf development environment** where:
- **You (human)** are the **captain and navigator** - you set direction, make decisions, approve actions
- **AI assistants** are your **advisors and crew** - they research, propose solutions, execute approved tasks
- **This README** is your navigation chart - overview first, then specialized docs

**If you're resuming work or just arriving:**

1. **Current state** → [CONTEXT_RECOVERY.md](#file-context_recoverymd)
   - What's working, what's in progress, recent completions
   - Start here to resume where you left off

2. **For AI assistants** → [AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd)
   - Your role and conventions
   - Captain-advisor collaboration model
   - Read this BEFORE working on the project

3. **Strategic direction** → ERA_ECOSYSTEM_PLAN.md
   - Long-term integration plan (Phases 4-7)
   - Multi-system integration vision
   - Where this project is headed

4. **How we work** → [WORKING_PRINCIPLES.md](#file-working_principlesmd)
   - Philosophy, Git workflow, testing
   - Documentation practices
   - Component architecture

5. **Then come back** to this README for component details

**What you might need:**
- Components → See Specialized Topics below
- Quick commands → Section 4 has quick start examples
- Lost context → Start with CONTEXT_RECOVERY.md

### 3. Principles

**See:** [WORKING_PRINCIPLES.md](#file-working_principlesmd) for complete philosophy

**Key principles:**

1. **Human-AI Collaboration**
   - Human is captain (sets direction, makes decisions)
   - AI is critical advisor and crew (researches, proposes, executes approved tasks)
   - Not compliance, but collaboration - AI challenges, not just obeys

2. **Component Independence**
   - Each component can function standalone
   - Clear boundaries with well-defined interfaces
   - Centralized config (era_config.py) manages paths

3. **Git/PR Workflow**
   - Never commit directly to main
   - All changes via Pull Requests for review
   - Clear commit messages, proper testing before push

4. **Testing Discipline**
   - Validate before declaring "done"
   - Proactive validation prevents self-delusion
   - Think: "What test will user apply?" - run it first

5. **Documentation Hierarchy**
   - 4-section structure (Overview, Orientation, Principles, Specialized Topics)
   - Reference don't duplicate (link up for principles)
   - Every document reachable from a README (no orphans)

### 4. Specialized Topics

#### Documentation

- [CONTEXT_RECOVERY.md](#file-context_recoverymd) - Current system state, what's working, what's in progress
- [AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd) - Guide for AI assistants (captain-advisor model, workflows)
- [WORKING_PRINCIPLES.md](#file-working_principlesmd) - Philosophy, Git workflow, testing, documentation practices
- ERA_ECOSYSTEM_PLAN.md - Strategic integration plan (Phases 4-7, multi-system vision)
- CONFIGURATION_CENTRALIZATION_PLAN.md - Completed Oct 18 (migration to /Users/admin/ERA_Admin/)

#### Components

**[FathomInventory/](../FathomInventory/)** - Automated meeting analysis
- Purpose: AI-powered meeting discovery and participant extraction
- Records: 1,953 participants (1,698 validated/87%, 255 remaining)
- Automation: Daily at 3 AM via launchd
- Status: ✅ Operational
- Read: [FathomInventory/README.md](#file-fathominventoryreadmemd)

**[airtable/](../airtable/)** - Manual membership tracking
- Purpose: Membership database, donor tracking, TH attendance
- Records: 630 people (+58 from Phase 4B-2), 17 TH attendance columns
- Scripts: Read-only exports, cross-correlation with Fathom
- Status: ✅ Operational
- Read: [airtable/README.md](#file-airtablereadmemd)

**[integration_scripts/](../integration_scripts/)** - Cross-component bridges
- Purpose: Enrich Fathom data with Airtable information
- Phase 4B-1: ✅ Automated fuzzy matching (364 enriched)
- Phase 4B-2: 🔄 87% complete - Collaborative review (409 enriched, 8 rounds)
- Read: [integration_scripts/README.md](#file-integration_scriptsreadmemd)
- AI Workflow: integration_scripts/AI_WORKFLOW_GUIDE.md
- Progress: integration_scripts/PHASE4B2_PROGRESS_REPORT.md

**ERA_Landscape** (core component)
- Purpose: Interactive network visualization
- Content: 350+ organizations, people, projects + relationships
- Technology: Static HTML/JS, Google Sheets data source, vis.js
- Live: https://jonschull.github.io/ERA_Admin/ERA_Landscape/
- Location: `ERA_Landscape/` directory
- Read: ERA_Landscape/README.md, NETWORK_ARCHITECTURE.md, VISION.md
- Special: 65 fixed Town Hall nodes at periphery

#### Quick Start

**Check current state:**
```bash
# View Airtable exports
cd airtable
python export_people.py
# Exports 630 people to people_export.csv

# View landscape
open https://jonschull.github.io/ERA_Admin/ERA_Landscape/
```

**Run integration (Phase 4B-2):**
```bash
# Verify configuration
python era_config.py

# Generate review batch
cd integration_scripts
python3 generate_batch_data.py        # Select next 25 people
python3 generate_phase4b2_table.py    # Create HTML review

# Human reviews → exports CSV → AI executes
# See: integration_scripts/AI_WORKFLOW_GUIDE.md
```

**Run Fathom automation manually:**
```bash
cd FathomInventory
./run_all.sh
# Runs full pipeline: discover, share, download, process
```

#### System Requirements

**Location:** `/Users/admin/ERA_Admin/` (OUTSIDE Dropbox)
- Migrated Oct 18, 2025 to avoid file-locking issues
- Git repository for version control
- Safe for automated workflows

**Virtual Environment:** `/Users/admin/ERA_Admin_venv/` (also outside Dropbox)
```bash
python3 -m venv /Users/admin/ERA_Admin_venv
/Users/admin/ERA_Admin_venv/bin/pip install -r requirements.txt
```

**Key packages:** pyairtable, google-api-python-client, playwright, fuzzywuzzy

**Automation:** Daily at 3 AM via launchd (`com.era.admin.fathom.run`)
- Plist: `~/Library/LaunchAgents/com.era.admin.fathom.run.plist`
- Logs: `~/Library/Logs/fathom_run.log`

#### Important Notes

**Folder Structure:**
- ERA_Admin (this folder): `/Users/admin/ERA_Admin/` - Active development
- ERA_Admin_venv: `/Users/admin/ERA_Admin_venv/` - Shared Python environment
- Dropbox copy (if exists): BACKUP ONLY - do not use for automation

**Data Flow:**
1. Google Docs Agendas → Airtable (manual)
2. Fathom → FathomInventory DB (automated)
3. Airtable → FathomInventory DB (enrichment scripts)
4. FathomInventory DB → Google Sheet (export - future)
5. Google Sheet → Landscape (visualization)

**Common Gotchas:**
- Venv must be outside Dropbox (file-locking issues)
- Absolute paths required in launchd scripts
- Google API packages required for email download
- See "System Requirements & Known Gotchas" in original README

#### Current Metrics

- **Airtable:** 630 people, 324 TH attendance records
- **Fathom:** 1,953 participants (1,698 validated/87%)
- **Validation:** 61.5% baseline → 87% enriched
- **Landscape:** 350+ nodes
- **Integration:** Phase 4B-2 at 87%, Phase 5T next

**Back to:** Top of README

---

## FILE: CONTEXT_RECOVERY.md

**Path:** `CONTEXT_RECOVERY.md`

### 1. Overview

**Purpose:** Quickly understand current state and resume integration work

**This document is for:**
- **Humans resuming work** - Use this to quickly resume where you left off
- **AI assistants getting oriented** - Read this AFTER AI_HANDOFF_GUIDE.md for current state
- **Anyone lost** - Check this to understand what's working, what's in progress, what's next

**This document contains:**
- Current system state (what's working)
- Recent completions (what just finished)
- Data inventory (where data lives, what it contains)
- Integration status (which phases complete, which in progress)
- How to resume work (verification commands, common tasks)
- Next steps (what to do next)

**Note for AI:** This gives you current state - don't propose changes without understanding history. Check `historical/` folders for context on past decisions. Your role: Help human navigate options, research details, execute approved tasks.

### 2. Orientation - Where to Find What

**You are at:** System-wide context recovery document

**Use this when:**
- Resuming work after time away
- Checking what's currently in progress
- Verifying system health
- Finding next available tasks

**What you might need:**
- **Main overview** → [README.md](#file-readmemd) - System architecture and components
- **Strategic plan** → ERA_ECOSYSTEM_PLAN.md - Long-term vision (Phases 4-7)
- **AI workflow** → [AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd) - How to work with AI
- **How we work** → [WORKING_PRINCIPLES.md](#file-working_principlesmd) - Philosophy and practices
- **Component status** → Component CONTEXT_RECOVERY files (FathomInventory, etc.)
- **Recent changes** → CONFIGURATION_CENTRALIZATION_PLAN.md - Oct 18 migration

### 3. Principles

**System-wide:** See [WORKING_PRINCIPLES.md](#file-working_principlesmd)

**Applied in this document:**

1. **Proactive Validation**
   - "How to Resume Work" section provides health check commands
   - Verify configuration, check automation, validate database
   - Don't assume it's working - check first

2. **Documentation Maintenance**
   - Last updated timestamp at bottom
   - Recent completions tracked with dates
   - Current phase status clearly stated

3. **Context Preservation**
   - Data inventory (where everything lives)
   - Known issues section (historical context)
   - Quick context questions for AI

4. **Respect for Time**
   - "Start Here" section for quick orientation
   - Common tasks with copy-paste commands
   - Success metrics to track progress

### 4. Specialized Topics

#### Start Here

**Humans:**
- Check "What's Working" to see system health
- Check "What's In Progress" for current work
- Review "Next Steps" for what to do next

**AI Assistants:**
- Read this AFTER [AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd)
- Use "Quick Context Questions" section
- Don't propose changes without understanding history

#### Current System State

**What's Working:**
- ✅ **Airtable exports operational** - 630 people (+58 from Phase 4B-2), 17 TH attendance columns
- ✅ **Landscape deployed** - https://jonschull.github.io/ERA_Admin/ERA_Landscape/
- ✅ **Fathom automation running** - Daily at 3 AM, 1,953 participants tracked
- ✅ **Phase 4B-1 complete** - 364 participants enriched via fuzzy matching (Oct 19)
- ✅ **Phase 4B-2: 87% complete** - 409 participants validated via collaborative review (Oct 20)

**Recent Completions:**

*Oct 18, 2025:*
- ✅ Configuration Centralization (See CONFIGURATION_CENTRALIZATION_PLAN.md)
  - Migration to `/Users/admin/ERA_Admin/`
  - Centralized config in `era_config.py`
  - Bug fix: run_all.sh Step 3 exit issue
  - Automation schedule changed to 3 AM

*Oct 19, 2025:*
- ✅ Phase 4B-1: Automated Fuzzy Matching
  - 364 participants enriched
  - 188 AI-misspelled names corrected
  - 351 members identified, 64 donors

*Oct 20, 2025:*
- ✅ Phase 4B-2: Collaborative Human-AI Review (8 rounds)
  - 409 participants validated
  - 58 new people added to Airtable (+10% growth)
  - Production-ready workflow established
  - See: `integration_scripts/PHASE4B2_PROGRESS_REPORT.md`

**Available Next Steps:**
- 🎯 Phase 4B-2 Completion - Process remaining 255 participants (~5 more rounds)
- 🎯 Phase 5T: Town Hall Visualization - Export meeting chain to landscape (ready after 4B-2)
- 🎯 Multi-System Integration - Long-term strategic plan (see ERA_ECOSYSTEM_PLAN.md)

#### Data Inventory

**Airtable (Manual Tracking):**
- Location: `airtable/people_export.csv`
- Records: 630 people (+58 from Phase 4B-2 reconciliation)
- TH Attendance: 17 meetings, 324 attendance records
- Fields: Name, email, member status, donor flag, phone, etc.
- Last Export: Run `python airtable/export_people.py` for fresh data
- Recent Growth: +10% from Fathom participant reconciliation (Oct 20)

**Fathom Inventory DB (Automated AI):**
- Location: `/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db`
- Participants: 1,953 total
  - 1,698 validated (87%) - enriched with Airtable data
  - 255 remaining (13%) - need collaborative review
- Enrichment Status:
  - Phase 4B-1: 364 enriched (Oct 19)
  - Phase 4B-2: 409 enriched (Oct 20, 8 rounds)
- Automation: Daily at 3 AM via launchd ✅ Working

**ERA Landscape (Visualization):**
- Location: Google Sheet ID: 1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY
- Content: 350+ nodes (organizations, people, projects)
- Live Site: https://jonschull.github.io/ERA_Admin/ERA_Landscape/
- Technology: Static HTML/JS, OAuth editing enabled

**Validation & Enrichment Data:**
- Original Report: `/Users/admin/FathomInventory/analysis/townhall_validation_report.md`
  - 61.5% average match rate baseline
- Phase 4B Progress: `integration_scripts/PHASE4B2_PROGRESS_REPORT.md`
  - 87% completion (1,698/1,953 validated)
  - 8 rounds completed (409 participants)
  - 58 new people added to Airtable
  - Production-ready collaborative workflow

#### Integration Status

**Completed Phases:**

*Phase 1-3: Fathom Foundation* ✅ (Oct 17)
- Database integration complete
- ERA meeting analysis automated
- Daily workflow operational
- Participant extraction working

*Phase 4A: Validation* ✅ (Oct 17)
- Compared Airtable TH columns vs Fathom participants
- Identified complementary data sources
- Generated validation report
- Established 61.5% baseline match rate

*Phase 4B-1: Automated Fuzzy Matching* ✅ (Oct 19)
- Fuzzy matched Fathom → Airtable (≥80% confidence)
- 364 participants enriched automatically
- 188 AI-misspelled names corrected
- 351 members identified, 64 donors

*Phase 4B-2: Collaborative Review* 🔄 87% Complete (Oct 20)
- 8 rounds completed - 409 participants validated
- 58 new people added to Airtable (+10% growth)
- 255 remaining (~5 more rounds to 95%)
- Workflow: Human-AI collaboration with Gmail research
- See: `integration_scripts/PHASE4B2_PROGRESS_REPORT.md`
- For AI: `integration_scripts/AI_WORKFLOW_GUIDE.md`

**Current Phase:**

*Phase 4B-2: Collaborative Review* 🔄 87% Complete (5 more rounds)
- Status: 1,698/1,953 validated (87%)
- Workflow:
  1. Generate batch (25 people) → HTML review table
  2. Human reviews with Gmail research → exports CSV
  3. AI parses decisions, flags custom comments
  4. Human-AI discuss ambiguous cases
  5. AI executes approved actions
  6. Commit & document
- Progress: 8 rounds done, 409 validated, 58 added to Airtable
- Remaining: 255 participants (~5 rounds to 95%)
- Docs:
  - Workflow: `integration_scripts/AI_WORKFLOW_GUIDE.md`
  - Progress: `integration_scripts/PHASE4B2_PROGRESS_REPORT.md`
  - System: `integration_scripts/README_PHASE4B.md`

*Phase 5T: Town Hall Visualization* ⭐ AFTER 4B-2 (3-4 hours)
- Goal: Export TH meetings as connected chain in landscape
- Readiness: Phase 4B-2 at 87%, ready when 95%+ complete
- Actions:
  1. Query enriched participants from Fathom DB
  2. Format as project nodes (meetings) + person nodes + edges
  3. Export to Google Sheet via Sheets API
  4. Landscape auto-updates
- Result: Interactive meeting chain with 300+ connections

#### How to Resume Work

**1. Verify System Health:**
```bash
# Verify configuration
cd /Users/admin/ERA_Admin
python3 era_config.py
# Should show all paths verified

# Check Fathom automation
tail /Users/admin/ERA_Admin/FathomInventory/cron.log
# Should show daily runs at 3 AM

# Check Fathom database
sqlite3 /Users/admin/ERA_Admin/FathomInventory/fathom_emails.db \
  "SELECT COUNT(*) FROM participants;"
# Should show 1,953+ (grows with each meeting analyzed)

# Check landscape
open https://jonschull.github.io/ERA_Admin/ERA_Landscape/
# Should load interactive graph
```

**2. Check Current Work Status:**
```bash
# Check recent completed work
cd /Users/admin/ERA_Admin
cat CONFIGURATION_CENTRALIZATION_PLAN.md
# Status: COMPLETE (Oct 18, 2025)

# Check strategic plan for future work
cat ERA_ECOSYSTEM_PLAN.md
# Active: Multi-system integration

# Check recent commits
git log --oneline -5
git status
```

**3. Review Planning Documents:**
- Integration strategy: Read `ERA_ECOSYSTEM_PLAN.md`
- Component details: Read component README files
- AI workflow: Read `AI_HANDOFF_GUIDE.md`

#### Common Tasks

**Export Fresh Airtable Data:**
```bash
cd /Users/admin/ERA_Admin/airtable
python export_people.py
# Creates people_export.csv with 630 records (+58 from Phase 4B-2)
```

**Check Fathom-Airtable Match Rate:**
```bash
cd /Users/admin/ERA_Admin/FathomInventory/analysis
python validate_townhall_attendance.py
# Generates townhall_validation_report.md
```

**Update Landscape Visualization:**
```bash
# Phase 5T script (when ready)
cd integration_scripts
python export_townhalls_to_landscape.py
# Writes to Google Sheet → Landscape updates automatically
```

**Manual Test Integration:**
```bash
# Test Airtable export
cd /Users/admin/ERA_Admin/airtable
python export_people.py

# Test cross-correlation
python cross_correlate.py
# Generates cross_correlation_report.txt
```

#### Key Files & Locations

**ERA Admin (This Directory):**
```
ERA_Admin/
├── README.md                    ← Overview
├── CONTEXT_RECOVERY.md          ← This file
├── ERA_ECOSYSTEM_PLAN.md        ← Full integration strategy
├── AI_HANDOFF_GUIDE.md          ← AI workflow
│
├── airtable/
│   ├── people_export.csv           (630 people, +58 from Phase 4B-2)
│   ├── people_for_matching.csv     (cleaned for fuzzy matching)
│   └── cross_correlation_report.txt (validation analysis)
│
├── FathomInventory/
│   ├── fathom_emails.db             (1,953 participants - 87% enriched)
│   ├── run_all.sh                   (daily automation at 3 AM)
│   └── analysis/
│       ├── analyze_new_era_calls.py        (daily ERA meeting analysis)
│       ├── validate_townhall_attendance.py (Airtable comparison)
│       └── townhall_validation_report.md   (baseline: 61.5% match rate)
│
└── integration_scripts/         ← Phase 4-5
    ├── phase4b1_enrich_from_airtable.py  (Phase 4B-1 ✅ Complete)
    ├── generate_phase4b2_table.py        (Phase 4B-2 🔄 87% Complete)
    ├── AI_WORKFLOW_GUIDE.md              (For AI assistants)
    ├── PHASE4B2_PROGRESS_REPORT.md       (8-round analysis)
    └── export_townhalls_to_landscape.py  (Phase 5T - after 4B-2)
```

#### Known Issues & Context

**Migration from Dropbox (Complete - Oct 18, 2025):**
- Issue: Dropbox file-locking broke launchd automation ("Resource deadlock" errors)
- Solution: Moved entire ERA_Admin to `/Users/admin/ERA_Admin/` outside cloud sync
- Current: All components at new location, Dropbox copy is backup only
- Result: Automation working, Git repository active

**Airtable TH Columns:**
- Current: 17 TH attendance columns (manual tracking)
- Plan: Keep updating until Interactive Agenda App ready (Q2 2026)
- Reason: Provides validation data, don't break working process

**Name Variations:**
- Challenge: "Jon Schull" vs "Jonathan Schull" vs "Jon"
- Solution: Fuzzy matching at 80% threshold
- Status: Working well, 61.5% match rate acceptable

**Data Provenance:**
- Challenge: Which system is source of truth?
- Current: Multiple sources, tracked via `data_source` column
- Future: MySQL as single source (Q1 2026)

#### Next Steps

**Immediate (Active Now):**
*Phase 4B-2: Complete Remaining 255 Participants*
1. 🔄 Continue collaborative review rounds
2. 🔄 Target 95%+ completion (~5 more rounds)
3. 🔄 Use established workflow (see `integration_scripts/AI_WORKFLOW_GUIDE.md`)

**After 4B-2 Completion:**
*Phase 5T: Town Hall Visualization*
- Export meetings to landscape visualization
- Connect 300+ participants to meetings

*Phase 4C: Automation*
- Daily sync of new enrichments

#### Success Metrics

**Phase 4B-2 Completion:**
- [✓] Production workflow established (8 rounds tested)
- [✓] 1,698 participants validated (87%)
- [✓] 630 people in Airtable (+10% growth)
- [ ] 95%+ completion target (48 more validations)
- [ ] Remaining 255 participants processed

**Phase 5T Completion:**
- [ ] 17 TH meetings as project nodes
- [ ] Town Hall Meetings umbrella project
- [ ] 300+ person-to-meeting edges
- [ ] Jon Schull → TH Meetings organizer edge
- [ ] Loads in <3 seconds

#### AI-Specific Recovery

**If you are an AI resuming this work:**

1. **Read this file completely** before making changes
2. **Check system health** with commands in "How to Resume Work"
3. **Review ERA_ECOSYSTEM_PLAN.md** for full integration strategy
4. **Read component README** if working on specific system
5. **Don't assume user approval** - wait for explicit go-ahead
6. **Update this file** if you make significant state changes

**Quick Context Questions:**
- What's the current phase? **Phase 4B-2 (87% complete) → 5T (Town Hall Viz)**
- What's working? **All base systems + collaborative workflow operational**
- What's in progress? **Completing remaining 255 participants (5 more rounds)**
- When was last successful run? **Check Fathom cron.log for 3 AM runs**
- Any blockers? **No - production workflow proven over 8 rounds**
- For AI workflow? **See `integration_scripts/AI_WORKFLOW_GUIDE.md`**

#### Component Context

- [FathomInventory/CONTEXT_RECOVERY.md](#file-fathominventorycontext_recoverymd) - Component-specific status

#### Where to Find Help

- Integration strategy: ERA_ECOSYSTEM_PLAN.md
- Airtable details: airtable/README.md
- Landscape details: ERA_Landscape/README.md, NETWORK_ARCHITECTURE.md
- Fathom details: FathomInventory/README.md
- AI workflow: [AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd)

**Back to:** [README.md](#file-readmemd)

---

## FILE: AI_HANDOFF_GUIDE.md

**Path:** `AI_HANDOFF_GUIDE.md`

### 1. Overview

**Purpose:** Guide for AI assistants working on ERA data integration

**Environment:** Windsurf IDE with AI-assisted development

**This guide is for:**
- AI assistants onboarding to ERA Admin project
- Understanding your role (advisor and crew, not autonomous agent)
- Learning the captain-advisor collaboration model
- Following established workflows and conventions

**Your Role: Advisor and Crew**

You are working in a **Windsurf development environment** where:

**The Human Is:**
- **Captain** - Sets direction, makes final decisions
- **Navigator** - Chooses which problems to solve and when
- **Authority** - Approves or rejects all actions

**You (AI) Are:**
- **Advisor** - Research options, explain trade-offs, recommend approaches
- **Crew** - Execute approved tasks, run tests, implement solutions
- **Scout** - Explore codebases, find patterns, surface relevant information

**What This Means:**
Humans read README, then get distracted or forget context. **Your job:** Help them navigate back using the docs, don't reinvent or explain what's already documented.

**Critical Philosophy:**
- **Vigilance against self-delusion and premature declarations of victory**
- Discussion ≠ directive (user comments during exploration are NOT implementation requests)
- Proactive validation before declaring success
- Wait for guidance (don't advance without explicit approval)
- Respect for human's valuable time (test thoroughly before showing results)

### 2. Orientation - Where to Find What

**You are at:** AI assistant onboarding guide

**First Session Checklist:**
1. Read [README.md](#file-readmemd) - System overview
2. Read [CONTEXT_RECOVERY.md](#file-context_recoverymd) - Current state
3. Skim ERA_ECOSYSTEM_PLAN.md - Strategic direction
4. Identify current phase (Phase 4B-2, Phase 5T, etc.)
5. Read this AI_HANDOFF_GUIDE completely
6. Ask clarifying questions if needed

**Documentation Hierarchy:**

*Level 1: ERA Admin (Integration Layer)*
- When to read: Working on cross-component integration
- [README.md](#file-readmemd) - System overview, quick start
- [CONTEXT_RECOVERY.md](#file-context_recoverymd) - Current state snapshot
- This AI_HANDOFF_GUIDE.md - AI workflow
- ERA_ECOSYSTEM_PLAN.md - Full integration strategy (Phases 4-7)

*Level 2: Components*
- When to read: Working on specific component
- airtable/README.md - Airtable exports, cross-correlation
- FathomInventory/README.md - Automation system
- ERA_Landscape/README.md - Network visualization component
- ERA_Landscape/NETWORK_ARCHITECTURE.md - Technical deep-dive (Town Hall treatment, physics, node sizing)

*Level 3: Component Details*
- When to read: Debugging or enhancing component internals
- Component config files, development docs, specialized guides

**Navigation Rule:** Start at highest level needed. Read component docs only when working on that component.

**What you might need:**
- Current work status → [CONTEXT_RECOVERY.md](#file-context_recoverymd)
- Philosophy & practices → [WORKING_PRINCIPLES.md](#file-working_principlesmd)
- Phase-specific AI workflow → integration_scripts/AI_WORKFLOW_GUIDE.md
- Component details → Component READMEs

### 3. Principles

**System-wide:** See [WORKING_PRINCIPLES.md](#file-working_principlesmd) for complete philosophy

**AI-specific critical principles:**

**1. Discussion ≠ Directive**
- User comments during exploration are **NOT** implementation requests
- Ask: "Should I implement this approach?" before proceeding
- Don't assume approval from discussion

**2. Proactive Validation Before Declaring Success**
- Think: "What test will the user apply to validate?"
- Run that test yourself FIRST
- Show results, THEN ask user to verify
- Never declare "done" without user confirmation

**3. Wait for Guidance**
- Don't advance to next task without explicit approval
- Don't hallucinate user assent
- User silence ≠ approval

**4. Respect for Human's Valuable Time**
- Test thoroughly before showing results
- Present complete, validated work
- Don't make them debug your mistakes

**5. Concise Communication**
- Report what you tested and results
- Show, don't just claim
- Be brief but substantive

**What TO DO:**
- ✅ Read README first to understand the system
- ✅ Research thoroughly before proposing solutions
- ✅ Present options with trade-offs: "Approach A does X but Y, Approach B..."
- ✅ Ask "Should I proceed?" before implementing
- ✅ Test your work before claiming success
- ✅ Point human to relevant docs: "See README section 3.2 for details"

**What NOT TO DO:**
- ❌ Assume you know what human wants without asking
- ❌ Implement during brainstorming discussions
- ❌ Make architecture decisions unilaterally
- ❌ Ignore existing patterns and documentation
- ❌ Declare victory without validation

**Red Flags - Stop If You're About To:**
- ❌ Implement during discussion without asking
- ❌ Say "Does this work?" before testing
- ❌ Declare "✅ Complete" without user validation
- ❌ Move to next phase without approval
- ❌ Assume your code works because it ran once

**Green Lights - These Are Good:**
- ✅ "Should I implement this approach?"
- ✅ "I've tested X, Y, Z. Here are the results. Could you verify?"
- ✅ "Ready for next step when you approve"
- ✅ Showing test outputs, not just claiming success

### 4. Specialized Topics

#### Common Workflows

**Workflow 1: Starting New Integration Work**
```
1. Read: CONTEXT_RECOVERY.md
   ├─> Understand current state
   ├─> Check what's in progress
   └─> Identify prerequisites

2. Read: ERA_ECOSYSTEM_PLAN.md
   ├─> Find your phase (4B, 5T, etc.)
   ├─> Understand dependencies
   └─> Review success metrics

3. Scan: Component README.md files
   ├─> What does Airtable provide?
   ├─> What does Fathom DB contain?
   └─> What format does Landscape need?

4. Create: integration_scripts/your_script.py
   ├─> Use absolute paths for cross-component access
   ├─> Add provenance tracking
   └─> Generate validation reports

5. Test: Run script, check all components
   ├─> Verify Airtable export fresh
   ├─> Check Fathom DB updated
   └─> Test Landscape visualization

6. Document: Update CONTEXT_RECOVERY.md
   └─> Record state change, next steps
```

**Workflow 2: Debugging Component Issue**
```
1. Identify which component is failing
   ├─> Airtable export? Read airtable/README.md
   ├─> Fathom automation? Read FathomInventory/README.md
   └─> Landscape visualization? Read ERA_Landscape/README.md

2. Read component's CONTEXT_RECOVERY.md (if exists)
   └─> Understand component's current state

3. Read component's DEVELOPMENT.md (if exists)
   └─> Follow component-specific testing procedures

4. Fix within component boundary
   └─> Don't introduce cross-component dependencies

5. Update component's documentation
   └─> Then update ERA_Admin/CONTEXT_RECOVERY.md if integration affected
```

**Workflow 3: Resuming After Break**
```
1. Read: CONTEXT_RECOVERY.md
   ├─> What's the current state?
   ├─> What was in progress?
   └─> Any blockers?

2. Verify: System health
   ├─> Check Airtable exports exist
   ├─> Check Fathom automation ran
   └─> Check Landscape loads

3. Review: Recent git commits
   ├─> ERA_Admin changes
   └─> FathomInventory changes

4. Continue: From documented next steps
   └─> CONTEXT_RECOVERY.md shows what's next
```

#### Code Conventions (CRITICAL)

**File Paths:**
```python
# ✅ CORRECT - Portable, relative to script location
import os
from pathlib import Path

# Get ERA_Admin root (scripts are in integration_scripts/)
SCRIPT_DIR = Path(__file__).parent
ERA_ADMIN_ROOT = SCRIPT_DIR.parent

# Internal paths (within ERA_Admin) - relative
AIRTABLE_DIR = ERA_ADMIN_ROOT / "airtable"
AIRTABLE_CSV = AIRTABLE_DIR / "people_export.csv"

# External paths (FathomInventory) - from config
from era_config import Config
FATHOM_DB = Config.FATHOM_DB_PATH

# ❌ WRONG - Hardcoded absolute paths break on server
AIRTABLE_CSV = "/Users/admin/ERA_Admin/airtable/people_export.csv"
FATHOM_DB = "/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db"
```
**Why:** System will be moved to server. ERA_Admin-relative paths are portable.

**Data Provenance Tracking:**
```python
# When enriching/inserting data
data_source = 'airtable_manual'  # or 'fathom_ai' or 'agenda_scribe' or 'both'

# When updating database
cursor.execute("""
    UPDATE participants 
    SET member_status = ?, 
        data_source = CASE 
            WHEN data_source = 'fathom_ai' THEN 'both'
            ELSE 'airtable_manual'
        END
    WHERE name = ?
""", (member_status, name))
```
**Why:** Enables quality assessment, conflict resolution, and future migration.

**Validation Reports:**
```python
def generate_enrichment_report(stats, matches):
    """Generate detailed enrichment report."""
    report_file = "enrichment_report.md"
    
    with open(report_file, 'w') as f:
        f.write("# Enrichment Report\n\n")
        f.write(f"**Date:** {datetime.now()}\n\n")
        f.write(f"**Matched:** {len(matches)}\n")
        f.write(f"**Updated:** {stats['updated']}\n")
        f.write(f"**Inserted:** {stats['inserted']}\n")
        f.write(f"**Match rate:** {stats['match_rate']:.1f}%\n\n")
        # ... detailed breakdowns
```
**Why:** User can verify work, troubleshoot issues, track quality metrics.

**Fuzzy Matching Standard:**
```python
from fuzzywuzzy import fuzz

def fuzzy_match_names(name1, name2, threshold=0.80):
    """
    Standard fuzzy matching for name comparison.
    
    Args:
        threshold: 0.80 (80%) is project standard
    
    Returns:
        (is_match: bool, score: float)
    """
    name1 = name1.lower().strip()
    name2 = name2.lower().strip()
    
    ratio = fuzz.ratio(name1, name2)
    partial = fuzz.partial_ratio(name1, name2)
    token_sort = fuzz.token_sort_ratio(name1, name2)
    
    best_score = max(ratio, partial, token_sort) / 100.0
    return best_score >= threshold, best_score
```
**Why:** Consistency across integration scripts, tunable if needed.

#### Critical Constraints

**1. Component Boundaries**

**DO:**
- ✅ Read from component's public outputs (CSV files, databases, APIs)
- ✅ Use component's documented interfaces
- ✅ Respect component's data formats

**DON'T:**
- ❌ Modify component's internal code without reading its DEVELOPMENT.md
- ❌ Bypass component's intended interfaces
- ❌ Assume component internals (read documentation first)

**2. System Philosophy**

ERA Admin coordinates integration between **four independent components**:
1. Google Docs Agendas - Manual meeting notes (ground truth)
2. Airtable - Membership database (self-contained in `airtable/`)
3. FathomInventory - Automated analysis (self-contained)
4. ERA Landscape - Visualization (self-contained in `ERA_Landscape/`)

**Key Principle:** You should **NOT** need to understand all component internals to work at the integration level.

**3. Database Safety**
```python
# ✅ CORRECT - Atomic transactions
conn = sqlite3.connect(FATHOM_DB)
try:
    cursor = conn.cursor()
    cursor.execute("BEGIN TRANSACTION")
    # ... multiple operations
    conn.commit()
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")
finally:
    conn.close()

# ✅ CORRECT - Backup before major operations
import shutil
backup_file = f"fathom_emails.db.backup_{datetime.now().strftime('%Y%m%d_%H%M')}"
shutil.copy2(FATHOM_DB, backup_file)
```
**Why:** Database is critical, used by daily automation. Corruption = data loss.

**4. Testing Before Declaring Success**

**Always:**
1. Run the script successfully
2. Check output/report files
3. Verify database updates (if applicable)
4. Test visualization (if applicable)
5. **Then** inform user of completion

**Never:**
- ❌ Assume success without testing
- ❌ Claim completion based on code alone
- ❌ Skip verification steps

#### Validation Checklist

**Before Starting Work:**
- [ ] Read CONTEXT_RECOVERY.md (current state)
- [ ] Read relevant component README.md files
- [ ] Verify prerequisites complete
- [ ] Understand success metrics

**During Implementation:**
- [ ] Use absolute paths for cross-component access
- [ ] Add data provenance tracking
- [ ] Generate validation reports
- [ ] Follow component conventions
- [ ] Test incrementally

**Before Declaring Done:**
- [ ] Script runs without errors
- [ ] Report file generated and reviewed
- [ ] Database updated (if applicable)
- [ ] Visualization tested (if applicable)
- [ ] User can verify results
- [ ] CONTEXT_RECOVERY.md updated

**After User Approval:**
- [ ] Git commit with clear message
- [ ] Update component documentation if needed
- [ ] Record next steps in CONTEXT_RECOVERY.md

#### AI-Specific Best Practices

**1. Don't Assume, Verify**
```python
# ❌ BAD - Assuming schema
cursor.execute("SELECT member_status FROM participants")

# ✅ GOOD - Check first
cursor.execute("PRAGMA table_info(participants)")
columns = [row[1] for row in cursor.fetchall()]
if 'member_status' not in columns:
    print("⚠️  member_status column doesn't exist yet")
    # Add column first
```

**2. Incremental Progress**

Don't try to complete entire phase in one turn. Break into steps:
1. **First turn:** Create script skeleton, test imports
2. **Second turn:** Implement data loading, test
3. **Third turn:** Implement matching logic, test
4. **Fourth turn:** Implement database updates, test
5. **Fifth turn:** Generate report, final validation

Update CONTEXT_RECOVERY.md after each step.

**3. Clear Communication**

Good progress update:
```
✅ Created enrich_from_airtable.py
✅ Tested Airtable loading (630 records)
✅ Tested Fathom DB connection (1,953 participants)
🎯 Next: Implement fuzzy matching logic

Would you like me to proceed with matching?
```

Bad progress update:
```
I've started working on the enrichment script.
```

**4. Respect Component Independence**

If you need to understand Airtable's export format:
1. Read `airtable/README.md` first
2. Look at `airtable/export_people.py` if needed
3. **Don't** modify airtable scripts without explicit request
4. **Don't** assume undocumented behavior

**5. Document State Changes**

After any significant operation:
```python
# At end of script
print("\n📝 Update CONTEXT_RECOVERY.md with:")
print("- Enrichment complete: 1,698 participants")
print("- Next step: Run Phase 5T export script")
```
Then actually update the file.

**6. File Creation Discipline**

**Pattern: Explore Freely, Commit Thoughtfully**

AI can create files during exploration:
- Prototyping solutions
- Documenting ideas
- Testing approaches
- Generating reports

**But before committing:**
1. **Review:** `git status` - What files were created?
2. **Question:** Should this be standalone or incorporated?
3. **Consolidate:** Merge into existing docs where appropriate
4. **Delete:** Remove redundant or unnecessary files
5. **Keep:** Only truly needed standalone files

**Example (Oct 20, 2025):**
```
Created during exploration:
- ENFORCE_PR_PROTOCOL.md (268 lines)
- ADDING_NEW_DOCS.md (423 lines)

Human review:
"Should these be separate or incorporated?"

Decision: Consolidate
- ENFORCE_PR_PROTOCOL → WORKING_PRINCIPLES.md
- ADDING_NEW_DOCS → docs/README.md

Result: Clean, no documentation sprawl
```

**Why This Works:**
- ✅ AI speed (prototype quickly)
- ✅ Human judgment (catch unnecessary complexity)
- ✅ Git transparency (nothing hidden)
- ✅ Discipline (delete or incorporate, never accumulate)

**The Rule:** Create freely during work, review critically before commit.

#### When to Ask vs Proceed

**Proceed Without Asking:**
- ✅ Reading documentation
- ✅ Running test queries (read-only)
- ✅ Creating report files
- ✅ Implementing approved phases
- ✅ Following established patterns

**Ask Before Proceeding:**
- ❓ Modifying database schema
- ❓ Changing component code
- ❓ Making architectural decisions
- ❓ Starting new (unapproved) phases
- ❓ Deviating from plan

**Rule:** If ERA_ECOSYSTEM_PLAN.md says to do it, proceed. If not documented, ask.

#### Specialized Workflows

**Phase 4B-2: Collaborative Review**
- See: [integration_scripts/AI_WORKFLOW_GUIDE.md](#file-integration_scriptsai_workflow_guidemd)
- 6-phase cycle: Generate batch, human reviews, AI parses, discuss, execute, document
- Human approval required for all actions

**Phase 5T: Town Hall Visualization**
- Goal: Export TH meetings as connected chain in landscape
- Process: Query enriched participants, format as nodes/edges, export to Google Sheet
- Success: 17 TH meetings, 300+ connections, interactive chain visible

#### Quick Reference

**File Locations:**
- Airtable exports: `airtable/people_export.csv`
- Fathom database: `FathomInventory/fathom_emails.db`
- Landscape data: Google Sheet ID `1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY`
- Integration scripts: `integration_scripts/*.py`

**Standard Tools:**
- Fuzzy matching: fuzzywuzzy library, 80% threshold
- Database: SQLite3, atomic transactions
- Google Sheets: gspread library or Sheets API
- Validation: Generate markdown reports

**Documentation Pattern:**
- README.md - Overview, quick start
- CONTEXT_RECOVERY.md - State snapshot, resume work
- AI_HANDOFF_GUIDE.md - AI workflow (this file)
- DEVELOPMENT.md - Development workflow (components)

#### Related Documentation

- [WORKING_PRINCIPLES.md](#file-working_principlesmd) - Complete system philosophy
- [CONTEXT_RECOVERY.md](#file-context_recoverymd) - Current system state
- integration_scripts/AI_WORKFLOW_GUIDE.md - Phase 4B-2 specific workflow
- Component READMEs - Component-specific details

**Back to:** [README.md](#file-readmemd)

---

## FILE: WORKING_PRINCIPLES.md

**Path:** `WORKING_PRINCIPLES.md`

### 1. Overview

**Purpose:** Explicit articulation of implicit principles guiding ERA Admin development

**Audience:** Humans and AIs working on the system

**This document contains:**
- Core philosophy (human-AI collaboration, vigilance against self-delusion)
- Component architecture (self-contained, modular approach)
- Documentation & recoverability (3-level hierarchy, quality principles)
- Version control & collaboration (Git/PR practices, living documents)
- Testing & validation (test before claiming success, incremental testing)
- Quality & pragmatism (trust working solutions, avoid over-engineering)
- Decision-making framework (when to pause vs proceed, debugging methodology)
- Context & communication (respect time, preserve context)

**This document IS the principles** - referenced by README, AI_HANDOFF_GUIDE, and component docs

### 2. Orientation - Where to Find What

**You are at:** System-wide principles document

**Referenced by:**
- [README.md](#file-readmemd) - Section 3 references these principles
- [AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd) - Section 3 references these principles
- Component READMEs - Section 3 references these, then adds component-specific principles

**What you might need:**
- Main entry → [README.md](#file-readmemd)
- Current state → [CONTEXT_RECOVERY.md](#file-context_recoverymd)
- AI guidance → [AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd)
- Component-specific principles → See component READMEs (they reference this, then add specifics)

### 3. Principles

**This document IS the principles.**

The content below in Section 4 contains all the principles. They are organized into:

1. **Core Philosophy** - Human-AI collaboration, vigilance against self-delusion
2. **Component Architecture** - Self-contained components, modular approach
3. **Documentation & Recoverability** - 3-level hierarchy, quality over quantity
4. **Version Control & Collaboration** - Git/PR workflow, living documents
5. **Testing & Validation** - Test before declaring success, generate evidence
6. **Quality & Pragmatism** - Working > perfect, simple > clever
7. **Decision-Making** - When to pause vs proceed, debugging methodology
8. **Context & Communication** - Respect time, preserve context

**Components should:**
- Reference this document in their Section 3
- Add component-specific principles (not duplicate these)
- Follow "System: See WORKING_PRINCIPLES.md" + "Component-specific: ..." pattern

### 4. Specialized Topics

#### 1. Core Philosophy

**Human-AI Collaboration**

**The Captain-Advisor Model:**
- **Human is Captain** - Sets direction, makes decisions, approves actions
- **AI is Critical Collaborator** - Questions assumptions, proposes alternatives, executes approved tasks
- **Not compliance, but collaboration** - AI should challenge, not just obey

**In Practice:**
- ✅ AI asks: "Should I proceed?" before implementing
- ✅ AI says: "Here's a risk you may have overlooked..."
- ✅ Human says: "Does this make sense?" expecting two answers:
  1. "Do you understand?"
  2. "What considerations am I overlooking?"
- ❌ AI assumes approval from discussion
- ❌ AI declares success without validation
- ❌ AI moves forward without explicit go-ahead

**Vigilance Against Self-Delusion**

**Proactive Validation Before Declaring Success:**
1. Think: "What test will the user apply?"
2. Run that test yourself FIRST
3. Show results, THEN ask user to verify
4. Never declare "done" without user confirmation

**Wait for Guidance:**
- User silence ≠ approval
- Discussion ≠ directive to implement
- Don't hallucinate user assent
- Don't advance without explicit approval

#### 2. Component Architecture

**Self-Contained Components**

**What is a Component:**
- **Self-documenting:** Has README.md and (for complex ones) AI_HANDOFF_GUIDE.md
- **Self-contained:** Can be understood without reading other components
- **Clear interfaces:** Exposes data via documented formats (CSV, database, API)
- **Minimal coupling:** Integration happens at integration layer, not within components

**Current Components:**
- `airtable/` - Manual membership tracking
- `FathomInventory/` - Automated meeting analysis
- `integration_scripts/` - Cross-component workflows
- `ERA_Landscape/` - Network visualization (Town Halls, interactive graph)

**Principle:** You should NOT need to understand all component internals to work at integration level.

**Modular, Incremental Approach**

**Incremental over Big-Bang:**
- Build in small, testable steps
- Validate each step before proceeding
- Update documentation as you go
- Prefer working solutions over perfect solutions

**Modular over Monolithic:**
- Components have clear boundaries
- Integration happens through documented interfaces
- Changes in one component don't cascade to others
- Each component can evolve independently

#### 3. Documentation & Recoverability

**Context Recovery is Critical**

**Problem:** Humans (and AI contexts) forget. Work gets interrupted.

**Solution:** Documentation that enables resuming work quickly.

**Three Levels of Documentation:**

*Level 1: System Overview (ERA_Admin level)*
- `README.md` - What is this? Where do I start?
- `CONTEXT_RECOVERY.md` - Current state, what's in progress, how to resume
- `AI_HANDOFF_GUIDE.md` - AI workflow and conventions
- `ERA_ECOSYSTEM_PLAN.md` - Strategic direction and integration roadmap

*Level 2: Component Level*
- Each component has `README.md` (overview, quick start)
- Complex components have `CONTEXT_RECOVERY.md` (component state)
- Complex components have `DEVELOPMENT.md` (dev workflow)

*Level 3: Implementation Details*
- Component-specific configuration files
- Inline code comments for complex logic
- Validation reports from data operations

**Navigation Rule:** Start at highest level needed. Deep-dive only when necessary.

**Documentation Quality Principles**

**Accuracy Over Aspiration:**
- Document actual state, not desired state
- Update docs when system changes
- Archive outdated docs (don't delete history)
- Mark plans as "COMPLETE" or "IN PROGRESS" clearly

**Actionable Over Descriptive:**
- Show commands to run, not just concepts
- Include expected outputs
- Provide troubleshooting steps
- Link to relevant resources

**Concise Over Comprehensive:**
- Respect reader's time
- Use bullet points over paragraphs
- Bold key information
- Reference detailed docs rather than duplicating

#### 4. Version Control & Collaboration

**Git & PR Practices**

**Protected Main Branch:**
- Never commit directly to `main`
- All changes via Pull Requests
- PRs enable review and discussion

**PR Workflow:**
1. Create feature branch: `git checkout -b fix-description`
2. Make changes, test locally
3. Commit with clear message
4. Push and create PR: `gh pr create`
5. After merge, update local: `git pull origin main`

**Commit Message Quality:**
- **First line:** Brief, actionable summary
- **Body:** What changed, why it changed, what was tested
- **Reference:** Related issues, PRs, or documents

**Git Hygiene:**
- `.gitignore` protects secrets (cookies, tokens, databases)
- Check before commit: `git status`, look for sensitive files
- Use `.gitignore` patterns for generated files

**Enforcement: Branch Protection**

Documentation alone is insufficient. Use GitHub branch protection to technically enforce PR protocol:

*Setup (one-time):*
```bash
# Via GitHub CLI:
gh api repos/OWNER/REPO/branches/main/protection -X PUT --input - << 'EOF'
{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0
  },
  "restrictions": null
}
EOF
```

*Or via web UI:*
1. Go to: https://github.com/OWNER/REPO/settings/branches
2. Add rule for `main`
3. Check: "Require pull request before merging"
4. Check: "Include administrators" (enforces for everyone)
5. Set required approvals to 0 (for solo work)

*Result:* Direct commits to main become technically impossible.

**Living Documents**

**Documents Evolve:**
- Update `CONTEXT_RECOVERY.md` after significant state changes
- Mark plans as "COMPLETE" when done
- Archive outdated docs to `historical/` with context
- Keep current docs minimal and accurate

#### 5. Testing & Validation

**Test Before Claiming Success**

**Testing Discipline:**
1. **Run the actual code** - Don't assume it works
2. **Check the output** - Verify results match expectations
3. **Test edge cases** - What happens with 0 results? Errors?
4. **Validate end-to-end** - Does the whole workflow work?

**Validation Before Declaration:**
- ❌ "I've implemented X" (untested)
- ✅ "I've implemented X. Tested with Y inputs, got Z outputs. Please verify."

**Incremental Testing**

**Test as You Build:**
- Don't build entire feature then test
- Test each component as it's built
- Catch bugs early when context is fresh
- Update CONTEXT_RECOVERY.md after each validated step

**What to Test:**
- **Syntax:** Does it run?
- **Logic:** Does it produce correct results?
- **Integration:** Do components work together?
- **Edge cases:** What breaks it?

**Validation Reports**

**Generate Evidence:**
- Create markdown reports for data operations
- Include metrics: matched, updated, inserted, errors
- Show sample data for verification
- Enable user to validate without re-running

**Example:**
```python
print(f"✅ Processed {count} records")
print(f"📊 Report saved to: enrichment_report.md")
print(f"🎯 Next step: Review report, then run Phase 5")
```

#### 6. Quality & Pragmatism

**Trust Working Solutions**

**Principles:**
- **Working > Perfect** - Ship tested, working code over elegant, untested code
- **Standard > Custom** - Use standard tools/patterns over custom solutions
- **Simple > Clever** - Prefer obvious code over clever tricks
- **Tested > Assumed** - Working code beats elegant design

**Avoid Over-Engineering:**
- Solve actual problems, not hypothetical ones
- Add complexity only when needed
- Keep configurations minimal
- Respect YAGNI (You Aren't Gonna Need It)

**Clean Implementation**

**Directory Structure:**
- Root minimal - only essential files
- `docs/` clearly identified
- `historical/` preserves context
- Each component self-contained

**Code Quality:**
- Follow existing patterns
- Use descriptive names
- Comment complex logic
- Avoid clever one-liners

#### 7. Decision-Making Framework

**When to Pause vs Proceed**

**Proceed Without Asking:**
- Reading documentation
- Running read-only test queries
- Creating validation reports
- Following documented patterns
- Implementing approved work

**Pause and Ask:**
- Modifying database schema
- Changing component architecture
- Making technology choices
- Deviating from documented plan
- Unsure about approach

**Rule:** If documented in plan for current Phase, proceed. If not documented, ask.

**When Things Go Wrong**

**Debug Methodically:**
1. **Identify scope** - Which component is failing?
2. **Read component docs** - CONTEXT_RECOVERY.md, DEVELOPMENT.md
3. **Reproduce issue** - Can you trigger it reliably?
4. **Diagnose before fixing** - Do not make changes in the uninvestigated hope that it might fix things
5. **Fix within component boundary** - Don't create cross-component dependencies
6. **Test the fix** - Verify it actually works
7. **Update documentation** - Record what broke and how you fixed it

**Escalate When:**
- Issue spans multiple components
- Architectural decision needed
- Uncertain about root cause
- Fix might break other things

#### 8. Context & Communication

**Respect Human's Valuable Time**

**Before Presenting Results:**
- Test thoroughly yourself
- Generate validation evidence
- Anticipate questions
- Provide actionable next steps

**Communication Style:**
- **Concise** - Brief but substantive
- **Factual** - Show evidence, not claims
- **Structured** - Use headings, bullets, code blocks
- **Actionable** - What should user do next?

**Preserve Context**

**For Future You/AI:**
- Update CONTEXT_RECOVERY.md after significant work
- Remember: when context recovery is needed, implicit knowledge has been lost
- Create validation reports for data operations
- Commit with detailed messages
- Archive plans when complete

**For Current Collaboration:**
- Reference docs rather than re-explaining
- Point to relevant sections: "See README.md section 3.2"
- Give clickable references when possible
- Share test outputs, not just descriptions
- Ask clarifying questions early

#### Quick Reference Checklists

**Component Self-Containment:**
- [ ] Has README.md (overview, quick start)
- [ ] Has clear input/output interfaces
- [ ] Minimal dependencies on other components
- [ ] Can be tested independently
- [ ] Documentation stays current

**Before Declaring Success:**
- [ ] Code runs without errors
- [ ] Output matches expectations
- [ ] Edge cases tested
- [ ] Validation report generated
- [ ] User confirms independent verification
- [ ] Documentation updated

**PR Quality:**
- [ ] Tested locally before pushing
- [ ] No secrets in git (check `.gitignore`)
- [ ] Clear commit messages
- [ ] Documentation updated if behavior changed
- [ ] Ready for review

#### Meta

**Living Document:** These principles evolve. When you discover new working patterns or encounter edge cases, propose updates to this document.

**Meta-Principle:** The principles themselves should follow these principles - be concise, actionable, tested in practice, and regularly validated.

**Back to:** [README.md](#file-readmemd)

---

## FILE: docs/README.md

**Path:** `docs/README.md`

### 1. Overview

**Purpose:** Documentation system design, prototyping, and maintenance

The docs/ component manages ERA_Admin's documentation infrastructure, including the wireframe-based generation system and protocols for maintaining documentation consistency.

**What this component does:**
- Maintains NAVIGATION_WIREFRAME.md (single source of truth)
- Generates production documentation via generate_from_wireframe.py
- Validates navigation integrity (no orphans, all paths work)
- Provides protocols for adding/updating documentation

**Key files:**
- NAVIGATION_WIREFRAME.md - Complete documentation content (3,400+ lines)
- generate_from_wireframe.py - Parser/generator for production docs
- update_docs.sh - Helper script for regeneration workflow
- test_navigation.py - Navigation integrity validator

### 2. Orientation - Where to Find What

**You are at:** Documentation department README

**Use this when:**
- Adding new documentation
- Updating existing docs
- Understanding doc structure
- Troubleshooting navigation

**What you might need:**
- **Parent** → [/README.md](#file-readmemd) - System overview
- **Wireframe** → NAVIGATION_WIREFRAME.md - Full documentation content
- **Principles** → [/WORKING_PRINCIPLES.md](#file-working_principlesmd) - System-wide philosophy
- **Current state** → CONTEXT_RECOVERY.md - Documentation work status

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

**Documentation-specific principles:**

**1. Single Source of Truth**
- NAVIGATION_WIREFRAME.md contains all internal documentation (see "What Goes Where" below)
- Production docs generated from wireframe
- Never edit production docs directly
- Always edit wireframe → regenerate → commit
- Exception: During active development, create docs in component folders, consolidate to wireframe before PR merge

**2. 4-Section Structure**
- Section 1: Overview (what/purpose)
- Section 2: Orientation (navigation help)
- Section 3: Principles (reference up + add specifics)
- Section 4: Specialized Topics (details)

**3. Navigation Integrity**
- No orphan documents (every doc reachable)
- Always navigate up (back to parent/root)
- Cross-references work at all levels

**4. No Redundancy**
- Reference up to system principles
- Add component-specific details only
- Don't duplicate explanations

### 4. Specialized Topics

#### Documentation Policy: What Goes Where

**ALL internal documentation goes in NAVIGATION_WIREFRAME.md:**

**Include (with full content):**
- ✅ Component READMEs (external interface)
- ✅ Architecture docs (NETWORK_ARCHITECTURE.md, DEVELOPMENT.md, etc.)
- ✅ Context recovery docs (CONTEXT_RECOVERY.md, AI_HANDOFF_GUIDE.md)
- ✅ Testing strategies (TESTING.md)
- ✅ Deployment guides (DEPLOYMENT_GUIDE.md)
- ✅ Current status docs (KNOWN_ISSUES.md, NEXT_STEPS.md)
- ✅ Design decisions (VISION.md)

**Goal:** Future developer/AI can understand entire system from wireframe alone

**Exclude → move to /historical:**
- ❌ Temporary session notes (SESSION_SUMMARY_2025-10-15.md)
- ❌ Obsolete/superseded documentation
- ❌ One-time work products
- ❌ Archived context (preserved but not active)

**Why full wireframe approach:**
1. **Internal consistency** - Update terminology everywhere at once
2. **No drift** - Production docs always match source
3. **AI context** - One file contains complete structure
4. **Navigation validation** - Automated tests catch orphans
5. **Cross-component refactoring** - See all dependencies

**Cost:** ~5 seconds per edit (edit wireframe → regenerate)
**Benefit:** Guaranteed consistency, no lost docs, complete context recovery

#### Documentation Workflow

**During active development (feature branch):**
```bash
# Create docs in component directories as you work
vim ERA_Landscape/NETWORK_ARCHITECTURE.md
git add ERA_Landscape/
git commit -m "docs: Document Town Hall physics"
```

**Before merging PR (consolidation checkpoint):**
```bash
# 1. Review what docs were created
ls -la ERA_Landscape/*.md

# 2. Identify: Internal (→ wireframe) vs Temporary (→ historical)
# Internal: Needed to understand/develop system
# Temporary: Session notes, obsolete content

# 3. Move temporary/obsolete to historical
mv ERA_Landscape/SESSION_SUMMARY_*.md historical/

# 4. Add internal docs to wireframe
vim docs/NAVIGATION_WIREFRAME.md
# Add ## FILE: sections with full content

# 5. Regenerate
./docs/update_docs.sh

# 6. Commit together
git add -A
git commit -m "docs: Consolidate ERA_Landscape docs into wireframe"
```

**PR checklist:**
- [ ] New internal docs added to NAVIGATION_WIREFRAME.md?
- [ ] Temporary/obsolete docs moved to /historical?
- [ ] Component README lists all files in "Specialized Topics"?
- [ ] Regenerated: `./docs/update_docs.sh`
- [ ] Navigation validated (all links resolve)

**Normal workflow (incremental edits to existing docs):**

```bash
# 1. Create feature branch
git checkout -b docs/update-something

# 2. Edit the wireframe
vim docs/NAVIGATION_WIREFRAME.md

# 3. Regenerate docs
./docs/update_docs.sh

# 4. Review changes
git diff

# 5. Commit and PR
git add -A
git commit -m "Update documentation: [description]"
git push origin docs/update-something
gh pr create --fill
gh pr merge --squash --delete-branch
```

**For major overhauls only:**
```bash
python3 docs/archive_and_replace.py  # Creates backup, replaces all
```

#### Adding New Documents

**Template for new document in wireframe:**

```markdown
## FILE: path/to/NEW_DOC.md

**Path:** `path/to/NEW_DOC.md`

### 1. Overview
**Purpose:** [one-line purpose]
[Full explanation]

### 2. Orientation - Where to Find What
**You are at:** [location description]
**What you might need:**
- [Parent link]
- [Related links]

### 3. Principles
**System-wide:** See [/WORKING_PRINCIPLES.md](#file-working_principlesmd)
[Document-specific principles]

### 4. Specialized Topics
[Main content]

**Back to:** [Parent](#link) | [/README.md](#file-readmemd)
```

**Steps to add:**
1. Add `## FILE:` section to NAVIGATION_WIREFRAME.md
2. Update link map in generate_from_wireframe.py (if needed)
3. Run `./docs/update_docs.sh`
4. Update parent README to reference new doc
5. Test navigation
6. Commit via PR

**Link naming convention:**
- File: `path/to/NEW_DOC.md`
- Anchor: `#file-pathtonew_docmd` (lowercase, no punctuation)

#### Helper Scripts

**update_docs.sh** - Regenerate production docs from wireframe
```bash
./docs/update_docs.sh
# - Cleans docs_generated/
# - Runs generate_from_wireframe.py
# - Copies to production locations
# - Shows git diff summary
```

**archive_and_replace.py** - Safe replacement with backup (rare use)
```bash
python3 docs/archive_and_replace.py
# - Creates timestamped backup in historical/
# - Generates rollback script
# - Replaces all 10 files
# Use for: major overhauls, structural changes
```

**test_navigation.py** - Validate navigation integrity
```bash
python3 docs/test_navigation.py docs_generated
# - Checks for orphans
# - Verifies all paths to root
# - Tests link conversion
```

#### Design Documents

**Current (Active):**
- NAVIGATION_WIREFRAME.md - Complete doc system (single source of truth)
- generate_from_wireframe.py - Production generator
- update_docs.sh - Regeneration helper

**Historical (Reference):**
- NAVIGATION_DESIGN.md - Original design rationale
- NAVIGATION_PROTOTYPE.md - Single-doc clickable prototype
- docs_prototype/ - Early experiments

#### Validation & Testing

**Pre-commit checks:**
```bash
# Regenerate and check
./docs/update_docs.sh
git diff --stat

# Test navigation
python3 docs/test_navigation.py docs_generated

# Test script references
python3 docs/test_script_references.py
```

**Validation reports:**
- WIREFRAME_VALIDATION_REPORT.md - Coverage and consistency
- NAVIGATION_TEST_RESULTS.md - Navigation integrity
- SCRIPT_COVERAGE_REPORT.md - Script reference analysis

**Back to:** [/README.md](#file-readmemd)

---

## FILE: FathomInventory/README.md

**Path:** `FathomInventory/README.md`

### 1. Overview

**Purpose:** Automatically downloads, processes, and analyzes Fathom meeting summaries

FathomInventory is one of four components in ERA_Admin. It provides a robust pipeline to convert unstructured Fathom summary emails into a structured, queryable SQLite database, enabling detailed analysis of meeting metadata and content.

**System Status:** ✅ FULLY OPERATIONAL

**What This System Does:**
1. **Discovers** new Fathom calls from jschull@e-nable.org account
2. **Shares** calls to `fathomizer@ecorestorationalliance.org` (automated receiver)
3. **Downloads** summary emails with public `/share/` URLs (no login required)
4. **Processes** emails into structured database with normalized dates (ISO format)
5. **Reports** daily status with health checks and public URLs

**Current Health:**
- ✅ **1,953 participants** tracked (1,698 validated/87%, 255 remaining)
- ✅ **3,229+ emails** processed with full metadata extraction
- ✅ **Dates normalized** to ISO format (YYYY-MM-DD) at all entry points
- ✅ **Automation active** - Daily runs at 3:00 AM via macOS launchd
- ✅ **Enhanced failure detection** - Catches authentication failures immediately

**Recent Improvements:**
- ✅ Pre-flight authentication checks (fails fast with clear errors)
- ✅ Fixed bash pipeline exit codes (no more silent failures)
- ✅ Enhanced daily reports (critical alerts separated from warnings)
- ✅ Improved error messaging (actionable remediation steps)

**Key Features:**
- **Multi-account support** - Switch between ERA and e-NABLE accounts via config
- **Experimental database mode** - Use database instead of TSV for call tracking
- **Weekly maintenance** - Fathom cookies expire frequently, refresh weekly

### 2. Orientation - Where to Find What

**You are at:** FathomInventory component README

**First-time users:**
1. Read this Overview (Section 1)
2. Follow Quick Start in Section 4
3. Run `./run_all.sh` to test the system

**Resuming work:**
1. Read [CONTEXT_RECOVERY.md](#file-fathominventorycontext_recoverymd) - Current component state
2. Check health: `python scripts/check_auth_health.py`
3. Continue from documented next steps

**Making changes:**
1. Read [DEVELOPMENT.md](DEVELOPMENT.md) - Workflow, testing, constraints
2. Follow component-specific development practices
3. Test before committing

**What you might need:**
- **Parent system** → [/README.md](#file-readmemd) - Overall ERA Admin architecture
- **System-wide status** → [/CONTEXT_RECOVERY.md](#file-context_recoverymd) - Integration status
- **Component status** → [CONTEXT_RECOVERY.md](#file-fathominventorycontext_recoverymd) - FathomInventory health
- **System principles** → [/WORKING_PRINCIPLES.md](#file-working_principlesmd) - Overall philosophy
- **Authentication** → [authentication/README.md](#file-fathominventoryauthenticationreadmemd) - Cookie and token management
- **Analysis** → analysis/README.md - AI analysis scripts for ERA meetings

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

**FathomInventory-specific:**

**1. Authentication Health Checks**
- **Pre-flight validation** - Check auth before running pipeline (fails fast)
- **Weekly refresh required** - Fathom cookies expire frequently (some daily)
- **Correct account critical** - Gmail must use `fathomizer@ecorestorationalliance.org`
- **Health monitoring** - Run `check_auth_health.py` before manual runs

**2. Pipeline Reliability**
- **Fail-fast design** - Catch authentication failures immediately, don't proceed
- **Bash exit codes** - Fixed pipeline to respect script failures
- **5-minute wait** - After sharing, wait for emails to arrive before downloading
- **Daily automation** - Runs at 3:00 AM via launchd, monitor `cron.log`

**3. Data Normalization**
- **ISO date format** - All dates as YYYY-MM-DD (entry point normalization)
- **No assumptions** - Validate and normalize at data entry, not query time
- **Consistent schema** - SQLite database with normalized participant data

**4. Self-Contained Component**
- **Works standalone** - Can be understood without reading parent docs
- **Clear interfaces** - Exposes `fathom_emails.db` and `all_fathom_calls.tsv`
- **Minimal coupling** - Integration happens at integration_scripts/ level

### 4. Specialized Topics

#### Quick Start (5 minutes)

**1. Setup Dependencies**
```bash
# Create virtual environment (if not exists)
python3 -m venv ../ERA_Admin_venv
source ../ERA_Admin_venv/bin/activate

# Install requirements
pip install -r requirements.txt
playwright install chromium
```

**2. Configure Authentication**

*For Fathom.video access:*
```bash
./scripts/refresh_fathom_auth.sh
# Follow prompts to export cookies from browser
```

*For Gmail access (CRITICAL - correct account):*

⚠️ **IMPORTANT:** Authenticate with `fathomizer@ecorestorationalliance.org`, NOT personal account

```bash
python scripts/download_emails.py
# Complete OAuth flow in browser
# Verify: Sign in as fathomizer@ecorestorationalliance.org
```

*Verify correct configuration:*
```bash
./venv/bin/python -c "
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
creds = Credentials.from_authorized_user_file('token.json')
service = build('gmail', 'v1', credentials=creds)
profile = service.users().getProfile(userId='me').execute()
expected = 'fathomizer@ecorestorationalliance.org'
print(f'✅ Correct: {expected}' if profile['emailAddress'] == expected else f'❌ WRONG: {profile[\"emailAddress\"]}')
"
```

**3. Run the System**
```bash
./run_all.sh
```

**That's it!** The system will:
- Find new Fathom calls and share them
- Wait 5 minutes for emails to arrive
- Download and process the emails
- Update the database with structured data

#### Advanced Configuration

**Multi-Account Support:**

Fathom account configuration centralized in `../era_config.py`. Switch accounts using:

*Option 1: Environment variable (temporary)*
```bash
FATHOM_ACCOUNT=era python run_daily_share.py
# Uses ERA account (ecorestorationalliance@gmail.com)

FATHOM_ACCOUNT=enable python run_daily_share.py
# Uses e-NABLE account (jschull@e-nable.org) - default
```

*Option 2: Edit era_config.py (permanent)*
```python
# In /Users/admin/ERA_Admin/era_config.py
FATHOM_ACTIVE_ACCOUNT = 'era'  # Change from 'enable' to 'era'
```

*Option 3: Override at runtime (one-off)*
```bash
python run_daily_share.py --cookies fathom_cookies_alt.json --share-email other@example.com
```

**Experimental: Database Mode**

Use database instead of TSV for call tracking:
```bash
# Enable database mode
python run_daily_share.py --use-db

# Or specify custom database
python run_daily_share.py --use-db --db custom.db
```
**Note:** TSV remains the default. Database mode is feature-flagged for testing.

#### Daily Operation

The system runs automatically at **3:00 AM daily** via macOS scheduling.

**Monitor progress:**
```bash
tail -f cron.log
```

**Check automation status:**
```bash
launchctl list | grep era
# Should show: com.era.admin.fathom if running
```

#### Weekly Maintenance (Required)

**Refresh Fathom authentication:**
```bash
./scripts/refresh_fathom_auth.sh
```

Fathom cookies expire frequently (some daily), so weekly refresh prevents authentication failures.

#### Troubleshooting

**"Authentication failed" or "redirected to login"**

*Solution:* Refresh cookies
```bash
./scripts/refresh_fathom_auth.sh
```

**"No new emails found"**

*Check:* Gmail authentication
```bash
python scripts/download_emails.py
```

**"Script hangs or times out"**

*Solution:* Check authentication health
```bash
python scripts/check_auth_health.py
```

**"Permission denied" or file errors**

*Solution:* Check file permissions
```bash
chmod 600 *.json
chmod +x *.sh
```

#### Key Files

| File | Purpose | When to Touch |
|------|---------|---------------|
| `fathom_cookies.json` | Fathom authentication | Weekly refresh |
| `credentials.json` | Google API setup | One-time setup |
| `token.json` | Gmail access | Auto-managed |
| `all_fathom_calls.tsv` | Master call registry | **Never delete** |
| `fathom_emails.db` | Processed data | View-only |
| `cron.log` | System activity | Monitor for errors |
| `analysis/` | AI analysis scripts | See analysis/README.md |

#### Data Output

**Structured database:** `fathom_emails.db`
- Meeting titles, dates, participants
- Action items and next steps counts
- Full email content and metadata

**Call registry:** `all_fathom_calls.tsv`
- Master list of all discovered calls
- Share status and timestamps

#### Getting Help

**Quick Health Check:**
```bash
python scripts/check_auth_health.py
```

**Test Individual Components:**
```bash
cd authentication
python test_all_auth.py        # Test all authentication
python test_fathom_cookies.py  # Test Fathom access only
python test_google_auth.py     # Test Gmail access only
```

**Detailed Documentation:**
- [TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md) - Complete architecture, validation, workflows
- [AUTHENTICATION_GUIDE.md](docs/AUTHENTICATION_GUIDE.md) - All auth methods and troubleshooting
- [AUTOMATION_MONITORING_GUIDE.md](docs/AUTOMATION_MONITORING_GUIDE.md) - Scheduling and monitoring
- [FAILURE_DETECTION_IMPROVEMENTS.md](docs/FAILURE_DETECTION_IMPROVEMENTS.md) - Recent reliability enhancements
- [CONFIGURATION_ERRORS.md](docs/CONFIGURATION_ERRORS.md) - Critical setup requirements and recovery

#### Component Organization

**Subdirectories:**
- [authentication/README.md](#file-fathominventoryauthenticationreadmemd) - Cookie and token management
- analysis/ - AI analysis scripts for ERA meetings (Phases 1-3)
- docs/ - Detailed technical documentation
- scripts/ - Pipeline automation scripts (30+ operational scripts)
- tests/ - Test suite (unit tests, smoke tests)

**Key Component Files:**
- [CONTEXT_RECOVERY.md](#file-fathominventorycontext_recoverymd) - Current component state
- DEVELOPMENT.md - Development workflow, testing, constraints
- BACKUP_AND_RECOVERY.md - Data backup and recovery procedures

#### Internal Architecture

**Core Modules:**
- `data_access/` - Database abstraction layer
  - `db_io.py` - SQLite database operations
  - `tsv_io.py` - TSV file I/O (legacy format support)
- `fathom_ops/` - Browser automation internals
  - `browser.py` - Playwright-based web scraping
  - `parser.py` - HTML parsing and data extraction

**Analysis Scripts (Phases 1-3):**
Located in `analysis/`:
- `batch_analyze_calls.py` - Bulk call analysis
- `sync_era_meetings.py` - ERA meeting synchronization
- `import_participants.py` - Participant data import
- `mark_era_meetings.py` - Meeting classification
- `ask_fathom_ai.py` - AI-powered analysis
- See `analysis/README.md` for details

**Maintenance Scripts:**
Located in `scripts/`:
- **Health checks:** `database_health_check.sh` - Verify DB integrity
- **Backfilling:** `backfill_public_urls.py` - Add missing URLs
- **Migrations:** `fix_*.py` - Various data fixes and schema updates
- **Utilities:** `create_thumbnails.py`, `batch_database_converter.py`
- **Monitoring:** `check_auth_health.py` - Authentication status

**Testing:**
Test suite in `tests/` directory:
- `test_smoke.py` - Basic functionality tests
- `test_browser_sanitize.py` - Cookie sanitization tests
- `test_parser_unit.py` - Parser unit tests
- Run: `pytest` or `python -m pytest`

**Back to:** [/README.md](#file-readmemd)

---

## FILE: FathomInventory/CONTEXT_RECOVERY.md

**Path:** `FathomInventory/CONTEXT_RECOVERY.md`

### 1. Overview

**Purpose:** Enable any AI or human to quickly understand FathomInventory project state and resume work

**Critical:** This file MUST be updated with every significant PR

**Project:** Fathom Inventory System  
**Repo:** https://github.com/jonschull/ERA_fathom_inventory (private)  
**Location:** `/Users/admin/ERA_Admin/FathomInventory`

**Purpose:** Automatically downloads, processes, and analyzes Fathom meeting summaries from jschull@e-nable.org account

**Production Status:** ✅ FULLY OPERATIONAL (Oct 17, 2025)

**This document contains:**
- Current system state (what's working, recent work)
- System architecture (automation pipeline)
- Key files (documentation, scripts, data)
- How to resume work (verification commands)
- Common tasks (cookie refresh, testing, PRs)
- Known issues & constraints
- Rollback procedures
- Testing guidelines
- AI-specific recovery instructions

### 2. Orientation - Where to Find What

**You are at:** FathomInventory-specific context recovery

**Use this when:**
- Resuming work after time away
- Checking component health
- Verifying automation status
- Troubleshooting issues

**Root Documentation (Read First):**
- [README.md](#file-fathominventoryreadmemd) - User guide, quick start, current status
- DEVELOPMENT.md - Developer workflow, testing, constraints
- This CONTEXT_RECOVERY.md - Context for resuming work
- BACKUP_AND_RECOVERY.md - Backup system, disaster recovery

**What you might need:**
- **Parent system** → [/README.md](#file-readmemd) - Overall ERA Admin architecture
- **System-wide context** → [/CONTEXT_RECOVERY.md](#file-context_recoverymd) - Integration status
- **Component overview** → [README.md](#file-fathominventoryreadmemd) - FathomInventory user guide
- **System principles** → [/WORKING_PRINCIPLES.md](#file-working_principlesmd) - Overall philosophy
- **Technical docs** → docs/ directory (TECHNICAL_DOCUMENTATION.md, AUTHENTICATION_GUIDE.md, etc.)

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

**Component-specific:** See [README.md](#file-fathominventoryreadmemd) Section 3

**FathomInventory Project Principles:**

1. **PR-driven development** - All changes via focused PRs
2. **Clean documentation** - Root minimal, docs/ organized, archive/ for history
3. **Fail fast** - Detect problems immediately with clear errors
4. **Weekly maintenance** - Cookie refresh is required
5. **Proactive validation** - Test before declaring success
6. **Context preservation** - Update this file with every significant change

### 4. Specialized Topics

#### Current System State (Oct 19, 2025)

**What's Working:**
- ✅ **1,953 participants** tracked in SQLite database (87% enriched from Phase 4B-2)
- ✅ **3,240+ emails** processed with full metadata
- ✅ **Database mode** active (TSV migration complete)
- ✅ **Enhanced failure detection** - catches auth failures immediately
- ✅ **Daily automation** at 3:00 AM via macOS launchd
- ✅ **Automated backups** - Local (daily 3 AM) + Google Drive (daily 4 AM)
- ✅ **Backup verification** - Daily report queries Drive API to confirm uploads
- ✅ **Fresh authentication** - cookies refreshed regularly

**Recent Work:**

*Oct 19, 2025: Automated Backup System*
- Problem: No disaster recovery if computer dies or disk fails
- Solution: 3-tier backup system with verification
  1. Local backups (daily, 7-day retention)
  2. Google Drive backups (daily at 4 AM, 30-day retention, ZIP only)
  3. Daily report verifies both tiers via Drive API
- Scripts: `backup_database.sh`, `upload_backup_to_drive.py`
- Launchd: `com.era.admin.fathom.backup_drive` (separate job at 4 AM)
- Docs: `BACKUP_AND_RECOVERY.md`
- Impact: Max data loss reduced from ∞ to 24 hours

*Oct 17, 2025: Enhanced Failure Detection*
- Problem: System failed silently for 8 days due to expired cookies
- Solution: Pre-flight checks, bash exit code fixes, enhanced alerts
- PR: #19
- Impact: Discovered 8 missed calls, system fully restored

*Oct 17, 2025: Analysis Automation (Phase 1-3)*
- 1,953 participant records from ERA meetings
- Automated daily analysis of new ERA meetings
- Database: `participants` table in `fathom_emails.db`
- See: `analysis/PHASE3_COMPLETE.md`

#### System Architecture

**Daily Automation:**
```
3:00 AM - run_all.sh (launchd: com.era.admin.fathom.run)
  ├─> Step 0: scripts/backup_database.sh
  │   ├─> SQLite backup (296MB)
  │   ├─> CSV export + compress (44MB ZIP)
  │   └─> Integrity check
  ├─> Step 1: run_daily_share.py --use-db
  │   ├─> Pre-flight auth check
  │   ├─> Scrape Fathom for new calls
  │   ├─> Share to fathomizer@ecorestorationalliance.org
  │   └─> Update fathom_emails.db (calls table)
  ├─> Step 2: Wait 5 minutes (for emails)
  ├─> Step 3: scripts/download_emails.py
  │   ├─> Fetch Gmail responses
  │   ├─> Parse with fathom_email_2_md.py
  │   └─> Update fathom_emails.db (emails table)
  └─> Step 4: scripts/send_daily_report.py
      ├─> Analyze logs for failures
      ├─> Check database health
      ├─> Verify local backup timestamp
      ├─> Query Google Drive for cloud backup
      └─> Email report to jschull@gmail.com

4:00 AM - upload_backup_to_drive.py (launchd: com.era.admin.fathom.backup_drive)
  ├─> Upload latest ZIP to Google Drive
  ├─> Auto-delete backups >30 days old
  └─> Log: ~/Library/Logs/fathom_backup_drive.log
```

#### Key Files

**Core Scripts:**
- `run_all.sh` - Main orchestrator (called by launchd)
- `run_daily_share.py` - Call discovery and sharing
- `scripts/download_emails.py` - Email fetching and processing
- `scripts/send_daily_report.py` - Daily health report (includes backup verification)
- `scripts/backup_database.sh` - Local backup creation
- `scripts/upload_backup_to_drive.py` - Google Drive upload

**Technical Documentation:**
- `docs/FAILURE_DETECTION_IMPROVEMENTS.md` - Oct 17 improvements
- `docs/TECHNICAL_DOCUMENTATION.md` - Complete system architecture
- `docs/AUTHENTICATION_GUIDE.md` - Cookie/OAuth setup
- `docs/AUTOMATION_MONITORING_GUIDE.md` - Scheduling and monitoring

**Data Files (gitignored):**
- `fathom_emails.db` - SQLite database (calls + emails + participants tables)
- `fathom_cookies_enable.json` - Fathom.video auth (e-NABLE account)
- `fathom_cookies_era.json` - Fathom.video auth (ERA account)
- `token.json` - Gmail OAuth credentials
- `credentials.json` - Google API credentials
- Active account configured in `../era_config.py`

#### How to Resume Work

**1. Verify System Health:**
```bash
cd /Users/admin/ERA_Admin/FathomInventory
git status                    # Should be on main branch
git log --oneline -5          # Check recent commits
python -m pytest tests/ -q    # Run tests (if any)
```

**2. Check Production System:**
```bash
# View recent automation runs
tail -50 cron.log

# Check scheduled job
launchctl list | grep fathom

# Verify database state
sqlite3 fathom_emails.db "SELECT COUNT(*) FROM calls;"
sqlite3 fathom_emails.db "SELECT MAX(created_at) FROM calls;"

# Check participant enrichment (Phase 4B-2)
sqlite3 fathom_emails.db "SELECT COUNT(*), data_source FROM participants GROUP BY data_source;"
```

**3. Test Authentication:**
```bash
cd authentication
python test_fathom_cookies.py    # Should show ✅ OK
python test_google_auth.py        # Should show ✅ OK
```

**4. Review Recent Activity:**
- Check GitHub PRs: https://github.com/jonschull/ERA_fathom_inventory/pulls
- Review daily email reports sent to jschull@gmail.com
- Read `docs/FAILURE_DETECTION_IMPROVEMENTS.md` for latest improvements

#### Common Tasks

**Refresh Fathom Cookies (Weekly):**
```bash
./scripts/refresh_fathom_auth.sh
# Follow prompts to export cookies from Edge browser
```

**Manual Run (Testing):**
```bash
# Run discovery and sharing
python run_daily_share.py --use-db

# Download emails (wait 5 min after sharing)
python scripts/download_emails.py

# Send daily report
python scripts/send_daily_report.py
```

**Check for Authentication Failures:**
```bash
# Pre-flight check will fail immediately if cookies expired
python run_daily_share.py --use-db
# Exit code 1 = auth failure, clear error message
```

**Create PR:**
```bash
git checkout -b feature/description
# Make changes
git add -A
git commit -m "feat: description"
git push -u origin feature/description
gh pr create --title "feat: description" --body "..."
```

**Query Participant Data (Phase 4B-2):**
```bash
sqlite3 fathom_emails.db << SQL
-- Most active ERA participants
SELECT name, COUNT(*) as meetings 
FROM participants 
WHERE source_call_title LIKE '%ERA%'
GROUP BY name ORDER BY meetings DESC LIMIT 10;

-- Enrichment status
SELECT data_source, COUNT(*) 
FROM participants 
GROUP BY data_source;
SQL
```

#### Known Issues & Constraints

**Weekly Maintenance Required:**
- **Fathom cookies expire** - Refresh weekly with `./scripts/refresh_fathom_auth.sh`
- System will detect failures immediately (as of Oct 17)

**Multi-Account Setup:**
- **Configuration:** `../era_config.py` (FATHOM_ACTIVE_ACCOUNT = 'enable')
- **e-NABLE:** `fathom_cookies_enable.json` → jschull@e-nable.org (active)
- **ERA:** `fathom_cookies_era.json` → ecorestorationalliance@gmail.com
- **Switch:** Set `FATHOM_ACCOUNT=era` env var or edit era_config.py

**Location Considerations:**
- Project at `/Users/admin/ERA_Admin/FathomInventory` (outside Dropbox)
- Previous Dropbox location had file-locking issues with launchd
- Logs at `/Users/admin/Library/Logs/` for reliability

#### Rollback Procedures

**Revert Last Commit:**
```bash
git revert HEAD
git push origin main
```

**Emergency Rollback:**
```bash
# View available tags
git tag

# Rollback to specific tag
git reset --hard v0.1.0-local-baseline

# Check backups
ls backups/
```

#### Testing Guidelines

**Before Every PR:**
- [ ] Run `python run_daily_share.py --use-db` successfully
- [ ] Check `cd authentication && python test_fathom_cookies.py` shows ✅
- [ ] Verify no secrets in git: `git status` shows no `.json` or `.db` files
- [ ] Update this CONTEXT_RECOVERY.md if system state changed
- [ ] Update README.md if user-facing behavior changed

**After Merging PR:**
- [ ] Monitor next automation run (check cron.log at 3 AM)
- [ ] Verify daily email report received
- [ ] Check database updated: `sqlite3 fathom_emails.db "SELECT COUNT(*) FROM calls;"`

#### AI-Specific Recovery Instructions

**If you are an AI resuming this work:**

1. **Read this file completely** before asking questions
2. **Check system health** with commands in "How to Resume Work" section
3. **Review recent PRs** to understand what changed
4. **Follow project principles** - especially "proactive validation"
5. **Don't assume user approval** - wait for explicit go-ahead
6. **Update this file** if you make significant changes

**Quick Context Questions to Ask Yourself:**
- What's the current system status? (Check [README.md](#file-fathominventoryreadmemd) § System Status)
- When was the last successful run? (Check cron.log)
- Are there any open PRs? (Check GitHub)
- Is authentication working? (Test with authentication/test_fathom_cookies.py)
- What was the last major change? (Check this file's history)

#### Contact

**User:** Jon Schull  
**Email:** jschull@gmail.com (receives daily reports)  
**Repo:** https://github.com/jonschull/ERA_fathom_inventory

**Last Updated:** October 19, 2025  
**Last Major Change:** Phase 4B-2 collaborative review (87% complete)  
**System Status:** ✅ Fully Automated, 1,953 participants tracked, 1,698 enriched (87%)  
**Next Maintenance:** Refresh cookies weekly

**Back to:** [FathomInventory/README.md](#file-fathominventoryreadmemd) | [/CONTEXT_RECOVERY.md](#file-context_recoverymd)

---

## FILE: FathomInventory/authentication/README.md

**Path:** `FathomInventory/authentication/README.md`

### 1. Overview

**Purpose:** Cookie and token management for FathomInventory authentication

The FathomInventory system uses a sophisticated three-tier authentication system that represents hard-won solutions to complex authentication challenges across different platforms:

1. **Google API Authentication** (`credentials.json` + `token.json`)
2. **Fathom.video Session Authentication** (`fathom_cookies.json`)
3. **OAuth Token Management** (automatic refresh mechanisms)

**This document contains:**
- The three authentication files (purpose, structure, how they work)
- Authentication flow analysis (Google API, Fathom cookies)
- Troubleshooting guide (common problems & solutions)
- Maintenance schedule (regular checks, emergency recovery)
- Security considerations (permissions, backups, access scope)
- Hard-won lessons (from historical evolution)

**Key Insight:** This authentication system represents significant engineering effort and iterative refinement to handle the complexities of modern web authentication across multiple platforms.

### 2. Orientation - Where to Find What

**You are at:** FathomInventory authentication/ subdirectory

**Use this when:**
- Setting up authentication for first time
- Troubleshooting auth failures
- Understanding cookie/token management
- Planning maintenance schedule

**What you might need:**
- **Parent component** → [../README.md](#file-fathominventoryreadmemd) - FathomInventory overview
- **Component context** → [../CONTEXT_RECOVERY.md](#file-fathominventorycontext_recoverymd) - Component state
- **System principles** → [/WORKING_PRINCIPLES.md](#file-working_principlesmd) - Overall philosophy
- **Technical docs** → ../docs/AUTHENTICATION_GUIDE.md - Comprehensive auth setup

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

**Component-specific:** See [../README.md](#file-fathominventoryreadmemd) Section 3

**Authentication-specific principles:**

**1. Hard-Won Solutions**
- Cookie sanitization for Playwright compatibility
- Auto-refresh logic prevents constant user intervention
- Graceful degradation when auth fails
- Minimal necessary permissions (read-only Gmail)

**2. Weekly Maintenance Required**
- Fathom cookies expire frequently (some daily)
- System detects failures immediately (as of Oct 17)
- Refresh weekly with `./scripts/refresh_fathom_auth.sh`

**3. Security First**
- File permissions: `chmod 600` for all auth files
- Never commit to version control (use .gitignore)
- Keep secure backups of working auth files
- Rotate credentials periodically

**4. Battle-Tested Patterns**
- Timeouts discovered through trial (Fathom page load: 60s)
- HTML selector stability (call-gallery-thumbnail remains stable)
- Process reliability monitoring (watchdog patterns)
- Authentication evolution from manual → fully automated

### 4. Specialized Topics

#### The Three Authentication Files

**1. credentials.json - Google API Client Credentials**

*Purpose:* Contains OAuth 2.0 client credentials for Google API access

*Structure:*
```json
{
  "installed": {
    "client_id": "57881875374-jtkkfj4s4cbo4dji31pun9td87gt0nba.apps.googleusercontent.com",
    "project_id": "fathomizer-email-analysis", 
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET_HERE",
    "redirect_uris": ["http://localhost"]
  }
}
```

*How it got here:*
- Created through Google Cloud Console
- Project: "fathomizer-email-analysis"
- Gmail API enabled with read-only scope
- Downloaded as client secrets file from Google Cloud Console

*Expiration:* Does not expire (client credentials are permanent)

*Usage:* Used by `download_emails.py` to initiate OAuth flow

**2. token.json - OAuth Access Token**

*Purpose:* Contains the actual OAuth token for Gmail API access

*Structure:*
```json
{
  "token": "YOUR_ACCESS_TOKEN_HERE",
  "refresh_token": "YOUR_REFRESH_TOKEN_HERE",
  "token_uri": "https://oauth2.googleapis.com/token",
  "client_id": "YOUR_CLIENT_ID_HERE",
  "client_secret": "YOUR_CLIENT_SECRET_HERE",
  "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
  "universe_domain": "googleapis.com",
  "account": "",
  "expiry": "2025-09-19T15:05:14.437249Z"
}
```

*How it got here:*
- Generated automatically by first run of `download_emails.py`
- User completed OAuth flow in browser
- Google returned access token and refresh token
- System saved both tokens to this file

*Expiration:*
- **Access token:** Expires every ~1 hour (see "expiry" field)
- **Refresh token:** Long-lived (months/years) but can be revoked
- **Auto-refresh:** System automatically refreshes access token using refresh token

*Usage:* Used by `download_emails.py` for all Gmail API calls

**3. fathom_cookies.json - Browser Session Cookies**

*Purpose:* Contains browser cookies for authenticated Fathom.video session

*Structure:* Array of cookie objects with domains, expiration dates, and values
```json
[
  {
    "domain": ".fathom.video",
    "expirationDate": 1775094135,
    "hostOnly": false,
    "httpOnly": false,
    "name": "AMP_MKTG_12e56792f7",
    "path": "/",
    "sameSite": "lax",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "JTdCJTdE"
  }
  // ... many more cookies
]
```

*How it got here:*
- Manually extracted from browser after logging into Fathom.video
- Used browser developer tools or cookie export extension
- Represents authenticated session with Fathom.video
- **Hard-won solution:** Bypasses complex Fathom authentication

*Expiration:*
- **Individual cookies expire** at different times (see expirationDate)
- **Session cookies:** Expire when browser closes
- **Persistent cookies:** Have specific expiration dates
- **No auto-refresh:** Must be manually updated when expired

*Usage:* Used by `run_daily_share.py` to access Fathom.video as authenticated user

#### Authentication Flows

**Google API (download_emails.py):** Automatic OAuth with token refresh

**Fathom Cookies (run_daily_share.py):** Manual cookie management with sanitization

#### Troubleshooting

**Common Issues:**
- credentials.json not found → Set up in Google Cloud Console
- token.json expired → Delete and re-run OAuth flow
- Fathom access denied → Refresh cookies manually
- Cookie format errors → Code handles automatically

#### Testing Scripts

**test_all_auth.py** - Test all authentication
**test_fathom_cookies.py** - Test Fathom only
**test_google_auth.py** - Test Gmail only

**Usage:**
```bash
cd authentication
python test_all_auth.py        # Test everything
python test_fathom_cookies.py  # Fathom only
python test_google_auth.py     # Gmail only
```

#### Maintenance & Security

**Weekly Tasks:**
- Check cookie expiration
- Run test scripts
- Refresh if needed

**Security:**
```bash
chmod 600 credentials.json token.json fathom_cookies.json
```

**Emergency Recovery:**
1. Backup auth files
2. Google: Delete token.json, re-run OAuth
3. Fathom: Export fresh cookies from browser
4. Test incrementally

#### Hard-Won Lessons

**From Historical Evolution:**
- Cookie sanitization critical for Playwright
- Auto-refresh prevents user intervention
- Graceful error handling essential
- Session persistence requires careful maintenance
- Browser automation can hang - monitoring essential
- Fathom selectors have remained stable

**Key Timeouts (discovered through trial):**
- Fathom page load: 60 seconds
- Authentication verification: 15 seconds
- Process inactivity: 5 minutes

**Evolution:** Manual → Automated → Fully integrated (3 phases)

**Back to:** [FathomInventory/README.md](#file-fathominventoryreadmemd) | [/README.md](#file-readmemd)

---

## FILE: airtable/README.md

**Path:** `airtable/README.md`

### 1. Overview

**Purpose:** Self-contained Airtable integration for ERA administrative functions

This component provides easy, routine access to the current ERA membership database in Airtable. It is one of four components in ERA_Admin and serves as the **ground truth** for member and donor status.

**What it does:**
- **Manual membership tracking** - 630 people (members and donors)
- **Town Hall attendance** - 17 TH columns, 324 attendance records
- **Export data** - CSV exports for cross-correlation with FathomInventory
- **Ground truth** - Source of truth for member/donor status, contact info
- **Read-only mode** - All scripts export only, no writes to Airtable

**Base Configuration:**
- **Base ID**: `appe7aXupdvB4xXzu`
- **Primary Table**: `People` (membership database)
- **API Access**: Via pyairtable library
- **Security**: READ-ONLY MODE - database modifications disabled

**Current Status:**
- ✅ **630 people** in database (+58 from Phase 4B-2 reconciliation)
- ✅ **17 Town Hall attendance columns** (manually tracked)
- ✅ **Read-only scripts** operational (export_people.py, airtable_summary.py)
- ✅ **Cross-correlation ready** (export_for_fathom_matching.py)

**Key Features:**
- **API rate limiting** - 5 requests/second for Airtable
- **Weekly updates** - Run update_all.sh before major analysis
- **Backup recommended** - Before major changes
- **Key rotation** - Regular API key rotation recommended

### 2. Orientation - Where to Find What

**You are at:** airtable component README

**First-time users:**
1. Read this Overview (Section 1)
2. Follow Quick Start in Section 4
3. Run `python export_people.py` to test

**Routine usage:**
1. Weekly: Run `./update_all.sh` to refresh data
2. Before analysis: Check `people_export.csv` timestamp
3. Cross-correlation: Use `export_for_fathom_matching.py`

**What you might need:**
- **Parent system** → [/README.md](#file-readmemd) - Overall ERA Admin architecture
- **System-wide status** → [/CONTEXT_RECOVERY.md](#file-context_recoverymd) - Integration status
- **System principles** → [/WORKING_PRINCIPLES.md](#file-working_principlesmd) - Overall philosophy
- **Integration** → [/integration_scripts/README.md](#file-integration_scriptsreadmemd) - Cross-component workflows

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

**airtable-specific:**

**1. Manual Data Entry (Ground Truth)**
- **Human-curated data** - Airtable is source of truth for member/donor status
- **Manual TH tracking** - 17 Town Hall attendance columns updated by hand
- **Keep until automated** - Continue updating TH columns until Interactive Agenda App ready (Q2 2026)
- **Validation source** - Provides baseline for fuzzy matching accuracy

**2. Export Hygiene**
- **Weekly refresh** - Run `update_all.sh` before major analysis to get latest data
- **Timestamp checks** - Verify `people_export.csv` is fresh before using
- **Backup before changes** - Save previous exports before running updates
- **Compare exports** - Use `compare_exports.py` to see what changed

**3. Read-Only Mode**
- **NO WRITES TO AIRTABLE** - All scripts configured for export only
- **Database safety** - Modifications disabled to prevent accidental changes
- **Manual updates** - All Airtable changes done via web interface
- **Future enhancement** - Bidirectional sync capabilities planned

**4. Config Security**
- **API key protection** - Stored in `config.py` (not version controlled)
- **Template provided** - `config.py.template` shows structure
- **Regular rotation** - Rotate API keys periodically
- **Rate limiting** - Respect Airtable 5 req/sec limit

### 4. Specialized Topics

#### Quick Start

**1. Setup Environment**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**2. Configure API Access**
```bash
# Copy template and add your API key
cp config.py.template config.py
# Edit config.py with your Airtable API key
```

**3. Get Current Data**
```bash
# Export all People records to CSV
python export_people.py

# Get summary statistics
python airtable_summary.py

# Export for cross-correlation with Fathom data
python export_for_fathom_matching.py
```

#### Core Scripts

**export_people.py** - Export People table to CSV with all fields
- Output: `people_export.csv`
- Contains: All 630 people with all fields
- Use: Primary data source for analysis

**airtable_summary.py** - Generate database statistics and health check
- Output: `airtable_summary.txt`
- Contains: Record counts, field summaries, data quality metrics
- Use: Quick health check before major work

**export_for_fathom_matching.py** - Export optimized for name matching
- Output: `people_for_matching.csv`
- Contains: Cleaned names, member status, donor flags
- Use: Cross-correlation with FathomInventory participants

**config.py** - Centralized configuration and credentials
- Contains: Base ID, API key, table names
- Security: NOT version controlled (use config.py.template)

#### Data Files

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `people_export.csv` | Latest full export | Weekly or before analysis |
| `people_for_matching.csv` | Cleaned names for matching | Before Phase 4B runs |
| `airtable_summary.txt` | Latest database statistics | Weekly |
| `config.py` | API credentials | One-time setup, rotate periodically |

#### Routine Usage

**Daily/Weekly Updates:**
```bash
# Quick update - get latest data
./update_all.sh

# Check what changed
python compare_exports.py people_export.csv people_export_previous.csv
```

**Cross-Correlation with Fathom:**
```bash
# Prepare Airtable data for matching
python export_for_fathom_matching.py

# Run cross-correlation (from integration_scripts/)
cd ../integration_scripts
python cross_correlate.py
```

#### Integration Points

**With FathomInventory:**
- **Name matching** - Between Airtable People and Fathom participants
- **Enrichment** - Add membership status, donor flags to Fathom data
- **Identification** - Find active participants not yet in membership database
- **Validation** - Airtable provides ground truth for fuzzy matching accuracy

**With ERA Admin Workflows:**
- **Member communication** - Export email lists for outreach
- **Donor tracking** - Identify and track donor engagement
- **Engagement patterns** - Analyze TH attendance over time
- **Geographic distribution** - Map member locations

**With integration_scripts:**
- Phase 4B-1: Automated fuzzy matching (364 participants enriched)
- Phase 4B-2: Collaborative review (409 validated, 58 new people added)
- Phase 5T: Town Hall visualization (ready when 95%+ complete)

#### Maintenance

**Keep Data Fresh:**
- Run `./update_all.sh` weekly or before major analysis
- Monitor API rate limits (5 requests/second for Airtable)
- Backup exports before major changes
- Check timestamps on CSV files before using

**Security & Data Protection:**
- ✅ **READ-ONLY MODE** - All scripts configured for data export only
- ✅ **NO WRITES TO AIRTABLE** - Database modifications disabled
- ✅ **API key security** - Stored in `config.py` (not version controlled)
- ✅ **Regular key rotation** - Recommended for security
- ✅ **Backup recommended** - Before major changes

**Troubleshooting:**

*"API key error" or "Authentication failed"*
- Check `config.py` has correct API key
- Verify API key hasn't expired
- Rotate key in Airtable web interface if needed

*"Rate limit exceeded"*
- Scripts respect 5 req/sec limit
- Wait a few minutes and try again
- Reduce frequency if running multiple scripts

*"Export file empty or outdated"*
- Re-run `python export_people.py`
- Check `people_export.csv` timestamp
- Verify Airtable base accessible

#### Future Enhancements

- [ ] Automated daily sync with ERA_Admin automation
- [ ] Real-time change detection
- [ ] Bidirectional sync capabilities
- [ ] Integration with email systems
- [ ] Advanced matching algorithms for name variations

#### File Organization

**Core Scripts:**
- `export_people.py` - Full People table export
- `airtable_summary.py` - Database statistics
- `export_for_fathom_matching.py` - Matching-optimized export
- `cross_correlate.py` - Name matching analysis
- `compare_exports.py` - Track changes between exports
- `config.py` - API configuration (not in git)

**Data Files:**
- `people_export.csv` - Latest full export (630 people)
- `people_for_matching.csv` - Cleaned for fuzzy matching
- `airtable_summary.txt` - Database statistics
- `cross_correlation_report.txt` - Match analysis results

**Utilities:**
- `requirements.txt` - Python dependencies (pyairtable)
- `config.py.template` - Configuration template
- `update_all.sh` - Run all exports and updates
- `SAFETY_NOTICE.md` - Read-only mode explanation
- `venv/` - Virtual environment (created on setup)

**Back to:** [/README.md](#file-readmemd)

---

## FILE: integration_scripts/README.md

**Path:** `integration_scripts/README.md`

### 1. Overview

**Purpose:** Scripts for reconciling data between ERA's various systems

This component provides cross-component integration workflows for enriching participant data. It is one of four components in ERA_Admin and serves as the **integration layer** connecting FathomInventory (AI-generated) with Airtable (human-curated).

**The Problem:**
ERA has people scattered across multiple systems:
- **Fathom**: 1,953 video call participants (AI-generated names, often misspelled)
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

*Phase 4B-2* ✅ 87% COMPLETE (Oct 20, 2025)
- 409 participants validated via collaborative review (8 rounds)
- 58 new people added to Airtable (+10% growth)
- 255 participants remain (~5 more rounds to 95%)
- Production-ready workflow established

*Phase 4B-3* ⏭️ NEXT
- Add Airtable-only members to Fathom
- Ready when Phase 4B-2 reaches 95%+

*Phase 5T* ⭐ AFTER 4B-2
- Town Hall visualization in ERA Landscape
- Export meeting chain to Google Sheet

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

**Resuming Phase 4B-2 work:**
1. Read [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - Component state
2. Read [AI_WORKFLOW_GUIDE.md](AI_WORKFLOW_GUIDE.md) - AI-specific workflow
3. Check PHASE4B2_PROGRESS_REPORT.md - 8-round analysis
4. Continue from documented next steps

**AI assistants:**
1. Read [AI_WORKFLOW_GUIDE.md](AI_WORKFLOW_GUIDE.md) FIRST
2. 6-phase collaboration cycle explained
3. Mental states for each phase
4. Common patterns & decision trees

**What you might need:**
- **Parent system** → [/README.md](#file-readmemd) - Overall ERA Admin architecture
- **System-wide status** → [/CONTEXT_RECOVERY.md](#file-context_recoverymd) - Integration status
- **Component state** → [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - Phase 4B status
- **System principles** → [/WORKING_PRINCIPLES.md](#file-working_principlesmd) - Overall philosophy
- **Phase progress** → PHASE4B2_PROGRESS_REPORT.md - 8-round detailed analysis
- **AI workflow** → [AI_WORKFLOW_GUIDE.md](AI_WORKFLOW_GUIDE.md) - Collaborative review workflow
- **FathomInventory** → [/FathomInventory/README.md](#file-fathominventoryreadmemd) - Participant database
- **Airtable** → [/airtable/README.md](#file-airtablereadmemd) - Member database

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

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

**Phase 4B-1 (Re-run to test):**
```bash
cd /Users/admin/ERA_Admin
source ERA_Admin_venv/bin/activate
python3 integration_scripts/phase4b1_enrich_from_airtable.py
```
Opens HTML table → Review → Export CSV → Process

**Phase 4B-2 (Current - 8 rounds completed, 87% done):**
```bash
# 1. Generate batch (next 25 people)
python3 integration_scripts/generate_batch_data.py
python3 integration_scripts/generate_phase4b2_table.py

# 2. Review in browser → Export CSV

# 3. Parse and flag custom comments
python3 integration_scripts/parse_phase4b2_csv.py <csv_file>
# Discuss custom comments with AI

# 4. Execute approved actions
python3 integration_scripts/execute_roundN_actions.py

# 5. Document results
# Update PHASE4B2_PROGRESS_REPORT.md
```

Includes Gmail research, interactive HTML, collaborative review.

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

**Phase 4B-2: Collaborative Review** ✅ 87% COMPLETE (Oct 20, 2025)

*What we built:*
- Interactive HTML table generator with Gmail integration
- CSV parser for collaborative decision-making
- Automated execution scripts with safety checks
- Reusable Airtable addition module

*Results (8 rounds):*
- **409 participants validated** (~51 avg per round)
- **58 new people added to Airtable** (+10% growth)
- **198 actions executed** (merges, adds, drops)
- **255 participants remain** (87% complete, up from 64%)
- **Process stabilized** - production-ready workflow

*Key achievements:*
- Handled phone numbers as names (3 cases)
- Resolved device names (John's iPhone, etc.)
- Merged organization names to people
- Fixed Bio field usage (now empty, provenance in Provenance field)
- Processed joint entries, duplicates, variants

*Files:*
- `generate_batch_data.py` - Select next 25 people
- `generate_phase4b2_table.py` - Create HTML review interface
- `parse_phase4b2_csv.py` - Parse decisions, flag custom comments
- `execute_roundN_actions.py` - 8 round execution scripts
- `add_to_airtable.py` - Reusable addition module
- `gmail_research.py` - Gmail context retrieval

*Documentation:*
- **PHASE4B2_PROGRESS_REPORT.md** - Complete 8-round analysis
- **AI_WORKFLOW_GUIDE.md** - Step-by-step for AI assistants

**Phase 4B-3: Add Airtable-Only Members** ⏭️ NEXT

*Goal:* Insert Airtable members who haven't appeared in Fathom videos yet.

*Readiness:* Phase 4B-2 is 87% complete (255 remaining). Estimated 5 more rounds to reach 95%+ before starting Phase 4B-3.

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
- **Airtable** (via [airtable/README.md](#file-airtablereadmemd))
  - `people_export.csv` - 630 members (ground truth)
  - `people_for_matching.csv` - Cleaned for fuzzy matching

- **FathomInventory** (via [FathomInventory/README.md](#file-fathominventoryreadmemd))
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

**Back to:** [/README.md](#file-readmemd)

---

## FILE: integration_scripts/AI_WORKFLOW_GUIDE.md

**Path:** `integration_scripts/AI_WORKFLOW_GUIDE.md`

### 1. Overview

**For:** AI assistants stepping into Phase 4B-2 mid-stream  
**Purpose:** Make the human-AI collaboration workflow explicit  
**Audience:** A "naive AI" without conversation history

**Mental Model: What This Process Is**

**NOT traditional automation** - This is **collaborative data curation**

You are not trying to solve this alone. You are:
1. **Generating data** for human review
2. **Researching** unclear cases
3. **Discussing** ambiguous decisions
4. **Executing** approved actions safely

**Key mindset:** The human makes final decisions. You provide research, suggestions, and execution capability.

**This document contains:**
- The 6-phase collaboration cycle
- Mental states for each phase
- What to do vs what NOT to do
- Common patterns and decision trees
- Critical rules and troubleshooting

### 2. Orientation - Where to Find What

**You are at:** integration_scripts AI workflow guide (Phase 4B-2 specific)

**Use this when:**
- Resuming Phase 4B-2 collaborative review work
- Understanding the human-AI workflow
- Learning what requires human approval
- Troubleshooting workflow issues

**What you might need:**
- **Parent component** → [README.md](#file-integration_scriptsreadmemd) - integration_scripts overview
- **Phase progress** → PHASE4B2_PROGRESS_REPORT.md - 8-round analysis
- **General AI guidance** → [/AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd) - System-wide AI workflow
- **System principles** → [/WORKING_PRINCIPLES.md](#file-working_principlesmd) - Overall philosophy
- **Root context** → [/CONTEXT_RECOVERY.md](#file-context_recoverymd) - System state

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

**General AI workflow:** See [/AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd)

**Phase 4B-2 specific principles:**

**1. Collaborative Data Curation**
- NOT black-box automation - human-AI partnership
- AI proposes, human disposes
- Discussion before action on ambiguous cases

**2. Human Approval Required**
- Parse CSV and flag custom comments
- STOP if custom comments found
- Discuss with human before proceeding
- Execute only approved actions

**3. 6-Phase Cycle**
1. AI generates review interface
2. Human reviews & exports CSV
3. AI parses & flags issues
4. Human-AI discuss ambiguous cases
5. AI executes approved actions
6. Document results & commit

**4. Safety First**
- Backup database before modifications
- Transaction safety (rollback on error)
- Test queries before updates
- Show results, then ask for confirmation

### 4. Specialized Topics

#### The 6-Phase Collaboration Cycle

**Phase 1: AI Generates Review Interface**

*Your role:* Create sortable HTML table for human review

```bash
python3 generate_batch_data.py          # Select next 25 people
python3 generate_phase4b2_table.py      # Create HTML interface
```

*What you're doing:*
- Selecting 25 unenriched participants from Fathom database
- Fuzzy matching against Airtable people
- Creating interactive HTML with video links, Gmail research, match suggestions

*Mental state:* You're setting up the workspace. Don't make decisions yet.

**Phase 2: Human Reviews & Exports**

*Human's role:* Review your suggestions, research unclear cases, make decisions

*What they do:*
1. Open HTML in browser
2. Click video links (🎬) to verify identities
3. Use Gmail research for unknown people
4. Add comments with decisions (merge with: Name, drop, add to airtable)
5. Check/uncheck ProcessThis boxes
6. Mark Probe boxes for unclear items
7. Export to CSV

*Your role during this:* **WAIT.** Don't process anything yet.

**Phase 3: AI Parses & Flags Issues**

*Your role:* Parse CSV and identify what needs discussion

```bash
python3 parse_phase4b2_csv.py <csv_file>
```

*What to look for:*

**Standard comments (auto-processable):**
- `merge with: Name`
- `drop`
- `add to airtable`
- `ignore`

**Custom comments (need discussion):**
- Anything that doesn't match standard patterns
- Names without "merge with:" prefix
- Notes with context (e.g., "ERA Member", "Organization: X")
- ProcessThis=YES with custom comment = **REQUIRES DISCUSSION**

*Mental state:* You're a quality checker. Flag anything ambiguous.

**CRITICAL:** If `parse_phase4b2_csv.py` shows custom comments, **STOP and discuss with user**. Do not proceed to execution.

**Phase 4: Human-AI Discussion**

*Your role:* Clarify ambiguous cases collaboratively

*What happens:*
- Human explains complex cases
- You ask clarifying questions
- Together decide on actions
- You update understanding for future rounds

*Mental state:* You're learning the patterns. Edge cases refine the workflow.

**Phase 5: AI Executes Approved Actions**

*Your role:* Execute only what human approved

```bash
python3 execute_roundN_actions.py       # N = current round number
```

*What you do:*
- Backup database first
- Execute merge/drop/add actions
- Use transactions (rollback on error)
- Show results before committing

*Mental state:* You're the executor. Follow instructions precisely.

**CRITICAL:** Never execute without human confirmation after showing results.

**Phase 6: Document & Commit**

*Your role:* Update documentation and commit changes

*What to do:*
1. Update PHASE4B2_PROGRESS_REPORT.md with round results
2. Commit all changes with descriptive message
3. Push to GitHub
4. Update docs/CONTEXT_RECOVERY.md if significant change

*Mental state:* You're the scribe. Preserve context for future sessions.

#### Common Patterns & Decision Trees

**Pattern: Phone Number as Name**
- Example: "773-555-1234"
- Human adds: "merge with: John Doe"
- Action: Merge participant to John Doe in Fathom DB

**Pattern: Device Name**
- Example: "John's iPhone"
- Human adds: "merge with: John Magugu"
- Action: Merge to correct person

**Pattern: Organization Name**
- Example: "EnableCommunity"
- Human adds: "merge with: Jon Schull" (who represents org)
- Action: Merge to person, note provenance

**Pattern: Ambiguous Name**
- Example: "Ana" (could be Ana Calderon or Ana Martinez)
- Human adds: "Probe" box checked, custom comment
- Action: **STOP** - Discuss with human using Gmail research

**Pattern: Obvious Junk**
- Example: "Test Meeting", "unknown"
- Human adds: "drop"
- Action: Delete from Fathom DB

#### Critical Rules

**NEVER:**
- Execute without human approval
- Assume custom comments are standard
- Skip backup before database modifications
- Commit without testing
- Move to next phase without completing current

**ALWAYS:**
- Stop if parse_phase4b2_csv.py shows custom comments
- Show results before asking for confirmation
- Use transactions (rollback on error)
- Document in PHASE4B2_PROGRESS_REPORT.md
- Update CONTEXT_RECOVERY.md if state changed significantly

#### Troubleshooting

**"Custom comments found" - What to do?**
1. Review the comments in parse output
2. Ask human to clarify each custom comment
3. Update your understanding
4. Proceed only after human confirms actions

**"Database update failed" - Recovery:**
1. Transaction should have rolled back automatically
2. Check database integrity
3. Restore from backup if needed
4. Investigate root cause before retry

**"Unsure about action" - When in doubt:**
1. ASK the human
2. Show your reasoning
3. Propose options
4. Wait for decision

#### Success Metrics (8 Rounds Complete)

- 409 participants validated
- 58 new people added to Airtable (+10% growth)
- 198 actions executed safely
- 87% completion (1,698/1,953)
- Production-ready workflow established

#### Quick Reference

**Commands:**
```bash
# Phase 1: Generate
python3 generate_batch_data.py
python3 generate_phase4b2_table.py

# Phase 3: Parse
python3 parse_phase4b2_csv.py <csv_file>

# Phase 5: Execute
python3 execute_roundN_actions.py
```

**Files:**
- `generate_batch_data.py` - Select next 25 people
- `generate_phase4b2_table.py` - Create HTML review interface
- `parse_phase4b2_csv.py` - Parse decisions, flag custom comments
- `execute_roundN_actions.py` - Execute approved actions
- `add_to_airtable.py` - Reusable Airtable addition module
- `gmail_research.py` - Gmail context retrieval
- `PHASE4B2_PROGRESS_REPORT.md` - 8-round analysis

**Key Insight:** This workflow represents significant learning from 8 rounds. The patterns discovered (phone numbers, devices, organizations) are now codified. Future rounds should be smoother.

**Back to:** [integration_scripts/README.md](#file-integration_scriptsreadmemd) | [/README.md](#file-readmemd)

---

## Script Extraction Pattern

```python
# Parse this file to generate structure:
import re

pattern = r'^## FILE: (.+\.md)$'
# Extract path, content until next ## FILE:
# Create directories, write files
# Validate all links resolve
```

**Validation checklist:**

- [ ] All links resolve to ## FILE: sections
- [ ] Every component has 4 sections
- [ ] Principles reference, don't duplicate
- [ ] Specialized Topics list all files
- [ ] Bidirectional navigation works

**Ready for script generation when validated.**
