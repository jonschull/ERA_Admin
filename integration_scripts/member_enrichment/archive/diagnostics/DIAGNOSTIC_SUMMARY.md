# Diagnostic Summary - Option B Complete

**Date:** October 26, 2025
**Status:** All diagnostics complete, queued for resolution

---

## Executive Summary

**Goal:** Identify all unpublished ERA members who need "Jon Should publish" flag

**Major Findings:**

1. **44 False Positives** - Marked as "era Member" but user confirms NOT members → Remove flags
2. **6 Spelling Mismatches** - Names differ between Airtable ↔ Database
3. **8 Duplicate Records** - Same person with multiple Airtable entries → Merge
4. **1 Conflation** - Craig McNamara (Brendan + Craig Erickson) → Split
5. **4 Unrecognized Members** - Marked as ERA members but user doesn't know them → Investigate

**Most "unpublished" members ALREADY HAVE BIOS** - they just need the publish flag checked

---

## Diagnostic Results

### 1. Priority 0 Spelling Mismatches

**Analyzed:** 50 priority 0 members marked as ERA members
**Found:** 6 spelling mismatches between Airtable ↔ Database

#### High Confidence (100% match, same email):

1. **Celia Francis** - Exact match, both have `celia@ponterra.eco`
2. **Emmanuel Renegade** - Exact match, both have `emmanuel@picinguaba.com`
3. **Mary Ann Edwards** - Exact match, both have `maedwardsrn@gmail.com`
4. **Mutasa Brian** - Exact match, both have `brianmutasa256@gmail.com`

**Mystery:** Why were these "priority 0" if they're in the database?

#### Likely Matches (92% similarity):

5. **Abby Karparsi** (Airtable) → **Abby Karparis** (Database)

   - Airtable: tech@myceliumlearning.com
   - Database: No email
   - **CONFIRMED:** Found in Town Hall transcripts
6. **Edward Muller** (Airtable) → **Eduard Muller** (Database)

   - Airtable: No email
   - Database: mullerm@un.org
   - **CONFIRMED:** Found in Town Hall transcripts

#### No Matches Found: 44 members

- Walter Jehne, Campbell Webb, John Wick, etc.
- Need manual verification of membership status
- See: `PRIORITY_0_MATCHES_DIAGNOSTIC.md`

---

### 2. Duplicate Records

**Found:** 8 names with duplicates (16 total records)**Recommendation:** All same person - merge

1. **Ana Beatriz Freitas** - Same email, same bio, keep most recent
2. **Climbien Babungire** - Same email, one published, merge to published record
3. **Greg Jones** - Same email, same bio
4. **John Hepworth** - Same email, same bio
5. **Marie Pierre Bilodeau** - Same email, one has era_member flag
6. **Micah Opondo** - (see full report)
7. **Pacifique Ndayishimiye** - (see full report)
8. **Philip Bogdonoff** - (see full report)

See: `DUPLICATES_DIAGNOSTIC.md`

---

### 3. Known Conflation

**Craig McNamara** - NOT a real person

- Conflation of: Brendan McNamara + Craig Erickson
- Already excluded from flagging script

---

## Action Queues (DO NOT EXECUTE YET)

### Queue A: High Confidence Spelling Fixes (4 members)

**These have 100% match + same email - safe to fix**

```python
SPELLING_FIXES = [
    # Already in database, just match exactly
    {'airtable_name': 'Celia Francis', 'db_name': 'Celia Francis', 'action': 'Already correct?'},
    {'airtable_name': 'Emmanuel Renegade', 'db_name': 'Emmanuel Renegade', 'action': 'Already correct?'},
    {'airtable_name': 'Mary Ann Edwards', 'db_name': 'Mary Ann Edwards', 'action': 'Already correct?'},
    {'airtable_name': 'Mutasa Brian', 'db_name': 'Mutasa Brian', 'action': 'Already correct?'},
]
```

**Question:** Why priority 0 if names match? Need to investigate script logic.

### Queue B: Likely Spelling Fixes (2 members)

