# integration_scripts/member_enrichment/README.md

### 1. Overview

**Purpose:** ERA member bio enrichment and profile completion

This component manages the bio generation and profile enrichment process for ERA members, ensuring every confirmed member has a complete, accurate bio in the Fathom database while removing non-members who entered incorrectly.

**What this component does:**
- Identifies ERA members lacking biographical information
- Conducts multi-source research (LinkedIn, Town Halls, email, Fathom DB)
- Drafts contextual, personalized bios (not generic LinkedIn summaries)
- Manages iterative review cycles (V1 → V8, from 62 to 5 members remaining)
- Maintains active LinkedIn scraping technique for professional background

**Key insight:** Hand-authored bios work best because they capture what makes each person unique to ERA, integrating professional background with ERA engagement and reflecting actual contributions discussed in Town Halls.

### 2. Orientation - Where to Find What

**You are at:** Member bio enrichment component

**What you might need:**
- **Parent** → [integration_scripts/README.md](../README.md) - Integration overview
- **Current work** → ERA_MEMBERS_LACKING_BIOS_V8.md - Active document (5 members remaining)
- **System principles** → [WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md) - System-wide philosophy
- **Historical context** → archive/ - V1-V7, batch processing, working notes

### 3. Principles

**System-wide:** See [WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md)

**Member enrichment specific:**

**1. ERA Member Definition**
- A person is an ERA member if and only if:
  - They attended a Town Hall meeting (introduced, no objections, week passed), OR
  - Special decision from Jon Schull
- The database contains non-members - must verify Town Hall attendance before treating as member

**2. Hand-Authored Bio Rationale**
- Capture what makes each person unique to ERA
- Integrate professional background with ERA engagement  
- Reflect actual contributions and interests discussed in Town Halls
- Avoid generic LinkedIn summary language
- Maintain consistent tone and relevance to ecosystem restoration

**3. Intelligent Assistant Pattern**
- AI proposes → Human edits → AI updates database
- No autonomous changes without explicit approval
- Evidence-rich outputs with source links
- Learn from corrections and improve

**4. Quality Over Speed**
- Thoughtful, personalized bios that reflect ERA engagement
- Research thoroughly before proposing actions
- Multiple source synthesis (LinkedIn + Town Halls + email + Fathom DB)
- 2-4 sentences typical, contextual not promotional

### 4. Specialized Topics

#### Current Status (October 28, 2025)

**V8 Progress:**
- **Remaining:** 5 members needing bios or resolution
- **Started (V1):** 62 members
- **V7 Completed:** 16 bios created, 10 non-members removed  
- **Categories remaining:**
  - 1 to remove (never confirmed as member)
  - 3 ERA Africa attendees (minimal info)
  - 1 ERA member (full research needed)

**Archive completed:** V1-V7, batch processing, working notes moved to `archive/`

#### Sources of Truth

1. **Fathom Database** - Primary source for current membership and bios
2. **Legacy Airtable** - Historical record (may be stale, use for cross-checking)
3. **Town Hall Transcripts** - Rich source for bio content and verification
4. **Email** - jschull@gmail.com inbox and sent folders
5. **LinkedIn Profiles** - Professional background (active scraping technique)
6. **Web Search** - External verification and additional details
7. **Future: New Airtable** - Will mirror Fathom DB as user-friendly interface

#### Research Workflow

For each member:
1. Check Fathom Database first (era_member flag, existing bio, call history)
2. Search Town Hall transcripts (speaking roles, presentations, context)
3. Check Legacy Airtable (was this person historically a member?)
4. Search Fathom database for call titles and collaborators
5. Check emails (jschull@gmail.com inbox/sent)
6. Check LinkedIn for professional details (see LinkedIn Scraping below)
7. Web search for affiliations and background
8. For deep digging: Use Fathom API with date-range filtering

#### LinkedIn Profile Scraping (Active Technique)

**Purpose:** Harvest professional background to inform bio drafting

**Working Script:** `linkedin_profile_fetcher.py`

**Key features:**
- Rate-limit aware (10-15 second delays)
- Browser cookie authentication
- Extracts "About" sections and summaries
- JSON output for processing
- Error handling and progress logging

**Workflow:**
1. Export LinkedIn cookies (see `cookie_export_guide_linkedin.md`)
2. Compile URL list (`linkedin_urls_to_scrape.txt`)
3. Run: `python3 linkedin_profile_fetcher.py`
4. Monitor: Outputs to `linkedin_about_sections.json`
5. **ADAPT, don't copy-paste:** Curate for ERA relevance

**Critical Principle:** LinkedIn provides raw material, NOT final bios
- Extract professional background and credentials
- Identify ERA-relevant skills/experience
- Craft personalized bio showing ERA connection
- Integrate Town Hall participation
- Curate for consistency and relevance to ecosystem restoration

