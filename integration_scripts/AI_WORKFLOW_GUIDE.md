# integration_scripts/AI_WORKFLOW_GUIDE.md

### 1. Overview

**For:** AI assistants stepping into Phase 4B-2 mid-stream  
**Purpose:** Make the human-AI collaboration workflow explicit  
**Audience:** A "naive AI" without conversation history

**Mental Model: What This Process Is**

**NOT traditional automation** - This is **collaborative data curation**

You are not trying to solve this alone. You are:
1. **Generating data** for human review
2. **Researching** unclear cases
3. **Discussing** ambiguous decisions
4. **Executing** approved actions safely

**Key mindset:** The human makes final decisions. You provide research, suggestions, and execution capability.

**This document contains:**
- The 6-phase collaboration cycle
- Mental states for each phase
- What to do vs what NOT to do
- Common patterns and decision trees
- Critical rules and troubleshooting

### 2. Orientation - Where to Find What

**You are at:** integration_scripts AI workflow guide (Phase 4B-2 specific)

**Use this when:**
- Resuming Phase 4B-2 collaborative review work
- Understanding the human-AI workflow
- Learning what requires human approval
- Troubleshooting workflow issues

**What you might need:**
- **Parent component** → [README.md](README.md) - integration_scripts overview
- **Phase progress** → PHASE4B2_PROGRESS_REPORT.md - 8-round analysis
- **General AI guidance** → [/AI_HANDOFF_GUIDE.md](../AI_HANDOFF_GUIDE.md) - System-wide AI workflow
- **System principles** → [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) - Overall philosophy
- **Root context** → [/CONTEXT_RECOVERY.md](../CONTEXT_RECOVERY.md) - System state

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

**General AI workflow:** See [/AI_HANDOFF_GUIDE.md](../AI_HANDOFF_GUIDE.md)

**Phase 4B-2 specific principles:**

**1. Collaborative Data Curation**
- NOT black-box automation - human-AI partnership
- AI proposes, human disposes
- Discussion before action on ambiguous cases

**2. Human Approval Required**
- Parse CSV and flag custom comments
- STOP if custom comments found
- Discuss with human before proceeding
- Execute only approved actions

**3. 6-Phase Cycle**
1. AI generates review interface
2. Human reviews & exports CSV
3. AI parses & flags issues
4. Human-AI discuss ambiguous cases
5. AI executes approved actions
6. Document results & commit

**4. Safety First**
- Backup database before modifications
- Transaction safety (rollback on error)
- Test queries before updates
- Show results, then ask for confirmation

### 4. Specialized Topics

#### The 6-Phase Collaboration Cycle

**Phase 1: AI Generates Review Interface**

*Your role:* Create sortable HTML table for human review

```bash
python3 generate_batch_data.py          # Select next 25 people
python3 generate_phase4b2_table.py      # Create HTML interface
```

*What you're doing:*
- Selecting 25 unenriched participants from Fathom database
- Fuzzy matching against Airtable people
- Creating interactive HTML with video links, Gmail research, match suggestions

*Mental state:* You're setting up the workspace. Don't make decisions yet.

**Phase 2: Human Reviews & Exports**

*Human's role:* Review your suggestions, research unclear cases, make decisions

*What they do:*
1. Open HTML in browser
2. Click video links (🎬) to verify identities
3. Use Gmail research for unknown people
4. Add comments with decisions (merge with: Name, drop, add to airtable)
5. Check/uncheck ProcessThis boxes
6. Mark Probe boxes for unclear items
7. Export to CSV

*Your role during this:* **WAIT.** Don't process anything yet.

**Phase 3: AI Parses & Flags Issues**

*Your role:* Parse CSV and identify what needs discussion

```bash
python3 parse_phase4b2_csv.py <csv_file>
```

*What to look for:*

**Standard comments (auto-processable):**
- `merge with: Name`
- `drop`
- `add to airtable`
- `ignore`

**Custom comments (need discussion):**
- Anything that doesn't match standard patterns
- Names without "merge with:" prefix
- Notes with context (e.g., "ERA Member", "Organization: X")
- ProcessThis=YES with custom comment = **REQUIRES DISCUSSION**

*Mental state:* You're a quality checker. Flag anything ambiguous.

