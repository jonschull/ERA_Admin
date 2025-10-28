#!/bin/bash

# Member Enrichment Archive Script
# Date: October 28, 2025
# Purpose: Move completed/obsolete files to historical archive
# DO NOT DELETE - only move to /historical/

set -e  # Exit on error

ARCHIVE_BASE="/Users/admin/ERA_Admin/historical/member_enrichment_archive_20251028"
SOURCE_DIR="/Users/admin/ERA_Admin/integration_scripts/member_enrichment"

echo "=========================================="
echo "Member Enrichment Archive - October 28, 2025"
echo "=========================================="
echo ""
echo "Source: $SOURCE_DIR"
echo "Archive: $ARCHIVE_BASE"
echo ""
echo "Press ENTER to proceed, Ctrl+C to cancel..."
read

cd "$SOURCE_DIR"

# ============================================================================
# CATEGORY D: Working Notes (Intermediate Understanding)
# ============================================================================
echo ""
echo "Moving working notes to archive..."

mv -v BIO_GENERATION_PLAN.md "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"
mv -v FEEDBACK_LOOP.md "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"
mv -v BATCH_4-7_COMPLETION_REPORT.md "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"
mv -v BIO_SYNC_SESSION_SUMMARY.md "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"
mv -v ERA_AFRICA_ENRICHMENT_SUMMARY.md "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"
mv -v V6_BIO_IMPROVEMENTS.md "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"
mv -v V7_RESEARCH_SUMMARY.md "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"
mv -v CONTEXT_RECOVERY.md "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"
mv -v PROCESS.md "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"

# ============================================================================
# CATEGORY E: Version History
# ============================================================================
echo ""
echo "Moving version history to archive..."

mv -v ERA_MEMBERS_LACKING_BIOS.md "$ARCHIVE_BASE/versions/" 2>/dev/null || echo "  (already moved or not found)"
mv -v ERA_MEMBERS_LACKING_BIOS_V2.md "$ARCHIVE_BASE/versions/" 2>/dev/null || echo "  (already moved or not found)"
mv -v ERA_MEMBERS_LACKING_BIOS_V3.md "$ARCHIVE_BASE/versions/" 2>/dev/null || echo "  (already moved or not found)"
mv -v ERA_MEMBERS_LACKING_BIOS_V4.md "$ARCHIVE_BASE/versions/" 2>/dev/null || echo "  (already moved or not found)"
mv -v ERA_MEMBERS_LACKING_BIOS_V5.md "$ARCHIVE_BASE/versions/" 2>/dev/null || echo "  (already moved or not found)"
mv -v ERA_MEMBERS_LACKING_BIOS_V6.md "$ARCHIVE_BASE/versions/" 2>/dev/null || echo "  (already moved or not found)"
mv -v ERA_MEMBERS_LACKING_BIOS_V7.md "$ARCHIVE_BASE/versions/" 2>/dev/null || echo "  (already moved or not found)"
mv -v "ERA_MEMBERS_LACKING_BIOS_V6 copy.md" "$ARCHIVE_BASE/trash/" 2>/dev/null || echo "  (already moved or not found)"
mv -v ERA_MEMBERS_V6_ENRICHED.md "$ARCHIVE_BASE/versions/" 2>/dev/null || echo "  (already moved or not found)"
mv -v ENRICHMENTS_FOR_REVIEW.md "$ARCHIVE_BASE/versions/" 2>/dev/null || echo "  (already moved or not found)"
mv -v NEW_ENRICHMENTS_FROM_FUZZY_MATCH.md "$ARCHIVE_BASE/versions/" 2>/dev/null || echo "  (already moved or not found)"

# ============================================================================
# CATEGORY F: Diagnostics
# ============================================================================
echo ""
echo "Moving diagnostic files to archive..."

mv -v DIAGNOSTIC_SUMMARY.md "$ARCHIVE_BASE/diagnostics/" 2>/dev/null || echo "  (already moved or not found)"
mv -v FINAL_DIAGNOSTIC_SUMMARY.md "$ARCHIVE_BASE/diagnostics/" 2>/dev/null || echo "  (already moved or not found)"
mv -v PRIORITY_0_DIAGNOSTIC.md "$ARCHIVE_BASE/diagnostics/" 2>/dev/null || echo "  (already moved or not found)"
mv -v PRIORITY_0_MATCHES_DIAGNOSTIC.md "$ARCHIVE_BASE/diagnostics/" 2>/dev/null || echo "  (already moved or not found)"
mv -v DUPLICATES_DIAGNOSTIC.md "$ARCHIVE_BASE/diagnostics/" 2>/dev/null || echo "  (already moved or not found)"
mv -v FUZZY_MATCH_FINDINGS.md "$ARCHIVE_BASE/diagnostics/" 2>/dev/null || echo "  (already moved or not found)"
mv -v AIRTABLE_DUPLICATES.md "$ARCHIVE_BASE/diagnostics/" 2>/dev/null || echo "  (already moved or not found)"

