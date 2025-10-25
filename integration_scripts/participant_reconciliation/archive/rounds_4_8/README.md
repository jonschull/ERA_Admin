# Rounds 4-8 Execution Scripts (Archive)

**Purpose:** Historical record of Phase 4B-2 Round 4-8 execution scripts

---

## What's Here

These are the **round-specific executors** from Rounds 4-8 of Phase 4B-2 (Oct 20, 2025).

### Files:

1. **`execute_round4_actions.py`** - Round 4 (25 people)
2. **`execute_round5_actions.py`** - Round 5 (25 people)
3. **`execute_round6_actions.py`** - Round 6 (25 people)
4. **`execute_round7_actions.py`** - Round 7 (25 people)
5. **`execute_round8_actions.py`** - Round 8 (25 people)

**Total:** 125 people processed, 198 actions executed

---

## Why Archived

These scripts served their purpose for their specific rounds. Each contains:
- Hardcoded lists of people to add
- Hardcoded merge decisions
- Round-specific custom logic

**For Round 9+:** Copy `execute_round8_actions.py` as template and modify for new round.

---

## Pattern Reference

These scripts follow the production pattern:

```python
#!/usr/bin/env python3
"""Execute Round N actions from CSV."""

# 1. Backup database
# 2. Load Airtable
# 3. Execute standard merges (from CSV)
# 4. Execute drops
# 5. Add people to Airtable (add_to_airtable module)
# 6. Execute custom merges (device names, orgs, etc.)
# 7. Handle newly added people
# 8. Commit & report stats
```

**See:** `../../AI_WORKFLOW_GUIDE.md` for complete workflow

---

## Results Summary

| Round | People | Actions | Added to Airtable | Validated |
|-------|--------|---------|-------------------|-----------|
| 4 | 25 | 24 | 4 | +46 |
| 5 | 25 | 27 | 5 | +37 |
| 6 | 25 | 24 | 5 | +46 |
| 7 | 25 | 25 | 8 | +29 |
| 8 | 25 | 25 | 8 | +21 |
| **Total** | **125** | **125** | **30** | **+179** |

---

**Created:** 2025-10-20  
**Status:** ARCHIVED - Reference only  
**See:** `../PHASE4B2_PROGRESS_REPORT.md` for full analysis
