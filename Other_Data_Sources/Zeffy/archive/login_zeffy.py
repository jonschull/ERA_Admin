#!/usr/bin/env python3
"""
Login to Zeffy using Google OAuth with your existing Edge profile.

PATTERN: Persistent Browser Context (uses your actual Edge profile)
SIMPLER THAN: Cookie management - just click through OAuth!

This script:
1. Launches Edge with your actual profile (already logged into Google)
2. Navigates to Zeffy login
3. You click "Log in with Google"
4. You select jschull@gmail.com
5. Script waits for you to complete login
6. Then navigates to payments page
7. Stays open for inspection
"""

from pathlib import Path
from playwright.sync_api import sync_playwright
import time

# Configuration
SCRIPT_DIR = Path(__file__).parent
ZEFFY_LOGIN = "https://www.zeffy.com/login"
ZEFFY_PAYMENTS = "https://www.zeffy.com/en-US/o/campaigns/all-payments"

def login_zeffy():
    """Login to Zeffy using persistent browser context."""
    print("=" * 80)
    print("ZEFFY LOGIN - Using Your Edge Profile")
    print("=" * 80)
    print()
    
    with sync_playwright() as p:
        # Launch Edge with persistent context (your actual profile)
        print("🌐 Launching Microsoft Edge with your profile...")
        print("   This will use your existing Google login")
        print()
        
        # Use your Edge user data directory
        user_data_dir = Path.home() / "Library" / "Application Support" / "Microsoft Edge"
        
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            channel="msedge",
            headless=False,
            args=['--profile-directory=Default']  # Use default profile
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        # Navigate to Zeffy login
        print(f"📍 Navigating to: {ZEFFY_LOGIN}")
        page.goto(ZEFFY_LOGIN, wait_until='domcontentloaded', timeout=60000)
        print()
        
        print("👉 MANUAL STEPS:")
        print("   1. Click 'Log in with Google' button")
        print("   2. Select 'jschull@gmail.com' from the account list")
        print("   3. Wait for login to complete")
        print()
        print("⏳ Waiting for you to complete login...")
        print("   (Script will wait up to 2 minutes)")
        print()
        
        # Wait for user to complete login (check for authenticated page)
        try:
            # Wait for either the payments page or dashboard to appear
            page.wait_for_url("**/o/**", timeout=120000)  # 2 minutes
            print("✅ Login detected! You're now authenticated.")
            print()
        except:
            print("⚠️  Didn't detect automatic redirect - checking manually...")
            print()
        
        # Navigate to payments page
        print(f"📍 Navigating to: {ZEFFY_PAYMENTS}")
        page.goto(ZEFFY_PAYMENTS, wait_until='domcontentloaded', timeout=60000)
        
        # Wait for page to load
        print("⏳ Waiting for page to load...")
        page.wait_for_timeout(5000)
        print()
        
        # Check authentication
        print("🔍 Checking authentication...")
        if page.locator('text=Payments').count() > 0:
            print("✅ Successfully authenticated! Payments page loaded.")
        elif page.locator('text=Log in').count() > 0:
            print("❌ Still on login page - authentication may have failed")
        else:
            print("⚠️  Status unclear - check the browser window")
        print()
        
        # Take screenshot
        screenshot_path = SCRIPT_DIR / "zeffy_logged_in.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"📸 Screenshot saved: {screenshot_path}")
        print()
        
        print("🔍 Browser will stay open indefinitely...")
        print("   Inspect the page and press Ctrl+C when done")
        
        # Wait indefinitely
        try:
            page.wait_for_timeout(3600000)  # 1 hour
        except KeyboardInterrupt:
            print("\n👋 Closing browser...")
        
        context.close()
    
    print()
    print("=" * 80)
    print("Complete!")
    print("=" * 80)

if __name__ == "__main__":
    login_zeffy()
