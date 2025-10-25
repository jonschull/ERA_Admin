# integration_scripts/participant_reconciliation/ALIAS_RESOLUTION_README.md

# Fathom Alias Resolution System

### 1. Overview

**Purpose:** Context-aware participant alias resolution and database cleanup

Track context-dependent alias-to-person mappings from Fathom meetings. Enables queries like "show me all of Brian Kravitz's sessions" which automatically includes meetings where he appeared as "bk", "brian", "Brian K", etc.

**What this component does:**
- Builds alias resolution table from Phase 4B-2 decisions
- Provides command-line tools to query sessions by name or alias
- Detects and merges participant redundancies
- Maintains database quality (reduced duplicates by 77%)

**Key deliverables:**
- `fathom_alias_resolutions` table - 495 context-aware alias mappings
- `participant_meetings` view - Easy session queries
- Participant count reduced from 461 → 423 (38 duplicates merged)
- All changes backed up and reversible

### 2. Orientation - Where to Find What

**You are at:** Alias Resolution & Cleanup System

**Use this when:**
- Need to find all sessions for a participant (by any name they've used)
- Want to extract transcript excerpts for someone
- Cleaning up database redundancies
- Resolving ambiguous participant names

**What you might need:**
- **Parent** → [integration_scripts/README.md](../README.md) - Integration workflows
- **Data source** → Phase 4B-2 CSV decisions in `past_decisions/`
- **Database** → [FathomInventory/fathom_emails.db](../../FathomInventory/README.md)
- **Scripts** → build_alias_resolution_table.py, query_participant_sessions.py, detect_participant_redundancies.py, execute_redundancy_merges.py

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md)

**Alias resolution-specific:**

**1. Context Dependency**
- Same alias can map to different people in different meetings
- "bk" = Brian Kravitz in Meeting A, Bob King in Meeting B
- Never merge aliases globally - always preserve meeting context

**2. Data Safety**
- Always create timestamped backups before merges
- All operations are reversible
- Log all actions for audit trail
- Test queries before bulk operations

**3. Human Oversight**
- High-confidence merges executed automatically
- Medium-confidence cases need user verification
- Always show reasoning and evidence links

### 4. Specialized Topics

#### Usage Examples

**Find all sessions for a participant:**
```bash
python query_participant_sessions.py "Brian Kravitz"
```

**Search by alias:**
```bash
python query_participant_sessions.py "bk"
```

**Detect redundancies:**
```bash
python detect_participant_redundancies.py
# Generates HTML report with 56→13 redundancies found
```

**Execute merges:**
```bash
python execute_redundancy_merges.py
# Processes redundancy_merge_actions.csv
# Creates automatic backups
# Logs all operations
```

#### Database Schema

**fathom_alias_resolutions table:**
- `fathom_name` - What Fathom displayed (e.g. "bk")
- `meeting_url` - Which meeting (preserves context)
- `resolved_to` - Actual person (e.g. "Brian Kravitz")
- `decision_type` - "merge", "add", or "drop"
- `decision_source` - Which Phase 4B-2 batch CSV

**participant_meetings view:**
- Joins alias resolutions with calls table
- Easy queries by participant name or alias
- Returns meeting dates, titles, and how they appeared

#### Results Achieved

- **495 alias resolutions** mapped from Phase 4B-2 decisions
- **38 participant duplicates** merged (461 → 423)
- **77% reduction** in database redundancies (56 → 13)
- **Zero data loss** - all operations reversible
- **4 automatic backups** created during cleanup

#### Key Scripts

1. **build_alias_resolution_table.py** - Extract aliases from Phase 4B-2 CSVs, create database table
2. **query_participant_sessions.py** - Find sessions by name/alias with context awareness
3. **detect_participant_redundancies.py** - Systematic duplicate detection across 5 strategies
4. **execute_redundancy_merges.py** - Safe merge execution with automatic backups

**Back to:** [integration_scripts/README.md](../README.md) | [/README.md](../../README.md)