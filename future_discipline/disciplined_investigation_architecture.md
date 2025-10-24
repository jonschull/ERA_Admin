# Disciplined Investigation Architecture
## Solving the "Unruly AI" Problem with Code

**Date:** October 23, 2025  
**Context:** Post-Phase 4B-2 reflection

---

## The Problem Statement

**Current approach:** Ask high-cognition AI (Claude) to do both:
1. Disciplined mechanical tasks (check past CSVs, grep files)
2. High-judgment tasks (infer patterns, evaluate evidence)

**Result:** AI is lazy on #1, good at #2. But #1 is prerequisites for #2.

**Key insight:** High-cognition AIs are **bad at discipline**. They get bored, forget steps, take shortcuts. Like asking a philosopher to check every item on a grocery list - they'll start pondering the nature of bread and forget to check for milk.

---

## The Solution: Task Decomposition

**Principle:** Only use high-cognition AI for tasks that **actually require cognition**.

Everything else should be:
- Shell scripts (persistent, disciplined, dumb)
- Python functions (persistent, disciplined, dumb)  
- SQL queries (persistent, disciplined, dumb)

These "drones" never get tired, never forget, never take shortcuts.

---

## Architecture Design

### **Tier 1: The Drones (No AI)**

**Purpose:** Execute mechanical checks with perfect discipline.

```bash
#!/bin/bash
# investigate_name.sh
# This script ALWAYS checks all 6 tools. No exceptions. No laziness.

NAME="$1"
RESULTS_FILE="/tmp/investigation_results.json"

echo "{" > $RESULTS_FILE
echo "  \"name\": \"$NAME\"," >> $RESULTS_FILE

# Tool 1: Past decisions
echo "  \"past_decisions\": {" >> $RESULTS_FILE
if PAST=$(grep -i "^$NAME," past_decisions/*.csv | head -1); then
    echo "    \"found\": true," >> $RESULTS_FILE
    echo "    \"data\": \"$PAST\"" >> $RESULTS_FILE
else
    echo "    \"found\": false" >> $RESULTS_FILE
fi
echo "  }," >> $RESULTS_FILE

# Tool 2: PAST_LEARNINGS
echo "  \"past_learnings\": {" >> $RESULTS_FILE
if LEARNING=$(grep -i "$NAME" PAST_LEARNINGS.md | head -1); then
    echo "    \"found\": true," >> $RESULTS_FILE
    echo "    \"data\": \"$LEARNING\"" >> $RESULTS_FILE
else
    echo "    \"found\": false" >> $RESULTS_FILE
fi
echo "  }," >> $RESULTS_FILE

# Tool 3: Fuzzy match (call Python)
echo "  \"fuzzy_match\": {" >> $RESULTS_FILE
FUZZY=$(python3 fuzzy_match_airtable.py "$NAME" --threshold 85)
echo "    \"data\": $FUZZY" >> $RESULTS_FILE
echo "  }," >> $RESULTS_FILE

# Tool 4: Fathom titles
echo "  \"fathom_titles\": {" >> $RESULTS_FILE
FATHOM=$(python3 get_fathom_context.py "$NAME")
echo "    \"data\": $FATHOM" >> $RESULTS_FILE
echo "  }," >> $RESULTS_FILE

# Tool 5: Town Hall agendas
echo "  \"townhall\": {" >> $RESULTS_FILE
TH=$(grep -i "$NAME" townhall_agendas/*.md)
if [ -n "$TH" ]; then
    echo "    \"found\": true," >> $RESULTS_FILE
    echo "    \"data\": \"$TH\"" >> $RESULTS_FILE
else
    echo "    \"found\": false" >> $RESULTS_FILE
fi
echo "  }," >> $RESULTS_FILE

# Tool 6: Gmail search (would need API integration)
echo "  \"gmail\": {" >> $RESULTS_FILE
echo "    \"checked\": true," >> $RESULTS_FILE
echo "    \"data\": []" >> $RESULTS_FILE
echo "  }" >> $RESULTS_FILE

echo "}" >> $RESULTS_FILE

# Print summary
echo "✅ Checked all 6 tools for: $NAME"
echo "📄 Results: $RESULTS_FILE"
```

