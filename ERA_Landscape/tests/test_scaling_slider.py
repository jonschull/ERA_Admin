#!/usr/bin/env python3
"""Test Scaling Intensity slider changes node sizes"""

from playwright.sync_api import sync_playwright
import time

def test_scaling_slider():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        print("1. Loading page...")
        page.goto('http://localhost:8765', wait_until='networkidle', timeout=10000)
        time.sleep(3)
        page.wait_for_function("window.__edgeAdjustmentComplete === true", timeout=10000)
        
        # Find Jon Schull's initial size
        print("\n2. Getting Jon Schull's initial size...")
        jon_initial = page.evaluate("""() => {
            const jon = nodes.get().find(n => n.label === 'Jon Schull');
            return jon ? jon.value : null;
        }""")
        print(f"   Jon Schull value: {jon_initial}")
        
        # Open Network modal
        print("\n3. Opening Network settings...")
        page.click("#networkBtn")
        time.sleep(0.5)
        
        # Get initial slider value
        initial_intensity = page.evaluate("document.getElementById('scalingIntensity').value")
        print(f"   Initial scaling intensity: {initial_intensity}")
        
        # Move slider to 0 (no scaling)
        print("\n4. Moving slider to 0 (no scaling)...")
        page.evaluate("document.getElementById('scalingIntensity').value = 0")
        page.evaluate("document.getElementById('scalingIntensity').dispatchEvent(new Event('input'))")
        time.sleep(0.5)
        
        jon_at_zero = page.evaluate("""() => {
            const jon = nodes.get().find(n => n.label === 'Jon Schull');
            return jon ? jon.value : null;
        }""")
        print(f"   Jon Schull value at 0: {jon_at_zero}")
        
        # Move slider to 1 (full logarithmic)
        print("\n5. Moving slider to 1 (logarithmic)...")
        page.evaluate("document.getElementById('scalingIntensity').value = 1")
        page.evaluate("document.getElementById('scalingIntensity').dispatchEvent(new Event('input'))")
        time.sleep(0.5)
        
        jon_at_one = page.evaluate("""() => {
            const jon = nodes.get().find(n => n.label === 'Jon Schull');
            return jon ? jon.value : null;
        }""")
        print(f"   Jon Schull value at 1: {jon_at_one}")
        
        # Close modal
        page.click("#applyNetwork")
        
        browser.close()
        
        print("\n=== VERDICT ===")
        success = True
        
        if jon_initial is None:
            print("❌ Jon Schull not found")
            return False
        
        # At 0, size should be constant (around 10)
        if jon_at_zero > 15:
            print(f"❌ At 0 scaling: Jon still large ({jon_at_zero}), should be ~10")
            success = False
        else:
            print(f"✅ At 0 scaling: Jon normalized ({jon_at_zero})")
        
        # At 1, size should be logarithmic (around log(60) ≈ 4.1)
        if jon_at_one > 10:
            print(f"❌ At 1 scaling: Jon too large ({jon_at_one}), should be ~4 (log scale)")
            success = False
        else:
            print(f"✅ At 1 scaling: Jon logarithmic ({jon_at_one})")
        
        # Values should be different
        if abs(jon_at_zero - jon_at_one) < 1:
            print(f"❌ Slider has no effect (values too similar: {jon_at_zero} vs {jon_at_one})")
            success = False
        else:
            print(f"✅ Slider works: {jon_at_zero:.1f} (at 0) → {jon_at_one:.1f} (at 1)")
        
        if success:
            print("\n✅ SCALING SLIDER TEST PASSED")
            return True
        else:
            print("\n❌ TEST FAILED")
            return False

if __name__ == "__main__":
    success = test_scaling_slider()
    exit(0 if success else 1)
