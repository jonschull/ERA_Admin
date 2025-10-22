# ERA_Landscape Documentation Consolidation - TODO

**Status:** Phase 1 complete (historical files moved)

**Next:** Add internal docs to NAVIGATION_WIREFRAME.md

---

## Files to Add to Wireframe

Per documentation policy (docs/README.md), these internal docs need full content in NAVIGATION_WIREFRAME.md:

### Core Documentation
1. [ ] `README.md` (328 lines) - Quick start, deployment, features
2. [ ] `NETWORK_ARCHITECTURE.md` (388 lines) - Technical deep-dive
3. [ ] `KNOWN_ISSUES.md` (145 lines) - Current bugs, workarounds

### Development Documentation  
4. [ ] `DEVELOPMENT.md` - Development workflow
5. [ ] `TESTING.md` - Test strategy
6. [ ] `DEPLOYMENT_GUIDE.md` - Deployment procedures

### Context Recovery
7. [ ] `AI_HANDOFF_GUIDE.md` - AI context
8. [ ] `START_HERE_NEW_AI.md` - Quick orientation

### Design & Planning
9. [ ] `VISION.md` - Design decisions
10. [ ] `NEXT_STEPS.md` - Current status
11. [ ] `SHEET_ANALYSIS_V2.md` - Google Sheets design

**Total estimated:** ~2,500 lines to add to wireframe

---

## Moved to /historical

✅ `SESSION_SUMMARY_2025-10-15.md` - Session notes  
✅ `ERA_ADMIN_INTEGRATION.md` - Integration notes (now obsolete)

---

## Insert Location in Wireframe

After line 3760 (end of `integration_scripts/AI_WORKFLOW_GUIDE.md` section)

Add new section header:
```markdown
---

## FILE: ERA_Landscape/README.md

**Path:** `ERA_Landscape/README.md`

[full content here...]
```

Repeat for all 11 files.

---

## Implementation Options

**Option A: Manual (recommended for review)**
1. Open `docs/NAVIGATION_WIREFRAME.md`
2. Scroll to line 3760
3. Add each `## FILE:` section with full content
4. Run `./docs/update_docs.sh`
5. Review regenerated docs
6. Commit

**Option B: Script** (faster but less reviewable)
```bash
# Create script to append all files
for file in README.md NETWORK_ARCHITECTURE.md KNOWN_ISSUES.md ...; do
  echo "---" >> temp_wireframe_addition.md
  echo "" >> temp_wireframe_addition.md
  echo "## FILE: ERA_Landscape/$file" >> temp_wireframe_addition.md
  echo "" >> temp_wireframe_addition.md
  echo "**Path:** \`ERA_Landscape/$file\`" >> temp_wireframe_addition.md
  echo "" >> temp_wireframe_addition.md
  cat "ERA_Landscape/$file" >> temp_wireframe_addition.md
  echo "" >> temp_wireframe_addition.md
done

# Insert into wireframe at line 3760
```

**Option C: Incremental**
1. Add README.md first
2. Test regeneration
3. Add 2-3 more files
4. Test again
5. Repeat until complete

---

## After Consolidation

1. Run `./docs/update_docs.sh` to regenerate
2. Verify navigation links work
3. Check no files are orphaned
4. Update ERA_Landscape/README.md to reference wireframe
5. Commit and create PR