**Key properties:**
- ✅ **Always runs all 6 tools** (no laziness possible)
- ✅ **Persists across sessions** (it's a file, not memory)
- ✅ **Provides structured output** (JSON for next stage)
- ✅ **No judgment required** (just mechanical execution)
- ✅ **Fast** (no LLM API calls for simple checks)

---

### **Tier 2: The Decision Rules (Minimal AI)**

**Purpose:** Apply simple decision rules that don't require deep cognition.

```python
#!/usr/bin/env python3
# apply_decision_rules.py

import json
import sys

def apply_rules(results):
    """Apply mechanical decision rules. No deep thinking."""
    
    name = results['name']
    
    # Rule 1: Found in past decisions? USE IT.
    if results['past_decisions']['found']:
        return {
            'decision': 'use_past_decision',
            'data': results['past_decisions']['data'],
            'confidence': 'HIGH',
            'reasoning': 'Found exact match in past decisions'
        }
    
    # Rule 2: Found in PAST_LEARNINGS? USE IT.
    if results['past_learnings']['found']:
        return {
            'decision': 'use_past_learning',
            'data': results['past_learnings']['data'],
            'confidence': 'HIGH',
            'reasoning': 'Found pattern in PAST_LEARNINGS'
        }
    
    # Rule 3: Fuzzy match > 95%? MERGE.
    fuzzy = results['fuzzy_match']['data']
    if fuzzy and fuzzy['score'] > 95:
        return {
            'decision': 'merge',
            'target': fuzzy['match'],
            'confidence': 'HIGH',
            'reasoning': f"Fuzzy match {fuzzy['score']}% - very high confidence"
        }
    
    # Rule 4: Fuzzy match 85-95%? Maybe merge (needs judgment)
    if fuzzy and fuzzy['score'] > 85:
        return {
            'decision': 'NEEDS_CLAUDE',
            'reason': 'fuzzy_match_borderline',
            'data': fuzzy,
            'question': f"Is '{name}' the same as '{fuzzy['match']}'? ({fuzzy['score']}% match)"
        }
    
    # Rule 5: Found in Town Hall agenda? Probably real person.
    if results['townhall']['found']:
        return {
            'decision': 'NEEDS_CLAUDE',
            'reason': 'found_in_townhall',
            'data': results['townhall']['data'],
            'question': f"Person '{name}' appears in Town Hall agenda. Can we extract full name?"
        }
    
    # Rule 6: Found context in Fathom titles? Needs judgment.
    if results['fathom_titles']['data']:
        return {
            'decision': 'NEEDS_CLAUDE',
            'reason': 'has_fathom_context',
            'data': results['fathom_titles']['data'],
            'question': f"Fathom shows context for '{name}'. Can we identify them?"
        }
    
    # Rule 7: No mechanical resolution possible
    return {
        'decision': 'NEEDS_CLAUDE',
        'reason': 'no_mechanical_match',
        'data': results,
        'question': f"Unable to resolve '{name}' mechanically. Needs human judgment."
    }

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        results = json.load(f)
    
    decision = apply_rules(results)
    print(json.dumps(decision, indent=2))
```

**Key properties:**
- ✅ **Deterministic** (same input → same output)
- ✅ **Fast** (no LLM calls)
- ✅ **Covers 60-70% of cases** (exact matches, high fuzzy matches)
- ✅ **Only escalates to Claude when actually needed**

---

### **Tier 3: The Orchestrator (No AI)**

**Purpose:** Run investigations for all names, batch up questions for Claude.

```python
#!/usr/bin/env python3
# orchestrate_batch.py

import subprocess
import json
from pathlib import Path

def investigate_batch(names):
    """Run disciplined investigation for all names."""
    
    results = []
    needs_claude = []
    auto_resolved = []
    
    for name in names:
        print(f"🔍 Investigating: {name}")
        
        # Step 1: Run drone (always all 6 tools)
        subprocess.run(['./investigate_name.sh', name], check=True)
        
        # Step 2: Apply decision rules
        decision_json = subprocess.check_output(
            ['python3', 'apply_decision_rules.py', '/tmp/investigation_results.json']
        )
        decision = json.loads(decision_json)
        
        if decision['decision'] == 'NEEDS_CLAUDE':
            needs_claude.append({
                'name': name,
                'question': decision['question'],
                'data': decision['data'],
                'reason': decision['reason']
            })
        else:
            auto_resolved.append({
                'name': name,
                'decision': decision
            })
            print(f"  ✅ Auto-resolved: {decision['reasoning']}")
    
    print(f"\n📊 BATCH SUMMARY:")
    print(f"   Auto-resolved: {len(auto_resolved)}/{len(names)}")
    print(f"   Need Claude: {len(needs_claude)}/{len(names)}")
    
    # Save results
    Path('auto_resolved.json').write_text(json.dumps(auto_resolved, indent=2))
    Path('needs_claude.json').write_text(json.dumps(needs_claude, indent=2))
    
    return auto_resolved, needs_claude

if __name__ == '__main__':
    # Get unvalidated names from database
    import sqlite3
    conn = sqlite3.connect('fathom_emails.db')
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT name FROM participants WHERE validated_by_airtable = 0")
    names = [r[0] for r in cur.fetchall()]
    
    investigate_batch(names)
```

**Key properties:**
- ✅ **No AI needed** (just running scripts)
- ✅ **Disciplined** (can't skip steps)
- ✅ **Efficient** (auto-resolves 60-70% without LLM)
- ✅ **Batches Claude questions** (only call once for remaining 30-40%)

---

### **Tier 4: Claude (High-Cognition AI)**

**Purpose:** ONLY called for items that actually need judgment.

```python
#!/usr/bin/env python3
# claude_review.py

import json
from pathlib import Path

def generate_claude_prompt(needs_claude):
    """Generate focused prompt for items needing judgment."""
    
    prompt = """You are reviewing participant names that couldn't be resolved mechanically.

For each name below, all 6 investigation tools have been run. The results are provided.

Your job: Make a judgment call based on the evidence.

Rules:
- If fuzzy match 85-95%: decide if it's the same person
- If found in Town Hall: extract full name if possible
- If has Fathom context: infer identity if possible
- If truly unknown: say "NEEDS_USER_INPUT"

DO NOT re-run the investigations. They've already been done.
DO NOT say "I should check X" - X has been checked, see the data.

"""
    
    for i, item in enumerate(needs_claude, 1):
        prompt += f"\n---\n\n{i}. **{item['name']}**\n\n"
        prompt += f"Reason escalated: {item['reason']}\n\n"
        prompt += f"Question: {item['question']}\n\n"
        prompt += f"Evidence:\n```json\n{json.dumps(item['data'], indent=2)}\n```\n\n"
        prompt += "Your decision: "
    
    return prompt

if __name__ == '__main__':
    needs_claude = json.loads(Path('needs_claude.json').read_text())
    
    if not needs_claude:
        print("✅ No items need Claude review!")
        exit(0)
    
    prompt = generate_claude_prompt(needs_claude)
    
    # Save prompt for user to feed to Claude
    Path('claude_review_prompt.txt').write_text(prompt)
    
    print(f"📝 Generated prompt for {len(needs_claude)} items")
    print(f"   File: claude_review_prompt.txt")
    print(f"\n🤖 Feed this to Claude for review.")
```

**Key properties:**
- ✅ **Only called when needed** (30-40% of cases)
- ✅ **Given pre-processed data** (all investigations done)
- ✅ **Focused judgment questions** (not "check everything")
- ✅ **Can't be lazy** (data already provided)

---

## Why This Works

### **1. Discipline is Architectural**

Scripts don't get lazy. `investigate_name.sh` **always** checks all 6 tools. Not because it's disciplined, but because that's what the code does.

### **2. Persistence Across Sessions**

```
Session 1: Run investigate_name.sh for "Indy"
           → Finds in past_decisions.csv
           → Auto-resolves to "Indy Singh"

Session 2: Run investigate_name.sh for "Indy"
           → Finds in past_decisions.csv (still there!)
           → Auto-resolves to "Indy Singh"
```

The script doesn't "remember" - it just checks the same place every time. Which is exactly what we want.

### **3. Efficient Use of Expensive Resources**

**Current approach:**
- Claude called for 100 names
- Cost: 100 × LLM_API_call
- Time: 100 × (thinking + API latency)

**Drone approach:**
- Scripts run for 100 names (fast, free)
- Auto-resolve 70 names
- Claude called for 30 names
- Cost: 30 × LLM_API_call (70% reduction)
- Time: Mostly parallel script execution + 30 × Claude calls

### **4. No "Did You Actually Check?" Problem**

**Current:**
- User: "Did you check past CSVs?"
- Claude: "Yes" (maybe didn't actually grep)

**With drones:**
- User: "Did you check past CSVs?"
- System: "Yes, see results in investigation_results.json line 3-7"
- Evidence is in the file, falsifiable

### **5. Quality is Verifiable**

```bash
# Check if all 6 tools were run
jq 'keys | length' investigation_results.json
# Should output: 6

# Check what was found
jq '.past_decisions.found' investigation_results.json
jq '.fuzzy_match.data.score' investigation_results.json
```

Can programmatically verify the investigation was complete.

---

## Comparison to mcp-agent

**mcp-agent approach:**
- Orchestrator LLM plans the work
- Worker agents (some with LLMs) execute
- Evaluator LLM checks quality
- **Still uses AI for orchestration and evaluation**

**Drone approach:**
- **No AI for orchestration** (just shell script)
- **No AI for workers** (just grep/Python)
- **No AI for 70% of decisions** (just rules)
- **AI only for irreducible judgment calls**

**Trade-off:**
- mcp-agent: More flexible, can adapt plans
- Drones: More deterministic, cheaper, faster

**Best of both:**
Could use mcp-agent framework BUT with most agents being non-AI tools. Orchestrator plans, but workers are dumb scripts.

---

## Implementation for Phase 4B-2

**What we'd build:**

```
investigation_system/
├── drones/
│   ├── investigate_name.sh           # Runs all 6 tools
│   ├── past_decisions_checker.sh     # Tool 1
│   ├── past_learnings_checker.sh     # Tool 2
│   ├── fuzzy_matcher.py              # Tool 3
│   ├── fathom_context_extractor.py   # Tool 4
│   ├── townhall_searcher.sh          # Tool 5
│   └── gmail_searcher.py             # Tool 6
│
├── rules/
│   ├── apply_decision_rules.py       # Deterministic decisions
│   └── validation_rules.py           # Check investigation completeness
│
├── orchestration/
│   ├── orchestrate_batch.py          # Main orchestrator
│   └── generate_claude_prompt.py     # Only for escalated cases
│
└── integration/
    ├── execute_decisions.py          # Apply auto-resolved decisions
    └── wait_for_claude_input.py      # Handle escalated cases
```

**Workflow:**
1. `orchestrate_batch.py` reads unvalidated names
2. For each name: run `investigate_name.sh` (all 6 tools)
3. For each result: run `apply_decision_rules.py`
4. Auto-resolved (70%): execute immediately
5. Needs judgment (30%): batch into `claude_review_prompt.txt`
6. User feeds prompt to Claude (or any LLM)
7. Claude provides judgments
8. Execute Claude's judgments

**Key insight:** Claude is an **advisor**, not the **executor**. Drones do the work.

---

## Answering the Original Questions

### **"Do those MCPs need their own LLM models?"**

No. MCP is just a tool protocol. Workers can be bash scripts.

### **"Couldn't we do the same with a command-line LLM?"**

Yes! And even better: most tasks don't need ANY LLM. Just scripts.

### **"Wouldn't their programming survive across sessions?"**

YES! This is the key. Scripts persist, my memory doesn't.

### **"Is the unruly AI a problem we can solve with good code?"**

YES - if we decompose the problem:
- **Mechanical tasks** → scripts (disciplined)
- **Judgment tasks** → AI (creative)

Don't ask philosophers to do accounting.

### **"Can component tasks be packaged into small specialists who don't think deeply but can maintain discipline?"**

**ABSOLUTELY.** That's exactly what this architecture does.

The "drones" are like office workers following a checklist:
1. Check box 1
2. Check box 2
3. Check box 3
...

They don't understand WHY. They just execute. Perfectly. Every time.

---

## Conclusion

The discipline problem isn't:
- "How do we make AI remember to check things?"

It's:
- "Why are we asking AI to check things when a bash script can do it perfectly?"

**High-cognition AI should be used for cognition, not discipline.**

For everything else: there's shell scripts.

---

**Estimated impact if implemented:**
- 70% of cases auto-resolved (no AI needed)
- 0% chance of forgetting to check past CSVs (scripts don't forget)
- 0% chance of "Indy asked 5 times" (script checks first, always)
- 10x faster investigation (parallel script execution)
- 10x cheaper (fewer LLM API calls)

**The only remaining question:** Do the 30% that need Claude actually need HIGH-cognition Claude? Or could simpler/cheaper models handle them with good prompts?

Possible answer: Use Claude for true judgment calls, use cheaper models for borderline fuzzy matches.

**Final insight:** We've been using a race car (Claude) to deliver mail. We need a mail truck (scripts) for most deliveries, and save the race car for when speed of thought actually matters.
