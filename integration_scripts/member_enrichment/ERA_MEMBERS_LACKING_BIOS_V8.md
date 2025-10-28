# ERA Members Lacking Bios - V8 (SHORT LIST)

**Date Created:** October 28, 2025
**Status:** Members still needing bios or resolution after V7 processing

---

## Purpose & Context

This document tracks ERA members who lack biographical information in the Fathom database. The goal is to ensure every ERA member has a complete, accurate bio while removing non-members who entered the database incorrectly.

### ERA Member Definition

**CRITICAL:** A person is an ERA member if and only if:

1. They attended a Town Hall meeting (introduced, no objections, week passed), OR
2. Special decision from Jon Schull

**The database contains non-members.** We must verify Town Hall attendance or special approval before treating someone as a member.

### Why Hand-Authored Bios

**Hand-authored bios work best** because they:

- Capture what makes each person relevant to ERA
- Integrate professional background with ERA engagement
- Reflect actual contributions and interests discussed in Town Halls
- Avoid generic LinkedIn summary language
- Maintain consistent tone and relevance to ecosystem restoration

### Sources of Truth (Current Paradigm)

1. **Fathom Database** = Primary source of truth for current membership and bios
2. **Legacy Airtable** = Historical record of past membership (may be stale, use for cross-checking)
3. **Town Hall Transcripts** = Rich source for bio content and verification
4. **Email** = jschull@gmail.com inbox and sent folders
5. **LinkedIn Profiles** = Professional background (active scraping technique - see below)
6. **Web Search** = External verification and additional bio details
7. **Future: New Airtable** = Will mirror Fathom DB as user-friendly interface

**Key Insight:** Legacy Airtable is NOT our current source of truth—it's a snapshot of past truth. Our Fathom Database is more current and accurate. Legacy Airtable is useful for discovering people who WERE members and verifying historical context.

### Critical Distinctions

- **ERA Member** (era_member=1 in Fathom DB) = Current confirmed member based on Town Hall participation, direct contact, or legacy Airtable verification
- **ERA Africa Attendee** (era_africa=1, era_member may be 0 or 1) = Participated in ERA Africa meetings; may or may not be full ERA member
- **Private Meeting Participant** = NOT an ERA member; may be retained in database as potential member or for relationship tracking
- **Legacy Airtable Member** = Person with bio in old Airtable; likely was a member; verify against Fathom DB for current status

### Intelligent Assistant Pattern (Human-AI Collaboration)

Following the participant_reconciliation model:

1. AI identifies members needing profiles
2. AI conducts multi-source research (see Research Workflow below)
3. AI compiles research notes with sources inline in document
4. AI drafts complete profile updates (bio, email, affiliations)
5. **Human reviews, edits, approves** (critical oversight step)
6. AI updates database ONLY after explicit approval
7. AI creates next version removing completed members
8. **Eventually there will be no members left**

**Key:** AI is intelligent assistant, not autonomous agent. Human has final say on all additions/changes.

### Workflow (Proven Through V7 → V8)

1. **Research each member:**
   - Check Fathom Database first (era_member flag, existing bio, call history)
   - Search Town Hall transcripts (speaking roles, presentations, context)
   - Check Legacy Airtable (was this person historically a member? any bio there?)
   - Search Fathom database for call titles and collaborators
   - Check emails (jschull@gmail.com inbox/sent)
   - Check LinkedIn for professional details (see LinkedIn Scraping section below)
   - Web search for affiliations and background
   - For deep digging: Use Fathom API to retrieve transcripts from other calls
     - **Date-range trick**: API allows filtering by date ranges to find older events not in current exports
2. **Draft bio following ERA standards:**

   - Focus on work relevant to ecosystem restoration
   - Include current role and organization
   - Highlight ERA-relevant contributions
   - Avoid age references and overly promotional language
   - Be concise (2-4 sentences typical)
   - Use existing bios as exemplary.
