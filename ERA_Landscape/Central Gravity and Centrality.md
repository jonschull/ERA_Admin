# Central Gravity and Centrality-Based Spreading

**Created:** October 22, 2025  
**Status:** Planning Phase  
**Component:** ERA_Landscape visualization  
**Type:** Physics Enhancement

---

## Problem Statement

### Central Gravity Slider is Broken

The Central Gravity slider produces inverted/unexpected behavior:
- Higher gravity (0.6) → nodes spread MORE (6829px)
- Lower gravity (0.05) → nodes spread more (7699px)  
- Baseline (0.4) → 5704px spread

**Evidence:** Visual test `test_visual_centralgravity.py`

**Hypothesis:** The 65 fixed Town Halls at periphery (`physics: false`) interfere with barnesHut centralGravity calculations.

**Current Workaround:** Use Node Spacing slider instead.

---

## Proposed Solution: Centrality-Based Spreading System

Instead of fighting with centralGravity, **make edge springs longer/weaker for central nodes** so they naturally spread out more while peripheral nodes stay tight.

### Core Idea

- Calculate each node's distance from center (centrality)
- Apply variable spring length based on centrality
- Central nodes get longer/weaker springs → more spread
- Peripheral nodes keep short/stiff springs → stay tight
- Works WITH fixed Town Halls, doesn't fight physics

---

## Implementation Plan

### Step 1: Calculate Node Centrality

Add this function to `index.html`:

```javascript
/**
 * Calculate centrality for all nodes based on distance from center
 * @returns {Object} Map of nodeId -> centrality (0=center, 1=periphery)
 */
function calculateNodeCentrality() {
  const positions = window.network.getPositions();
  const centrality = {};
  
  // For each node, calculate distance from center (0,0)
  Object.keys(positions).forEach(nodeId => {
    const pos = positions[nodeId];
    const distance = Math.sqrt(pos.x * pos.x + pos.y * pos.y);
    
    // Normalize: 0 = center, 1 = at Town Hall ring (1000px)
    centrality[nodeId] = Math.min(distance / 1000, 1.0);
  });
  
  return centrality;
}
```

---

### Step 2: Apply Variable Spring Length

Modify edge springs based on BOTH connected nodes' centrality:

```javascript
/**
 * Apply variable spring length to edges based on node centrality
 * @param {number} spreadFactor - User control (0=no spread, 1=max spread)
 */
function applyVariableSpringLength(spreadFactor = 0.5) {
  const centrality = calculateNodeCentrality();
  const edges = window.edgesDataset.get();
  
  edges.forEach(edge => {
    // Skip Town Hall edges (they're special)
    if (edge.relationship === 'follows' || edge.relationship === 'attended') {
      return;
    }
    
    // Get centrality of both connected nodes
    const fromCentrality = centrality[edge.from] || 0;
    const toCentrality = centrality[edge.to] || 0;
    
    // Average centrality (both nodes matter)
    const avgCentrality = (fromCentrality + toCentrality) / 2;
    
    // Spring length grows for central nodes
    // User controls how much spreading happens
    const baseLength = 100;
    const maxLength = 100 + (200 * spreadFactor); // 0=no spread, 1=max spread
    const springLength = baseLength + (maxLength - baseLength) * (1 - avgCentrality);
    
    // Also reduce spring stiffness for central nodes
    const baseStiffness = 0.04;  // Current default
    const minStiffness = 0.04 - (0.03 * spreadFactor); // Weaken at high spread
    const springConstant = minStiffness + (baseStiffness - minStiffness) * avgCentrality;
    
    // Update edge
    window.edgesDataset.update({
      id: edge.id,
      length: springLength,
      physics: {
        springLength: springLength,
        springConstant: springConstant
      }
    });
  });
  
  console.log(`✅ Applied variable spring length to ${edges.length} edges (spread=${spreadFactor})`);
}
```

**Edge Behavior Examples:**

| Avg Centrality | Spread=0.5 | Spring Length | Spring Constant |
|----------------|------------|---------------|-----------------|
| 0.0 (center)   | 0.5        | 200px         | 0.025 (weak)    |
| 0.5 (mid)      | 0.5        | 150px         | 0.0325          |
| 1.0 (periphery)| 0.5        | 100px         | 0.04 (stiff)    |

---

### Step 3: Add UI Control

Add slider to Physics Settings modal in `index.html`:

```html
<!-- Add to Physics Settings modal -->
<div class="slider-container">
  <label for="centralSpread">Central Spread:</label>
  <input type="range" id="centralSpread" min="0" max="1" step="0.1" value="0.5">
  <span id="centralSpreadValue">0.5</span>
  <div class="slider-description">Higher = more room for central nodes</div>
</div>
```

---

### Step 4: Connect Slider to Function

