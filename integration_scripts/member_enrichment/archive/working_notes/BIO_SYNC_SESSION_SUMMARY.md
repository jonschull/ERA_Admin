# Bio Sync Session Summary - Oct 26, 2025

## Context for Next Session

### Current State
- **Database:** `fathom_emails.db` with `bio` column added
- **Backup:** `fathom_emails_BACKUP_AFTER_BIO_SYNC_20251026_205144.db`
- **ERA members without bios:** 60 (down from 93)
- **Total bios synced:** 280+ from Airtable → Database

### What We Accomplished

1. **Added bio column** to participants table
2. **Synced 280+ bios** from Airtable to database
3. **Name matching cleanup (33 cases):**
   - Fuzzy matching: 11 cases (Neil/Neal Spackman, Dr. Poulomi, etc.)
   - Substring matching: 10 cases (Graham Boyd - Evolutesix, Grant Holton, etc.)
   - PAST_LEARNINGS: 15 cases (Cosmic Labyrinth → Indy Singh, etc.)
   - Additional fixes: 4 cases (Sanmi, Nathalie, kPm5Xu, Steffie)
   - Manual corrections: 3 cases (Jeremy Epstein, Jeremiah Agnew, etc.)
4. **Data recovery:** Restored 7 lost Town Hall attendance records
5. **Cleanup:** Removed Duane Norris from ERA members (deceased)

---

## Next Steps: Generate Bios for 60 Members

### The 60 ERA Members Still Needing Bios

1. Abby Karparis
2. Abigail Castle
3. Alexa Hankins
4. Alexander Watson
5. Alfredo Quarto
6. Ali Bin Shahid
7. Allison Wu
8. Amanda Joy Ravenhill
9. Andrea Miller
10. Andrew Atencia
11. Angelique Garcia
12. Apryle Schneeberger
13. Aviv Green
14. Cassandra Kiki Ami
15. Chris Pilley
16. Consolata Gitau
17. Cory Albers
18. Craig McNamara
19. Daphne Amory
20. Elizabeth Morgan Tyler
21. Fadja Robert
22. Frank van Schoubroeck
23. Fred Hornaday
24. George Orbelian
25. George Sendero
26. Haley Kraczek
27. Hadziqah
28. Ilarion
29. Ivan Owen
30. Jeremiah Agnew
31. Jeremy Epstein
32. John Magugu
33. John Perlin
34. Joshua Konkankoh
35. Juan Bernal
36. Julia Lindley
37. Justin Ritchie
38. Karim Camara
39. Kathleen Groppe
40. Kriss Scioneaux
41. Larry Kopald
42. Laura Perez Arce
43. Lauren Miller
44. Lisa Merton
45. Luc Lendrum
46. Majd Thabit
47. Mark Frederiks
48. Mark Luckenbach
49. Matthew Hotsko
50. Michael Haupt
51. Michael Levin
52. Myra Jackson
53. Nima Schei
54. Pete Corke
55. Poyom Boydell
56. Richard Lukens
57. Roberto Pedraza Ruiz
58. Sarah Scherr
59. Steffie Rijpkema
60. Wambui Muthee

### Known Information About Some Members

- **Jeremy Epstein:** Open Forest Protocol
- **Sarah Scherr:** EcoAgriculture Partners
- **Laura Perez Arce:** Grupo Ecológico Sierra Gorda
- **Steffie Rijpkema:** FarmTree (from PAST_LEARNINGS)
- **Lisa Merton:** Greenbelt Movement International (from PAST_LEARNINGS)

### Bio Generation Strategy

1. **Check existing data sources:**
   - Airtable contact info (emails, organizations)
   - Fathom call transcripts/titles
   - Google contacts export (if available)
   - LinkedIn profiles (if accessible)

2. **Use bio generation script:**
   - Location: `integration_scripts/member_enrichment/generate_bio_batch.py`
   - Review and improve prompting (see Bio Generation Prompting section below)

3. **Manual review and editing:**
   - User preference: Generate drafts, then review
   - Set "Jon Should publish" flag for approved bios

---

## Critical Issues & Solutions

### Issue 1: Unsafe Merges Without Data Preservation

**Problem:** During this session, we performed multiple "merges" using ad-hoc UPDATE/DELETE:

```python
# BAD - What we did:
cursor.execute("UPDATE participants SET name = ? WHERE name = ?", (new_name, old_name))
# This fails if new_name already exists (UNIQUE constraint)

cursor.execute("DELETE FROM participants WHERE name = ?", (old_name,))
# This loses Town Hall attendance data!
```

**Why This Is Dangerous:**
- Database has `UNIQUE(name)` constraint
- Each person can only have ONE record
- Multiple Town Hall attendances stored in comma-separated `source_call_url` field
- Simple rename fails if canonical name already exists
- Simple delete loses attendance records

**Examples Where We Did It Wrong:**
1. Deleted "Jake Fairbanks Kelley" without merging attendance
2. Deleted 6 duplicates via merge_duplicate_participants.py without verifying unique calls
3. Lost 5 unique Town Hall attendance records initially

**The Safe Solution: `merge_participant_safely.py`**

We created this script but **didn't use it**! The script:
1. Checks if both names exist
2. Compares attendance data
3. Merges unique calls to canonical name
4. Only then deletes duplicate
5. Verifies merge success

**Location:** `/Users/admin/ERA_Admin/integration_scripts/merge_participant_safely.py`

**Usage:**
```bash
# Dry run first
python merge_participant_safely.py "Duplicate Name" "Canonical Name"

# Execute after review
python merge_participant_safely.py "Duplicate Name" "Canonical Name" --execute
```

