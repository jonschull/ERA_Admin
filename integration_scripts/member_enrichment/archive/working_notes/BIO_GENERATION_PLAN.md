# Bio Generation Plan - 60 ERA Members

**Date:** Oct 26, 2025  
**Status:** Ready to execute  
**Target:** Generate bios for 60 ERA members who attended Town Halls

---

## Current Situation

- **Database:** Has bio column, 280+ bios already synced
- **Remaining:** 60 ERA members need bios
- **Tools:** Scripts exist but need minor updates
- **Backup:** Fresh backup created (fathom_emails_BACKUP_AFTER_BIO_SYNC_20251026_205144.db)

---

## The 60 Members (Organized by Data Availability)

### Tier 1: Known Organizations/Context (10 members)
*These have clear organizational affiliations to highlight*

1. **Sarah Scherr** - EcoAgriculture Partners
2. **Jeremy Epstein** - Open Forest Protocol
3. **Laura Perez Arce** - Grupo Ecológico Sierra Gorda
4. **Steffie Rijpkema** - FarmTree
5. **Lisa Merton** - Greenbelt Movement International
6. **George Sendero** - For the Oceans
7. **Frank van Schoubroeck** - (check affiliation)
8. **Fadja Robert** - ERA Africa context
9. **Consolata Gitau** - (check affiliation)
10. **Wambui Muthee** - ERA Africa context

### Tier 2: Town Hall Presenters (3 members)
*From PAST_LEARNINGS - were presenters*

11. **Michael Haupt** - Was TH presenter
12. **Michael Levin** - Was TH presenter  
13. **Myra Jackson** - Was TH presenter

### Tier 3: Have Some Context (20 members)
*Names suggest professional context or have partial info*

14. Abby Karparis
15. Abigail Castle
16. Alexa Hankins
17. Alexander Watson
18. Alfredo Quarto
19. Ali Bin Shahid
20. Andrew Atencia
21. Angelique Garcia
22. Apryle Schneeberger
23. Aviv Green
24. Chris Pilley
25. Craig McNamara (note: known conflation issue)
26. Daphne Amory
27. Elizabeth Morgan Tyler
28. Fred Hornaday
29. Haley Kraczek
30. John Magugu
31. Joshua Konkankoh
32. Juan Bernal
33. Justin Ritchie

### Tier 4: Minimal Context (27 members)
*Single names, usernames, or very limited info*

