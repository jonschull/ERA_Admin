# PLAN: Finish Missing Bios and Review ERA_Africa

**Created:** October 27, 2025  
**Status:** Draft for approval

---

## PHASE 1: Complete V6 Processing ⏳ IN PROGRESS

### 1.1 V6 Document Completion ✅ DONE
- [x] Emmanuel URAMUTSE - Bio enriched from transcripts, marked APPROVED
- [x] Hashim Yussif - Complete bio added from transcripts, marked APPROVED  
- [x] Mtokani Saleh - Complete bio added from transcripts, marked APPROVED
- [x] Mutasa Brian - Complete bio added from transcripts, marked APPROVED
- [x] All enrichments italicized in V6 document
- [x] MUTASA BRIAN spliced into V6

**V6 Status:** Ready for user review

---

### 1.2 User Review & Approval ⏳ NEXT STEP
- [ ] User reviews ERA_MEMBERS_LACKING_BIOS_V6.md
- [ ] User marks entries as APPROVED (or leaves unmarked for V7)
- [ ] User provides feedback/corrections if needed

**Expected Outcome:** Most V6 entries marked APPROVED; some → V7

---

### 1.3 Process APPROVED V6 Entries to SQL Database ⏳ IN PROGRESS

**✅ DATABASE INVESTIGATION COMPLETE (Oct 27, 7:50pm):**

**Schema Confirmed:**
- era_member field EXISTS (BOOLEAN, 387 true / 17 false)
- era_africa field EXISTS (INTEGER, 26 tagged / 378 not tagged)
- bio, email, affiliation, linkedin_url fields all exist
- Database backups exist (most recent: Oct 27, 3:04pm - before batch script)

**⚠️ BATCH SCRIPT ISSUE (Oct 27, 7:30pm):**
- Attempted batch script approach (`process_v6_to_database.py`)
- Script claimed "5 updated" but had regex parsing errors
- Potential issues noted in V6_PROCESSING document (will check later)
- Less severe than initially thought (V6 members likely lacked bios)

**Corrected Process:**
- ❌ NOT batch scripting
- ✅ Case-by-case intelligent review with human judgment
- ✅ Use reusable `update_participant_bio()` function
- ✅ Update bio + email + affiliation + linkedin_url + era_member
- ✅ Verify each update, document decisions
- ⚠️ NAME MATCHING is the critical issue - be very careful

**Process Details:** See `V6_PROCESSING_CONTEXT_RECOVERY.md`

**16 APPROVED Cases to Process:**
1. Emmanuel URAMUTSE (ERA Africa enrichment)
2. Fadja Robert
3. Fred Ogden
4. Hashim Yussif (ERA Africa enrichment)
5. Julia Lindley
6. Kaluki Paul Mutuku
7. Maxime Weidema
8. Minot Weld
9. Mtokani Saleh (ERA Africa enrichment)
10. Mutasa Brian (ERA Africa enrichment)
11. Penny Heiple
12. Roberto Forte
13. Roberto Pedraza Ruiz
14. Scott Schulte
15. Theopista Abalo
16. nding'a ndikon

---

### 1.4 Create V7 for Non-Approved Entries ⏳ PENDING
- [ ] Extract non-approved V6 entries
- [ ] Create ERA_MEMBERS_LACKING_BIOS_V7.md
- [ ] Document why entries weren't approved (if applicable)
- [ ] Plan V7 research approach

**Note:** V6 is not the end of member enrichment

---

## PHASE 2: ERA_Africa_review 📋 FUTURE

**Goal:** Comprehensively characterize the ERA Africa network and enrich member bios

### 2.1 Scope Definition (TBD)
Details to be determined after V6 is processed.

**Preliminary Scope:**
1. Tag ERA Africa members in database
2. Review existing bios
3. Enrich bios with transcript information
4. Document network structure/relationships

---

### 2.2 ERA Africa Speaker Inventory
**Resource:** 59 unique speakers identified in ERA Africa transcripts

