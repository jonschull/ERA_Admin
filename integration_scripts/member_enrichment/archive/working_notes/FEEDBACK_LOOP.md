# Bio Feedback Loop: AI Learning from Human Edits

**Purpose:** Enable Claude to learn from Jon's editorial judgment through systematic comparison.

---

## Workflow

### Step 1: AI Generates Initial Bios

Claude creates: `batch4_review.AI.md`

Contains:
- All proposed bios
- Char counts
- Data concerns
- STATUS: PENDING for all

### Step 2: Human Reviews and Edits

Jon:
1. Copies `batch4_review.AI.md` → `batch4_review.JS.md`
2. Edits bios directly in JS file
3. Changes STATUS to APPROVED/NEEDS_REVISION/SKIP
4. Adds comments as needed
5. Saves when done

### Step 3: AI Diffs and Learns

Jon tells Claude: "Review batch 4 feedback"

Claude:
1. Runs diff between `.AI.md` and `.JS.md`
2. For each bio, identifies:
   - **Structural changes** (sentences removed/added)
   - **Word choice changes** (leads → promotes, etc.)
   - **Tone adjustments** (removed posturing, added specificity)
   - **Factual corrections** (wrong info fixed)
3. Discusses patterns:
   - "You changed 'leads' to 'promotes' 3 times - prefer softer verbs?"
   - "You removed 'Introduced to ERA by...' - too much process detail?"
   - "You bracketed one sentence - mark for removal?"
4. Asks clarifying questions:
   - "Is this pattern or case-specific?"
   - "Should I apply this rule going forward?"
5. Updates learning documents:
   - `BIO_WRITING_PATTERNS.md` - Accumulates rules
   - `CONTEXT_RECOVERY.md` - Updates standards

### Step 4: Apply Learning to Next Batch

Next batch uses patterns from previous feedback.

---

## File Naming Convention

```
batch4_review.AI.md     ← Claude's initial output
batch4_review.JS.md     ← Jon's edited version
batch4_review.FINAL.md  ← After discussion, approved version
```

**Never overwrite AI or JS versions** - preserve for diff comparison.

---

## Diff Analysis Script

```bash
# Quick diff summary
diff -u batch4_review.AI.md batch4_review.JS.md > batch4_changes.diff

# Or line-by-line analysis
python3 analyze_bio_feedback.py batch4_review.AI.md batch4_review.JS.md
```

---

## Learning Categories

When analyzing diffs, Claude looks for:

### 1. **Verb Choice**
- AI: "leads initiatives"
- JS: "promotes initiatives"
- **Learning:** "leads" implies authority we can't verify, "promotes" is factual

### 2. **Sentence Structure**
- AI: Long compound sentences
- JS: Split into shorter statements
- **Learning:** Prefer clarity over eloquence

### 3. **Claims vs Facts**
- AI: "one of ERA's most engaged members"
- JS: [deleted]
- **Learning:** Don't make engagement claims without verification

### 4. **Process Details**
- AI: "Introduced to ERA by Russ Spear in May 2024"
- JS: [bracketed or removed]
- **Learning:** Focus on work, not how they got here?

### 5. **Mission Statements**
- AI: "demonstrating that restoration requires..."
- JS: [deleted]
- **Learning:** No ERA posturing, let work speak

### 6. **Puffed Language**
- AI: "navigate complex institutional landscapes"
- JS: [deleted]
- **Learning:** Simple, direct language only

---

## Discussion Template

After diff analysis, Claude presents:

```markdown
## BATCH 4 FEEDBACK ANALYSIS

### Changes Detected: 5 bios edited

---

### Alex Carlin (Bio #1)

**Change:** "leads" → "promotes"
**Pattern:** Verb softening
**Question:** Should I avoid "leads" when we can't verify leadership role?

**Change:** Bracketed "Introduced to ERA by Russ Spear..."
**Pattern:** Process detail removal
**Question:** Should I skip "how they joined ERA" details in general?

---

### Eduardo Marino (Bio #4)

**Change:** Removed entire second paragraph
**Pattern:** Confabulation caught
**Learning:** I had inferred engagement level without reading transcripts
**Applied:** Only use verified presentation content

---

### Patterns Observed Across All Edits:

1. **Verb softening** - "leads" → "promotes" (3x)
2. **Process details** - Bracketed/removed (2x)
3. **Removed posturing** - Deleted mission statement language (1x)

### Questions for Jon:

1. Should I always use "promotes/works on" instead of "leads" unless verified?
2. Should I skip "introduced by X" and "attended Y date" details?
3. Are brackets your mark for "consider removing" or immediate delete?

### Proposed Updates to Standards:

- ✅ Prefer: promotes, works on, focuses on
- ❌ Avoid: leads, spearheads, pioneers (unless verified)
- ⚠️ Process details: Skip unless central to story
```

---

## Implementation

**Script to create:**

```python
#!/usr/bin/env python3
"""
analyze_bio_feedback.py

Compare .AI.md and .JS.md versions, extract editorial patterns.
"""

import difflib
import re
from pathlib import Path

def analyze_feedback(ai_file, js_file):
    """Generate structured feedback analysis."""
    
    with open(ai_file) as f:
        ai_content = f.read()
    with open(js_file) as f:
        js_content = f.read()
    
    # Split into bio sections
    ai_bios = extract_bios(ai_content)
    js_bios = extract_bios(js_content)
    
    patterns = {
        'verb_changes': [],
        'deletions': [],
        'additions': [],
        'structural': []
    }
    
    for name in ai_bios:
        if name in js_bios:
            changes = compare_bios(ai_bios[name], js_bios[name])
            categorize_changes(changes, patterns)
    
    print_analysis(patterns)

def extract_bios(content):
    """Extract individual bio sections by name."""
    # Parse markdown sections
    pass

def compare_bios(ai_bio, js_bio):
    """Detailed diff of single bio."""
    pass

def categorize_changes(changes, patterns):
    """Identify change patterns."""
    pass

def print_analysis(patterns):
    """Generate discussion markdown."""
    pass

if __name__ == "__main__":
    import sys
    analyze_feedback(sys.argv[1], sys.argv[2])
```

---

## Benefits

1. **Systematic learning** - Every edit becomes training data
2. **Pattern recognition** - Identify recurring corrections
3. **Explicit standards** - Turn implicit judgment into explicit rules
4. **Faster improvement** - Apply patterns immediately to next batch
5. **Preserved history** - Never lose original AI output or human edits

---

## Integration with Existing Workflow

Current: 
```
generate batch → human reviews → process feedback
```

New:
```
generate batch.AI.md → human edits → saves batch.JS.md → 
  AI diffs → discussion → updates standards → next batch applies learning
```

---

## First Test: Batch 4

Let's use the current situation:
- I rename current file to `batch4_review.AI.md`
- You edit and save as `batch4_review.JS.md`
- I analyze diff and discuss
- We document patterns for batch 5

Ready to implement?
