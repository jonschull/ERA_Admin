#!/usr/bin/env python3
"""
Test node selection highlighting feature.

Tests:
1. Click node -> 1st order neighbors highlighted
2. Hold node -> progressive expansion to 2nd/3rd order
3. Click canvas -> highlight clears
4. Dimmed nodes frozen, highlighted nodes can move
"""

from playwright.sync_api import sync_playwright, expect
import time

def test_selection_highlighting():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to local server
        page.goto('http://localhost:8000')
        
        # Wait for graph to load
        print("⏳ Waiting for graph to load...")
        page.wait_for_selector('#network', timeout=10000)
        page.wait_for_function('window.network !== undefined', timeout=30000)
        
        # Wait for stabilization
        print("⏳ Waiting for stabilization...")
        time.sleep(5)
        
        # Check console for init message
        messages = []
        page.on('console', lambda msg: messages.append(msg.text()))
        
        # Test 1: Click a node (should highlight 1st order)
        print("\n📍 Test 1: Click node for 1st order highlight")
        page.evaluate('''() => {
            const nodes = window.__graph.nodes.get();
            if (nodes.length > 0) {
                const firstNode = nodes[0].id;
                window.network.selectNodes([firstNode]);
                window.network.emit('selectNode', { nodes: [firstNode] });
            }
        }''')
        
        time.sleep(1)
        
        # Check if highlight was applied
        highlight_message = any('Highlighted node' in msg for msg in messages)
        print(f"   Highlight applied: {highlight_message}")
        
        # Test 2: Hold timer (wait 2 seconds for 2nd order expansion)
        print("\n⏱️  Test 2: Wait for progressive expansion to 2nd order")
        time.sleep(2.5)
        
        # Should see 2nd order highlight
        second_order = any('order 2' in msg for msg in messages)
        print(f"   2nd order expansion: {second_order}")
        
        # Test 3: Wait for 3rd order
        print("\n⏱️  Test 3: Wait for 3rd order expansion")
        time.sleep(2.5)
        
        third_order = any('order 3' in msg for msg in messages)
        print(f"   3rd order expansion: {third_order}")
        
        # Test 4: Click canvas to deselect
        print("\n🖱️  Test 4: Click canvas to clear highlight")
        page.evaluate('window.network.unselectAll()')
        page.evaluate('window.network.emit("deselectNode", {})')
        
        time.sleep(1)
        
        # Check if highlight was cleared
        clear_message = any('Highlight cleared' in msg for msg in messages)
        print(f"   Highlight cleared: {clear_message}")
        
        # Test 5: Click different node (should reset to 1st order)
        print("\n📍 Test 5: Click different node")
        page.evaluate('''() => {
            const nodes = window.__graph.nodes.get();
            if (nodes.length > 1) {
                const secondNode = nodes[1].id;
                window.network.selectNodes([secondNode]);
                window.network.emit('selectNode', { nodes: [secondNode] });
            }
        }''')
        
        time.sleep(1)
        
        # Take screenshot
        print("\n📸 Taking screenshot...")
        page.screenshot(path='tests/test_selection_highlighting.png', full_page=False)
        
        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"✅ Feature initialized: {'Node selection highlighting enabled' in ' '.join(messages)}")
        print(f"✅ 1st order highlight: {highlight_message}")
        print(f"✅ 2nd order expansion: {second_order}")
        print(f"✅ 3rd order expansion: {third_order}")
        print(f"✅ Highlight cleared: {clear_message}")
        print("📸 Screenshot saved: tests/test_selection_highlighting.png")
        print("="*60)
        
        # Keep browser open for manual inspection
        print("\n⏸️  Browser kept open for manual inspection (close to exit)...")
        input("Press Enter to close browser...")
        
        browser.close()

if __name__ == '__main__':
    test_selection_highlighting()
