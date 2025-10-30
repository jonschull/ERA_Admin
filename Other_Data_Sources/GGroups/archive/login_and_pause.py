#!/usr/bin/env python3
"""
Login to Google Groups using cookies and pause for inspection.

Uses Edge browser (not Chrome) and cookie-based authentication.
Based on FathomInventory authentication pattern.
"""

import os
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# Cookies file path
COOKIES_FILE = Path(__file__).parent / 'google_cookies.json'

def load_cookies():
    """Load cookies from google_cookies.json."""
    print("🔍 Loading cookies from google_cookies.json...")
    
    if not COOKIES_FILE.exists():
        print(f"❌ Cookie file not found: {COOKIES_FILE}")
        print("\nTo create cookies file:")
        print("1. Log into groups.google.com in Edge browser")
        print("2. Open Developer Tools (F12)")
        print("3. Go to Application > Cookies")
        print("4. Export cookies as JSON array")
        print("5. Save as google_cookies.json")
        return None
    
    try:
        with open(COOKIES_FILE, 'r') as f:
            cookies = json.load(f)
        
        if not isinstance(cookies, list):
            print("❌ google_cookies.json should contain an array of cookies")
            return None
        
        print(f"✅ Loaded {len(cookies)} cookies")
        return cookies
        
    except json.JSONDecodeError:
        print("❌ google_cookies.json is not valid JSON")
        return None
    except Exception as e:
        print(f"❌ Error reading cookies: {e}")
        return None

def sanitize_cookies(cookies):
    """Sanitize cookies for Playwright compatibility."""
    print("🧹 Sanitizing cookies for Playwright...")
    
    valid_same_site_values = {'Strict', 'Lax', 'None'}
    sanitized_count = 0
    
    for cookie in cookies:
        # Fix sameSite values
        if cookie.get('sameSite') not in valid_same_site_values:
            cookie['sameSite'] = 'Lax'
            sanitized_count += 1
        
        # Remove problematic partitionKey
        if 'partitionKey' in cookie and not isinstance(cookie.get('partitionKey'), str):
            del cookie['partitionKey']
            sanitized_count += 1
    
    if sanitized_count > 0:
        print(f"🔧 Sanitized {sanitized_count} cookie attributes")
    else:
        print("✅ No cookie sanitization needed")
    
    return cookies

async def login_and_pause():
    """Login to Google Groups and pause for inspection."""
    print("\n" + "=" * 60)
    print("🌐 GOOGLE GROUPS LOGIN")
    print("=" * 60)
    
    # Load cookies
    cookies = load_cookies()
    if not cookies:
        return False
    
    try:
        async with async_playwright() as p:
            # Launch browser (exactly like Fathom example)
            print("\n🚀 Launching browser...")
            browser = await p.chromium.launch(
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',  # Hide automation
                ]
            )
            
            # Create context with realistic user agent
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='en-US',
            )
            
            # Add cookies to context (exactly like Fathom)
            sanitized_cookies = sanitize_cookies(cookies.copy())
            await context.add_cookies(sanitized_cookies)
            
            # Create page and navigate
            page = await context.new_page()
            print("🔄 Navigating to Google Groups...")
            
            try:
                # Navigate to Google Groups home
                await page.goto("https://groups.google.com/", timeout=30000)
                await page.wait_for_load_state('networkidle', timeout=15000)
                
                # Check if we're logged in
                title = await page.title()
                print(f"📄 Page title: {title}")
                
                # Look for login indicators
                login_button = await page.query_selector('a[href*="accounts.google.com"], button:has-text("Sign in")')
                if login_button:
                    print("⚠️  Detected login button - cookies may be expired")
                    print("   But browser is open - you can inspect the page")
                else:
                    print("✅ Appears to be logged in (no login button detected)")
                
                # Look for user menu/account indicator
                user_menu = await page.query_selector('[aria-label*="Account"], [aria-label*="Google Account"]')
                if user_menu:
                    print("✅ Found user account menu - authentication successful!")
                
                # Pause for inspection
                print("\n" + "=" * 60)
                print("⏸️  BROWSER PAUSED FOR INSPECTION")
                print("=" * 60)
                print("\nThe browser will stay open until you:")
                print("  1. Inspect the page")
                print("  2. Verify authentication status")
                print("  3. Press Ctrl+C in this terminal to close")
                print("\n" + "=" * 60)
                
                # Keep browser open indefinitely
                while True:
                    await asyncio.sleep(1)
                
            except KeyboardInterrupt:
                print("\n\n✅ Browser session ended by user")
                return True
            except Exception as nav_error:
                print(f"❌ Navigation error: {nav_error}")
                print("\nBrowser will stay open for inspection...")
                print("Press Ctrl+C to close")
                
                # Keep browser open even on error
                try:
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    print("\n\n✅ Browser session ended by user")
                    return False
            
            finally:
                await browser.close()
            
    except Exception as e:
        print(f"❌ Browser launch error: {e}")
        return False

async def main():
    """Main entry point."""
    try:
        await login_and_pause()
    except KeyboardInterrupt:
        print("\n\n✅ Exiting...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
