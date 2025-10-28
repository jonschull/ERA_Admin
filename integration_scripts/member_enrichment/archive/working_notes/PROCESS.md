# Member Bio Enrichment Process

**Status:** VALIDATED (Oct 25, 2025)  
**Test batch:** 4 members completed successfully

---

## Overview

This process creates context-rich, professional bios for ERA members by intelligently synthesizing information from multiple sources. It follows the "AI → HTML review → Human approval → Apply" pattern established in Phase 4B-2 participant reconciliation.

---

## The Process (4 Steps)

### Step 1: Aggregate Data

**Tool:** `aggregate_member_info.py`

**What it does:**
- Collects data from 5 sources (mechanical, no judgment):
  1. **Fathom Database** - Location, affiliation, email, ERA status, Town Hall attendance
  2. **Airtable** - Current record, email, phone, affiliated orgs
  3. **LinkedIn Connections Export** - Fuzzy matching for position/company
  4. **Town Hall Transcripts** - Searches for name mentions with context
  5. **Google Contacts** - Phone numbers with labels (Mobile, Work, etc.)

**Usage:**
```bash
# Single member
python3 aggregate_member_info.py "Member Name"

# Batch mode (multiple members, combined file)
python3 aggregate_member_info.py "Member 1" "Member 2" "Member 3" "Member 4" --batch 3
```

**Output:**
- JSON: `batches/aggregated_data/{name}.json` (always individual)
- Markdown: `batches/aggregated_data/{name}.md` (single mode)
- Markdown: `batches/batch{N}.md` (batch mode - all members combined)

---

### Step 2: Get LinkedIn Profiles

**Tool:** `read_linkedin_profiles.py`

**What it does:**
- Launches Microsoft Edge with your LinkedIn cookies
- Navigates to profile URLs
- Scrolls to load all content
- Extracts full visible text (not just structured fields)
- Keeps browser open between profiles (efficient batch processing)
- Saves cookies for next session

**Usage:**
```bash
# Single profile
python3 read_linkedin_profiles.py https://www.linkedin.com/in/username

# Multiple profiles (batch)
python3 read_linkedin_profiles.py URL1 URL2 URL3
```

**Prerequisites:**
- Must be logged into LinkedIn in regular browser
- Export cookies once (see `cookie_export_guide_linkedin.md`)
- Save to `linkedin_cookies.json`

**Output:**
- JSON with full_text: `batches/linkedin_profiles/{username}.json`
- Captures 5,000-30,000 chars per profile

---

### Step 3: Intelligent Synthesis (Human)

**Review all sources and draft bio considering:**

**Length Guidelines:**
- Students/Early career: 400-600 chars
- Mid-career professionals: 600-800 chars  
- Established leaders: 800-1000 chars
- Max: ~950 chars

**Voice:**
- Third person, conversational
- Professional but warm
- Narrative flow (not resume-style)

**Required Elements:**
- Current work/role
- Professional background (brief)
- ERA connection/engagement
- Unique value/perspective
- Optional: Philosophy/personal touch

**Bio Quality Checks:**
- ✅ Accurate (verified against sources)
- ✅ Contextual (shows HOW they engage, not just credentials)
- ✅ Current (database often more current than LinkedIn)
- ✅ Specific (projects, philosophies, not generic)
- ✅ Connected (ERA relevance clear)

**Create Review Page:**
- Use template: `bio_review_{name}.md`
- Include: proposed bio, character count, email, affiliations, supporting data
- Mark status: PENDING APPROVAL or APPROVED

---

### Step 4: Human Review & Approval

**Human reviews one-pager and:**
1. Edits bio directly in review page
2. Verifies email, affiliated orgs
3. Marks status as APPROVED
4. Moves to `approved_bios.md` for batch Airtable update

**Review Questions to Consider:**
- Right length/tone for this person?
- Appropriate balance of background vs ERA engagement?
- Any sensitive information to avoid?
- Affiliated orgs accurate and linkable?

---

## Workflow Summary

```
Member Name
    ↓
aggregate_member_info.py → Database, Airtable, TH transcripts, LinkedIn export match
    ↓
read_linkedin_profiles.py → Full LinkedIn profile text (using cookies)
    ↓
Human reads all sources → Drafts bio intelligently
    ↓
Create review one-pager → bio_review_{name}.md
    ↓
Human reviews/edits → Approves or requests revision
    ↓
Add to approved_bios.md → Ready for Airtable batch update
```

