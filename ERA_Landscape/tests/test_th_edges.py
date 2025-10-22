#!/usr/bin/env python3
"""Test Town Hall edge thickness and positioning"""

from playwright.sync_api import sync_playwright
import time

def test_th_edges():
    """Test that TH edges to nearby orphans are thick and visible"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Collect console messages
        console_messages = []
        errors = []
        page.on('console', lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
        page.on('pageerror', lambda err: errors.append(str(err)))
        
        print("1. Loading page on localhost:8765...")
        try:
            page.goto('http://localhost:8765', wait_until='networkidle', timeout=10000)
        except Exception as e:
            print(f"   ❌ Failed to load. Is server running? (python3 -m http.server 8765)")
            return False
        
        print("2. Waiting for data load...")
        time.sleep(3)
        
        print("3. Waiting for setTimeout to fire (up to 10 seconds)...")
        try:
            # Wait for the setTimeout callback to execute and log the adjustment message
            page.wait_for_function(
                "window.__edgeAdjustmentComplete === true",
                timeout=10000
            )
            print("   ✅ Edge adjustment completed!")
        except Exception as e:
            print(f"   ⚠️ Timeout waiting for edge adjustment: {e}")
        
        # First show ALL console messages
        print(f"\n3. All console messages ({len(console_messages)} total):")
        for msg in console_messages:
            print(f"   {msg}")
        
        print("\n4. Analyzing key messages:")
        
        # Check for TH positioning
        th_positioned = None
        for msg in console_messages:
            if 'Fixed' in msg and 'Town Halls' in msg:
                th_positioned = msg
                print(f"   ✅ {msg}")
                break
        if not th_positioned:
            print("   ❌ Town Halls NOT positioned")
        
        # Check for orphan positioning
        orphan_positioned = None
        for msg in console_messages:
            if 'Positioned' in msg and 'orphan' in msg:
                orphan_positioned = msg
                print(f"   ✅ {msg}")
                break
        if not orphan_positioned:
            print("   ❌ Orphans NOT positioned")
        
        # Check for edge adjustments - THIS IS THE KEY TEST
        edge_adjustment = None
        near_count = 0
        for msg in console_messages:
            if 'Adjusted' in msg and 'TH→person' in msg:
                edge_adjustment = msg
                print(f"   ✅ {msg}")
                
                # Parse near/medium/far counts
                import re
                match = re.search(r'(\d+) near.*?(\d+) medium.*?(\d+) far', msg)
                if match:
                    near_count = int(match.group(1))
                    medium_count = int(match.group(2))
                    far_count = int(match.group(3))
                    print(f"      📊 Distribution: {near_count} near, {medium_count} medium, {far_count} far")
                break
        
        if not edge_adjustment:
            print("   ❌ Edge adjustment NOT executed")
        
        # Check for warnings
        warnings = [msg for msg in console_messages if 'warn' in msg.lower() or '⚠️' in msg]
        if warnings:
            print("\n4. Warnings:")
            for w in warnings:
                print(f"   ⚠️ {w}")
        
        # Check for errors
        if errors:
            print(f"\n5. JavaScript errors: {len(errors)}")
            for err in errors:
                print(f"   ❌ {err}")
        else:
            print("\n5. ✅ No JavaScript errors")
        
        browser.close()
        
        # Verdict
        print("\n=== VERDICT ===")
        success = True
        
        if not th_positioned:
            print("❌ Town Halls not positioned")
            success = False
        else:
            print("✅ Town Halls positioned in circle")
        
        if not orphan_positioned:
            print("❌ Orphans not positioned")
            success = False
        else:
            print("✅ Orphans positioned")
        
        if not edge_adjustment:
            print("❌ Edge distance adjustment not executed")
            success = False
        elif near_count == 0:
            print(f"❌ No near edges found! Orphans may still be too far from TH ring")
            success = False
        else:
            print(f"✅ {near_count} near edges found (thick grey edges should be visible)")
        
        if errors:
            print(f"❌ {len(errors)} JavaScript errors")
            success = False
        
        if success:
            print("\n✅ TH EDGE TEST PASSED")
            print(f"   {near_count} thick grey edges from Town Halls to nearby orphans")
            return True
        else:
            print("\n❌ TEST FAILED")
            print("   Review console logs above for details")
            return False

if __name__ == "__main__":
    success = test_th_edges()
    exit(0 if success else 1)