3. **User review and corrections:**

   - User edits bio for accuracy and tone
   - User identifies errors (wrong affiliations, confused identities)
   - User confirms or decleare membership status, or suggests other queries.
   - AI must READ these User edits and respond Intelligently and Thoughtfully, discussing issues that arise.  Scripts can not do this.
4. **Database update ONLY after user approval:**
   - Never update database speculatively or impulsively
   - Wait for explicit approval
   - Document all changes in version notes
   - Record provenance information (see Provenance Tracking below)
5. **Create next version with remaining items:**
   - Short list of unresolved members
   - Clear action items for each
   - **Naming convention**: V1, V2, V3... (future: consider adding datetime like V8_20251028)
   - Include processing summary and learnings for next cycle

### Procedural Guidelines (From Past Versions)

**1. Quality Control**
- AI proposes, human edits, AI updates database
- No "bad apples" - fix issues permanently so they don't resurface
- Document fixes in PAST_LEARNINGS.md (for participant reconciliation context)

**2. Member Verification**
- Database contains non-members
- MUST verify Town Hall attendance before treating as member
- Remove flagged non-members immediately (with documentation)

**3. Data Preservation**
- When removing members, document WHY
- Database corrections (spelling, case, merges) done immediately
- All changes tracked AND REVERTABLE

**4. Document Versioning**
- Each iteration creates new numbered version: V1, V2, V3, etc.
- Completed members removed in NEXT version when marked APPROVED/RESOLVED
- Document versions shrink each iteration

### Key Principles (From Past Versions)

**1. Context-Rich Bios**
- NOT: Generic LinkedIn summary copy-paste
- YES: Curated for consistency of tone and relevance to ERA
- Focus on work relevant to ecosystem restoration
- 2-4 sentences typical

**2. Prioritization**
- Act on those where action is clear
- Insert questions for those where you don't know what to do
- Flag unresolved items for user decision

**3. Human Oversight**
- AI collects data, drafts bios
- Human edits and approves every bio
- AI learns from corrections and improves
- AI must READ user edits intelligently and thoughtfully

**4. Quality Over Speed**
- Intelligent solutions via intelligence, not scripts alone
- Thoughtful, personalized bios that reflect ERA engagement
- Research thoroughly before proposing actions

### Key Learnings from V7 Processing

**Name Confusion:**

- Elizabeth Morgan Tyler ≠ Eliza Herald (both water activists, easy to confuse)
- Always verify identity when multiple people have similar names/roles

**Affiliation Errors:**

