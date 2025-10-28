# Airtable Duplicate Records

**Date:** October 26, 2025  
**Issue:** 8 names with duplicate Airtable records (16 records total)

---

## Duplicates Found

### 1. Ana Beatriz Freitas (2 records)
- `recGFs9XTcC2jnIDh`
- `recLt3XCk52TZwWk4`

### 2. Climbien Babungire (2 records)
- `recdnTAG6vu4mMCLX`
- `recsNjlDwH3PKtlg3`

### 3. Greg Jones (2 records)
- `recRSD92aDqhNH9Y6`
- `recXLNG7IZ4a9fQWt`

### 4. John Hepworth (2 records)
- `recQo8zLzTjUjgZx9`
- `reczbnaxdDvrIyUSX`

### 5. Marie Pierre Bilodeau (2 records)
- `rec8ZOirE8XY3mOFg`
- `recFOUrSaMCV5Xpbv`

### 6. Micah Opondo (2 records)
- `recX1da6YJtWDksqa`
- `reckcK4G2iaCOaSya`

### 7. Pacifique Ndayishimiye (2 records)
- `recBIwdENBslbOPto`
- `recCJLiqFSEsXtcTm`

### 8. Philip Bogdonoff (2 records)
- `recmYdaawIXc693As`
- `recn4KBLBzYkWx7cO`

---

## Recommended Actions

### Investigate Each Duplicate:
1. Compare records to determine if they're:
   - **Same person** → Merge (keep one, delete other)
   - **Different people** → Rename to distinguish
   
2. Check for data differences:
   - Different emails?
   - Different affiliated orgs?
   - Different bio content?
   - Different era_member flags?

### Merge Strategy (if same person):
1. Identify which record has more complete data
2. Merge data into primary record
3. Update any external references to use primary ID
4. Delete duplicate record

---

## Impact on Current Work

**Priority:** MEDIUM - Not blocking bio generation for priority 1 members

**But affects:**
- "Jon Should publish" flagging (may flag duplicates)
- Database/Airtable reconciliation
- Member count accuracy

---

## Next Steps

1. User reviews each duplicate pair
2. Confirms merge or rename strategy
3. We execute corrections
4. Re-run priority list generation to get clean data

**DO NOT auto-fix** - Need user review first.