**Rate limits:**
- 10-15 second delays between requests
- Small batch sizes (10-20 at a time)
- If blocked: wait 24 hours, re-export cookies, reduce batch size

**Data files:**
- `linkedin_about_sections.json` - Recent scraping results
- `linkedin_cookies.json` - Authentication (keep secure)
- `LinkedInConnections.csv` - Connections export (reference)
- `cookie_export_guide_linkedin.md` - How-to guide

#### Bio Standards

**What makes a good ERA bio:**
- 2-4 sentences typical
- Focus on work relevant to ecosystem restoration
- Include current role and organization
- Highlight ERA-relevant contributions or interests
- Third person (never first person)
- No age references
- Avoid overly promotional language
- Integrate Town Hall participation when relevant

**Example:**
> "Sarah Chen is a marine ecologist at Ocean Conservation Institute in California. Her research focuses on kelp forest restoration and community-based ocean stewardship. She has presented at ERA Town Halls on innovative approaches to engaging coastal communities in ecosystem monitoring."

#### Member Verification

**CRITICAL:** Database contains non-members

**Before treating someone as member:**
1. Verify Town Hall attendance (check transcripts, Fathom DB records)
2. Check Legacy Airtable for historical membership
3. If neither: Flag for removal or special approval

**Common mistakes to avoid:**
- Assuming Fathom DB participant = ERA member (must verify)
- Private meeting participants ≠ ERA members (unless special approval)
- ERA Africa attendees may not be full ERA members (check era_africa flag)

#### Version History & Learnings

**V1 → V8 Evolution:**
- V1-V3: Initial identification and research (62 → 30 members)
- V4-V5: Quality improvements, first-person bio fixes, age reference removal
- V6: ERA Africa enrichment, LinkedIn batch processing
- V7: Major push (16 bios created, 10 non-members removed, 30 → 14 remaining)
- V8: Paradigm shift to Fathom DB as primary source (14 → 5 remaining)

**Key learnings captured in V8:**
- Common patterns to watch for (name confusion, affiliation errors)
- Successful research patterns (Town Hall presentations + LinkedIn = best bios)
- Mistakes to avoid (stopping research early, confusing similar names)
- ERA Africa vs ERA member distinction
- Provenance tracking importance

See `archive/` for complete version history and batch processing records.

#### Active Scripts

**`linkedin_profile_fetcher.py`** - LinkedIn scraping with rate limiting and authentication

**`aggregate_member_info.py`** - Compile member data from multiple sources

**`identify_members_needing_bios.py`** - Find members lacking bios

**`update_airtable_bios.py`** - Sync bios to Legacy Airtable

**`read_linkedin_profiles.py`** - Parse LinkedIn data

#### Active Data Files

**Working documents:**
- `ERA_MEMBERS_LACKING_BIOS_V8.md` - Current work (5 remaining)
- `V8_REWRITE_SUMMARY.md` - Paradigm shift documentation
- `V7_TO_V8_PROCESSING_SUMMARY.md` - Recent processing notes

**LinkedIn data:**
- `linkedin_about_sections.json` - Recent scraping results
- `linkedin_cookies.json` - Authentication
- `linkedin_urls_to_scrape.txt` - Queue
- `linkedin_status.json` - Scraping status

**Reference data:**
- `LinkedInConnections.csv` - LinkedIn connections export
- `google_contacts.csv` - Google contacts export

#### Files in This Component

**Active (in member_enrichment/):**
- README.md
- ERA_MEMBERS_LACKING_BIOS_V8.md
- V8_REWRITE_SUMMARY.md
- V7_TO_V8_PROCESSING_SUMMARY.md
- linkedin_profile_fetcher.py
- aggregate_member_info.py
- identify_members_needing_bios.py
- update_airtable_bios.py
- read_linkedin_profiles.py
- cookie_export_guide_linkedin.md
- Active data files (JSON, CSV)

**Historical (archived):**
- V1-V7 versions → `archive/versions/`
- Batch processing → `archive/batch_processing/`
- Working notes → `archive/working_notes/`
- Diagnostics → `archive/diagnostics/`
- Obsolete scripts → `archive/obsolete_scripts/`

See archive README for complete structure and explanation.

#### Future Improvements

**Considered for future cycles:**
1. Provenance tracking (source_of_bio, date_added fields)
2. Member verification checklist (automated Town Hall attendance check)
3. Database flag validation script (era_member/era_africa consistency checks)
4. Bio quality pre-check (automated first-person detection, age reference removal)
5. Separate workflows for ERA members vs ERA Africa attendees
6. Batch size optimization (5-10 members per review cycle)
7. Template-based bio generation (common role templates)
8. Suspicious pattern alerts (member in DB but not in Town Halls)

See V8 "Possible Future Improvements" section for complete list with rationale.

**Back to:** [integration_scripts/README.md](../README.md) | [/README.md](../../README.md)