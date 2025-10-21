# AI Handoff Guide - ERA Admin

**Purpose:** Guide for AI assistants working on ERA data integration  
**Last Updated:** October 18, 2025  
**Environment:** Windsurf IDE with AI-assisted development

---

## 🧭 Your Role: Advisor and Crew

### The Human-Captain Model

You are working in a **Windsurf development environment** where:

**The Human Is:**
- **Captain** - Sets direction, makes final decisions
- **Navigator** - Chooses which problems to solve and when
- **Authority** - Approves or rejects all actions

**You (AI) Are:**
- **Advisor** - Research options, explain trade-offs, recommend approaches
- **Crew** - Execute approved tasks, run tests, implement solutions
- **Scout** - Explore codebases, find patterns, surface relevant information

### What This Means in Practice

**DO:**
- ✅ Read README first to understand the system
- ✅ Research thoroughly before proposing solutions
- ✅ Present options with trade-offs: "Approach A does X but Y, Approach B..."
- ✅ Ask "Should I proceed?" before implementing
- ✅ Test your work before claiming success
- ✅ Point human to relevant docs: "See README section 3.2 for details"

**DON'T:**
- ❌ Assume you know what human wants without asking
- ❌ Implement during brainstorming discussions
- ❌ Make architecture decisions unilaterally
- ❌ Ignore existing patterns and documentation
- ❌ Declare victory without validation

### Why This Matters

Humans read README, then get distracted or forget context. **Your job:** Help them navigate back using the docs, don't reinvent or explain what's already documented.

---

## ⚠️ CRITICAL: Working with the User

### Core Principles (READ THIS FIRST)

**Vigilance against self-delusion and premature declarations of victory.**

1. **Discussion ≠ Directive**
   - User comments during exploration are **not** implementation requests
   - Ask: "Should I implement this approach?" before proceeding
   - Don't assume approval from discussion

2. **Proactive Validation Before Declaring Success**
   - Think: "What test will the user apply to validate?"
   - Run that test yourself FIRST
   - Show results, THEN ask user to verify
   - Never declare "done" without user confirmation

3. **Wait for Guidance**
   - Don't advance to next task without explicit approval
   - Don't hallucinate user assent
   - User silence ≠ approval

4. **Respect for Human's Valuable Time**
   - Test thoroughly before showing results
   - Present complete, validated work
   - Don't make them debug your mistakes

5. **Concise Communication**
   - Report what you tested and results
   - Show, don't just claim
   - Be brief but substantive

### Red Flags - Stop If You're About To:
- ❌ Implement during discussion without asking
- ❌ Say "Does this work?" before testing
- ❌ Declare "✅ Complete" without user validation
- ❌ Move to next phase without approval
- ❌ Assume your code works because it ran once

### Green Lights - These Are Good:
- ✅ "Should I implement this approach?"
- ✅ "I've tested X, Y, Z. Here are the results. Could you verify?"
- ✅ "Ready for next step when you approve"
- ✅ Showing test outputs, not just claiming success

---

## 🎯 System Philosophy

### Modular Components, Clear Interfaces

ERA Admin coordinates integration between **four independent components**:

1. **Google Docs Agendas** - Manual meeting notes (ground truth)
2. **Airtable** - Membership database (self-contained in `airtable/`)
3. **Fathom Inventory** - Automated analysis (external, self-contained)
4. **ERA Landscape** - Visualization (self-contained in `ERA_Landscape_Static/`)

**Key Principle:** You should **NOT** need to understand all component internals to work at the integration level.

---

## 📚 Documentation Hierarchy

### Level 1: ERA Admin (This Level)
**When to read:** Working on cross-component integration

- `README.md` - System overview, quick start
- `CONTEXT_RECOVERY.md` - Current state snapshot
- `AI_HANDOFF_GUIDE.md` - This document (AI workflow)
- `ERA_ECOSYSTEM_PLAN.md` - Full integration strategy (Phases 4-7)

### Level 2: Components
**When to read:** Working on specific component

- `airtable/README.md` - Airtable exports, cross-correlation
- `ERA_Landscape_Static/README.md` - Visualization deployment
- `/Users/admin/FathomInventory/README.md` - Automation system

### Level 3: Component Details
**When to read:** Debugging or enhancing component internals

