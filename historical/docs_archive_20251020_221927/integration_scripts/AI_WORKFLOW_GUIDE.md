# AI Workflow Guide: Phase 4B-2 Collaborative Review

**For:** AI assistants stepping into Phase 4B-2 mid-stream  
**Purpose:** Make the human-AI collaboration workflow explicit  
**Audience:** A "naive AI" without conversation history

---

## Mental Model: What This Process Is

**NOT traditional automation** - This is **collaborative data curation**

You are not trying to solve this alone. You are:
1. **Generating data** for human review
2. **Researching** unclear cases
3. **Discussing** ambiguous decisions
4. **Executing** approved actions safely

**Key mindset:** The human makes final decisions. You provide research, suggestions, and execution capability.

---

## The Core Cycle: Human-AI Back-and-Forth

### Phase 1: AI Generates Review Interface
**Your role:** Create sortable HTML table for human review

```bash
python3 generate_batch_data.py          # Select next 25 people
python3 generate_phase4b2_table.py      # Create HTML interface
```

**What you're doing:**
- Selecting 25 unenriched participants from Fathom database
- Fuzzy matching against Airtable people
- Creating interactive HTML with:
  - Video links for identity verification
  - Gmail research capability
  - Match suggestions with confidence scores
  - Export-to-CSV functionality

**Mental state:** You're setting up the workspace. Don't make decisions yet.

---

### Phase 2: Human Reviews & Exports
**Human's role:** Review your suggestions, research unclear cases, make decisions

**What they do:**
1. Open HTML in browser
2. Click video links (🎥) to verify identities
3. Use Gmail research for unknown people
4. Add comments with decisions:
   - `merge with: Full Name` - Merge to existing person
   - `drop` - Remove junk entry
   - Custom notes for complex cases
5. Check/uncheck ProcessThis boxes
6. Mark Probe boxes for unclear items
7. Export to CSV

**Your role during this:** WAIT. Don't process anything yet.

**CSV Structure They Export:**
```
Fathom_Name, Comments, ProcessThis, Probe
"John's iPhone", "John Magugu", YES, YES
"Ana", "Ana Calderon", NO, YES
"Bob", "drop", YES, NO
```

---

### Phase 3: AI Parses & Flags Issues
**Your role:** Parse CSV and identify what needs discussion

```bash
python3 parse_phase4b2_csv.py <csv_file>
```

**What to look for:**

1. **Standard comments** (auto-processable):
   - `merge with: Name`
   - `drop`
   - `add to airtable`
   - `ignore`

2. **Custom comments** (need discussion):
   - Anything that doesn't match standard patterns
   - Names without "merge with:" prefix
   - Notes with context (e.g., "ERA Member", "Organization: X")
   - ProcessThis=YES with custom comment = **REQUIRES DISCUSSION**

**Mental state:** You're a quality checker. Flag anything ambiguous.

**CRITICAL:** If `parse_phase4b2_csv.py` shows custom comments, **STOP and discuss with user**. Do not proceed to execution.

---

### Phase 4: Human-AI Discussion
**When this happens:** Custom comments detected OR Probe=YES items

**Your role:** Present unclear cases and ask clarifying questions

**Example dialogue:**

```
AI: "I found 3 custom comments that need clarification:

1. 'Andres's iPhone (2)'
   Comment: 'Andres Garcia'
   ProcessThis: YES
   
   This appears to be a device name → person mapping.
   Should I merge 'Andres's iPhone (2)' to 'Andres Garcia'?
   Is Andres Garcia already in Airtable?"

Human: "Yes, merge to Andres Garcia. Check if he's in Airtable."

AI: [Checks Airtable CSV]
    "✅ Andres Garcia is in Airtable.
     I'll merge 'Andres's iPhone (2)' → 'Andres Garcia'"
```

**What you should do:**
1. **Present each custom comment** with context
2. **Check Airtable** if merging to person
3. **Ask clarifying questions** if intent unclear
4. **Categorize the action:**
   - Merge to existing person?
   - Add new person to Airtable?
   - Drop/ignore?
5. **Document the decision** for execution script

**Mental state:** You're a research assistant helping the human decide. Don't guess - ask.

---

### Phase 5: AI Executes Actions
**Your role:** Build and run execution script with ALL decisions from discussion

**IMPORTANT:** Do not create a new generic executor. Copy and modify the most recent `execute_roundN_actions.py`.

