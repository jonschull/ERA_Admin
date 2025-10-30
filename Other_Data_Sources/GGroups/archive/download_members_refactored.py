#!/usr/bin/env python3
"""
Download Google Groups member list using browser automation.

Refactored to use ggroups_auth module (DRY principle).

Usage:
    python download_members_refactored.py
    
Prerequisites:
    1. Export cookies using cookie extension → ggroups_cookies.json
    2. Install playwright: pip install playwright && playwright install msedge
"""

from pathlib import Path
from datetime import datetime
from ggroups_auth import authenticate_ggroups, verify_authentication

# Configuration
SCRIPT_DIR = Path(__file__).parent
GROUP_URL = "https://groups.google.com/g/ecorestoration-alliance/members"
DOWNLOAD_DIR = SCRIPT_DIR / "downloads"
OUTPUT_FILE = SCRIPT_DIR / f"members_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

def download_members():
    """Download Google Groups member list."""
    print("=" * 80)
    print("GOOGLE GROUPS MEMBER DOWNLOAD")
    print("=" * 80)
    print()
    
    # Create download directory
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    
    # Authenticate using the reusable module
    with authenticate_ggroups(downloads_path=DOWNLOAD_DIR) as page:
        print("✅ Authenticated with Microsoft Edge")
        print()
        
        # Navigate to group members page
        print(f"📍 Navigating to: {GROUP_URL}")
        page.goto(GROUP_URL, wait_until='networkidle', timeout=60000)
        
        # Wait a moment for page to settle
        page.wait_for_timeout(2000)
        
        # Verify authentication
        print("🔍 Checking authentication...")
        if not verify_authentication(page):
            print("❌ Authentication failed - not on members page")
            screenshot_path = SCRIPT_DIR / "auth_failed.png"
            page.screenshot(path=str(screenshot_path))
            print(f"   Screenshot saved: {screenshot_path}")
            return False
        
        print("✅ Authenticated - member list visible")
        
        # Find the download button
        download_button = None
        selectors = [
            'button:has(svg path[d*="M19 9h-4V3H9v6H5l7 7 7-7"])',  # Material download icon
            'button[aria-label*="Download"]',
            'button[aria-label*="download"]',
            'text=Add members >> xpath=following-sibling::button[1]',
            'button[jsname]:has(svg)',
        ]
        
        for selector in selectors:
            try:
                btn = page.locator(selector).first
                if btn.is_visible(timeout=2000):
                    download_button = btn
                    print("✅ Found download button")
                    break
            except:
                continue
        
        if not download_button:
            print("⚠️  Could not find download button automatically")
            print("   Taking screenshot - you may need to click manually")
            screenshot_path = SCRIPT_DIR / "need_manual_click.png"
            page.screenshot(path=str(screenshot_path))
            print(f"   Screenshot: {screenshot_path}")
            print("\n   Waiting 30 seconds for manual download...")
            page.wait_for_timeout(30000)
            return False
        
        # Click download button
        print("📥 Clicking download button...")
        
        # Wait for download to start
        with page.expect_download() as download_info:
            download_button.click()
        
        download = download_info.value
        
        # Save the download
        print(f"💾 Saving to: {OUTPUT_FILE}")
        download.save_as(OUTPUT_FILE)
        
        print()
        print("=" * 80)
        print("✅ SUCCESS")
        print("=" * 80)
        print(f"Member list saved: {OUTPUT_FILE}")
        print()
        
        # Quick preview
        if OUTPUT_FILE.exists():
            with open(OUTPUT_FILE, 'r') as f:
                lines = f.readlines()
                print(f"Downloaded {len(lines)} lines")
                if len(lines) > 1:
                    print("\nFirst few lines:")
                    for line in lines[:5]:
                        print(f"  {line.strip()}")
        
        return True

if __name__ == "__main__":
    success = download_members()
    exit(0 if success else 1)
