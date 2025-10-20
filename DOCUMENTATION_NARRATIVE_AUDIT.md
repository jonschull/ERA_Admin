# Documentation Narrative & Hierarchy Audit
**Date:** October 20, 2025  
**Focus:** Guided paths, narrative flow, entry/exit points

---

## The Ideal: Guided Journey

```
Person arrives
   ↓
README.md (Front Door - "Who are you?")
   ↓
   ├─→ Human resuming work → CONTEXT_RECOVERY.md → specific component
   ├─→ AI assistant → AI_HANDOFF_GUIDE.md → component + WORKING_PRINCIPLES
   ├─→ Strategic understanding → ERA_ECOSYSTEM_PLAN.md → phase docs
   └─→ Component work → component/README.md → component docs
```

**Each doc should answer:**
1. Where did I come from? (breadcrumb)
2. Where am I? (purpose, scope)
3. Where should I go next? (explicit links)
4. What if I'm lost? (escape hatch back to main)

---

## Current State Analysis

### ✅ GOOD: Main README has clear signposting

**Lines 9-22:**
```
## 🚨 STARTING POINT - READ THIS FIRST
1. Start here: CONTEXT_RECOVERY.md
2. Strategic direction: ERA_ECOSYSTEM_PLAN.md
3. For AI assistants: AI_HANDOFF_GUIDE.md
4. Recent work: CONFIGURATION_CENTRALIZATION_PLAN.md
5. Then come back to this README
```

**Assessment:** ✅ Clear entry point with role-based routing

### ✅ GOOD: ERA_ECOSYSTEM_PLAN has navigation

**Top of file:**
```
## 📍 Quick Navigation
**New to this project?** → Start with README.md
**Lost context?** → See CONTEXT_RECOVERY.md
**Working on integration?** → You're in the right place
**Need component details?** → See component folders
```

**Assessment:** ✅ Breadcrumb + context + next steps

### ⚠️ MIXED: CONTEXT_RECOVERY.md

**Has:**
- Clear purpose statement
- Role identification (Humans + AI)
- Good internal structure

**Missing:**
- No breadcrumb (how did you get here from README?)
- No "See also" to WORKING_PRINCIPLES or ERA_ECOSYSTEM_PLAN
- No component links at end

**Assessment:** ⚠️ Good content, weak navigation

### ⚠️ MIXED: AI_HANDOFF_GUIDE.md

**Has:**
- Clear purpose
- Role definition
- Documentation hierarchy section (lines 110-136)

**Missing:**
- No reference to WORKING_PRINCIPLES.md
- No reference to integration_scripts/AI_WORKFLOW_GUIDE.md
- Doesn't explain relationship between the TWO AI guides

**Assessment:** ⚠️ Isolated - needs cross-references

### ❌ WEAK: WORKING_PRINCIPLES.md

**Has:**
- Git/PR workflow (lines 144-183)
- Philosophy and principles
- Good content

**Missing:**
- No navigation at all
- Not linked from AI_HANDOFF_GUIDE
- Not clear when to read this vs other guides
- No "See also"

**Assessment:** ❌ Orphan document - excellent content, no path

---

## Orphan Documents (Not in guided path)

### Documents with NO links TO them from main path:

1. **WORKING_PRINCIPLES.md**
   - Contains critical Git/PR workflow
   - Should be linked from AI_HANDOFF_GUIDE
   - Should be linked from README

2. **MONOREPO_CONSOLIDATION.md** 
   - Created today
   - Historical record
   - Should be linked from somewhere or archived

3. **CONFIGURATION_CENTRALIZATION_PLAN.md**
   - Marked COMPLETE
   - Still in active tree
   - Referenced in README but should be archived

4. **integration_scripts/AI_WORKFLOW_GUIDE.md**
   - Specialized guide for Phase 4B-2
   - Not linked from main AI_HANDOFF_GUIDE
   - Users won't find it

5. **integration_scripts/PHASE4B2_PROGRESS_REPORT.md**
   - Great analysis
   - Linked from integration_scripts/README but not main README
   - Lost if you don't know to look

### Component READMEs - Unclear relationship to main:

- **FathomInventory/README.md** - Does it reference main README?
- **airtable/README.md** - Does it explain how to get back?
- **integration_scripts/README.md** - Multiple README levels

**Assessment:** ❌ Many orphans - excellent content, no discoverability

---

## Navigation Anti-Patterns Found

### 1. **Parallel Hierarchies** (Integration Scripts)

```
/integration_scripts/
├── README.md              ← Overview
├── README_PHASE4B.md      ← Phase 4B system
├── README_PHASE4B_DETAILED.md  ← Detailed?
└── AI_WORKFLOW_GUIDE.md   ← Another guide?
```

