# integration_scripts Directory Inventory
**Date:** October 25, 2025  
**Purpose:** Systematic categorization for cleanup

---

## Context from Reading

**Phase 4B-2 Status:** ✅ COMPLETE (Oct 23, 2025)
- 280 cases processed, 100% validation achieved
- Completion documented in PHASE4B2_COMPLETION_SUMMARY.md
- Working files marked for "archive or delete" (line 209)

**Phase 5T Status:** 🎯 READY (per README line 42-44)
- export_townhalls_to_landscape.py reinstated (exists, Oct 24)
- Prerequisites met

---

## Files by Category

### 1. ACTIVE CORE SCRIPTS (Keep - Future Use)

**For Phase 5T (Town Hall visualization):**
- `export_townhalls_to_landscape.py` (15K, Oct 24) - ACTIVE for Phase 5T

**For Phase 4C (future participants):**
- `generate_batch_CANONICAL.py` (10K) - Canonical batch generator
- `add_to_airtable.py` (8K) - Reusable Airtable module
- `phase4b1_enrich_from_airtable.py` (41K) - Fuzzy matching pipeline

**For general use:**
- `build_alias_resolution_table.py` (11K) - Alias system
- `query_participant_sessions.py` (4K) - Query tool
- `detect_participant_redundancies.py` (9K) - Duplicate detection
- `execute_redundancy_merges.py` (6K) - Merge execution
- `deduplicate_participants.py` (7K) - Deduplication tool
- `merge_participants_properly.py` (8K) - Merge tool
- `download_town_hall_agendas.py` (4K) - Town Hall data

---

### 2. DOCUMENTATION (Keep - Active Reference)

**Active:**
- `README.md` (13K) - Component overview
- `ALIAS_RESOLUTION_README.md` (4K) - Alias system docs
- `PAST_LEARNINGS.md` (29K) - 300+ patterns (ACTIVE for Phase 4C)
- `AI_ASSISTANT_CONTEXT_RECOVERY.md` (13K) - AI workflow guide
- `.cascade_guidance.md` (2K) - Cascade-specific guidance

**Completion records (archive candidate but keep for now):**
- `PHASE4B2_COMPLETION_SUMMARY.md` (9K) - Phase 4B-2 summary
- `CLEANUP_SUMMARY.md` (4K) - Oct 23 cleanup notes
- `POST_CLEANUP_TODOS.md` (2K) - Identified concerns
- `README_CREATE_FULL_JSON.md` (1K) - JSON creation docs
- `categorization_summary.md` (3K) - Categorization notes

---

### 3. COMPLETED WORK - PHASE 4B-2 (Archive Candidates)

**Batch 10 HTML files (7 files, ~500K total):**
- `BATCH10_FINAL_104items_20251023_2123.html` (35K)
- `BATCH10_FINAL_104items_20251023_2127.html` (90K)
- `BATCH10_FINAL_104items_20251023_2130.html` (90K)
- `BATCH10_FINAL_104items_20251023_2137.html` (90K)
- `BATCH10_FINAL_104items_20251023_2152.html` (90K)
- `BATCH10_FINAL_104items_REVIEWED.html` (36K)
- `BATCH10_FINAL_38items_20251023_2215.html` (36K)

**Decision records (keep - may need for analysis):**
- `all_206_categorizations.json` (35K) - 174 cases from conversation
- `batch_106_approved_cases.json` (21K) - 106 remaining cases
- `redundancy_merge_actions.csv` (3K) - Alias resolution merges

**Execution scripts (archive - completed):**
- `execute_206_categorizations.py` (12K)
- `execute_106_cases.py` (11K) 
- `execute_phase4b2_actions.py` (20K) - Generic executor (keep?)
- `comprehensive_validation.py` (3K)
- `all_206_categorizations.py` (36K)
- `all_206_categorizations_COMPLETE.py` (889B)
- `all_206_categorizations_EXTRACTED.py` (483B)
- `compile_all_categorizations.py` (2K)
- `extract_all_206_from_markdown.py` (2K)
- `final_extract_206.py` (3K)
- `interactive_categorization.py` (4K)