- Cross-check affiliations (e.g., Myra Jackson was incorrectly linked to Earth Law Center—that's Missy Lahren)
- Primary vs secondary affiliations matter (Myra: ERA/Global Being Foundation, not Earth Law Center) [Note Myra's ERA is Earth Regeneration Alliance. don't be confused.]

**Membership Status:**
- Legacy Airtable members may not be in Fathom DB yet (e.g., Mary Ann Edwards—now added)
- Fathom DB participants may not be in Legacy Airtable (Batch 5 additions correctly in DB, never made it to old Airtable)
- "In Legacy Airtable with bio" is strong signal they WERE a member—cross-check with Fathom DB for current status
- Fathom DB is authoritative for CURRENT membership (era_member flag)

**ERA Africa Distinction:**
- Some ERA Africa attendees are ERA members (Wambui Muthee: era_member=1, era_africa=1)
- Some ERA Africa attendees are not ERA members (Arun Bangura, Chris Pilley: era_africa=1, era_member=0)
- Both flags needed in Fathom DB to track properly
- Legacy Airtable doesn't have era_africa flag—this is a Fathom DB improvement

**Data Quality Issues:**

- Name variants get merged incorrectly (Loren → Lauren, then marked for removal)
- Location errors from wrong participant attribution ("Nakavali" from different meeting)
- Spelling corrections needed (Geiversity → Geoversity)

**Common Patterns to Watch For:**

- **ERA Africa attendees:** May speak in transcripts or may be silent attendees—verify era_member vs era_africa flags
- **Private meeting participants:** NOT ERA members unless special approval—don't add to member database
- **First-person bios:** Must be rewritten in third person (caught in V4 quality check)
- **Age references:** Remove from bios (caught with Aviv Green "31-year-old")
- **Spelling/case corrections:** Do immediately, don't let propagate (Emmanuel, Geiversity examples)
- **Generic affiliations:** "This participant's company is not listed" → research further
- **Single-name entries:** Never propose additions for single names without full research

**Successful Research Patterns:**

- Town Hall presentations → Rich bio material (Eliza Herald, Juan Bernal)
- LinkedIn + Town Hall combination → Best quality bios
- Email search → Often finds full names for partial entries
- Fathom call titles → Can reveal organizational context
- Legacy Airtable → Strong signal for historical membership

**Mistakes to Avoid:**

- Stopping research too early ("needs investigation" instead of investigating)
- Confusing people with similar names/roles (Elizabeth vs Eliza)
- Attributing wrong organization affiliations (Myra/Missy confusion)
- Assuming Fathom DB participant = ERA member (must verify)
- Not checking Legacy Airtable for historical members

---

## Summary

**Total Remaining:** 5 members needing action (down from 30 in V7, 1 resolved in V8)

### Categories:

- **Remove from database:** 1 member (Lauren Miller - never confirmed as member)
- **ERA Africa attendees (minimal info):** 3 members (Malaika Patricia, Stella Nakityo, Munyembabazi Aloys)
- **Confirm status:** 1 member (Malaika Patricia marked "not a ERA" - verify flags)

### Resolved in V8:

- ✅ **Mary Ann Edwards** - Added to Fathom DB from Legacy Airtable with bio

---

## Members Needing Action

### 25. Lauren Miller [REMOVE FROM DATABASE]

**Fields:**

- **Affiliation:** Not listed
- **Location:** New York, Hudson Valley

**Notes:**

🔍 **RESEARCH:**

- Fathom Database: ERA Town Hall Meeting (New York, Hudson Valley)
- Transcripts: ❌ No speaking mentions

**USER QUESTION:** Any context about Lauren Miller? **[NO. HOW DID SHE GET INTO THE DATABASE?]**

**Action:** Resolve database entry - possibly remove if no ERA connection found

---

### 27. Malaika Patricia [ERA AFRICA; Not a ERA]

**Fields:**

- **Affiliation:** Not listed
- **Location:** Uganda

**Notes:**

🔍 **RESEARCH:**

- Fathom Database: ERA Africa (Uganda)
- Transcripts: ❌ No speaking mentions
- Collaborators: Theopista Abalo, Arun Bangura, nding'a ndikon, others

**Action:** ERA Africa attendee but not ERA member - confirm in database

---

### 28. Mary Ann Edwards [✅ RESOLVED - ADDED TO FATHOM DB]

**Fields:**

- **Email:** maedwardsrn@gmail.com
- **Affiliation:** Author
- **Bio:** "Mary Edwards maintains a food forest in her yard in Irondequoit, New York."
- **Provenance:** legacy_airtable

**Notes:**

✅ **RESOLVED:**

- Was in Legacy Airtable with "Author" affiliation
- Now added to Fathom DB with era_member=1
- Bio provided by user
- Source: Legacy Airtable migration

**Action:** ✅ Complete - no further action needed

---

### 35. Munyembabazi Aloys [ERA AFRICA - NEED MORE INFO]

**Fields:**

- **Affiliation:** Not listed
- **Location:** Unknown

**Notes:**

🔍 **RESEARCH:**

- Fathom Database: ERA Africa
- Transcripts: ❌ No speaking mentions

**Action:** Need context about Munyembabazi Aloys - any other records?

---

### 43. Stella Nakityo [ERA AFRICA - NEED MORE INFO]

**Fields:**

- **Affiliation:** Not listed
- **Location:** Unknown

**Notes:**

🔍 **RESEARCH:**

- Fathom Database: ERA Africa
- Transcripts: ❌ No speaking mentions

**Action:** Need context about Stella Nakityo

---

## V7 Processing Complete

**✅ Bios Created:** 16 members
**❌ Removed from database:** 10 members (private meetings only)
**✅ Already had bios:** 7 members (Eliza Herald, Heraclio Herrera, Jerald Katch, etc.)
**⚠️ Remaining in V8:** 7 members needing resolution

---

## Next Steps (Immediate)

1. ✅ **DONE:** Mary Ann Edwards added to Fathom DB with bio
2. Remove Lauren Miller from Fathom database
3. Confirm ERA Africa attendees' status and update flags (Malaika, Stella, Munyembabazi)
4. Update database flags for ERA Africa vs ERA member distinction

---

## Next Major Task: Legacy Airtable → Fathom DB Reconciliation

**Goal:** Ensure all historical ERA members from Legacy Airtable are represented in Fathom DB.

### Phase 1: Discovery

**Query Legacy Airtable for members with bios:**
```sql
SELECT Name, Bio, Email, Affiliated_Orgs, City_Town, Country 
FROM legacy_airtable 
WHERE Bio IS NOT NULL AND Bio != ''
ORDER BY Name;
```

**Cross-check against Fathom DB:**
```sql
SELECT name, bio, email, era_member 
FROM participants 
WHERE era_member = 1;
```

**Identify gaps:** People in Legacy Airtable with bios but NOT in Fathom DB

### Phase 2: Verification

For each gap:
1. Is this person still active/relevant? (check recent Town Halls, emails)
2. Is their bio still accurate?
3. Should they have era_member=1 in Fathom DB?

### Phase 3: Migration

For confirmed active members:
1. Add to Fathom DB with provenance_source='legacy_airtable'
2. Include bio from Legacy Airtable (edit if outdated)
3. Set era_member=1
4. Add provenance_notes if known (e.g., "Board member", "Founding member")

### Expected Findings:

- **True members not yet migrated:** Like Mary Ann Edwards—add them
- **Inactive/past members:** Document decision (keep with era_member=0? remove? note as historical?)
- **Batch 5 mystery solved:** People correctly in Fathom DB but never made it to old Airtable
- **Data quality issues:** Duplicates, spelling variants, merged identities

### Success Metric:

Every person with a bio in Legacy Airtable has been:
1. Evaluated for current membership status
2. Added to Fathom DB if appropriate (with provenance)
3. OR documented reason for exclusion

---

## Possible Future Improvements

### 1. Pre-Flight Verification Checklist

Before starting each bio enrichment cycle:

- [ ] Export fresh Legacy Airtable data (verify timestamp)
- [ ] Export fresh Fathom database (verify timestamp)
- [ ] Run sync check: Legacy Airtable members with bios vs Fathom DB
- [ ] Review previous version's learnings and corrections
- [ ] Identify any new systematic issues from recent batches
- [ ] Check for new Town Hall participants since last cycle

**Why:** We discovered Mary Ann Edwards was in Legacy Airtable but not Fathom DB—regular sync checks catch these gaps. Goal is to migrate all historical members from Legacy Airtable to Fathom DB.

### 2. Similar Names Warning System

Maintain a list of easily-confused member pairs:

- Elizabeth Morgan Tyler ⟷ Eliza Herald (both water activists)
- Any future pairs discovered

When researching someone on this list, require explicit verification step:

- "Confirming this is [Name A], NOT [Name B]"
- Check distinguishing details (location, email, specific affiliations)

**Why:** We spent significant time correcting the Elizabeth/Eliza confusion and updating database.

### 3. Affiliation Cross-Reference Database

Build a simple lookup table:

| Organization       | Known Members        | Last Verified |
| ------------------ | -------------------- | ------------- |
| Earth Law Center   | Missy Lahren (Chair) | 2025-10-28    |
| Greenbelt Movement | Wambui Muthee        | 2025-10-28    |
| Geoversity Panama  | Juan Bernal (ED)     | 2025-10-28    |

When assigning an affiliation, check if another member is already listed with that org.

**Why:** Prevents affiliation errors like attributing Earth Law Center to Myra Jackson when it's Missy Lahren's organization.

### 4. Provenance Tracking (HIGH PRIORITY)

**Add to Fathom Database schema:**

- **provenance_source:** (legacy_airtable | batch_5_addition | town_hall_2024_03_05 | private_meeting | web_form)
- **provenance_date:** (timestamp when added to Fathom DB)
- **provenance_added_by:** (script name | manual | user_name)
- **provenance_notes:** Free text field for social connections and context
  - Examples: "Invited by Russ Speer", "Presenter at Town Hall", "ERA Africa attendee", "Board member"
- **provenance_verification_status:** (confirmed_member | attendee_only | potential_member | uncertain)

**Why:** Would have immediately answered "How did Lauren Miller get in the database?" Instead of forensic research, we'd see: "Added: Batch 5, Oct 2023, execute_round5_actions.py, from 'Loren Miller' typo correction."

**Implementation:** Add these columns to participants table. Retroactively populate for existing entries where possible.

### 5. Bio Quality Checklist

Before submitting bio for approval:

- [ ] Contains current role/affiliation
- [ ] Explains ERA-relevant work
- [ ] 2-4 sentences (concise)
- [ ] No age references
- [ ] No promotional language
- [ ] Cross-checked affiliations against known members
- [ ] Verified person's identity (if similar names exist)

**Why:** Standardizes quality and catches common errors before user review.

### 6. Database Flag Validation Script

Run before/after each processing cycle:

```python
# Consistency checks:
- Anyone with era_africa=1 should have either era_member=0 or era_member=1 (not NULL)
- Anyone in Fathom DB with bio != NULL should have era_member=1 OR era_africa=1
- Anyone in Legacy Airtable with bio should be checked against Fathom DB
- Flag members with email=NULL (may need follow-up)
- Flag members with provenance_source=NULL (needs retroactive population)
- Check: Legacy Airtable count vs Fathom DB era_member=1 count
```

**Why:** Catches inconsistent flags and identifies gaps between Legacy Airtable and Fathom DB.

### 7. Separate Workflows for Different Participant Types

Create distinct processes:

**A. Full ERA Members** (era_member=1 in Fathom DB)
- Bio required
- Priority: High
- Sources: Town Halls, Legacy Airtable, LinkedIn, website
- Provenance tracking essential

**B. Legacy Airtable Members Not Yet in Fathom DB**
- Cross-check if still active
- If active: migrate to Fathom DB with bio
- Priority: High (data migration)
- Record provenance: "legacy_airtable"

**C. ERA Africa Attendees** (may or may not be members)
- Clarify membership status first (era_member flag)
- Minimal bio if not member
- Priority: Medium

**D. Private Meeting Participants**
- No bio needed unless potential member
- May track for relationship/provenance ("invited by X")
- Priority: Low

**Why:** We conflated these categories in V7. New paradigm requires distinguishing current members (Fathom DB) from historical members (Legacy Airtable).

### 8. Incremental Processing with Checkpoints

Instead of processing 30 members in one session:

- Process in batches of 5-10
- User review after each mini-batch
- Update database after each approval
- Maintain running changelog

**Why:** Easier to track changes, catch errors early, less overwhelming for user review. We had to do forensic work when the file got overwritten partway through.

### 9. Template-Based Bio Generation

Create bio templates for common roles:

**Founder/ED template:**

```
[Name] is [role] of [organization] in [location]. [He/She/They] [main work description]. [Optional: Notable achievement or ERA connection].
```

**Activist template:**

```
[Name] is a [type] activist based in [location]. [He/She/They focus on [specific issues/approaches]. [Optional: Collaboration or project highlight].
```

Reduces cognitive load, ensures consistency.

### 10. "Suspicious Pattern" Alerts

Flag for manual review:

- Member appears in database but not in any Town Hall transcript
- Member added in batch processing but not in current Airtable export
- Member has multiple conflicting locations
- Affiliation contains "Unknown" or "Not listed" but bio claims specific org

**Why:** Would have flagged Lauren Miller (added in Batch 5, never in Airtable), Mary Ann Edwards (in Airtable, zero Fathom records).

---

## Meta-Improvement: Learning Loop

After each version cycle:

1. **Document what went wrong** (not just what was fixed)
2. **Identify root causes** (not just symptoms)
3. **Update this improvements list** with concrete, actionable items
4. **Implement ONE improvement** before next cycle (not everything at once)

**Current priority recommendation:** Implement #4 (Provenance Tracking) first—it's simple, prevents most forensic work, and catches many other issues downstream.

---

## LinkedIn Profile Scraping (Active Technique)

### Purpose

Harvest professional background information from LinkedIn to inform bio drafting. This is an **active, ongoing technique** (not legacy) for gathering high-quality professional context about ERA members.

### Working Script

**File:** `linkedin_profile_fetcher.py`

**Key features:**
- Rate-limit aware (10-15 second delays between requests)
- Uses authentication cookies exported from browser session
- Extracts "About" sections and profile summaries
- Stores results in JSON format for processing
- Handles errors gracefully (continues on failures)
- Logs progress for monitoring

### Workflow

**1. Export LinkedIn Authentication Cookies**

See `cookie_export_guide_linkedin.md` for detailed instructions:
- Use browser extension (e.g., "Get cookies.txt")
- Export cookies while logged into LinkedIn
- Save as `linkedin_cookies.json`
- Keep secure (contains authentication)

**2. Compile URL List**

Create `linkedin_urls_to_scrape.txt` with one URL per line:
```
https://www.linkedin.com/in/username1
https://www.linkedin.com/in/username2
```

**Sources for URLs:**
- ERA member LinkedIn fields from database
- Google/web search for member names
- LinkedIn Connections export (`LinkedInConnections.csv`)
- Email signatures
- Member-provided links

**3. Run Scraping Script**

```bash
cd /Users/admin/ERA_Admin/integration_scripts/member_enrichment
python3 linkedin_profile_fetcher.py
```

**4. Monitor Progress**

- Script outputs status for each profile
- Check `linkedin_about_sections.json` for results
- Also creates `linkedin_profiles_extracted.json` with full data
- Runs in background, can take 30+ minutes for large batches

**5. Process Results**

Results stored in JSON files:
- `linkedin_about_sections.json` - "About" sections only
- `linkedin_profiles_extracted.json` - Full profile data
- `linkedin_status.json` - Scraping status/errors

### Critical Principle: ADAPT, Don't Copy-Paste

**❌ WRONG approach:**
```
Bio: [Copy entire LinkedIn About section verbatim]
```

**✅ CORRECT approach:**
1. **Extract** professional background and credentials
2. **Identify** ERA-relevant skills, experience, or interests
3. **Craft** personalized bio showing ERA connection
4. **Integrate** Town Hall participation or contributions
5. **Curate** for consistency of tone and relevance to ecosystem restoration

**Example transformation:**

**LinkedIn "About" (generic):**
> "Experienced sustainability professional with 15 years in environmental consulting. Passionate about climate solutions and community engagement. MBA from Stanford, certified in project management."

**Curated ERA Bio (contextual):**
> "John Smith is a sustainability consultant based in California who participated in ERA's Town Hall discussions on regenerative agriculture financing. With 15 years of experience in environmental consulting, he focuses on climate adaptation strategies for rural communities."

### Rate Limits & Best Practices

**LinkedIn's anti-scraping measures:**
- Too-fast requests → temporary blocks
- Missing authentication → limited data
- Unusual patterns → account flags

**Our mitigation:**
- 10-15 second delays (configurable in script)
- Authenticated requests via cookies
- Random delay variation
- Small batch sizes (10-20 at a time)
- Monitor for errors, pause if issues

**If blocked:**
- Wait 24 hours before retrying
- Check cookie validity (may need re-export)
- Reduce batch size
- Increase delay between requests

### Data Files

**Active/Current:**
- `linkedin_about_sections.json` - Recent scraping results
- `linkedin_cookies.json` - Authentication (keep secure)
- `LinkedInConnections.csv` - Your LinkedIn connections export (reference)

**Reference/Historical:**
- `linkedin_profiles_curated.json` - Previously curated profiles
- `linkedin_urls_to_scrape.txt` - Queue of URLs to process

### Integration with Bio Workflow

**When to use LinkedIn scraping:**

1. **New member without bio** - Primary research source for professional background
2. **Partial bio needing enrichment** - Fill in credentials, current role
3. **Verification** - Confirm affiliations and roles mentioned elsewhere
4. **Discovery** - Find ERA-relevant experience not obvious from Town Halls

**LinkedIn data prioritization:**
- Current role and organization (high priority)
- Relevant credentials/education (medium priority)
- Career history (context only)
- Skills and endorsements (rarely useful)
- Generic mission statements (usually ignore)

### Quality Control

**Red flags in LinkedIn data:**
- Promotional language ("world-leading," "innovative solutions")
- Buzzwords without substance ("synergy," "thought leader")
- Generic mission statements (not person-specific)
- Outdated information (check dates)
- Profile hasn't been updated in years

**What to extract:**
- Current job title and organization
- Relevant educational background
- Specific technical skills
- Geographic location
- Industry/sector experience
- Projects or achievements (if ERA-relevant)

### Troubleshooting

**Script fails immediately:**
- Check `linkedin_cookies.json` exists and is valid
- Verify you're in correct directory
- Check Python dependencies installed

**Getting blocked/limited:**
- Increase delay in script (edit DELAY_SECONDS variable)
- Reduce batch size
- Wait 24 hours before retrying
- Re-export cookies from fresh browser session

**No data extracted:**
- Profile may be private (requires connection)
- URL format incorrect (check for /in/ pattern)
- Profile deleted or doesn't exist
- Need to be logged in (check cookies)

### Script Maintenance

**Active file:** `linkedin_profile_fetcher.py`

**Key variables to adjust:**
- `DELAY_SECONDS` - Time between requests (default: 12)
- `RANDOM_DELAY_RANGE` - Variation in delay (default: 3)
- `COOKIE_FILE` - Path to cookies JSON
- `URL_FILE` - Path to URLs list

**Future improvements considered:**
- Batch progress saving (resume mid-batch)
- Better error reporting
- Profile change detection (re-scrape if updated)
- Integration with database (auto-populate LinkedIn URLs)

---

## Files in This Component

**Active Working Documents:**
- `ERA_MEMBERS_LACKING_BIOS_V8.md` - Current working document
- `V8_REWRITE_SUMMARY.md` - Summary of V8 paradigm shift
- `V7_TO_V8_PROCESSING_SUMMARY.md` - Processing notes

**Active Scripts:**
- `linkedin_profile_fetcher.py` - LinkedIn scraping (documented above)
- `aggregate_member_info.py` - Compile member data from multiple sources
- `identify_members_needing_bios.py` - Find members lacking bios
- `update_airtable_bios.py` - Sync bios to Airtable (Legacy)

**Active Data:**
- `linkedin_about_sections.json` - Recent scraping results
- `LinkedInConnections.csv` - LinkedIn connections export
- `google_contacts.csv` - Google contacts export

**Documentation:**
- `cookie_export_guide_linkedin.md` - How to export LinkedIn cookies
- `README.md` - Component overview (to be updated)

**Historical:**
- See `/historical/member_enrichment_archive_20251028/` for V1-V7, batch processing, working notes