**Problem:** 4 documentation files, unclear which to read when  
**Solution:** Need clear "Read X for overview, Y for details, Z for workflow"

### 2. **Dual AI Guides** (No bridge)

- `/AI_HANDOFF_GUIDE.md` - General AI guide
- `/integration_scripts/AI_WORKFLOW_GUIDE.md` - Specific workflow

**Problem:** Don't reference each other  
**Solution:** Main guide should say "For Phase 4B-2 work, see integration_scripts/AI_WORKFLOW_GUIDE.md"

### 3. **Completed Plans in Active Tree**

- CONFIGURATION_CENTRALIZATION_PLAN.md (marked COMPLETE)
- But still in root, not archived

**Problem:** Clutters active navigation  
**Solution:** Move to historical/ with date

### 4. **Multiple CONTEXT_RECOVERY Files**

- `/CONTEXT_RECOVERY.md` - Main
- `/FathomInventory/CONTEXT_RECOVERY.md` - Component
- `/FathomInventory/analysis/CONTEXT_RECOVERY.md` - Sub-component

**Problem:** Updated main today, others may be stale  
**Solution:** Component ones should start with "See main CONTEXT_RECOVERY.md, this adds component-specific context"

---

## Proposed Navigation Structure

### Root Level (Front Door):

```
README.md
  ├─ Purpose & Overview
  ├─ 🚨 START HERE section
  │   ├→ CONTEXT_RECOVERY.md (where we are now)
  │   ├→ AI_HANDOFF_GUIDE.md (for AI assistants)
  │   ├→ ERA_ECOSYSTEM_PLAN.md (strategic vision)
  │   └→ WORKING_PRINCIPLES.md (how we work) ← ADD THIS
  │
  ├─ Components
  │   ├→ airtable/README.md
  │   ├→ FathomInventory/README.md
  │   └→ integration_scripts/README.md
  │
  └─ Reference
      ├→ MONOREPO_CONSOLIDATION.md (today's work)
      └→ historical/ (completed plans)
```

### Each Document Template:

```markdown
# Title

**Purpose:** [One sentence]
**Audience:** [Who should read this]
**Breadcrumb:** [Where you came from]

---

## 📍 Navigation

**From:** [Previous doc in path]
**See also:** [Related docs]
**Next:** [Where to go from here]

---

[Content]

---

## Related Documentation

- **[Link]** - [Why you'd read it]
- **[Link]** - [Why you'd read it]

**Back to:** [Main README](README.md)
```

---

## Action Plan

### Phase 1: Connect the Orphans (Tonight)

1. ✅ **Add WORKING_PRINCIPLES.md to navigation**
   - Link from README "START HERE" section
   - Link from AI_HANDOFF_GUIDE
   - Add Git workflow reference

2. ✅ **Bridge the two AI guides**
   - AI_HANDOFF_GUIDE: Add section "For Phase 4B-2, see integration_scripts/AI_WORKFLOW_GUIDE.md"
   - integration_scripts/AI_WORKFLOW_GUIDE: Add header "Part of AI_HANDOFF_GUIDE system"

3. ✅ **Add navigation headers to key docs**
   - CONTEXT_RECOVERY.md: Add breadcrumb + "See also"
   - WORKING_PRINCIPLES.md: Add navigation section
   - AI_HANDOFF_GUIDE.md: Add "See also" section

4. ✅ **Archive completed plan**
   - Move CONFIGURATION_CENTRALIZATION_PLAN.md to historical/oct2025/
   - Add note in README about where historical docs live

### Phase 2: Component Integration (Next session)

5. **Add bidirectional links**
   - Component READMEs link back to main
   - Main README references where to find progress reports

6. **Clarify integration_scripts hierarchy**
   - README vs README_PHASE4B vs README_PHASE4B_DETAILED
   - Add "Which doc to read when" section

7. **Sync multiple CONTEXT_RECOVERY files**
   - Component ones reference main
   - Add "last updated" dates
   - Check for contradictions

---

## Questions

1. **Archive threshold?** Should MONOREPO_CONSOLIDATION.md stay active (it's current state) or go to historical/ (it's done)?

2. **Component autonomy?** Should FathomInventory docs reference ERA_Admin main docs, or stay self-contained?

3. **README proliferation?** integration_scripts/ has 3 READMEs - consolidate or differentiate?

4. **Git workflow location?** Extract from WORKING_PRINCIPLES into separate GIT_WORKFLOW.md, or keep integrated?

---

**Recommendation:** Start with Phase 1 tonight - connect the orphans, add navigation headers. This makes the EXISTING excellent content discoverable without creating new docs.
