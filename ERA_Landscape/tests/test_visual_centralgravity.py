#!/usr/bin/env python3
"""Visual test - verify Central Gravity actually affects node layout"""

from playwright.sync_api import sync_playwright
import time
import os

def test_visual_central_gravity():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1600, 'height': 1000})
        page = context.new_page()
        
        screenshot_dir = "tests/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        print("1. Loading page...")
        page.goto('http://localhost:8765', wait_until='networkidle', timeout=10000)
        time.sleep(3)
        page.wait_for_function("window.__edgeAdjustmentComplete === true", timeout=10000)
        
        # Let physics settle
        print("\n2. Letting initial physics settle (5 seconds)...")
        time.sleep(5)
        
        # Zoom to consistent view
        page.evaluate("window.network.moveTo({scale: 0.4})")
        time.sleep(1)
        
        # Baseline
        print("\n3. Baseline screenshot (default Central Gravity = 0.15)...")
        page.screenshot(path=f"{screenshot_dir}/gravity_1_baseline.png")
        
        # Measure spread
        spread_baseline = page.evaluate("""() => {
            const positions = window.network.getPositions();
            // Only measure mobile nodes (exclude fixed Town Halls)
            const mobileNodes = window.__graph.nodes.get().filter(n => !n.id.startsWith('event::Town Hall'));
            const mobileIds = mobileNodes.map(n => n.id);
            const coords = mobileIds.map(id => positions[id]).filter(p => p);
            const xs = coords.map(p => p.x);
            const ys = coords.map(p => p.y);
            const minX = Math.min(...xs);
            const maxX = Math.max(...xs);
            const minY = Math.min(...ys);
            const maxY = Math.max(...ys);
            return {
                width: maxX - minX,
                height: maxY - minY,
                spread: Math.sqrt((maxX - minX)**2 + (maxY - minY)**2)
            };
        }""")
        print(f"   Spread: {spread_baseline['spread']:.0f}px")
        
        # Set Central Gravity to 0.6 (tight)
        print("\n4. Setting Central Gravity = 0.6 (tight)...")
        page.click("#physicsBtn")
        time.sleep(0.5)
        
        page.evaluate("document.getElementById('centralGravity').value = 0.6")
        page.evaluate("document.getElementById('centralGravity').dispatchEvent(new Event('input'))")
        time.sleep(0.5)
        
        # Check what value was actually set
        actual_cg = page.evaluate("window.network.physics.options.barnesHut.centralGravity")
        print(f"   Confirmed centralGravity set to: {actual_cg}")
        
        page.click("#applyPhysics")
        
        # Let physics pull nodes toward center
        print("   Waiting for physics to pull nodes together (15 seconds)...")
        time.sleep(15)
        
        page.screenshot(path=f"{screenshot_dir}/gravity_2_tight_0.6.png")
        
        spread_tight = page.evaluate("""() => {
            const positions = window.network.getPositions();
            const mobileNodes = window.__graph.nodes.get().filter(n => !n.id.startsWith('event::Town Hall'));
            const mobileIds = mobileNodes.map(n => n.id);
            const coords = mobileIds.map(id => positions[id]).filter(p => p);
            const xs = coords.map(p => p.x);
            const ys = coords.map(p => p.y);
            return Math.sqrt((Math.max(...xs) - Math.min(...xs))**2 + (Math.max(...ys) - Math.min(...ys))**2);
        }""")
        print(f"   Spread: {spread_tight:.0f}px")
        print(f"   CHECK: Should be SMALLER than baseline ({spread_baseline['spread']:.0f}px)")
        
        # Set Central Gravity to 0.05 (loose)
        print("\n5. Setting Central Gravity = 0.05 (loose)...")
        page.click("#physicsBtn")
        time.sleep(0.5)
        
        page.evaluate("document.getElementById('centralGravity').value = 0.05")
        page.evaluate("document.getElementById('centralGravity').dispatchEvent(new Event('input'))")
        time.sleep(0.5)
        
        page.click("#applyPhysics")
        
        # Let nodes spread out
        print("   Waiting for nodes to spread out (8 seconds)...")
        time.sleep(8)
        
        page.screenshot(path=f"{screenshot_dir}/gravity_3_loose_0.05.png")
        
        spread_loose = page.evaluate("""() => {
            const positions = window.network.getPositions();
            const mobileNodes = window.__graph.nodes.get().filter(n => !n.id.startsWith('event::Town Hall'));
            const mobileIds = mobileNodes.map(n => n.id);
            const coords = mobileIds.map(id => positions[id]).filter(p => p);
            const xs = coords.map(p => p.x);
            const ys = coords.map(p => p.y);
            return Math.sqrt((Math.max(...xs) - Math.min(...xs))**2 + (Math.max(...ys) - Math.min(...ys))**2);
        }""")
        print(f"   Spread: {spread_loose:.0f}px")
        print(f"   CHECK: Should be LARGER than tight ({spread_tight:.0f}px)")
        
        browser.close()
        
        print("\n=== ANALYSIS ===")
        print(f"Baseline (0.15):  {spread_baseline['spread']:.0f}px")
        print(f"Tight (0.6):      {spread_tight:.0f}px")
        print(f"Loose (0.05):     {spread_loose:.0f}px")
        
        # Expected: tight < baseline < loose
        success = True
        
        if spread_tight < spread_baseline['spread']:
            print("✅ Tight is more compact than baseline")
        else:
            print(f"❌ Tight ({spread_tight:.0f}) NOT smaller than baseline ({spread_baseline['spread']:.0f})")
            success = False
        
        if spread_loose > spread_baseline['spread']:
            print("✅ Loose is more spread out than baseline")
        else:
            print(f"❌ Loose ({spread_loose:.0f}) NOT larger than baseline ({spread_baseline['spread']:.0f})")
            success = False
        
        if spread_tight < spread_loose:
            print("✅ Tight < Loose (correct order)")
        else:
            print(f"❌ Tight ({spread_tight:.0f}) NOT less than Loose ({spread_loose:.0f})")
            success = False
        
        print(f"\n{'✅ CENTRAL GRAVITY WORKING' if success else '❌ CENTRAL GRAVITY NOT WORKING'}")
        print(f"\nScreenshots saved in {screenshot_dir}/")
        
        return success

if __name__ == "__main__":
    success = test_visual_central_gravity()
    exit(0 if success else 1)
