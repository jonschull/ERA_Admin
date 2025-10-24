# Intelligent AI Assistant Workflow

## The Right Way: AI First, Human Review

### Old Way (WRONG)
1. Script makes crude heuristic guesses
2. Human fixes all the mistakes
3. AI assists with unclear cases

### New Way (RIGHT)
1. Script gathers ALL the data
2. **AI (Claude) reads everything and makes intelligent decisions**
3. Human reviews AI's decisions (only overrides ~5-10%)

---

## Workflow

### Step 1: Generate Data (Script)
```bash
cd integration_scripts
python3 generate_phase4b2_table.py
```

**What it does:** Collects raw data (Town Hall, Gmail, Airtable)
**What it doesn't do:** Make decisions (that's Claude's job)

### Step 2: Prepare for AI Analysis (Script)
```bash
python3 prepare_for_ai_analysis.py
```

**What it does:**
- Searches Town Hall agendas → gets actual snippets
- Fetches Gmail → gets actual email subjects/content
- Formats everything readable for Claude
- Creates `ai_analysis_input.md`

**Takes:** 2-3 minutes (one Gmail search per person)

### Step 3: AI Analysis (Claude)
1. Open `ai_analysis_input.md`
2. Copy entire contents
3. Paste to Claude in chat
4. Claude reads ALL the context and makes decisions
5. Save Claude's response to `claude_decisions.txt`

**What Claude does:**
- **Reads** actual Town Hall snippets (not just counts)
- **Reads** actual Gmail content (not just counts)
- **Thinks** about patterns (number variants, name spellings)
- **Uses context** (Jon Schull = you, common patterns)
- **Makes confident decisions** with brief reasoning

**Example decision:**
```
CASE 41: Katharine King
DECISION: add to airtable
REASON: Found in 2 Town Hall meetings (clear ERA participant). No Airtable match yet.
VALIDATE: [Town Hall links]
```

### Step 4: Apply AI Decisions (Script)
```bash
python3 apply_ai_decisions.py approvals.csv claude_decisions.txt
```

**What it does:**
- Parses Claude's decisions
- Updates CSV with Claude's recommendations
- Auto-checks "ProcessThis" for non-drop cases
- Creates `approvals_WITH_AI_DECISIONS.csv`

### Step 5: Human Review (You)
Open the CSV with AI decisions:
- **Green/checked** = Claude recommends processing
- **Red/unchecked** = Claude recommends dropping

**Your job:**
- Spot-check a few (validate Claude's reasoning)
- Override any you disagree with
- Approve the rest

**Expected:** 90-95% of Claude's decisions are correct

### Step 6: Execute (Script)
```bash
python3 execute_phase4b2_actions.py approvals_WITH_AI_DECISIONS.csv
```

---

## What Claude Actually Reads

### Example: "Katharine King"

**OLD (heuristics):**
- Town Hall count: 2
- Gmail count: 0
- → "unclear" (cowardly)

**NEW (intelligent):**
- **Town Hall snippets:**
  - 2024-03-15: "Jon Schull, **Katharine King**, Philip Bogdonoff attended..."
  - 2024-04-20: "...discussion led by **Katharine King** on regenerative ag..."
- **Gmail:** (checks actual emails, not just count)
- **Decision:** "add to airtable" 
- **Reason:** "Found in 2 Town Hall meetings (clear ERA participant). No Airtable match yet."

---

## Key Principles

### Claude Should Know
1. **Jon Schull = you** (all variants merge to "Jon Schull")
2. **Number variants = same person** ("Joshua (2)" = "Joshua (4)")
3. **3+ Town Halls = obviously add** (they're ERA participants)
4. **80%+ Airtable match = obviously merge** (not "unclear")
5. **Device names = drop** ("iPhone", "Galaxy")

### Claude Should Read
1. **Actual Town Hall snippets** (who they talked to, what they discussed)
2. **Actual Gmail subjects** (meeting invites, collaborations)
3. **Context from learned mappings** (patterns from previous rounds)

### Claude Should Be
1. **Confident** (not cowardly with "unclear")
2. **Consistent** (same logic for similar cases)
3. **Intelligent** (use knowledge + context, not just rules)

---

## Time Savings

**Old workflow:**
- Generate table: 2 min
- You manually decide 50 cases: 5 min per case = 250 min total
- **Total: 252 minutes (4+ hours)**

**New workflow:**
- Generate data: 2 min
- Prepare for AI: 3 min
- Claude analyzes 50 cases: 5 min total (batch)
- You review Claude's work: 15 min
- **Total: 25 minutes**

**Savings: 90% reduction**

---

## Next Enhancement

If this works well, we can automate Steps 2-4:
- Script calls Claude API directly
- No copy/paste needed
- Fully automated intelligent analysis
- Human just reviews final decisions

**Cost:** ~$0.02-0.05 per participant via API
**Benefit:** Zero manual steps, instant analysis
