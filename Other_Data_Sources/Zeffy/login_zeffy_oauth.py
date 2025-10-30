#!/usr/bin/env python3
"""
Login to Zeffy using Google OAuth automation.

PATTERN: OAuth automation with Playwright
SIMPLER THAN: Cookie management!

This script:
1. Launches fresh Edge browser
2. Navigates to Zeffy login
3. Clicks "Log in with Google"
4. YOU manually select jschull@gmail.com
5. After login, extracts cookies
6. Saves cookies for future use
7. Navigates to payments page
"""

from pathlib import Path
from playwright.sync_api import sync_playwright
import json

# Configuration
SCRIPT_DIR = Path(__file__).parent
COOKIE_FILE = SCRIPT_DIR / "zeffy_cookies.json"
ZEFFY_LOGIN = "https://www.zeffy.com/login"
ZEFFY_PAYMENTS = "https://www.zeffy.com/en-US/o/campaigns/all-payments"

def login_and_save_cookies():
    """Login to Zeffy via OAuth and save cookies."""
    print("=" * 80)
    print("ZEFFY OAUTH LOGIN")
    print("=" * 80)
    print()
    
    with sync_playwright() as p:
        # Launch fresh Edge browser with flags to avoid detection
        print("🌐 Launching Microsoft Edge...")
        browser = p.chromium.launch(
            channel="msedge",
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',  # Hide automation
            ]
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        )
        page = context.new_page()
        
        # Remove webdriver flag
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        # Navigate to Zeffy login
        print(f"📍 Navigating to: {ZEFFY_LOGIN}")
        page.goto(ZEFFY_LOGIN, wait_until='domcontentloaded', timeout=60000)
        page.wait_for_timeout(2000)
        print()
        
        # Click "Log in with Google" button
        print("🔘 Clicking 'Log in with Google' button...")
        try:
            google_button = page.locator('text=Log in with Google').first
            google_button.click()
            print("✅ Clicked! Google account selector should appear...")
            print()
        except Exception as e:
            print(f"❌ Could not click button: {e}")
            print("   You may need to click manually")
            print()
        
        print("👉 MANUAL STEPS:")
        print("   1. Select 'jschull@gmail.com' from the account list")
        print("   2. Complete any additional Google auth steps if needed")
        print("   3. Wait for Zeffy dashboard to load")
        print()
        print("⏳ Waiting for you to complete login...")
        print("   (Script will detect when you're authenticated)")
        print()
        
        # Wait for authentication (URL changes to /o/ path)
        try:
            page.wait_for_url("**/o/**", timeout=120000)  # 2 minutes
            print("✅ Login successful! You're now authenticated.")
            print()
        except:
            print("⚠️  Timeout waiting for redirect - checking status...")
            if "/o/" in page.url:
                print("✅ You appear to be logged in!")
            else:
                print("❌ Still on login page - please complete login manually")
            print()
        
        # Extract and save cookies
        print("🍪 Extracting cookies...")
        cookies = context.cookies()
        print(f"   Found {len(cookies)} cookies")
        
        # Backup existing cookies
        if COOKIE_FILE.exists():
            backup_dir = SCRIPT_DIR / "backups"
            backup_dir.mkdir(exist_ok=True)
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"zeffy_cookies_{timestamp}.json"
            with open(COOKIE_FILE, 'r') as f:
                old_cookies = json.load(f)
            with open(backup_file, 'w') as f:
                json.dump(old_cookies, f, indent=2)
            print(f"   Backed up old cookies to: {backup_file}")
        
        # Save new cookies
        with open(COOKIE_FILE, 'w') as f:
            json.dump(cookies, f, indent=2)
        print(f"✅ Saved {len(cookies)} cookies to: {COOKIE_FILE}")
        print()
        
        # Navigate to payments page
        print(f"📍 Navigating to: {ZEFFY_PAYMENTS}")
        page.goto(ZEFFY_PAYMENTS, wait_until='domcontentloaded', timeout=60000)
        page.wait_for_timeout(5000)
        print()
        
        # Check authentication
        print("🔍 Checking payments page...")
        if page.locator('text=Payments').count() > 0:
            print("✅ Successfully authenticated! Payments page loaded.")
        elif page.locator('text=Log in').count() > 0:
            print("❌ Still on login page")
        else:
            print("⚠️  Status unclear - check the browser window")
        print()
        
        # Take screenshot
        screenshot_path = SCRIPT_DIR / "zeffy_logged_in.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"📸 Screenshot saved: {screenshot_path}")
        print()
        
        print("🔍 Browser will stay open for 60 seconds...")
        print("   Inspect the page, then it will close automatically")
        print("   (Press Ctrl+C to close early)")
        
        try:
            page.wait_for_timeout(60000)
        except KeyboardInterrupt:
            print("\n👋 Closing early...")
        
        browser.close()
    
    print()
    print("=" * 80)
    print("Complete! Cookies saved for future automation.")
    print("=" * 80)
    print()
    print("Next: Run sanitize_cookies.py to prepare cookies for automation")

if __name__ == "__main__":
    login_and_save_cookies()