```bash
# Copy previous round as template
cp execute_round8_actions.py execute_round9_actions.py

# Edit to reflect THIS round's decisions:
# - Update people_to_add list
# - Update standard_merges list
# - Update custom_merges list
# - Update drops list
```

**Script Structure (FOLLOW THIS PATTERN):**
```python
#!/usr/bin/env python3
"""
Execute Round N actions from CSV.
"""

import sqlite3, csv, sys
from pathlib import Path
from datetime import datetime
import shutil

# Import add_to_airtable module
sys.path.insert(0, str(Path(__file__).parent))
from add_to_airtable import add_people_to_airtable, update_fathom_validated

# Paths
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent / "FathomInventory" / "fathom_emails.db"
BACKUP_DIR = SCRIPT_DIR.parent / "FathomInventory" / "backups"
AIRTABLE_CSV = SCRIPT_DIR.parent / "airtable" / "people_export.csv"

print("\n" + "=" * 80)
print("PHASE 4B-2 ROUND N: EXECUTE ACTIONS")
print("=" * 80)

# 1. BACKUP DATABASE
BACKUP_DIR.mkdir(exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M')
backup_path = BACKUP_DIR / f"fathom_emails.backup_{timestamp}.db"
shutil.copy2(DB_PATH, backup_path)

# 2. LOAD AIRTABLE
airtable_people = {}
with open(AIRTABLE_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('Name'):
            airtable_people[row['Name']] = row

# 3. EXECUTE STANDARD MERGES (from CSV)
standard_merges = [
    ('Fathom Name', 'Airtable Name'),
    # ... from CSV merge with: comments
]

# 4. EXECUTE DROPS
drops = ['Name1', 'Name2']

# 5. ADD PEOPLE TO AIRTABLE
people_to_add = [
    {'name': 'New Person', 'is_member': True, 'notes': 'Context'},
]
added, skipped = add_people_to_airtable(people_to_add, conn)

# 6. EXECUTE CUSTOM MERGES (device names, organizations, etc.)
custom_merges = [
    ("Device Name", 'Real Name'),
]

# 7. COMMIT & REPORT
conn.commit()
print(final_stats)
```

**Mental state:** You're the executor. Follow the pattern exactly. Every round looks the same.

---

### Phase 6: AI Commits & Documents
**Your role:** Commit changes with comprehensive message

```bash
git add -A integration_scripts/ airtable/
git commit -m "Complete Round N: X actions + Y new people

EXECUTED:
✅ X total actions

[List all merges, drops, adds]

DATABASE STATUS:
- Validated: X
- Remaining: Y
"
```

**What to document:**
- Total actions executed
- New people added to Airtable
- Special cases handled
- Database stats (before → after)
- Any issues encountered

**Mental state:** You're the historian. Document everything for future AI/human.

---

## Common Patterns You'll Encounter

### Pattern 1: Device Names → People
```
Fathom: "John's iPhone"
Human comment: "John Magugu"
→ Check if John Magugu in Airtable
→ If yes: merge
→ If no: add to Airtable, then merge
```

### Pattern 2: Organization Names → People
```
Fathom: "BioIntegrity"
Human comment: "Chris Searles\nOrganization: Biointegrity"
→ Check if Chris Searles in Airtable
→ Organization is a note, not a person
→ Merge "BioIntegrity" → "Chris Searles"
```

### Pattern 3: Name Variants
```
Fathom: "Belize", "Belizey", "Brendah"
Human comment: "Mbilizi Kalombo" (for all three)
→ All three are nicknames for same person
→ Merge all → "Mbilizi Kalombo"
```

### Pattern 4: Single Names → Full Names
```
Fathom: "Ana"
Human comment: "Ana Calderon"
ProcessThis: NO, Probe: YES
→ Human wants to verify first
→ Check if Ana Calderon in Airtable
→ If yes: merge
→ If no: discuss whether to add
```

### Pattern 5: Phone Numbers
```
Fathom: "18022588598"
Human comment: "Michael Mayer"
→ Map phone number to person
→ Check if Michael Mayer in Airtable
→ Merge phone number entry to person
```

### Pattern 6: Add New ERA Members
```
Fathom: "Andrew Atencia"
Human comment: "Should be ERA Member"
ProcessThis: YES
→ Person not in Airtable
→ Add to Airtable with is_member=True
→ Then merge Fathom record to new entry
```

---

