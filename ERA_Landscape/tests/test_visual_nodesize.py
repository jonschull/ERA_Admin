#!/usr/bin/env python3
"""Visual test - take screenshots to verify Node Size actually changes node rendering"""

from playwright.sync_api import sync_playwright
import time
import os

def test_visual_node_size():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Visible for debugging
        context = browser.new_context(viewport={'width': 1600, 'height': 1000})
        page = context.new_page()
        
        # Create screenshots directory
        screenshot_dir = "tests/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        print("1. Loading page...")
        page.goto('http://localhost:8765', wait_until='networkidle', timeout=10000)
        time.sleep(3)
        page.wait_for_function("window.__edgeAdjustmentComplete === true", timeout=10000)
        
        # Zoom to a consistent view focused on center nodes
        print("\n2. Setting consistent view...")
        page.evaluate("window.network.moveTo({scale: 0.5})")
        time.sleep(1)
        
        # Take baseline screenshot
        print("\n3. Screenshot at default size (nodeSize=1.0, scaling=1.0)...")
        page.screenshot(path=f"{screenshot_dir}/nodesize_1_baseline.png")
        print(f"   Saved: {screenshot_dir}/nodesize_1_baseline.png")
        
        # Open Network modal, set Node Scaling to 0 (constant)
        print("\n4. Setting Node Scaling = 0 (constant size)...")
        page.click("#networkBtn")
        time.sleep(0.5)
        
        page.evaluate("document.getElementById('scalingIntensity').value = 0")
        page.evaluate("document.getElementById('scalingIntensity').dispatchEvent(new Event('input'))")
        time.sleep(1)
        
        page.click("#applyNetwork")
        time.sleep(0.5)
        
        page.screenshot(path=f"{screenshot_dir}/nodesize_2_constant_scaling.png")
        print(f"   Saved: {screenshot_dir}/nodesize_2_constant_scaling.png")
        print("   CHECK: All nodes should be equal size now")
        
        # Set Node Size to 0.5 (small)
        print("\n5. Setting Node Size = 0.5 (small)...")
        page.click("#networkBtn")
        time.sleep(0.5)
        
        page.evaluate("document.getElementById('nodeSize').value = 0.5")
        page.evaluate("document.getElementById('nodeSize').dispatchEvent(new Event('input'))")
        time.sleep(1)
        
        page.click("#applyNetwork")
        time.sleep(0.5)
        
        page.screenshot(path=f"{screenshot_dir}/nodesize_3_size_0.5.png")
        print(f"   Saved: {screenshot_dir}/nodesize_3_size_0.5.png")
        print("   CHECK: Nodes should be SMALLER than previous screenshot")
        
        # Set Node Size to 2.0 (large)
        print("\n6. Setting Node Size = 2.0 (large)...")
        page.click("#networkBtn")
        time.sleep(0.5)
        
        page.evaluate("document.getElementById('nodeSize').value = 2.0")
        page.evaluate("document.getElementById('nodeSize').dispatchEvent(new Event('input'))")
        time.sleep(1)
        
        page.click("#applyNetwork")
        time.sleep(0.5)
        
        page.screenshot(path=f"{screenshot_dir}/nodesize_4_size_2.0.png")
        print(f"   Saved: {screenshot_dir}/nodesize_4_size_2.0.png")
        print("   CHECK: Nodes should be MUCH LARGER than screenshot 3")
        
        # Get actual canvas pixel data to measure a sample node
        print("\n7. Analyzing node sizes in canvas...")
        node_measurements = page.evaluate("""() => {
            // Get canvas context
            const canvas = document.querySelector('canvas');
            const ctx = canvas.getContext('2d');
            
            // Get a sample node position
            const sampleNode = nodes.get().find(n => n.id.startsWith('person::'));
            const pos = window.network.getPositions([sampleNode.id])[sampleNode.id];
            const canvasPos = window.network.canvasToDOM(pos);
            
            return {
                nodeLabel: sampleNode.label,
                nodeValue: sampleNode.value,
                canvasX: canvasPos.x,
                canvasY: canvasPos.y
            };
        }""")
        
        print(f"   Sample node: {node_measurements['nodeLabel']}")
        print(f"   Data value: {node_measurements['nodeValue']:.2f}")
        print(f"   Canvas position: ({node_measurements['canvasX']:.0f}, {node_measurements['canvasY']:.0f})")
        
        browser.close()
        
        print("\n=== MANUAL VALIDATION REQUIRED ===")
        print(f"Compare screenshots in {screenshot_dir}/:")
        print("1. nodesize_2_constant_scaling.png - all nodes equal")
        print("2. nodesize_3_size_0.5.png - nodes SMALL")
        print("3. nodesize_4_size_2.0.png - nodes LARGE (4x bigger than #2)")
        print("\nIf nodes look the same size in all 3 → ❌ BUG NOT FIXED")
        print("If nodes change size progressively → ✅ WORKING")
        
        return True

if __name__ == "__main__":
    test_visual_node_size()