```javascript
// Add event listener for Central Spread slider
document.getElementById('centralSpread').addEventListener('input', function(e) {
  const spreadFactor = parseFloat(e.target.value);
  document.getElementById('centralSpreadValue').textContent = spreadFactor.toFixed(1);
  
  // Apply spreading
  applyVariableSpringLength(spreadFactor);
  
  // Restart physics briefly to settle new spring configuration
  window.network.setOptions({ physics: { enabled: true } });
  setTimeout(() => {
    window.network.setOptions({ physics: { enabled: false } });
  }, 3000);
  
  // Save to config
  networkConfig.centralSpread = spreadFactor;
  localStorage.setItem('networkConfig', JSON.stringify(networkConfig));
});

// Load saved value on page init
document.addEventListener('DOMContentLoaded', function() {
  const savedConfig = JSON.parse(localStorage.getItem('networkConfig') || '{}');
  if (savedConfig.centralSpread !== undefined) {
    document.getElementById('centralSpread').value = savedConfig.centralSpread;
    document.getElementById('centralSpreadValue').textContent = savedConfig.centralSpread.toFixed(1);
  }
});
```

---

### Step 5: Call on Data Load

Integrate into the data loading workflow:

```javascript
// In loadDataFromSheets(), after graph is rendered
setTimeout(() => {
  console.log('🎯 Applying centrality-based spreading...');
  
  // Apply variable spring length based on saved config
  const spreadFactor = networkConfig.centralSpread || 0.5;
  applyVariableSpringLength(spreadFactor);
  
  // Let physics settle with new spring configuration
  window.network.setOptions({ physics: { enabled: true } });
  setTimeout(() => {
    window.network.setOptions({ physics: { enabled: false } });
    console.log('✅ Physics settled after spreading adjustment');
  }, 5000);
}, 1000);
```

---

## Expected Behavior

### Central Spread = 0 (No spreading)
- All edges same length (~100px)
- All springs same stiffness (0.04)
- Central cluster stays tight
- Same as current default behavior

### Central Spread = 0.5 (Medium - Default)
- Central nodes: ~200px edge length, 0.025 stiffness
- Mid-range nodes: ~150px edge length, 0.0325 stiffness
- Peripheral nodes: ~100px edge length, 0.04 stiffness
- Central cluster expands moderately
- Peripheral structure preserved

### Central Spread = 1.0 (Maximum)
- Central nodes: ~300px edge length, 0.01 stiffness (very weak)
- Peripheral nodes: ~100px edge length, 0.04 stiffness
- Central cluster spreads wide
- Peripheral structure tightly preserved

---

## Advantages Over Central Gravity

1. **Works WITH Town Halls** - Doesn't conflict with fixed nodes
2. **User-controllable** - Simple slider, predictable behavior
3. **Preserves structure** - Peripheral nodes stay organized
4. **Doesn't fight physics** - Natural force-directed result
5. **Granular control** - Affects individual edges, not global force
6. **Testable** - Can measure actual spring lengths

---

## Testing Strategy

### Manual Browser Testing

1. **Load page** - `python3 -m http.server 8000`
2. **Open Physics modal** - Click ⚙️ button
3. **Adjust Central Spread slider:**
   - 0 → Verify central cluster tight
   - 0.5 → Verify moderate spreading
   - 1.0 → Verify maximum spreading
4. **Check console logs** - Spring length updates
5. **Refresh page** - Verify setting persists

### Automated Testing

```python
# tests/test_central_spreading.py
from playwright.sync_api import sync_playwright
import math

def test_spring_lengths():
    """Verify central edges longer than peripheral edges"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:8765')
        
        # Wait for data load
        page.wait_for_selector('.loading-screen', state='hidden', timeout=30000)
        
        # Open Physics modal
        page.click('button:has-text("⚙")')
        
        # Set Central Spread = 1.0
        page.evaluate("document.getElementById('centralSpread').value = 1.0")
        page.evaluate("document.getElementById('centralSpread').dispatchEvent(new Event('input'))")
        
        # Wait for physics to settle
        page.wait_for_timeout(5000)
        
        # Get edge lengths via console
        edge_data = page.evaluate("""
            () => {
                const edges = window.edgesDataset.get();
                const centrality = {};
                const positions = window.network.getPositions();
                
                // Calculate centrality
                Object.keys(positions).forEach(nodeId => {
                    const pos = positions[nodeId];
                    const distance = Math.sqrt(pos.x * pos.x + pos.y * pos.y);
                    centrality[nodeId] = Math.min(distance / 1000, 1.0);
                });
                
                // Group edges by avg centrality
                const central = [];
                const peripheral = [];
                
                edges.forEach(edge => {
                    if (edge.relationship === 'follows' || edge.relationship === 'attended') {
                        return;
                    }
                    
                    const fromCent = centrality[edge.from] || 0;
                    const toCent = centrality[edge.to] || 0;
                    const avgCent = (fromCent + toCent) / 2;
                    
                    if (avgCent < 0.3) {
                        central.push(edge.length || edge.physics?.springLength);
                    } else if (avgCent > 0.7) {
                        peripheral.push(edge.length || edge.physics?.springLength);
                    }
                });
                
                return {
                    central_avg: central.reduce((a,b) => a+b, 0) / central.length,
                    peripheral_avg: peripheral.reduce((a,b) => a+b, 0) / peripheral.length
                };
            }
        """)
        
        # Assert central edges longer than peripheral
        assert edge_data['central_avg'] > edge_data['peripheral_avg'], \
            f"Central edges ({edge_data['central_avg']:.1f}px) should be longer than peripheral ({edge_data['peripheral_avg']:.1f}px)"
        
        print(f"✅ Central edges: {edge_data['central_avg']:.1f}px")
        print(f"✅ Peripheral edges: {edge_data['peripheral_avg']:.1f}px")
        
        browser.close()

if __name__ == '__main__':
    test_spring_lengths()
```