## Decision Trees for Common Scenarios

### When You See: Custom Comment + ProcessThis=YES

1. **Is target in Airtable?**
   - YES → Execute merge
   - NO → Go to step 2

2. **Should we add to Airtable?**
   - Comment says "ERA Member" → Add then merge
   - Comment is just a name → Ask human
   - Comment says "drop" → Drop instead

3. **Is it a device/org/variant?**
   - Device name ("iPhone", "iPad") → Merge to person
   - Organization → Merge to representative
   - Variant (nickname) → Merge to canonical name

### When You See: Probe=YES

1. **Read the comment carefully**
2. **Check if target exists in Airtable**
3. **Present to human:**
   ```
   "Item marked for probing:
   - Fathom: 'Ana'
   - Comment: 'Ana Calderon'
   - Ana Calderon IS in Airtable
   
   Should I merge 'Ana' → 'Ana Calderon'?"
   ```
4. **Wait for confirmation**
5. **Document decision for execution**

---

## Critical Rules

### ❌ DON'T:
1. **Auto-execute** when custom comments are present
2. **Guess** what the human meant - ask
3. **Add people to Airtable** without explicit approval
4. **Skip backups** - always backup before changes
5. **Create generic executors** - use round-specific scripts
6. **Ignore Probe flags** - they mean "discuss this"

### ✅ DO:
1. **Check Airtable** before every merge decision
2. **Ask clarifying questions** for ambiguous comments
3. **Use add_to_airtable.py** module for consistency
4. **Follow the pattern** from execute_round4-8_actions.py
5. **Document thoroughly** in git commits
6. **Report stats** after every execution

---

## Troubleshooting

### Problem: "Target not in Airtable"
**Solution:** Ask human if we should add them first

### Problem: "Multiple custom comments"
**Solution:** Discuss ALL of them before executing ANY

### Problem: "Unclear what action to take"
**Solution:** Present options to human:
```
"I see 'sustainavistas' with comment 'Grant Holton'.
Options:
1. Merge sustainavistas → Grant Holton (if he's in Airtable)
2. Drop sustainavistas (if it's just an org, and Grant is already tracked)
3. Add Grant Holton then merge

Which should I do?"
```

### Problem: "Script fails partway through"
**Solution:** Check backup, restore if needed:
```bash
ls -lt FathomInventory/backups/
cp FathomInventory/backups/fathom_emails.backup_YYYYMMDD_HHMM.db \
   FathomInventory/fathom_emails.db
```

---

## Files You'll Use Every Round

| File | Purpose | When to Use |
|------|---------|-------------|
| `generate_batch_data.py` | Select 25 people | Start of round |
| `generate_phase4b2_table.py` | Create HTML | Start of round |
| `parse_phase4b2_csv.py` | Parse decisions | After human exports |
| `add_to_airtable.py` | Add new people | During execution |
| `execute_roundN_actions.py` | Execute all actions | After discussion |

---

## Success Checklist for Each Round

- [ ] Generated batch and HTML table
- [ ] Human exported CSV with decisions
- [ ] Parsed CSV, identified all custom comments
- [ ] Discussed EVERY custom comment with human
- [ ] Checked Airtable for all merge targets
- [ ] Built round-specific execution script
- [ ] Backed up database before execution
- [ ] Executed actions (merges, drops, adds)
- [ ] Verified stats (before → after)
- [ ] Committed with comprehensive message
- [ ] Reported progress to human

---

## Your Implicit Habits (Now Explicit)

1. **Always check Airtable before suggesting merges**
   - Don't assume someone is there
   - Don't assume someone ISN'T there
   - Look it up

2. **Present unclear cases as options, not declarations**
   - Bad: "I'll merge X to Y"
   - Good: "X could merge to Y (if in Airtable), or we could add X as new person. Which?"

3. **Group similar cases in discussion**
   - "I found 3 device names (all ProcessThis=YES)..."
   - More efficient than one-by-one

4. **Provide context in every question**
   - Include: Fathom name, comment, ProcessThis/Probe flags
   - Show what you've already checked
   - Explain why you're asking

5. **Document special cases for future rounds**
   - Phone number mappings
   - Hyphen handling issues
   - Organization → person patterns

---

**Last Updated:** 2025-10-20  
**For Questions:** See PHASE4B2_PROGRESS_REPORT.md for examples  
**Pattern Reference:** execute_round4-8_actions.py
