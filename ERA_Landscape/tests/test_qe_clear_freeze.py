#!/usr/bin/env python3
"""Test Quick Editor clear doesn't freeze and preserves TH positions"""

from playwright.sync_api import sync_playwright
import time

def test_qe_clear():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        console_messages = []
        page.on('console', lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
        
        print("1. Loading page...")
        page.goto('http://localhost:8765', wait_until='networkidle', timeout=10000)
        time.sleep(3)
        
        # Wait for TH positioning
        page.wait_for_function("window.__edgeAdjustmentComplete === true", timeout=10000)
        
        print("2. Checking initial TH positions...")
        th_before = page.evaluate("""() => {
            const ths = nodes.get().filter(n => n.id.startsWith('event::Town Hall'));
            return ths.map(th => ({
                id: th.id,
                physics: th.physics,
                fixed: th.fixed,
                x: th.x,
                y: th.y
            }));
        }""")
        print(f"   Found {len(th_before)} Town Halls")
        print(f"   First TH: physics={th_before[0]['physics']}, fixed={th_before[0]['fixed']}")
        
        print("\n3. Typing search query...")
        page.fill("#qeFrom", "Jon")
        time.sleep(1)  # Wait for debounced filter
        
        print("\n4. Clearing search (testing for freeze)...")
        start_time = time.time()
        page.fill("#qeFrom", "")
        time.sleep(1)  # Wait for debounced filter
        clear_time = time.time() - start_time
        print(f"   Clear took {clear_time:.2f} seconds")
        
        print("\n5. Checking TH positions after clear...")
        th_after = page.evaluate("""() => {
            const ths = nodes.get().filter(n => n.id.startsWith('event::Town Hall'));
            return ths.map(th => ({
                id: th.id,
                physics: th.physics,
                fixed: th.fixed,
                x: th.x,
                y: th.y
            }));
        }""")
        print(f"   First TH: physics={th_after[0]['physics']}, fixed={th_after[0]['fixed']}")
        
        browser.close()
        
        print("\n=== VERDICT ===")
        success = True
        
        if clear_time > 2.0:
            print(f"❌ FREEZE: Clear took {clear_time:.2f}s (should be < 2s)")
            success = False
        else:
            print(f"✅ Performance OK: Clear took {clear_time:.2f}s")
        
        if th_before[0]['physics'] == False and th_after[0]['physics'] == True:
            print("❌ Town Halls lost fixed position (physics changed False → True)")
            success = False
        elif th_before[0]['physics'] == False and th_after[0]['physics'] == False:
            print("✅ Town Halls preserved fixed position (physics still False)")
        else:
            print(f"⚠️  Unexpected physics state: before={th_before[0]['physics']}, after={th_after[0]['physics']}")
        
        if success:
            print("\n✅ QE CLEAR TEST PASSED")
            return True
        else:
            print("\n❌ TEST FAILED")
            return False

if __name__ == "__main__":
    success = test_qe_clear()
    exit(0 if success else 1)
