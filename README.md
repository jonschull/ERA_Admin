# ERA Admin - Data Integration Hub

**Purpose:** Coordinate integration between ERA's data systems  
**Location:** `/Users/admin/ERA_Admin/` (deployed Oct 18, 2025)  
**Status:** ✅ System operational, config centralized, automation at 3 AM

---

## 🚨 STARTING POINT - READ THIS FIRST

### 👥 **For Everyone (Humans & AI):**

> **✅ RECENT:** Configuration centralization complete (Oct 18, 2025)  
> **📋 Strategic Plan:** [ERA_ECOSYSTEM_PLAN.md](ERA_ECOSYSTEM_PLAN.md) ← Multi-system integration vision  
> **📍 Current State:** [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) ← Start here

**If you're resuming work or just arriving:**
1. **Start here:** [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) ← Current system state & recent completions
2. **Strategic direction:** [ERA_ECOSYSTEM_PLAN.md](ERA_ECOSYSTEM_PLAN.md) ← Long-term integration plan
3. **For AI assistants:** [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md) ← Your role and conventions
4. **Recent work:** [CONFIGURATION_CENTRALIZATION_PLAN.md](CONFIGURATION_CENTRALIZATION_PLAN.md) ← Completed Oct 18
5. **Then come back** to this README for system overview

---

## 👤 For Humans: You Are the Captain

This is a **Windsurf development environment** where:
- **You (human)** are the **captain and navigator** - you set direction, make decisions, approve actions
- **AI assistants** are your **advisors and crew** - they research, propose solutions, execute approved tasks
- **This README** is your navigation chart - overview first, then specialized docs

---

## 🎯 What Is This?

ERA Admin is the **integration hub** for connecting four separate ERA data systems:

1. **Google Docs Agendas** - Meeting notes with participant lists (ground truth)
2. **Airtable** - Membership database (592 people, member/donor tracking)
3. **Fathom Inventory** - Automated meeting analysis (1,560 participants, AI-extracted)
4. **ERA Landscape** - Network visualization (350+ organizations/people/projects)

**Goal:** Connect these systems to create a unified view of the ERA community.

---

## 📂 What's In This Folder?

### Documentation (Start Here)
- **README.md** - This file (overview and quick start)
- **CONTEXT_RECOVERY.md** - Current state, how to resume work
- **AI_HANDOFF_GUIDE.md** - Working with AI assistants
- **ERA_ECOSYSTEM_PLAN.md** - Full integration strategy (Phases 4-7)

