#!/usr/bin/env python3
"""
Playwright test for Phase 4B-2 approval table.
Validates fixes and enables iterative tuning.
"""

from playwright.sync_api import sync_playwright, expect
from pathlib import Path
import sys

def test_approval_table():
    """Test the generated approval table for correctness."""
    
    # Find latest HTML file
    script_dir = Path(__file__).parent
    html_files = list(script_dir.glob("phase4b2_TEST_APPROVALS_*.html"))
    if not html_files:
        print("❌ No approval table HTML files found")
        return False
    
    latest_html = max(html_files, key=lambda p: p.stat().st_mtime)
    print(f"🧪 Testing: {latest_html.name}")
    print("=" * 80)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Load the HTML file
        page.goto(f"file://{latest_html}")
        
        results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        
        # Test 1: Check fuzzy Airtable matching
        print("\n1️⃣  Testing fuzzy Airtable matching...")
        
        # Mike Lynn should match Michael Lynn
        mike_row = page.locator('tr:has-text("Mike Lynn")').first
        airtable_cell = mike_row.locator('td').nth(4)  # In Airtable column
        airtable_text = airtable_cell.inner_text()
        
        if '✅' in airtable_text and 'Michael' in airtable_text:
            results['passed'].append("✅ Mike Lynn matched to Michael Lynn (fuzzy)")
            print(f"   ✅ Mike Lynn → {airtable_text.strip()}")
        else:
            results['failed'].append(f"❌ Mike Lynn not fuzzy matched (got: {airtable_text})")
            print(f"   ❌ Mike Lynn → {airtable_text.strip()}")
        
        # Neal Spackman should match (Neil/Neal variant)
        neal_row = page.locator('tr:has-text("Neal Spackman")').first
        airtable_cell = neal_row.locator('td').nth(4)
        airtable_text = airtable_cell.inner_text()
        
        if '✅' in airtable_text:
            results['passed'].append(f"✅ Neal Spackman matched in Airtable: {airtable_text.strip()}")
            print(f"   ✅ Neal Spackman → {airtable_text.strip()}")
        else:
            results['warnings'].append(f"⚠️  Neal Spackman not matched (got: {airtable_text})")
            print(f"   ⚠️  Neal Spackman → {airtable_text.strip()}")
        
        # Test 2: Check Gmail search works for hyphenated names
        print("\n2️⃣  Testing Gmail search for hyphenated names...")
        
        petruzzi_row = page.locator('tr:has-text("Petruzzi-McHale")').first
        gmail_cell = petruzzi_row.locator('td').nth(5)  # Gmail column
        gmail_text = gmail_cell.inner_text()
        
        if '📧' in gmail_text and 'emails' in gmail_text.lower():
            emails_count = gmail_text.split('📧')[1].split('email')[0].strip()
            results['passed'].append(f"✅ C. Petruzzi-McHale: Found {emails_count} emails")
            print(f"   ✅ C. Petruzzi-McHale → Found {emails_count} emails")
        else:
            results['failed'].append(f"❌ C. Petruzzi-McHale: {gmail_text}")
            print(f"   ❌ C. Petruzzi-McHale → {gmail_text}")
        
        # Test 3: Check no "check if in Airtable" obsolete comments
        print("\n3️⃣  Testing for obsolete comments...")
        
        obsolete_comments = page.locator('textarea:has-text("check if in Airtable")').count()
        if obsolete_comments == 0:
            results['passed'].append("✅ No obsolete 'check if in Airtable' comments")
            print("   ✅ No obsolete comments found")
        else:
            results['failed'].append(f"❌ Found {obsolete_comments} obsolete comments")
            print(f"   ❌ Found {obsolete_comments} obsolete 'check if in Airtable' comments")
        
        # Test 4: Check suggestions use Airtable matches
        print("\n4️⃣  Testing suggestion quality...")
        
        # Mike Lynn should suggest merge (since in Airtable)
        mike_comment = mike_row.locator('textarea').input_value()
        if 'merge with:' in mike_comment.lower() and 'michael' in mike_comment.lower():
            results['passed'].append("✅ Mike Lynn suggests merge with Michael Lynn")
            print(f"   ✅ Mike Lynn → {mike_comment}")
        else:
            results['warnings'].append(f"⚠️  Mike Lynn suggestion: {mike_comment}")
            print(f"   ⚠️  Mike Lynn → {mike_comment}")
        
        # Test 5: Check table structure
        print("\n5️⃣  Testing table structure...")
        
        total_rows = page.locator('#approvalTable tbody tr').count()
        if total_rows == 25:
            results['passed'].append(f"✅ Table has {total_rows} rows")
            print(f"   ✅ Table has {total_rows} rows (expected 25)")
        else:
            results['failed'].append(f"❌ Table has {total_rows} rows (expected 25)")
            print(f"   ❌ Table has {total_rows} rows (expected 25)")
        
        # Test 6: Check Gmail links are clickable
        print("\n6️⃣  Testing Gmail links...")
        
        gmail_links = page.locator('a[href*="mail.google.com"]').count()
        if gmail_links >= 25:  # Should have at least one per person
            results['passed'].append(f"✅ {gmail_links} Gmail links present")
            print(f"   ✅ {gmail_links} Gmail links present")
        else:
            results['failed'].append(f"❌ Only {gmail_links} Gmail links (expected ≥25)")
            print(f"   ❌ Only {gmail_links} Gmail links (expected ≥25)")
        
        # Test 7: Check CSV export function exists
        print("\n7️⃣  Testing CSV export...")
        
        export_button = page.locator('button:has-text("Export to CSV")').count()
        if export_button > 0:
            results['passed'].append("✅ CSV export button present")
            print("   ✅ CSV export button present")
        else:
            results['failed'].append("❌ CSV export button missing")
            print("   ❌ CSV export button missing")
        
        browser.close()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        print(f"\n✅ PASSED ({len(results['passed'])}):")
        for item in results['passed']:
            print(f"   {item}")
        
        if results['warnings']:
            print(f"\n⚠️  WARNINGS ({len(results['warnings'])}):")
            for item in results['warnings']:
                print(f"   {item}")
        
        if results['failed']:
            print(f"\n❌ FAILED ({len(results['failed'])}):")
            for item in results['failed']:
                print(f"   {item}")
        
        # Overall result
        print("\n" + "=" * 80)
        if not results['failed']:
            print("✅ ALL TESTS PASSED")
            return True
        else:
            print(f"❌ {len(results['failed'])} TESTS FAILED")
            return False


if __name__ == "__main__":
    try:
        success = test_approval_table()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
