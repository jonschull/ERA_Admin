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

## FILE: README.md

**Path:** `README.md`

### 1. Overview

ERA Admin integrates 4 ERA data systems:

- Google Docs Agendas - Meeting notes with participant lists
- Airtable - Membership database
- Fathom Inventory - Automated meeting analysis
- ERA Landscape - Network visualization

**Goal:** Unified view of the ERA community

### 2. Orientation - Where to Find What

**You are here:** Main entry point for ERA_Admin

**For current status:** [CONTEXT_RECOVERY.md](#file-context_recoverymd)
**For AI assistants:** [AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd)
**For principles:** [WORKING_PRINCIPLES.md](#file-working_principlesmd)
**For components:** See Specialized Topics below

### 3. Principles

- Human-AI Collaboration
- Component Independence
- Git/PR Workflow
- Testing Discipline

**Details:** [WORKING_PRINCIPLES.md](#file-working_principlesmd)

### 4. Specialized Topics

**Documentation:**

- [CONTEXT_RECOVERY.md](#file-context_recoverymd)
- [AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd)
- [WORKING_PRINCIPLES.md](#file-working_principlesmd)

**Components:**

- [FathomInventory/README.md](#file-fathominventoryreadmemd)
- [airtable/README.md](#file-airtablereadmemd)
- [integration_scripts/README.md](#file-integration_scriptsreadmemd)

---

## FILE: CONTEXT_RECOVERY.md

**Path:** `CONTEXT_RECOVERY.md`

### 1. Overview

**Purpose:** Current system state and how to resume work

**This document contains:** Status, recent changes, what's in progress

### 2. Orientation

**Path:** [README.md](#file-readmemd) → CONTEXT_RECOVERY

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

### 2. Orientation

**Path:** [README.md](#file-readmemd) → AI_HANDOFF_GUIDE

**After this:** [CONTEXT_RECOVERY.md](#file-context_recoverymd)

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

### 2. Orientation

**Referenced by:**

- [AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd)
- All component READMEs

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

**Path:** [/README.md](#file-readmemd) → FathomInventory

**For system-wide status:** [/CONTEXT_RECOVERY.md](#file-context_recoverymd)
**For component status:** [CONTEXT_RECOVERY.md](#file-fathominventorycontext_recoverymd)
**For principles:** See section 3 below

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

### 2. Orientation

**Main context:** See [/CONTEXT_RECOVERY.md](#file-context_recoverymd)

**This adds:** Component-specific details

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

**Path:** [/README](#file-readmemd) → [FathomInventory](#file-fathominventoryreadmemd) → authentication

**When to use:** Cookies expired, token refresh, account switching
**For status:** See parent component's CONTEXT_RECOVERY.md

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

**Path:** [/README.md](#file-readmemd) → airtable

**For system-wide status:** [/CONTEXT_RECOVERY.md](#file-context_recoverymd)
**For component status:** Check actual data (630 people tracked)
**For principles:** See section 3 below

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

**Path:** [/README.md](#file-readmemd) → integration_scripts

**For system-wide status:** [/CONTEXT_RECOVERY.md](#file-context_recoverymd)
**For phase progress:** PHASE4B2_PROGRESS_REPORT.md
**Which README to read:** See section 4 below

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

### 2. Orientation

**Path:** [/README](#file-readmemd) → [AI_HANDOFF_GUIDE](#file-ai_handoff_guidemd) → [integration_scripts](#file-integration_scriptsreadmemd) → This

**General AI:** See [/AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd)

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