**High-Frequency Speakers Already in Database:**
- Edward Paul Munaaba (525 mentions)
- Leonce Bulonze (239 mentions)
- mbilizi Kalombo (337 mentions)
- Moses Ojunju (248 mentions)
- Leonard IYAMUREME (500 mentions)
- And others...

---

### 2.3 Proposed ERA_Africa_review Tasks (TBD)

#### Task A: Tag ERA Africa Members
- [ ] Tag all/most 59 speakers with era_africa = 1 in SQL database
- [ ] Note: era_africa field already exists (currently 26 tagged)
- [ ] Document participation level (mention count from transcripts)
- [ ] Note meeting attendance patterns
- [ ] Cross-reference with era_member status

#### Task B: Review Existing Bios
- [ ] For each ERA Africa member in database:
  - Read current bio
  - Check against transcript information
  - Identify gaps or outdated information
  - Flag bios needing enrichment

#### Task C: Enrich Bios from Transcripts
- [ ] For members flagged in Task B:
  - Extract relevant information from transcripts
  - Draft enrichments (italicized)
  - Get user approval
  - Update database

#### Task D: Network Characterization (Scope TBD)
Options to consider:
- Document network structure (who connects with whom)
- Identify key coordinators/connectors
- Map geographic distribution
- Categorize by focus area (permaculture, youth, education, etc.)
- Create network visualization
- Document project collaborations

**Details:** To be determined collaboratively after V6 completion

---

## DEPENDENCIES & SEQUENCING

```
PHASE 1 (V6 Processing)
├── 1.1 V6 Document Completion ✅ DONE
├── 1.2 User Review & Approval ⏳ NEXT
├── 1.3 Process to SQL Database ⏳ Waiting on 1.2
└── 1.4 Create V7 ⏳ Waiting on 1.3

    ↓ (Clear the deck on V6)

PHASE 2 (ERA_Africa_review)
├── 2.1 Define Scope ⏳ After Phase 1
├── 2.2 Speaker Inventory ✅ Complete
├── 2.3 Execute Tasks A-D ⏳ After 2.1
└── Final Review & Documentation
```

---

## CURRENT STATUS SUMMARY

**✅ Completed:**
- ERA Africa transcript analysis (22,857 lines, 25 meetings)
- Extracted 4 member bios from transcripts
- Fuzzy matched all 59 speakers against V6 members
- Identified high-frequency speakers in database
- Spliced all enrichments into V6
- Marked enrichments as APPROVED

**⏳ Ready for User Action:**
- Review ERA_MEMBERS_LACKING_BIOS_V6.md
- Confirm APPROVED markings (or adjust)
- Provide any feedback/corrections

**⏳ Pending:**
- Process APPROVED V6 entries to SQL database
- Create V7 for non-approved entries
- Define ERA_Africa_review scope

---

## FILES REFERENCE

**Current V6 Work:**
- `ERA_MEMBERS_LACKING_BIOS_V6.md` - Main document with enrichments
- `ENRICHMENTS_FOR_REVIEW.md` - Summary of enriched members
- `FUZZY_MATCH_FINDINGS.md` - Analysis methodology
- `NEW_ENRICHMENTS_FROM_FUZZY_MATCH.md` - Detailed findings
- `transcript_speakers_complete.txt` - All 59 speakers list

**Supporting Documents:**
- `ERA_MEMBERS_V6_ENRICHED.md` - Comparison document
- `ERA_AFRICA_ENRICHMENT_SUMMARY.md` - Complete methodology

**ERA Africa Source:**
- `fathom/output/era_africa_complete.md` - 25 meetings, 22,857 lines

---

## NEXT IMMEDIATE ACTION

**USER:** Review `ERA_MEMBERS_LACKING_BIOS_V6.md` and confirm APPROVED markings

**Then:** I will process APPROVED entries to SQL database (following V1-V5 workflow)