**Working CSVs (mostly empty, delete):**
- `phase4b2_approvals_CURRENT.csv` (1K)
- `phase4b2_approvals_batch5_20251023.csv` (2K)
- `phase4b2_approvals_batch5_FIXED.csv` (2K)
- `batch2_partial_decisions.csv` (0B) - EMPTY
- `batch3_corrections.csv` (0B) - EMPTY
- `phase4b2_batch9_SKIP.csv` (0B) - EMPTY

---

### 4. GITIGNORED FILES (Not tracked, verify then delete)

**Per .gitignore lines 8-20:**
- `credentials.json` (413B) - Gmail auth (KEEP, gitignored)
- `token_jschull.json` (738B) - OAuth token (KEEP, gitignored)
- `token_jschull_drive.json` (689B) - Drive OAuth (KEEP, gitignored)
- `execution_log_*.json` (5 files, ~160K) - Execution logs (DELETE)
- `member_review_*.html` (6 files, 10MB!) - Phase 4B-1 reviews (DELETE)
- `phase4b1_APPROVALS_*.html` (2 files, 216K) - Phase 4B-1 (DELETE)
- `audit_report.csv` (30K) - Diagnostic (DELETE)
- `diagnostic_report_detailed.csv` (26K) - Diagnostic (DELETE)
- `diagnostic_report_v2_detailed.csv` (29K) - Diagnostic (DELETE)
- `extracted_cases.json` (2B) - Nearly empty (DELETE)

---

### 5. SPECIALIZED/UTILITY SCRIPTS (Review Purpose)

**API/enrichment:**
- `api_enrich_remaining.py` (9K) - API enrichment tool
- `quick_sync_member_status.py` (3K) - Quick sync tool

**Diagnostics:**
- `diagnostic_report.py` (9K)
- `diagnostic_report_v2.py` (11K)
- `audit_database_vs_decisions.py` (5K)
- `fix_step1_drops.py` (4K)

**HTML generation:**
- `generate_member_review_html.py` (19K)
- `generate_html_from_intermediate.py` (9K)

**Unknown purpose - need to read:**
- `create_full_json.sh` (690B)
- `town_hall_agenda_index.json` (19K) - Data file?

---

### 6. EMPTY FILES (Delete)

- `batch2_partial_decisions.csv` (0B)
- `batch3_corrections.csv` (0B)
- `phase4b2_batch9_SKIP.csv` (0B)
- `REDUNDANCY_RESOLUTIONS.md` (0B) - Created but never populated

---

## Cleanup Recommendations

### Phase 1: Safe Cleanup (Low Risk)

**DELETE immediately:**
- Empty files (4 files, 0 bytes)
- Gitignored working files already in .gitignore (execution logs, review HTMLs, diagnostic CSVs)
- **Space saved:** ~11MB

### Phase 2: Archive Completed Work (Medium Risk)

**MOVE to archive/completed_phase4b2/:**
- Batch 10 HTML files (7 files, 500K) - Completed Oct 23
- Execution scripts for 206/106 cases (10 files, ~100K)
- Working CSVs (small, but completed)
- **Rationale:** Phase 4B-2 complete, may need for historical reference

### Phase 3: Evaluate Specialized Scripts (High Risk - Read First)

**READ to understand purpose:**
- API enrichment scripts - still needed?
- Diagnostic scripts - still needed or superseded?
- HTML generation - needed for Phase 4C?

**Decision criteria:**
- Will Phase 4C reuse these?
- Are they superseded by canonical scripts?
- Do they provide unique functionality?

---

## Actions Required Before Cleanup

1. **Verify Phase 5T readiness:**
   - Test export_townhalls_to_landscape.py
   - Ensure no dependencies on files marked for deletion

2. **Read specialized scripts to understand:**
   - Which are still needed vs historical
   - What functionality is unique vs duplicate

3. **Create archive structure:**
   ```
   archive/
     completed_phase4b2/
       batch_outputs/
       execution_scripts/
       working_csvs/
   ```

4. **Document decisions:**
   - Update this inventory with decisions
   - Update CLEANUP_SUMMARY.md with results

---

## Questions for User

1. Should we keep Batch 10 HTML files in git or move to archive?
2. Are diagnostic scripts (diagnostic_report*.py) still needed?
3. Is generate_member_review_html.py needed for Phase 4C?
4. Should decision records (all_206_categorizations.json, batch_106_approved_cases.json) stay in root or move to archive?

---

**Status:** INVENTORY COMPLETE - Ready for Phase 2 (Full categorization with user decisions)
