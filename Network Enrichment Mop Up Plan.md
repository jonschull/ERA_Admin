# Network Enrichment Mop Up Plan (NEMUP)

**Created:** 2025-10-21  
**Status:** Draft - Revised after docs consultation  
**Component:** ERA_Landscape visualization  
**Type:** Technical debt cleanup + feature completion

---

## 1. Overview

**Purpose:** Complete Town Hall visualization features and fix non-functional Network settings

**What was accomplished today:**
- Town Hall meetings exported from Fathom DB (65 events)
- Circular TH positioning at periphery with grey edges
- Network settings panel created (3 sliders)
- Reduced TH connection weighting (0.1x vs 1.0x)

**What needs fixing:**
- TH edges to nearby orphans not thick/visible
- Scaling Intensity slider non-functional
- Edge Fading slider non-functional  
- Edge Thickness Tuning slider non-functional
- localStorage persistence uncertain
- Initial zoom too tight

**Related docs:**
- [ERA_Landscape/START_HERE_NEW_AI.md](ERA_Landscape/START_HERE_NEW_AI.md) - Component onboarding
- [ERA_Landscape/KNOWN_ISSUES.md](ERA_Landscape/KNOWN_ISSUES.md) - Issue tracking
- [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md) - Development discipline

---

## 2. Orientation - Where to Find What

**You are at:** Town Hall visualization cleanup plan

**Critical files:**
- `ERA_Landscape/index.html` - Main visualization (1000+ lines, TH logic at ~640-740)
- `integration_scripts/export_townhalls_to_landscape.py` - Data export
- `FathomInventory/fathom_emails.db` - Source database (65 TH meetings)

**Key concepts:**
- **Town Halls:** Grey hexagons in circle at radius 1000px
- **Network Settings:** Scaling intensity, edge fading, edge thickness
- **Distance-based edges:** Opacity/width vary by distance (implemented but broken)

**What you might need:**
- Testing workflow → [ERA_Landscape/TESTING.md](ERA_Landscape/TESTING.md)
- Component guide → [ERA_Landscape/START_HERE_NEW_AI.md](ERA_Landscape/START_HERE_NEW_AI.md)
- Development discipline → [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md)

---

## 3. Principles

**System-wide:** See [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md) and [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md)

**Applied to this plan:**

1. **Test Before Claiming Success** (AI_HANDOFF_GUIDE §3.2)
   - Browser test FIRST, Playwright SECOND, user verification THIRD
   - Never say "should work" - say "tested, works"
   - Show evidence (console logs, screenshots)

2. **No Guessing** (AI_HANDOFF_GUIDE §3.1)
   - Use extensive console logging
   - Browser inspector for edge properties
   - Verify assumptions with actual data

3. **Incremental Progress** (AI_HANDOFF_GUIDE §4.2)
   - One fix → test → verify → next fix
   - Update KNOWN_ISSUES.md after each resolution
   - Commit working state before moving on

4. **Branch-Based Workflow** (START_HERE_NEW_AI §2.6)
   - Create feature branch before changes
   - Never push directly to main
   - PR with screenshots and testing notes

---

## 4. Specialized Topics

### Context Briefing

### What We've Accomplished Today

We successfully integrated **Town Hall meeting data** from the Fathom database into the ERA Landscape network visualization. This involved:

#### 1. **Data Export** (`integration_scripts/export_townhalls_to_landscape.py`)
- Joined `participants` and `calls` tables to get meeting dates
- Exported 65 Town Hall meetings with date-based IDs (e.g., `event::Town Hall 2024.09.18`)
- Created umbrella node `project::Town Hall Meetings`
- Built linear chain with `follows` edges (chronological timeline)
- Connected 160 people to their attended meetings via `attended` edges
- Weighted TH connections as 0.1 instead of 1.0 to reduce node size inflation

#### 2. **Visual Representation** (`ERA_Landscape/index.html`)
- **Town Halls as Events:** Grey hexagons positioned in fixed circle at radius 1000px
- **TH Chain:** Directed arrows showing temporal sequence (follows edges)
- **Reduced Scaling:** TH attendance counts 10% of normal connections
- **Distance-based Edges:** 
  - Near edges (< 300px): Thick (2.5), high opacity (80%) - for orphans
  - Medium edges (300-600px): Moderate thickness/opacity
  - Far edges (> 600px): Thin (0.5), nearly invisible (5%)
- **Grey Color:** All TH edges use #999999
- **Hidden Labels:** "attended" and "follows" labels removed for cleaner view

#### 3. **Network Settings Panel**
- Added "🌐 Network" button to toolbar
- Created draggable modal with three sliders:
  - **Scaling Intensity:** Control log/linear node size scaling
  - **Edge Fading:** Control TH edge opacity by distance
  - **Edge Thickness Tuning:** Control TH edge width by distance
- Settings persist to localStorage

### The Problem: Implementation Incomplete

Despite code being written, features don't work:

1. ❌ TH edges not thicker near orphans (should be 2.5 width, 80% opacity)
2. ❌ Scaling Intensity slider no effect
3. ❌ Edge Fading slider no effect
4. ❌ Edge Thickness Tuning slider no effect
5. ❓ localStorage persistence unverified
6. 📐 Initial zoom too tight

---

## Execution Plan

### Phase 1: Save Current Work
**Goal:** Protect progress before debugging

**Tasks:**
1. `git status` in ERA_Admin
2. Commit with message:
   ```
   feat: Town Hall integration with Network settings panel (partial)
   
   - Export 65 TH meetings from Fathom DB (date-based IDs)
   - Circular TH positioning at radius 1000px, grey edges
   - Network settings: Scaling/Fading/Thickness sliders (UI only)
   - Reduced TH connection weight (0.1x vs 1.0x)
   - Distance-based edge logic added (not functional yet)
   ```