---

## Tools & Files

### Scripts
- `aggregate_member_info.py` - Data collection
- `read_linkedin_profiles.py` - LinkedIn profiles via Edge
- `identify_members_needing_bios.py` - Find members without bios

### Data Files
- `linkedin_cookies.json` - LinkedIn session (gitignored)
- `batches/aggregated_data/` - Per-member aggregated data
- `batches/linkedin_profiles/` - LinkedIn profile extracts
- `batches/bio_review_{name}.md` - One-pagers for review
- `batches/approved_bios.md` - Approved bios ready for Airtable

### Guides
- `cookie_export_guide_linkedin.md` - How to get LinkedIn cookies
- `README.md` - Component overview

---

## Key Patterns (Hard-Won)

### 1. Database Often More Current Than LinkedIn
- **Example:** Ben Rubin's LinkedIn shows "Media Coordinator at E-nable" (his volunteer work)
- **Reality:** He's actually a full-time teacher (database correct)
- **Lesson:** Always check Town Hall transcripts for self-descriptions

### 2. Transcripts Are Gold
- **Ben:** 103 mentions, full self-introduction, project details
- **Bill:** His philosophy in his own words
- **Lesson:** Prioritize members who spoke in Town Halls (rich context)

### 3. LinkedIn Content Is in HTML
- Don't just read structured fields
- Extract `full_text` (5K-30K chars)
- Includes About, Experience, Education sections

### 4. Cookies Work Better Than Chrome Profile
- Tried: Chrome user data directory (crashed)
- Works: Export cookies manually, load in Edge
- Pattern: Same as Fathom authentication

### 5. Keep Browser Open Between Profiles
- Script already does this for batches
- Saves ~10 seconds per profile
- Cookies persist automatically

---

## Success Metrics

### Batch 1-2 (Test + Validation)
**4 members completed:**
- ✅ Ben Rubin (839 chars) - APPROVED
- ✅ Noura Angulo (836 chars) - APPROVED  
- ✅ Bill Reed (828 chars) - PENDING
- ✅ Celia Francis (874 chars) - PENDING

**Data quality:**
- 100% had database info
- 100% had Airtable records
- 100% had LinkedIn matches (exact)
- 50% had rich Town Hall context (Ben, Bill)
- 50% had minimal TH mentions (Noura, Celia)
- 25% had phone numbers (Ben)

### Batch 3 (Process Improvements)
**4 members with enhanced data:**
- Jacob Denlinger - All 5 sources ✅ (including phone)
- Mary Minton - 4/5 sources
- Mark Luckenbach - 3/5 sources (no LinkedIn, no phone)
- Rayan Naraqi Farhoumand - 4/5 sources

**Improvements validated:**
- ✅ Phone number integration working
- ✅ Batch mode (combined files) working
- ✅ 5-source aggregation complete

**Time per member:**
- Data aggregation: ~5 seconds
- LinkedIn fetch: ~15 seconds
- Intelligent synthesis: ~5-10 minutes (human)
- Review: ~2-3 minutes (human)

**Total:** ~15-20 minutes per bio (mostly human intelligence, as intended)

---

## Next Steps

1. **Get 4 more reviews approved** (Bill, Celia + 2 new)
2. **Batch update Airtable** (execute all approved bios at once)
3. **Scale to next 10-20 members** (prioritize those with Town Hall attendance)
4. **Document Airtable update process** (field mapping, org linking)
5. **Iterate on bio style** based on user feedback

---

## Principles (From Memory System)

**Intelligent, not mechanical:**
- Scripts collect data (mechanical)
- Human reads and synthesizes (intelligent)
- No "fill in the template" approach

**Context-rich, not resume-style:**
- Show HOW they engage with ERA
- Include projects, philosophies, anecdotes
- Cite Town Hall quotes when available

**Accurate, not assumptive:**
- Cross-check sources (database vs LinkedIn)
- Note discrepancies in review pages
- Flag uncertainty for human judgment

**Efficient, not rushed:**
- Tools minimize mechanical work
- But don't skip the intelligent reading
- 15-20 min per bio is appropriate for quality

---

**Last updated:** October 25, 2025, 8:10pm  
**Version:** 2.0 (added phone numbers + batch mode)