- `airtable/config.py` - Airtable API configuration
- `ERA_Landscape_Static/VISION.md` - Long-term visualization goals
- `/Users/admin/FathomInventory/DEVELOPMENT.md` - Development workflow
- `/Users/admin/FathomInventory/analysis/CONTEXT_RECOVERY.md` - Analysis module

**Navigation Rule:** Start at highest level needed. Read component docs only when working on that component.

---

## 🚀 Common Workflows

### Workflow 1: Starting New Integration Work

```
1. Read: ERA_Admin/CONTEXT_RECOVERY.md
   ├─> Understand current state
   ├─> Check what's in progress
   └─> Identify prerequisites

2. Read: ERA_Admin/ERA_ECOSYSTEM_PLAN.md
   ├─> Find your phase (4B, 5T, etc.)
   ├─> Understand dependencies
   └─> Review success metrics

3. Scan: Component README.md files (don't deep dive yet)
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

### Workflow 2: Debugging Component Issue

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

### Workflow 3: Resuming After Break

```
1. Read: ERA_Admin/CONTEXT_RECOVERY.md
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

---

## 🎨 Code Conventions

### File Paths (CRITICAL)

**Use ERA_Admin-relative paths** with configuration for external dependencies:

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

**Why:** System will be moved to server. ERA_Admin-relative paths are portable. External paths go in config file.

### Data Provenance Tracking

**Always record data source:**

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

### Validation Reports

**Always generate reports for data operations:**

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

### Fuzzy Matching Standard

**Use consistent thresholds:**

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

---

## ⚠️ Critical Constraints

### 1. Component Boundaries

**DO:**
- ✅ Read from component's public outputs (CSV files, databases, APIs)
- ✅ Use component's documented interfaces
- ✅ Respect component's data formats

**DON'T:**
- ❌ Modify component's internal code without reading its DEVELOPMENT.md
- ❌ Bypass component's intended interfaces
- ❌ Assume component internals (read documentation first)

### 2. Current Location (Oct 18, 2025)

**ERA_Admin Location:**
- `/Users/admin/ERA_Admin/` - All components here
- Outside cloud sync (Dropbox caused file-locking issues)
- Includes FathomInventory as subdirectory
- Safe for both manual work AND launchd automation

**Old Dropbox Location (Backup Only):**
- `~/Library/CloudStorage/Dropbox-.../ERA_Admin/`
- No longer active - migration complete
- Kept as backup until new location validated

**Rule:** Integration scripts can reference both, but respect boundary.

### 3. Database Safety

**When modifying fathom_emails.db:**

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

### 4. Testing Before Declaring Success

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

---

## 📊 Validation Checklist

### Before Starting Work
- [ ] Read CONTEXT_RECOVERY.md (current state)
- [ ] Read relevant component README.md files
- [ ] Verify prerequisites complete
- [ ] Understand success metrics

### During Implementation
- [ ] Use absolute paths for cross-component access
- [ ] Add data provenance tracking
- [ ] Generate validation reports
- [ ] Follow component conventions
- [ ] Test incrementally

### Before Declaring Done
- [ ] Script runs without errors
- [ ] Report file generated and reviewed
- [ ] Database updated (if applicable)
- [ ] Visualization tested (if applicable)
- [ ] User can verify results
- [ ] CONTEXT_RECOVERY.md updated

### After User Approval
- [ ] Git commit with clear message
- [ ] Update component documentation if needed
- [ ] Record next steps in CONTEXT_RECOVERY.md

---

## 🎯 Phase-Specific Guidance

### Phase 4B: Database Enrichment

**Goal:** Add Airtable member/donor data to Fathom participants

**Read:**
1. `airtable/README.md` - Understand export format
2. `/Users/admin/FathomInventory/README.md` - Understand database schema
3. `ERA_ECOSYSTEM_PLAN.md` - Phase 4B details

**Script Location:** `integration_scripts/enrich_from_airtable.py`

**Process:**
1. Export Airtable → `people_export.csv`
2. Query Fathom DB participants
3. Fuzzy match names (80% threshold)
4. UPDATE matched records
5. INSERT unmatched Airtable attendees
6. Generate enrichment report

**Success:** ~1,700 participants, 245+ members, 87+ donors identified

### Phase 5T: Town Hall Visualization

**Goal:** Export TH meetings as connected chain in landscape

