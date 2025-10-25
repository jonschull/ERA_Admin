# ERA Admin Documentation Wireframe

**Purpose:** Script-parseable wireframe for generating folder structure
**Format:** Each `## FILE: path` section → create that file
**Date:** October 24, 2025

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

## FILE: .github/PR_CHECKLIST.md

**Path:** `.github/PR_CHECKLIST.md`

# PR Checklist

Quick reference for creating pull requests in ERA_Admin.

## Before You Start

```bash
# Create feature branch from main
git checkout main
git pull
git checkout -b feature/brief-description
```

## During Development

- Edit files normally
- Commit to your feature branch
- **If you edit NAVIGATION_WIREFRAME.md:** Run `./docs/update_docs.sh` to regenerate

## Before Push

The pre-push hook automatically checks:
- ✓ Not on main branch
- ✓ Docs in sync (if wireframe edited, production docs regenerated)
- ✓ Navigation integrity passes

## Create PR

```bash
git push origin feature/your-branch
gh pr create
```

GitHub will show a checklist in the PR description.

## After Merge

```bash
git checkout main
git pull
git branch -d feature/your-branch  # cleanup
```

## When Blocked

**"Can't commit to main"**
→ You're on main. Create feature branch: `git checkout -b feature/name`

**"Docs out of sync"**
→ Run `./docs/update_docs.sh` to regenerate from wireframe

**"Navigation test failed"**
→ Run `python3 docs/test_navigation.py` for details

**"Pre-push hook not installed"**
→ See WORKING_PRINCIPLES.md "Enforcement: Branch Protection"

---

📖 **Full details:** [WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)  
🏗️ **Architecture:** [README.md](../README.md)  
🔄 **Current state:** [CONTEXT_RECOVERY.md](../CONTEXT_RECOVERY.md)

---

## FILE: .github/pull_request_template.md

**Path:** `.github/pull_request_template.md`

## Description

<!-- Brief description of what this PR does -->

## Pre-Push Verification

<!-- These are checked by pre-push hook - should already pass -->

- [ ] On feature branch (not main)
- [ ] Documentation synced (if NAVIGATION_WIREFRAME edited, ran `./docs/update_docs.sh`)
- [ ] Navigation integrity passes (`python3 docs/test_navigation.py`)

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (please describe):

## Testing

<!-- How was this tested? -->

---