### Visual Validation

```python
# tests/test_visual_centrality_spread.py
def test_visual_spread():
    """Screenshot test for spread levels"""
    # Baseline (spread=0)
    # Medium (spread=0.5)
    # Maximum (spread=1.0)
    # Compare central node dispersion
```

---

## Implementation Timeline

### Phase 1: Core Logic (~1 hour)
- [ ] Add `calculateNodeCentrality()` function
- [ ] Add `applyVariableSpringLength()` function
- [ ] Test in browser console manually
- [ ] Verify spring lengths in inspector

### Phase 2: UI Integration (~30 min)
- [ ] Add slider to Physics modal HTML
- [ ] Wire up event handler
- [ ] Implement localStorage persistence
- [ ] Test slider interaction

### Phase 3: Data Load Integration (~20 min)
- [ ] Call from `loadDataFromSheets()`
- [ ] Verify timing (after layout, before freeze)
- [ ] Test page refresh persistence

### Phase 4: Testing (~30 min)
- [ ] Browser testing (all 3 spread levels)
- [ ] Create automated test
- [ ] Visual validation
- [ ] Edge length measurements

### Phase 5: Documentation (~20 min)
- [ ] Update NETWORK_ARCHITECTURE.md
- [ ] Update KNOWN_ISSUES.md (resolve Central Gravity issue)
- [ ] Add to README.md features list
- [ ] Update this plan with results

**Total Estimated Time:** ~2.5 hours

---

## Success Criteria

**Functional Requirements:**
- ✅ Central Spread slider (0-1.0 range)
- ✅ Central nodes have longer springs than peripheral
- ✅ Setting persists across page refreshes
- ✅ Physics settles within 5 seconds

**User Experience:**
- ✅ Slider 0 → tight central cluster
- ✅ Slider 0.5 → moderate spreading
- ✅ Slider 1.0 → wide central spreading
- ✅ Peripheral structure preserved at all levels
- ✅ Console logs confirm spring updates

**Testing:**
- ✅ Automated test verifies spring length gradient
- ✅ Visual validation shows expected behavior
- ✅ No regressions in other physics controls

---

## Alternative Approaches Considered

### 1. Fix Central Gravity Directly
**Rejected:** Town Hall ring interference too complex to untangle

### 2. Repulsion Slider (gravitationalConstant)
**Deferred:** Affects all nodes equally, not granular enough

### 3. Custom Radial Force Field
**Rejected:** Requires custom physics engine, over-engineered

### 4. Centrality-Based Spreading (THIS APPROACH)
**Selected:** 
- Works with existing physics
- Granular control
- Predictable behavior
- User-controllable

---

## Related Documentation

- [NETWORK_ARCHITECTURE.md](NETWORK_ARCHITECTURE.md) - Technical deep-dive
- [KNOWN_ISSUES.md](KNOWN_ISSUES.md) - Central Gravity bug details
- [README.md](README.md) - Feature overview
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development workflow

---

## Future Enhancements

After basic implementation works:

1. **Adaptive Centrality**
   - Recalculate on physics stabilization
   - Handle dynamic node movement

2. **Visual Feedback**
   - Show centrality heat map
   - Edge length overlay
   - Spring stiffness visualization

3. **Advanced Controls**
   - Separate length/stiffness multipliers
   - Non-linear centrality curves
   - Per-type spreading (people vs orgs)

4. **Performance**
   - Cache centrality calculations
   - Batch edge updates
   - Optimize for >1000 nodes

---

**Back to:** [README.md](README.md) | [NETWORK_ARCHITECTURE.md](NETWORK_ARCHITECTURE.md)
