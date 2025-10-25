# Intelligent Cleanup Analysis - Round 2
**Date:** October 25, 2025  
**Method:** Read files to understand purpose, not just list them

---

## Understanding from Reading

### Phase 4B-2 is COMPLETE (Oct 23-24)
- All 280 cases processed
- 100% validation achieved
- No future participant processing planned yet (Phase 4C is "future")
- Scripts that ran once for specific batch work are now historical

### Phase 5T is READY
- export_townhalls_to_landscape.py (active, needs to stay)

### Phase 4C is "FUTURE" 
- When 223 new participants need processing
- Will use: generate_batch_CANONICAL.py, PAST_LEARNINGS.md, add_to_airtable.py

---

## Categories

### 1. ONE-TIME EXECUTION SCRIPTS (Completed, Archive)

**These executed specific batches that are DONE:**

**execute_206_categorizations.py** (12K)
- Purpose: Execute the 206 cases from all_206_categorizations.json
- Status: Ran once Oct 24, produced execution_log
- Judgment: **ARCHIVE** - specific to that batch, won't run again

**execute_106_cases.py** (11K)
- Purpose: Execute the 106 remaining cases from batch_106_approved_cases.json
- Status: Ran once Oct 24, produced execution_log
- Judgment: **ARCHIVE** - specific to that batch, won't run again

**Why archive not delete:** These show the execution pattern IF we need to run similar batch execution in Phase 4C. But they're not reusable as-is (hardcoded to specific JSON files we already archived).

---

### 2. ONE-TIME COMPILATION/EXTRACTION SCRIPTS (Archive)

**compile_all_categorizations.py** (2K)
- Purpose: Compile 206 categorizations from interactive Claude session
- Status: Generated all_206_categorizations.json (now archived)
- Judgment: **ARCHIVE** - job done, JSON compiled

**extract_all_206_from_markdown.py** (2K)
- Purpose: Extract cases from markdown
- Status: Part of 206 case compilation workflow
- Judgment: **ARCHIVE** - specific to that batch

**final_extract_206.py** (3K)
- Purpose: Final extraction for 206 cases
- Status: Part of 206 case compilation workflow
- Judgment: **ARCHIVE** - specific to that batch

**interactive_categorization.py** (4K)
- Purpose: Interactive tool that forced Claude to judge each of 106 cases
- Status: Generated batch_106_approved_cases.json (now archived)
- Judgment: **ARCHIVE** - specific batch tool, job complete

**Why these matter:** They show HOW the 206/106 decisions were compiled. Historical reference for the process.

---

### 3. DIAGNOSTIC/AUDIT SCRIPTS (One-time fixes, Archive)

**diagnostic_report.py** (9K)
- Purpose: "Analyze all past decisions vs current database state" (line 3)
- Status: Diagnostic to find discrepancies during Phase 4B-2
- Judgment: **ARCHIVE** - Phase 4B-2 complete, diagnostic done

**diagnostic_report_v2.py** (11K)
- Purpose: Version 2 of diagnostic (improved)
- Status: Same as above
- Judgment: **ARCHIVE** - diagnostic complete

**audit_database_vs_decisions.py** (5K)
- Purpose: "Find EVERY discrepancy" (line 5) - comprehension phase
- Status: Audit to understand Phase 4B-2 execution issues
- Judgment: **ARCHIVE** - audit complete, issues resolved

**fix_step1_drops.py** (4K)
- Purpose: "Process DROP decisions... Run on small sample first" (line 5-6)
- Status: One-time fix for DROP decisions during Phase 4B-2
- Judgment: **ARCHIVE** - fix applied, problem solved

**Why archive:** These diagnosed and fixed specific Phase 4B-2 issues. Done. But show problem-solving approach.

---

### 4. WORKING CSVs (Completed work, Archive or Delete)

**phase4b2_approvals_batch5_20251023.csv** (57 lines)
- Purpose: Batch 5 approvals from Phase 4B-2
- Status: Historical batch data, already in past_decisions/ folder
- Judgment: **CHECK** - Is this a duplicate of one in past_decisions/?

**phase4b2_approvals_batch5_FIXED.csv** (57 lines - identical)
- Purpose: Fixed version of batch 5
- Status: Historical
- Judgment: **DELETE** or **ARCHIVE** - duplicate, batch complete

**phase4b2_approvals_CURRENT.csv** (31 lines)
- Purpose: "Current" approvals - but Phase 4B-2 is COMPLETE
- Status: Stale working file
- Judgment: **CHECK CONTENT** then likely DELETE or ARCHIVE

