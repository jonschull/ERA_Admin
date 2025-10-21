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

**Purpose:** Current system state and how to resume work

**This document contains:** Status, recent changes, what's in progress

### 2. Orientation - Where to Find What

**You are at:** System-wide context document

**What you might need:**
- Main entry → [README.md](#file-readmemd)
- Component status → See component CONTEXT_RECOVERY files
- Principles → [WORKING_PRINCIPLES.md](#file-working_principlesmd)

### 3. Principles

**See:** [WORKING_PRINCIPLES.md](#file-working_principlesmd)

**Applied:** Proactive validation, documentation maintenance

### 4. Specialized Topics

**System State:**

- ✅ Airtable: 630 people
- ✅ Fathom: 1,953 participants, 3AM automation
- ✅ Phase 4B-2: 87% (1,698/1,953)

**Recent:** Oct 20 monorepo consolidation

**Component context:**

- [FathomInventory/CONTEXT_RECOVERY.md](#file-fathominventorycontext_recoverymd)

**Back:** [README.md](#file-readmemd)

---

## FILE: AI_HANDOFF_GUIDE.md

**Path:** `AI_HANDOFF_GUIDE.md`

### 1. Overview

Guide for AI assistants on ERA Admin

### 2. Orientation - Where to Find What

**You are at:** AI assistant onboarding guide

**What you might need:**
- Main entry → [README.md](#file-readmemd)
- Current state → [CONTEXT_RECOVERY.md](#file-context_recoverymd)
- Principles → [WORKING_PRINCIPLES.md](#file-working_principlesmd)
- Specialized AI workflows → See Specialized Topics below

### 3. Principles

**See:** [WORKING_PRINCIPLES.md](#file-working_principlesmd) for complete philosophy

**Key for AI:**

- Discussion ≠ directive
- Ask "Should I proceed?"
- Proactive validation

### 4. Specialized Topics

**General workflow:** DO/DON'T lists

**Specialized workflows:**

- Phase 4B-2: [integration_scripts/AI_WORKFLOW_GUIDE.md](#file-integration_scriptsai_workflow_guidemd)

**Related:**

- [WORKING_PRINCIPLES.md](#file-working_principlesmd)
- [CONTEXT_RECOVERY.md](#file-context_recoverymd)

**Back:** [README.md](#file-readmemd)

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