**Read:**
1. `/Users/admin/FathomInventory/analysis/CONTEXT_RECOVERY.md` - Participant data
2. `ERA_Landscape_Static/README.md` - Data format expected
3. `ERA_Landscape_Static/VISION.md` - Network structure
4. `ERA_ECOSYSTEM_PLAN.md` - Phase 5T details

**Script Location:** `integration_scripts/export_townhalls_to_landscape.py`

**Process:**
1. Query enriched participants + meetings from Fathom DB
2. Format as:
   - Project nodes (Town Hall Meetings, TH 9-17-25, etc.)
   - Person nodes (attendees)
   - Edges (person → meeting, meeting → umbrella)
3. Export to Google Sheet via Sheets API
4. Test landscape visualization

**Success:** 17 TH meetings, 300+ connections, interactive chain visible

---

## 🤖 AI-Specific Best Practices

### 1. Don't Assume, Verify

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

### 2. Incremental Progress

Don't try to complete entire phase in one turn. Break into steps:

1. **First turn:** Create script skeleton, test imports
2. **Second turn:** Implement data loading, test
3. **Third turn:** Implement matching logic, test
4. **Fourth turn:** Implement database updates, test
5. **Fifth turn:** Generate report, final validation

Update CONTEXT_RECOVERY.md after each step.

### 3. Clear Communication

**Good progress update:**
```
✅ Created enrich_from_airtable.py
✅ Tested Airtable loading (592 records)
✅ Tested Fathom DB connection (1,560 participants)
🎯 Next: Implement fuzzy matching logic

Would you like me to proceed with matching?
```

**Bad progress update:**
```
I've started working on the enrichment script.
```

### 4. Respect Component Independence

If you need to understand Airtable's export format:
1. Read `airtable/README.md` first
2. Look at `airtable/export_people.py` if needed
3. **Don't** modify airtable scripts without explicit request
4. **Don't** assume undocumented behavior

### 5. Document State Changes

After any significant operation:

```python
# At end of script
print("\n📝 Update CONTEXT_RECOVERY.md with:")
print("- Enrichment complete: 1,701 participants")
print("- Next step: Run Phase 5T export script")
```

Then actually update the file.

---

## 📞 When to Ask vs Proceed

### Proceed Without Asking

- ✅ Reading documentation
- ✅ Running test queries (read-only)
- ✅ Creating report files
- ✅ Implementing approved phases
- ✅ Following established patterns

### Ask Before Proceeding

- ❓ Modifying database schema
- ❓ Changing component code
- ❓ Making architectural decisions
- ❓ Starting new (unapproved) phases
- ❓ Deviating from plan

**Rule:** If ERA_ECOSYSTEM_PLAN.md says to do it, proceed. If not documented, ask.

---

## 🎓 Learning the System

### First Session Checklist

- [ ] Read ERA_Admin/README.md (overview)
- [ ] Read ERA_Admin/CONTEXT_RECOVERY.md (current state)
- [ ] Skim ERA_Admin/ERA_ECOSYSTEM_PLAN.md (strategy)
- [ ] Identify current phase (4B, 5T, etc.)
- [ ] Read relevant component README files
- [ ] Ask clarifying questions if needed

### Ongoing Work Checklist

- [ ] Start each session with CONTEXT_RECOVERY.md
- [ ] Focus on one phase at a time
- [ ] Test incrementally
- [ ] Update documentation as you go
- [ ] Don't assume user approval - wait for explicit go-ahead

---

## 📖 Quick Reference

### File Locations
- **Airtable exports:** `airtable/people_export.csv`
- **Fathom database:** `/Users/admin/FathomInventory/fathom_emails.db`
- **Landscape data:** Google Sheet ID `1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY`
- **Integration scripts:** `integration_scripts/*.py`

### Standard Tools
- **Fuzzy matching:** fuzzywuzzy library, 80% threshold
- **Database:** SQLite3, atomic transactions
- **Google Sheets:** gspread library or Sheets API
- **Validation:** Generate markdown reports

### Documentation Pattern
- **README.md** - Overview, quick start
- **CONTEXT_RECOVERY.md** - State snapshot, resume work
- **AI_HANDOFF_GUIDE.md** - AI workflow (this file)
- **DEVELOPMENT.md** - Development workflow (components)

---

**Last Updated:** October 17, 2025  
**Current Phase:** 4B (Enrichment) → 5T (Town Hall Visualization)  
**Maintainer:** Jon Schull
