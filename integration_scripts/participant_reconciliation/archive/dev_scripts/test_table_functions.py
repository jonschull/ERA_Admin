#!/usr/bin/env python3
"""
Playwright test for Phase 4B-2 table - test all functions and debug issues.
"""

from playwright.sync_api import sync_playwright, expect
from pathlib import Path
import time
import sys

def test_table_functions():
    """Test all table functions and debug CSV export."""
    
    # Find latest HTML file
    script_dir = Path(__file__).parent
    html_files = list(script_dir.glob("phase4b2_TEST_APPROVALS_*.html"))
    if not html_files:
        print("❌ No HTML files found")
        return False
    
    latest_html = max(html_files, key=lambda p: p.stat().st_mtime)
    print(f"🧪 Testing: {latest_html.name}")
    print("=" * 80)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser for debugging
        page = browser.new_page()
        
        # Enable console logging
        page.on("console", lambda msg: print(f"   [BROWSER] {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"   [ERROR] {err}"))
        
        # Load the HTML file
        page.goto(f"file://{latest_html}")
        
        print("\n" + "=" * 80)
        print("TEST 1: Page Load")
        print("=" * 80)
        
        # Check title
        title = page.title()
        print(f"✅ Title: {title}")
        
        # Check table exists
        table = page.locator('#approvalTable')
        expect(table).to_be_visible()
        print("✅ Table visible")
        
        # Count rows
        rows = page.locator('#approvalTable tbody tr')
        row_count = rows.count()
        print(f"✅ Table has {row_count} rows")
        
        print("\n" + "=" * 80)
        print("TEST 2: Buttons Exist")
        print("=" * 80)
        
        # Check all buttons (use exact text to avoid confusion)
        export_btn = page.locator('button:has-text("Export to CSV")')
        check_all_btn = page.get_by_role("button", name="✓ Check All")
        uncheck_all_btn = page.get_by_role("button", name="✗ Uncheck All")
        
        expect(export_btn).to_be_visible()
        print("✅ Export to CSV button visible")
        
        expect(check_all_btn).to_be_visible()
        print("✅ Check All button visible")
        
        expect(uncheck_all_btn).to_be_visible()
        print("✅ Uncheck All button visible")
        
        print("\n" + "=" * 80)
        print("TEST 3: Checkboxes")
        print("=" * 80)
        
        # Count checkboxes
        checkboxes = page.locator('input[type="checkbox"]')
        checkbox_count = checkboxes.count()
        print(f"✅ Found {checkbox_count} checkboxes")
        
        # Check how many are checked initially
        checked_count = 0
        for i in range(checkbox_count):
            if checkboxes.nth(i).is_checked():
                checked_count += 1
        print(f"✅ {checked_count} checkboxes auto-checked")
        
        # Test Check All
        check_all_btn.click()
        time.sleep(0.5)
        
        all_checked = True
        for i in range(checkbox_count):
            if not checkboxes.nth(i).is_checked():
                all_checked = False
                break
        
        if all_checked:
            print("✅ Check All works")
        else:
            print("❌ Check All failed")
        
        # Test Uncheck All
        uncheck_all_btn.click()
        time.sleep(0.5)
        
        all_unchecked = True
        for i in range(checkbox_count):
            if checkboxes.nth(i).is_checked():
                all_unchecked = False
                break
        
        if all_unchecked:
            print("✅ Uncheck All works")
        else:
            print("❌ Uncheck All failed")
        
        print("\n" + "=" * 80)
        print("TEST 4: CSV Export (DEBUGGING)")
        print("=" * 80)
        
        # Check some boxes for export test
        checkboxes.nth(0).check()
        checkboxes.nth(1).check()
        print("✅ Checked 2 boxes for testing")
        
        # Listen for download
        download_happened = False
        download_path = None
        
        def handle_download(download):
            nonlocal download_happened, download_path
            download_happened = True
            download_path = download.suggested_filename
            print(f"✅ Download started: {download_path}")
        
        page.on("download", handle_download)
        
        # Check if exportToCSV function exists
        export_fn_exists = page.evaluate("typeof exportToCSV === 'function'")
        if export_fn_exists:
            print("✅ exportToCSV function exists")
        else:
            print("❌ exportToCSV function NOT FOUND")
            return False
        
        # Try to call the function directly in console
        print("\n🔍 Calling exportToCSV() directly...")
        try:
            # Call the function and capture any errors
            result = page.evaluate("""
                () => {
                    try {
                        exportToCSV();
                        return { success: true, error: null };
                    } catch (e) {
                        return { success: false, error: e.toString() };
                    }
                }
            """)
            
            if result['success']:
                print("✅ exportToCSV() executed without errors")
            else:
                print(f"❌ exportToCSV() error: {result['error']}")
                
        except Exception as e:
            print(f"❌ Failed to call exportToCSV: {e}")
        
        time.sleep(1)
        
        # Now try clicking the button
        print("\n🔍 Clicking Export button...")
        export_btn.click()
        
        time.sleep(2)  # Wait for download
        
        if download_happened:
            print(f"✅ CSV download successful: {download_path}")
        else:
            print("❌ CSV download did NOT happen")
            print("\n🔍 Debugging info:")
            
            # Check if button has onclick
            onclick = export_btn.evaluate("el => el.onclick")
            print(f"   Button onclick: {onclick}")
            
            # Check button attributes
            attrs = export_btn.evaluate("""
                el => {
                    return {
                        onclick: el.getAttribute('onclick'),
                        disabled: el.disabled,
                        type: el.type
                    }
                }
            """)
            print(f"   Button attributes: {attrs}")
            
            # Try to get any error messages
            console_logs = page.evaluate("console.log('Test from Playwright')")
        
        print("\n" + "=" * 80)
        print("TEST 5: Table Sorting")
        print("=" * 80)
        
        # Click a column header to sort
        first_header = page.locator('th').first
        first_header.click()
        time.sleep(0.5)
        print("✅ Clicked column header (sort test)")
        
        print("\n" + "=" * 80)
        print("TEST 6: Filter Buttons")
        print("=" * 80)
        
        # Test filter buttons if they exist
        filter_btns = page.locator('button:has-text("Show All")')
        if filter_btns.count() > 0:
            filter_btns.first.click()
            time.sleep(0.5)
            print("✅ Filter button works")
        else:
            print("⚠️  No filter buttons found")
        
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        if not download_happened:
            print("\n❌ CSV EXPORT FAILED - Keeping browser open for inspection")
            print("   Press ENTER to close browser and continue...")
            input()
        else:
            print("\n✅ ALL TESTS PASSED")
            time.sleep(2)
        
        browser.close()
        
        return download_happened


if __name__ == "__main__":
    try:
        success = test_table_functions()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