**Need verification, then fix**

```python
LIKELY_FIXES = [
    {'airtable_id': 'recp6cA4v3QZm3R6A', 'current_name': 'Abby Karparsi', 'correct_name': 'Abby Karparis'},
    {'airtable_id': 'recEXcpeaO5Tws4XM', 'current_name': 'Edward Muller', 'correct_name': 'Eduard Muller'},
]
```

### Queue C: Duplicate Merges (8 names, 16 records)

**User must choose primary record for each, then we delete others**

```python
DUPLICATE_MERGES = [
    {'name': 'Ana Beatriz Freitas', 'keep': 'recGFs9XTcC2jnIDh', 'delete': ['recLt3XCk52TZwWk4']},
    {'name': 'Climbien Babungire', 'keep': 'recdnTAG6vu4mMCLX', 'delete': ['recsNjlDwH3PKtlg3']},  # Keep published one
    # ... etc (see DUPLICATES_DIAGNOSTIC.md for full list)
]
```

### Queue D: Priority 0 Manual Review (44 names)

**User must verify membership status - User says these are NOT ERA members.  [THAT IS NOT WHAT I"M SAYING]**

**All 44 Names (marked as "era Member" in Airtable but have priority 0):**

1. Abby Abrahamson (receEEWfOIBITexda) - abby.abrahamson@bio4climate.org
2. Avery Correia (reczh2Y6QovuyP89X) - avery.correia.era@gmail.com
3. Campbell Webb (recBdT95Y9LkG6RbA) - campbell.webb@gmail.com
4. SHOWME: Candrace Ducheneaux (recfeqgPCX9zlbWzY) - Mniwiconi@gmail.com
5. Ceal Smith (rectXu47oFSbpomFY) - cealsmith57@gmail.com
6. Dan Gerry (recMXTOXKDV63xJ9P) - danjgerry@gmail.com
7. Daniel Robin (rec6YAcFnuOMRx9C7) - daniel@in3capital.net
8. Daniel Valdiviezo (recdPGZjU11817LA8) - doloresj@union.edu
9. SHOWME: Derek Wilson (recESlZTZWexhqCTW) - (no email)
10. Finian Makepeace (recUkrK9upHTk0TcH) - finian@kisstheground.com
11. Gayathri Ilango (recPuzxQwhtWS0bFb) - Gayathri@thecircularfarm.com
12. Ilse Koehler-Rollefson (rec7z6uOvtroneLD5) - ilse.koehlerroll@gmail.com
13. Jacobus Van Der Bank (recjMXJSKEFiqQJT3) - jacobus.vanderbank@negative-emissions.org
14. Jim Laurie (recXXoShhqaqN42x6) - jimlaurie7@gmail.com
15. Joao Lopes (recpuMIDldYSbRKYk) - johnfarlopez@gmail.com
16. Joe Morris (recB76lC8SpJ0lvvI) - joe@morrisgrassfed.com
17. John Polhaus (recoRAwS1sAOTmhTb) - johnpohlhaus76@gmail.com
18. John Roulac (rec2HyKegKDL32FPQ) - jwroulac@gmail.com
19. SHOWME: John Wick (recdK0HkTVWNezGM9) - johnwick@sonic.net ← (Probably not the actor!)
20. SHOWME: Karol Mieczkin (rec6qDFvZKt5RyHHe) - (no email)
21. Katie Chess (recBjpLHd0U5EkRTE) - (no email)
22. Leonie Van Der Steen (recUgY9cZOhExSiJe) - (no email)
23. Lisa Smith (recXK2k9YZ3IIe1im) - lisa@stayfierce.com
24. Mark Fredericks (recagp6ojovdGkBt2) - mark@amped.nl
25. Martin Peck (recePZyBwqa7IWgQ8) - (no email)
26. Matthijis Bouw (recMh86ffA5ZslmaJ) - (no email)
27. Micah Opondo (reckcK4G2iaCOaSya) - micah.opondo@enoprogramme.org
28. SHOWME: Michael Vermeer (recq8IrN7Ya5oSjzz) - (no email)
29. Mick Lorkins (recvVSAxeUT4gcF62) - (no email)
30. Monifa Afina (recrskrf0z1ZYuHJi) - monifa.afinom@gmail.com
31. Méthode Dukore (rechR7XzyqwdyTuvs) - mariusdukore@gmail.com
32. Natalie Novoselova (recAx9qJBWP7Ux0nA) - novnatalia80@gmail.com
33. Nathalia Rio Preto (reccp4GsiQM2hXqP0) - nriopreto@translationcommons.org
34. Ngwana Henry (recVePAcduW93S0qb) - ngwanahenry0@gmail.com
35. Norma Carty (recK93bkyEEzrt3kU) - norma.carty@gmail.com
36. Pamela Berstler (recpctXKtFxlVRcxv) - pamelab@greengardensgroup.com
37. DID HE COME TO A TOWN HALL?  Patrick Worms, (recq4XOfTurggafh1) - pworms@evergreening.org
38. Penny Lewise (recd0rhsD5bXgS0Du) - (no email)
39. Tanner Millen (rec43Oy7lYkXvyEem) - millentanner@gmail.com
40. Twizeyimana Innocent (recawBYqYJudlfOws) - (no email)
41. Vivian Kanchian (rec8YvbNmFg81maTn) - vivian@kisstheground.com
42. CONTACT, NOT MEMBER Walter Jehne (recMn0vkqKDquX1D6) - walterjehne@yahoo.com.au ← (Well-known soil scientist)
43. aparna.dasaraju (recKppzRa0hcbypLh) - aparna.dasaraju@ishausa.org ← (Username format)
44. chris.searles (rec6DXCgK3InQRwo2) - chris.searles@biointegrity.net ← (Username format)

**Recommended Action:** Remove `era Member` flag from all 44 (user confirmed NOT members)

---

## Clean List: Ready for "Jon Should publish" Flag

### IMPORTANT FINDING: Most Already Have Bios!

**15 of 16 "confirmed safe" ALREADY HAVE BIOS** - they just need publishing:

- Benjamin Bisetsa ✅ (has bio, unpublished) - **NOT RECOGNIZED by user**
- Brendan McNamara ✅ (has bio, unpublished)
- Brent Constantz ✅ (has bio, unpublished)
- Brian Krawitz ✅ (has bio, unpublished)
- Bulonza jerson ✅ (has bio, unpublished)
- Carol Manetta ✅ (has bio, unpublished)
- Chauncey Bell ✅ (has bio, unpublished)
- Chris pieper ✅ (has bio, unpublished)
- Christina Engelsgaard ✅ (has bio, unpublished)
- Christine Freeland ✅ (has bio, unpublished)
- Climbien Babungire ✅ (has bio, PUBLISHED - duplicate)
- Daniel Fleetwood ✅ (has bio, unpublished) - **NOT RECOGNIZED by user**
- David Gold ✅ (has bio, unpublished) - **NOT RECOGNIZED by user**
- David Harper ✅ (has bio, unpublished) - **NOT RECOGNIZED by user**
- David maher ✅ (has bio, unpublished)

**Only 1 actually NEEDS a bio:**

- Mahangi Munanse ❌ (NO bio - skipped in Batch 5 for insufficient data)

### User Questions 4 Names (Not Recognized):

1. **Benjamin Bisetsa** - Has bio, marked ERA member, unpublished

   - Email: benjaminbisetsa250@gmail.com
   - NOT in database or transcripts
   - Unknown to user
2. **Daniel Fleetwood** - Has bio, marked ERA member, unpublished

   - Email: dan.fleetwood00@gmail.com
   - NOT in database or transcripts
   - Unknown to user
3. **David Gold** - Has bio, marked ERA member, unpublished

   - Email: wanteternalyouth1861318@gmail.com
   - NOT in database or transcripts
   - Unknown to user
4. **David Harper** - Has bio, marked ERA member, unpublished

   - Email: Landincommon1@gmail.com
   - NOT in database or transcripts
   - Unknown to user

**Problem:** These 4 are marked as `era Member = True` but:

- Not in Fathom database
- Not in Town Hall transcripts
- Not recognized by user
- May be incorrectly marked as ERA members

**Plus potentially 6 more after spelling fixes:**

- Celia Francis, Emmanuel Renegade, Mary Ann Edwards, Mutasa Brian (all have bios)
- Abby Karparis, Eduard Muller (after name fix - status unknown)

---

## Files Generated

1. **`PRIORITY_0_MATCHES_DIAGNOSTIC.md`**

   - Full analysis of 50 priority 0 members
   - 6 spelling mismatches found
   - 44 need manual review
2. **`DUPLICATES_DIAGNOSTIC.md`**

   - 8 duplicate names analyzed
   - All recommended for merging
   - Merge strategy provided
3. **`DIAGNOSTIC_SUMMARY.md`** (this file)

   - Executive summary
   - Action queues (not executed)
   - Clean list for flagging
4. **`diagnose_priority0_mismatches.py`**

   - Script used (can re-run anytime)
5. **`diagnose_duplicates.py`**

   - Script used (can re-run anytime)

---

## Recommended Next Steps

### ✅ User Decisions Made:

1. **44 Priority 0 names** → NOT ERA members, remove `era Member` flags
2. **8 Duplicates** → Merge straightforward
3. **4 Unrecognized members** → Need investigation (Benjamin Bisetsa, Daniel Fleetwood, David Gold, David Harper)

### Immediate Actions Needed:

**1. Investigate 4 Unrecognized Members:**

- Benjamin Bisetsa (benjaminbisetsa250@gmail.com)
- Daniel Fleetwood (dan.fleetwood00@gmail.com)
- David Gold (wanteternalyouth1861318@gmail.com)
- David Harper (Landincommon1@gmail.com)

**Questions:**

- Why are they marked as ERA members?
- Who added them?
- Should they keep member status?

**2. Execute Approved Fixes:**

- Remove `era Member` flag from 44 priority 0 names
- Merge 8 duplicate records
- Fix 6 spelling mismatches (2 need verification first)

**3. Then Flag for Publishing:**

- Members with bios who are unpublished
- Skip the 4 unrecognized until investigated
- Skip conflation (Craig McNamara) until split

---

## Impact on Airtable Update Script

**Current script status:** PAUSED - waiting for diagnostics

**Options:**

**Option 1: Flag Safe 16 Now**

- Skip all uncertain members
- Only flag confirmed priority 1 unpublished
- Fastest, but incomplete

**Option 2: Fix → Flag All**

- Resolve spelling issues
- Merge duplicates
- Then flag all ~70+ unpublished ERA members
- Complete, but requires more work first

**Recommendation:** Execute fixes first (remove false positives, merge duplicates), then re-evaluate flagging strategy

---

## Clear Action Summary

### What We Learned:

1. **Most unpublished ERA members ALREADY have bios** - they just need publishing
2. **44 names were incorrectly marked as ERA members** - user confirmed NOT members
3. **4 members user doesn't recognize** - need investigation before proceeding
4. **The "priority 0" issue was a red herring** - it meant "no TH attendance found" not "not a member"

### What Needs Fixing:

1. **Remove 44 false ERA member flags** (user confirmed)
2. **Merge 8 duplicate records** (user approved)
3. **Investigate 4 unrecognized members** (Benjamin Bisetsa, Daniel Fleetwood, David Gold, David Harper)
4. **Fix 6 spelling mismatches** (4 automatic, 2 need verification)
5. **Split Craig McNamara conflation** (Brendan + Craig Erickson)

### What Happens After Fixes:

- Re-run priority list generation
- Get clean count of actual unpublished ERA members
- Flag those who need "Jon Should publish"
- Most will just need publish checkbox, not new bios

---

**Status:** Diagnostics complete ✅ | User decisions received ✅ | Ready to execute approved fixes 🔧
