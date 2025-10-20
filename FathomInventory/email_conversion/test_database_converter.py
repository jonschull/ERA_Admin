#!/usr/bin/env python3
"""
Test the new database converter on all samples.
"""

import os
from fathom_email_2_md import convert_file

def test_all_samples():
    """Test the database converter on all HTML samples."""
    print("=" * 80)
    print("TESTING NEW DATABASE CONVERTER")
    print("=" * 80)
    
    total_success = 0
    total_failed = 0
    
    for i in range(1, 11):  # Test 1.html through 10.html
        html_file = f"{i}.html"
        md_file = f"{i}_new.md"
        
        if not os.path.exists(html_file):
            print(f"\n[{i}] MISSING: {html_file}")
            total_failed += 1
            continue
        
        print(f"\n[{i}] Converting {html_file}...")
        
        success, link_count, preview = convert_file(html_file, md_file)
        
        if success:
            print(f"    ✅ SUCCESS: Created {md_file}")
            print(f"    📊 Found {link_count} markdown links")
            print(f"    📄 Preview: {preview}")
            total_success += 1
        else:
            print(f"    ❌ FAILED: {preview}")
            total_failed += 1
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Successful conversions: {total_success}")
    print(f"❌ Failed conversions: {total_failed}")
    
    if total_success > 0:
        print(f"\n🎉 {total_success} files converted successfully!")
        print("📁 New Markdown files: *_new.md")
        print("💡 Compare with old results in *.md files")
    
    if total_failed > 0:
        print(f"\n⚠️  {total_failed} conversions failed")

if __name__ == '__main__':
    test_all_samples()
