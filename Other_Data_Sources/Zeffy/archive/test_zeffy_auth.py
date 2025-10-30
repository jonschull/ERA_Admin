#!/usr/bin/env python3
"""
Test Zeffy authentication with saved cookies.

PATTERN: Browser Cookie Authentication Pattern
BASED ON: GGroups/ggroups_auth.py

This script:
1. Loads cookies from zeffy_cookies.json
2. Launches Edge browser
3. Navigates to Zeffy dashboard
4. Takes screenshot to verify authentication
5. Waits 10 seconds for you to inspect
"""

import json
from pathlib import Path
from playwright.sync_api import sync_playwright

# Configuration
SCRIPT_DIR = Path(__file__).parent
COOKIE_FILE = SCRIPT_DIR / "zeffy_cookies.json"
ZEFFY_HOME = "https://www.zeffy.com"
ZEFFY_PAYMENTS = "https://www.zeffy.com/en-US/o/campaigns/all-payments"

def load_cookies():
    """Load cookies from JSON file."""
    if not COOKIE_FILE.exists():
        print(f"❌ Cookie file not found: {COOKIE_FILE}")
        print("   Run: ./refresh_zeffy_auth.sh")
        exit(1)
    
    with open(COOKIE_FILE, 'r') as f:
        cookies = json.load(f)
    
    return cookies

def test_authentication():
    """Test Zeffy authentication."""
    print("=" * 80)
    print("ZEFFY AUTHENTICATION TEST")
    print("=" * 80)
    print()
    
    # Load cookies
    print("🔐 Loading cookies...")
    cookies = load_cookies()
    print(f"   Loaded {len(cookies)} cookies")
    print()
    
    with sync_playwright() as p:
        # Launch Edge
        print("🌐 Launching Microsoft Edge...")
        browser = p.chromium.launch(
            channel="msedge",
            headless=False  # Visible so you can see it working
        )
        
        # Create context and add cookies
        context = browser.new_context()
        context.add_cookies(cookies)
        
        page = context.new_page()
        
        # Navigate directly to payments page (cookies only work in /o/ section)
        print(f"📍 Navigating to: {ZEFFY_PAYMENTS}")
        print("   (Cookies are only valid in the organization section)")
        page.goto(ZEFFY_PAYMENTS, wait_until='domcontentloaded', timeout=60000)
        
        # Wait for page to fully load (Zeffy is a React app, needs extra time)
        print("⏳ Waiting for page to fully load...")
        page.wait_for_timeout(15000)  # Increased to 15 seconds
        print()
        
        # Wait specifically for the Payments heading to appear
        try:
            page.locator('text=Payments').first.wait_for(state='visible', timeout=15000)
            print("✅ Payments page loaded")
        except:
            print("⚠️  Payments page may not have loaded completely")
        print()
        
        # Check if we need to switch profiles
        print("🔄 Checking organization profile...")
        try:
            # Look for "Jon Schull" text in the profile area
            profile_button = page.locator('text=Jon Schull').first
            profile_button.wait_for(state='visible', timeout=10000)
            print("   Found profile button")
            
            # Check if we see "EcoRestoration Alliance" (without Inc)
            current_org_check = page.locator('text=EcoRestoration Alliance').first
            if current_org_check.is_visible():
                # Check if it's the Inc version
                inc_check = page.locator('text=EcoRestoration Alliance Inc').first
                if not inc_check.is_visible():
                    print("   Current organization: EcoRestoration Alliance (need to switch to Inc)")
                    
                    # Click the profile button
                    print("   Clicking profile button...")
                    profile_button.click()
                    page.wait_for_timeout(2000)
                    
                    # Click "Switch profile"
                    switch_profile = page.locator('text=Switch profile').first
                    print("   Clicking 'Switch profile'...")
                    switch_profile.click()
                    page.wait_for_timeout(2000)
                    
                    # Select "EcoRestoration Alliance Inc"
                    inc_profile = page.locator('text=EcoRestoration Alliance Inc').first
                    print("   Clicking 'EcoRestoration Alliance Inc'...")
                    inc_profile.click()
                    page.wait_for_timeout(5000)  # Wait for page to reload
                    print("✅ Switched to EcoRestoration Alliance Inc")
                else:
                    print("✅ Already on 'EcoRestoration Alliance Inc'")
            else:
                print("⚠️  Could not determine current organization")
        except Exception as e:
            print(f"⚠️  Profile switch failed: {e}")
            import traceback
            traceback.print_exc()
        print()
        
        # Check for signs of authentication
        print("🔍 Checking authentication...")
        
        # Look for common authenticated elements
        if page.locator('text=Sign in').count() > 0:
            print("❌ Appears to be logged OUT (found 'Sign in' button)")
            print("   Cookies may have expired - export fresh cookies")
        elif page.locator('text=Payments').count() > 0 or page.locator('text=Jon Schull').count() > 0:
            print("✅ Appears to be logged IN (found Payments page)")
        else:
            print("⚠️  Authentication status unclear - check screenshot")
        print()
        
        # Click Export button to open dialog
        print("📥 Looking for Export button...")
        try:
            export_button_top = page.locator('text=Export').first
            export_button_top.wait_for(state='visible', timeout=10000)
            print("   Found Export button")
            print("   Clicking Export button (opens dialog)...")
            export_button_top.click()
            page.wait_for_timeout(2000)
            
            # Now click the Export button in the dialog using XPath
            print("   Looking for Export button in dialog...")
            export_button_dialog = page.locator('xpath=/html/body/div[16]/div[3]/div/div[3]/div[2]')
            export_button_dialog.wait_for(state='visible', timeout=5000)
            print("   Found Export button in dialog")
            
            # Set up download handler and click (force=True to bypass overlay)
            with page.expect_download(timeout=60000) as download_info:
                print("   Clicking Export button in dialog...")
                export_button_dialog.click(force=True)
            
            download = download_info.value
            
            # Save the download with correct extension (.xlsx)
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            download_path = SCRIPT_DIR / f"zeffy_payments_{timestamp}.xlsx"
            download.save_as(str(download_path))
            print(f"✅ Downloaded: {download_path}")
            print(f"   File size: {download_path.stat().st_size} bytes")
        except Exception as e:
            print(f"⚠️  Export failed: {e}")
            import traceback
            traceback.print_exc()
        print()
        
        # Take screenshot AFTER page loads
        screenshot_path = SCRIPT_DIR / "zeffy_auth_test.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"📸 Screenshot saved: {screenshot_path}")
        print()
        
        print("✅ Automation complete!")
        print("   Closing browser in 5 seconds...")
        page.wait_for_timeout(5000)
        
        browser.close()
    
    print()
    print("=" * 80)
    print("Test complete!")
    print("=" * 80)

if __name__ == "__main__":
    test_authentication()
