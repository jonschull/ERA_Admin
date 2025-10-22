#!/usr/bin/env python3
"""Test that Physics sliders still work after using Network modal"""

from playwright.sync_api import sync_playwright
import time

def test_physics_after_network():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        console_messages = []
        page.on('console', lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
        
        print("1. Loading page...")
        page.goto('http://localhost:8765', wait_until='networkidle', timeout=10000)
        time.sleep(3)
        
        print("\n2. Opening Network modal and adjusting slider...")
        page.click("#networkBtn")
        time.sleep(0.5)
        
        page.evaluate("document.getElementById('nodeSize').value = 1.5")
        page.evaluate("document.getElementById('nodeSize').dispatchEvent(new Event('input'))")
        time.sleep(0.5)
        
        # Check console for network settings applied
        network_applied = [msg for msg in console_messages if 'Applied network settings' in msg]
        print(f"   Network settings applied: {len(network_applied)} times")
        
        page.click("#applyNetwork")
        time.sleep(0.5)
        
        print("\n3. Opening Physics modal and adjusting slider...")
        page.click("#physicsBtn")
        time.sleep(0.5)
        
        # Try to adjust Central Gravity
        initial_cg = page.evaluate("document.getElementById('centralGravity').value")
        print(f"   Initial Central Gravity: {initial_cg}")
        
        page.evaluate("document.getElementById('centralGravity').value = 0.5")
        page.evaluate("document.getElementById('centralGravity').dispatchEvent(new Event('input'))")
        time.sleep(0.5)
        
        # Check if physics was applied
        physics_applied = [msg for msg in console_messages if 'Physics updated' in msg]
        print(f"   Physics updated: {len(physics_applied)} times")
        
        if len(physics_applied) > 0:
            print(f"   Last physics message: {physics_applied[-1]}")
        
        browser.close()
        
        print("\n=== VERDICT ===")
        if len(physics_applied) > 0:
            print("✅ Physics sliders working after Network modal")
            return True
        else:
            print("❌ Physics sliders NOT working - no 'Physics updated' message")
            print(f"   Total console messages: {len(console_messages)}")
            return False

if __name__ == "__main__":
    success = test_physics_after_network()
    exit(0 if success else 1)