34. Allison Wu
35. Andrea Miller (was afmiller09)
36. Cassandra Kiki Ami
37. Cory Albers
38. George Orbelian (was georgeorbelian)
39. Hadziqah
40. Ilarion (was Lastborn's Galaxy A11)
41. Ivan Owen (was emmafisher - using Emma's account)
42. Jeremiah Agnew
43. John Perlin
44. Julia Lindley
45. Karim Camara
46. Kathleen Groppe
47. Kriss Scioneaux
48. Larry Kopald
49. Lauren Miller
50. Luc Lendrum
51. Majd Thabit
52. Mark Frederiks
53. Mark Luckenbach
54. Matthew Hotsko
55. Nima Schei
56. Pete Corke (was Kwaxala / Pete)
57. Poyom Boydell
58. Richard Lukens
59. Roberto Pedraza Ruiz (was robertopedrazaruiz)
60. Sanmi Olowosile

---

## Step-by-Step Process

### Phase 1: Preparation (1-2 hours)

**1.1 Update bio generation prompt**

Location: `integration_scripts/member_enrichment/bio_writer_pilot.py`

Add to prompt template:
- [ ] PAST_LEARNINGS context check section
- [ ] Organization representative detection
- [ ] Town Hall presenter highlighting
- [ ] Data sparsity handling guide
- [ ] Multi-source verification instructions

**1.2 Create aggregated data files**

For each member, aggregate:
- Database info (location, affiliation, email)
- Airtable contact info
- Town Hall participation count
- Call transcripts if available
- LinkedIn matches if available
- Known organizations from PAST_LEARNINGS

Script: `aggregate_member_info.py` (may need updates)

**1.3 Organize by batches**

Suggested batching:
- **Batch 1:** Tier 1 (10 org reps) - Easiest, richest data
- **Batch 2:** Tier 2 (3 presenters) - Check TH agendas for topics
- **Batch 3:** Tier 3 (20 with context) - 10 at a time
- **Batch 4:** Tier 4 (27 minimal) - 10 at a time, may need research

---

### Phase 2: Batch 1 - Organization Representatives (Pilot)

**Goal:** Generate 10 bios with rich organizational context, establish quality bar

**2.1 Aggregate data for Batch 1**
```bash
cd integration_scripts/member_enrichment
python3 aggregate_member_info.py \
  "Sarah Scherr" \
  "Jeremy Epstein" \
  "Laura Perez Arce" \
  "Steffie Rijpkema" \
  "Lisa Merton" \
  "George Sendero" \
  "Frank van Schoubroeck" \
  "Fadja Robert" \
  "Consolata Gitau" \
  "Wambui Muthee"
```

**2.2 Generate bios using sub-agent pattern**

For each member:
```bash
python3 bio_writer_pilot.py --member "Sarah Scherr"
# Creates task file
# User tells Claude: "Read task_1_sarah_scherr.txt and write bio"
# Claude writes bio
# User pastes to response_1_sarah_scherr.txt
```

**2.3 Review and refine**

Create review pages:
```bash
python3 bio_writer_pilot.py --collect --batch 1
# Creates comparison page with all 10 bios
```

User reviews in browser, edits bios directly

**2.4 Process feedback**
```bash
python3 process_batch_feedback.py 1
# Collects approved bios
# Generates upload CSV
```

**2.5 Upload to database**
```bash
python3 update_database_bios.py batch1_approved.csv
```

**2.6 Upload to Airtable**
```bash
python3 update_airtable_bios.py batch1_approved.csv
```

**2.7 Set "Jon Should publish" flags**
```bash
python3 set_jon_should_publish.py --batch 1
```

---

### Phase 3: Refine Process Based on Batch 1

**Review questions:**
- Was data aggregation sufficient?
- Did prompt generate good quality?
- What needed most editing?
- How long did 10 bios take?
- Any pattern issues to fix?

**Update for remaining batches:**
- Refine prompt template
- Adjust data aggregation
- Create shortcuts for common edits

---

### Phase 4: Batches 2-4 (Remaining 50)

Repeat process for each batch:
1. Aggregate data (10 members at a time)
2. Generate bios
3. Review and refine
4. Upload to database
5. Upload to Airtable
6. Set publish flags

**Estimated timeline:**
- Batch 1 (10): 3-4 hours (includes learning)
- Batch 2 (3): 1 hour
- Batch 3 (20): 4-5 hours (2 sub-batches)
- Batch 4 (27): 6-7 hours (3 sub-batches)

**Total: ~15-20 hours** (can be split across sessions)

---

## Special Cases to Handle

### Organization Representatives
**Pattern:** Lead with organization role
- "Sarah Scherr leads EcoAgriculture Partners..."
- "Jeremy Epstein founded Open Forest Protocol..."

### Town Hall Presenters
**Pattern:** Highlight presentation topic
- "Michael Haupt presented at Town Hall on [topic]..."
- Check Town Hall agendas for presentation details

### Minimal Data Cases
**Pattern:** Focus on ERA engagement
- "Has participated in X Town Hall meetings..."
- "Active in ERA discussions on [topic if known]..."
- Keep it honest - don't fabricate

### Username Resolutions
**Note in bio if relevant:**
- Ivan Owen (formerly listed as emmafisher) - using Emma's Zoom
- Roberto Pedraza Ruiz (username: robertopedrazaruiz)

### Known Conflations
**Craig McNamara:** Known conflation issue - investigate before writing

---

## Quality Standards

### Bio Requirements
- **Length:** 600-950 characters (aim for ~800)
- **Style:** Third person, conversational, narrative (not resume)
- **Tone:** Professional but warm
- **ERA connection:** Specific, not generic

### Required Elements
1. Current work/role
2. Professional background (brief)
3. ERA connection/engagement (specific)
4. Unique value/perspective
5. Optional: Philosophy or personal touch

### Review Checklist
- [ ] Accurate (verified against sources)
- [ ] Right tone (professional but warm)
- [ ] Right length (600-950 chars)
- [ ] ERA connection clear
- [ ] Story not resume
- [ ] No fabricated details

---

## Data Sources Priority

**Trust hierarchy:**
1. **Database + Town Hall transcripts** (highest confidence)
2. **Airtable contact info** (verified)
3. **PAST_LEARNINGS** (human-verified patterns)
4. **LinkedIn** (verify carefully - may be wrong person)
5. **Inference from name/context** (lowest - be conservative)

**When in doubt:**
- Focus on ERA participation
- Note uncertainties in review
- Ask user for clarification

---

## Scripts Reference

### Core Scripts
- `aggregate_member_info.py` - Collect data for member
- `bio_writer_pilot.py` - Generate bios via sub-agent
- `process_batch_feedback.py` - Collect approved bios
- `update_database_bios.py` - Upload to database
- `update_airtable_bios.py` - Upload to Airtable
- `set_jon_should_publish.py` - Set publish flags

### Supporting Scripts
- `identify_members_needing_bios.py` - List members without bios
- `analyze_bio_feedback.py` - Quality analysis

### Locations
- **Scripts:** `/Users/admin/ERA_Admin/integration_scripts/member_enrichment/`
- **Batches:** `/Users/admin/ERA_Admin/integration_scripts/member_enrichment/batches/`
- **Database:** `/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db`

---

## Progress Tracking

### Checklist

**Batch 1 (Organization Reps - 10):**
- [ ] Data aggregated
- [ ] Bios generated
- [ ] User reviewed
- [ ] Uploaded to database
- [ ] Uploaded to Airtable
- [ ] Publish flags set

**Batch 2 (TH Presenters - 3):**
- [ ] Data aggregated (check TH agendas)
- [ ] Bios generated
- [ ] User reviewed
- [ ] Uploaded to database
- [ ] Uploaded to Airtable
- [ ] Publish flags set

**Batch 3 (Context Available - 20):**
- [ ] Sub-batch 3a (10) complete
- [ ] Sub-batch 3b (10) complete

**Batch 4 (Minimal Data - 27):**
- [ ] Sub-batch 4a (10) complete
- [ ] Sub-batch 4b (10) complete
- [ ] Sub-batch 4c (7) complete

### Status Commands

```bash
# Count remaining
sqlite3 FathomInventory/fathom_emails.db << 'EOF'
SELECT COUNT(DISTINCT p.name)
FROM participants p
JOIN calls c ON p.call_hyperlink = c.hyperlink
WHERE c.title LIKE '%Town Hall%'
  AND p.era_member = 1
  AND (p.era_africa IS NULL OR p.era_africa = 0)
  AND (p.bio IS NULL OR p.bio = '');
EOF

# List by batch status
# (Add bio_batch_number field to track)
```

---

## Next Session Kickoff

**Before starting:**
1. Read this plan completely
2. Review BIO_SYNC_SESSION_SUMMARY.md
3. Check database backup exists
4. Verify scripts are ready

**First task:**
```bash
# Update bio_writer_pilot.py with improvements
# Test on Sarah Scherr (org rep with known data)
# Review output quality
# Refine if needed
# THEN start Batch 1
```

**Questions to answer in first session:**
1. Is aggregated data sufficient for quality bios?
2. Does prompt generate appropriate style/tone?
3. How much editing is needed per bio?
4. Should we research LinkedIn before generating?
5. Batch size: 10 optimal or adjust?

---

## Success Criteria

**Completion:**
- [ ] All 60 members have bios in database
- [ ] All 60 bios uploaded to Airtable
- [ ] "Jon Should publish" flags set for approved bios
- [ ] Quality review complete
- [ ] No data fabricated or misrepresented

**Quality:**
- Bios match ERA tone and style
- Accurate to available data
- ERA connection clearly stated
- User-approved for publication

**Documentation:**
- Process improvements captured
- Common patterns documented
- Lessons learned added to PAST_LEARNINGS

---

**Last Updated:** Oct 26, 2025  
**Next Review:** After Batch 1 completion  
**Owner:** User + Claude collaboration
