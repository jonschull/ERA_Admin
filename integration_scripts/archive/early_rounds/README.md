# Early Round Scripts (Historical Archive)

**Purpose:** Preserve the evolution of Phase 4B-2 execution scripts

---

## What's Here

These are the **early prototypes** from Rounds 1-3 of Phase 4B-2 (Oct 20, 2025).

### Files:

1. **`execute_phase4b2_actions.py`** (Round 1)
   - First attempt at generic executor
   - Hardcoded probe results
   - Direct CSV parsing
   - Basic merge/drop/add logic

2. **`execute_round2_actions.py`** (Round 2)
   - Custom merges list
   - Organization handling (Global Earth Repair, sustainavistas)
   - Still hardcoded actions

3. **`execute_round3_actions.py`** (Round 3)
   - First CSV-driven approach
   - Parse "merge with:" comments
   - More generic, less hardcoded

---

## Why They Were Replaced

**Problems with early scripts:**
- Mix of hardcoded and CSV-driven logic
- Inconsistent error handling
- No separation of concerns
- Difficult to maintain across rounds

**Evolution to current pattern (Rounds 4-8):**
- Each round = dedicated script with full logic
- Use `add_to_airtable.py` module for consistency
- Clear structure: standard merges → drops → adds → custom merges
- Comprehensive error handling and reporting
- Well-documented with comments

---

## Current Best Practice

**Don't use these!** Use the pattern from `execute_round4-8_actions.py`:

```python
#!/usr/bin/env python3
"""Execute Round N actions from CSV."""

# 1. Setup & backup
# 2. Load Airtable
# 3. Execute standard merges (from CSV)
# 4. Execute drops
# 5. Add people to Airtable (add_to_airtable module)
# 6. Execute custom merges
# 7. Handle newly added people
# 8. Commit & report stats
```

---

## Historical Value

These scripts show:
- **Iteration process** - How we refined the workflow
- **Learning curve** - What problems we encountered
- **Decision points** - Why we chose current architecture

They're preserved for:
- Understanding project evolution
- Learning from early mistakes
- Recovering old logic if needed

---

**Created:** 2025-10-20  
**Status:** ARCHIVED - Do not use in production  
**See:** `../execute_round4-8_actions.py` for current pattern
