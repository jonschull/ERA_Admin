# ERA_Landscape/NETWORK_ARCHITECTURE.md

# Network Visualization Architecture

**Purpose:** Technical documentation of ERA Landscape's network graph implementation  
**Audience:** Developers and AI assistants working on the visualization layer

## Table of Contents
1. [Overview](#overview)
2. [Town Hall Special Treatment](#town-hall-special-treatment)
3. [Node Sizing System](#node-sizing-system)
4. [Physics Engine](#physics-engine)
5. [User Controls](#user-controls)
6. [Testing](#testing)

---

## Overview

### Technology Stack
- **Library:** vis-network.js (v9.1.9)
- **Physics Solver:** barnesHut
- **Data Sources:** Google Sheets API
- **Node Types:** Person, Organization, Project, Event (Town Halls)

### Core Architecture
```
Google Sheets Data → JavaScript Processing → vis.js DataSets → Network Rendering
                                              ↓
                                     Physics Simulation
                                              ↓
                                     User Interactions
```

**Key Files:**
- `index.html` - Main UI, modals, and event handlers
- `graph.js` - vis.js initialization and options
- `tests/test_visual_*.py` - Screenshot-based visual validation tests

---

## Town Hall Special Treatment

### Why Special?
Town Hall events have **65 nodes** at the periphery that serve as temporal landmarks. They must remain **fixed in position** while other nodes (people, orgs, projects) are mobile.

### Implementation

**Location:** `index.html` lines 696-715

```javascript
// Position Town Hall events in a fixed circle at periphery
const townHalls = nodesPayload.filter(node => node.id.startsWith('event::Town Hall'));
if (townHalls.length > 0) {
  const thUpdates = townHalls.map((node, idx) => {
    // Arrange in a large circle (radius 1000px)
    const angle = (idx / townHalls.length) * 2 * Math.PI;
    const radius = 1000;
    const x = Math.cos(angle) * radius;
    const y = Math.sin(angle) * radius;
    
    return {
      ...node,
      x: x,
      y: y,
      fixed: { x: true, y: true },  // Fixed position
      physics: false  // Don't participate in physics simulation
    };
  });
  nodes.update(thUpdates);
}
```

**Key Properties:**
- `physics: false` - Town Halls don't move, don't exert forces
- `fixed: {x: true, y: true}` - Locked at specified coordinates
- `radius: 1000px` - Peripheral ring distance from center (0,0)
- Arranged in circular order by chronological index

**Implications:**
1. **Physics sliders** affect only mobile nodes (people/orgs/projects)
2. **Central Gravity** pulls mobile nodes toward center, not toward THs
3. **Spread measurements** should exclude Town Halls (see `tests/test_visual_centralgravity.py`)
4. **Edge adjustment** - TH→person edges fade by distance (see `adjustTHEdges()`)

---

## Node Sizing System

### How Node Sizes Work

vis.js uses a **two-stage sizing system**:

1. **Data Value** → Node's `value` property (JavaScript number)
2. **Visual Scaling** → `scaling.min` and `scaling.max` (pixel range)

**Formula:**
```
Visual Size (px) = scaling.min + (normalized_value × (scaling.max - scaling.min))
```

### Implementation

**Initial Load:** `index.html` lines 658-679
```javascript
const updates = nodesPayload.map(node => {
  const connections = connectionCount[node.id] || 1;
  const type = parseTypeFromId(node.id);
  
  let finalValue;
  if (type === 'event') {
    // Town Halls: capped scaling with nodeSize multiplier
    finalValue = Math.min(connections * 0.3, 10) * networkConfig.nodeSize;
  } else {
    // Other nodes: blend constant ↔ logarithmic based on scalingIntensity
    const constantScale = 10;
    const logScale = Math.log(connections + 1);
    const intensity = networkConfig.scalingIntensity;
    const blendedScale = constantScale + (logScale - constantScale) * intensity;
    finalValue = blendedScale * networkConfig.nodeSize;
  }
  
  return { ...node, value: finalValue };
});
```

**Dynamic Scaling:** `index.html` lines 1187-1202
```javascript
// Update vis.js scaling range based on nodeSize multiplier
if (window.network) {
  const baseMin = 12;
  const baseMax = 60;
  window.network.setOptions({
    nodes: {
      scaling: {
        min: baseMin * networkConfig.nodeSize,
        max: baseMax * networkConfig.nodeSize
      }
    }
  });
  window.network.redraw();
}
```

**Why This Matters:**
- Changing `value` alone doesn't resize nodes visually
- Must also update `scaling.min/max` and call `redraw()`
- This is why Node Size slider was initially broken (values changed but visuals didn't)

### Connection Weighting

**Town Hall edges:** Count as `0.1` instead of `1.0` to avoid inflating node sizes
```javascript
const weight = edge.isTownHallEdge ? 0.1 : 1;
connectionCount[edge.from] = (connectionCount[edge.from] || 0) + weight;
```

---

## Physics Engine

### Configuration

**Location:** `graph.js` lines 5-22

```javascript
physics: {
  barnesHut: {
    gravitationalConstant: -2000,    // Node-to-node repulsion
    centralGravity: 0.4,             // Pull toward center (0,0)
    springLength: 175,               // Natural edge length
    springConstant: 0.04,            // Spring tightness
    damping: 0.35,                   // Movement decay
    avoidOverlap: 0.2                // Overlap repulsion (use sparingly)
  },
  maxVelocity: 50,
  minVelocity: 2.5,
  solver: 'barnesHut',
  timestep: 0.35,
  adaptiveTimestep: true,
  stabilization: { enabled: true, iterations: 1000 }
}
```

### How It Works

**barnesHut Solver:**
- Simulates N-body gravitational forces efficiently (O(n log n))
- Nodes repel each other (`gravitationalConstant < 0`)
- Edges act as springs pulling nodes together
- Central gravity pulls toward origin (0,0)
- Damping causes motion to slow and settle

**Key Parameters:**

| Parameter | Effect | Default | Range |
|-----------|--------|---------|-------|
| `centralGravity` | Pull toward center | 0.4 | 0-1.0 |
| `springLength` | Natural edge length | 175px | 50-400 |
| `springConstant` | Spring tightness | 0.04 | 0.001-0.15 |
| `avoidOverlap` | Overlap repulsion | 0.2 | 0-1.0 |

**⚠️ Known Issue:** Central Gravity produces inverted behavior
- Expected: Higher → tighter clustering
- Actual: Higher → more spread
- Hypothesis: Fixed Town Hall ring interferes with barnesHut calculations
- See `tests/test_visual_centralgravity.py` for evidence

---

## User Controls

### Network Settings Modal (🌐)

**Purpose:** Visual appearance (node sizes, edge visibility)

| Slider | Range | Default | Effect |
|--------|-------|---------|--------|
| Node Scaling | 0-2.0 | 1.0 | Blend constant ↔ logarithmic sizing |
| Node Size | 0.2-3.0 | 1.0 | Overall size multiplier |
| Edge Fading | 0-2.0 | 1.0 | TH edge opacity adjustment |
| Edge Thickness | 0-3.0 | 1.0 | TH edge width adjustment |

**Node Scaling Details:**
- `0.0` = All nodes same size (constant = 10)
- `1.0` = Logarithmic scaling by connections (default)
- `2.0` = Super-logarithmic scaling (exaggerated differences)

**Formula:**
```javascript
const constantScale = 10;
const logScale = Math.log(connections + 1);
const blendedScale = constantScale + (logScale - constantScale) * scalingIntensity;
const finalValue = blendedScale * nodeSize;
```

### Physics Settings Modal (⚙️)

**Purpose:** Network layout and spacing

| Slider | Range | Default | Effect |
|--------|-------|---------|--------|
| Central Gravity | 0-1.0 | 0.4 | Pull toward center ⚠️ |
| Node Spacing | 50-400 | 175 | Natural edge length |
| Edge Springs | 0.001-0.15 | 0.04 | Spring tightness |
| Avoid Overlap | 0-1.0 | 0.2 | Overlap repulsion (causes jitter) |
| Edge Length Multiplier | 0-30 | 10 | Per-degree spacing boost |
| Edge Length Max | 100-500 | 300 | Maximum edge length |

**⚠️ Central Gravity:** Known to be broken - higher values spread nodes instead of tightening

**Design Choice:** Defaults are in the **middle** of ranges to provide "elbow room" for experimentation

### Persistence

**localStorage Keys:**
- `scalingIntensity`, `nodeSize`, `edgeFading`, `edgeThickness`
- `era_physics_settings` (JSON object with all physics params)

Settings persist across browser sessions.

---

## Testing

### Visual Validation Tests

**Location:** `tests/test_visual_*.py`

**Purpose:** Screenshot-based validation to catch visual regressions

#### test_visual_nodesize.py
```bash
python3 tests/test_visual_nodesize.py
```
- Takes screenshots at Node Size 0.5, 1.0, 2.0
- Verifies 4x visual size difference between extremes
- **Result:** ✅ Passing (as of Oct 22, 2025)

#### test_visual_centralgravity.py
```bash
python3 tests/test_visual_centralgravity.py
```
- Measures mobile node spread at gravity 0.05, 0.4, 0.6
- Verifies tighter = smaller spread
- **Result:** ❌ Failing - tight config spreads nodes more (inverted)

#### test_slider_interactions.py
```bash
python3 tests/test_slider_interactions.py
```
- Tests slider behavior through multiple modal open/close cycles
- Verifies no state corruption between Physics/Network modals
- **Result:** ✅ Passing

### Test Strategy

**Why Screenshot Tests:**
- JavaScript values can change without visual effect
- vis.js rendering is complex (physics, scaling, canvas)
- Only way to validate "it looks right" is to look at it

**Test Pattern:**
```python
# 1. Load page
page.goto('http://localhost:8765')

# 2. Change setting
page.evaluate("document.getElementById('nodeSize').value = 2.0")
page.evaluate("document.getElementById('nodeSize').dispatchEvent(new Event('input'))")

# 3. Screenshot
page.screenshot(path='nodesize_2.0.png')

# 4. Measure (if possible)
spread = page.evaluate("/* calculate geometric spread */")
```

**Guidelines:**
- Always hard-refresh browser before manual testing (`Cmd+Shift+R`)
- Check both data values AND visual rendering
- Screenshot tests run on `localhost:8765` (must start server first)

---

## Future Work

### Planned Improvements

1. **Centrality-Based Spreading**
   - Variable spring length based on distance from center
   - Longer edges for central nodes → less crowding
   - Implementation: Option B from discussion (Oct 22, 2025)

2. **Fix Central Gravity**
   - Investigate Town Hall ring interference
   - Possibly implement custom radial force field
   - See KNOWN_ISSUES.md

3. **Repulsion Slider**
   - Expose `gravitationalConstant` (-2000 default)
   - Allow user to boost repulsion → spread central core
   - Recommended range: -1000 to -5000

4. **Better Visual Feedback**
   - Show physics "heat map" (which areas are active)
   - Edge length visualization
   - Connection count overlay

---

## Quick Reference

**Problem:** Nodes aren't resizing when I change Node Size slider  
**Solution:** Must update `scaling.min/max` AND call `redraw()`. See lines 1187-1202.

**Problem:** Central Gravity slider does the opposite of what I expect  
**Solution:** Known issue. Use Node Spacing slider instead.

**Problem:** Physics sliders stopped working after using Network modal  
**Solution:** Was a bug (fixed Oct 21, 2025). Hard-refresh browser.

**Problem:** Test passes but visual is wrong  
**Solution:** Test is checking data values, not rendered output. Use screenshot tests.

**Problem:** Want to spread out central nodes without affecting peripheral ring  
**Solution:** Increase Node Spacing (175→250) or reduce Edge Springs (0.04→0.02).

---

## Change Log

**Oct 22, 2025:**
- Updated slider ranges with wider "elbow room"
- Moved defaults to middle of ranges
- Central Gravity: 0.15→0.4, Node Spacing: 120→175, Edge Springs: 0.02→0.04

**Oct 21, 2025:**
- Fixed Node Size slider visual rendering (added `setOptions` + `redraw`)
- Fixed Physics slider position recalculation on modal open
- Added screenshot-based visual tests

**Oct 20, 2025:**
- Renamed "Scaling Intensity" → "Node Scaling"
- Added Node Size slider (0.5-2.0)
- Fixed Edge Fading and Edge Thickness labels

---

**Back to:** [README.md](README.md)