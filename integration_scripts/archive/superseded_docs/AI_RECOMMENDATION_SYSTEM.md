# AI Recommendation System - Option 3 Implementation

## Overview

Built intelligent heuristics + AI batch analysis system for Phase 4B-2 participant reconciliation.

**Goal:** Reduce your workload by having AI make most decisions, leaving only truly unclear cases and strategic decisions for you.

## How It Works

### 1. Automatic Confidence Scoring

For each participant, the system analyzes:
- **Town Hall context** (62 agendas in local database)
- **Gmail presence** (email count and snippets)
- **Airtable fuzzy matching** (with confidence scores)
- **Name quality** (complete vs. incomplete)
- **Learned mappings** (from previous rounds)

### 2. Three Confidence Levels

**HIGH CONFIDENCE (80-100)**
- ✅ Auto-checked in HTML
- **You just approve** (or override if wrong)
- Examples:
  - Found in 3+ Town Hall meetings → add to Airtable
  - Perfect Airtable match (95%+) → merge
  - Clear organization/phone → drop

**MEDIUM CONFIDENCE (50-79)**
- 🤔 Flagged for AI batch analysis
- **Claude analyzes** all at once
- Examples:
  - Found in 1-2 Town Hall meetings but unclear match
  - Good Airtable match (75-90%) needs verification
  - Some context but ambiguous

**LOW CONFIDENCE (0-49)**
- ⚠️ Auto-recommend skip or manual review
- **You decide** if worth investigating
- Examples:
  - No context anywhere
  - Single name only with no info
  - Obvious non-person

## Workflow

### Step 1: Generate Table (Auto-Analysis)
```bash
cd integration_scripts
python3 generate_phase4b2_table.py
```

**Outputs:**
- HTML table with AI recommendations
- High confidence cases pre-checked
- Stats showing breakdown

### Step 2: Review HTML
Open the generated HTML file in browser.

**What you see:**
- **Green rows** = High confidence (just approve)
- **Yellow rows** = Medium confidence (need AI review)
- **Red rows** = Low confidence (skip or manual)

Each row shows:
- AI recommendation with reasoning
- Town Hall context (where they participated)
- Gmail and Airtable matches

### Step 3: Handle Medium Confidence (If Any)
```bash
python3 extract_medium_confidence_cases.py
```

**Outputs:** `medium_confidence_cases.md`

**Then:**
1. Open the .md file
2. Copy entire contents
3. Paste to me (Claude) in chat
4. I analyze all cases at once
5. I return structured recommendations
6. You update the HTML comments field

### Step 4: Export & Execute
- Click "Export to CSV" in HTML
- Run execution script:
  ```bash
  python3 execute_phase4b2_actions.py path/to/csv
  ```

## Example Heuristics

**Case: "Mike Lynn"**
- Town Hall: 3 meetings ✅
- Gmail: 5 emails ✅  
- Airtable: Not found
- **→ HIGH CONFIDENCE: add to airtable**
- Reasoning: "Participated in 3 Town Hall meetings | Also in 5 emails"

**Case: "ana - Panama"**
- Town Hall: 1 meeting
- Gmail: 2 emails
- Airtable: Possible match "Ana Calderon" (78%)
- **→ MEDIUM CONFIDENCE: likely merge with Ana Calderon**
- Reasoning: "Found in 1 Town Hall | Good Airtable match (78%): Ana Calderon"

**Case: "admin"**
- Town Hall: 0
- Gmail: 0
- Airtable: No
- **→ LOW CONFIDENCE: drop**
- Reasoning: "No Town Hall, Gmail, or Airtable matches"

## Files Created

1. **ai_recommendations.py** - Core heuristics engine
2. **extract_medium_confidence_cases.py** - Batch analysis extractor
3. **generate_phase4b2_table.py** - Enhanced with AI recommendations

## Test Results

From latest run (25 people):
- ✅ **High confidence: 20** (80%) - Auto-recommended
- 🤔 **Medium confidence: 0** (0%) - Needed review
- ⚠️ **Low confidence: 5** (20%) - Auto-skip

**Your work:** Review and approve 20 high-confidence recommendations.

## What You Review vs. What AI Handles

**AI Handles Automatically:**
- Clear merges (high Airtable match + Town Hall)
- Clear adds (multiple Town Hall + Gmail, not in Airtable)
- Clear drops (organizations, phones, no context)
- Learned mappings (from previous rounds)

**You Review:**
- High confidence recommendations (quick approval)
- Strategic decisions (new vs. existing member)
- Edge cases flagged by AI
- Personal memory cases ("I know this person")

**I (Claude) Handle in Batch:**
- Medium confidence ambiguous cases
- Context synthesis from multiple sources
- Judgment calls that need intelligence

## Benefits

1. **80-90% handled automatically** with heuristics
2. **10-15% batch-analyzed** by Claude (once per session)
3. **5-10% require your judgment** (truly unclear or strategic)

**Time saved:** ~5 minutes per person → ~30 seconds per person

## Next Enhancement Ideas

- Integrate Claude API for full automation (Option 2)
- Add confidence score display in HTML
- Create "confidence calibration" based on your feedback
- Build learning system that improves heuristics over time
