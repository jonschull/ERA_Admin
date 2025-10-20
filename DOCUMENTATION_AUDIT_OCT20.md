# Documentation Audit & Curation Plan
**Date:** October 20, 2025  
**Purpose:** Audit all markdown files for accuracy, consistency, redundancy, and alignment with working principles

---

## Summary

**Total markdown files:** 53  
**Issues found:**
- ❌ Redundancy: Multiple overlapping guides
- ❌ Outdated info: References to old Dropbox paths
- ❌ Missing: Git/GitHub hygiene guide
- ⚠️ Scattered: Related docs in different locations
- ⚠️ Inconsistency: Multiple CONTEXT_RECOVERY files

---

## Issues by Category

### 1. REDUNDANCY - Documentation Overlap

**AI Guidance (3 docs covering similar ground):**
- `/AI_HANDOFF_GUIDE.md` (607 lines) - AI workflow, conventions
- `/integration_scripts/AI_WORKFLOW_GUIDE.md` (457 lines) - Phase 4B-2 specific
- `/WORKING_PRINCIPLES.md` (389 lines) - Includes PR workflow

**Recommendation:** Keep AI_HANDOFF_GUIDE as main, reference others for specifics

**FathomInventory Authentication (2 docs):**
- `/FathomInventory/authentication/README.md` - Overview
- `/FathomInventory/docs/AUTHENTICATION_GUIDE.md` - Detailed guide

**Recommendation:** Consolidate or clearly differentiate (quick ref vs detailed)

**System Overview (Multiple):**
- `/README.md` - Main ERA_Admin overview
- `/FathomInventory/README.md` - FathomInventory overview  
- `/FathomInventory/docs/SYSTEM_OVERVIEW.md` - Another overview?
- `/integration_scripts/README.md` - Integration overview

**Recommendation:** These are appropriate if non-overlapping, but need audit

### 2. CONTEXT_RECOVERY Proliferation (3 files!)

- `/CONTEXT_RECOVERY.md` - Main ERA_Admin
- `/FathomInventory/CONTEXT_RECOVERY.md` - FathomInventory specific
- `/FathomInventory/analysis/CONTEXT_RECOVERY.md` - Analysis specific

**Issue:** Updated main one today, but others may be stale

**Recommendation:** 
- Keep main as authoritative
- Component-specific ones should reference main + add component details
- Audit all 3 for consistency

### 3. COMPLETED PLANS (Should be archived?)

- `/CONFIGURATION_CENTRALIZATION_PLAN.md` - COMPLETE (Oct 18)
- `/FathomInventory/analysis/PHASE2_COMPLETE.md`
- `/FathomInventory/analysis/PHASE2_PLAN.md`
- `/FathomInventory/analysis/PHASE3_COMPLETE.md`

**Recommendation:** Move to `historical/` with date stamps

### 4. MISSING CRITICAL DOCUMENTATION

**Git/GitHub Hygiene Guide** - MISSING!

Should cover:
- Branch/PR workflow (from WORKING_PRINCIPLES.md)
- Commit message guidelines
- .gitignore patterns
- Secret management
- How to handle retrospective PRs (learned today!)

**Recommendation:** Create `GIT_WORKFLOW.md` at root

### 5. OUTDATED REFERENCES (Need verification)

Files that may reference old Dropbox paths or outdated information:
- FathomInventory/docs/* (various)
- All files created before Oct 18 migration

**Recommendation:** Systematic grep audit

### 6. FathomInventory Documentation Sprawl (37 files!)

**Structure:**
```
FathomInventory/
├── Main docs (4)
├── analysis/ (9 docs)
├── authentication/ (4 docs)
├── docs/ (8 docs)
└── email_conversion/ (12 docs)
```

**Questions:**
- Why both `/authentication/` AND `/docs/AUTHENTICATION_GUIDE.md`?
- Why both main README and `/docs/SYSTEM_OVERVIEW.md`?
- Are email_conversion numbered files needed in active tree?

**Recommendation:** FathomInventory-specific audit needed

### 7. REPORT FILES vs DOCUMENTATION

**Data reports (not documentation):**
- `/FathomInventory/zoom_fathom_crosscheck_report.md`
- `/FathomInventory/analysis/townhall_validation_report.md`
- `/FathomInventory/analysis/ERA_Town_Hall_Participants.md`

**Recommendation:** Consider moving to `reports/` subdirectory or archive

---

## Proposed Curation Plan

### Phase 1: Quick Wins (Tonight)

1. **Create GIT_WORKFLOW.md**
   - Extract from WORKING_PRINCIPLES.md
   - Add lessons from today (retrospective PR, secret handling)
   - Make concise, actionable

2. **Archive completed plans**
   - Move CONFIGURATION_CENTRALIZATION_PLAN.md to historical/
   - Note: Already documented as complete

3. **Audit CONTEXT_RECOVERY files**
   - Check all 3 for consistency
   - Update stale references
   - Add cross-references

### Phase 2: Systematic Audit (Next session)

4. **Check all docs for Dropbox path references**
   - Grep for old paths
   - Update to current locations
   - Verify all paths accurate

5. **Consolidate redundant authentication docs**
   - Merge or clearly differentiate
   - Remove duplication

6. **FathomInventory doc reorganization**
   - Rationalize /docs vs root
   - Move data reports to reports/
   - Archive or delete numbered conversion files

### Phase 3: Structural Improvements (Future)

7. **Create documentation index**
   - `/docs/INDEX.md` - Complete doc map
   - By topic, by component, by audience

8. **Standardize doc headers**
   - Date, Status, Audience, Purpose
   - "Last Updated" on all

9. **Navigation improvements**
   - Clear "See also" sections
   - Breadcrumb guidance
   - Component isolation maintained

---

## Immediate Action Items

**Tonight (if you approve):**

1. ✅ Create `/GIT_WORKFLOW.md`
2. ✅ Audit 3 CONTEXT_RECOVERY files
3. ✅ Check key docs for Dropbox paths
4. ✅ Update README.md doc section to reflect new structure

**Save for next session:**
- Deep FathomInventory audit (37 files is too many to rush)
- Consolidation of authentication docs
- Archive completed plans

---

## Questions for You

1. **Git guide priority?** Should I create GIT_WORKFLOW.md tonight?

2. **Completed plans?** Archive CONFIGURATION_CENTRALIZATION_PLAN to historical/?

3. **FathomInventory sprawl?** That component has 37 docs - do full audit tonight or separate session?

4. **Email conversion files?** The numbered .md files (1_new.md, 2_new.md, etc.) - are these needed in active tree?

5. **Threshold for "too many docs"?** What's your comfort level?

---

**Ready to proceed with Phase 1 quick wins if you approve the approach.**
