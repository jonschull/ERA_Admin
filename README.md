# ERA Admin - System Overview

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

1. **Current state** → [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md)
   - What's working, what's in progress, recent completions
   - Start here to resume where you left off

2. **For AI assistants** → [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md)
   - Your role and conventions
   - Captain-advisor collaboration model
   - Read this BEFORE working on the project

3. **Strategic direction** → ERA_ECOSYSTEM_PLAN.md
   - Long-term integration plan (Phases 4-7)
   - Multi-system integration vision
   - Where this project is headed

4. **How we work** → [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md)
   - Philosophy, Git workflow, testing
   - Documentation practices
   - Component architecture

5. **Then come back** to this README for component details

**What you might need:**
- Components → See Specialized Topics below
- Quick commands → Section 4 has quick start examples
- Lost context → Start with CONTEXT_RECOVERY.md

### 3. Principles

**See:** [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md) for complete philosophy

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

- [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - Current system state, what's working, what's in progress
- [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md) - Guide for AI assistants (captain-advisor model, workflows)
- [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md) - Philosophy, Git workflow, testing, documentation practices
- ERA_ECOSYSTEM_PLAN.md - Strategic integration plan (Phases 4-7, multi-system vision)
- CONFIGURATION_CENTRALIZATION_PLAN.md - Completed Oct 18 (migration to /Users/admin/ERA_Admin/)

#### Components

**[FathomInventory/](../FathomInventory/)** - Automated meeting analysis
- Purpose: AI-powered meeting discovery and participant extraction
- Records: 1,953 participants (1,698 validated/87%, 255 remaining)
- Automation: Daily at 3 AM via launchd
- Status: ✅ Operational
- Read: [FathomInventory/README.md](FathomInventory/README.md)

**[airtable/](../airtable/)** - Manual membership tracking
- Purpose: Membership database, donor tracking, TH attendance
- Records: 630 people (+58 from Phase 4B-2), 17 TH attendance columns
- Scripts: Read-only exports, cross-correlation with Fathom
- Status: ✅ Operational
- Read: [airtable/README.md](airtable/README.md)

**[integration_scripts/](../integration_scripts/)** - Cross-component bridges
- Purpose: Enrich Fathom data with Airtable information
- Phase 4B-1: ✅ Automated fuzzy matching (364 enriched)
- Phase 4B-2: 🔄 87% complete - Collaborative review (409 enriched, 8 rounds)
- Read: [integration_scripts/README.md](integration_scripts/README.md)
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