### Components (Self-Contained)
- **airtable/** - Manual membership tracking and exports
  - Read: `airtable/README.md` for details
  - Scripts: Export people, cross-correlation with Fathom
  
- **ERA_Landscape_Static** (sibling project) - Interactive network visualization
  - Git: https://github.com/jonschull/ERA_Landscape_Static
  - Live: https://jonschull.github.io/ERA_Landscape_Static/
  - Read its `README.md` for deployment and development

### Integration Scripts (Phase 4-5)
- **integration_scripts/** - Cross-component bridging scripts
  - **Phase 4B-1:** Automated fuzzy matching (✅ Complete - 364 enriched)
  - **Phase 4B-2:** Collaborative human-AI review (✅ 87% Complete - 8 rounds, 409 enriched)
  - **Read:** `integration_scripts/README.md` for complete workflow
  - **For AI:** `integration_scripts/AI_WORKFLOW_GUIDE.md` for collaboration process
  - **Progress:** `integration_scripts/PHASE4B2_PROGRESS_REPORT.md` for 8-round analysis

---

## 🚀 Quick Start

### View Current State
```bash
# Check Airtable exports
cd airtable
python export_people.py
# Exports 592 people to people_export.csv

# View landscape visualization
open https://jonschull.github.io/ERA_Landscape_Static/
# Interactive network graph
```

### Run Integration (Phase 4B-2)
```bash
# First: Verify configuration
python era_config.py
# Shows paths, verifies they exist

# Phase 4B-2: Collaborative review workflow (see integration_scripts/AI_WORKFLOW_GUIDE.md)
cd integration_scripts

# Generate review batch
python3 generate_batch_data.py          # Select next 25 people
python3 generate_phase4b2_table.py      # Create HTML review interface

# Human reviews in browser → exports CSV with decisions
# AI parses and executes approved actions

# Status: 87% complete (1,698/1,953 validated)
# See: integration_scripts/PHASE4B2_PROGRESS_REPORT.md
```

---

## 🗺️ How Systems Connect

### Current Integration Status

```
Google Docs Agendas (scribe notes)
    ↓ (manual extraction)
Airtable (592 people, TH attendance)
    ↓ (Phase 4B - enrichment scripts)
Fathom Inventory DB (1,560 participants)
    ↓ (Phase 5T - export scripts)
Google Sheet
    ↓ (automatic)
ERA Landscape (visualization)
```

**Phase 4B-1 (Complete):** Automated fuzzy matching - 364 enriched  
**Phase 4B-2 (87% Complete):** Collaborative review - 409 enriched (8 rounds)  
**Phase 5T (Next):** Fathom → Landscape Town Hall meetings

---

## 📋 Integration Roadmap

### ✅ Completed
- Phase 1-3: Fathom automation, participant database
- Phase 4A: Airtable validation (61.5% match with Fathom)
- **Phase 4B-1:** Automated fuzzy matching ✅ (Oct 19, 2025)
  - 364 participants enriched
  - 188 AI-misspelled names corrected
  - 351 members identified, 64 donors
- **Phase 4B-2:** Collaborative human-AI review (Oct 20, 2025)
  - **8 rounds completed** - 409 participants validated
  - **58 new people added to Airtable** (+10% growth)
  - **87% complete** (1,698/1,953 validated)
  - **Production-ready workflow** established
  - See: `integration_scripts/PHASE4B2_PROGRESS_REPORT.md`

### 🎯 Current Priority
- **Phase 4B-2 Completion** (Estimated: 5 more rounds)
  - Process remaining 255 participants
  - Target 95%+ completion
  - Use established collaborative workflow
  
- **Phase 5T:** Town Hall Visualization ⭐ AFTER 4B-2 (3-4 hours)
  - Export 17 TH meetings as project nodes
  - Connect 300+ participants to meetings
  - Create sequential meeting chain in landscape

### ⏳ Upcoming
- Phase 4C: Daily Airtable sync automation
- Phase 6: MySQL migration (Q1 2026)
- Phase 7: Interactive agenda app (Q2 2026)

**Full plan:** See [ERA_ECOSYSTEM_PLAN.md](ERA_ECOSYSTEM_PLAN.md)

---

## 🔍 Component Details

### Airtable (Manual Tracking)
- **Purpose:** Membership database, donor tracking
- **Records:** 630 people (+58 from Phase 4B-2), 17 TH attendance columns
- **Scripts:** Read-only exports, cross-correlation
- **Docs:** `airtable/README.md`
- **Recent:** +10% growth from Fathom participant reconciliation (Oct 20)

### ERA Landscape (Visualization)
- **Purpose:** Interactive network graph of ERA ecosystem
- **Content:** 350+ organizations, people, projects + relationships
- **Technology:** Static HTML/JS, Google Sheets data source
- **Docs:** `ERA_Landscape_Static/README.md`, `VISION.md`
- **Live:** https://jonschull.github.io/ERA_Landscape_Static/

### Fathom Inventory (Automated Analysis)
- **Location:** `ERA_Admin/FathomInventory/` (moved into ERA_Admin Oct 2025)
- **Purpose:** Automated meeting discovery & participant extraction
- **Records:** 1,953 participants tracked
  - **1,698 validated (87%)** - enriched with Airtable data
  - **255 remaining (13%)** - need review
- **Automation:** Daily at 3 AM via launchd (`com.era.admin.fathom.run`)
- **Docs:** `FathomInventory/README.md`, `integration_scripts/README_PHASE4B.md`
- **Venv:** `/Users/admin/ERA_Admin_venv` (shared, outside Dropbox)

**Note:** Now integrated into ERA_Admin. Uses shared venv outside Dropbox to avoid automation conflicts.

---

## ⚠️ Important Notes

### Folder Structure
- **ERA_Admin** (this folder) is at `/Users/admin/ERA_Admin/`
  - **OUTSIDE Dropbox** - migrated Oct 18, 2025
  - Contains all components including FathomInventory
  - Safe for automated workflows (no file-locking issues)
  - Git repository for version control
  
- **ERA_Admin_venv** is at `/Users/admin/ERA_Admin_venv/`
  - Shared Python virtual environment (also outside Dropbox)
  - Required packages: See `requirements.txt`
  
- **Dropbox copy** (if it exists) is BACKUP ONLY
  - Active development is in `/Users/admin/ERA_Admin/`
  - Do not use Dropbox copy for automation

### Data Flow Direction
1. **Agendas** (Google Docs) → Airtable (manual)
2. **Fathom** (automated) → FathomInventory DB
3. **Airtable** → FathomInventory DB (enrichment)
4. **FathomInventory DB** → Google Sheet (export)
5. **Google Sheet** → Landscape (visualization)

**Future:** All → MySQL Database (single source of truth)

---

## ⚙️ System Requirements & Known Gotchas

### Virtual Environment
**Location:** `/Users/admin/ERA_Admin_venv` (outside Dropbox)  
**Why:** Prevents file-locking issues during launchd automation

**Setup:**
```bash
python3 -m venv /Users/admin/ERA_Admin_venv
/Users/admin/ERA_Admin_venv/bin/pip install -r requirements.txt
```

**Required packages:** See `requirements.txt` for full list including:
- `pyairtable` - Airtable API access
- `google-api-python-client` - Gmail/Google APIs (critical for FathomInventory)
- `playwright` - Browser automation for Fathom scraping
- `fuzzywuzzy` - String matching for cross-correlation

### Launchd Automation (FathomInventory)
**Job:** `com.era.admin.fathom.run`  
**Schedule:** Daily at 3:00 AM  
**Plist:** `~/Library/LaunchAgents/com.era.admin.fathom.run.plist`

**Key gotchas:**
1. **Venv paths must be absolute** - No relative paths in scripts
2. **Google API packages required** - Email download fails without them
3. **Bash output capturing** - Use temp files, not command substitution with multiple pipes
4. **Log locations** - Use `~/Library/Logs/`, not Dropbox paths

**Monitoring:**
```bash
# Check if job is loaded
launchctl list | grep fathom

# View recent logs
tail -f ~/Library/Logs/fathom_run.log

# Manual test run
cd FathomInventory && ./run_all.sh
```

### Common Issues & Solutions

**Issue:** "ModuleNotFoundError: No module named 'google'"  
**Solution:** Install FathomInventory requirements in shared venv:
```bash
/Users/admin/ERA_Admin_venv/bin/pip install -r FathomInventory/requirements.txt
```

**Issue:** Script hangs during launchd execution  
**Solution:** Avoid command substitution with pipes. Use temp files:
```bash
# Bad (hangs):
OUTPUT=$(python script.py 2>&1 | tee log.txt)

# Good (works):
python script.py 2>&1 | tee /tmp/output.log
OUTPUT=$(cat /tmp/output.log)
```

**Issue:** "Resource deadlock avoided" in venv activation  
**Solution:** Venv must be outside Dropbox. Use `/Users/admin/ERA_Admin_venv`

**Recovery from move issues:** See `historical/move_recovery_oct2025/` for detailed documentation.

---

## 📊 Current Metrics

### Data Coverage
- **Airtable:** 630 people (+58 from Phase 4B-2), 324 TH attendance records
- **Fathom:** 1,953 participants tracked
  - 1,698 validated (87%) - enriched with Airtable data
  - 255 remaining (13%) - need review
- **Validation:** 61.5% baseline → 87% enriched (Phase 4B-1 + 4B-2)
- **Landscape:** 350+ nodes (organizations, people, projects)

### Integration Status
- **Phase 4B-1:** ✅ Complete - 364 enriched via fuzzy matching
- **Phase 4B-2:** 🔄 87% Complete - 409 enriched via collaborative review (8 rounds)
- **Phase 5T:** Ready to implement after 4B-2 completion
- **All → MySQL:** Planned for Q1 2026

---

## 🎓 Getting Started

### New to ERA Admin?
1. Read this README (you are here)
2. Read component READMEs for areas of interest
3. See ERA_ECOSYSTEM_PLAN.md for full strategy

### Resuming Work?
1. Read CONTEXT_RECOVERY.md (current state)
2. Check component CONTEXT_RECOVERY.md if working on specific system
3. Follow integration scripts README for Phase 4-5 work

### Working with AI?
1. Read AI_HANDOFF_GUIDE.md (workflows and conventions)
2. Point AI to component README for focused work
3. Use ERA_ECOSYSTEM_PLAN.md for integration understanding

---

## 📞 Questions?

**System integration:** See ERA_ECOSYSTEM_PLAN.md  
**Airtable exports:** See airtable/README.md  
**Landscape visualization:** See ERA_Landscape_Static/README.md  
**Fathom automation:** See FathomInventory/README.md  
**System gotchas:** See "System Requirements & Known Gotchas" section above  
**Lost context:** See CONTEXT_RECOVERY.md

---

**Last Updated:** October 20, 2025  
**Current Phase:** 4B-2 Collaborative Review (87% Complete) → 5T (Town Hall Visualization)  
**Maintainer:** Jon Schull (jschull@gmail.com)  
**Recent:** Phase 4B-2 - 8 rounds completed, 409 participants validated, 58 people added to Airtable  
**See:** `integration_scripts/PHASE4B2_PROGRESS_REPORT.md` for detailed analysis