3. Consider feature branch: `feat/townhall-network-viz`

**Success Criteria:**
- ✅ All changes committed
- ✅ No uncommitted work at risk

---

### Phase 2: Debug & Fix Issues
**Goal:** Make features functional via browser testing

**Testing Order (per START_HERE_NEW_AI.md):**
1. Browser test FIRST (console, visual check)
2. Run after each fix, not after all fixes
3. Show evidence before claiming success

#### 2.1 Fix TH Edge Thickness (HIGH)
**Problem:** Nearby edges not 2.5 width, 80% opacity

**Debug:**
```javascript
// Add in setTimeout edge adjustment section
console.log(`Edge ${edge.id}: dist=${distance}, width=${width}, opacity=${opacity}, rel=${edge.relationship}`);
```
- Check: `edge.relationship !== 'follows'` filter working?
- Verify: `edges.update()` actually applying?
- Browser inspector: Check edge properties after 4 seconds

**Test:** Orphan node near TH → thick grey edge visible

#### 2.2 Fix Scaling Intensity (HIGH)
**Problem:** Slider doesn't change Jon Schull's size

**Target Range:** 0 (no scaling) → 1 (logarithmic)
- 0: All nodes base size (value = 10)
- 1: log(connections) scaling

**Debug:**
```javascript
// Add in applyNetworkSettings()
console.log(`Jon: connections=${conns}, log=${log}, value=${value}`);
```
- Verify: `nodes.update()` called?
- Check: Node.value property changes?

**Test:** Move slider → Jon's size changes visibly

#### 2.3 Implement Edge Fading (MEDIUM)
**Current:** Slider exists, not connected

**Connect to distance logic:**
```javascript
// In setTimeout edge adjustment
const fadeFactor = networkConfig.edgeFading;
opacity = baseOpacity * (1 - fadeFactor * 0.5);
```

**Test:** Slider 0 = edges visible, 1 = faded

#### 2.4 Implement Edge Thickness (MEDIUM)
**Current:** Slider exists, not connected

**Connect to distance logic:**
```javascript
// In setTimeout edge adjustment
const thicknessFactor = networkConfig.edgeThickness;
width = baseWidth * (1 + thicknessFactor);
```

**Test:** Slider 0 = constant, 2 = extreme variation

#### 2.5 Verify localStorage (MEDIUM)
**Test:**
- Set sliders → refresh → check positions
- Browser DevTools → Application → Local Storage
- Console log on page load: retrieved values

#### 2.6 Adjust Initial Zoom (LOW)
**Implementation:**
```javascript
// After loadDataFromSheets()
window.network.fit({ animation: false, scale: 0.7 });
```

---

### Phase 3: Testing & Validation
**Workflow (per TESTING.md):**
1. Browser test each fix individually
2. Show console logs as evidence
3. Take screenshots before/after
4. User verification last

**Test Checklist:**
- ✅ TH edges thick near orphans (browser inspector)
- ✅ Scaling slider affects Jon's size (visual)
- ✅ Fading slider affects distant edges (visual)
- ✅ Thickness slider affects edge width (visual)
- ✅ Settings persist after refresh (localStorage check)
- ✅ Initial zoom appropriate (visual)

---

### Phase 4: Documentation Updates
**Per docs/README.md workflow:**

1. **Update KNOWN_ISSUES.md:**
   - Move resolved items to "Recently Resolved"
   - Add date, root cause, fix applied
   
2. **Update CONTEXT_RECOVERY.md:**
   - "Recent Completions" section
   - Town Hall visualization complete with Network settings

3. **This plan (NEMUP.md):**
   - Final status: Complete or issues remaining
   - Lessons learned

**No need to create:** CHANGELOG (not in this component)

---

### Phase 5: Git Workflow
**Per START_HERE_NEW_AI.md §2.6:**

```bash
# Already on feature branch or create one
git checkout -b feat/townhall-network-complete

# After all fixes tested and working
git add -A
git commit -m "fix: Complete Town Hall Network settings functionality

- Fix TH edge thickness/opacity distance calculation
- Implement Scaling Intensity slider (0=none, 1=log)
- Connect Edge Fading slider to opacity
- Connect Thickness Tuning slider to width
- Verify localStorage persistence
- Adjust initial zoom to scale 0.7"

# Push and PR if desired, or merge to main
git push origin feat/townhall-network-complete
```

---

## Execution Timeline

**Estimated:** 90-120 minutes

1. **Phase 1: Git commit** (5 min) - Protect work
2. **Phase 2: Debug/fix** (60 min) - Fix issues one by one
3. **Phase 3: Testing** (20 min) - Verify each fix
4. **Phase 4: Docs** (10 min) - Update KNOWN_ISSUES, CONTEXT_RECOVERY
5. **Phase 5: Final commit** (5 min) - Clean submission

**Critical:** Test after EACH fix, not after all fixes

---

## Success Criteria

**Features working:**
- ✅ Thick grey edges from TH to nearby orphans
- ✅ Scaling slider changes node sizes (console logs confirm)
- ✅ Fading slider changes edge opacity
- ✅ Thickness slider changes edge width
- ✅ Settings persist after refresh
- ✅ Initial zoom appropriate

**Process followed:**
- ✅ Tested each fix in browser before moving on
- ✅ Showed console logs as evidence
- ✅ Updated documentation
- ✅ No guessing (verified with inspector/logs)

---

**Back to:** [README.md](README.md) | [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md)
