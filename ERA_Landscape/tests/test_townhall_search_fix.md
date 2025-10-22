# Manual Test: Town Hall Search Fix

**Issue:** Typing "T" in quicksearch causes Town Halls to drift inward  
**Fix:** Preserve `physics: false, fixed: {x:true, y:true}` for Town Halls even when visible/highlighted

## Test Steps

1. **Start server:**
   ```bash
   cd ERA_Landscape
   python3 -m http.server 8765
   open http://localhost:8765
   ```

2. **Wait for page load** (loading screen disappears)

3. **Verify initial state:**
   - Open browser console (Cmd+Option+J)
   - Run:
     ```javascript
     // Check Town Hall count and positions
     const townHalls = nodes.get().filter(n => n.id.startsWith('event::Town Hall'));
     const thPositions = network.getPositions();
     console.log(`Town Halls: ${townHalls.length}`);
     townHalls.slice(0, 3).forEach(th => {
       const pos = thPositions[th.id];
       console.log(`${th.label}: (${pos.x.toFixed(0)}, ${pos.y.toFixed(0)}) physics=${th.physics} fixed=${JSON.stringify(th.fixed)}`);
     });
     ```
   - Expected: ~65 Town Halls at periphery (radius ~1000px), physics=false, fixed={x:true, y:true}

4. **Test search functionality:**
   - Type "T" in the "From" field (Quick Editor)
   - Wait 500ms for debounce
   - Observe:
     - ✅ Town Halls should be highlighted (yellow border or color change)
     - ✅ View should zoom to show matching nodes
     - ✅ Town Halls should **STAY FIXED** at periphery (NOT drift inward)

5. **Verify in console:**
   ```javascript
   // After typing 'T'
   const townHallsAfter = nodes.get().filter(n => n.id.startsWith('event::Town Hall'));
   const thPositionsAfter = network.getPositions();
   townHallsAfter.slice(0, 3).forEach(th => {
     const pos = thPositionsAfter[th.id];
     console.log(`${th.label}: (${pos.x.toFixed(0)}, ${pos.y.toFixed(0)}) physics=${th.physics} fixed=${JSON.stringify(th.fixed)}`);
   });
   ```
   - Expected: Same positions as before, physics=false, fixed={x:true, y:true}

6. **Clear search:**
   - Clear the "From" field
   - Wait 500ms
   - Verify Town Halls still at periphery

## Expected Results

✅ **Color highlighting works** - matching nodes highlighted  
✅ **Zoom to selected works** - view auto-fits to visible nodes  
✅ **Town Halls stay fixed** - no drift when searched  
✅ **Town Halls stay fixed** - positions unchanged after clear

## Failure Modes

❌ Town Halls drift inward when "T" is typed  
❌ Town Halls have physics=true or fixed=false after search  
❌ Town Hall positions change (x/y coordinates differ by >10px)

## Code Changed

**File:** `ERA_Landscape/graph.js`  
**Lines:** 1050-1071  
**Change:** Added `isTownHall` check before setting physics/fixed properties

```javascript
const isTownHall = n.id.startsWith('event::Town Hall');

if(visibleSet.has(n.id)){
  const update = { id: n.id, opacity: 1 };
  
  // Town Halls must stay fixed at periphery even when visible
  if(isTownHall){
    update.physics = false;
    update.fixed = {x: true, y: true};
  } else {
    update.physics = true;
    update.fixed = false;
  }
  // ...
}
```