**CRITICAL:** If `parse_phase4b2_csv.py` shows custom comments, **STOP and discuss with user**. Do not proceed to execution.

**Phase 4: Human-AI Discussion**

*Your role:* Clarify ambiguous cases collaboratively

*What happens:*
- Human explains complex cases
- You ask clarifying questions
- Together decide on actions
- You update understanding for future rounds

*Mental state:* You're learning the patterns. Edge cases refine the workflow.

**Phase 5: AI Executes Approved Actions**

*Your role:* Execute only what human approved

```bash
python3 execute_roundN_actions.py       # N = current round number
```

*What you do:*
- Backup database first
- Execute merge/drop/add actions
- Use transactions (rollback on error)
- Show results before committing

*Mental state:* You're the executor. Follow instructions precisely.

**CRITICAL:** Never execute without human confirmation after showing results.

**Phase 6: Document & Commit**

*Your role:* Update documentation and commit changes

*What to do:*
1. Update PHASE4B2_PROGRESS_REPORT.md with round results
2. Commit all changes with descriptive message
3. Push to GitHub
4. Update docs/CONTEXT_RECOVERY.md if significant change

*Mental state:* You're the scribe. Preserve context for future sessions.

#### Common Patterns & Decision Trees

**Pattern: Phone Number as Name**
- Example: "773-555-1234"
- Human adds: "merge with: John Doe"
- Action: Merge participant to John Doe in Fathom DB

**Pattern: Device Name**
- Example: "John's iPhone"
- Human adds: "merge with: John Magugu"
- Action: Merge to correct person

**Pattern: Organization Name**
- Example: "EnableCommunity"
- Human adds: "merge with: Jon Schull" (who represents org)
- Action: Merge to person, note provenance

**Pattern: Ambiguous Name**
- Example: "Ana" (could be Ana Calderon or Ana Martinez)
- Human adds: "Probe" box checked, custom comment
- Action: **STOP** - Discuss with human using Gmail research

**Pattern: Obvious Junk**
- Example: "Test Meeting", "unknown"
- Human adds: "drop"
- Action: Delete from Fathom DB

#### Critical Rules

**NEVER:**
- Execute without human approval
- Assume custom comments are standard
- Skip backup before database modifications
- Commit without testing
- Move to next phase without completing current

**ALWAYS:**
- Stop if parse_phase4b2_csv.py shows custom comments
- Show results before asking for confirmation
- Use transactions (rollback on error)
- Document in PHASE4B2_PROGRESS_REPORT.md
- Update CONTEXT_RECOVERY.md if state changed significantly

#### Troubleshooting

**"Custom comments found" - What to do?**
1. Review the comments in parse output
2. Ask human to clarify each custom comment
3. Update your understanding
4. Proceed only after human confirms actions

**"Database update failed" - Recovery:**
1. Transaction should have rolled back automatically
2. Check database integrity
3. Restore from backup if needed
4. Investigate root cause before retry

**"Unsure about action" - When in doubt:**
1. ASK the human
2. Show your reasoning
3. Propose options
4. Wait for decision

#### Success Metrics (8 Rounds Complete)

- 409 participants validated
- 58 new people added to Airtable (+10% growth)
- 198 actions executed safely
- 87% completion (1,698/1,953)
- Production-ready workflow established

#### Quick Reference

**Commands:**
```bash
# Phase 1: Generate
python3 generate_batch_data.py
python3 generate_phase4b2_table.py

# Phase 3: Parse
python3 parse_phase4b2_csv.py <csv_file>

# Phase 5: Execute
python3 execute_roundN_actions.py
```

**Files:**
- `generate_batch_data.py` - Select next 25 people
- `generate_phase4b2_table.py` - Create HTML review interface
- `parse_phase4b2_csv.py` - Parse decisions, flag custom comments
- `execute_roundN_actions.py` - Execute approved actions
- `add_to_airtable.py` - Reusable Airtable addition module
- `gmail_research.py` - Gmail context retrieval
- `PHASE4B2_PROGRESS_REPORT.md` - 8-round analysis

**Key Insight:** This workflow represents significant learning from 8 rounds. The patterns discovered (phone numbers, devices, organizations) are now codified. Future rounds should be smoother.

**Back to:** [integration_scripts/README.md](README.md) | [/README.md](../README.md)