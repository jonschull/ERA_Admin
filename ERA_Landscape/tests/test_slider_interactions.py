#!/usr/bin/env python3
"""Test slider interactions - check for state corruption after multiple operations"""

from playwright.sync_api import sync_playwright
import time

def test_slider_sequence():
    """Test sliders work correctly through a sequence of operations"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        console_messages = []
        page.on('console', lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
        
        print("1. Loading page...")
        page.goto('http://localhost:8765', wait_until='networkidle', timeout=10000)
        time.sleep(3)
        page.wait_for_function("window.__edgeAdjustmentComplete === true", timeout=10000)
        
        # Get a sample node
        sample = page.evaluate("""() => {
            const node = window.__graph.nodes.get().find(n => n.id.startsWith('person::'));
            return {id: node.id, label: node.label, value: node.value};
        }""")
        print(f"   Tracking: {sample['label']} (initial: {sample['value']:.2f})")
        
        results = {}
        
        # Test 1: Node Scaling = 0 (constant), Node Size should still work
        print("\n2. TEST 1: Node Scaling = 0 (constant), then adjust Node Size")
        page.click("#networkBtn")
        time.sleep(0.3)
        
        # Set scaling to 0
        page.evaluate("document.getElementById('scalingIntensity').value = 0")
        page.evaluate("document.getElementById('scalingIntensity').dispatchEvent(new Event('input'))")
        time.sleep(0.5)
        
        val_at_constant = page.evaluate(f"window.__graph.nodes.get('{sample['id']}').value")
        print(f"   After scaling=0: {val_at_constant:.2f}")
        
        # Now change node size to 0.5
        page.evaluate("document.getElementById('nodeSize').value = 0.5")
        page.evaluate("document.getElementById('nodeSize').dispatchEvent(new Event('input'))")
        time.sleep(0.5)
        
        val_at_half_size = page.evaluate(f"window.__graph.nodes.get('{sample['id']}').value")
        print(f"   After size=0.5: {val_at_half_size:.2f}")
        
        ratio = val_at_half_size / val_at_constant if val_at_constant > 0 else 0
        print(f"   Ratio: {ratio:.2f} (expect 0.5)")
        results['nodesize_at_constant_scaling'] = abs(ratio - 0.5) < 0.1
        
        page.click("#applyNetwork")
        time.sleep(0.3)
        
        # Test 2: Open Physics modal, adjust Central Gravity
        print("\n3. TEST 2: Physics - Central Gravity adjustment")
        page.click("#physicsBtn")
        time.sleep(0.3)
        
        initial_cg = page.evaluate("document.getElementById('centralGravity').value")
        print(f"   Initial Central Gravity: {initial_cg}")
        
        page.evaluate("document.getElementById('centralGravity').value = 0.5")
        page.evaluate("document.getElementById('centralGravity').dispatchEvent(new Event('input'))")
        time.sleep(0.5)
        
        # Check console for physics update
        physics_msgs = [msg for msg in console_messages if 'Physics updated' in msg]
        if physics_msgs:
            print(f"   ✅ Physics updated (found {len(physics_msgs)} messages)")
            results['physics_central_gravity'] = True
        else:
            print(f"   ❌ Physics NOT updated (no console message)")
            results['physics_central_gravity'] = False
        
        page.click("#applyPhysics")
        time.sleep(0.3)
        
        # Test 3: Open Network again, verify Node Size still works
        print("\n4. TEST 3: Network modal again - verify Node Size still responsive")
        page.click("#networkBtn")
        time.sleep(0.3)
        
        # Change size to 2.0
        page.evaluate("document.getElementById('nodeSize').value = 2.0")
        page.evaluate("document.getElementById('nodeSize').dispatchEvent(new Event('input'))")
        time.sleep(0.5)
        
        val_after_reopen = page.evaluate(f"window.__graph.nodes.get('{sample['id']}').value")
        print(f"   After reopening and size=2.0: {val_after_reopen:.2f}")
        
        # Should be 4x the half-size value (from 0.5 to 2.0)
        ratio2 = val_after_reopen / val_at_half_size if val_at_half_size > 0 else 0
        print(f"   Ratio to previous: {ratio2:.2f} (expect 4.0 since 2.0/0.5)")
        results['nodesize_after_physics'] = abs(ratio2 - 4.0) < 0.5
        
        page.click("#applyNetwork")
        
        # Test 4: Physics again - verify still works
        print("\n5. TEST 4: Physics modal again - verify Central Gravity still works")
        page.click("#physicsBtn")
        time.sleep(0.3)
        
        page.evaluate("document.getElementById('centralGravity').value = 0.2")
        page.evaluate("document.getElementById('centralGravity').dispatchEvent(new Event('input'))")
        time.sleep(0.5)
        
        physics_msgs2 = [msg for msg in console_messages if 'Physics updated' in msg and 'centralGravity: 0.2' in msg]
        if physics_msgs2:
            print(f"   ✅ Physics updated with new value")
            results['physics_after_network'] = True
        else:
            print(f"   ❌ Physics NOT updated")
            results['physics_after_network'] = False
        
        browser.close()
        
        # Report
        print("\n=== RESULTS ===")
        for test, passed in results.items():
            status = "✅" if passed else "❌"
            print(f"{status} {test}")
        
        all_passed = all(results.values())
        print(f"\n{'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
        
        if not all_passed:
            print("\nRecent console messages:")
            for msg in console_messages[-15:]:
                print(f"  {msg}")
        
        return all_passed

if __name__ == "__main__":
    success = test_slider_sequence()
    exit(0 if success else 1)
