# Proposed Database Cleanup Fixes
## Based on PAST_LEARNINGS and User Corrections

**Date:** 2025-10-26
**Context:** Cleaning up 71 ERA members without bios by applying known identifications

---

## Category 1: Known Identifications from PAST_LEARNINGS

### Organizations → People (PAST_LEARNINGS lines 16-23)

| Database Name | Should Be | Action | Bio Source | Confidence |
|---------------|-----------|--------|------------|------------|
| Cosmic Labyrinth | Indy Singh | Merge & copy bio | Airtable: Indy Singh | HIGH ✅ |
| Agri-Tech Producers LLC, Joe James | Joe James | Already done ✅ | Already synced | Done |
| EcoAgriculture Partners | Sarah Scherr | Merge & copy bio | Airtable: Sara Scherr | HIGH ✅ |

### Name Variants → Canonical (PAST_LEARNINGS lines 26-51)

| Database Name | Canonical Name | Action | Bio Source | Confidence |
|---------------|----------------|--------|------------|------------|
| KALOMBO-MBILIZI | Mbilizi Kalombo | Merge & copy bio | Airtable | HIGH ✅ |
| Angelique Rodriguez | Angelique Garcia | Merge (duplicate) | Already has bio | HIGH ✅ |
| aniqa Locations: Bangladesh, Egypt, Sikkim | Aniqa Moinuddin | Merge & copy bio | Airtable | HIGH ✅ |

### Past CSV Resolutions

| Database Name | Resolution | Action | Bio Source | Confidence |
|---------------|------------|--------|------------|------------|
| Jeremy - Open Forest Protocol | Jeremy Epstein | Merge & copy bio | Airtable | HIGH ✅ |
| Julia | Julia Lindley | Merge & copy bio | Airtable | HIGH ✅ |
| Lastborn's Galaxy A11 | Ilarion Mercullief | Merge & copy bio | Airtable: Ilarion | HIGH ✅ |

---

## Category 2: User-Provided Corrections

| Database Name | Correction | Action | Reason |
|---------------|------------|--------|--------|
| Dumi (Joomi Vanda) | Dumi Banda | Fix spelling | User: "Dumi is Dumi Banda" (PAST_LEARNINGS line 559 confirms) |
| Allison Chia-Yi Wu | Allison Wu | Merge duplicates | User: "The 2 Allisons are the same people" |
| Duane Norris | DELETE | Remove from database | User: "Duane is deceased so should be removed" ⚠️ |

---

## Category 3: Usernames (PAST_LEARNINGS patterns)

### Username = firstname+lastname Pattern

| Database Name | Pattern | Likely Resolution | Need to Verify | Confidence |
|---------------|---------|-------------------|----------------|------------|
| afmiller09 | username | Andrea Miller (line 146) | ✅ Confirmed | HIGH ✅ |
| georgeorbelian | firstname+last | George Orbelian (line 235) | ✅ Confirmed | HIGH ✅ |
| robertopedrazaruiz | first+last+last | Roberto Pedraza Ruiz (line 320) | ✅ Confirmed | HIGH ✅ |
| emmafisher | username | Ivan Owen (using Emma's account, line 194) | ✅ Confirmed | HIGH ✅ |

---

## Category 4: Need Further Investigation

### Device Names (May have identifications)

| Database Name | Pattern | Past Pattern Suggests | Check Past CSVs |
|---------------|---------|----------------------|-----------------|
| Samsung SM-N986U (Edward Paul Manaba) | device+person | Extract: Edward Paul Manaba (line 330) | HIGH ✅ |

### Single Names (Check Town Hall agendas per PAST_LEARNINGS)

| Database Name | Should Check | Investigation Method |
|---------------|--------------|---------------------|
| Frank van Schoubroeck | Fathom titles, Airtable fuzzy | Different from "Frank" |
| John Perlin | Check if in Airtable as "JP" | Initials pattern (line 50) |

---

## Proposed Execution Plan

### Phase 1: HIGH Confidence Merges (16 cases)
1. ✅ Cosmic Labyrinth → Indy Singh
2. ✅ KALOMBO-MBILIZI → Mbilizi Kalombo  
3. ✅ Angelique Rodriguez → Angelique Garcia (merge duplicates)
4. ✅ aniqa Locations... → Aniqa Moinuddin
5. ✅ Jeremy - Open Forest Protocol → Jeremy Epstein
6. ✅ Julia → Julia Lindley
7. ✅ Lastborn's Galaxy A11 → Ilarion Mercullief
8. ✅ EcoAgriculture Partners → Sarah Scherr
9. ✅ afmiller09 → Andrea Miller
10. ✅ georgeorbelian → George Orbelian
11. ✅ robertopedrazaruiz → Roberto Pedraza Ruiz
12. ✅ emmafisher → Ivan Owen
13. ✅ Samsung SM-N986U → Edward Paul Manaba
14. ✅ Dumi (Joomi Vanda) → Dumi Banda (fix spelling)
15. ✅ Allison Chia-Yi Wu + Allison Wu → Merge as Allison Wu

### Phase 2: Removal
16. ⚠️ Duane Norris → DELETE (deceased, user confirmed)

### Phase 3: Lower Confidence - Need User Verification
- Frank van Schoubroeck (no bio in Airtable)
- John Perlin (check if same as "JP" → John Perlin)
- Craig McNamara (known conflation issue)

---

## Expected Impact

**Before:** 71 ERA members without bios
**After Phase 1:** ~56 ERA members without bios (15 resolved)
**After Phase 2:** ~55 (1 deleted)

**Total bios recovered:** 15
**Total removed:** 1

---

## Data Safety

**Method:** 
1. Create CSV with all proposed changes
2. Copy bios from Airtable to database (preserving data)
3. Merge duplicates (preserving Town Hall attendance)
4. Single deletion for deceased person (Duane Norris)

**Backup:** Already created `fathom_emails_BACKUP_20251026_184829.db`

---

## Questions for User

1. **Duane Norris deletion:** Confirm this is correct? Will lose his Town Hall attendance records.
2. **Allison Wu vs Allison Chia-Yi Wu:** Which is the canonical name to keep?
3. **John Perlin:** Is he in Airtable? (didn't find bio earlier)

