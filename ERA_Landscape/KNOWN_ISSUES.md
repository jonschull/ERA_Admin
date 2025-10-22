# Known Issues - ERA Landscape

**See also:** [NETWORK_ARCHITECTURE.md](NETWORK_ARCHITECTURE.md) for technical details

## Active Issues

### ❌ Central Gravity Slider Inverted Behavior (Oct 22, 2025)
**Status:** Broken - produces opposite of expected behavior  
**Symptom:** Higher central gravity spreads nodes MORE instead of pulling them tighter

**Evidence:** Visual test `test_visual_centralgravity.py`
- Baseline (0.4): 5704px spread
- Tight (0.6): 6829px spread ❌ (should be < baseline)
- Loose (0.05): 7699px spread ✅ (correctly larger)

**Hypothesis:** 65 fixed Town Halls at periphery (`physics: false`) interfere with barnesHut centralGravity calculations

**Workaround:** Use Node Spacing slider instead to control layout density

**Planned Fix:** Investigate centrality-based spreading system (variable spring length by distance from center) - see NETWORK_ARCHITECTURE.md "Future Work"

---

## Recently Resolved (Oct 22, 2025)

### ✅ RESOLVED: Node Size Slider Not Working Visually (Oct 21-22, 2025)
**Status:** Fixed - nodes now resize visually when slider moves  
**Symptom:** Node Size slider changed JavaScript `value` but nodes didn't change size on screen

**Root Cause:** vis.js requires BOTH:
1. Update node `value` properties
2. Update `scaling.min/max` range
3. Call `network.redraw()`

**Fix Applied:**
```javascript
// Update vis.js scaling range based on nodeSize multiplier
window.network.setOptions({
  nodes: {
    scaling: {
      min: baseMin * networkConfig.nodeSize,
      max: baseMax * networkConfig.nodeSize
    }
  }
});
window.network.redraw();
```

**Validation:** Screenshot test `test_visual_nodesize.py` confirms 4x visual size difference ✅

### ✅ RESOLVED: Slider Ranges Too Narrow (Oct 22, 2025)
**Status:** Fixed - all sliders now have wider ranges with defaults in middle

**Changes:**
- Network Settings: All ranges expanded (Node Size 0.5-2.0 → 0.2-3.0, etc.)
- Physics Settings: Ranges expanded, defaults moved to middle (Central Gravity 0.15 → 0.4)
- Provides "elbow room" for experimentation

## Recently Added (Oct 21, 2025)

### ✅ Town Hall Network Visualization Complete
**Added:** Town Hall integration with Network settings panel  
**Features:**
- 65 Town Halls positioned in circular ring at periphery (radius 1000px)
- Grey edges with distance-based thickness/opacity
  - <450px: Thick (2.5 width), 80% opacity
  - 450-700px: Medium thickness, fading
  - >700px: Thin (0.5 width), nearly invisible
- Network settings panel with 3 sliders:
  - Scaling Intensity: 0 (constant) → 1 (logarithmic)
  - Edge Fading: 0 (no fade) → 1 (50% reduction)
  - Edge Thickness: 0 (base) → 2 (2x multiplier)
- Settings persist to localStorage
- Initial zoom: scale 0.8 for better overview

**Tests:** 3 Playwright tests created, all passing

---

## Recently Resolved

### 1. ✅ RESOLVED: Nodes Not Settling (Oct 21, 2025)
**Status:** Fixed - nodes settle naturally within 5-10 seconds  
**Symptom:** Nodes continue to move/wiggle indefinitely, never stabilizing  

**Root Cause Analysis:**
- Stabilization was being disabled during slider adjustments
- Low damping (0.09) wasn't stopping motion effectively
- Low minVelocity (0.1) allowed tiny movements to continue indefinitely
- Stabilization was being re-disabled on every slider change

**Fix Applied:**
- Increased damping: 0.09 → 0.15 (stops motion faster)
- Increased minVelocity: 0.1 → 0.75 (stops tiny movements)
- Added flag to track when actively adjusting vs initial load
- Only disable stabilization during active slider adjustment
- Force stabilization on Done button with explicit trigger
- Increased timeout from 500ms → 800ms before re-enabling

**Additional Fix (Oct 21, 7:44pm):**
- Removed Settle button (was freezing nodes and preventing dragging)
- Changed strategy: NO stabilization after initial load
- Increased minVelocity: 0.75 → 1.5 (stops movements < 1.5 units/frame)
- Reduced timestep: 0.5 → 0.35 (smoother physics simulation)
- Increased damping to 0.15 (was 0.09)
- All stabilization triggers removed - rely purely on physics parameters

**Theory:** High damping + high minVelocity should naturally stop micro-movements without locking nodes

**Final Tuning (Oct 21, 7:47pm):**
- User confirmed nodes DO settle but too slowly (~15-20 seconds)
- Increased damping: 0.15 → 0.35 (133% increase = much faster deceleration)
- Increased minVelocity: 1.5 → 2.5 (67% increase = stops sooner)
- Goal: Settle within 5-8 seconds

**Status:** Nodes now settle naturally while remaining draggable throughout

---

### ✅ Event Type Added for Town Halls (Oct 21, 2025)
**Added:** New 'event' node type with hexagon shape, grey color, reduced scaling (30% rate, max 10)

### ✅ Town Hall Linear Chain (Oct 21, 2025)
**Fixed:** Town Halls now form linear chain (Project → TH 01 → TH 02...) instead of all connecting to umbrella

### ✅ Modal UI Improvements (Oct 21, 2025)
**Fixed:** 
- Removed grey overlay from modals (transparent background)
- Physics controls redesigned with centered labels, endpoint labels (loose/tight, etc.)
- Values now float and follow slider handles

### ✅ Double-click opens both modal and URL (Oct 21, 2025)
**Fixed:** Removed duplicate doubleClick handler

### ✅ Orphan nodes drifting too far (Oct 21, 2025)
**Fixed:** Position orphans in circle near center, increased central gravity to 0.15

### ✅ Curation modal opens on single-click (Oct 21, 2025)
**Fixed:** Changed to double-click only

### ✅ Physics modal styling (Oct 21, 2025)
**Fixed:** Made draggable, semi-transparent, narrower (380px)

### ✅ Physics settings not persisted (Oct 21, 2025)
**Fixed:** Save to localStorage, restore on load
