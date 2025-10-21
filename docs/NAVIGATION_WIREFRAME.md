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

ERA Admin integrates 4 ERA data systems:

- Google Docs Agendas - Meeting notes with participant lists
- Airtable - Membership database
- Fathom Inventory - Automated meeting analysis
- ERA Landscape - Network visualization

**Goal:** Unified view of the ERA community

### 2. Orientation - Where to Find What

**You are at:** Main entry point (root README)

**What you might need:**
- Current status → [CONTEXT_RECOVERY.md](#file-context_recoverymd)
- AI guidance → [AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd)
- How we work → [WORKING_PRINCIPLES.md](#file-working_principlesmd)
- Components → See Specialized Topics below

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
- `ERA_Landscape_Static/` - Network visualization

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
- analysis/ - AI analysis scripts for ERA meetings
- docs/ - Detailed technical documentation
- scripts/ - Pipeline automation scripts

**Key Component Files:**
- [CONTEXT_RECOVERY.md](#file-fathominventorycontext_recoverymd) - Current component state
- DEVELOPMENT.md - Development workflow, testing, constraints
- BACKUP_AND_RECOVERY.md - Data backup and recovery procedures

**Back to:** [/README.md](#file-readmemd)

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