**Lesson:** ALWAYS use merge_participant_safely.py for duplicates, NEVER ad-hoc DELETE.

### Issue 2: Name Matching Gaps

**Problems We Encountered:**
1. Name order variants (Sanmi Olowosile vs Olowwosile Sanmi)
2. Accent differences (Nathalie Ríos vs Nathalie Rios Duran)
3. Partial names (JS vs Joshua Shepard)
4. Organizations vs people (Cosmic Labyrinth vs Indy Singh)
5. Device names (Samsung SM-N986U vs Edward Paul Munaaba)

**Solution:** Multi-pass matching strategy:
1. Exact match
2. Case-insensitive match
3. Fuzzy match (>85% similarity)
4. Substring match (organizations, devices)
5. PAST_LEARNINGS lookup
6. Manual review

**Important:** Check PAST_LEARNINGS.md BEFORE assuming no match exists.

### Issue 3: Database Recovery After Reckless Merges

**What Happened:**
- Deleted 9 duplicate names
- Lost 7 unique Town Hall attendance records
- Had to recover from Oct 25 backup

**Recovery Method:**
1. Extract deleted records to CSV from backup
2. Add lost attendance to canonical names (UPDATE, not INSERT)
3. Verify restoration

**Script:** `/Users/admin/ERA_Admin/integration_scripts/restore_lost_attendance.py`

**Lesson:** 
- Always backup BEFORE bulk operations
- Name backup with descriptive timestamp
- Keep multiple backup generations

---

## Scripts Created This Session

### Data Sync & Cleanup
1. `sync_bios_to_database.py` - Added bio column, synced 267 bios
2. `merge_participant_safely.py` - **Safe merge with data preservation (NOT USED)**
3. `restore_lost_attendance.py` - Recovered 7 lost attendance records
4. `LOST_ATTENDANCE_RECORDS.csv` - Extracted data from backup

### Airtable Integration
5. `create_jon_should_publish_field.py` - Created new Airtable field
6. `set_jon_should_publish.py` - Set flags for 10 Town Hall attendees
7. `revert_publish_flags.py` - Fixed incorrect "Publish" flag usage

### Member Enrichment (existing)
8. `generate_bio_batch.py` - Bio generation (needs review)
9. `update_airtable_bios.py` - Upload bios to Airtable

---

## Bio Generation Prompting Review

**Current Script:** `integration_scripts/member_enrichment/generate_bio_batch.py`

### Issues to Address

1. **Review prompting strategy**
2. **Incorporate hard-won lessons from Phase 4B-2**
3. **Add context from multiple sources:**
   - Airtable contact info
   - Fathom call participation
   - Organization affiliations
   - Town Hall presentations

### Next Session Tasks

1. Review `generate_bio_batch.py` prompting
2. Test on small batch (5-10 members)
3. Manual review and refinement
4. Upload approved bios to Airtable
5. Set "Jon Should publish" flags

---

## Key Files & Locations

### Database
- **Active:** `/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db`
- **Backup:** `/Users/admin/ERA_Admin/FathomInventory/fathom_emails_BACKUP_AFTER_BIO_SYNC_20251026_205144.db`

### Scripts
- **Integration:** `/Users/admin/ERA_Admin/integration_scripts/`
- **Member Enrichment:** `/Users/admin/ERA_Admin/integration_scripts/member_enrichment/`
- **Reconciliation:** `/Users/admin/ERA_Admin/integration_scripts/participant_reconciliation/`

### Reference
- **PAST_LEARNINGS:** `/Users/admin/ERA_Admin/integration_scripts/participant_reconciliation/PAST_LEARNINGS.md`
- **Airtable Export:** `/Users/admin/ERA_Admin/airtable/people_export.csv`

---

## Lessons Learned

1. **Always use safe merge scripts** - Don't write ad-hoc DELETE statements
2. **Backup before bulk operations** - Name backups descriptively
3. **Check PAST_LEARNINGS first** - Many "unknowns" are already resolved
4. **Multi-pass name matching** - Exact → Fuzzy → Substring → Manual
5. **Verify before DELETE** - Check for unique data in records being deleted
6. **Database has UNIQUE(name)** - Can't have multiple records per person
7. **Attendance stored as CSV** - Multiple calls in `source_call_url` field

---

## Status Check Commands

```bash
# Count ERA members without bios
sqlite3 FathomInventory/fathom_emails.db << 'EOF'
SELECT COUNT(DISTINCT p.name)
FROM participants p
JOIN calls c ON p.call_hyperlink = c.hyperlink
WHERE c.title LIKE '%Town Hall%'
  AND p.era_member = 1
  AND (p.era_africa IS NULL OR p.era_africa = 0)
  AND (p.bio IS NULL OR p.bio = '');
EOF

# List them
sqlite3 FathomInventory/fathom_emails.db << 'EOF'
SELECT DISTINCT p.name
FROM participants p
JOIN calls c ON p.call_hyperlink = c.hyperlink
WHERE c.title LIKE '%Town Hall%'
  AND p.era_member = 1
  AND (p.era_africa IS NULL OR p.era_africa = 0)
  AND (p.bio IS NULL OR p.bio = '')
ORDER BY p.name;
EOF
```

---

## Questions for Next Session

1. Should we generate all 60 bios at once or in batches?
2. What's the review/approval workflow for generated bios?
3. Should we check LinkedIn/other sources before generating?
4. How to handle organization representatives (Sarah Scherr, Jeremy Epstein)?
5. Priority order for bio generation?