**redundancy_merge_actions.csv** (55 lines)
- Purpose: Alias resolution merge actions (from today's work!)
- Status: ACTIVE - we used this today for alias cleanup
- Judgment: **KEEP** - may need for future redundancy cleanup

---

### 5. DOCUMENTATION - Historical Summaries (Archive)

**categorization_summary.md** (70 lines)
- Purpose: Summary of 206 case categorizations with action items
- Date: 2025-10-24
- Content: Investigation notes (Michael, Moses, Samuel), corrections made
- Judgment: **ARCHIVE** - Historical record of batch work, completed

**README_CREATE_FULL_JSON.md** (46 lines)
- Purpose: Instructions for creating all_206_categorizations.py
- Status: Instructions for task that's DONE (JSON already created and archived)
- Judgment: **ARCHIVE** - Process documentation, task complete

**Why archive:** Shows HOW the work was done. Educational for understanding the process.

---

### 6. DATA FILES (Check purpose)

**town_hall_agenda_index.json** (19K)
- Purpose: Town Hall agenda data
- Status: **READ to understand** - Is this for Phase 5T? Or historical?
- Judgment: **NEEDS READING**

**credentials.json, token_*.json** (gitignored)
- Purpose: OAuth credentials
- Judgment: **KEEP** - needed for Gmail/Drive API access

**create_full_json.sh** (690B)
- Purpose: Shell script to create full JSON
- Status: Related to 206 case compilation
- Judgment: **ARCHIVE** - task complete

---

## REUSABLE TOOLS (KEEP - Future Use)

These are generalizable, not tied to specific batches:

✅ **generate_batch_CANONICAL.py** - Canonical batch generator for Phase 4C
✅ **generate_html_from_intermediate.py** - HTML generator from intermediate JSON
✅ **generate_member_review_html.py** - Member review HTML generator
✅ **add_to_airtable.py** - Reusable Airtable addition module
✅ **phase4b1_enrich_from_airtable.py** - Fuzzy matching pipeline
✅ **execute_phase4b2_actions.py** - Generic executor (MAY be reusable for Phase 4C?)
✅ **comprehensive_validation.py** - Post-execution verification tool
✅ **export_townhalls_to_landscape.py** - ACTIVE for Phase 5T
✅ **build_alias_resolution_table.py** - Alias system builder
✅ **query_participant_sessions.py** - Query tool by name/alias
✅ **detect_participant_redundancies.py** - Duplicate detection
✅ **execute_redundancy_merges.py** - Merge execution with backups
✅ **deduplicate_participants.py** - Deduplication tool
✅ **merge_participants_properly.py** - Proper merge tool
✅ **download_town_hall_agendas.py** - Town Hall data downloader
✅ **quick_sync_member_status.py** - Quick sync utility
✅ **api_enrich_remaining.py** - API enrichment (may be useful for Phase 4C?)

---

## Proposed Actions

### ARCHIVE to archive/completed_phase4b2/execution_scripts/
- execute_206_categorizations.py
- execute_106_cases.py
- compile_all_categorizations.py
- extract_all_206_from_markdown.py
- final_extract_206.py
- interactive_categorization.py
- diagnostic_report.py
- diagnostic_report_v2.py
- audit_database_vs_decisions.py
- fix_step1_drops.py
- create_full_json.sh

### ARCHIVE to archive/completed_phase4b2/documentation/
- categorization_summary.md
- README_CREATE_FULL_JSON.md

### INVESTIGATE then ARCHIVE or DELETE
- phase4b2_approvals_batch5_*.csv (check if duplicates of past_decisions/)
- phase4b2_approvals_CURRENT.csv (check content, likely stale)

### READ to understand purpose
- town_hall_agenda_index.json (Phase 5T data? Or historical?)

### KEEP
- All REUSABLE TOOLS listed above
- redundancy_merge_actions.csv (active)
- credentials.json, token_*.json (gitignored, needed)

---

## Questions for User

1. **execute_phase4b2_actions.py** (20K) - Generic executor. Is this reusable for Phase 4C or specific to 4B-2 workflow?

2. **comprehensive_validation.py** (3K) - Post-execution validator. Reusable or specific to Phase 4B-2?

3. **api_enrich_remaining.py** (9K) - Says "ONE-TIME cleanup script" in header but could be useful for Phase 4C?

4. **quick_sync_member_status.py** (3K) - Purpose unclear from filename. Read or keep?

---

## Expected Result

**Current:** 48 files in root
**After Round 2:** ~25-30 files in root (reusable tools + active data)
**Archived:** ~15-20 files (one-time execution, diagnostics, historical docs)

---

**Method:** Read file headers and understand purpose, not just list by date/size. Applied multi-factor judgment based on:
- Completion status of Phase 4B-2
- Reusability for Phase 4C
- Active use for Phase 5T
- Historical vs operational value
