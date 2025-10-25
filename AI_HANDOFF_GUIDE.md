# AI_HANDOFF_GUIDE.md

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
1. Read [README.md](README.md) - System overview
2. Read [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - Current state
3. Skim ERA_ECOSYSTEM_PLAN.md - Strategic direction
4. Identify current phase (Phase 4B-2, Phase 5T, etc.)
5. Read this AI_HANDOFF_GUIDE completely
6. Ask clarifying questions if needed

**Documentation Hierarchy:**

*Level 1: ERA Admin (Integration Layer)*
- When to read: Working on cross-component integration
- [README.md](README.md) - System overview, quick start
- [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - Current state snapshot
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
- Current work status → [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md)
- Philosophy & practices → [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md)
- Historical Phase 4B-2 workflow → integration_scripts/participant_reconciliation/archive/superseded_docs/AI_WORKFLOW_GUIDE.md
- Component details → Component READMEs

### 3. Principles

**System-wide:** See [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md) for complete philosophy

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

4. Create: integration_scripts/[integration_type]/your_script.py
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

# Get ERA_Admin root (scripts are in integration_scripts/[type]/)
SCRIPT_DIR = Path(__file__).parent
ERA_ADMIN_ROOT = SCRIPT_DIR.parent.parent  # Up two levels

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
- Historical workflow: integration_scripts/participant_reconciliation/archive/superseded_docs/AI_WORKFLOW_GUIDE.md
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
- Integration scripts: `integration_scripts/participant_reconciliation/*.py`

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

- [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md) - Complete system philosophy
- [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - Current system state
- integration_scripts/participant_reconciliation/archive/ - Historical Phase 4B-2 workflows
- Component READMEs - Component-specific details

**Back to:** [README.md](README.md)