# ============================================================================
# CATEGORY G: Completed Phase Data - Batch Processing
# ============================================================================
echo ""
echo "Moving batch processing directory to archive..."

mv -v batches/ "$ARCHIVE_BASE/batch_processing/" 2>/dev/null || echo "  (already moved or not found)"

# ============================================================================
# CATEGORY G: LinkedIn Batch Outputs (old HTML/MD files)
# ============================================================================
echo ""
echo "Moving old LinkedIn batch outputs to archive..."

mv -v LINKEDIN_PROFILES_V2.md "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v LINKEDIN_PROFILES_CURATED.md "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v LINKEDIN_PROFILES_REVIEW.html "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v LINKEDIN_PROFILES_FULL_CONTENT.html "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v LINKEDIN_PROFILES_ADDITIONAL_12_V2.md "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v LINKEDIN_PROFILES_ADDITIONAL_12_V2_EDITED.md "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v LINKEDIN_ABOUT_SECTIONS.md "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v NEXT_3_LINKEDIN_PROFILES.md "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"

# ============================================================================
# CATEGORY H: Obsolete Scripts
# ============================================================================
echo ""
echo "Moving obsolete scripts to archive..."

mv -v scrape_batch_24.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v scrape_batch_24.log "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v scrape_batch_28.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v scrape_batch_28.log "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v scrape_next_3.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v scrape_remaining_12_slow.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v rescrape_16_fixed.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v create_v7_from_v6.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v bio_writer_pilot.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v generate_bio_batch.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v analyze_bio_feedback.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v process_batch_feedback.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v process_v6_to_database.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v diagnose_duplicates.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v diagnose_priority0_mismatches.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v execute_era_member_fixes.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v fix_era_member_flags.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v merge_mahangi_munanse.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v create_jon_should_publish_field.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v set_jon_should_publish.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v set_publish_flags.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v revert_publish_flags.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"
mv -v test_airtable_write.py "$ARCHIVE_BASE/obsolete_scripts/" 2>/dev/null || echo "  (already moved or not found)"

# ============================================================================
# Obsolete Data Files
# ============================================================================
echo ""
echo "Moving obsolete data files to archive..."

mv -v profiles_to_process.json "$ARCHIVE_BASE/trash/" 2>/dev/null || echo "  (already moved or not found)"
mv -v members_to_enrich.json "$ARCHIVE_BASE/trash/" 2>/dev/null || echo "  (already moved or not found)"
mv -v recent_profiles_v6.json "$ARCHIVE_BASE/trash/" 2>/dev/null || echo "  (already moved or not found)"
mv -v matched_profiles.json "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v profiles_for_v2.json "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v profiles_new_12.json "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v new_bios_v6.json "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v new_linkedin_bios.json "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v linkedin_profiles_curated.json "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v linkedin_profiles_extracted.json "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"
mv -v v6_processing_results.txt "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"
mv -v transcript_speakers_complete.txt "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"
mv -v urls_to_scrape_v5.txt "$ARCHIVE_BASE/linkedin_batch_outputs/" 2>/dev/null || echo "  (already moved or not found)"

# ============================================================================
# Other Reference Docs
# ============================================================================
echo ""
echo "Moving other reference docs to archive..."

mv -v JON_SHOULD_UNPUBLISH.md "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"
mv -v READY_FOR_PUBLISH_FLAG.md "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"
mv -v PLAN_Finish_Missing_Bios_and_Review_ERA_Africa.md "$ARCHIVE_BASE/working_notes/" 2>/dev/null || echo "  (already moved or not found)"

# ============================================================================
# Summary
# ============================================================================
echo ""
echo "=========================================="
echo "Archive Complete!"
echo "=========================================="
echo ""
echo "Files moved to: $ARCHIVE_BASE"
echo ""
echo "Archive structure:"
ls -la "$ARCHIVE_BASE"
echo ""
echo "Remaining active files in $SOURCE_DIR:"
ls -1 "$SOURCE_DIR"/*.md 2>/dev/null || echo "(No markdown files)"
ls -1 "$SOURCE_DIR"/*.py 2>/dev/null | grep -v archive_files || echo "(Only active scripts)"
echo ""
echo "Next steps:"
echo "1. Review remaining files in member_enrichment/"
echo "2. Update component README"
echo "3. Add to NAVIGATION_WIREFRAME.md"
echo "4. Regenerate docs"
echo ""
