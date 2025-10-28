# Priority 0 Diagnostic Report

**Date:** October 26, 2025  
**Issue:** 50 people marked as "era Member = True" but have priority 0 (no Town Hall attendance found)

---

## Problem Identified

**Root Cause:** Spelling mismatches between Airtable and Fathom database

**Example:**
- **Airtable:** `Abby Karparsi`
- **Database:** `Abby Karparis`
- **Result:** Script couldn't find her Town Hall attendance → priority 0
- **Reality:** She DID attend Town Halls (found in transcripts)

---

## The 50 "Priority 0" ERA Members

These people are marked as `era Member = True` in Airtable but the script found no Town Hall attendance:

### Possible Reasons:
1. **Spelling mismatch** - Name in Airtable ≠ name in database
2. **Real member** - Joined but hasn't attended Town Halls yet  
3. **False positive** - Incorrectly marked as ERA member

---

## Full List (sorted alphabetically):

1. Abby Abrahamson
2. Abby Karparsi ← **CONFIRMED MISMATCH** (Database: "Abby Karparis")
3. Avery Correia
4. Campbell Webb
5. Candrace Ducheneaux
6. Ceal Smith
7. Celia Francis
8. Dan Gerry
9. Daniel Robin
10. Daniel Valdiviezo
11. Derek Wilson
12. Edward Muller ← **Attended Town Hall** (found in transcript)
13. Emmanuel Renegade
14. Finian Makepeace
15. Gayathri Ilango
16. Ilse Koehler-Rollefson
17. Jacobus Van Der Bank
18. Jim Laurie
19. Joao Lopes
20. Joe Morris
21. John Polhaus
22. John Roulac
23. John Wick
24. Karol Mieczkin
25. Katie Chess
26. Leonie Van Der Steen
27. Lisa Smith
28. Mark Fredericks
29. Martin Peck
30. Mary Ann Edwards
31. Matthijis Bouw
32. Micah Opondo
33. Michael Vermeer
34. Mick Lorkins
35. Monifa Afina
36. Mutasa Brian
37. Méthode Dukore
38. Natalie Novoselova
39. Nathalia Rio Preto
40. Ngwana Henry
41. Norma Carty
42. Pamela Berstler
43. Patrick Worms,
44. Penny Lewise
45. Tanner Millen
46. Twizeyimana Innocent
47. Vivian Kanchian
48. Walter Jehne ← **Well-known soil scientist** (likely real member)
49. aparna.dasaraju ← **Username format** (likely spelling issue)
50. chris.searles ← **Username format** (likely spelling issue)

---

## Next Steps (DON'T FIX YET)

### 1. **Investigate Spelling Mismatches**
Run fuzzy matching between Airtable names and database names to find:
- Similar names with typos
- Different name formats (FirstLast vs First Last)
- Username formats vs. real names

### 2. **Verify Real Members**
Check which of these:
- Attended Town Halls (search transcripts)
- Are known in the restoration community
- Should legitimately be ERA members

### 3. **Identify False Positives**
Determine which were incorrectly marked as `era Member = True`

### 4. **Create Correction Plan**
Once we understand the categories, create fixes for:
- Database name corrections
- Airtable name corrections  
- Incorrect era_member flags

---

## Questions for User

1. **Are contacts ever marked as "era Member = True"?**
   - Or should that ONLY be for people who attended Town Halls?

2. **Walter Jehne, Edward Muller, etc. - are these real members?**
   - They're marked as members in Airtable
   - But script found no Town Hall attendance

3. **Should we run fuzzy matching to find spelling mismatches?**
   - Abby Karparsi ↔ Abby Karparis
   - aparna.dasaraju ↔ Aparna Dasaraju?
   - chris.searles ↔ Chris Searles?

---

## Impact on "Jon Should publish" Flag

**Current plan:** Flag all unpublished ERA members for publishing

**Problem:** We don't know which priority 0 people should be flagged:
- If they're real members → Yes, flag them
- If spelling mismatches → Fix names first, then flag
- If false positives → Remove era_member flag, don't flag for publish

**Recommendation:** Resolve priority 0 diagnostic BEFORE running the Airtable update script.
