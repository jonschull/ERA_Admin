#!/usr/bin/env python3
"""Comprehensive test of Node Size slider affecting all node types"""

from playwright.sync_api import sync_playwright
import time

def test_node_size_all_types():
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
        
        # Sample different node types
        print("\n2. Getting initial sizes of different node types...")
        initial_sizes = page.evaluate("""() => {
            const allNodes = window.__graph.nodes.get();
            
            // Find one of each type
            const person = allNodes.find(n => n.id.startsWith('person::'));
            const org = allNodes.find(n => n.id.startsWith('org::'));
            const project = allNodes.find(n => n.id.startsWith('project::'));
            const townhall = allNodes.find(n => n.id.startsWith('event::Town Hall'));
            
            return {
                person: person ? {id: person.id, label: person.label, value: person.value} : null,
                org: org ? {id: org.id, label: org.label, value: org.value} : null,
                project: project ? {id: project.id, label: project.label, value: project.value} : null,
                townhall: townhall ? {id: townhall.id, label: townhall.label, value: townhall.value} : null
            };
        }""")
        
        print(f"   Person: {initial_sizes['person']['label'] if initial_sizes['person'] else 'NONE'} = {initial_sizes['person']['value'] if initial_sizes['person'] else 'N/A'}")
        print(f"   Org: {initial_sizes['org']['label'] if initial_sizes['org'] else 'NONE'} = {initial_sizes['org']['value'] if initial_sizes['org'] else 'N/A'}")
        print(f"   Project: {initial_sizes['project']['label'] if initial_sizes['project'] else 'NONE'} = {initial_sizes['project']['value'] if initial_sizes['project'] else 'N/A'}")
        print(f"   TownHall: {initial_sizes['townhall']['label'] if initial_sizes['townhall'] else 'NONE'} = {initial_sizes['townhall']['value'] if initial_sizes['townhall'] else 'N/A'}")
        
        # Open Network modal and change to 0.5
        print("\n3. Setting Node Size to 0.5 (small)...")
        page.click("#networkBtn")
        time.sleep(0.5)
        
        page.evaluate("document.getElementById('nodeSize').value = 0.5")
        page.evaluate("document.getElementById('nodeSize').dispatchEvent(new Event('input'))")
        time.sleep(0.5)
        
        sizes_at_half = page.evaluate("""() => {
            const allNodes = window.__graph.nodes.get();
            const person = allNodes.find(n => n.id.startsWith('person::'));
            const org = allNodes.find(n => n.id.startsWith('org::'));
            const project = allNodes.find(n => n.id.startsWith('project::'));
            const townhall = allNodes.find(n => n.id.startsWith('event::Town Hall'));
            
            return {
                person: person ? person.value : null,
                org: org ? org.value : null,
                project: project ? project.value : null,
                townhall: townhall ? townhall.value : null
            };
        }""")
        
        print(f"   Person: {sizes_at_half['person']}")
        print(f"   Org: {sizes_at_half['org']}")
        print(f"   Project: {sizes_at_half['project']}")
        print(f"   TownHall: {sizes_at_half['townhall']}")
        
        # Change to 2.0
        print("\n4. Setting Node Size to 2.0 (large)...")
        page.evaluate("document.getElementById('nodeSize').value = 2.0")
        page.evaluate("document.getElementById('nodeSize').dispatchEvent(new Event('input'))")
        time.sleep(0.5)
        
        sizes_at_double = page.evaluate("""() => {
            const allNodes = window.__graph.nodes.get();
            const person = allNodes.find(n => n.id.startsWith('person::'));
            const org = allNodes.find(n => n.id.startsWith('org::'));
            const project = allNodes.find(n => n.id.startsWith('project::'));
            const townhall = allNodes.find(n => n.id.startsWith('event::Town Hall'));
            
            return {
                person: person ? person.value : null,
                org: org ? org.value : null,
                project: project ? project.value : null,
                townhall: townhall ? townhall.value : null
            };
        }""")
        
        print(f"   Person: {sizes_at_double['person']}")
        print(f"   Org: {sizes_at_double['org']}")
        print(f"   Project: {sizes_at_double['project']}")
        print(f"   TownHall: {sizes_at_double['townhall']}")
        
        page.click("#applyNetwork")
        browser.close()
        
        print("\n=== ANALYSIS ===")
        
        # Check if values changed at all
        success = True
        
        for node_type in ['person', 'org', 'project', 'townhall']:
            initial = initial_sizes[node_type]['value'] if initial_sizes[node_type] else None
            at_half = sizes_at_half[node_type]
            at_double = sizes_at_double[node_type]
            
            if initial is None or at_half is None or at_double is None:
                print(f"⚠️  {node_type.capitalize()}: missing data")
                continue
            
            # At 0.5, should be ~50% of initial (which is at 1.0)
            # At 2.0, should be ~200% of initial
            ratio_half = at_half / initial if initial > 0 else 0
            ratio_double = at_double / initial if initial > 0 else 0
            
            print(f"\n{node_type.capitalize()}:")
            print(f"  Initial (1.0): {initial:.2f}")
            print(f"  At 0.5: {at_half:.2f} (ratio: {ratio_half:.2f}x, expect ~0.5x)")
            print(f"  At 2.0: {at_double:.2f} (ratio: {ratio_double:.2f}x, expect ~2.0x)")
            
            # Check if slider is working (allow 10% tolerance)
            if abs(ratio_half - 0.5) > 0.1:
                print(f"  ❌ At 0.5: ratio {ratio_half:.2f} not near 0.5")
                success = False
            else:
                print(f"  ✅ At 0.5: correct scaling")
            
            if abs(ratio_double - 2.0) > 0.2:
                print(f"  ❌ At 2.0: ratio {ratio_double:.2f} not near 2.0")
                success = False
            else:
                print(f"  ✅ At 2.0: correct scaling")
        
        print("\n=== VERDICT ===")
        if success:
            print("✅ NODE SIZE SLIDER WORKING for all node types")
            return True
        else:
            print("❌ NODE SIZE SLIDER NOT WORKING CORRECTLY")
            print("\nConsole messages:")
            for msg in console_messages[-10:]:
                print(f"  {msg}")
            return False

if __name__ == "__main__":
    success = test_node_size_all_types()
    exit(0 if success else 1)
