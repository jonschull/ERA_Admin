# Archive Plan - Member Enrichment Consolidation

**Date:** October 28, 2025  
**Status:** Ready to execute

---

## What Will Happen

Execute: `./archive_files_20251028.sh`

This will **MOVE** (not delete) ~80+ files from `member_enrichment/` to `/historical/member_enrichment_archive_20251028/`

---

## Files That Will Remain ACTIVE

### Working Documents (3 files)
- `ERA_MEMBERS_LACKING_BIOS_V8.md` ← Current work, comprehensive
- `V8_REWRITE_SUMMARY.md` ← Paradigm shift documentation
- `V7_TO_V8_PROCESSING_SUMMARY.md` ← Recent processing notes

### Active Scripts (4 files)
- `linkedin_profile_fetcher.py` ← **ACTIVE technique**, documented in V8
- `aggregate_member_info.py` ← Utility
- `identify_members_needing_bios.py` ← Utility
- `update_airtable_bios.py` ← Legacy Airtable sync

### Active Data (3 files)
- `linkedin_about_sections.json` ← Recent scraping results
- `LinkedInConnections.csv` ← Reference data
- `google_contacts.csv` ← Reference data

### Active Configuration
- `linkedin_cookies.json` ← Authentication (keep secure)
- `linkedin_urls_to_scrape.txt` ← Queue

### Documentation
- `cookie_export_guide_linkedin.md` ← How-to guide
- `README.md` ← Component README (to be updated)

### Support Files
- `linkedin_status.json` ← Scraping status
- `linkedin_urls_additional.txt` ← Reference

**Total remaining: ~15 active files** (down from 80+)

---

## Files That Will Be Archived

### Working Notes → `/working_notes/` (9 files)
- BIO_GENERATION_PLAN.md
- FEEDBACK_LOOP.md
- BATCH_4-7_COMPLETION_REPORT.md
- BIO_SYNC_SESSION_SUMMARY.md
- ERA_AFRICA_ENRICHMENT_SUMMARY.md
- V6_BIO_IMPROVEMENTS.md
- V7_RESEARCH_SUMMARY.md
- CONTEXT_RECOVERY.md
- PROCESS.md

### Version History → `/versions/` (11 files)
- ERA_MEMBERS_LACKING_BIOS.md (V1)
- ERA_MEMBERS_LACKING_BIOS_V2.md through V7.md
- ERA_MEMBERS_V6_ENRICHED.md
- ENRICHMENTS_FOR_REVIEW.md
- NEW_ENRICHMENTS_FROM_FUZZY_MATCH.md

### Batch Processing → `/batch_processing/` (1 directory)
- `batches/` entire directory (~155 items)

### Diagnostics → `/diagnostics/` (7 files)
- DIAGNOSTIC_SUMMARY.md
- FINAL_DIAGNOSTIC_SUMMARY.md
- PRIORITY_0_DIAGNOSTIC.md
- PRIORITY_0_MATCHES_DIAGNOSTIC.md
- DUPLICATES_DIAGNOSTIC.md
- FUZZY_MATCH_FINDINGS.md
- AIRTABLE_DUPLICATES.md

### LinkedIn Batch Outputs → `/linkedin_batch_outputs/` (8+ files)
- LINKEDIN_PROFILES_*.md
- LINKEDIN_PROFILES_*.html
- NEXT_3_LINKEDIN_PROFILES.md
- Various historical JSON files

### Obsolete Scripts → `/obsolete_scripts/` (20+ files)
- scrape_batch_*.py and *.log
- Various one-off scripts
- Version-specific utilities

### Trash → `/trash/` (duplicates)
- ERA_MEMBERS_LACKING_BIOS_V6 copy.md
- Empty JSON files

---

## Safety Measures

✅ **No deletions** - All files moved to `/historical/`  
✅ **Script uses `mv -v`** - Shows each file moved  
✅ **Error handling** - Continues if file not found  
✅ **Confirmation prompt** - Press ENTER to proceed  
✅ **Preserves structure** - Organized by category  

---

## Rollback

If needed, reverse the moves:

```bash
# Move everything back
cp -r /Users/admin/ERA_Admin/historical/member_enrichment_archive_20251028/* \
     /Users/admin/ERA_Admin/integration_scripts/member_enrichment/
```

---

## After Archiving

### Immediate Actions

1. **Verify active files remain:**
   ```bash
   cd /Users/admin/ERA_Admin/integration_scripts/member_enrichment
   ls -la
   ```

2. **Check archive created properly:**
   ```bash
   ls -la /Users/admin/ERA_Admin/historical/member_enrichment_archive_20251028/
   ```

3. **Update component README** (add 4-section structure)

### Next Steps (Wireframe Consolidation)

4. **Add to NAVIGATION_WIREFRAME.md:**
   - Create `## FILE: integration_scripts/member_enrichment/README.md`
   - Include V8 content with 4-section structure
   - Document LinkedIn scraping technique
   - Reference historical archive

5. **Regenerate docs:**
   ```bash
   ./docs/update_docs.sh
   ```

6. **Validate navigation:**
   ```bash
   python3 docs/test_navigation.py
   ```

7. **Create PR:**
   ```bash
   git checkout -b docs/member-enrichment-consolidation
   git add -A
   git commit -m "docs: Consolidate member enrichment, archive V1-V7"
   git push origin docs/member-enrichment-consolidation
   gh pr create --web
   ```

---

## What This Accomplishes

**Before:**
- 245+ files in member_enrichment/
- Mix of active, historical, obsolete
- Difficult to find current documentation
- Unclear what's authoritative

**After:**
- ~15 active files in member_enrichment/
- Clear separation: active vs historical
- V8 as single source of current understanding
- Archive preserves history for reference
- Ready for wireframe consolidation
- Clean PR to document system

---

## Execute When Ready

```bash
cd /Users/admin/ERA_Admin/integration_scripts/member_enrichment
./archive_files_20251028.sh
```

Script will:
1. Show what it's about to do
2. Wait for your ENTER
3. Move files with verbose output
4. Show summary of results

**Estimated time:** 1-2 minutes

---

**Created:** October 28, 2025  
**Ready:** Yes - all preparation complete
