# Member Enrichment Archive (October 28, 2025)

**Archive Date:** October 28, 2025  
**Reason:** Consolidation after V1-V8 completion, prepare for wireframe integration  
**Current Work:** See `/integration_scripts/member_enrichment/ERA_MEMBERS_LACKING_BIOS_V8.md`  
**Archival Process:** See [ARCHIVE_PLAN_20251028.md](ARCHIVE_PLAN_20251028.md) for detailed plan and execution log

---

## What This Archive Contains

Historical materials from the member bio enrichment project (V1-V8 iterations, Oct 2025).

### Purpose of Archival

These documents represent **intermediate understanding** during active development. The **refined, current understanding** is captured in:
- **V8 Document:** `/integration_scripts/member_enrichment/ERA_MEMBERS_LACKING_BIOS_V8.md`
- **Wireframe:** (to be added to `/docs/NAVIGATION_WIREFRAME.md`)

This archive preserves working notes, version history, and completed phases for **reference only**—not as authoritative documentation.

---

## Archive Structure

### `/working_notes/`
**Category D files** - "Inside baseball" working documents representing intermediate understanding:
- `BIO_GENERATION_PLAN.md` - Oct 26 planning (superseded by V8 workflow)
- `FEEDBACK_LOOP.md` - Separate file approach (superseded by inline editing in V8)
- `BATCH_4-7_COMPLETION_REPORT.md` - Stats now captured in V8
- `BIO_SYNC_SESSION_SUMMARY.md` - Process notes refined in V8
- `ERA_AFRICA_ENRICHMENT_SUMMARY.md` - Findings integrated into V8
- `V6_BIO_IMPROVEMENTS.md`, `V7_RESEARCH_SUMMARY.md` - Version learnings now in V8
- `CONTEXT_RECOVERY.md` (member_enrichment version) - Superseded

**Status:** These represent working understanding during development, not final process.

### `/versions/`
Version history V1 through V7:
- `ERA_MEMBERS_LACKING_BIOS.md` (original, V1)
- `ERA_MEMBERS_LACKING_BIOS_V2.md` through `V7.md`
- `ERA_MEMBERS_V6_ENRICHED.md`
- `ENRICHMENTS_FOR_REVIEW.md`
- `NEW_ENRICHMENTS_FROM_FUZZY_MATCH.md`

**Progress:** 62 → 30 → 5 members remaining (V1 → V7 → V8)

### `/batch_processing/`
Complete batch processing phase:
- `batches/` directory (entire structure)
  - Batch 1-8 documents
  - Batch learnings (BATCH*_LEARNINGS.md)
  - Approved bios
  - LinkedIn profiles by batch
  - Aggregated data

**Status:** Batch processing phase complete, LinkedIn scraping technique now active (see V8)

### `/diagnostics/`
Quality control and analysis documents:
- `DIAGNOSTIC_SUMMARY.md`
- `FINAL_DIAGNOSTIC_SUMMARY.md`
- `PRIORITY_0_DIAGNOSTIC.md`
- `PRIORITY_0_MATCHES_DIAGNOSTIC.md`
- `DUPLICATES_DIAGNOSTIC.md`
- `FUZZY_MATCH_FINDINGS.md`
- `AIRTABLE_DUPLICATES.md`

**Status:** Issues identified and resolved, patterns captured in V8

### `/linkedin_batch_outputs/`
Old LinkedIn scraping batch outputs:
- `LINKEDIN_PROFILES_*.md` and `.html` files
- `LINKEDIN_ABOUT_SECTIONS.md`
- `NEXT_3_LINKEDIN_PROFILES.md`

**Note:** LinkedIn scraping is **ACTIVE technique** (not legacy), see V8. These are just old batch output files.

### `/obsolete_scripts/`
One-off and superseded scripts:
- Various `scrape_*.py` and `scrape_*.log` files (batch-specific runs)
- `create_v7_from_v6.py` (version migration)
- `bio_writer_pilot.py` (pilot phase)
- `rescrape_16_fixed.py` (one-off fix)
- Other task-specific scripts

**Note:** LinkedIn scraping pattern still active, these are just specific instances.

### `/trash/`
Duplicates and true garbage:
- `ERA_MEMBERS_LACKING_BIOS_V6 copy.md` (duplicate)
- Empty JSON files
- Other redundant copies

---

## Key Statistics

**V1 → V8 Progress:**
- **Started:** 62 members lacking bios
- **V7 Completed:** 16 bios created, 10 non-members removed
- **V8 Remaining:** 5 members (down to final handful)

**Batch Processing (Complete):**
- Batches 1-8 processed
- Multiple LinkedIn scraping rounds
- Established active LinkedIn technique (documented in V8)

**Major Learnings Captured in V8:**
- ERA member definition (Town Hall attendance required)
- Hand-authored bio rationale (vs generic LinkedIn)
- Research workflow (Fathom DB first, then sources)
- Common patterns to watch for
- Mistakes to avoid
- LinkedIn scraping as active technique

---

## Current State (October 28, 2025)

**Active Work:**
- Document: `/integration_scripts/member_enrichment/ERA_MEMBERS_LACKING_BIOS_V8.md`
- Remaining: 5 members needing resolution
- Next: Legacy Airtable → Fathom DB reconciliation

**Active Techniques:**
- LinkedIn Profile Scraping (documented in V8)
- Town Hall transcript research
- Email search
- Fathom DB queries

**Active Scripts:**
- `linkedin_profile_fetcher.py` (working, documented in V8)
- `aggregate_member_info.py`
- `identify_members_needing_bios.py`
- `update_airtable_bios.py`

---

## How to Use This Archive

**For Context Recovery:**
1. Start with V8 (current refined understanding)
2. Reference this archive for historical decisions if needed
3. Batch learnings are consolidated in V8 "Common Patterns" section

**For Historical Research:**
- Version history shows evolution of process
- Working notes show intermediate thinking
- Batch processing shows what was tried

**What NOT to do:**
- Don't treat working notes as authoritative (they're superseded)
- Don't resurrect old workflows without checking V8 first
- Don't assume patterns here are current (V8 has refined versions)

---

## Archive Rationale

**Why archive instead of delete:**
- Preserves decision history
- Shows evolution of understanding
- Reference for "why we tried X"
- Data for future meta-analysis

**Why not in wireframe:**
- Working notes represent intermediate understanding
- V8 has refined/superior patterns
- These are "inside baseball" not needed for system understanding
- Wireframe is for current system knowledge, not process archaeology

---

## Archival Process Documentation

**See:** [ARCHIVE_PLAN_20251028.md](ARCHIVE_PLAN_20251028.md)

Complete details on:
- Files that remained active vs archived
- Safety measures and rollback procedures
- Archive structure and organization
- Script execution (`archive_files_20251028.sh`)
- Before/after comparison

---

**Back to:** [/integration_scripts/member_enrichment/](../../integration_scripts/member_enrichment/) | [Current V8](../../integration_scripts/member_enrichment/ERA_MEMBERS_LACKING_BIOS_V8.md)
