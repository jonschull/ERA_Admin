# Members Ready for "Jon Should publish" Flag

**Date:** October 26, 2025  
**Status:** SAFE TO FLAG (after resolving priority 0 diagnostic)

---

## Current Situation

**Total unpublished ERA members found:** 66  
**Minus priority 0 (uncertain):** -50  
**Minus conflation (Craig McNamara):** -1  
**Clean list:** **15 members**

---

## 15 Members - SAFE TO FLAG

These are confirmed ERA members (priority 1 = attended Town Halls) who are unpublished:

1. **Benjamin Bisetsa** - `recX2Nb4HlxWes39p`
2. **Brendan McNamara** - `recRsz61TznaNVvB3` ← (Part of Craig conflation)
3. **Brent Constantz** - `recDgMDvRyObZ7zVy`
4. **Brian Krawitz** - `recuLLZtlrJkkVy6N`
5. **Bulonza jerson** - `recOzJabfDph8Qmcr`
6. **Carol Manetta** - `recPJJSejpAHNQg4K`
7. **Chauncey Bell** - `recqXvu8bRZrEJUYw`
8. **Chris pieper** - `recVPFOyDjpMpm1T4`
9. **Christina Engelsgaard** - `recsS2wW3VUWb4444`
10. **Christine Freeland** - `rec3UYlE8mt42V65a`
11. **Climbien Babungire** - `recsNjlDwH3PKtlg3` ← (Has duplicate)
12. **Daniel Fleetwood** - `rec1cGNko6jemycbu`
13. **David Gold** - `recmcs7dkxGXebE2Y`
14. **David Harper** - `reczTmOAOuR1N18s1`
15. **David maher** - `rec66aVpCukqpYans`

Plus **Mahangi Munanse** - `recjmTo1C7JGqdZYs` (skipped in Batch 5 for insufficient data, but is priority 1)

---

## 50 Priority 0 Members - UNCERTAIN

**DO NOT FLAG YET** - Need to resolve:
- Spelling mismatches (Abby Karparsi vs Karparis)
- Verify real membership status
- Check if they attended Town Halls under different names

See: `PRIORITY_0_DIAGNOSTIC.md`

---

## 8 Duplicate Records - NEED CLEANUP

**DO NOT FLAG YET** - Need to merge/resolve:
- Ana Beatriz Freitas (2 records)
- Climbien Babungire (2 records) ← Also in safe list above
- Greg Jones (2 records)
- John Hepworth (2 records)
- Marie Pierre Bilodeau (2 records)
- Micah Opondo (2 records)
- Pacifique Ndayishimiye (2 records)
- Philip Bogdonoff (2 records)

See: `AIRTABLE_DUPLICATES.md`

---

## Recommended Workflow

### Option A: Flag Only the Safe 15
- Skip all uncertain priority 0 members
- Skip duplicates
- Flag only confirmed priority 1 members

### Option B: Resolve Issues First, Then Flag All
1. Resolve priority 0 diagnostic (spelling mismatches)
2. Merge/cleanup duplicates
3. Re-run priority list generation
4. Flag all confirmed unpublished ERA members

---

## Impact on Airtable Update Script

**Current script will flag:** ~66 members  
**Should flag:** Only 15-16 confirmed members (until priority 0 resolved)

**Recommendation:** Update script to skip priority 0 members until diagnostic is resolved.

---

## Files Created

1. `PRIORITY_0_DIAGNOSTIC.md` - 50 uncertain members
2. `AIRTABLE_DUPLICATES.md` - 8 duplicate names
3. `READY_FOR_PUBLISH_FLAG.md` - This file (safe list)

**All waiting for user review - NO AUTO-FIXES applied.**
