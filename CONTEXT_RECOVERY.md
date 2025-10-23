# CONTEXT_RECOVERY.md

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
- **Main overview** → [README.md](README.md) - System architecture and components
- **Strategic plan** → ERA_ECOSYSTEM_PLAN.md - Long-term vision (Phases 4-7)
- **AI workflow** → [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md) - How to work with AI
- **How we work** → [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md) - Philosophy and practices
- **Component status** → Component CONTEXT_RECOVERY files (FathomInventory, etc.)
- **Recent changes** → CONFIGURATION_CENTRALIZATION_PLAN.md - Oct 18 migration

### 3. Principles

**System-wide:** See [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md)

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
- Read this AFTER [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md)
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

*Oct 20, 2025:*
- ✅ Phase 4B-2: Collaborative Human-AI Review (8 rounds)
  - 409 participants validated
  - 58 new people added to Airtable (+10% growth)
  - Production-ready workflow established
  - See: `integration_scripts/PHASE4B2_PROGRESS_REPORT.md`

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

- [FathomInventory/CONTEXT_RECOVERY.md](FathomInventory/CONTEXT_RECOVERY.md) - Component-specific status

#### Where to Find Help

- Integration strategy: ERA_ECOSYSTEM_PLAN.md
- Airtable details: airtable/README.md
- Landscape details: ERA_Landscape/README.md, NETWORK_ARCHITECTURE.md
- Fathom details: FathomInventory/README.md
- AI workflow: [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md)

**Back to:** [README.md](README.md)