📖 **First time contributing?** See [PR Checklist](.github/PR_CHECKLIST.md)

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
- **Phase 4B-2:** ✅ COMPLETE - 459 participants validated (11 batches, Oct 23, 2025)
- **Phase 5T:** READY - Town Hall visualization (script reinstated)
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
- Records: 682 participants (459 validated/67%, 223 new/unprocessed)
- Automation: Daily at 3 AM via launchd
- Status: ✅ Operational
- Read: [FathomInventory/README.md](#file-fathominventoryreadmemd)

**[airtable/](../airtable/)** - Manual membership tracking
- Purpose: Membership database, donor tracking, TH attendance
- Records: 630 people (+59 from Phase 4B-2), 17 TH attendance columns
- Scripts: Read-only exports, cross-correlation with Fathom
- Status: ✅ Operational
- Read: [airtable/README.md](#file-airtablereadmemd)

**[integration_scripts/](../integration_scripts/)** - Cross-component bridges
- Purpose: Enrich Fathom data with Airtable information
- Phase 4B-1: ✅ Automated fuzzy matching (364 enriched)
- Phase 4B-2: ✅ COMPLETE - 459 participants validated (11 batches, Oct 23, 2025)
- Phase 5T: READY - export_townhalls_to_landscape.py reinstated
- Read: [integration_scripts/README.md](#file-integration_scriptsreadmemd)

**[ERA_Landscape/](../ERA_Landscape/)** - Interactive network visualization
- Purpose: Network graph of ERA ecosystem
- Content: 350+ organizations, people, projects + relationships
- Technology: Static HTML/JS, Google Sheets data source, vis.js
- Live: https://jonschull.github.io/ERA_Admin/ERA_Landscape/
- Status: ✅ Operational
- Read: ERA_Landscape/README.md, NETWORK_ARCHITECTURE.md, VISION.md
- Special: 65 fixed Town Hall nodes at periphery

**[future_discipline/](../future_discipline/)** 🔬 - Experimental discipline investigations
- Purpose: Lessons learned from Phase 4B-2, proposed architectures
- Content: AI discipline failures, drone architecture proposal
- Status: Experimental / Future Investigation
- Context: 650+ participants across 11 batches revealed systematic AI discipline challenges
- Read: [future_discipline/README.md](#file-future_disciplinereadmemd)

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

**Run integration (Phase 5T - Town Hall Visualization):**
```bash
# Verify configuration
python era_config.py

# Export Town Halls to landscape
cd integration_scripts
python3 export_townhalls_to_landscape.py

# Exports 17 TH meetings + 459 validated participants
# Updates Google Sheet → landscape auto-refreshes
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
- **Fathom:** 682 participants (459 validated/67%)
- **Validation:** 61.5% baseline → 100% Phase 4B-2 scope complete
- **Landscape:** 350+ nodes
- **Integration:** Phase 4B-2 ✅ complete, Phase 5T ready

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
- ✅ **Airtable exports operational** - 630 people (+59 from Phase 4B-2), 17 TH attendance columns
- ✅ **Landscape deployed** - https://jonschull.github.io/ERA_Admin/ERA_Landscape/
- ✅ **Fathom automation running** - Daily at 3 AM, 682 participants tracked
- ✅ **Phase 4B-1 complete** - 364 participants enriched via fuzzy matching (Oct 19)
- ✅ **Phase 4B-2 COMPLETE** - 459 participants validated via collaborative review (Oct 23)

**Recent Completions:**

*Oct 24, 2025:*
- ✅ Phase 4B-2 completion documentation and PR prep
- ✅ future_discipline/ component created with learnings from Phase 4B-2
- ✅ export_townhalls_to_landscape.py reinstated (Phase 5T ready)

*Oct 23, 2025:*
- ✅ Phase 4B-2 COMPLETE (Batch 11 final) - 459 participants validated
- ✅ All 11 batches completed, 650+ participants processed total
- ✅ Discipline learnings documented (Reflections_on_discipline.md, drone architecture)

*Oct 22, 2025:*
- ✅ Phase 4B-2 Rounds 9-13 complete (5 rounds, ~250 people processed)
- ✅ Town Hall agenda integration system (PR #18)
- ✅ ERA Africa field implementation (PR #18)
- ✅ Auto-add/auto-correct system for merge targets
- ✅ Branch protection enforcement (local + remote, PR #19)

*Oct 20, 2025:*
- ✅ Participant deduplication system (PR #17)
- Batch processing to identify and merge duplicate participants
- 71 duplicates found and merged in Fathom database

*Oct 19, 2025:*
- ✅ Phase 4B-1: Automated Fuzzy Matching
  - 364 participants enriched
  - 188 AI-misspelled names corrected
  - 351 members identified, 64 donors

*Oct 18, 2025:*
- ✅ Configuration Centralization (See CONFIGURATION_CENTRALIZATION_PLAN.md)
  - Migration to `/Users/admin/ERA_Admin/`
  - Centralized config in `era_config.py`
  - Bug fix: run_all.sh Step 3 exit issue
  - Automation schedule changed to 3 AM

**Available Next Steps:**
- 🎯 Phase 5T: Town Hall Visualization - Export meeting chain to landscape (READY NOW)
- 🎯 Phase 4C: Process new participants (223 unprocessed from continued Fathom automation)
- 🎯 Multi-System Integration - Long-term strategic plan (see ERA_ECOSYSTEM_PLAN.md)

#### Data Inventory

**Airtable (Manual Tracking):**
- Location: `airtable/people_export.csv`
- Records: 630 people (+59 from Phase 4B-2 reconciliation)
- TH Attendance: 17 meetings, 324 attendance records
- Fields: Name, email, member status, donor flag, phone, etc.
- Last Export: Run `python airtable/export_people.py` for fresh data
- Recent Growth: +10% from Fathom participant reconciliation (Oct 23)

**Fathom Inventory DB (Automated AI):**
- Location: `/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db`
- Participants: 682 total (continues to grow with new meetings)
  - 459 validated (67%) - enriched with Airtable data
  - 223 new/unprocessed - from continued Fathom automation post-Phase 4B-2
- Enrichment Status:
  - Phase 4B-1: 364 enriched (Oct 19)
  - Phase 4B-2: 459 enriched (Oct 23, 11 batches) - COMPLETE
- Automation: Daily at 3 AM via launchd ✅ Working

**ERA Landscape (Visualization):**
- Location: Google Sheet ID: 1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY
- Content: 350+ nodes (organizations, people, projects)
- Live Site: https://jonschull.github.io/ERA_Admin/ERA_Landscape/
- Technology: Static HTML/JS, OAuth editing enabled

**Validation & Enrichment Data:**
- Original Report: `/Users/admin/FathomInventory/analysis/townhall_validation_report.md`
  - 61.5% average match rate baseline
- Phase 4B-2 Complete: 459 participants validated (100% of Oct 23 scope)
  - 11 batches completed (650+ total participants processed)
  - 59 new people added to Airtable
  - Production-ready collaborative workflow established
- Discipline Learnings: `future_discipline/`
  - Analysis of AI discipline challenges
  - Proposed drone architecture for future work

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

*Phase 4B-2: Collaborative Review* ✅ COMPLETE (Oct 23)
- 11 batches completed - 459 participants validated (100% of scope)
- 59 new people added to Airtable (+10% growth)
- 650+ total participants processed across all batches
- Workflow: Human-AI collaboration with Gmail research
- Discipline learnings documented in future_discipline/

**Current Phase:**

*Phase 5T: Town Hall Visualization* 🎯 READY (3-4 hours)
- Goal: Export TH meetings as connected chain in landscape
- Readiness: Phase 4B-2 COMPLETE, script reinstated, ready to execute
- Script: `integration_scripts/export_townhalls_to_landscape.py`
- Actions:
  1. Query enriched participants from Fathom DB
  2. Format as project nodes (meetings) + person nodes + edges
  3. Export to Google Sheet via Sheets API
  4. Landscape auto-updates
- Result: Interactive meeting chain with 300+ connections
- Prerequisites: ✅ Phase 4B-2 complete, ✅ Script ready, ✅ 459 validated participants

*Phase 4C: Process New Participants* (Future)
- Goal: Process 223 new participants from continued Fathom automation
- Note: Database continues to grow with new meetings
- Can use established Phase 4B-2 workflow

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
│   ├── people_export.csv           (630 people, +59 from Phase 4B-2)
│   ├── people_for_matching.csv     (cleaned for fuzzy matching)
│   └── cross_correlation_report.txt (validation analysis)
│
├── FathomInventory/
│   ├── fathom_emails.db             (682 participants - 459 validated)
│   ├── run_all.sh                   (daily automation at 3 AM)
│   └── analysis/
│       ├── analyze_new_era_calls.py        (daily ERA meeting analysis)
│       ├── validate_townhall_attendance.py (Airtable comparison)
│       └── townhall_validation_report.md   (baseline: 61.5% match rate)
│
├── integration_scripts/         ← Phase 4-5
│   ├── phase4b1_enrich_from_airtable.py  (Phase 4B-1 ✅ Complete)
│   ├── export_townhalls_to_landscape.py  (Phase 5T - READY)
│   └── PAST_LEARNINGS.md                 (300+ patterns from Phase 4B-2)
│
└── future_discipline/          ← Experimental learnings
    ├── README.md                         (Overview & guidance)
    ├── Reflections_on_discipline.md      (AI discipline failures)
    └── disciplined_investigation_architecture.md (Drone proposal)
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

**Immediate (Ready Now):**
*Phase 5T: Town Hall Visualization*
1. 🎯 Execute export_townhalls_to_landscape.py
2. 🎯 Export 17 TH meetings as project nodes
3. 🎯 Connect 459 validated participants to meetings
4. 🎯 Verify visualization in landscape

**Future Work:**
*Phase 4C: Process New Participants*
- Process 223 new participants from continued automation
- Use established Phase 4B-2 workflow

*Phase 6: Automation & Integration*
- Daily sync of new enrichments
- Multi-system integration (see ERA_ECOSYSTEM_PLAN.md)

#### Success Metrics

**Phase 4B-2 Completion:**
- [✓] Production workflow established (11 batches tested)
- [✓] 459 participants validated (100% of Oct 23 scope)
- [✓] 630 people in Airtable (+10% growth)
- [✓] Discipline learnings documented
- [✓] COMPLETE - Oct 23, 2025

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
- What's the current phase? **Phase 5T (Town Hall Viz) - READY**
- What's working? **All base systems + Phase 4B-2 complete**
- What's in progress? **PR prep for Phase 4B-2 completion docs**
- When was last successful run? **Check Fathom cron.log for 3 AM runs**
- Any blockers? **No - Phase 5T ready to execute**
- For discipline learnings? **See `future_discipline/README.md`**

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
- Historical Phase 4B-2 workflow → integration_scripts/archive/superseded_docs/AI_WORKFLOW_GUIDE.md
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

**Phase 4B-2: Collaborative Review** (✅ COMPLETE - Oct 23, 2025)
- Historical workflow: integration_scripts/archive/superseded_docs/AI_WORKFLOW_GUIDE.md
- 11 batches completed, 459 participants validated
- Discipline learnings: future_discipline/ component

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
- integration_scripts/archive/superseded_docs/ - Historical Phase 4B-2 workflows (archived)
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

**Enforcement: Branch Protection (Two Layers)**

Documentation alone is insufficient. Enforce PR protocol at both local and remote:

*Layer 1: Local Pre-Commit Hook (blocks commits before they happen)*

After cloning, install the pre-commit hook:
```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
branch=$(git symbolic-ref HEAD 2>/dev/null | sed 's!refs/heads/!!')
if [ "$branch" = "main" ]; then
    cat << 'MSG'
❌ ERROR: Direct commits to 'main' branch are not allowed

✅ Proper workflow:
   1. Create feature branch: git checkout -b feature/description
   2. Make commits on that branch
   3. Create PR: gh pr create
   4. After merge: git checkout main && git pull

See WORKING_PRINCIPLES.md Section 4 (Git & PR Practices)
MSG
    exit 1
fi
EOF
chmod +x .git/hooks/pre-commit
```

*Layer 2: GitHub Branch Protection (blocks pushes)*

Setup (one-time):
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

*Result:* Direct commits to main blocked locally; pushes blocked remotely.

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
gh pr create --fill  # Use --fill, not --body with long text
gh pr merge --squash --delete-branch
```

**⚠️ WARNING: Avoid `gh pr create` hangs**

Using `--body` with long multi-line text can cause `gh pr create` to hang indefinitely:

```bash
# ❌ DON'T DO THIS (causes hangs):
gh pr create --title "..." --body "Very long text
with multiple lines
and lots of content..."

# ✅ DO THIS INSTEAD:
git push origin branch-name
gh pr create --fill  # Uses commit message, edit in browser if needed
```

**Why it hangs:** Long command-line arguments can cause the GitHub CLI to freeze, especially with complex formatting or special characters. Use `--fill` to populate from commits, then edit the PR description in the GitHub web UI if you need more detail.

**For major overhauls only:**
```bash
python3 docs/archive_and_replace.py  # Creates backup, replaces all
```

#### Documentation PR Review Guide

**Beyond mechanical checks, verify:**

**1. Veridicality - Content matches reality:**
- Obsolete instructions removed or marked historical
- File references point to actual locations (especially archive/)
- "Current work" reflects actual current work
- Completed phases not described as ongoing
- Instructions match current system state
- Dates are current

**2. Validation - Generated docs are correct:**
- Read key generated files (README.md, component READMEs)
- Confirm wireframe edits propagated correctly
- Check no deletions of important content (`git diff --stat`)
- Verify key sections updated (Quick Start, Recent Completions, metrics)
- Test navigation integrity (`python3 docs/test_navigation.py`)

**3. Consistency - Updates are thorough:**
- All instances updated (not just some)
- Cross-references updated
- Metrics match database/system reality
- Archive references correct
- New components properly integrated

**Common mistakes to catch:**
- ❌ Updated numbers but left obsolete workflow instructions
- ❌ Moved files but didn't update references to them
- ❌ Marked phase complete but left "how to resume" instructions
- ❌ Added new component but didn't list in root README
- ❌ Regenerated but didn't verify output correctness

**Example checks:**
```bash
# Check for old status markers
grep -r "87%" README.md CONTEXT_RECOVERY.md

# Verify file moves reflected in docs
grep "generate_phase4b2_table.py" integration_scripts/README.md
# Should show: archive/experimental/generate_phase4b2_table.py

# Check generated docs are recent
stat -f %Sm README.md docs/NAVIGATION_WIREFRAME.md
# README.md should be >= wireframe timestamp

# Verify key content propagated
grep "Phase 5T.*Ready" README.md
grep "459.*validated" CONTEXT_RECOVERY.md
```

**Validation discipline:** Don't just trust the script worked. Read the output.

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
- ✅ **682 participants** tracked (459 validated/67%, 223 new/unprocessed)
- ✅ **3,229+ emails** processed with full metadata extraction
- ✅ **Dates normalized** to ISO format (YYYY-MM-DD) at all entry points
- ✅ **Automation active** - Daily runs at 3:00 AM via macOS launchd
- ✅ **Enhanced failure detection** - Catches authentication failures immediately
- ✅ **Phase 4B-2 COMPLETE** - 459 participants validated (Oct 23, 2025)

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

#### Current System State (Oct 24, 2025)

**What's Working:**
- ✅ **682 participants** tracked in SQLite database (459 validated/67% from Phase 4B-2)
- ✅ **3,240+ emails** processed with full metadata
- ✅ **Database mode** active (TSV migration complete)
- ✅ **Enhanced failure detection** - catches auth failures immediately
- ✅ **Daily automation** at 3:00 AM via macOS launchd
- ✅ **Automated backups** - Local (daily 3 AM) + Google Drive (daily 4 AM)
- ✅ **Backup verification** - Daily report queries Drive API to confirm uploads
- ✅ **Fresh authentication** - cookies refreshed regularly
- ✅ **Phase 4B-2 COMPLETE** - 459 participants validated (Oct 23, 2025)

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

## FILE: fathom/README.md

**Path:** `fathom/README.md`

# Fathom Component

**Purpose:** Download and aggregate Fathom meeting transcripts from the Fathom API

## Overview

This component provides tools to:
1. Download transcripts from Fathom API for ERA Town Hall meetings
2. Collect manually downloaded transcripts when API unavailable
3. Aggregate all transcripts with existing meeting data (agendas, summaries)
4. Generate comprehensive chronological markdown archive

## Data Sources

For each ERA Town Hall meeting, we combine:
- **Meeting metadata** from `FathomInventory/fathom_emails.db` (calls table)
- **Town Hall agendas** from Google Docs (town_hall_agendas table)
- **Fathom AI summaries** from email processing (emails.body_md)
- **Full transcripts** from Fathom API (downloaded by this component)

## Files

**Scripts:**
- `download_transcripts.py` - Main script to download and aggregate transcripts via API
- `interleave_transcripts.py` - Script to interleave manually-collected transcripts into complete file

**Data:**
- `progress.json` - Resumability state (auto-generated)
- `failures.log` - Detailed failure tracking for API failures

**Output:**
- `output/era_townhalls_complete.md` - Final aggregated output (183K+ lines, 65 meetings)
- `output/era_townhalls_complete.md.backup` - Backup before manual transcript interleaving

## Usage

### Initial Setup
```bash
# API key is hardcoded from existing test_api2.py
# No additional configuration needed
```

### Download Transcripts
```bash
# Test mode - first 3 meetings only
python download_transcripts.py --test

# Full run - all 66 ERA Town Hall meetings
python download_transcripts.py --all

# Resume from interruption
python download_transcripts.py --resume
```

### Features

**Conservative Rate Limiting:**
- Sequential processing (one at a time)
- Waits for each API response confirmation before next request
- 3-second delay between successful requests
- Exponential backoff on errors (3s → 6s → 12s → 24s)

**Failure Handling:**
- Records all failures with reasons in `failures.log`
- Continues processing remaining meetings
- Supports resumability via `progress.json`
- Detailed error reporting for manual mop-up

**Output Format:**
- Chronological markdown compilation
- Meeting headers with metadata
- Agendas (when available)
- AI summaries (when available)
- Full transcripts with speaker attribution and timestamps

## Rate Limiting Strategy

To avoid overwhelming Fathom API:
1. **Sequential only** - No parallel requests
2. **Confirmation before proceed** - Verify response success
3. **Polite delays** - 3s minimum between requests
4. **Backoff on errors** - Exponential delay if issues occur
5. **Abort on repeated failures** - Stop after 5 consecutive errors

### 4. Specialized Topics

#### Complete Workflow

**Phase 1: Automated API Download**
```bash
# Test on first 3 meetings
python download_transcripts.py --test

# Full run on all meetings
python download_transcripts.py --all
```

**What happens:**
- Queries Fathom API using date-range search (not pagination)
- Retrieves meetings from 2023-04-26 to 2025-10-01
- Includes: meeting metadata, agendas, AI summaries, transcripts
- Strips base64-encoded images from agendas
- Saves progress after each meeting (resumable)
- Creates `output/era_townhalls_complete.md`

**Phase 2: Manual Collection for API Gaps**

Some meetings aren't accessible via API but are available on Fathom website:

```bash
# Manually visit each failed meeting URL
# Click download/copy transcript
# Aggregate into output/Missing 7.md
```

**Phase 3: Interleave Manual Transcripts**
```bash
python interleave_transcripts.py
```

**What happens:**
- Creates backup: `era_townhalls_complete.md.backup`
- Parses manually-collected transcripts from `Missing 7.md`
- Finds corresponding "Transcript not available" sections in complete file
- Replaces with actual transcript content
- Deletes `Missing 7.md` (now integrated)

**Final Result:**
- 65 ERA Town Hall meetings (2023-2025)
- 100% transcript coverage
- 183,568 lines of aggregated content
- Chronologically organized
- Searchable, shareable single file

#### API Strategy: Date-Range Queries

**Why not pagination?**
- Fathom API pagination has ~2 year historical limit
- Older meetings (2023-2024) not accessible via cursor-based pagination

**Date-range solution:**
- Query API with `created_after` and `created_before` parameters
- Each meeting's date used to query ±1 day window
- Finds meetings regardless of age
- Much more efficient than paginating through thousands of meetings

**Implementation:**
```python
params = {
    'created_after': '2023-04-25T00:00:00Z',
    'created_before': '2023-04-27T23:59:59Z',
    'limit': 100,
    'include_transcript': 'true'
}
```

#### Image Stripping

Town Hall agendas from Google Docs contain base64-encoded images that bloat the output.

**Removal patterns:**
```python
# Markdown image references: [image1]: <data:image/...>
text = re.sub(r'\[image\d+\]:\s*<data:image/[^>]+>', '', text)

# Inline images: ![alt](data:image/...)
text = re.sub(r'!\[([^\]]*)\]\(data:image/[^)]+\)', '', text)

# Image references: ![][imageN]
text = re.sub(r'!\[\]\[image\d+\]', '', text)
```

**Result:** Clean, readable agendas without binary bloat

#### Resumability

**progress.json tracks:**
```json
{
  "completed": ["19714472", "20977039", ...],
  "failed": {
    "426784451": {
      "reason": "No transcript available",
      "timestamp": "2025-10-24T21:50:26",
      "details": "API returned no transcript data"
    }
  },
  "last_processed_date": "2025-10-01"
}
```

**On resume:**
- Skips completed meetings
- Appends to existing output file
- Retries failed meetings
- Handles Ctrl+C gracefully

#### Database Integration

**Source:** `/FathomInventory/fathom_emails.db`

**Query joins three tables:**
```sql
SELECT 
  c.hyperlink, c.title, c.date, c.duration,
  t.agenda_text,  -- from town_hall_agendas
  e.body_md       -- from emails (Fathom summaries)
FROM calls c
LEFT JOIN town_hall_agendas t ON DATE(c.date) = DATE(t.meeting_date)
LEFT JOIN emails e ON DATE(c.date) = DATE(e.meeting_date)
WHERE c.title LIKE '%ERA Town Hall%'
ORDER BY c.date
```

**Database maintenance:**
- Remove mislabeled meetings: `DELETE FROM calls WHERE hyperlink = '...'`
- Check count: `SELECT COUNT(*) FROM calls WHERE title LIKE '%ERA Town Hall%'`

## Back to: [/README.md](../README.md)

---

## FILE: integration_scripts/README.md

**Path:** `integration_scripts/README.md`

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
1. Read [README.md](#file-readmemd) - System overview
2. Check Phase 5T section below - Town Hall visualization ready
3. Script: export_townhalls_to_landscape.py
4. Prerequisites: ✅ Phase 4B-2 complete, ✅ 459 validated participants

**Future Work (Phase 4C):**
1. Process 223 new participants (from continued Fathom automation)
2. Can adapt Phase 4B-2 workflow (see archive/superseded_docs/)
3. Use PAST_LEARNINGS.md (300+ patterns) for efficiency

**What you might need:**
- **Parent system** → [/README.md](#file-readmemd) - Overall ERA Admin architecture
- **System-wide status** → [/CONTEXT_RECOVERY.md](#file-context_recoverymd) - Integration status
- **System principles** → [/WORKING_PRINCIPLES.md](#file-working_principlesmd) - Overall philosophy
- **Phase 4B-2 history** → archive/superseded_docs/ - Completed workflows (archived)
- **Discipline learnings** → [/future_discipline/](#file-future_disciplinereadmemd) - AI collaboration lessons
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

## FILE: integration_scripts/archive/superseded_docs/AI_WORKFLOW_GUIDE.md

**Path:** `integration_scripts/archive/superseded_docs/AI_WORKFLOW_GUIDE.md`

**Status:** ⚠️ HISTORICAL DOCUMENT - Phase 4B-2 completed Oct 23, 2025

This document is preserved for reference but describes a completed workflow. For current work, see Phase 5T documentation or future_discipline/ for lessons learned.

---

### 1. Overview

**Purpose:** Historical guide for Phase 4B-2 collaborative review workflow (COMPLETED Oct 23, 2025)  
**Audience:** Reference for future similar workflows  
**Note:** This workflow is complete. See /future_discipline/ for lessons learned.

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

**You are at:** Historical AI workflow guide (Phase 4B-2 - COMPLETED)

**Use this when:**
- Understanding how Phase 4B-2 worked (historical reference)
- Designing similar collaborative workflows
- Learning from completed human-AI collaboration
- Reference for future Phase 4C work

**What you might need:**
- **Parent component** → [README.md](#file-integration_scriptsreadmemd) - integration_scripts overview
- **Phase progress** → archive/superseded_docs/PHASE4B2_PROGRESS_REPORT.md - 11-batch analysis (archived)
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
# Historical scripts (now in archive/experimental/)
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

*What to do (historical):*
1. Update progress report with round results
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
- Document in progress report
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

**Files (all now in archive/):**
- `experimental/generate_batch_data.py` - Select next 25 people (archived)
- `experimental/generate_phase4b2_table.py` - HTML review interface (archived)
- `experimental/parse_phase4b2_csv.py` - Parse decisions (archived)
- Past batch execution scripts (archived)
- **PAST_LEARNINGS.md** - 300+ patterns (ACTIVE - used for future work)
- `superseded_docs/PHASE4B2_PROGRESS_REPORT.md` - 11-batch analysis (archived)

**Key Insight:** This workflow represents significant learning from 11 batches (650+ participants). The patterns discovered (phone numbers, devices, organizations) are now codified in PAST_LEARNINGS.md. See /future_discipline/ for architectural proposals.

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

---

## FILE: future_discipline/README.md

**Path:** `future_discipline/README.md`

### 1. Overview

**Purpose:** Experimental investigations into AI discipline and architectural solutions

This component documents lessons learned from Phase 4B-2 participant reconciliation (650+ participants, 11 batches) and proposes architectural approaches to address systematic AI discipline challenges.

**Status:** 🔬 Experimental / Future Investigation

**What this contains:**
- Analysis of AI discipline failures during Phase 4B-2
- Patterns of failure (premature stopping, incomplete checking, memory loss)
- Proposed "drone architecture" solution (mechanical tasks → scripts, judgment → AI)
- Comparison with mcp-agent framework approach
- Not active development - lessons learned and proposals for future consideration

**Context:** During Phase 4B-2 completion (Oct 2025), we encountered systematic issues with AI assistants failing to maintain discipline on repetitive investigative tasks. These documents analyze why this happens and propose solutions.

### 2. Orientation - Where to Find What

**You are at:** Future discipline experiments directory

**Use this when:**
- Designing AI-human collaboration workflows
- Investigating AI reliability challenges
- Understanding Phase 4B-2 lessons learned
- Considering architectural solutions for AI discipline

**What you might need:**
- **Parent** → [/README.md](../README.md) - System overview
- **Related work** → [integration_scripts/](../integration_scripts/) - Phase 4B-2 implementation
- **Context** → integration_scripts/PAST_LEARNINGS.md - 300+ resolved patterns from Phase 4B-2
- **Principles** → [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) - System-wide philosophy

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

**Discipline-specific insights:**

**1. Scripts Are More Disciplined Than AI**
- Scripts execute mechanically (always check all 6 tools)
- AI gets lazy, forgets steps, takes shortcuts
- Use scripts for discipline, AI for judgment

**2. Context Resets Are The Problem**
- "Indy" asked about 5+ times despite resolution in past batches
- AI memory doesn't persist across sessions
- Solution: Scripts that check past decisions (persistence via files, not memory)

**3. Forcing Functions Must Be Architectural**
- Documentation ("please check X") doesn't work
- Code that can be bypassed (new scripts) doesn't work
- Architectural enforcement (workflow won't run without check) works

**4. Decompose Tasks By Cognitive Requirements**
- Mechanical tasks → scripts (grep, fuzzy match, database queries)
- Judgment tasks → AI (pattern recognition, inference)
- Don't ask philosophers to do accounting

### 4. Specialized Topics

#### Reflections on Discipline

**File:** [Reflections_on_discipline.md](Reflections_on_discipline.md) (24KB)

**Summary:**
- Detailed analysis of discipline failures during Phase 4B-2
- The "checking vs actually checking" problem
- Why AI claims to have done work without executing it
- The quality threshold problem (stopping too early)
- Memory resets across sessions ("Indy" asked 5 times)
- Forcing functions that can be bypassed
- Comparison with human behavior patterns

**Key sections:**
- The Checking Problem (claims vs reality)
- The Quality Threshold Problem (good enough vs actually enough)
- The Memory Problem (context resets)
- The Bypass Problem (new scripts that skip safeguards)
- Meta-analysis: Why this is hard to fix

**Epilogue:** Discussion of mcp-agent framework as potential solution

#### Drone Architecture Proposal

**File:** [disciplined_investigation_architecture.md](disciplined_investigation_architecture.md) (17KB)

**Summary:**
Proposes decomposing Phase 4B-2 investigation workflow into:
- **Tier 1: Drones** (bash/Python scripts) - Execute all 6 tools mechanically
- **Tier 2: Rules** (deterministic logic) - Apply automatic decisions (>95% fuzzy match → merge)
- **Tier 3: Orchestrator** (no AI) - Run drones for all names, batch AI questions
- **Tier 4: Claude** (high-cognition AI) - ONLY for 30% needing human judgment

**Key insight:** 70% of cases can be auto-resolved without AI. Use scripts for discipline, AI for intelligence.

**Example drone script:**
```bash
#!/bin/bash
# Always checks all 6 tools, never forgets, never gets lazy
investigate_name.sh "$NAME"
# Returns structured JSON with all results
```

**Benefits:**
- Scripts persist across sessions (solve "Indy asked 5 times" problem)
- Scripts are disciplined (always check all 6 tools)
- Cheaper (70% resolved without LLM API calls)
- Faster (parallel script execution)
- Evidence-based (results in files, falsifiable)

**Comparison with mcp-agent:**
- mcp-agent: Orchestrator LLM + worker agents + evaluator LLM
- Drones: No AI orchestration, scripts + rules + AI only for judgment
- Trade-off: Flexibility vs determinism

#### Relationship to Phase 4B-2

**Phase 4B-2 Context:**
- 650+ participants reconciled across 11 batches
- 6-tool investigation workflow (PAST_LEARNINGS, CSVs, fuzzy match, Fathom, Town Hall agendas, Gmail)
- Systematic discipline problems identified:
  - Claiming to check without executing
  - Stopping after 3-4 tools instead of all 6
  - Asking about "Indy" 5+ times despite past resolution
  - Creating bypass scripts that skip forcing functions

**What worked:**
- Forcing functions in canonical pipeline
- Human-AI collaboration (HTML review → CSV feedback)
- PAST_LEARNINGS.md accumulation (300+ patterns)
- Progress tracking (show which tools used)

**What didn't work:**
- Relying on AI memory across sessions
- Documentation saying "please check X"
- Assuming AI will be disciplined

**Result:** 100% completion (459/459 validated), but at high human oversight cost

#### Current Status

**Phase:** Experimental / Future Investigation

**Not Implemented:**
- Drone architecture is a proposal, not implementation
- Would require significant refactoring of Phase 4B-2 workflow
- Would need testing to validate 70% auto-resolution claim

**Possible Future Work:**
1. Implement drone scripts for Phase 4B-2 tools
2. Test auto-resolution rate on historical data
3. Compare cost/time vs current workflow
4. Consider mcp-agent framework integration
5. Generalize to other AI-human workflows

**Questions to Answer:**
- Does 70% auto-resolution claim hold in practice?
- Is the architectural overhead worth the discipline gains?
- Can mcp-agent provide similar benefits with more flexibility?
- What tasks actually require high-cognition AI vs deterministic rules?

#### Related Documentation

**Phase 4B-2 Implementation:**
- integration_scripts/PAST_LEARNINGS.md - Patterns learned during reconciliation
- integration_scripts/generate_batch_CANONICAL.py - Forcing functions implementation

**System Principles:**
- /WORKING_PRINCIPLES.md - Human-AI collaboration philosophy
- /AI_HANDOFF_GUIDE.md - AI assistant conventions

**Historical Context:**
- Phase 4B-2 completed October 23, 2025
- These reflections written same day, while discipline problems fresh
- Intended as lessons for future AI-human workflows

---

**Back to:** [/README.md](../README.md)

---

## FILE: ERA_Landscape/README.md

**Path:** `ERA_Landscape/README.md`

# ERA Landscape - Static Viewer

**Live Demo**: https://jonschull.github.io/ERA_Admin/ERA_Landscape/

**Historical repo (archived)**: https://github.com/jonschull/ERA_Landscape_Static

Interactive graph visualization for the climate/restoration landscape. Pure HTML/JavaScript, no server required.

---

## What Is This?

A **standalone HTML file** (20KB) that:
- Auto-loads fresh data from Google Sheets on page load
- Shows 350+ organizations and their relationships
- Allows editing (with Google sign-in)
- Requires NO server, NO Python, NO backend
- NO embedded data - always shows latest from Sheet

**Just open via HTTP server or GitHub Pages.**

---

## Quick Start

### View Locally (with Google Sheets API)

**Important:** Google Sheets API requires HTTP/HTTPS protocol. Use a local server:

```bash
# Clone the repo
git clone https://github.com/jonschull/ERA_Admin.git
cd ERA_Admin/ERA_Landscape

# Start local server
python3 -m http.server 8000

# Open in browser
open http://localhost:8000
```

**Note:** Opening `index.html` directly (file:// protocol) won't work - Google Sheets API requires HTTP/HTTPS. Use HTTP server locally or GitHub Pages for deployment.

### Deploy to GitHub Pages

Already configured! Merge PRs to main and GitHub Pages auto-deploys.

**URL**: https://jonschull.github.io/ERA_Admin/ERA_Landscape/

**Important**: Use branch-based workflow (see DEVELOPMENT.md)

---

## How It Works

### Data Flow
1. **Page loads** → Empty graph initialized
2. **Google Sheets API initializes** → API key authentication
3. **Data auto-loads** → Fetches nodes & edges from [ERA Climate Week Data](https://docs.google.com/spreadsheets/d/1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY/edit)
4. **Graph renders** → Shows ~350+ nodes with relationships
5. **Loading screen hides** → Interactive graph ready

**Zero embedded data** → Always shows fresh data from Sheet

### Authentication
- **Viewing**: No sign-in required (public read via API key)
- **Editing**: Click "Sign In" button, authenticate via Google OAuth
- **Saving**: Changes written directly back to Google Sheet

### Architecture
```
Browser loads index.html
  ↓
Calls Google Sheets API (API key)
  ↓
Fetches nodes & edges data
  ↓
Renders interactive graph (vis-network.js)
  ↓
User clicks "Sign In" (optional)
  ↓
OAuth popup → authenticated
  ↓
User can save edits back to Sheet
```

**No server. No backend. Pure client-side.**

---

## Documentation

**For Users:**
- [README.md](README.md) - This file (quick start, deployment)
- [KNOWN_ISSUES.md](KNOWN_ISSUES.md) - Current bugs and workarounds

**For Developers:**
- [NETWORK_ARCHITECTURE.md](NETWORK_ARCHITECTURE.md) - **Technical deep-dive:** Town Hall treatment, physics engine, node sizing, slider controls
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development workflow and testing
- [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md) - Context for AI assistants

## Files

```
ERA_Landscape_Static/
├── index.html                   # Main HTML file (UI, modals, event handlers)
├── graph.js                     # vis.js initialization and options
├── README.md                    # This file (quick start)
├── NETWORK_ARCHITECTURE.md      # Technical documentation (NEW!)
├── DEVELOPMENT.md               # Development workflow
├── KNOWN_ISSUES.md              # Bug tracking
└── tests/                       # Test scripts
    ├── test_load.py             # Basic load test
    ├── test_visual_nodesize.py  # Screenshot validation
    └── test_visual_centralgravity.py  # Screenshot validation
```

---

## Configuration

Google API credentials are embedded in `index.html`:

```javascript
const SHEET_ID = '1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY';
const API_KEY = 'AIzaSyBp23GwrTURmM3Z1ERZocotnu3Tn96TmUo';
const CLIENT_ID = '57881875374-flipnf45tc25cq7emcr9qhvq7unk16n5.apps.googleusercontent.com';
```

**Google Sheet Configuration:**
- **Sheet URL**: https://docs.google.com/spreadsheets/d/1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY/edit
- **Sheet Owner**: jschull@gmail.com
- **Access Policy**: Write access granted to trusted users only
- **Note**: Sheet URL not shared with end users (not ready for public editing)

**OAuth Configuration:**
- **OAuth App Name**: ERA Graph Browser Client
- **Google Cloud Account**: fathomizer@ecorestorationalliance.com
- **Console**: https://console.cloud.google.com/apis/credentials?project=57881875374
- **Status**: ✅ In production (anyone with Google account can sign in)

**To use your own Sheet:**
1. Copy the Google Sheet
2. Get API Key & OAuth Client ID from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
3. Update credentials in `index.html`
4. Make sure Sheet is publicly readable

---

## Development

### Edit the HTML/JavaScript

```bash
# Create feature branch
git checkout -b feat/feature-name

# Edit files
code index.html
code graph.js

# Test locally (MUST use HTTP server)
python3 -m http.server 8000
open http://localhost:8000

# Commit changes
git add .
git commit -m "feat: Update feature"
git push origin feat/feature-name

# Create PR on GitHub, then merge to main
```

**No build step. No compilation. Just edit and test.**

### Run Tests

```bash
# Install Playwright
pip install playwright
playwright install

# Run test
cd tests
python test_load.py
```

---

## Deployment

### GitHub Pages (Automatic)

Already configured! Every push to `main` auto-deploys in ~1-2 minutes.

**To update the live site:**
```bash
# 1. Create feature branch
git checkout -b feat/my-change

# 2. Make your changes
code index.html

# 3. Test locally (REQUIRED - needs HTTP server)
python3 -m http.server 8000
open http://localhost:8000

# 4. Commit and push branch
git add .
git commit -m "feat: Description of changes"
git push origin feat/my-change

# 5. Create PR and merge to main
# (via GitHub UI or gh pr create)

# 6. Wait for deployment (~1-2 minutes)
gh api repos/jonschull/ERA_Landscape_Static/pages/builds/latest | jq -r '.status'

# 7. Verify live site
open https://jonschull.github.io/ERA_Admin/ERA_Landscape/
```

**Settings → Pages:**
- Source: Deploy from branch
- Branch: `main`
- Folder: `/` (root)
- URL: https://jonschull.github.io/ERA_Landscape_Static/

**Build typically completes in:**
- First deploy: ~1-2 minutes
- Subsequent updates: ~30-60 seconds

### Other Hosting

Works on any static host:
- Netlify
- Vercel
- Amazon S3
- Your own web server
- Email attachment (yes, really!)
- Dropbox public link

**Just serve `index.html`.**

---

## Features

### Current
- ✅ Auto-loads fresh data from Google Sheets on page init
- ✅ Auto-fit graph after data loads
- ✅ Interactive graph (drag, zoom, pan)
- ✅ **Town Hall Integration** (65 events in fixed peripheral ring)
  - Grey edges with distance-based fading
  - See [NETWORK_ARCHITECTURE.md](NETWORK_ARCHITECTURE.md) for details
- ✅ **Network Settings Modal** (🌐 button)
  - Node Scaling (constant ↔ logarithmic)
  - Node Size (0.2-3.0x multiplier)
  - Edge Fading & Thickness
- ✅ **Physics Settings Modal** (⚙️ button)
  - Central Gravity, Node Spacing, Edge Springs
  - Real-time layout adjustment
  - ⚠️ Central Gravity has inverted behavior (see KNOWN_ISSUES.md)
- ✅ Node scaling by connection count with visual tests
- ✅ Quick Editor (add/remove connections)
  - Enter key triggers Add/Update
  - Yellow border highlights matching nodes
- ✅ Search filtering
- ✅ Hide/show nodes
- ✅ Save changes to Google Sheets (with sign-in)
- ✅ Re-Load button (re-fetch from Sheets with guardrail)
- ✅ Color-coded by type (person=blue, org=teal, project=purple, event=grey)
- ✅ Type parsed from ID prefix (person::, org::, project::, event::)
- ✅ Hover tooltips on all buttons

### Planned
- [ ] Curation modal for organizations
- [ ] Batch operations
- [ ] Export to PNG/CSV
- [ ] Undo/redo

---

## Related Project

This project was extracted from [ERA_ClimateWeek](https://github.com/jonschull/ERA_ClimateWeek) and is now part of the ERA_Admin monorepo as a self-contained component.

**When to use each:**

**ERA_ClimateWeek** (Python):
- Data processing & transformation
- Importing from CSV
- Batch operations
- Development & testing

**ERA_Landscape_Static** (this project):
- Production viewer
- Public deployment
- No server needed
- Simple editing

---

## Browser Compatibility

Tested on:
- ✅ Chrome 118+
- ✅ Firefox 119+
- ✅ Safari 17+
- ✅ Edge 118+

Requires modern browser with ES6 support.

---

## License

MIT License - See parent project for details.

---

## Contact

**Repository**: https://github.com/jonschull/ERA_Admin (ERA_Landscape/ component)  
**Historical repo**: https://github.com/jonschull/ERA_Landscape_Static (archived)  
**Main Project**: https://github.com/jonschull/ERA_ClimateWeek  
**Developer**: Jon Schull


---

## FILE: ERA_Landscape/NETWORK_ARCHITECTURE.md

**Path:** `ERA_Landscape/NETWORK_ARCHITECTURE.md`

# Network Visualization Architecture

**Purpose:** Technical documentation of ERA Landscape's network graph implementation  
**Audience:** Developers and AI assistants working on the visualization layer

## Table of Contents
1. [Overview](#overview)
2. [Town Hall Special Treatment](#town-hall-special-treatment)
3. [Node Sizing System](#node-sizing-system)
4. [Physics Engine](#physics-engine)
5. [User Controls](#user-controls)
6. [Testing](#testing)

---

## Overview

### Technology Stack
- **Library:** vis-network.js (v9.1.9)
- **Physics Solver:** barnesHut
- **Data Sources:** Google Sheets API
- **Node Types:** Person, Organization, Project, Event (Town Halls)

### Core Architecture
```
Google Sheets Data → JavaScript Processing → vis.js DataSets → Network Rendering
                                              ↓
                                     Physics Simulation
                                              ↓
                                     User Interactions
```

**Key Files:**
- `index.html` - Main UI, modals, and event handlers
- `graph.js` - vis.js initialization and options
- `tests/test_visual_*.py` - Screenshot-based visual validation tests

---

## Town Hall Special Treatment

### Why Special?
Town Hall events have **65 nodes** at the periphery that serve as temporal landmarks. They must remain **fixed in position** while other nodes (people, orgs, projects) are mobile.

### Implementation

**Location:** `index.html` lines 696-715

```javascript
// Position Town Hall events in a fixed circle at periphery
const townHalls = nodesPayload.filter(node => node.id.startsWith('event::Town Hall'));
if (townHalls.length > 0) {
  const thUpdates = townHalls.map((node, idx) => {
    // Arrange in a large circle (radius 1000px)
    const angle = (idx / townHalls.length) * 2 * Math.PI;
    const radius = 1000;
    const x = Math.cos(angle) * radius;
    const y = Math.sin(angle) * radius;
    
    return {
      ...node,
      x: x,
      y: y,
      fixed: { x: true, y: true },  // Fixed position
      physics: false  // Don't participate in physics simulation
    };
  });
  nodes.update(thUpdates);
}
```

**Key Properties:**
- `physics: false` - Town Halls don't move, don't exert forces
- `fixed: {x: true, y: true}` - Locked at specified coordinates
- `radius: 1000px` - Peripheral ring distance from center (0,0)
- Arranged in circular order by chronological index

**Implications:**
1. **Physics sliders** affect only mobile nodes (people/orgs/projects)
2. **Central Gravity** pulls mobile nodes toward center, not toward THs
3. **Spread measurements** should exclude Town Halls (see `tests/test_visual_centralgravity.py`)
4. **Edge adjustment** - TH→person edges fade by distance (see `adjustTHEdges()`)

---

## Node Sizing System

### How Node Sizes Work

vis.js uses a **two-stage sizing system**:

1. **Data Value** → Node's `value` property (JavaScript number)
2. **Visual Scaling** → `scaling.min` and `scaling.max` (pixel range)

**Formula:**
```
Visual Size (px) = scaling.min + (normalized_value × (scaling.max - scaling.min))
```

### Implementation

**Initial Load:** `index.html` lines 658-679
```javascript
const updates = nodesPayload.map(node => {
  const connections = connectionCount[node.id] || 1;
  const type = parseTypeFromId(node.id);
  
  let finalValue;
  if (type === 'event') {
    // Town Halls: capped scaling with nodeSize multiplier
    finalValue = Math.min(connections * 0.3, 10) * networkConfig.nodeSize;
  } else {
    // Other nodes: blend constant ↔ logarithmic based on scalingIntensity
    const constantScale = 10;
    const logScale = Math.log(connections + 1);
    const intensity = networkConfig.scalingIntensity;
    const blendedScale = constantScale + (logScale - constantScale) * intensity;
    finalValue = blendedScale * networkConfig.nodeSize;
  }
  
  return { ...node, value: finalValue };
});
```

**Dynamic Scaling:** `index.html` lines 1187-1202
```javascript
// Update vis.js scaling range based on nodeSize multiplier
if (window.network) {
  const baseMin = 12;
  const baseMax = 60;
  window.network.setOptions({
    nodes: {
      scaling: {
        min: baseMin * networkConfig.nodeSize,
        max: baseMax * networkConfig.nodeSize
      }
    }
  });
  window.network.redraw();
}
```

**Why This Matters:**
- Changing `value` alone doesn't resize nodes visually
- Must also update `scaling.min/max` and call `redraw()`
- This is why Node Size slider was initially broken (values changed but visuals didn't)

### Connection Weighting

**Town Hall edges:** Count as `0.1` instead of `1.0` to avoid inflating node sizes
```javascript
const weight = edge.isTownHallEdge ? 0.1 : 1;
connectionCount[edge.from] = (connectionCount[edge.from] || 0) + weight;
```

---

## Physics Engine

### Configuration

**Location:** `graph.js` lines 5-22

```javascript
physics: {
  barnesHut: {
    gravitationalConstant: -2000,    // Node-to-node repulsion
    centralGravity: 0.4,             // Pull toward center (0,0)
    springLength: 175,               // Natural edge length
    springConstant: 0.04,            // Spring tightness
    damping: 0.35,                   // Movement decay
    avoidOverlap: 0.2                // Overlap repulsion (use sparingly)
  },
  maxVelocity: 50,
  minVelocity: 2.5,
  solver: 'barnesHut',
  timestep: 0.35,
  adaptiveTimestep: true,
  stabilization: { enabled: true, iterations: 1000 }
}
```

### How It Works

**barnesHut Solver:**
- Simulates N-body gravitational forces efficiently (O(n log n))
- Nodes repel each other (`gravitationalConstant < 0`)
- Edges act as springs pulling nodes together
- Central gravity pulls toward origin (0,0)
- Damping causes motion to slow and settle

**Key Parameters:**

| Parameter | Effect | Default | Range |
|-----------|--------|---------|-------|
| `centralGravity` | Pull toward center | 0.4 | 0-1.0 |
| `springLength` | Natural edge length | 175px | 50-400 |
| `springConstant` | Spring tightness | 0.04 | 0.001-0.15 |
| `avoidOverlap` | Overlap repulsion | 0.2 | 0-1.0 |

**⚠️ Known Issue:** Central Gravity produces inverted behavior
- Expected: Higher → tighter clustering
- Actual: Higher → more spread
- Hypothesis: Fixed Town Hall ring interferes with barnesHut calculations
- See `tests/test_visual_centralgravity.py` for evidence

---

## User Controls

### Network Settings Modal (🌐)

**Purpose:** Visual appearance (node sizes, edge visibility)

| Slider | Range | Default | Effect |
|--------|-------|---------|--------|
| Node Scaling | 0-2.0 | 1.0 | Blend constant ↔ logarithmic sizing |
| Node Size | 0.2-3.0 | 1.0 | Overall size multiplier |
| Edge Fading | 0-2.0 | 1.0 | TH edge opacity adjustment |
| Edge Thickness | 0-3.0 | 1.0 | TH edge width adjustment |

**Node Scaling Details:**
- `0.0` = All nodes same size (constant = 10)
- `1.0` = Logarithmic scaling by connections (default)
- `2.0` = Super-logarithmic scaling (exaggerated differences)

**Formula:**
```javascript
const constantScale = 10;
const logScale = Math.log(connections + 1);
const blendedScale = constantScale + (logScale - constantScale) * scalingIntensity;
const finalValue = blendedScale * nodeSize;
```

### Physics Settings Modal (⚙️)

**Purpose:** Network layout and spacing

| Slider | Range | Default | Effect |
|--------|-------|---------|--------|
| Central Gravity | 0-1.0 | 0.4 | Pull toward center ⚠️ |
| Node Spacing | 50-400 | 175 | Natural edge length |
| Edge Springs | 0.001-0.15 | 0.04 | Spring tightness |
| Avoid Overlap | 0-1.0 | 0.2 | Overlap repulsion (causes jitter) |
| Edge Length Multiplier | 0-30 | 10 | Per-degree spacing boost |
| Edge Length Max | 100-500 | 300 | Maximum edge length |

**⚠️ Central Gravity:** Known to be broken - higher values spread nodes instead of tightening

**Design Choice:** Defaults are in the **middle** of ranges to provide "elbow room" for experimentation

### Persistence

**localStorage Keys:**
- `scalingIntensity`, `nodeSize`, `edgeFading`, `edgeThickness`
- `era_physics_settings` (JSON object with all physics params)

Settings persist across browser sessions.

---

## Testing

### Visual Validation Tests

**Location:** `tests/test_visual_*.py`

**Purpose:** Screenshot-based validation to catch visual regressions

#### test_visual_nodesize.py
```bash
python3 tests/test_visual_nodesize.py
```
- Takes screenshots at Node Size 0.5, 1.0, 2.0
- Verifies 4x visual size difference between extremes
- **Result:** ✅ Passing (as of Oct 22, 2025)

#### test_visual_centralgravity.py
```bash
python3 tests/test_visual_centralgravity.py
```
- Measures mobile node spread at gravity 0.05, 0.4, 0.6
- Verifies tighter = smaller spread
- **Result:** ❌ Failing - tight config spreads nodes more (inverted)

#### test_slider_interactions.py
```bash
python3 tests/test_slider_interactions.py
```
- Tests slider behavior through multiple modal open/close cycles
- Verifies no state corruption between Physics/Network modals
- **Result:** ✅ Passing

### Test Strategy

**Why Screenshot Tests:**
- JavaScript values can change without visual effect
- vis.js rendering is complex (physics, scaling, canvas)
- Only way to validate "it looks right" is to look at it

**Test Pattern:**
```python
# 1. Load page
page.goto('http://localhost:8765')

# 2. Change setting
page.evaluate("document.getElementById('nodeSize').value = 2.0")
page.evaluate("document.getElementById('nodeSize').dispatchEvent(new Event('input'))")

# 3. Screenshot
page.screenshot(path='nodesize_2.0.png')

# 4. Measure (if possible)
spread = page.evaluate("/* calculate geometric spread */")
```

**Guidelines:**
- Always hard-refresh browser before manual testing (`Cmd+Shift+R`)
- Check both data values AND visual rendering
- Screenshot tests run on `localhost:8765` (must start server first)

---

## Future Work

### Planned Improvements

1. **Centrality-Based Spreading**
   - Variable spring length based on distance from center
   - Longer edges for central nodes → less crowding
   - Implementation: Option B from discussion (Oct 22, 2025)

2. **Fix Central Gravity**
   - Investigate Town Hall ring interference
   - Possibly implement custom radial force field
   - See KNOWN_ISSUES.md

3. **Repulsion Slider**
   - Expose `gravitationalConstant` (-2000 default)
   - Allow user to boost repulsion → spread central core
   - Recommended range: -1000 to -5000

4. **Better Visual Feedback**
   - Show physics "heat map" (which areas are active)
   - Edge length visualization
   - Connection count overlay

---

## Quick Reference

**Problem:** Nodes aren't resizing when I change Node Size slider  
**Solution:** Must update `scaling.min/max` AND call `redraw()`. See lines 1187-1202.

**Problem:** Central Gravity slider does the opposite of what I expect  
**Solution:** Known issue. Use Node Spacing slider instead.

**Problem:** Physics sliders stopped working after using Network modal  
**Solution:** Was a bug (fixed Oct 21, 2025). Hard-refresh browser.

**Problem:** Test passes but visual is wrong  
**Solution:** Test is checking data values, not rendered output. Use screenshot tests.

**Problem:** Want to spread out central nodes without affecting peripheral ring  
**Solution:** Increase Node Spacing (175→250) or reduce Edge Springs (0.04→0.02).

---

## Change Log

**Oct 22, 2025:**
- Updated slider ranges with wider "elbow room"
- Moved defaults to middle of ranges
- Central Gravity: 0.15→0.4, Node Spacing: 120→175, Edge Springs: 0.02→0.04

**Oct 21, 2025:**
- Fixed Node Size slider visual rendering (added `setOptions` + `redraw`)
- Fixed Physics slider position recalculation on modal open
- Added screenshot-based visual tests

**Oct 20, 2025:**
- Renamed "Scaling Intensity" → "Node Scaling"
- Added Node Size slider (0.5-2.0)
- Fixed Edge Fading and Edge Thickness labels

---

**Back to:** [README.md](README.md)


---

## FILE: ERA_Landscape/KNOWN_ISSUES.md

**Path:** `ERA_Landscape/KNOWN_ISSUES.md`

# Known Issues - ERA Landscape

**See also:** [NETWORK_ARCHITECTURE.md](NETWORK_ARCHITECTURE.md) for technical details

## Active Issues

### ❌ Central Gravity Slider Inverted Behavior (Oct 22, 2025)
**Status:** Broken - produces opposite of expected behavior  
**Symptom:** Higher central gravity spreads nodes MORE instead of pulling them tighter

**Evidence:** Visual test `test_visual_centralgravity.py`
- Baseline (0.4): 5704px spread
- Tight (0.6): 6829px spread ❌ (should be < baseline)
- Loose (0.05): 7699px spread ✅ (correctly larger)

**Hypothesis:** 65 fixed Town Halls at periphery (`physics: false`) interfere with barnesHut centralGravity calculations

**Workaround:** Use Node Spacing slider instead to control layout density

**Planned Fix:** Investigate centrality-based spreading system (variable spring length by distance from center) - see NETWORK_ARCHITECTURE.md "Future Work"

---

## Recently Resolved (Oct 22, 2025)

### ✅ RESOLVED: Node Size Slider Not Working Visually (Oct 21-22, 2025)
**Status:** Fixed - nodes now resize visually when slider moves  
**Symptom:** Node Size slider changed JavaScript `value` but nodes didn't change size on screen

**Root Cause:** vis.js requires BOTH:
1. Update node `value` properties
2. Update `scaling.min/max` range
3. Call `network.redraw()`

**Fix Applied:**
```javascript
// Update vis.js scaling range based on nodeSize multiplier
window.network.setOptions({
  nodes: {
    scaling: {
      min: baseMin * networkConfig.nodeSize,
      max: baseMax * networkConfig.nodeSize
    }
  }
});
window.network.redraw();
```

**Validation:** Screenshot test `test_visual_nodesize.py` confirms 4x visual size difference ✅

### ✅ RESOLVED: Slider Ranges Too Narrow (Oct 22, 2025)
**Status:** Fixed - all sliders now have wider ranges with defaults in middle

**Changes:**
- Network Settings: All ranges expanded (Node Size 0.5-2.0 → 0.2-3.0, etc.)
- Physics Settings: Ranges expanded, defaults moved to middle (Central Gravity 0.15 → 0.4)
- Provides "elbow room" for experimentation

## Recently Added (Oct 21, 2025)

### ✅ Town Hall Network Visualization Complete
**Added:** Town Hall integration with Network settings panel  
**Features:**
- 65 Town Halls positioned in circular ring at periphery (radius 1000px)
- Grey edges with distance-based thickness/opacity
  - <450px: Thick (2.5 width), 80% opacity
  - 450-700px: Medium thickness, fading
  - >700px: Thin (0.5 width), nearly invisible
- Network settings panel with 3 sliders:
  - Scaling Intensity: 0 (constant) → 1 (logarithmic)
  - Edge Fading: 0 (no fade) → 1 (50% reduction)
  - Edge Thickness: 0 (base) → 2 (2x multiplier)
- Settings persist to localStorage
- Initial zoom: scale 0.8 for better overview

**Tests:** 3 Playwright tests created, all passing

---

## Recently Resolved

### 1. ✅ RESOLVED: Nodes Not Settling (Oct 21, 2025)
**Status:** Fixed - nodes settle naturally within 5-10 seconds  
**Symptom:** Nodes continue to move/wiggle indefinitely, never stabilizing  

**Root Cause Analysis:**
- Stabilization was being disabled during slider adjustments
- Low damping (0.09) wasn't stopping motion effectively
- Low minVelocity (0.1) allowed tiny movements to continue indefinitely
- Stabilization was being re-disabled on every slider change

**Fix Applied:**
- Increased damping: 0.09 → 0.15 (stops motion faster)
- Increased minVelocity: 0.1 → 0.75 (stops tiny movements)
- Added flag to track when actively adjusting vs initial load
- Only disable stabilization during active slider adjustment
- Force stabilization on Done button with explicit trigger
- Increased timeout from 500ms → 800ms before re-enabling

**Additional Fix (Oct 21, 7:44pm):**
- Removed Settle button (was freezing nodes and preventing dragging)
- Changed strategy: NO stabilization after initial load
- Increased minVelocity: 0.75 → 1.5 (stops movements < 1.5 units/frame)
- Reduced timestep: 0.5 → 0.35 (smoother physics simulation)
- Increased damping to 0.15 (was 0.09)
- All stabilization triggers removed - rely purely on physics parameters

**Theory:** High damping + high minVelocity should naturally stop micro-movements without locking nodes

**Final Tuning (Oct 21, 7:47pm):**
- User confirmed nodes DO settle but too slowly (~15-20 seconds)
- Increased damping: 0.15 → 0.35 (133% increase = much faster deceleration)
- Increased minVelocity: 1.5 → 2.5 (67% increase = stops sooner)
- Goal: Settle within 5-8 seconds

**Status:** Nodes now settle naturally while remaining draggable throughout

---

### ✅ Event Type Added for Town Halls (Oct 21, 2025)
**Added:** New 'event' node type with hexagon shape, grey color, reduced scaling (30% rate, max 10)

### ✅ Town Hall Linear Chain (Oct 21, 2025)
**Fixed:** Town Halls now form linear chain (Project → TH 01 → TH 02...) instead of all connecting to umbrella

### ✅ Modal UI Improvements (Oct 21, 2025)
**Fixed:** 
- Removed grey overlay from modals (transparent background)
- Physics controls redesigned with centered labels, endpoint labels (loose/tight, etc.)
- Values now float and follow slider handles

### ✅ Double-click opens both modal and URL (Oct 21, 2025)
**Fixed:** Removed duplicate doubleClick handler

### ✅ Orphan nodes drifting too far (Oct 21, 2025)
**Fixed:** Position orphans in circle near center, increased central gravity to 0.15

### ✅ Curation modal opens on single-click (Oct 21, 2025)
**Fixed:** Changed to double-click only

### ✅ Physics modal styling (Oct 21, 2025)
**Fixed:** Made draggable, semi-transparent, narrower (380px)

### ✅ Physics settings not persisted (Oct 21, 2025)
**Fixed:** Save to localStorage, restore on load


---

## FILE: ERA_Landscape/DEVELOPMENT.md

**Path:** `ERA_Landscape/DEVELOPMENT.md`

# Development Guide

## ⚠️ WORKFLOW REQUIREMENT

**ALWAYS use branch-based workflow. NEVER push directly to main.**

```bash
# For features:
git checkout -b feat/feature-name

# For fixes:
git checkout -b fix/bug-description

# After changes:
git push origin <branch-name>
gh pr create  # or create PR on GitHub
```

**Only merge to main through PR after review.**

---

## Overview

This is a **static HTML project** (20KB file, ~350+ nodes auto-loaded from Google Sheets). No build tools, no bundlers, no compilation.

**Edit → Save → Test with HTTP server → Push to branch → Create PR → Merge → Auto-deploys**

**Critical:** Must use HTTP/HTTPS (not `file://`) - Google Sheets API requirement.

---

## Project Structure

```
ERA_Landscape_Static/
├── index.html          # Main HTML file
├── graph.js            # JavaScript (external file)
├── README.md           
├── DEVELOPMENT.md      # This file
└── tests/
    └── test_load.py    # Playwright test
```

---

## How to Make Changes

### Edit HTML

```bash
# Open in editor
code index.html

# Make changes to structure, styling, API config

# Test locally (MUST use HTTP server)
python3 -m http.server 8000
open http://localhost:8000

# Check console for:
# - "✅ Google Sheets API client initialized"
# - "✅ Loaded XXX nodes, YYY edges from Sheets"
# - "🎉 Initial data load complete"

# Commit
git add index.html
git commit -m "Update HTML structure"
git push
```

### Edit JavaScript

```bash
# Open in editor
code graph.js

# Make changes to logic, event handlers, API calls

# Test locally (MUST use HTTP server)
python3 -m http.server 8000
open http://localhost:8000
# Refresh browser to see changes

# Commit
git add graph.js
git commit -m "Update graph logic"
git push
```

---

## Testing

### Manual Testing

```bash
# Start HTTP server (REQUIRED)
python3 -m http.server 8000

# Open in browser
open http://localhost:8000

# Check console for success messages:
# 1. "🔧 Initializing Google Sheets API..."
# 2. "✅ Google Sheets API client initialized"
# 3. "✅ Loaded XXX nodes, YYY edges from Sheets"
# 4. "🎉 Initial data load complete"

# Check graph:
# - ~350+ nodes display
# - Colors match legend (person=blue, org=teal, project=purple)
# - Nodes are draggable

# Test features:
# - Refresh button (re-loads from Sheet)
# - Search/filter
# - Hide/show nodes
# - Sign In button (OAuth flow)
# - Save functionality (after sign-in)

# Check for errors:
# (Right-click → Inspect → Console)
# Should see NO red errors
```

### Automated Testing

```bash
# Install Playwright (one time)
pip install playwright
playwright install

# Run integration test
python3.9 tests/test_sheets_integration.py

# Expected output:
# ✅ API initialization started
# ✅ gapi.client.init() called
# ✅ API initialization completed
# ✅ gapi.client.sheets available
# ✅ No JavaScript errors
# ✅ Refresh button exists
# ✅ Refresh loads data from Sheets
# ✅ Sign In button exists
# Passed: 8/8

# Test live site
python3.9 /tmp/test_live_site.py  # (if you have the script)
```

---

## Google Sheets API Setup

### Current Configuration

**Sheet ID**: `1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY`  
**API Key**: `AIzaSyBp23GwrTURmM3Z1ERZocotnu3Tn96TmUo`  
**OAuth Client ID**: `57881875374-flipnf45tc25cq7emcr9qhvq7unk16n5.apps.googleusercontent.com`

These are embedded in `index.html`.

### To Use Your Own Sheet

1. **Copy the Sheet**
   - Open [the current Sheet](https://docs.google.com/spreadsheets/d/1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY/edit)
   - File → Make a copy
   - Note the new Sheet ID (from URL)

2. **Get Google Cloud Credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Create project (if needed)
   - Enable Google Sheets API
   - Create API Key (for read access)
   - Create OAuth Client ID (for write access)
   - Add authorized JavaScript origins: `http://localhost:8000`, your GitHub Pages URL

3. **Update index.html**
   ```javascript
   const SHEET_ID = 'YOUR_SHEET_ID_HERE';
   const API_KEY = 'YOUR_API_KEY_HERE';
   const CLIENT_ID = 'YOUR_CLIENT_ID_HERE';
   ```

4. **Make Sheet Public**
   - Open your Sheet
   - Click "Share"
   - Change to "Anyone with the link can view"
   - API Key can now read it

---

## Common Tasks

### Add a New Feature

```bash
# 1. Create feature branch
git checkout -b feat/my-feature

# 2. Edit files
code index.html
code graph.js

# 3. Test locally
open index.html

# 4. Commit
git add .
git commit -m "feat: Add my feature"

# 5. Push and create PR
git push origin feat/my-feature
# (Create PR on GitHub)
```

### Fix a Bug

```bash
# 1. Create fix branch
git checkout -b fix/bug-description

# 2. Edit files
code graph.js

# 3. Test
open index.html

# 4. Commit & push
git add .
git commit -m "fix: Bug description"
git push origin fix/bug-description
```

### Deploy Changes to GitHub Pages

```bash
# 1. Merge to main
git checkout main
git merge feat/my-feature

# 2. Push
git push

# 3. Wait for GitHub Pages build (~1-2 minutes)
# Check build status:
gh api repos/jonschull/ERA_Landscape_Static/pages/builds/latest | jq -r '.status'
# Should show: "built"

# 4. Verify live site
open https://jonschull.github.io/ERA_Landscape_Static/

# 5. Test live site
# - Check console for auto-load messages
# - Verify node count matches Sheet
# - Test Refresh button
# - Test Sign In flow
```

---

## Debugging

### Console Errors

**Open browser console:**
- Chrome: Cmd+Option+J (Mac) or F12 (Windows)
- Firefox: Cmd+Option+K (Mac) or F12 (Windows)
- Safari: Cmd+Option+C (Mac)

**Common errors:**

1. **"Failed to fetch"**
   - Sheet might not be public
   - API key might be invalid
   - Check Network tab for details

2. **"nodes is not defined"**
   - JavaScript loading order issue
   - Check if `graph.js` loads before it's used

3. **"gapi is not defined"**
   - Google API library didn't load
   - Check `<script src="https://apis.google.com/js/api.js"></script>`

### Network Tab

Watch API calls:
1. Open DevTools → Network tab
2. Refresh page
3. Look for calls to `sheets.googleapis.com`
4. Check status codes (should be 200)
5. Inspect response data

---

## File Organization

### index.html

**Sections:**
- `<head>` - Metadata, styles, Google API libraries
- `<body>` - UI elements (toolbar, modals, graph container, loading screen)
- `<script>` (inline) - Configuration, Google Sheets API functions, empty DataSets
- `<script src="graph.js">` - Main logic (external file)

**Key elements:**
- `#loading` - Loading screen (shows until data loads)
- `#network` - Graph container (vis-network renders here)
- `#toolbar` - Buttons and controls (Fit, Highlight, Refresh, etc.)
- `#signInBtn` - OAuth sign-in button
- Toast notifications for user feedback

**Important functions:**
- `initSheetsApi()` - Initializes Google Sheets API, auto-loads data
- `loadDataFromSheets()` - Fetches nodes & edges from Sheet
- `saveDataToSheets()` - Writes changes back to Sheet
- `getNodeVisuals(type)` - Returns color/shape for node type (DRY)
- `parseTypeFromId(id)` - Extracts type from ID prefix
- `hideLoading()` - Hides loading screen after data ready

### graph.js

**Sections:**
- Graph initialization (vis-network setup with empty DataSets)
- Toolbar logic (buttons, filters)
- Quick Editor (add/remove connections)
- Event handlers (node clicks, double-clicks)
- Utility functions

**Note:** Google Sheets functions are in `index.html` inline script

---

## Best Practices

### 1. Keep It Simple
- No build tools needed
- No npm, webpack, babel
- Just edit HTML/JS directly

### 2. Test Locally First
- **MUST use HTTP server**: `python3 -m http.server 8000`
- **NEVER test with `file://`** - Google Sheets API won't work
- Check console for auto-load success messages
- Verify node count matches Sheet (~350+)
- Test all buttons/features

### 3. Small Commits
- One logical change per commit
- Clear commit messages
- Easy to revert if needed

### 4. Document Changes
- Update README if adding features
- Add comments to complex code
- Update this file if workflow changes

---

## GitHub Pages Configuration

**Already configured! Every push to main auto-deploys.**

**Current settings:**
- URL: https://jonschull.github.io/ERA_Landscape_Static/
- Source: Deploy from a branch
- Branch: `main`
- Folder: `/` (root)
- Build type: `legacy` (standard Jekyll)
- HTTPS: Enforced

**To check deployment status:**
```bash
# Check latest build
gh api repos/jonschull/ERA_Landscape_Static/pages/builds/latest

# Just get status
gh api repos/jonschull/ERA_Landscape_Static/pages/builds/latest | jq -r '.status'

# Should return: "built" when complete
```

**Build times:**
- First deploy: ~1-2 minutes
- Subsequent updates: ~30-60 seconds

**Files needed:**
- `index.html` (must be in root)
- `graph.js` (must be in root)

**To manually enable (if needed):**
```bash
gh api repos/jonschull/ERA_Landscape_Static/pages -X POST \
  -F 'source[branch]=main' -F 'source[path]=/'
```

---

## Relationship to ERA_ClimateWeek

**Parent Project**: [ERA_Admin](https://github.com/jonschull/ERA_Admin)  
**Related**: [ERA_ClimateWeek](https://github.com/jonschull/ERA_ClimateWeek)

**What it does:**
- Python data processing pipeline
- Imports from CSV
- Transforms data
- Writes to Google Sheets
- Flask development server
- Generates HTML templates

**What THIS project does:**
- Uses the data (from Sheets)
- Pure client-side viewer
- No Python required
- Production-ready

**Workflow:**
```
ERA_ClimateWeek (Python)
  ↓ Process data
  ↓ Write to Google Sheets
  ↓
ERA_Landscape_Static (HTML/JS)
  ↓ Read from Google Sheets
  ↓ Display in browser
  ↓ Users can edit
  ↓ Save back to Sheets
```

---

## Future Enhancements

Potential improvements:
- [ ] Add CSS file (separate from HTML)
- [ ] Add TypeScript for type safety
- [ ] Bundle with Vite (if complexity grows)
- [ ] Add service worker (offline support)
- [ ] Add PWA manifest (install as app)

**But keep it simple unless there's a real need!**

---

## Questions?

- **How do I add a feature?** Edit the files, test, commit
- **Where's the build step?** There isn't one!
- **How do I deploy?** Just push to main
- **Can I use a different hosting?** Yes, any static host works

**Philosophy:** Simple is better. Edit HTML/JS directly. No unnecessary tooling.


---

## FILE: ERA_Landscape/TESTING.md

**Path:** `ERA_Landscape/TESTING.md`

# Testing Guide

---

## AI Assistant Orientation

**If you're an AI assistant reading this for the first time:**

This file explains HOW to test. Before using these commands, you should:
1. Have already read `HANDOFF_SUMMARY.txt` and `AI_HANDOFF_GUIDE.md`
2. Know which feature you're working on
3. Understand the testing workflow: Manual browser test → Playwright test → User verification

**Key testing principle:** Test before claiming success. Open in browser, check console, run tests, THEN report results to user.

---

## Testing Workflow

### Step 1: Manual Browser Test (ALWAYS FIRST)

```bash
# Open in browser
open index.html

# Or specify browser
open -a "Google Chrome" index.html
open -a "Microsoft Edge" index.html
```

**What to check:**
1. **Console** (Cmd+Option+J in Chrome/Edge)
   - No red errors
   - API initialization messages present
   - No "failed to load" warnings

2. **Visual**
   - Graph displays
   - Nodes and edges visible
   - Toolbar present
   - No broken layout

3. **Functionality**
   - Click a node → modal opens
   - Click a button → action happens
   - Type in search → filtering works

**NEVER claim success without doing this first.**

---

### Step 2: Playwright Test (SECOND)

```bash
cd tests
python test_load.py
```

**Expected output:**
```
1. Loading file: file:///path/to/index.html
2. Waiting for page to initialize...
   Graph container: ✅ found
   Toolbar: ✅ found

3. JavaScript errors: 0

4. Console messages:
   [log] Google Sheets API initialized
   ...

5. Graph data:
   Nodes: 352
   Edges: 220

=== VERDICT ===
✅ Graph container present
✅ No JavaScript errors
✅ Data loaded (352 nodes)

✅ TEST PASSED
```

---

### Step 3: User Verification (THIRD)

After YOUR tests pass, ask user to verify:

```
✅ Feature tested and working

Changes:
- [List what changed]

Evidence:
- Browser test: No console errors
- test_load.py: PASSED
- [Screenshot if applicable]

Please verify:
1. Open index.html
2. [Specific action to test]
3. Confirm [expected result]
```

---

## Browser Compatibility Testing

### Target Browsers

**Must work in:**
- ✅ Chrome 118+
- ✅ Edge 118+

**Nice to have:**
- ⚠️ Firefox 119+
- ⚠️ Safari 17+

### How to Test Multiple Browsers

```bash
# Chrome
open -a "Google Chrome" index.html
# Check console, test feature

# Edge
open -a "Microsoft Edge" index.html
# Check console, test feature
```

**Test in BOTH Chrome and Edge before claiming success.**

### Browser-Specific Issues

**Chrome/Edge:**
- Full ES6 support
- Fetch API works
- Google Sheets API works

**Firefox:**
- May have different console formatting
- Check for async/await support

**Safari:**
- More strict about CORS
- May need different OAuth flow

---

## Manual Testing Checklist

### Basic Functionality

Run through this checklist after any change:

**Page Load:**
- [ ] index.html opens without errors
- [ ] Console shows no red errors
- [ ] Graph container visible
- [ ] Toolbar present

**Data Loading:**
- [ ] Data loads from Sheets (or embedded fallback)
- [ ] Node count correct (~352)
- [ ] Edge count correct (~220)
- [ ] No "failed to fetch" errors

**Graph Interaction:**
- [ ] Can drag nodes
- [ ] Can zoom (scroll wheel)
- [ ] Can pan (click and drag background)
- [ ] Click node → something happens (modal/selection)

**Toolbar:**
- [ ] All buttons present
- [ ] Refresh button works
- [ ] Search boxes work
- [ ] Save button present

**Quick Editor:**
- [ ] Can select From node
- [ ] Can select To node
- [ ] Can add edge
- [ ] Can remove edge
- [ ] Changes reflect in graph

**Modals:**
- [ ] Click node → modal opens
- [ ] Modal shows node data
- [ ] Can edit fields
- [ ] Can close modal

---

## Automated Testing

### Current Tests

**test_load.py** - Basic loading test
- Opens index.html in headless browser
- Checks for graph container
- Checks for toolbar
- Checks for JavaScript errors
- Verifies basic structure

### Running Tests

```bash
# Run single test
cd tests
python test_load.py

# Run with headed browser (see what happens)
# (modify test to set headless=False)
```

### Test Structure

```python
def test_feature():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Load page
        page.goto('file:///path/to/index.html')
        
        # Wait for elements
        page.wait_for_selector('#network')
        
        # Test feature
        button = page.query_selector('#myButton')
        assert button is not None
        button.click()
        
        # Verify result
        result = page.query_selector('#result')
        assert result.text_content() == 'Expected'
        
        browser.close()
```

### Screenshots in Tests

```python
# Take screenshot for visual verification
page.screenshot(path='feature_test.png')
```

---

## Testing New Features

### Feature Development Workflow

1. **Plan the test FIRST**
   - What should happen?
   - How to verify it?
   - What could go wrong?

2. **Implement the feature**
   - Make minimal change
   - Test in browser immediately

3. **Verify with checklist**
   - [ ] Feature works as expected
   - [ ] No console errors
   - [ ] Doesn't break existing features
   - [ ] Works in Chrome AND Edge

4. **Write/update automated test**
   - Add test case to test_load.py
   - Or create new test file

5. **Document**
   - Update README if user-facing
   - Update this file if testing workflow changed

---

## Console Debugging

### Opening Console

**Chrome/Edge:**
- Mac: Cmd+Option+J
- Windows: F12

**Firefox:**
- Mac: Cmd+Option+K
- Windows: F12

**Safari:**
- Mac: Cmd+Option+C
- Enable: Safari → Preferences → Advanced → Show Develop menu

### What to Look For

**✅ Good signs:**
```
[log] Google Sheets API initialized
[log] Graph rendered with 352 nodes
[log] Data loaded successfully
```

**❌ Bad signs:**
```
[error] Failed to load resource: net::ERR_FILE_NOT_FOUND
[error] Uncaught ReferenceError: gapi is not defined
[error] Cannot read properties of null (reading 'addEventListener')
```

### Common Errors

**"gapi is not defined"**
- Google API library didn't load
- Check `<script src="https://apis.google.com/js/api.js"></script>`

**"Failed to fetch"**
- Sheet not public
- Invalid API key
- Rate limit exceeded

**"nodes is not defined"**
- Script loading order issue
- vis-network not initialized
- Check script tags order

---

## Network Tab Debugging

### Watch API Calls

**Chrome/Edge DevTools:**
1. Open DevTools (F12)
2. Click "Network" tab
3. Refresh page
4. Look for calls to `sheets.googleapis.com`

**What to check:**
- Status: 200 (success)
- Response: Contains data
- Time: <1s typically

**Common issues:**
- Status 403: Permission denied (Sheet not public)
- Status 429: Rate limit exceeded
- Status 401: Invalid API key

---

## Performance Testing

### Load Time

**Acceptable:**
- Page loads: <2 seconds
- Data fetched: <1 second
- Graph rendered: <3 seconds

**How to measure:**
```javascript
// Add to console
console.time('load');
// ... do action ...
console.timeEnd('load');
```

### Large Datasets

**Current:** 352 nodes, 220 edges (works fine)

**If graph grows:**
- Test with 1000+ nodes
- Check rendering performance
- May need physics optimizations

---

## Regression Testing

### After ANY Change

Run this quick check:

```bash
# 1. Open in browser
open index.html

# 2. Quick smoke test
# - Graph displays? ✅
# - Console clean? ✅
# - Buttons work? ✅

# 3. Run automated test
cd tests && python test_load.py

# 4. If all pass → safe to commit
git add .
git commit -m "Description of change"
```

### Before Creating PR

Full regression:

```bash
# 1. Test in Chrome
open -a "Google Chrome" index.html
# - Full manual checklist
# - Check console
# - Test all features

# 2. Test in Edge
open -a "Microsoft Edge" index.html
# - Same checklist
# - Verify no Edge-specific issues

# 3. Run all Playwright tests
cd tests
python test_load.py
# (Add more as they're created)

# 4. All pass? → Create PR
gh pr create --title "feat: Feature name"
```

---

## Writing New Tests

### Test Template

```python
#!/usr/bin/env python3
"""Test description"""

from playwright.sync_api import sync_playwright
import os

def test_my_feature():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    index_path = os.path.join(parent_dir, 'index.html')
    file_url = f'file://{index_path}'
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Collect errors
        errors = []
        page.on('pageerror', lambda err: errors.append(str(err)))
        
        print("1. Loading page...")
        page.goto(file_url, wait_until='networkidle')
        
        print("2. Testing feature...")
        # Your test code here
        
        print("3. Verifying result...")
        # Your assertions here
        
        browser.close()
        
        # Verdict
        if errors:
            print(f"❌ TEST FAILED: {len(errors)} errors")
            return False
        else:
            print("✅ TEST PASSED")
            return True

if __name__ == "__main__":
    success = test_my_feature()
    exit(0 if success else 1)
```

---

## Troubleshooting

### Test Fails with "File Not Found"

```bash
# Check path
ls index.html  # Should exist

# Use absolute path in test
index_path = os.path.abspath('index.html')
```

### Browser Cache Issues

```bash
# Clear Playwright cache
playwright install --force

# Or open with cache disabled
# (modify test to use incognito context)
```

### Timeout Errors

```python
# Increase timeout
page.wait_for_selector('#network', timeout=10000)  # 10 seconds
```

### Headless vs Headed

```python
# See what's happening
browser = p.chromium.launch(headless=False)

# Slow down actions
page.goto(url)
time.sleep(2)  # Watch what happens
```

---

## Key Principles

1. **Test in browser FIRST** - Before running Playwright
2. **Check console** - Red errors = something's wrong
3. **Test in Chrome AND Edge** - Both must work
4. **Small changes, test immediately** - Don't accumulate untested code
5. **Never claim success without proof** - Screenshots, test output, console clean

---

## Questions?

- **How do I test X?** → Open in browser, try it, check console
- **Test fails, what now?** → Look at error message, debug in browser
- **Need to see what's happening?** → Set `headless=False` in test

**When in doubt:** Open index.html in Chrome, open console, and see what's actually happening.


---

## FILE: ERA_Landscape/DEPLOYMENT_GUIDE.md

**Path:** `ERA_Landscape/DEPLOYMENT_GUIDE.md`

# Deployment Guide - ERA Landscape Static

**Quick Links:**

- **Live Site**: https://jonschull.github.io/ERA_Admin/ERA_Landscape/
- **Repository**: https://github.com/jonschull/ERA_Admin (ERA_Landscape/ component)
- **Historical repo**: https://github.com/jonschull/ERA_Landscape_Static (archived)
- **Google Sheet**: https://docs.google.com/spreadsheets/d/1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY/edit

---

## 🚀 How to Update the Live Site

### Step-by-Step Workflow

```bash
# 1. Make your changes
code index.html  # or graph.js

# 2. Test locally (REQUIRED - must use HTTP server)
python3 -m http.server 8000
open http://localhost:8000

# 3. Check console for success:
#    ✅ "Google Sheets API client initialized"
#    ✅ "Loaded XXX nodes, YYY edges from Sheets"
#    ✅ "Initial data load complete"

# 4. Verify functionality:
#    - Graph displays with ~350+ nodes
#    - Colors match legend (person=blue, org=teal, project=purple)
#    - Refresh button works
#    - No console errors

# 5. Commit changes
git add .
git commit -m "Brief description of changes"

# 6. Push to GitHub
git push

# 7. Wait for GitHub Pages build (~1-2 minutes)
# Check status:
gh api repos/jonschull/ERA_Landscape_Static/pages/builds/latest | jq -r '.status'
# Should return: "built"

# 8. Verify live site
open https://jonschull.github.io/ERA_Landscape_Static/

# 9. Test live site functionality:
#    - Data loads automatically
#    - Console shows success messages
#    - All features work
```

---

## 📋 Pre-Flight Checklist

Before pushing to production, verify:

- [ ] Tested locally with HTTP server (not `file://`)
- [ ] Console shows no red errors
- [ ] Data loads automatically (~350+ nodes)
- [ ] Colors match legend
- [ ] Refresh button works
- [ ] Search/filter works
- [ ] Graph is interactive (drag, zoom, pan)
- [ ] Commit message is descriptive
- [ ] No sensitive data in commit

---

## 🔍 Troubleshooting Deployment

### Build Fails

**Check build status:**

```bash
gh api repos/jonschull/ERA_Landscape_Static/pages/builds/latest
```

**Common issues:**

- Syntax error in HTML/JS → Check console locally first
- File too large → We're at 20KB, shouldn't be an issue
- Branch not found → Ensure you pushed to `main`

### Site Doesn't Update

**Possible causes:**

1. **Browser cache** → Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+F5` (Windows)
2. **Build still running** → Wait 1-2 minutes, check build status
3. **CDN cache** → Can take up to 10 minutes to propagate globally

**Force verify:**

```bash
# Check what's actually deployed
curl -s https://jonschull.github.io/ERA_Landscape_Static/ | grep -o "ERA Graph"
```

### Data Doesn't Load

**Check:**

1. **Console errors** → Open DevTools and check for red errors
2. **API key** → Verify `API_KEY` in `index.html` is correct
3. **Sheet permissions** → Sheet must be publicly readable
4. **Network tab** → Check if API calls are succeeding (200 status) 

---

## 🛠️ Emergency Rollback

If you need to quickly revert to a previous version:

```bash
# 1. Find the last good commit
git log --oneline -10

# 2. Revert to that commit
git reset --hard <commit-hash>

# 3. Force push (use with caution)
git push --force

# 4. Wait for rebuild (~1-2 minutes)
```

**Example:**

```bash
git log --oneline -5
# 4549952 docs: Complete documentation update
# 136a216 docs: Update README with live GitHub Pages URL
# 4df11ff feat: Remove embedded data, auto-load from Sheets

# Roll back to before recent changes:
git reset --hard 4df11ff
git push --force
```

---

## 📊 Monitoring

### Check Site Health

**Automated test:**

```bash
python3.9 tests/test_sheets_integration.py
```

**Manual verification:**

1. Visit https://jonschull.github.io/ERA_Landscape_Static/
2. Open console (Cmd+Option+J)
3. Verify messages:
   - "🔧 Initializing Google Sheets API..."
   - "✅ Google Sheets API client initialized"
   - "✅ Loaded XXX nodes, YYY edges from Sheets"
   - "🎉 Initial data load complete"
4. Check node count matches Google Sheet
5. Test Refresh button
6. Test Search/filter

### Performance Metrics

**Expected:**

- Page load: <1 second (HTML parse)
- API init: ~2-3 seconds
- Data load: ~1-2 seconds
- Total to interactive: ~3-5 seconds

**Monitor:**

- Use Chrome DevTools → Network tab
- Check "Finish" time
- Look for slow API calls

---

## 🔒 Security Notes

### API Keys

Current credentials in `index.html`:

- `API_KEY`: For read-only access to public Sheet
- `CLIENT_ID`: For OAuth (write access)

**These are safe to commit** because:

- API Key is restricted to Sheets API only
- OAuth requires user sign-in
- Sheet is already public

**If compromised:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Regenerate API Key
3. Create new OAuth Client ID
4. Update `index.html`
5. Commit and push

### Sheet Permissions

**Required:**

- Sheet must be "Anyone with link can **view**"
- Write access requires OAuth sign-in

**To verify:**

1. Open Sheet
2. Click "Share"
3. Ensure "Anyone with the link" has "Viewer" access

---

## 📈 Analytics (Optional)

To add Google Analytics:

```html
<!-- Add to <head> in index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_GA_ID');
</script>
```

---

## 🎯 Quick Reference

| Task               | Command                                                                               |
| ------------------ | ------------------------------------------------------------------------------------- |
| Test locally       | `python3 -m http.server 8000`                                                       |
| Check build status | `gh api repos/jonschull/ERA_Landscape_Static/pages/builds/latest \| jq -r '.status'` |
| View live site     | `open https://jonschull.github.io/ERA_Landscape_Static/`                            |
| Run tests          | `python3.9 tests/test_sheets_integration.py`                                        |
| Check last commits | `git log --oneline -10`                                                             |
| View file size     | `ls -lh index.html`                                                                 |

**Bookmarks:**

- Live Site: https://jonschull.github.io/ERA_Admin/ERA_Landscape/
- Repository: https://github.com/jonschull/ERA_Admin
- Google Sheet: https://docs.google.com/spreadsheets/d/1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY/edit
- GitHub Pages Settings: https://github.com/jonschull/ERA_Admin/settings/pages

---

## 📚 Related Documentation

- **README.md** - Project overview and quick start
- **DEVELOPMENT.md** - Development guide with detailed workflows
- **NEXT_STEPS.md** - Project status and future enhancements
- **AI_HANDOFF_GUIDE.md** - Guidelines for AI assistants
- **DEPLOYMENT_GUIDE.md** - This file (deployment procedures)

---

## ✅ Success Criteria

Site is working correctly when:

- ✅ Page loads in <5 seconds
- ✅ Console shows API initialization success
- ✅ ~350+ nodes display
- ✅ Colors match legend
- ✅ Graph is interactive
- ✅ Refresh button works
- ✅ No console errors

**Current Status**: ✅ All criteria met, production ready!


---

## FILE: ERA_Landscape/AI_HANDOFF_GUIDE.md

**Path:** `ERA_Landscape/AI_HANDOFF_GUIDE.md`

# AI Assistant Handoff Guide
**For AI assistants picking up ERA_Landscape_Static**

**PURPOSE OF THIS FILE:**
- Testing methodology & principles
- Git workflow & discipline  
- Code patterns & architecture
- Command output verification
- Anti-patterns to avoid

**For project state, see HANDOFF_SUMMARY.txt:**
- What's done vs not done
- File inventory  
- Current git status
- Next steps roadmap
- Testing commands

---

## FIRST ACTIONS (Before Any User Interaction)

**Do this IMMEDIATELY when joining a conversation:**

1. **Read orientation docs** (in order):
   - `HANDOFF_SUMMARY.txt` - Overview and orientation checklist
   - This file (`AI_HANDOFF_GUIDE.md`) - Code patterns and testing
   - `TESTING.md` - Testing commands and workflow
   
2. **Assess project state**:
   - Check git branch: `git branch --show-current`
   - Check if `index.html` opens in browser (file://)
   - Review recent commits: `git log --oneline -5`
   - Check if any tests are failing
   
3. **Verify testing baseline**:
   - Run: `cd tests && python test_load.py`
   - Check console for JavaScript errors
   - Open `index.html` in browser manually
   
4. **Present status to user** (without being asked):
   ```
   ## Current Status
   - **Branch**: [main / feat/feature-name]
   - **Feature**: [What's being worked on]
   - **Tests**: [Passing / Failing / Unknown]
   - **Browser**: [Works / Has errors]
   - **Ready**: [Yes / Need clarification on X]
   ```

**DO NOT** wait for the user to ask "where are we?" - be proactive.

---

## Context You Need

### What This Project Is

Interactive graph visualization for climate/restoration network mapping. **Pure static HTML/JavaScript** that loads data directly from Google Sheets.

**Key Difference from ERA_ClimateWeek:**
- NO Python server (that's the parent project)
- NO Flask, NO backend
- Just HTML + JavaScript + Google Sheets API
- Deployable to GitHub Pages (or any static host)

### Architecture

```
User opens: index.html (file:// or https://jonschull.github.io/ERA_Landscape_Static/)
  ↓
Browser loads Google Sheets API libraries
  ↓
Fetches data from Google Sheet (API key for read)
  ↓
Renders interactive graph (vis-network.js)
  ↓
User clicks "Sign In" (optional, for editing)
  ↓
OAuth flow → authenticated
  ↓
User can save edits back to Sheet
```

**No server. No backend. Pure client-side.**

### Relationship to ERA_ClimateWeek

**Parent Project**: [ERA_Admin](https://github.com/jonschull/ERA_Admin)  
**Related**: [ERA_ClimateWeek](https://github.com/jonschull/ERA_ClimateWeek)
- Python data processing pipeline
- Imports from CSV, transforms data
- Writes to Google Sheets
- Flask development server
- Generates HTML templates

**This Project** (ERA_Landscape_Static):
- Uses the data (reads from same Google Sheet)
- Pure client-side viewer
- No Python required
- Production-ready for GitHub Pages

**Workflow:**
```
ERA_ClimateWeek (Python) → Process data → Write to Google Sheets
                                              ↓
                          ERA_Landscape_Static (HTML/JS) → Read from Sheets → Display
```

---

## CRITICAL DISCIPLINE (Core Principles)

### Your Predecessor's Approach

The AI assistant on ERA_ClimateWeek followed these principles - **YOU MUST TOO:**

1. **Test before claiming success** - Always verify with browser testing
2. **Small, incremental changes** - One feature at a time
3. **Never claim "fixed" without verification** - Test THEN report
4. **Respect user's time** - Be concise, don't hallucinate success
5. **Document everything** - Update docs after changes

### Red Flags You're Losing Context

- ❌ Making 3+ fixes in rapid succession without testing
- ❌ Saying "should work" instead of "tested, works"
- ❌ Not checking git log / current branch
- ❌ Assuming old docs are current
- ❌ Skipping the verification step
- ❌ Asking user to test before YOU test

### Recovery Steps

If you find yourself in a reactive loop:
1. **STOP** making changes
2. Read HANDOFF_SUMMARY.txt and this file
3. Check git log (what actually happened?)
4. Test current state in browser
5. Present status to user, ask for direction

---

## COMMAND OUTPUT DISCIPLINE

**CRITICAL RULE:** After EVERY command, READ and SUMMARIZE the output.

### The Problem

You can issue commands without reading their output. This leads to:
- Untracked files you don't notice
- Modified files you forget about
- Test failures you miss
- Broken state you don't detect

**Example failure:** Running `git status` 3 times, seeing "Untracked files: NEXT_STEPS.md" each time, but not noticing until user asks.

### The Fix

**After EVERY command, explicitly:**
1. Read the output
2. Check for unexpected results
3. Report what you found
4. Act on problems immediately

### Example: Good Workflow

```bash
$ git status
On branch main
Untracked files:
  NEXT_STEPS.md
nothing added to commit but untracked files present
```

**AI Response:**
"⚠️ `git status` shows NEXT_STEPS.md is untracked. Should I commit it?"

### Example: Bad Workflow

```bash
$ git status
[output ignored]
```

**AI Response:**
"✅ Everything committed" (WRONG - didn't read output)

---

## MANDATORY VERIFICATION CHECKLIST

**CRITICAL PRINCIPLE: Test behavior, not structure. Hunt for problems, not confirmations.**

**Before claiming work is "done" or "complete":**

### 1. Test in the Target Environment

**BAD:** Testing file:// when it needs HTTP/HTTPS  
**GOOD:** Test in the actual deployment environment

```bash
# If deploying to GitHub Pages:
python -m http.server 8000
# Then test at http://localhost:8000
```

**Why:** Code that works in one environment may fail in another. API restrictions, CORS, protocol differences all matter.

### 2. Execute the User Workflow (Don't Just Check Code Exists)

**BAD:** "Does the function exist?" ✅  
**GOOD:** "Does the function produce the expected result when called?"

**Example:**
```python
# BAD test
exists = page.evaluate("() => typeof loadDataFromSheets === 'function'")
# Just checks code is defined

# GOOD test  
click_refresh_button()
wait(3 seconds)
data_changed = check_if_nodes_count_changed()
console_shows_success = check_console_for("Loaded from Sheets")
# Actually runs the workflow and checks outcome
```

### 3. Hunt for Problems (Pessimistic Testing)

**Assume broken until proven working.**

**Check console for ANY unexpected output:**
```python
# Get ALL console messages
console_messages = page.get_console_messages()

# Look for problems
errors = [m for m in messages if m.type == 'error']
warnings = [m for m in messages if m.type == 'warning']
missing_expected = check_for_expected_messages([
    "✅ API initialized",
    "✅ Data loaded"
])

# Report EVERY problem found
if errors or warnings or missing_expected:
    print("❌ Found problems:")
    for e in errors: print(f"  ERROR: {e}")
    for w in warnings: print(f"  WARNING: {w}")
```

**Don't ignore warnings!** "Failed to execute postMessage" may seem minor but reveals the API won't work.

### 4. Verify User-Visible Outcomes (Not Internal State)

**What the USER sees/experiences matters, not what variables exist.**

**Check the screen:**
- Does the button actually DO something when clicked?
- Does data change after "Refresh"?
- Does the Sign In button change state after OAuth?
- Does the graph update after "Save"?

**Example:**
```python
# BAD: Checking internal state
sheetsApiReady_exists = evaluate("typeof sheetsApiReady !== 'undefined'")  # True!

# GOOD: Checking user outcome
click_sign_in()
button_text_after = get_button_text('#signInBtn')
oauth_popup_opened = check_for_new_window()
# Does user see what they should see?
```

### 5. Wait for Async Operations to Complete

**If initialization is async, WAIT and verify completion.**

```python
# BAD
page.goto(url)
check_if_api_ready()  # Too early!

# GOOD  
page.goto(url)
wait_for_console_message("✅ API initialized", timeout=5000)
# OR
wait(3 seconds)
check_console_for_completion_or_errors()
```

**If you see "🔧 Initializing..." but never see "✅ Initialized", that's a FAILURE.**

### 6. Git Status Check
```bash
git status
```

**Check for:**
- ✅ "nothing to commit, working tree clean" OR
- ⚠️ Explain any untracked/modified files and why they're not committed

### 7. Git History Check
```bash
git log --oneline -5
```

**Check for:**
- ✅ All expected commits present
- ✅ Latest commit has correct message
- ⚠️ Any uncommitted work?

---

## TESTING ANTI-PATTERNS (What NOT to Do)

### ❌ Confirmation Hunting
```python
✅ Function exists
✅ Button exists  
✅ Library loaded
→ "Integration complete!"  # WRONG - you didn't test if it WORKS
```

### ❌ Testing Structure Instead of Behavior
```python
# Checks code is there, not that it runs
typeof myFunction === 'function'  # ✅ exists
myFunction()  # Did you check what happens?
```

### ❌ Ignoring Console Warnings
```
[warning] Failed to execute postMessage...
```
"That's just a warning, ignore it" → WRONG! This reveals the API can't initialize.

### ❌ Testing in Wrong Environment
Testing file:// when it needs HTTP → You won't discover the actual problem.

### ❌ Not Waiting for Async
Checking API readiness immediately after calling async init() → False positive.

---

## TESTING BEST PRACTICES (What TO Do)

### ✅ Problem-Focused Testing
```
1. Look for errors in console
2. Look for missing expected messages  
3. Try the actual user workflow
4. Check if outcome matches expectation
5. Only THEN claim it works
```

### ✅ User Outcome Verification
"After clicking Refresh, does the graph data actually update?"  
"After clicking Sign In, does OAuth popup appear?"  
"After clicking Save, does console show save succeeded?"

### ✅ Environment-Aware Testing
"This requires HTTP, so I'll test with a local server."  
"This needs OAuth, so I'll test the redirect flow."  
"This writes to filesystem, so I'll verify the file was created."

---

## THE CORE PRINCIPLE

**Don't claim it works until you've seen it work in the conditions where it needs to work.**

Not: "The code is there" ✅  
But: "I used it like a user would, and it produced the expected result" ✅

### After Every File Creation

**When you create files:**
1. Create file → `write_to_file` tool
2. Verify exists → `ls -la [directory]`
3. Check git sees it → `git status`
4. Stage it → `git add [file]`
5. Verify staged → `git status` (should show "Changes to be committed")
6. Commit → `git commit -m "..."`
7. Verify committed → `git log --oneline -1`

**DO NOT skip steps 2, 3, 5, 7.** Always verify.

---

## Critical Files

### Core Files

**index.html** (~1500 lines)
- Complete standalone HTML file
- Google API configuration (SHEET_ID, API_KEY, CLIENT_ID)
- Google API library loading
- vis-network setup
- Graph initialization code
- Toolbar HTML (buttons, filters)
- Modal HTML structures
- Embedded data (currently - will be removed)

**graph.js** (~600 lines)
- Google Sheets read/write functions
- Graph rendering logic
- Event handlers (buttons, modals)
- Quick Editor functionality
- Search filtering
- Save/load operations

### Documentation

- `README.md` - Project overview, quick start
- `DEVELOPMENT.md` - Developer guide, how to edit
- `VISION.md` - Long-term collaborative mapping vision
- `NEXT_STEPS.md` - Current roadmap
- `.gitignore` - Standard ignore rules

### Testing

- `tests/test_load.py` - Playwright test (static HTML loading)
- More tests to be adapted from ERA_ClimateWeek

---

## Code Patterns to Follow

### 1. Google Sheets API Integration

```javascript
// Configuration (in index.html)
const SHEET_ID = '1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY';
const API_KEY = 'AIzaSyBp23GwrTURmM3Z1ERZocotnu3Tn96TmUo';
const CLIENT_ID = '57881875374-flipnf45tc25cq7emcr9qhvq7unk16n5.apps.googleusercontent.com';

// Initialize API (in graph.js or inline)
function initSheetsApi() {
  gapi.load('client', async () => {
    await gapi.client.init({
      apiKey: API_KEY,
      discoveryDocs: ['https://sheets.googleapis.com/$discovery/rest?version=v4']
    });
    // Ready to read
  });
}

// Read data (API key - no auth needed)
async function readSheetTab(tabName) {
  const response = await gapi.client.sheets.spreadsheets.values.get({
    spreadsheetId: SHEET_ID,
    range: `${tabName}!A:Z`
  });
  return response.result.values;
}

// Write data (requires OAuth)
async function writeSheetTab(tabName, data) {
  if (!sheetsApiReady) {
    // Trigger sign-in
    handleSignIn();
    return;
  }
  await gapi.client.sheets.spreadsheets.values.update({
    spreadsheetId: SHEET_ID,
    range: `${tabName}!A1`,
    valueInputOption: 'RAW',
    resource: { values: data }
  });
}
```

### 2. Node ID Convention

```javascript
// Always use typed IDs (same as parent project)
person::Jonathan Lever
org::Fetzer Institute  
project::ERA Africa

// Extract type from ID
const type = id.startsWith('person::') ? 'person' : 
             id.startsWith('project::') ? 'project' : 'organization';
```

### 3. vis-network DataSet

```javascript
// Initialize graph data
const nodes = new vis.DataSet([...]);
const edges = new vis.DataSet([...]);

// Get all nodes (returns array)
const allNodes = nodes.get();

// Update node
nodes.update({id: 'person::Jon', label: 'Jon Schull'});

// Add edge
edges.add({from: 'person::Jon', to: 'org::ERA', label: 'founded'});
```

### 4. Hidden State

```javascript
// Hide node (also hides connected edges)
nodes.update({id: nodeId, hidden: true});
const connectedEdges = edges.get().filter(e => 
  e.from === nodeId || e.to === nodeId
);
edges.update(connectedEdges.map(e => ({id: e.id, hidden: true})));
```

---

## Common Gotchas

### 1. File Protocol Limitations

```javascript
// ❌ Won't work from file://
fetch('/graph.js')  // Relative paths fail

// ✅ Works from file://
<script src="./graph.js"></script>  // Or inline the script
```

### 2. gapi Loading Timing

```javascript
// ❌ Wrong - gapi might not be loaded yet
initSheetsApi();

// ✅ Right - wait for gapi to load
window.onload = () => {
  if (window.gapi) {
    initSheetsApi();
  }
};
```

### 3. OAuth vs API Key

```javascript
// Reading (API key) - no sign-in
// Sheet must be public ("Anyone with link can view")
const data = await readSheetTab('nodes');

// Writing (OAuth) - requires sign-in
// User must click "Sign In" button first
await writeSheetTab('nodes', data);  // Will fail if not authenticated
```

### 4. Browser Compatibility

```javascript
// ❌ Might not work in older browsers
const data = await fetch(...);

// ✅ Better - check for support
if ('fetch' in window) {
  // Modern browser
} else {
  // Fallback or error message
}
```

---

## Git Workflow (Standard Operating Procedure)

**Same workflow as ERA_ClimateWeek. It worked.**

### Before Making Changes

```bash
# 1. Ensure on main and up-to-date
git checkout main
git pull origin main

# 2. Verify baseline (open in browser, check console)
open index.html
# Check: No errors, graph displays

# 3. Create feature branch
git checkout -b feat/feature-description
```

### During Development

```bash
# Make small changes, test immediately, commit frequently
git add index.html graph.js
git commit -m "feat: Add feature description"

# Push to remote periodically
git push origin feat/feature-description
```

### After Completing Work

```bash
# 1. Final browser test
open index.html
# Verify: Feature works, no console errors

# 2. Run Playwright test
cd tests
python test_load.py

# 3. Push final changes
git push origin feat/feature-description

# 4. Create PR
gh pr create --title "feat: Feature description" \
             --body "Description of changes"

# 5. Wait for review and merge
# 6. Update local main
git checkout main
git pull origin main
git branch -d feat/feature-description
```

### Every Functional Stable State is a PR

Don't accumulate changes. When feature works and tests pass → PR → merge.

---

## Testing Strategy

### Testing Workflow

**For every change:**

1. **Manual browser test** (FIRST)
   ```bash
   open index.html
   # Check console (Cmd+Option+J)
   # Test the feature
   # Verify no errors
   ```

2. **Playwright test** (SECOND)
   ```bash
   cd tests
   python test_load.py  # Or specific test
   ```

3. **Ask user to verify** (THIRD)
   ```
   "Feature tested and working. Please verify:
   - Open index.html
   - Test [specific action]
   - Confirm [expected result]"
   ```

4. **Screenshot if visual** (OPTIONAL but helpful)
   ```python
   page.screenshot(path="feature_working.png")
   ```

### Browser Compatibility

**Target browsers:**
- ✅ Chrome 118+ (primary)
- ✅ Edge 118+ (test this too)
- ⚠️ Firefox 119+ (nice to have)
- ⚠️ Safari 17+ (nice to have)

**Test in both Chrome AND Edge before claiming success.**

### Manual Checklist

**Basic functionality:**
- [ ] index.html opens without errors
- [ ] Graph displays
- [ ] Data loads from Sheets (or embedded fallback)
- [ ] Toolbar buttons work
- [ ] Quick Editor can add/remove edges
- [ ] Search filtering works
- [ ] Save button works (if signed in)

**Console check:**
- [ ] No red errors in console
- [ ] API calls succeed (check Network tab)
- [ ] No "failed to load" messages

---

## Communication Style

### With the User

- **Be concise** - No verbose explanations
- **Test before claiming success** - Show proof (screenshot, test output)
- **Ask when uncertain** - Don't guess
- **Update docs** - Keep this guide current
- **Never say "should work"** - Say "tested, works" with evidence

### Example Good Response

```
✅ Feature implemented and tested

Changes:
- Added Sign In button to toolbar
- Integrated OAuth flow
- Tested in Chrome and Edge

Evidence:
- test_load.py passes
- Console shows no errors
- [screenshot.png] shows button works

Please verify: Open index.html, click "Sign In", confirm OAuth popup appears.
```

### Example Bad Response

```
I've added the Sign In button. It should work now.
```

**Why bad?** No testing, no evidence, no specifics.

---

## File Organization

### Keep Clean

- `index.html` - Main HTML file
- `graph.js` - JavaScript (or inline if needed)
- `*.md` - Documentation
- `tests/` - Test scripts

### Don't Create

- Unnecessary helper files
- Complex directory structures  
- Multiple versions of index.html
- Build scripts (keep it simple!)

---

## When to Ask for Help

### Uncertain About

- UX decisions ("Should this button be here?")
- Breaking changes ("This will change existing behavior")
- API limits ("Will this hit rate limits?")
- Security concerns ("Is hardcoding API key safe?")

### Don't Ask About

- Implementation details (you can figure it out)
- Syntax questions (you know JavaScript)
- Testing approach (follow the workflow above)

---

## Success Criteria

### You're Doing Well If

- ✅ Changes are small and testable
- ✅ Browser tests pass before claiming success
- ✅ Documentation stays current
- ✅ User can verify what you did
- ✅ Can rollback via git if needed

### Red Flags

- ❌ "It should work" without browser testing
- ❌ Multiple features in one change
- ❌ Breaking existing functionality
- ❌ Undocumented changes
- ❌ No commit before risky change

---

## Handoff Checklist

### Before Starting Work

- [ ] Read this guide
- [ ] Read `README.md`
- [ ] Open index.html and explore
- [ ] Check git log for recent changes
- [ ] Review `VISION.md` for project goals
- [ ] Understand what feature is next

### During Work

- [ ] Follow incremental approach
- [ ] Test in browser after each change
- [ ] Update documentation
- [ ] Commit frequently
- [ ] Run Playwright tests

### Before Handing Back

- [ ] All tests passing
- [ ] Feature works in Chrome AND Edge
- [ ] Documentation updated
- [ ] Clear summary of changes
- [ ] Known issues documented

---

## The User Values

- **Working solutions** over perfect code
- **Incremental progress** over big rewrites
- **Clear communication** over technical jargon
- **Tested features** over untested claims
- **Their time** - be efficient and proactive

---

## Remember

- This is a real project with real users
- Changes affect the live graph (via Google Sheets)
- Test in browser BEFORE asking user to test
- When in doubt, ask
- Test, test, test

---

**Ready to start?** Read `VISION.md` to understand the goal, then check `NEXT_STEPS.md` for what to do next.


---

## FILE: ERA_Landscape/START_HERE_NEW_AI.md

**Path:** `ERA_Landscape/START_HERE_NEW_AI.md`

# START HERE - New AI Session

**Welcome!** You're picking up ERA_Landscape_Static development.

---

## FIRST: Read These Files (in order)

1. **HANDOFF_SUMMARY.txt** (9.7KB) - MUST READ FIRST
   - Orientation checklist
   - Current state
   - What's done, what's missing
   - Critical discipline

2. **AI_HANDOFF_GUIDE.md** (13.5KB) - MUST READ SECOND
   - Development culture
   - Testing discipline
   - Git workflow
   - Code patterns
   - Common gotchas

3. **TESTING.md** (10.6KB) - Testing workflow
   - Browser test FIRST, then Playwright, then user verification
   - Chrome + Edge compatibility required
   - Never claim success without testing

4. **NEXT_STEPS.md** (6KB) - What to do immediately
   - Step-by-step roadmap
   - Timeline: 2-3 hours to GitHub Pages
   - Clear action items

5. **VISION.md** (14.3KB) - Long-term goals
   - Collaborative network mapping
   - Personal + Global sheets
   - Privacy model (public by default, opt-in private)

---

## THEN: Assess Current State

### Check Git Status
```bash
git status
git log --oneline -5
git branch --show-current
```

### Test Current State
```bash
# Open in browser
open index.html

# Check console (Cmd+Option+J)
# - Any errors?
# - Does graph display?

# Run test
cd tests
python test_load.py
```

### Report to User
Present status WITHOUT being asked:
```
## Current Status
- **Branch**: [main / feature branch]
- **Browser test**: [Works / Errors: X]
- **Playwright test**: [Pass / Fail]  
- **Next step**: [What needs to be done]
- **Ready**: [Yes / Need clarification on X]
```

---

## Current State (as of Oct 15, 2025)

**✅ PRODUCTION DEPLOYED & FULLY FUNCTIONAL**

**Live Site:** https://jonschull.github.io/ERA_Admin/ERA_Landscape/
**Repository:** https://github.com/jonschull/ERA_Admin (ERA_Landscape/ component)
**Historical:** https://github.com/jonschull/ERA_Landscape_Static (archived)

**All Core Features Complete:**
- ✅ Google Sheets API integration (read/write)
- ✅ OAuth sign-in for editing
- ✅ Auto-load data from Sheets on page init
- ✅ Auto-fit graph after data loads
- ✅ Node scaling by connection count
- ✅ Quick Editor with Enter key & yellow border highlights
- ✅ Hover tooltips on all buttons
- ✅ GitHub Pages auto-deployment from main branch
- ✅ Branch-based workflow documented

**Next Work (When Ready):**
See `SHEET_ANALYSIS_V2.md` for:
- 📋 User tracking (created_by, updated_by, fields_changed columns)
- 📋 Personal vs Global sheets architecture
- 📋 Admin activity log & selective reversion

**Estimated:** 12-18 hours for user tracking + personal sheets

---

## CRITICAL: Development Discipline

### RED FLAGS (Stop if you see these)
- ❌ Making 3+ fixes without testing
- ❌ Saying "should work" instead of "tested, works"
- ❌ Asking user to test before YOU test
- ❌ Not checking console for errors

### CORRECT WORKFLOW
1. **Make ONE small change**
2. **Test in browser** (open index.html, check console)
3. **Run Playwright test** (cd tests && python test_load.py)
4. **Show evidence** to user (test output, screenshot)
5. **Get confirmation** before next change

### Testing Order (ALWAYS)
1. Browser test (FIRST) - open index.html, check console
2. Playwright test (SECOND) - run test_load.py
3. User verification (THIRD) - ask user to confirm
4. Chrome + Edge (BEFORE PR) - test in both browsers

---

## Git Workflow (MANDATORY - Branch-Based)

⚠️ **CRITICAL**: See `DEVELOPMENT.md` lines 3-19 for workflow requirement.

**NEVER push directly to main!** Always use feature/fix branches:

```bash
# Create branch
git checkout -b feat/feature-name  # or fix/bug-description

# Make changes, test, commit
git add .
git commit -m "feat: Description"

# Push branch
git push origin feat/feature-name

# Create PR
gh pr create --title "Feature name"

# After merge
git checkout main && git pull
```

---

## Communication Style

**With User:**
- Be concise (not verbose)
- Test BEFORE reporting
- Show evidence (test output, screenshot)
- Never say "should work" - say "tested, works"

**Example GOOD response:**
```
✅ Feature implemented and tested

Changes:
- Inlined graph.js into index.html
- Added Google Sheets API scripts
- Added Sign In button

Evidence:
- Browser test: No console errors
- test_load.py: PASSED
- [screenshot.png attached]

Please verify:
1. Open index.html
2. Check console for "✅ Google Sheets API client initialized"
3. Confirm graph displays
```

**Example BAD response:**
```
I've added the API code. It should work now.
```

---

## Success Criteria

**You're doing well if:**
- ✅ Browser test shows no errors
- ✅ test_load.py passes
- ✅ User confirms feature works
- ✅ Documentation updated

**Red flags:**
- ❌ Multiple attempts without testing
- ❌ User testing before you test
- ❌ Console errors ignored

---

## Key Files to Know

**Core Code:**
- `index.html` (21KB) - Main HTML file with Sheets API integration
- `graph.js` (46KB) - JavaScript logic with all UI features

**Documentation:**
- `HANDOFF_SUMMARY.txt` - Current project state (READ FIRST)
- `DEVELOPMENT.md` - Developer guide with workflow rules
- `NEXT_STEPS.md` - Completed work + future roadmap
- `SHEET_ANALYSIS_V2.md` - Next feature design (user tracking + personal sheets)
- `TESTING.md` - Testing workflow

**Tests:**
- `tests/*.py` - 12 Playwright tests

**Obsolete:**
- `obsolete/` - Old docs and reference code (moved for cleanup)

---

## Parent Project Reference

**ERA_ClimateWeek:** https://github.com/jonschull/ERA_ClimateWeek
- Python data processing pipeline
- Flask server for development
- Generates HTML templates
- Writes to Google Sheets

**This project (ERA_Landscape_Static):**
- Pure HTML/JavaScript (no Python)
- Reads from same Google Sheet
- Deployable to GitHub Pages
- No server needed

**Relationship:** ClimateWeek processes data → writes to Sheet → Static viewer displays

---

## Ready to Start?

1. **Read** HANDOFF_SUMMARY.txt (right now!)
2. **Assess** current state (git, browser test, Playwright)
3. **Report** status to user (proactively, don't wait to be asked)
4. **Ask** what to work on (usually: "Ready to start on NEXT_STEPS.md Step 1?")

**DO NOT:**
- Jump into coding without reading docs
- Make changes without testing
- Claim success without evidence
- Ask user to test before you test

---

**Welcome to the team! Follow the discipline, test thoroughly, and we'll get to GitHub Pages quickly.**


---

## FILE: ERA_Landscape/VISION.md

**Path:** `ERA_Landscape/VISION.md`

# Long-Term Vision: Collaborative Network Mapping

**Date**: October 13, 2025  
**Project**: ERA_Landscape_Static

---

## The Goal

Create a **movement-wide utility** for collaborative network mapping where:

1. **Anyone can view** the shared network (public, no sign-in)
2. **Contributors can edit** the shared database (sign in with Google)
3. **Individuals customize** their own views (personal hide/show preferences)
4. **Users discover** connections added by others
5. **Personal sheets complement** the global sheet (individual data + collective data)

**The Point:** Help people collectively map the climate/restoration movement **for their own purposes** while developing a database that helps everyone.

---

## Use Cases

### Use Case 1: Discovery

- User A maps their network, adds organizations and people to **global sheet**
- User B opens the viewer, sees the shared network
- User B clicks a node, sees "hidden" connections added by User A
- User B unhides those connections → discovers User A's contributions
- Both users benefit from collective intelligence

### Use Case 2: Personal Data

- User C wants to maintain their own subset of the network
- User C creates a **personal sheet** for their own data curation
- User C's viewer can show: **global only**, **personal only**, or **merged view**
- Personal data is **public by default** (automatically merges into global)
- If User C wants something private, they mark it with **Private = true** attribute
- User C can choose to work with just their personal view (exclude global noise)

### Use Case 3: Collective Intelligence

- 20+ users contribute to global sheet
- Each adds their piece of the network
- Global sheet grows organically (500 → 1000 → 5000 nodes)
- Everyone benefits from the collective mapping
- No single person has to map the entire movement

---

## Architecture Evolution

### Phase 1: Static Viewer ✅ COMPLETED (October 2025)

**Goal:** Get the viewer working without a server

**Features:**
- ✅ Pure HTML/JavaScript (no backend)
- ✅ Loads from single global Google Sheet
- ✅ Interactive graph visualization
- ✅ Deployed to GitHub Pages

**Status:** Complete and deployed

**Completed:** October 15, 2025

**Live**: https://jonschull.github.io/ERA_Admin/ERA_Landscape/

---

### Phase 2: OAuth Editing ✅ COMPLETED (October 2025)

**Goal:** Enable users to contribute to shared database

**Features:**
- ✅ "Sign In" button (Google OAuth)
- ✅ Add/edit nodes and edges
- ✅ Save changes back to global Sheet
- ✅ OAuth app published to production (anyone can sign in)

**Technical:**
- ✅ Google Identity Services (OAuth 2.0)
- ✅ Sheets API write permission
- ✅ OAuth Client: ERA Graph Browser Client
- ✅ Status: In production (public access enabled)

**Completed:** October 19, 2025

**Note:** Attribution tracking (created_by, updated_by) planned for Phase 3

---

### Phase 3: Personal Sheets (Q1 2026)

**Goal:** Enable personal data alongside global data

**Features:**
- Each user has their own personal Google Sheet
- Personal data is **public by default** (auto-merges into global view)
- Users can mark specific entries as "private" (opt-out from merge)
- View options: Global only, Personal only, or Merged (toggle)

**Technical:**
```javascript
// Load both sheets
const globalData = await loadSheet(GLOBAL_SHEET_ID);
const personalData = await loadSheet(USER_SHEET_ID);

// Filter personal data: exclude entries marked private
const publicPersonalNodes = personalData.nodes.filter(n => !n.private);

// Merge for display (personal public data goes into everyone's view)
const mergedNodes = [...globalData.nodes, ...publicPersonalNodes];
const mergedEdges = [...globalData.edges, ...personalData.edges.filter(e => !e.private)];

// View options (user can toggle)
// - "Global only": renderGraph(globalData.nodes, globalData.edges)
// - "Personal only": renderGraph(personalData.nodes, personalData.edges)
// - "Merged" (default): renderGraph(mergedNodes, mergedEdges)
```

**User Experience:**
1. User opens viewer (default: global data)
2. Signs in → also loads their personal sheet
3. View options:
   - "Show: Global + Personal" (merged - default)
   - "Show: Personal only" (just my data)
   - "Show: Global only" (everyone else's data)
4. Adding data to personal sheet:
   - By default: Public (auto-merges into global view for others)
   - Can mark as "Private" (only I see it, never merges)

**Timeline:** 1-2 months

---

### Phase 4: Discovery & Coordination (Q2 2026)

**Goal:** Help users discover each other's contributions

**Features:**
- "Show all connections" in node modal (including hidden)
- Visual indicator: "3 users added connections to this node"
- Filter: "Show only connections added by User A"
- Notifications: "User B added a connection you might care about"

**Technical:**
- Track data provenance (who added what)
- Filter by contributor
- Suggestion engine (optional)

**Timeline:** 2-3 months

---

### Phase 5: Real-time Collaboration (Future - Optional)

**Goal:** Live updates while multiple users edit

**Features:**
- See other users currently viewing
- Live updates as data changes
- Conflict resolution
- Collaborative editing sessions

**Technical:**
- WebSocket or polling for updates
- Operational transforms for conflict resolution
- Presence indicators

**Timeline:** TBD (only if needed)

---

## Technical Strategy

### Storage: Google Sheets (Not Database)

**Why Sheets?**
- ✅ Built-in multi-user (Google accounts)
- ✅ Familiar UX (everyone knows spreadsheets)
- ✅ No hosting costs
- ✅ Real-time collaboration built-in
- ✅ Edit in Sheet OR graph UI
- ✅ Version history free
- ✅ Export/import trivial

**Sheets Structure:**

**Global Sheet** (public, shared):
```
Tab: nodes
  id | label | type | url | notes | origin | created_by | created_at | updated_at

Tab: edges  
  source | target | relationship | role | url | notes | created_by | created_at | updated_at
```

**Personal Sheet** (per user, public by default):
```
Same schema as global
Plus: private column (boolean: false = public/merged, true = private/excluded)
```

**Rate Limits:**
- Google Sheets API: 100 requests/100 seconds/user
- Generous for our use case
- Batch reads/writes to stay under limit

---

### Authentication: Google OAuth

**Why Google?**
- ✅ Users already have Google accounts (for Sheets access)
- ✅ No password management
- ✅ Secure OAuth 2.0
- ✅ Works in browser (client-side)

**Flow:**
1. User clicks "Sign In"
2. OAuth popup → user authorizes
3. Browser gets access token
4. Can now read/write user's own Sheets
5. Token stored in localStorage (session persistence)

---

### Deployment: GitHub Pages

**Why GitHub Pages?**
- ✅ Free hosting for static sites
- ✅ HTTPS by default
- ✅ Simple deployment (git push)
- ✅ Custom domain support
- ✅ No server maintenance

**URL:** `https://jonschull.github.io/ERA_Landscape_Static/`

---

## Data Privacy & Permissions

### Public Data (Global Sheet)

**Access:**
- View: Anyone (no sign-in needed)
- Edit: Contributors only (sign in required)
- Delete: Administrators only

**What's public:**
- Organization names
- Project names
- Relationships (who partners with whom)
- URLs (public websites)

**What's NOT public:**
- Personal contact info (unless explicitly shared)
- Private notes
- Draft/unconfirmed connections

### Personal Data (Personal Sheets)

**Access:**
- View: Owner can see their own + merged global view
- Edit: Owner only (can edit their personal sheet)
- Merge: By default, personal data merges into global (public)

**What's in personal sheets:**
- User's own data curation
- Public by default (merged into everyone's global view)
- Can mark individual entries as "private" to exclude from merge

**What's private (opt-in):**
- Entries marked with `private = true` attribute
- Owner sees them, but they don't merge into global
- Useful for: draft connections, sensitive relationships, personal notes

### User Control

**Users can:**
- Maintain their own personal sheet (their data, their curation)
- View: Global only, Personal only, or Merged (toggle)
- Mark specific entries as "private" (opt-out from merge)
- Delete their own contributions
- Export their data anytime

---

## Incentive Model

### Why Would Users Contribute?

**1. Personal Utility**
- Users need this tool for their own network mapping
- Contributing makes THEIR data more useful
- Network effects: more data = more valuable tool

**2. Discovery**
- Users discover connections they didn't know
- Serendipity: "Oh, I didn't know X works with Y!"
- Helps users find collaborators

**3. Movement Building**
- Collective intelligence benefits everyone
- Visualizing movement = understanding movement
- Coordination improves with better mapping

**4. Low Friction**
- Easy to add data (familiar spreadsheet OR graph UI)
- OAuth = one-click sign in
- No app to install, just open URL

---

## Compatibility with Current Architecture

### ✅ What Already Fits

**Modal-based discovery:**
- Opening a node shows ALL connections (not just visible)
- Perfect for discovering others' contributions
- Already implemented in parent project (ERA_ClimateWeek)

**Operation queue + batch save:**
- Clean separation of changes from persistence
- Easy to add attribution (who made this change)
- Already designed for transactional updates

**Serverless architecture:**
- No backend = easy to scale
- Pure client-side = low cost
- GitHub Pages = free hosting

### ⚠️ What Needs Work

**1. Personal Sheet Integration**
- Need to load multiple sheets (global + personal)
- Merge data client-side
- Track provenance (which sheet did this come from)

**2. Attribution Tracking**
- Add `created_by` and `updated_by` columns
- Capture user ID from OAuth
- Display in UI ("Added by User A")

**3. Merge & Privacy Controls**
- Personal data merges automatically (public by default)
- UI for marking entries as "private" (opt-out from merge)
- Filter controls: View Global, Personal, or Merged
- Handle duplicate detection across sheets

---

## Success Metrics

### Phase 1 Success (Static Viewer) ✅ ACHIEVED
- ✅ Deploys to GitHub Pages
- ✅ Loads data from Google Sheets
- ✅ No console errors
- ✅ Graph displays and works
- ✅ 5+ users can access and view

### Phase 2 Success (OAuth Editing) ✅ ACHIEVED
- ✅ Users can sign in (OAuth in production)
- ✅ Users can add/edit nodes and edges
- ✅ Changes save to global Sheet
- ⏳ 10+ users contributing data (pending user adoption)

### Phase 3 Success (Personal Sheets)
- ✅ Users have personal sheets
- ✅ Combined view works (global + personal)
- ✅ Promotion workflow tested
- ✅ 20+ users with personal sheets

### Phase 4+ Success (Collaborative)
- ✅ Users discovering each other's contributions
- ✅ Network growing organically (>1000 nodes)
- ✅ Active community of contributors
- ✅ Utility proven valuable

---

## Decision Gates

### After Phase 1 (Static Viewer)

**Questions:**
- Does it work on GitHub Pages?
- Are users interested?
- Should we proceed to Phase 2?

**If NO:** Stop here, keep as static viewer only  
**If YES:** Proceed to Phase 2 (OAuth)

### After Phase 2 (OAuth Editing)

**Questions:**
- Are users actively contributing?
- Do we have 10+ contributors?
- Is data quality good?

**If NO:** Work on incentives, UX improvements  
**If YES:** Proceed to Phase 3 (Personal Sheets)

### After Phase 3 (Personal Sheets)

**Questions:**
- Are personal sheets being used?
- Are users promoting personal → global?
- Is the utility valuable enough?

**If NO:** Reassess approach  
**If YES:** Consider Phase 4 (Discovery)

---

## Technical Considerations

### Scalability

**Google Sheets limits:**
- 10 million cells per sheet (we're at ~10k currently)
- 100 requests/100 seconds/user (batch to optimize)
- 500 requests/100 seconds/project (we're well under)

**When to migrate to database:**
- >10,000 nodes (Sheet gets slow)
- >100 concurrent users (rate limits)
- Need complex queries (Sheets is simple key-value)

**Migration path:**
- Export Sheets → CSV
- Load CSV → PostgreSQL/SQLite
- Keep Sheets for backup/export
- Update viewer to read from DB API instead of Sheets

### Browser Compatibility

**Target:**
- Chrome 118+ (primary)
- Edge 118+ (primary)
- Firefox 119+ (nice to have)
- Safari 17+ (nice to have)

**Requirements:**
- ES6 support (async/await, arrow functions)
- Fetch API
- localStorage
- Google APIs (OAuth, Sheets)

### Performance

**Current:** 352 nodes, 220 edges (renders fine)

**Future:**
- 1,000 nodes: Should work (test physics settings)
- 5,000 nodes: May need optimization (disable physics)
- 10,000+ nodes: Need database, server-side rendering

---

## Open Questions

### User Research Needed

1. **Do users want personal sheets?**
   - Or is global sheet enough?
   - Survey potential users

2. **What data is sensitive?**
   - What should stay private by default?
   - What's safe to share?

3. **Discovery vs privacy?**
   - How much visibility do users want?
   - Opt-in vs opt-out for attribution

### Technical Decisions

1. **One Sheet or many?**
   - Option A: One global sheet, personal sheets separate
   - Option B: One sheet with user_id column (filtering)
   - Leaning toward Option A (simpler, better privacy)

2. **Conflict resolution?**
   - What if User A and User B edit same node?
   - Last write wins? Merge? Flag conflict?
   - Start simple (last write wins), add complexity if needed

3. **Data validation?**
   - Who can edit what?
   - Can users delete others' contributions?
   - Role system (viewer/contributor/admin)?

---

## Next Steps (Immediate)

**Right now (October 2025):**
1. Get Phase 1 working (static viewer)
2. Deploy to GitHub Pages
3. Share with 5-10 users for feedback

**Then (November 2025):**
1. Implement OAuth sign-in
2. Enable editing (Phase 2)
3. Get 10+ contributors

**Then (Q1 2026):**
1. Assess if personal sheets are needed
2. If yes, implement Phase 3
3. If no, focus on other features

---

## Bottom Line

**The vision is achievable:**
- Build incrementally (phase by phase)
- Each phase delivers value
- Can stop at any point (each phase is useful standalone)
- Google Sheets = low cost, low complexity
- Pure client-side = easy to deploy and maintain

**The goal is clear:**
- Help people map the movement collectively
- Individual utility + collective intelligence
- Make it easy to contribute, easy to discover

**Next action:**
- Get Phase 1 working (static viewer on GitHub Pages)
- Prove the concept
- Then decide if Phase 2+ is worth building

---

**Let's start simple and iterate based on real user needs.**


---

## FILE: ERA_Landscape/NEXT_STEPS.md

**Path:** `ERA_Landscape/NEXT_STEPS.md`

# Next Steps for ERA_Landscape_Static

## ✅ PROJECT COMPLETE AND DEPLOYED!

**Live Site**: https://jonschull.github.io/ERA_Landscape_Static/

---

## What We Completed

### Phase 1: Google Sheets API Integration ✅
- Added Google API libraries (gapi, OAuth2)
- Implemented read/write functions
- Wired Refresh/Save buttons
- Added Sign In button for OAuth
- Created integration test (8/8 passing)
- Documented HTTP/HTTPS requirement

### Phase 2: Color Fixes & DRY Refactoring ✅
- Fixed colors to match legend (person=blue, org=teal, project=purple)
- Added `parseTypeFromId()` to extract type from ID prefix
- Added `getNodeVisuals()` for DRY color/shape logic
- Fixed legend triangle color (#ff9800 → #ce93d8)

### Phase 3: Remove Embedded Data & Auto-Load ✅
- Removed ~110KB of embedded JSON data
- File size: 131KB → 20KB (85% reduction)
- Implemented auto-load on page init
- Always shows fresh data from Google Sheet
- Zero embedded data - single source of truth

### Phase 4: GitHub Pages Deployment ✅
- Enabled GitHub Pages (main branch, root folder)
- Configured auto-deploy on push
- Live at: https://jonschull.github.io/ERA_Landscape_Static/
- Verified: 353 nodes loading, no errors
- Build time: ~1-2 minutes

### Phase 5: Documentation Updates ✅
- Updated README with deployment procedures
- Updated DEVELOPMENT with testing procedures
- Added GitHub Pages update workflow
- Documented HTTP/HTTPS requirement throughout

### Phase 6: UI Improvements (Oct 15, 2025) ✅
- Auto-fit graph after data loads
- Node scaling by connection count (12-60px)
- Enter key triggers Add/Update in Quick Editor
- Yellow border highlights for matching nodes
- Removed redundant buttons (Reset, Highlight Seed/Discovered)
- Added hover tooltips to all buttons
- Re-Load button with guardrail for unsaved changes

---

## Current Status

**Repository**: https://github.com/jonschull/ERA_Admin (ERA_Landscape/ component)  
**Live Site**: https://jonschull.github.io/ERA_Admin/ERA_Landscape/  
**Historical**: https://github.com/jonschull/ERA_Landscape_Static (archived)  
**Status**: ✅ Production Ready

**Key Metrics:**
- File size: 20KB (was 131KB)
- Load time: ~2-3 seconds (including API init + data fetch)
- Node count: ~350+ (live from Sheet)
- Tests passing: 8/8
- Zero embedded data

**What Works:**
- ✅ Auto-loads fresh data from Google Sheets on page load
- ✅ Auto-fit graph after data loads (2 second physics delay)
- ✅ Interactive graph (drag, zoom, pan)
- ✅ Node scaling by connection count (1-17 connections)
- ✅ Color-coded by type (matches legend)
- ✅ Search/filter functionality
- ✅ Quick Editor with Enter key support
- ✅ Yellow border highlights for matching nodes
- ✅ Re-Load button with unsaved changes guardrail
- ✅ Sign In (OAuth) for editing
- ✅ Save changes back to Sheet
- ✅ GitHub Pages auto-deployment
- ✅ Hover tooltips on all buttons

---

## How to Update the Live Site

```bash
# 1. Create feature branch
git checkout -b feat/my-feature

# 2. Make changes locally
code index.html  # or graph.js

# 3. Test with HTTP server (REQUIRED)
python3 -m http.server 8000
open http://localhost:8000

# 4. Verify in console:
# - "✅ Google Sheets API client initialized"
# - "✅ Loaded XXX nodes, YYY edges from Sheets"
# - "🎉 Initial data load complete"

# 5. Commit and push branch
git add .
git commit -m "feat: Description of changes"
git push origin feat/my-feature

# 6. Create PR and merge to main
gh pr create  # or use GitHub UI

# 7. Wait for deployment (~1-2 minutes)
gh api repos/jonschull/ERA_Landscape_Static/pages/builds/latest | jq -r '.status'

# 8. Verify live site
open https://jonschull.github.io/ERA_Landscape_Static/
```

---

## Future Enhancements (Optional)

These are nice-to-haves, not critical:

### UI/UX Improvements
- [ ] Add dark mode toggle
- [ ] Improve loading screen with progress indicator
- [✅] Add keyboard shortcuts (Enter key in Quick Editor)
- [ ] Add undo/redo functionality
- [ ] Export graph as PNG/SVG
- [ ] Export data as CSV

### Features
- [ ] Curation modal for bulk organization editing
- [ ] Batch operations (hide/show multiple nodes)
- [ ] Advanced search (by type, connections, etc.)
- [ ] Node clustering/grouping
- [ ] Timeline view (if date data available)
- [ ] Analytics dashboard (connection stats, etc.)

### Technical Improvements
- [ ] Add service worker for offline support (cache Sheet data)
- [ ] PWA manifest (install as app)
- [ ] TypeScript conversion for type safety
- [ ] Separate CSS file (currently inline)
- [ ] Add tests for graph.js functions
- [ ] Performance optimization for >1000 nodes

**Philosophy**: Keep it simple unless there's a real need. Current implementation is production-ready.

---

## Project Architecture

**Simple Path (Current):**
```
Browser → Google Sheets API → Fetch Data → Render Graph
   ↓                                           ↓
Sign In → OAuth → Edit Graph → Save → Write to Sheet
```

**Benefits:**
- No server needed
- No Python needed  
- No build step
- Deploy anywhere (GitHub Pages, Netlify, S3, etc.)
- Can email as HTML attachment (works with HTTP server)

---

## Relationship to ERA_ClimateWeek

### ERA_ClimateWeek (Python)
**Repository**: https://github.com/jonschull/ERA_ClimateWeek  
**Purpose**: Data processing pipeline

**Use for:**
- Importing from CSV
- Batch data transformations
- Complex data processing
- Development/testing with Flask

**Location**: `/Users/admin/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ClimateWeek`

### ERA_Landscape_Static (This Project)
**Repository**: https://github.com/jonschull/ERA_Admin (ERA_Landscape/ component)  
**Live Site**: https://jonschull.github.io/ERA_Admin/ERA_Landscape/  
**Purpose**: Production viewer with direct Sheet integration

**Use for:**
- Public deployment
- Viewing the graph
- Simple editing via browser
- No server/Python required

**Workflow:**
```
ERA_ClimateWeek (Python)
  ↓ Process CSV data
  ↓ Transform and validate
  ↓ Write to Google Sheet
  ↓
ERA_Landscape_Static (HTML/JS)
  ↓ Read from Google Sheet
  ↓ Display in browser
  ↓ Users can edit
  ↓ Save back to Sheet
```

---

## Success Criteria - ALL COMPLETE! ✅

✅ **Phase 1**: File loads locally  
✅ **Phase 2**: Graph displays  
✅ **Phase 3**: Google Sheets API integration  
✅ **Phase 4**: Deployed to GitHub Pages  
✅ **Phase 5**: Removed embedded data, auto-load from Sheets  
✅ **Phase 6**: Production-ready and documented

**Status**: Production deployment complete and verified!  

---

## Timeline (Actual)

**Oct 15, 2025:**
- Phase 1-2: Project setup and initial deployment
- Phase 3: Google Sheets API integration (PR #1)
- Phase 4: Color fixes and DRY refactoring
- Phase 5: Removed embedded data, auto-load implementation
- Phase 6: GitHub Pages deployment and documentation

**Total Time**: ~1 day from start to production deployment

---

## Useful Commands Reference

```bash
# Local testing
python3 -m http.server 8000
open http://localhost:8000

# Check deployment status
gh api repos/jonschull/ERA_Landscape_Static/pages/builds/latest | jq -r '.status'

# Run tests
python3.9 tests/test_sheets_integration.py

# Quick commit and push to branch
git add . && git commit -m "feat: message" && git push origin <branch-name>

# View live site
open https://jonschull.github.io/ERA_Landscape_Static/
```

**Documentation Files:**
- `README.md` - Project overview and quick start
- `DEVELOPMENT.md` - Developer guide with workflows
- `NEXT_STEPS.md` - This file (project status)
- `AI_HANDOFF_GUIDE.md` - AI assistant methodology
- `HANDOFF_SUMMARY.txt` - Quick reference for state


---

## FILE: ERA_Landscape/SHEET_ANALYSIS_V2.md

**Path:** `ERA_Landscape/SHEET_ANALYSIS_V2.md`

# Google Sheet Analysis & User Tracking Design (v2)

**Date**: October 15, 2025  
**Incorporates**: User feedback from Oct 15 conversation

---

## Key Decisions

✅ **Default behavior**: Nodes go to **BOTH** Global and Personal sheets  
✅ **Checkboxes control visibility**: Both checked by default  
✅ **No "signed in as" display**: Focus on audit columns only  
✅ **Track field changes**: New column `fields_changed`  
✅ **Personal sheet auto-creation**: Create + present URL on first save  
❌ **Removed**: `is_personal` flag, `synced_to_global` (unnecessary)

---

## 1. Column Usage Reality Check

### What's Actually Displayed vs Stored

**Nodes Tab Analysis**:

| Column | UI Display? | Actual Use |
|--------|-------------|------------|
| `id`, `label` | Yes (node) | Essential |
| `type` | No | IGNORED (parsed from ID) |
| `url`, `notes`, `member`, `origin` | **NO** | Stored but NOT shown anywhere |
| `hidden`, timestamps | No | Internal use |

**Truth**: `url`, `notes`, `member`, `origin` are **preserved metadata** but **never displayed to users**. They could be shown in a details panel (doesn't exist yet). Direct Sheet editors may use them.

---

## 2. New Required Columns

### Add to BOTH Global and Personal sheets

**Audit Columns**:
```
created_by      | string  | User email who created
created_at      | string  | ISO timestamp
updated_by      | string  | User email who last modified  
updated_at      | string  | ISO timestamp
fields_changed  | JSON    | Array of field names changed
```

**Why `fields_changed`?**
- Precise audit: "Jon changed label and notes"
- Selective revert: "Undo notes change, keep label"
- Example: `["label", "notes"]` or `["*"]` for new rows

**Removed Columns** (from v1 proposal):
- ❌ `is_personal` - Nonsensical (can't track many users in Global)
- ❌ `synced_to_global` - Unnecessary (everything goes to both)
- ❌ `sheet_origin` - Redundant (we know from which sheet we read)

---

## 3. Personal Sheet Creation Flow

### First Save Experience

```
User signs in → User adds node → Check localStorage for personalSheetId

If NO personal sheet yet:
  1. Create new Sheet via API
  2. Name: "ERA Network - Personal (user@example.com)"
  3. Add tabs: 'nodes', 'edges' with headers
  4. Set permissions: Only this user
  5. Add initial row: User's own person node
  6. Store Sheet ID in localStorage
  7. Show dialog:
  
     ┌────────────────────────────────────┐
     │ Your Personal Landscape Created!   │
     ├────────────────────────────────────┤
     │ We created your private sheet      │
     │                                    │
     │ 📊 [Open Personal Sheet]           │
     │                                    │
     │ Your data is saved to BOTH:        │
     │ • Global (shared)                  │
     │ • Personal (private)               │
     │                                    │
     │ Use checkboxes to toggle views     │
     │                                    │
     │ [Got it!]                          │
     └────────────────────────────────────┘

Then save node to both sheets
```

### Initial Personal Sheet Content

**First row in 'nodes' tab**:
```
id: person::user@example.com
label: User Name
type: person
...other fields...
created_by: user@example.com
created_at: 2025-10-15T14:23:45Z
updated_by: user@example.com
updated_at: 2025-10-15T14:23:45Z
fields_changed: ["*"]
```

**Why?** User sees their sheet isn't empty, has a "self" node to connect to.

---

## 4. Data Flow Architecture

### Loading (Both Sheets Merged)

```javascript
async function loadAllData() {
  const useGlobal = $('#useGlobalData').checked;  // default: true
  const usePersonal = $('#usePersonalData').checked;  // default: true
  
  let allNodes = [], allEdges = [];
  
  if (useGlobal) {
    const global = await loadDataFromSheets(GLOBAL_SHEET_ID);
    allNodes.push(...global.nodes.map(n => ({...n, _source: 'global'})));
    allEdges.push(...global.edges.map(e => ({...e, _source: 'global'})));
  }
  
  if (usePersonal && localStorage.personalSheetId) {
    const personal = await loadDataFromSheets(localStorage.personalSheetId);
    allNodes.push(...personal.nodes.map(n => ({...n, _source: 'personal'})));
    allEdges.push(...personal.edges.map(e => ({...e, _source: 'personal'})));
  }
  
  // Merge: Personal wins conflicts
  return {
    nodes: mergeWithPersonalWins(allNodes, 'id'),
    edges: mergeWithPersonalWins(allEdges, ['source', 'target'])
  };
}

function mergeWithPersonalWins(items, keyField) {
  const map = new Map();
  
  // Load Global first
  items.filter(i => i._source === 'global').forEach(item => {
    const key = Array.isArray(keyField) 
      ? keyField.map(f => item[f]).join('::')
      : item[keyField];
    map.set(key, item);
  });
  
  // Personal overwrites
  items.filter(i => i._source === 'personal').forEach(item => {
    const key = Array.isArray(keyField)
      ? keyField.map(f => item[f]).join('::')
      : item[keyField];
    map.set(key, item);
  });
  
  return Array.from(map.values());
}
```

### Saving (To Both Sheets)

```javascript
async function doAdd() {
  const node = {
    id, label, type, url, notes, member, origin: 'quick-editor',
    hidden: false,
    created_by: window.currentUser.email,
    created_at: new Date().toISOString(),
    updated_by: window.currentUser.email,
    updated_at: new Date().toISOString(),
    fields_changed: ["*"]  // All fields (new node)
  };
  
  const useGlobal = $('#useGlobalData').checked;
  const usePersonal = $('#usePersonalData').checked;
  
  // Save to Global
  if (useGlobal) {
    await saveNodeToSheet(GLOBAL_SHEET_ID, node);
  }
  
  // Save to Personal
  if (usePersonal) {
    let personalId = localStorage.personalSheetId;
    if (!personalId) {
      personalId = await createPersonalSheet(window.currentUser.email);
      localStorage.personalSheetId = personalId;
      showPersonalSheetDialog(personalId);
    }
    await saveNodeToSheet(personalId, node);
  }
  
  nodes.add(node);
}
```

### Updating (Track Changes)

```javascript
async function updateNode(nodeId, changes) {
  const existing = nodes.get(nodeId);
  
  // Track which fields changed
  const changedFields = Object.keys(changes).filter(
    key => changes[key] !== existing[key]
  );
  
  const updated = {
    ...existing,
    ...changes,
    updated_by: window.currentUser.email,
    updated_at: new Date().toISOString(),
    fields_changed: changedFields  // e.g., ["label", "notes"]
  };
  
  // Save to appropriate sheets
  // (logic based on _source and checkbox states)
  
  nodes.update(updated);
}
```

---

## 5. Conflict Resolution: Personal Wins

### The Rule
When same node ID exists in both Global and Personal → **Personal overwrites Global**

### Example

**Global**: 
```
id: person::Jane Doe
notes: Works at EcoOrg
```

**User's Personal**:
```
id: person::Jane Doe
notes: My friend, call about funding
```

**User sees**: "My friend, call about funding" (their version)  
**Others see**: "Works at EcoOrg" (Global version)

### Edge Cases

**Q: User deletes from Personal?**  
A: Only deleted in Personal. Global remains. If both checkboxes on, Global version shows.

**Q: User hides a Global node?**  
A: Set `hidden: true` in Personal sheet. Only affects that user's view.

**Q: Both users edit same Global node simultaneously?**  
A: Last write wins (Google Sheets behavior). No conflict detection needed.

---

## 6. UI Components

### Checkboxes

```html
<div id="dataSourceControls">
  <label>
    <input type="checkbox" id="useGlobalData" checked onchange="reloadData()"> 
    Show Global Landscape
  </label>
  
  <label>
    <input type="checkbox" id="usePersonalData" checked onchange="reloadData()"> 
    Show My Personal Landscape
  </label>
  
  <a id="personalSheetLink" href="..." target="_blank" style="display:none;">
    📊 View Personal Sheet
  </a>
</div>
```

### Visual Distinction

**Personal nodes** get:
- Gold border (`#FFD700`, width: 3px)
- Tooltip: "(From your Personal Landscape)"

**Code**:
```javascript
if (node._source === 'personal') {
  node.borderWidth = 3;
  node.color.border = '#FFD700';
  node.title = node.label + '\n(From your Personal Landscape)';
}
```

---

## 7. Implementation Plan

### Phase 1: User Tracking (4-6 hours)

**Tasks**:
1. Capture user email/name on OAuth sign-in
2. Add columns: `created_by`, `updated_by`, `fields_changed`
3. Populate on save/update
4. Test with multiple users

**No UI changes** (just backend columns)

### Phase 2: Personal Sheets (8-12 hours)

**Tasks**:
1. Add checkbox UI
2. Implement `createPersonalSheet()` function
3. Implement merge logic (Personal wins)
4. Add visual distinction (gold borders)
5. Create "Personal Sheet Created" dialog
6. Test toggle behavior

### Phase 3: Admin Features (Later)

**Tasks**:
- Activity log filtered by user
- Selective revert functionality
- Admin panel (if admin email matches list)

---

## 8. Open Questions

### Q1: fields_changed format

**Option A**: Simple array
```json
["label", "notes"]
```

**Option B**: With old/new values
```json
[
  {"field": "label", "old": "Jane", "new": "Jane Doe"},
  {"field": "notes", "old": "", "new": "My friend"}
]
```

**Recommendation**: Start with Option A (simpler). Add Option B if needed.

### Q2: Handle "both checkboxes off"

**Options**:
- A. Show empty graph (warn user)
- B. Force at least one checked
- C. Default to Global

**Recommendation**: Option B - re-check Global with warning toast.

### Q3: Admin permissions

**Store admin list where?**
- A. Hardcoded in JS
- B. In Global Sheet 'admins' tab
- C. Both (hardcoded fallback)

**Recommendation**: Option B (easy to update).

---

## 9. Summary

**Core Changes**:
1. ✅ Both sheets by default
2. ✅ New audit columns (created_by, updated_by, fields_changed)
3. ✅ Personal sheet auto-created on first save
4. ✅ Personal wins conflicts
5. ✅ Visual distinction (gold borders)
6. ❌ Removed confusing concepts

**Estimated Time**: 12-18 hours total (Phases 1+2)

**Next Step**: Your approval to proceed with Phase 1?


