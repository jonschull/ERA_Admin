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
   - Live at: https://jonschull.github.io/ERA_Landscape_Static/
   - Organizations, people, projects + relationships

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

**ERA_Landscape_Static** (sibling project)
- Purpose: Interactive network visualization
- Content: 350+ organizations, people, projects + relationships
- Technology: Static HTML/JS, Google Sheets data source
- Live: https://jonschull.github.io/ERA_Landscape_Static/
- Git: https://github.com/jonschull/ERA_Landscape_Static
- Read: ERA_Landscape_Static/README.md, VISION.md

#### Quick Start

**Check current state:**
```bash
# View Airtable exports
cd airtable
python export_people.py
# Exports 630 people to people_export.csv

# View landscape
open https://jonschull.github.io/ERA_Landscape_Static/
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
- ✅ **Landscape deployed** - https://jonschull.github.io/ERA_Landscape_Static/
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
- Live Site: https://jonschull.github.io/ERA_Landscape_Static/
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
open https://jonschull.github.io/ERA_Landscape_Static/
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
- Landscape details: ERA_Landscape_Static/README.md
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
- ERA_Landscape_Static/README.md - Visualization deployment

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
   └─> Landscape visualization? Read ERA_Landscape_Static/README.md

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
4. ERA Landscape - Visualization (self-contained in `ERA_Landscape_Static/`)

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

Philosophy, Git workflow, testing, documentation practices

### 2. Orientation - Where to Find What

**You are at:** System-wide principles document

**What you might need:**
- Main entry → [README.md](#file-readmemd)
- Current state → [CONTEXT_RECOVERY.md](#file-context_recoverymd)
- AI guidance → [AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd)
- Component-specific principles → See component READMEs

### 3. Principles

*This document IS the principles*

### 4. Specialized Topics

**Human-AI Collaboration:**

- Captain-advisor model
- Vigilance against self-delusion

**Component Architecture:**

- Independence, boundaries, centralized config

**Git/PR Workflow:**

```
git checkout -b feature
git commit -m "message"
gh pr create
```

**Testing:** Validate before declaring done

**Documentation:** 4-section structure, reference don't duplicate

**Back:** [README.md](#file-readmemd)

---

## FILE: FathomInventory/README.md

**Path:** `FathomInventory/README.md`

### 1. Overview

FathomInventory is one of three components in ERA_Admin.

**Purpose:** Automated meeting analysis system

**What it does:**
1. Discovers new Fathom calls
2. Shares to automated receiver
3. Downloads summary emails
4. Processes into structured database
5. Reports daily status

### 2. Orientation - Where to Find What

**You are at:** FathomInventory component README

**What you might need:**
- Parent README → [/README.md](#file-readmemd)
- System-wide status → [/CONTEXT_RECOVERY.md](#file-context_recoverymd)
- Component status → [CONTEXT_RECOVERY.md](#file-fathominventorycontext_recoverymd)
- System principles → [/WORKING_PRINCIPLES.md](#file-working_principlesmd)
- Component principles → See section 3 below

### 3. Principles

**System:** See [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

**FathomInventory-specific:**

- Authentication health checks
- Pipeline reliability
- Date normalization (ISO format)

### 4. Specialized Topics

**Subdirectories:**

- [authentication/README.md](#file-fathominventoryauthenticationreadmemd)
- analysis/
- docs/

**Files:**

- [CONTEXT_RECOVERY.md](#file-fathominventorycontext_recoverymd)
- DEVELOPMENT.md
- BACKUP_AND_RECOVERY.md

**Back:** [/README.md](#file-readmemd)

---

## FILE: FathomInventory/CONTEXT_RECOVERY.md

**Path:** `FathomInventory/CONTEXT_RECOVERY.md`

### 1. Overview

**Purpose:** FathomInventory-specific status and context

**This document contains:** Component health, recent changes, integration status

### 2. Orientation - Where to Find What

**You are at:** FathomInventory-specific context

**What you might need:**
- Parent README → [README.md](#file-fathominventoryreadmemd)
- System-wide context → [/CONTEXT_RECOVERY.md](#file-context_recoverymd)
- Component overview → [README.md](#file-fathominventoryreadmemd)

### 3. Principles

**See:** [/WORKING_PRINCIPLES.md](#file-working_principlesmd) and [README.md](#file-fathominventoryreadmemd)

### 4. Specialized Topics

**Component status:**

- Automation: ✅ Running
- Health: ✅ All checks passing
- Recent: Oct 20 test path fixed

**Back:** [FathomInventory/README.md](#file-fathominventoryreadmemd)

---

## FILE: FathomInventory/authentication/README.md

**Path:** `FathomInventory/authentication/README.md`

### 1. Overview

FathomInventory authentication subdirectory

**Purpose:** Cookie and token management for Fathom authentication

**Key files:** credentials.json, token.json, fathom_cookies_*.json (all gitignored)

### 2. Orientation - Where to Find What

**You are at:** FathomInventory/authentication guide

**What you might need:**
- Parent README → [../README.md](#file-fathominventoryreadmemd)
- Root README → [/README.md](#file-readmemd)
- Component status → ../CONTEXT_RECOVERY.md
- System principles → [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

**When to use:** Cookies expired, token refresh, account switching

### 3. Principles

**System:** [/WORKING_PRINCIPLES.md](#file-working_principlesmd)
**Component:** [../README.md](#file-fathominventoryreadmemd)

**Auth-specific:**

- Security first (never commit credentials)
- Pre-flight checks
- Multiple account support

### 4. Specialized Topics

**Guides:**

- cookie_export_guide.md
- google_api_setup_guide.md

**Back:** [FathomInventory](#file-fathominventoryreadmemd) | [/README](#file-readmemd)

---

## FILE: airtable/README.md

**Path:** `airtable/README.md`

### 1. Overview

airtable is one of three components in ERA_Admin.

**Purpose:** Manual membership tracking and exports

**What it does:**
- Manual database of ERA members and donors
- Export data for cross-correlation with FathomInventory
- Ground truth for member/donor status

### 2. Orientation - Where to Find What

**You are at:** airtable component README

**What you might need:**
- Parent README → [/README.md](#file-readmemd)
- System-wide status → [/CONTEXT_RECOVERY.md](#file-context_recoverymd)
- System principles → [/WORKING_PRINCIPLES.md](#file-working_principlesmd)
- Component principles → See section 3 below

### 3. Principles

**System:** See [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

**airtable-specific:**

- Manual data entry (ground truth)
- Export hygiene
- Config security

### 4. Specialized Topics

**Files:**

- config.py.template
- export_people.py
- SAFETY_NOTICE.md

**Back:** [/README.md](#file-readmemd)

---

## FILE: integration_scripts/README.md

**Path:** `integration_scripts/README.md`

### 1. Overview

integration_scripts is one of three components in ERA_Admin.

**Purpose:** Cross-component bridging for participant enrichment

**What it does:** Bridges FathomInventory ↔ Airtable to enrich participant data

**Phases:**

- Phase 4B-1: Automated fuzzy matching
- Phase 4B-2: Collaborative human-AI review

### 2. Orientation - Where to Find What

**You are at:** integration_scripts component README

**What you might need:**
- Parent README → [/README.md](#file-readmemd)
- System-wide status → [/CONTEXT_RECOVERY.md](#file-context_recoverymd)
- Phase progress → PHASE4B2_PROGRESS_REPORT.md
- System principles → [/WORKING_PRINCIPLES.md](#file-working_principlesmd)
- Which README to read → See section 4 below

### 3. Principles

**System:** See [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

**integration-specific:**

- Collaborative human-AI workflow
- Data validation with human approval

### 4. Specialized Topics

**Which README:**

- This file: Overview
- README_PHASE4B.md: System details
- README_PHASE4B_DETAILED.md: Technical deep dive

**AI Workflow:**

- [AI_WORKFLOW_GUIDE.md](#file-integration_scriptsai_workflow_guidemd) - Phase 4B-2 specific

**Back:** [/README.md](#file-readmemd)

---

## FILE: integration_scripts/AI_WORKFLOW_GUIDE.md

**Path:** `integration_scripts/AI_WORKFLOW_GUIDE.md`

### 1. Overview

integration_scripts → AI_WORKFLOW_GUIDE

**Purpose:** Specialized 6-phase workflow for Phase 4B-2 collaborative data review

**Scope:** Phase 4B-2 specifics (for general AI workflow, see /AI_HANDOFF_GUIDE.md)

### 2. Orientation - Where to Find What

**You are at:** integration_scripts AI workflow guide (Phase 4B-2 specific)

**What you might need:**
- Parent README → [README.md](#file-integration_scriptsreadmemd)
- Root README → [/README.md](#file-readmemd)
- General AI guidance → [/AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd)
- System principles → [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

### 3. Principles

**System:** [/WORKING_PRINCIPLES.md](#file-working_principlesmd)
**AI-general:** [/AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd)

**Phase 4B-2:** 6-phase cycle, human approval required

### 4. Specialized Topics

[6-phase workflow details]

**Back:** [integration_scripts](#file-integration_scriptsreadmemd) | [/README](#file-readmemd)

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
